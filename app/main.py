from fastapi import FastAPI
from app.routers import user_router, cattle_router, messaging_router, cattle_image_router
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
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(cattle_router.router, prefix="/cattle", tags=["cattle"])
app.include_router(messaging_router.router, prefix="/messaging", tags=["messaging"])
app.include_router(cattle_image_router.router, prefix="/images", tags=["images"])

@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint for health check and welcome message."""
    return {"message": "Welcome to N3G API!"}
