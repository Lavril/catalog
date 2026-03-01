from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Activity
from app.schemas import ActivitySchema
from app.deps import verify_api_key, get_db

router = APIRouter(
    prefix="/activities",
    tags=["Деятельности"],
    dependencies=[Depends(verify_api_key)]
)


@router.get(
    "/",
    summary="Список всех деятельностей",
    description="Возвращает список всех деятельностей по API ключу",
    response_model=list[ActivitySchema]
)
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Activity))
    return result.scalars().all()
