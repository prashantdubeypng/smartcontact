import jwt
from datetime import datetime, timedelta
from django.conf import settings

# You can set these in settings.py
JWT_SECRET = 'amit@2026'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

def generate_jwt(payload):
    """
    Generates a JWT token with expiration
    """
    payload['exp'] = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token):
    """
    Decodes the JWT token and returns payload if valid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')
