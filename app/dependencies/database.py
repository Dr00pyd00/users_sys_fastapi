
from app.core.database import LocalSession

async def get_db():
    async with LocalSession() as db:
        yield db

