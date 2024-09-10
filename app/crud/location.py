from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.location import Location

async def create_location(db: AsyncSession, obj_in: dict) -> Location:
    new_obj = Location(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_location(db: AsyncSession, location_id: int) -> Location:
    query = select(Location).filter_by(location_id=location_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return obj

async def update_location(db: AsyncSession, location_id: int, obj_in: dict) -> Location:
    query = select(Location).filter_by(location_id=location_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Location not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_location(db: AsyncSession, location_id: int) -> Location:
    query = select(Location).filter_by(location_id=location_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Location not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
