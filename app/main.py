from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, crud
from .database import Base, engine, SessionLocal  # Importing from database.py
from .schemas import UserResponse

# Create a new FastAPI app
app = FastAPI()

# Dependency to get the asynchronous database session
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# Asynchronous function to create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Startup event to initialize the database
@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def read_root():
    return {"message": "Welcome to N3G API!"}

# User endpoints
@app.post("/users/", response_model=UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    created_user = await crud.create_user(db=db, user=user)
    if created_user is None:
        raise HTTPException(status_code=400, detail="User could not be created")
    return UserResponse(message="Successfully registered new user", user=created_user)

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user_update: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_user(db=db, user_id=user_id, user_update=user_update)

@app.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_user(db=db, user_id=user_id)

# Farmer endpoints
@app.post("/farmers/", response_model=schemas.FarmerOut)
async def create_farmer(farmer: schemas.FarmerCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_farmer(db=db, farmer=farmer)

@app.get("/farmers/{farmer_id}", response_model=schemas.FarmerOut)
async def read_farmer(farmer_id: int, db: AsyncSession = Depends(get_db)):
    db_farmer = await crud.get_farmer(db, farmer_id=farmer_id)
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer

@app.get("/farmers/", response_model=list[schemas.FarmerOut])
async def read_farmers(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_farmers(db=db, skip=skip, limit=limit)

# Cattle endpoints
@app.post("/cattles/", response_model=schemas.CattleOut)
async def create_cattle(cattle: schemas.CattleCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_cattle(db=db, cattle=cattle)

@app.get("/cattles/{cattle_id}", response_model=schemas.CattleOut)
async def read_cattle(cattle_id: int, db: AsyncSession = Depends(get_db)):
    db_cattle = await crud.get_cattle(db, cattle_id=cattle_id)
    if db_cattle is None:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return db_cattle

@app.get("/cattles/", response_model=list[schemas.CattleOut])
async def read_cattles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_cattles(db=db, skip=skip, limit=limit)
