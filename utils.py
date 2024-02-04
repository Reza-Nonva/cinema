import hashlib

def validating_email(email):
    return True

def validating_username(username):
    return True

def validating_password(password):
    return True

def validating_mobile_number(mobile_number):
    return True

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_hashed_password(entered_password, stored_hashed_password):
    hashlib.sha256(entered_password.encode()).hexdigest() == stored_hashed_password
    