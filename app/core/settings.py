
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Setting object who contains all variables from .env.
    Access:  instance.variable_name

    Contains 1 property methods:
        - `get_db_url`: return the db url for Postgres
    """ 

    # Pour que pydantic sache ou aller chercher .env ( normalement ca prend que les variables de base )
    model_config = SettingsConfigDict(env_file='.env')

    # Postgres 
    postgres_host: str
    postgres_port: int 
    postgres_user: str 
    postgres_password: str 
    postgres_db: str 

    # JWT 
    jwt_secret: str 
    jwt_algorithm: str 

    
    @property 
    def get_db_url(self):
        """
        Property who return the postgresql async URL,   
        for connect to a DB.   

        Format : 'postgresql+asyncpg://[user]:[password]@[host]:[port]/[db_nane]'  
        """
        return (
                f'postgresql+asyncpg://{self.postgres_user}' 
                f':{self.postgres_password}' 
                f'@{self.postgres_host}' 
                f':{self.postgres_port}' 
                f'/{self.postgres_db}' 
                )


settings = Settings() # type:ignore




