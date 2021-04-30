from bson import ObjectId
import re

def checkName(val):
    if val == '':
        raise ValidationError("Value cannot be empty")

    # now we specifically block the following characters between brackets:
    if re.search('[0-9`~!@#$%^&*()|+=?;:",.<>{}[\]/]', val):
        app.logger.debug(f'incorrect char: {val}')
        raise ValidationError("Value cannot contain special chars")

def passwordStrengthOK(password):
    # Strength Checks
    charRegex = re.compile(r'(\w{8,})')  # Check if password has at least 8 characters
    lowerRegex = re.compile(r'[a-z]+') # Check if at least one lowercase letter
    upperRegex = re.compile(r'[A-Z]+')# Check if atleast one upper case letter
    digitRegex = re.compile(r'[0-9]+') # Check if at least one digit.
    specialRegex = re.compile(r'[`~!@#$%^&*()|+=?;:",.<>{}[\]/]+') # Check if at least one special character.

    ''' TODO: Enter conditions to see if password passes all checks and then return
    a message if it does.'''
    if charRegex.findall(password) == []:  # Checks if the password does not contain 8 characters and returns a message
        return False
    elif lowerRegex.findall(password)==[]: # Checks if the password does not contain a lowercase character and returns a message
        return False
    elif upperRegex.findall(password)==[]: # Checks if the password does not contain an uppercase character and returns a message
        return False
    elif digitRegex.findall(password)==[]: # Checks if the password does not contain a digit character and returns a message
        return False
    elif specialRegex.findall(password)==[]: # Checks if the password does not contain a digit character and returns a message
        return False
    else:  # if the above 4 conditions are successfully passed, password is strong enough
        return True

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")