from fastapi import FastAPI
from app.routers import (
    user, cattle, messaging, cattle_image,
    calving, cattle_ownership_history, favorite,
    insemination, milk_production, notification,
    pedigree
)
from app.models.database import Base, engine
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def lifespan_manager(app: FastAPI) -> AsyncIterator[None]:
    """Handle the lifespan of the application, including database setup and teardown."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(lifespan=lifespan_manager)

# Include routers
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(cattle.router, prefix="/cattle", tags=["cattle"])
app.include_router(messaging.router, prefix="/messaging", tags=["messaging"])
app.include_router(cattle_image.router, prefix="/images", tags=["images"])
app.include_router(calving.router, prefix="/calving", tags=["calving"])
app.include_router(cattle_ownership_history.router, prefix="/cattle_ownership_histories", tags=["cattle_ownership_histories"])
app.include_router(favorite.router, prefix="/favorite", tags=["favorite"])
app.include_router(insemination.router, prefix="/insemination", tags=["insemination"])
app.include_router(notification.router, prefix="/notification", tags=["notification"])
app.include_router(milk_production.router, prefix="/milk", tags=["milk"])
app.include_router(pedigree.router, prefix="/pedigree", tags=["pedigree"])