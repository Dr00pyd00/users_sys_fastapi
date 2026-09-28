
from pydantic import BaseModel, EmailStr


# Tokens  ----------------------------------------------------------------
class RefreshTokenRequestSchema(BaseModel):
    """
    Pydantic schema for ask a new access_token.
    Contains:
        - refresh_token: str 
    """
    refresh_token: str


class RefreshedAccessTokenSchema(BaseModel):
    """
        Pydantic schema for displays access_token AFTER a refresh to client.
        Contains:
            - access_token: str 
            - expires_in: int -> expiration time 
            - token_type: str 
    """
    access_token: str 
    expires_in: int 
    token_type: str = 'Bearer'


class UserLoginSchema(BaseModel):
    """
    Pydantic schema for forms login.
    Contains:
        - email: str 
        - password: str
    """
    email: EmailStr 
    password: str 


class UserSuccessLoginTokensSchema(BaseModel):
    """
    Pydantic schema for displays tokens ( access + refresh ) to client.
    Contains:
        - access_token: str 
        - refresh_token: str 
        - expires_in: int -> expiration time 
        - token_type: str 
    """
    access_token: str 
    refresh_token: str 
    expires_in: int 
    token_type: str = 'Bearer'



