from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Activity, Building, Organization, Phone


async def seed_data(db: AsyncSession):
    result = await db.execute(select(Organization))
    if result.scalars().first():
        return

    food = Activity(name="Еда")
    meat = Activity(name="Мясная продукция", parent=food)
    milk = Activity(name="Молочная продукция", parent=food)
    transport = Activity(name="Перевозка", parent=food)

    building = Building(
        address="г. Москва, ул. Ленина 1",
        latitude=55.75,
        longitude=37.61,
    )

    building2 = Building(
        address="г. Москва, ул. Пушкина 3",
        latitude=55.35,
        longitude=37.71,
    )

    org = Organization(
        name="ООО Рога и Копыта",
        building=building,
        activities=[meat, milk],
    )

    org2 = Organization(
        name="ООО Перевозки",
        building=building,
        activities=[transport, meat],
    )

    org.phones = [
        Phone(number="2-222-222"),
        Phone(number="8-923-666-13-13"),
    ]

    db.add_all([food, meat, milk, transport, building, building2, org, org2])
    await db.commit()
