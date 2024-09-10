from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import schemas
from app.crud import user_crud
from app.auth.auth import get_db
from app.models import User
from passlib.context import CryptContext
from datetime import timedelta
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.auth import create_access_token, authenticate_user
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/token", response_model=schemas.Token)
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

@router.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    created_user = await user_crud.create_user(db=db, user=user)
    if created_user is None:
        raise HTTPException(status_code=400, detail="User could not be created")
    return schemas.UserResponse(message="Successfully registered new user", user=created_user)

@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=List[schemas.User])
async def read_all_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_users(db=db)

@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    if user_update.password:
        update_data['password_hash'] = pwd_context.hash(user_update.password)

    if 'username' in update_data:
        username_query = select(User).where(User.username == update_data['username'])
        username_result = await db.execute(username_query)
        existing_user = username_result.scalars().first()
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(status_code=400, detail="Username already exists")

    try:
        await db.execute(update(User).where(User.user_id == user_id).values(update_data))
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        error_message = str(e.orig) if e.orig else "Unknown database integrity error"
        print(f"IntegrityError: {error_message}")
        raise HTTPException(status_code=400, detail=f"Database integrity error: {error_message}")

    query = select(User).where(User.user_id == user_id)
    result = await db.execute(query)
    updated_user = result.scalars().first()
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

@router.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted_user = await user_crud.delete_user(db=db, user_id=user_id)
        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return deleted_user
    except IntegrityError as e:
        await db.rollback()
        error_message = str(e.orig) if e.orig else "Unknown database integrity error"
        print(f"IntegrityError: {error_message}")
        raise HTTPException(status_code=400, detail=f"Database integrity error: {error_message}")
