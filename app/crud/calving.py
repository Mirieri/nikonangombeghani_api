from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.calving import Calving
from app.models.cattle import Cattle

async def create_calving(db: AsyncSession, obj_in: dict) -> Calving:
    new_obj = Calving(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_calving(db: AsyncSession, calving_id: int) -> Calving:
    query = select(Calving).filter_by(calving_id=calving_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Calving not found")
    return obj

async def update_calving(db: AsyncSession, calving_id: int, obj_in: dict) -> Calving:
    query = select(Calving).filter_by(calving_id=calving_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Calving not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_calving(db: AsyncSession, calving_id: int) -> Calving:
    query = select(Calving).filter_by(calving_id=calving_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Calving not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
