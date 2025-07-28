from app.utils.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
        