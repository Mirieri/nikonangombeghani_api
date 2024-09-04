from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from passlib.context import CryptContext
from . import schemas, crud
from .database import Base, engine
from .schemas import UserResponse
from .auth import create_access_token, authenticate_user, get_db
from .config import ACCESS_TOKEN_EXPIRE_MINUTES
from .models import User
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

# Create a new FastAPI app
app = FastAPI()

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

# Token endpoint for login
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the existing user
    query = select(User).where(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Prepare the update data
    update_data = user_update.model_dump(exclude_unset=True)

    # Hash the new password if it's provided
    if user_update.password:
        update_data['password_hash'] = pwd_context.hash(user_update.password)

    # Check if the new username is unique
    if 'username' in update_data:
        username_query = select(User).where(User.username == update_data['username'])
        username_result = await db.execute(username_query)
        existing_user = username_result.scalar_one_or_none()
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(status_code=400, detail="Username already exists")

    # Update the user
    try:
        await db.execute(update(User).where(User.user_id == user_id).values(update_data))
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        # Log the detailed error message for debugging
        error_message = str(e.orig) if e.orig else "Unknown database integrity error"
        print(f"IntegrityError: {error_message}")
        raise HTTPException(status_code=400, detail=f"Database integrity error: {error_message}")

    # Return the updated user
    query = select(User).where(User.user_id == user_id)
    result = await db.execute(query)
    updated_user = result.scalar_one_or_none()
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

@app.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Attempt to delete the user
        deleted_user = await crud.delete_user(db=db, user_id=user_id)
        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return deleted_user
    except IntegrityError as e:
        await db.rollback()
        # Log and handle the integrity error
        error_message = str(e.orig) if e.orig else "Unknown database integrity error"
        print(f"IntegrityError: {error_message}")
        raise HTTPException(status_code=400, detail=f"Database integrity error: {error_message}")

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
