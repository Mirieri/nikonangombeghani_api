from fastapi import FastAPI
from app.routers import user_router, cattle_router, messaging_router
from app.models.database import Base, engine
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def lifespan_handler(app: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(lifespan=lifespan_handler)

app.include_router(user_router.router)
app.include_router(cattle_router.router)
app.include_router(messaging_router.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to N3G API!"}
