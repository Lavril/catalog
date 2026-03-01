from fastapi import Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.config import settings


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def verify_api_key(x_api_key: str = Header("supersecret", description="API Key")):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
