from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.pedigree import Pedigree

async def create_pedigree(db: AsyncSession, obj_in: dict) -> Pedigree:
    new_obj = Pedigree(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_pedigree(db: AsyncSession, pedigree_id: int) -> Pedigree:
    query = select(Pedigree).filter_by(id=pedigree_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Pedigree record not found")
    return obj

async def update_pedigree(db: AsyncSession, pedigree_id: int, obj_in: dict) -> Pedigree:
    query = select(Pedigree).filter_by(id=pedigree_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Pedigree record not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_pedigree(db: AsyncSession, pedigree_id: int) -> Pedigree:
    query = select(Pedigree).filter_by(id=pedigree_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Pedigree record not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
