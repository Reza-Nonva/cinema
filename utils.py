import re
import hashlib


def validating_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_regex, email):
        return True
    return False

def validating_username(username):
    username_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{1,100}$'

    if re.match(username_regex, username):
        return True
    return False

def validating_password(password):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=(.*[@#$]){2,})[a-zA-Z\d@#$]{8,}$'

    if re.match(password_regex, password):
        return True
    return False

def validating_mobile_number(mobile_number):
    mobile_regex = r'^09\d{9}$'

    if re.match(mobile_regex, mobile_number):
        return True
    return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_hashed_password(entered_password, stored_hashed_password):
    hashlib.sha256(entered_password.encode()).hexdigest() == stored_hashed_password
    