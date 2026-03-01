from fastapi import APIRouter, Depends, Query, Path

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import OrganizationSchema
from app.models import Organization, Activity, Building
from app.deps import get_db, verify_api_key
from app.crud import get_activity_tree_ids, haversine

router = APIRouter(
    prefix="/organizations",
    tags=["Организации"],
    dependencies=[Depends(verify_api_key)],
)


@router.get(
    "/by-building/{building_id}",
    summary="Список всех организаций находящихся в конкретном здании",
    description="Возвращает список всех организаций находящихся в конкретном здании по его идентификатору и API ключу",
    response_model=list[OrganizationSchema]
)
async def by_building(building_id: int = Path(..., description="Идентификатор здания"), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .where(Organization.building_id == building_id)
    )
    return result.scalars().all()


@router.get(
    "/by-activity/{activity_id}",
    summary="Список всех организаций, которые относятся к указанному виду деятельности",
    description="Возвращает список всех организаций, которые относятся к указанному виду деятельности по его идентификатору и API ключу",
    response_model=list[OrganizationSchema]
)
async def by_activity(
    activity_id: int = Path(..., description="Идентификатор деятельности"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .join(Organization.activities)
        .where(Activity.id == activity_id)
    )
    return result.scalars().all()


@router.get(
    "/by-activity-tree/{activity_id}",
    summary="Список всех организаций, которые относятся к указанному виду деятельности (включая вложенные)",
    description="Возвращает список всех организаций, которые относятся к указанному виду деятельности (включая вложенные) по его идентификатору и API ключу",
    response_model=list[OrganizationSchema]
)
async def by_activity_tree(activity_id: int = Path(..., description="Идентификатор деятельности"), db: AsyncSession = Depends(get_db)):
    ids = await get_activity_tree_ids(db, activity_id)

    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .join(Organization.activities)
        .where(Activity.id.in_(ids))
    )
    return result.scalars().all()


@router.get(
    "/search",
    summary="Поиск организации по названию",
    description="Осуществляет поиск организации по названию и API ключу",
    response_model=list[OrganizationSchema]
)
async def search(name: str = Query("коп", description="Часть названия организации"), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .where(Organization.name.ilike(f"%{name}%"))
    )
    return result.scalars().all()


@router.get(
    "/in-radius",
    summary="Список организаций, которые находятся в заданном радиусе относительно указанной точки на карте.",
    description="Возвращает список организаций, которые находятся в заданном радиусе в км на основе широты и долготы",
    response_model=list[OrganizationSchema]
)
async def near(
    lat: float = Query(55, description="Широта"),
    lon: float = Query(36, description="Долгота"),
    radius: float = Query(100000, description="Радиус"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Organization).options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        ))
    orgs = result.scalars().all()

    filtered = []
    for org in orgs:
        d = haversine(lat, lon, org.building.latitude, org.building.longitude)
        if d <= radius:
            filtered.append(org)

    return filtered


@router.get(
    "/in-rectangle",
    summary="Список организаций, которые находятся в заданной прямоугольной области относительно указанной точки на карте.",
    description="Возвращает список организаций, которые находятся в заданной прямоугольной области на основе минимальных и максимальных широты и долготы",
    response_model=list[OrganizationSchema]
)
async def in_rectangle(
    lat: float = Query(55, description="Широта"),
    lon: float = Query(36, description="Долгота"),
    delta_lat: float = Query(55, description="Дельта широты"),
    delta_lon: float = Query(36, description="Дельта долготы"),
    db: AsyncSession = Depends(get_db),
):
    min_lat = lat - delta_lat
    max_lat = lat + delta_lat
    min_lon = lon - delta_lon
    max_lon = lon + delta_lon

    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .join(Organization.building)
        .where(
            Building.latitude.between(min_lat, max_lat),
            Building.longitude.between(min_lon, max_lon),
        )
    )

    return result.scalars().unique().all()


@router.get(
    "/{org_id}",
    summary="Вывод информации об организации",
    description="Возвращает полную информацию об организации по её идентификатору и API ключу",
    response_model=OrganizationSchema
)
async def get_org(org_id: int = Path(..., description="Идентификатор организации"), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .where(Organization.id == org_id)
    )
    return result.scalar_one_or_none()
