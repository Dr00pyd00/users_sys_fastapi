
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.security.jwt import verify_jwt_token
from app.users.models import User

"""
    HTTPBearer: agit comme une dependance
- Parsing du Header 
- Verifie le format bearer 
- leve 403 error si absent ou mal fait 

    il return HTTPAuthorizationCredentials object qui contient:
        - credentials.scheme = 'Bearer' ( type de token ) 
        - credentials.credentials = le token lui meme 
"""
bearer_scheme = HTTPBearer() 

async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
        db: Annotated[AsyncSession, Depends(get_db)],
        ):
    """
        Dependance for get the current User or HTTPException.

        Args:
            - `credentials`: HTTPAuthorizationCredentials object containt token type and token
            - `db`: async session DB 
        Returns:
            - The user 
        Errors:
            - HTTPException HTTP_401_UNAUTHORIZED 
    """ 

    token = credentials.credentials
    
    try:
        payload = verify_jwt_token(token=token)
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='token expired',
                )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='token error',
                )
    user_id = payload.get('sub')
    if user_id is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token payload',
                )
    res = await db.execute(select(User).where(User.id == int(user_id)))
    user = res.scalar_one_or_none()
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User does not exist',
                )
    return user 
    


