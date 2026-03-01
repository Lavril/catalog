import asyncio
from app.db import async_session
from app.seed import seed_data


async def main():
    async with async_session() as session:
        await seed_data(session)


if __name__ == "__main__":
    asyncio.run(main())
