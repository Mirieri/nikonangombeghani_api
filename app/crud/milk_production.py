from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.milk_production import MilkProduction

async def create_milk_production(db: AsyncSession, obj_in: dict) -> MilkProduction:
    new_obj = MilkProduction(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_milk_production(db: AsyncSession, production_id: int) -> MilkProduction:
    query = select(MilkProduction).filter_by(production_id=production_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="MilkProduction record not found")
    return obj

async def update_milk_production(db: AsyncSession, production_id: int, obj_in: dict) -> MilkProduction:
    query = select(MilkProduction).filter_by(production_id=production_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="MilkProduction record not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_milk_production(db: AsyncSession, production_id: int) -> MilkProduction:
    query = select(MilkProduction).filter_by(production_id=production_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="MilkProduction record not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
