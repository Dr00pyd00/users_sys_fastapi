
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status 

from app.core.database import get_db
from app.auth.schemas import UserLoginSchema, UserSuccessLoginTokensSchema, RefreshTokenRequestSchema
from app.auth.services import login_service, refresh_service

from app.users.services import create_user_service 
from app.users.schemas import   UserCreationFormSchema, UserClientDisplaySchema
from app.users.exceptions import EmailAlreadyTakenError, UsernameAlreadyTakenError 
from app.auth.exceptions import  InvalidRefreshToken, InvalidCredentialsError


router = APIRouter(
        prefix='/auth',
        tags=['authentication'],
        )


@router.post(
        '/register', 
        response_model=UserClientDisplaySchema,
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
    except InvalidCredentialsError:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid Credentials',
                )

    return tokens



@router.post(
        '/refresh',
        response_model=UserSuccessLoginTokensSchema,
        status_code=status.HTTP_200_OK,
        )
async def refresh(
        refresh_token: RefreshTokenRequestSchema,
        db: Annotated[AsyncSession, Depends(get_db)],
        ):
    try:
        tokens = await refresh_service(
                refresh_token=refresh_token,
                db=db,
                )
    except InvalidRefreshToken:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token',
                )
    return tokens




        

