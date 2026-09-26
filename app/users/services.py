
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_ 

from app.security.pw_hashing import hash_pw
from app.users.exceptions import EmailAlreadyTakenError, UsernameAlreadyTakenError
from app.users.models import User
from app.users.schemas import UserCreationFormSchema


async def create_user_service(form_data: UserCreationFormSchema, db: AsyncSession):
    """
    Take pydantic validation form,
    hash the password and put data in db. 
    
    Conditions:
        - Unique email
        - Unique username ( optional field )

    Args:
        - form_data: pydantic model for user creation 
        - db: async session 
    Return: 
        - the User created object 
    Errors: 
        - `EmailAlreadyTakenError`: if email already exist in db 
        - `UsernameAlreadyTakenError`: if username already exist in db
    """
    conditions = [User.email==form_data.email]
    if form_data.username is not None:
        conditions.append(User.username==form_data.username)
    result  = await db.execute(
            select(User).where(or_(*conditions))
            )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        if existing_user.email == form_data.email:
            raise EmailAlreadyTakenError 
        if existing_user.username == form_data.username:
            raise UsernameAlreadyTakenError

    data_dict = form_data.model_dump() 
    # delete password_confirmation
    data_dict.pop('password_confirmation')
    # pw hashing 
    pw = data_dict.pop('password') 
    data_dict['hashed_password'] = hash_pw(pw)
    user = User(**data_dict)
    db.add(user)
    # try except car si 2 requetes en meme temps sur le site, 
    # python va dire que email/username dispo mais pendant le save en base ca va planer pour un des deux:
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise EmailAlreadyTakenError # TODO: pour le moment email error toujours ( manque username )
    await db.refresh(user)
    return user 





 
