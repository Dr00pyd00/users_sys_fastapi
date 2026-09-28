"""
    - 401_Unauthorized = je ne sais pas qui c'est / identifiants Invalids 
    - 403_Forbidden = je sais qui tu es mais tu n'as pas le droit
""" 

from typing import Annotated

from fastapi import APIRouter, Depends 
from starlette import status 

from app.users.models import User
from app.auth.dependencies import get_current_user
from app.users.schemas import   UserClientDisplaySchema

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




