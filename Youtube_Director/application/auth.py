import jwt
import datetime
import hashlib


SECRET = "redacted"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(provided_password, stored_password):
    return hash_password(provided_password) == stored_password

def generate_token(username, role):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')