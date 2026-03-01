from fastapi import FastAPI

from app.routers import organizations, buildings, activities


app = FastAPI(
    title="Справочник Организаций, Зданий, Деятельности",
    description="Функционал API описан в README.md.",
    version="1.0.0",
    docs_url='/openapi',
    redoc_url="/redoc",
    openapi_url='/openapi.json',
)

app.include_router(organizations.router)
app.include_router(buildings.router)
app.include_router(activities.router)
