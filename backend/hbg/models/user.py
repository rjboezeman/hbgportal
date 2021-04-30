
import os
from fastapi import FastAPI, APIRouter, Body, status, HTTPException, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timedelta
from bson import ObjectId
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from pymongo.errors import *
from random import randint

from fastapi_jwt_auth.exceptions import JWTDecodeError

from hbg.config import Settings
from hbg.models.utils import PyObjectId, checkName, passwordStrengthOK
#from hbg.models.oauth2passwordbearerwithcookie import OAuth2PasswordBearerWithCookie
from hbg.db.mongo import db, userCollection
from hbg.logging import logger

settings = Settings()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
#oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/user/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError as e:
        logger.error(f"Password is not a {settings.ALGORITHM} hash")
        return False

def get_password_hash(password):
        return pwd_context.hash(password)

class UserBaseModel(BaseModel):
    title: str = Field(None)
    firstname: str = Field(...)
    lastname: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    comment: str = Field(None)

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}
            schema_extra = {
                    "example": {
                            "firstname": "Jane Doe",
                            "lastname": "Jane Doe",
                            "username": "jdoe@example.com",
                            "email": "jdoe@example.com",
                            "comment": "A basic user"
                    }
            }

class UserCreateBaseModel(UserBaseModel):
    password: str = Field(...)

class UserDbModel(UserBaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_date: datetime = Field(datetime.utcnow())
    password: str = Field(...)
    validated_email: bool = Field(False)
    validation_code: int = Field(randint(10000,99999))
    last_login: datetime = Field(None)
    last_failed_login: datetime = Field(None)
    failed_logins: int = Field(0)
    active: bool = Field(False)

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}


class LoginModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class UpdateUserBaseModel(UserBaseModel):
    title: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    comment: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
                "example": {
                "title": "Mr",
                "firstname": "John",
                "lastname": "Doe",
                "email": "rj@boezeman.net",
                "username": "rj@boezeman.net",
                "password": "1234"
            }
        }

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        to_encode.update({"domain": "localhost.boezeman.net"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.debug(f"encoded_jwt: {encoded_jwt}")
        return encoded_jwt

@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends() ):
    try:
        userDb = await db[userCollection].find_one({"username": form_data.username})
        if userDb is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            if userDb["failed_logins"] >= settings.MAX_LOGIN_ATTEMPTS:
                logger.warning(f"User {form_data.username} blocked, too many failed login attempts ({settings.MAX_LOGIN_ATTEMPTS})")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Too many password attempts, account blocked temporarily")
            if verify_password(form_data.password, userDb["password"]):
                await db[userCollection].update_one({"username": form_data.username}, { "$set": { "failed_logins": 0, "last_login": datetime.utcnow() }} )
                
                # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                # access_token = create_access_token(
                #     data={"username": form_data.username}, expires_delta=access_token_expires
                # )
                # Create the tokens and passing to set_access_cookies or set_refresh_cookies
                access_token = Authorize.create_access_token(subject=form_data.username)
                #refresh_token = Authorize.create_refresh_token(subject=form_data.username)
                response = JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Login successful"})
                Authorize.set_access_cookies(access_token, response)
                #Authorize.set_refresh_cookies(refresh_token, response)
                return response
            else:
                updateResult = await db[userCollection].update_one({"username": form_data.username}, {"$inc": { "failed_logins": 1 }, "$set": { "last_failed_login": datetime.utcnow()} })
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except PyMongoError as e:
        logger.error(f"Unknown database error ({str(type(e).__name__)}): {str(e)}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={ "detail": f"Sorry, service unavailable" })    
        user = UserInDB(**user_dict)
        hashed_password = fake_hash_password(form_data.password)
        if not hashed_password == user.hashed_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

# @router.post('/refresh')
# def refresh(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_refresh_token_required()

#     current_user = Authorize.get_jwt_subject()
#     new_access_token = Authorize.create_access_token(subject=current_user)
#     # Set the JWT cookies in the response
#     response = JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "The token has been refreshed"})
#     Authorize.set_access_cookies(new_access_token, response)
#     return response

async def get_current_user(request: Request, Authorize: AuthJWT = Depends()):
        credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            #payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            #logger.info(f"payload: {str(payload)}")
            #username: str = payload.get("username")
            Authorize.jwt_required(auth_from=request)
            logger.info(f"We did get here though: {str(request.cookies)}")
            username = Authorize.get_jwt_subject() ### CONTINUE HERE!! It returns None...
            logger.info(f"Username: {username}")
            if username is None:
                raise credentials_exception
            user = await db[userCollection].find_one({"username": username})
            if user is None:
                logger.warning(f"Token with unknown username: {username}")
                raise credentials_exception
            # user.pop('password', None), no longer needed
            return UserDbModel(**user)
        except jwt.ExpiredSignatureError as e:
            logger.warning(f"Token has expired: {str(e)}")
            raise credentials_exception
        except JWTError as e:
            logger.error(f"JWT token could not be decoded: {str(e)}")
            raise credentials_exception
        except PyMongoError as e:
            logger.error(f"Unknown database error ({str(type(e).__name__)}): {str(e)}")
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={ "detail": f"Sorry, service unavailable" })

async def get_current_active_user(current_user: UserDbModel = Depends(get_current_user)):
        if not current_user.active:
                raise HTTPException(status_code=400, detail="User is inactive")
        return current_user

@router.post("/create", response_description="Add new user", response_model=UserBaseModel)
async def create_user(user: UserCreateBaseModel = Body(...)):
    try:
        userIn = jsonable_encoder(user)
        userDb = UserDbModel(**(userIn))
        userDb.password = get_password_hash(user.password)
        newUser = await db[userCollection].insert_one(userDb.dict())
        logger.warning(f"New user: {str(userDb.dict())}")
        createdUser = await db[userCollection].find_one({"_id": newUser.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={ "detail": f"User {userIn['username']} created" })
    except DuplicateKeyError as e:
        logger.error(f"User already exists: {str(userIn['username'])}")
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={ "detail": f"User already exists", "username": userIn["username"] })
    except PyMongoError as e:
        logger.error(f"Unknown error ({str(type(e).__name__)}): {str(e)}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={ "detail": f"Bad request", "username": userIn["username"] })        

@router.put("/update", response_description="Update a user", response_model=UserBaseModel)
async def update_user(user: UpdateUserBaseModel = Body(...)):
    try:
        userIn = { k:v for k,v in user.dict().items() if v is not None}
        if "password" in userIn:
            if passwordStrengthOK(userIn['password']):
                userIn["password"] = get_password_hash(userIn['password']) 
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": f"Your password is not strong enough"})
        if len(userIn) >=1:
            updateResult = await db[userCollection].update_one({"username": userIn['username']}, {"$set": userIn})
            if updateResult is not None:
                if updateResult.modified_count == 1:
                    return JSONResponse(status_code=status.HTTP_200_OK, content={ "detail": f"User {userIn['username']} updated"})
        raise HTTPException(status_code=404, detail=f"User {userIn['username']} not found")
    except PyMongoError as e:
        logger.error(f"Unknown database error ({str(type(e).__name__)}): {str(e)}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={ "detail": f"Sorry, service unavailable" })


# @router.delete("/{id}", response_description="Delete a user")
# async def delete_user(id: str):
#     delete_result = await db[userCollection].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"user {id} not found")

@router.get("/me", response_model=UserBaseModel)
async def read_users_me(current_user: UserBaseModel = Depends(get_current_active_user)):
    return current_user

@router.get(
    "/{username}", response_description="Get a single user", response_model=UserBaseModel
)
async def get_user(username: str):
    try:
        user = await db[userCollection].find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=404, detail=f"User {username} not found")
        else:
            ret_user = {
                "username": user['username'],
                "firstname": user['firstname'],
                "lastname": user['lastname'],
                "email": user['email']
            }
            return JSONResponse(status_code=status.HTTP_200_OK, content=ret_user)
    except PyMongoError as e:
        logger.error(f"Unknown database error ({str(type(e).__name__)}): {str(e)}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={ "detail": f"Sorry, service unavailable" })

@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}