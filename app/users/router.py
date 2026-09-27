"""
    - 401_Unauthorized = je ne sais pas qui c'est / identifiants Invalids 
    - 403_Forbidden = je sais qui tu es mais tu n'as pas le droit
""" 

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status 

from app.users.models import User
from app.dependencies.database import get_db
from app.dependencies.users import get_current_user
from app.users.exceptions import EmailAlreadyTakenError, InvalidCredentialsError, InvalidRefreshToken, UsernameAlreadyTakenError 
from app.users.schemas import RefreshTokenRequestSchema, RefreshedAccessTokenSchema, UserCreationFormSchema, UserClientDisplaySchema, UserLoginSchema, UserSuccessLoginTokensSchema
from app.users.services import create_user_service, login_service, refresh_simple_service 

router = APIRouter(
        prefix='/users',
        tags=['Users'],
        # TODO dependencies et responses ici en args ? 
        )


@router.get(
        '/me',
        response_model=UserClientDisplaySchema,
        status_code=status.HTTP_200_OK,
        )
async def get_me(
        current_user: Annotated[User, Depends(get_current_user)],
        ):
    return current_user 




@router.post(
        '/register', 
        response_model=UserClientDisplaySchema, # type:ignore
        status_code=status.HTTP_201_CREATED,
        )
async def create_user(
        form_data: UserCreationFormSchema,
        db: Annotated[AsyncSession, Depends(get_db)],
        ):
    try:
        user = await create_user_service(form_data=form_data, db=db)
    except UsernameAlreadyTakenError:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Username already taken',
                )
    except EmailAlreadyTakenError:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email already taken',
                )
    return user



@router.post(
        '/login',
        response_model=UserSuccessLoginTokensSchema,
        status_code=status.HTTP_200_OK,
        )
async def login_user(
        form_data: UserLoginSchema,
        db: Annotated[AsyncSession, Depends(get_db)],
        ):
    try:
        tokens = await login_service(
                form_data=form_data,
                db=db,
                )
    except InvalidCredentialsError as e:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid Credentials',
                )

    return tokens



@router.post(
        '/refresh_simple',
        response_model= RefreshedAccessTokenSchema,
        status_code=status.HTTP_200_OK,
        )
async def refresh_simple(
        refresh_token: RefreshTokenRequestSchema,
        db: Annotated[AsyncSession, Depends(get_db)],
        ):
    try:
        tokens = await refresh_simple_service(refresh_token=refresh_token, db=db)
    except InvalidRefreshToken:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token',
                )
    return tokens 


        

