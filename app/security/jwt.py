

from datetime import datetime, timedelta, timezone 
import uuid

import jwt

from app.core.settings import settings
from app.users.models import User

def create_access_jwt(user: User, duration: int = 15):
    """
    Create a new jwt ACCESS token with:
        - `expiration`: 15 min
        - `payload` contain:
            - sud (user_id i-e)
            - exp (total life time of token)
            - iat (timestamp creation of token)
            - jti (id of the token) 
            - token_type ('access_token' i-e) 

    Args:
        - user : User object
        - duration: int -> live token duration in MINUTES. Default=15 
    Return:
        - Access Token (str)
    """
    now = datetime.now(timezone.utc)
    token_duration = timedelta(minutes=duration) 
    payload = {
            'sub': str(user.id),
            'exp': now + token_duration,
            'iat': now,
            'jti': str(uuid.uuid4()),
            'token_type':'access_token',
            }
    encoded_token = jwt.encode(
            payload=payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
            )
    return encoded_token 


def create_refresh_jwt(user: User, duration: int = 7):
    """
    Create a new jwt REFRESH token with:
        - `expiration`: 7 days
        - `payload` contain:
            - sud (user_id i-e)
            - exp (total life time of token)
            - iat (timestamp creation of token)
            - jti (id of the token) 
            - token_type ('refresh_token' i-e) 

    Args:
        - user : User object
        - duration: int -> live token duration in DAYS. Default=7 
    Return:
        - Refresh Token (str)
    """
    now = datetime.now(timezone.utc)
    token_duration = timedelta(days=duration) 
    payload = {
            'sub': str(user.id),
            'exp': now + token_duration,
            'iat': now,
            'jti': str(uuid.uuid4()),
            'token_type':'refresh_token',
            }
    encoded_token = jwt.encode(
            payload=payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
            )
    return encoded_token 


def verify_jwt_token(token: str):
    """
    Take a jwt token and verify if valid.

    Args:
        - token: jwt (str)
    Return:
        - `the token payload'
    Errors:
        - `jwt.ExpiredSignatureError` : if token expired 
        - `jwt.InvalidTokenError`: others problems like invalid user/ invalid secret etc...
    """
    payload = jwt.decode(
                jwt=token,
                key=settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
                )
    return payload 



