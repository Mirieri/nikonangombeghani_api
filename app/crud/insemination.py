from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.insemination import Insemination
from app.models.cattle import Cattle

async def create_insemination(db: AsyncSession, obj_in: dict) -> Insemination:
    new_obj = Insemination(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_insemination(db: AsyncSession, insemination_id: int) -> Insemination:
    query = select(Insemination).filter_by(insemination_id=insemination_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Insemination not found")
    return obj

async def update_insemination(db: AsyncSession, insemination_id: int, obj_in: dict) -> Insemination:
    query = select(Insemination).filter_by(insemination_id=insemination_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Insemination not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_insemination(db: AsyncSession, insemination_id: int) -> Insemination:
    query = select(Insemination).filter_by(insemination_id=insemination_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Insemination not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
