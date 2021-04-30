from mongoengine import *
from flask import current_app as app
from datetime import datetime, timedelta
from random import randint
import re

def checkName(val):
    if val == '':
        raise ValidationError("Value cannot be empty")

    # now we specifically block the following characters between brackets:
    if re.search('[0-9`~!@#$%^&*()|+=?;:",.<>{}[\]/]', val):
        app.logger.debug(f'incorrect char: {val}')
        raise ValidationError("Value cannot contain special chars")

class Session(Document):
    sessionId = UUIDField(unique=True)
    expiration = DateTimeField(required=True,default = datetime.now() + timedelta(hours=2))
    ipaddress = StringField(required=True, unique = False, max_length=39)   # to accomodate for IPv4 and IPv6
    userAgent = StringField(required=True, unique= False)
    host = StringField(required=True, unique=False, max_length=200)
    loggedIn = BooleanField(required=True, unique=False, default=False)
    username = StringField(required=False, unique=False, max_length=320, default="")
    userRef = ReferenceField('User', required=False);

class User(Document):
    title = StringField(max_length=60)
    firstname = StringField(unique = False, max_length=50, required=True, validation=checkName)
    lastname = StringField(unique = False, max_length=100, required=True, validation=checkName)
    createdDate = DateTimeField(required=True, default=datetime.now)
    username = StringField(unique = True, max_length=320, required=True)
    password = StringField(unique = False, max_length=500, required=True)
    email = EmailField(unique = True, max_length=320, required=True)
    validatedEmail = BooleanField(required=True, default=False)
    validationCode = IntField(unique=False, required=True, default = randint(10000,99999))
    failedLogins = IntField(unique=False, required=True, default=0)
    active = BooleanField(required=True, default=True)

class Reset(Document):
    userRef = ReferenceField('User', required=True);
    username = StringField(required=False, unique=False, max_length=320, default="")
    resetCode = StringField(unique=False, required=True, unique_with = 'username' )


