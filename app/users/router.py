
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status 

from app.dependencies.database import get_db
from app.users.exceptions import EmailAlreadyTakenError, UsernameAlreadyTakenError 
from app.users.schemas import UserCreationFormSchema, UserClientDisplaySchema
from app.users.services import create_user_service 

router = APIRouter(
        prefix='/users',
        tags=['Users'],
        # TODO dependencies et responses ici en args ? 
        )


@router.post(
        '/', 
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

