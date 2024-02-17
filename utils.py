import re
import hashlib
import time

def validating_email(email):
    """
        a function for validatning email when register a user
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        return True
    return False

def validating_username(username):
    """
        a function for validating username when register a user
    """
    username_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{1,100}$'

    if re.match(username_regex, username):
        return True
    return False

def validating_password(password):
    """
        a function for validation password when register user or change password
    """
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=(.*[@#$]){2,})[a-zA-Z\d@#$]{8,}$'

    if re.match(password_regex, password):
        return True
    return False

def validating_mobile_number(mobile_number):
    """"
        a function for validating phone number when register a user or change phone number
    """
    mobile_regex = r'^09\d{9}$'

    if re.match(mobile_regex, mobile_number):
        return True
    return False

def hash_password(password):
    """
        a func for hashing password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def card_number_check(card_number):
    """
        a fucntion for checking card number validity
    """
    sum = 0
    for i in range(len(card_number)):
        if (i+1) % 2 == 0:
            result = int(card_number[i]) * 1
        else:
            if (int(card_number[i]) * 2) > 9:
                result = (int(card_number[i]) * 2) - 9
            else:
                result = int(card_number[i]) * 2
        sum += result

    if sum % 10 == 0 and len(card_number) == 16:
        return True
    else:
        return False


def payment_code_hash():
    """
        a func for create unqiue hash for payment code by timestamp
    """
    return hash(time.time())
