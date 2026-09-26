
"""
    Installer : uv add python-dateutil
"""

from datetime import date 
from dateutil.relativedelta import relativedelta # prend en compte annees bisectiles

from typing import Optional
import re

from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo


USERNAME_REGEX = r'^[a-zA-Z0-9_-]+$'
NAMES_REGEX = r"^[a-zA-ZÀ-ÖØ-öø-ÿ' -]+$"
    

# Forms ------------------------------------------------------------------------------------ 
class UserCreationFormSchema(BaseModel):
    """ 
    Pydantic schema for create a new User 
    """

    # required ----------------
    email: EmailStr = Field(
            ..., # trois point pour rendre obligatoire le champ 
            description='User email for login etc.',
            )

    password: str = Field(
            ...,
            min_length=10,
            max_length=72,
            description='User password: 10 to 72 chars.',
            )

    password_confirmation: str = Field(
            ...,
            min_length=10,
            max_length=72,
            description='user password2, the confirmation one: 10 to 72 chars.',
            )

    # optional -----------------
    username: Optional[str] = Field(
            min_length=2,
            max_length=100,
            description='User username: 2 to 100 chars.',
            default=None,
            )
            
    first_name: Optional[str] = Field(
            min_length=2,
            max_length=100,
            description='User first_name: 2 to 100 chars.',
            default=None,
            )
    last_name: Optional[str] = Field(
            min_length=2,
            max_length=100,
            description='User last_name: 2 to 100 chars.',
            default=None,
            )
 
    birth: Optional[date] = None

    phone_number: Optional[str] = Field(
            min_length=10,
            max_length=20,
            description='User phone_number: 10 to 20 chars.',
            default=None,
            )

    # validators ----------------
    """
        field_validator: verifie avant de creer l'objet. 
        Donc il existe `ValidationInfo` qui sert a regarder les data saisis avant.

        - ValidationInfo.data -> dict qui contient les data saisis 
        - ValidationInfo.filed_name -> str du champ tester
    """
    @field_validator('username')
    @classmethod
    def verify_username_format(cls, input: str | None) -> str | None:
        if input:
            if re.match(USERNAME_REGEX, input) is None:
                raise ValueError('<username> must be alphanumeric (can contain: - _)')
            return input
        return None
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def verify_name_format(cls, input: str | None, info: ValidationInfo) -> str | None:
        if input:
            if re.match(NAMES_REGEX, input) is None:
                raise ValueError(f'<{info.field_name}> must contain only letters, spaces, - or \'')
            return input
        return None
    
    @field_validator('password')
    @classmethod
    def verify_complexity_password(cls, input: str) -> str:
        if not any(char.isdigit() for char in input):
            raise ValueError('<password> must contain at least ONE digit')
        if not any(char.isalpha() for char in input):
            raise ValueError('<password> must contain at least ONE alphabetic char')
        return input
    
    @field_validator('password_confirmation')
    @classmethod
    def verify_confirmation_password(cls, input: str, info: ValidationInfo) -> str:
        if input != info.data.get('password'):
            raise ValueError('<password_confirmation> does not match <password?>')
        return input
    
    @field_validator('birth')
    @classmethod
    def verify_age_possible(cls, input: date) -> date:
        if input >= date.today():
            raise ValueError('<birth> must be in the past.')
        if input <= date.today() - relativedelta(years=120):
            raise ValueError("<birth>, age can't be greater than 120 years")
        return input    


class UserClientDisplaySchema(BaseModel):
    """
    Pydantic schema for displays User data to a client
    """

    model_config = {'from_attributes':True}
    
    id: int  
    email: EmailStr 
    username: str | None = None 
    first_name: str | None = None 
    last_name: str | None = None 
    birth: date | None = None 
    phone_number: str | None = None 





