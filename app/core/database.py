
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings 


engine = create_async_engine(url=settings.get_db_url)

LocalSession = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        )

class Base(DeclarativeBase):
    pass 

