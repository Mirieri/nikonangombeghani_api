from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.favorite import Favorite

async def create_favorite(db: AsyncSession, obj_in: dict) -> Favorite:
    new_obj = Favorite(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_favorite(db: AsyncSession, favorite_id: int) -> Favorite:
    query = select(Favorite).filter_by(favorite_id=favorite_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Favorite record not found")
    return obj

async def update_favorite(db: AsyncSession, favorite_id: int, obj_in: dict) -> Favorite:
    query = select(Favorite).filter_by(favorite_id=favorite_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Favorite record not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_favorite(db: AsyncSession, favorite_id: int) -> Favorite:
    query = select(Favorite).filter_by(favorite_id=favorite_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Favorite record not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
