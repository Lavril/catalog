from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Building
from app.schemas import BuildingSchema
from app.deps import verify_api_key, get_db

router = APIRouter(
    prefix="/buildings",
    tags=["Здания"],
    dependencies=[Depends(verify_api_key)]
)


@router.get(
    "/",
    summary="Список всех зданий",
    description="Возвращает список всех зданий по API ключу",
    response_model=list[BuildingSchema])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Building))
    return result.scalars().all()


@router.get(
    "/in-area",
    summary="Список всех зданий в прямоугольной области",
    description="Возвращает список всех зданий в прямоугольной области по минимальным и максимальным широте и долготе и API ключу",
    response_model=list[BuildingSchema])
async def in_area(
    min_lat: float = Query("1", description="Минимальная широта"),
    max_lat: float = Query("100", description="Максимальная широта"),
    min_lon: float = Query("1", description="Минимальная долгота"),
    max_lon: float = Query("100", description="Максимальная долгота"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Building).where(
            Building.latitude.between(min_lat, max_lat),
            Building.longitude.between(min_lon, max_lon),
        )
    )
    return result.scalars().all()
