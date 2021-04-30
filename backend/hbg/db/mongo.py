import os
from motor.motor_asyncio import *
from pymongo.errors import *

client = AsyncIOMotorClient(os.environ["MONGODBSRV"], connect = True)
db = client[os.environ["MONGODB"]]
userCollection = "users"

def catchMongoExceptions(func):
    def catchExceptions(*args, **kwargs):
        answer = {
            'message': 'Unknown error',
            'status': 400
        }
        try:
            return func(*args, **kwargs)
        except BadRequest as msg:
            answer['message'] = 'Bad request'
            answer['reason'] = str(msg)
        except ValidationError as e:
            logger.warning(f"Provided data incorrect: {str(e)}")
            answer['message'] = f"Provided data incorrect"
        except KeyError as e:
            logger.warning(f"Value does not exist in request: {str(e)}")
            answer['message'] = f"Mandatory field is missing: {str(e)}"
        except DuplicateKeyError as e:
            logger.warning(f"Duplicate key in database")
        except Exception as e:
            answer['status'] = 500
            answer['message'] = 'Incorrect request received'
            logger.error(f"Something went wrong: {str(e)}")

        return make_response(jsonify(answer), answer['status'] )
    catchExceptions.__name__ = func.__name__
    return catchExceptions