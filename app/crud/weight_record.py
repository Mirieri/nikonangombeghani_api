from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.weight_record import WeightRecord

async def create_weight_record(db: AsyncSession, obj_in: dict) -> WeightRecord:
    new_obj = WeightRecord(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_weight_record(db: AsyncSession, weight_id: int) -> WeightRecord:
    query = select(WeightRecord).filter_by(weight_id=weight_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="WeightRecord not found")
    return obj

async def update_weight_record(db: AsyncSession, weight_id: int, obj_in: dict) -> WeightRecord:
    query = select(WeightRecord).filter_by(weight_id=weight_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="WeightRecord not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_weight_record(db: AsyncSession, weight_id: int) -> WeightRecord:
    query = select(WeightRecord).filter_by(weight_id=weight_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="WeightRecord not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
