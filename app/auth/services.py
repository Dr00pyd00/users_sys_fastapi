import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.settings import settings
from app.security.jwt import create_access_jwt, create_refresh_jwt, verify_jwt_token
from app.security.pw_hashing import  verify_pw
from app.auth.schemas import UserLoginSchema, UserSuccessLoginTokensSchema, RefreshTokenRequestSchema, RefreshedAccessTokenSchema
from app.auth.exceptions import InvalidCredentialsError, InvalidRefreshToken 

from app.users.models import User


async def login_service(form_data: UserLoginSchema, db: AsyncSession) -> UserSuccessLoginTokensSchema:
    """
    Take pydantic form.  
    Check the password with DB password.  
    Generate `access token` and `refresh token`. 

    Args: 
        - `UserLoginSchema`: email + password 
        - `db`: async db 
    Returns:
        - UserSuccessLoginTokensSchema: access_token, refresh_token, expires_in, token_type
    Errors: 
        - InvalidCredentialsError: if passwords not match.
    """
    # check if user exist
    res = await db.execute(select(User).where(User.email == form_data.email)) 
    existing_user = res.scalar_one_or_none()
    if existing_user is None: 
        raise InvalidCredentialsError

    # check pw 
    good_pw = verify_pw(plain_pw=form_data.password, db_hashed_pw=existing_user.hashed_password)
    if not good_pw:
        raise InvalidCredentialsError

    # create the tokens: 
    access_token = create_access_jwt(existing_user.id)
    refresh_token = create_refresh_jwt(existing_user.id)
    expires_in = settings.jwt_access_token_expire_minutes * 60 # in SECONDS 

    return UserSuccessLoginTokensSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                token_type='Bearer'
                )


async def refresh_simple_service(refresh_token: RefreshTokenRequestSchema, db: AsyncSession) -> RefreshedAccessTokenSchema:
    """
        Take a refresh_token, check if all is valid them return a RefreshedAccessTokenSchema: a new_access_token.

        Args:
            - refresh_token: `RefreshTokenRequestSchema` -> from frontend 
            - db: asyncsession 
        Returns:
            - RefreshedAccessTokenSchema: access_token, expires_in, token_type.
        Errors:
            - InvalidRefreshToken 
    """
    try:
        payload = verify_jwt_token(token=refresh_token.refresh_token)
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError): 
        raise InvalidRefreshToken

    if payload.get('token_type') != 'refresh_token':
        raise InvalidRefreshToken 

    user_id = payload.get('sub')
    if user_id is None:
        raise InvalidRefreshToken
    
    res = await db.execute(select(User).where(User.id == int(user_id)))
    user = res.scalar_one_or_none()
    if user is None:
        raise InvalidRefreshToken 

    new_access_token = create_access_jwt(user.id) 
    expires_in = settings.jwt_access_token_expire_minutes * 60 # in SECONDS 

    return RefreshedAccessTokenSchema(
                access_token=new_access_token,
                expires_in=expires_in,
                token_type='Bearer',
                )
    








