
import uuid
import jwt
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.auth.models import RefreshToken
from app.core.settings import settings
from app.security.jwt import create_access_jwt, create_refresh_jwt, verify_jwt_token
from app.security.pw_hashing import  verify_pw
from app.auth.schemas import UserLoginSchema, UserSuccessLoginTokensSchema, RefreshTokenRequestSchema, RefreshedAccessTokenSchema
from app.auth.exceptions import InvalidCredentialsError, InvalidRefreshToken 

from app.security.refresh_token import generate_refresh_token, hash_refresh_token
from app.users.models import User


async def login_service(form_data: UserLoginSchema, db: AsyncSession) -> UserSuccessLoginTokensSchema:
    """
    Take pydantic form.  
    Check the password with DB password.  
    Generate `access token` and `refresh token`. 

    The refresh_token is a UUID, we hash it for DB.

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

    # create the access token: 
    access_token: str = create_access_jwt(user_id=existing_user.id)

    # create refresh_token in tables for future checks 
    refresh_token: str = generate_refresh_token()

    hashed_refresh_token: str = hash_refresh_token(refresh_token=refresh_token)
    family_id: uuid.UUID = uuid.uuid4()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=settings.jwt_refresh_token_expire_days)
    family_expires_at = now + timedelta(days=settings.refresh_token_absolute_days)


    new_entry_refresh_token = RefreshToken(
            refresh_token_hash = hashed_refresh_token,
            is_active=True,
            expires_at=expires_at,
            family_id=family_id,
            family_expires_at=family_expires_at,
            user_id=existing_user.id,
            )
    db.add(new_entry_refresh_token)
    await db.commit()

    # for UserSuccessLoginTokensSchema:
    expires_in = settings.jwt_access_token_expire_minutes * 60 # in SECONDS 

    return UserSuccessLoginTokensSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
                token_type='Bearer'
                )



async def refresh_service(refresh_token: RefreshTokenRequestSchema, db: AsyncSession) -> UserSuccessLoginTokensSchema:
    """
    Take a refresh_token from client, check all and give new tokens (access+refresh) for next time.

    Args:
        - refresh_token: RefreshTokenRequestSchema -> uuid str represent the token 
        - db: AsyncSession
    Returns:
        - UserSuccessLoginTokensSchema: new_refresh_token + new_access_token 
    Errors:
        - InvalidRefreshToken
    
    Checks:
        - if refresh_token exist in DB 
        - if refresh_token is inactive 
        - if refresh_token expirations are ok 
    """

    # 1
    hashed_refresh_token: str = hash_refresh_token(refresh_token.refresh_token)

    # je regarde si le refresh_token exist en DB:
    res = await db.execute(select(RefreshToken).where(RefreshToken.refresh_token_hash == hashed_refresh_token))
    existing_refresh_token = res.scalar_one_or_none()
    if not existing_refresh_token:
        raise InvalidRefreshToken

    # Si le token est no_active: on met TOUTE la family en inactive 
    if existing_refresh_token.is_active == False:
        await db.execute(
                update(RefreshToken)
                .where(RefreshToken.family_id == existing_refresh_token.family_id)
                .values(is_active=False)
                )
        await db.commit()
        raise InvalidRefreshToken 

    # Verifie si les expirations sont passees ou non:
    now = datetime.now(timezone.utc) 
    if existing_refresh_token.expires_at < now or existing_refresh_token.family_expires_at < now: 
        raise InvalidRefreshToken

    # On va mettre le refresh token en DB sur inactive car on le consomme
    # on check l'id en meme temps le status active pour eviter une double requete 
    consumed = await db.execute(
            update(RefreshToken)
            .where(
                RefreshToken.id == existing_refresh_token.id,
                RefreshToken.is_active.is_(True),
                )
            .values(is_active=False)
            .returning(RefreshToken.id)
            )
    if consumed.scalar_one_or_none() is None:
        # si jamais consumed a pas marcher ca veut dire que c'etait DEJA sur inactive. donc on desactive a nouveau la famille entiere
        await db.execute(
                update(RefreshToken)
                .where(RefreshToken.family_id == existing_refresh_token.family_id)
                .values(is_active=False)
                )
        await db.commit()
        raise InvalidRefreshToken

    # creer access token 
    new_access_token = create_access_jwt(user_id=existing_refresh_token.user_id) 

    # creer refresh token 
    new_refresh_token = generate_refresh_token() 
    new_entry_refresh_token = RefreshToken(
            refresh_token_hash=hash_refresh_token(new_refresh_token),
            is_active=True,
            expires_at=now + timedelta(days=settings.jwt_refresh_token_expire_days),
            family_id=existing_refresh_token.family_id,
            family_expires_at=existing_refresh_token.family_expires_at,
            user_id=existing_refresh_token.user_id,
            )
    db.add(new_entry_refresh_token)
    await db.commit()
    
    return UserSuccessLoginTokensSchema(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.jwt_access_token_expire_minutes * 60,
            token_type='Bearer',
            )











