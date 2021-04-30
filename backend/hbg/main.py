#!/usr/bin/env python
import os, sys, urllib, logging, uvicorn
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from .config import Settings
settings = Settings()

from hbg.db.mongo import client, db
from hbg.models import user
from hbg.logging import logger

settings = Settings()
settings.checkEnvs()  # this will check the environment
settings.authjwt_secret_key = os.environ['SECRET_KEY']
app = FastAPI()
app.include_router(user.router, prefix="/user")

@AuthJWT.load_config
def get_config():
    return settings

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = db
    logger.info(f"Starting up! Connecting to database {os.environ['MONGODB']}")

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down, closing database connection...")
    client.close()

@app.get("/")
async def root():
    return { "message": "Hello there!"}

@app.get("/api/{id}")
async def getAPIID(id: int, q: Optional[str] = None, short: Optional[bool] = False ):
    return { 
            "id": id,
            "q": q,
            "short": short
          }
