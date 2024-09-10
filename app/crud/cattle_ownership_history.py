from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.cattle_ownership_history import CattleOwnershipHistory

async def create_cattle_ownership_history(db: AsyncSession, obj_in: dict) -> CattleOwnershipHistory:
    new_obj = CattleOwnershipHistory(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_cattle_ownership_history(db: AsyncSession, ownership_id: int) -> CattleOwnershipHistory:
    query = select(CattleOwnershipHistory).filter_by(ownership_id=ownership_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="CattleOwnershipHistory record not found")
    return obj

async def update_cattle_ownership_history(db: AsyncSession, ownership_id: int, obj_in: dict) -> CattleOwnershipHistory:
    query = select(CattleOwnershipHistory).filter_by(ownership_id=ownership_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="CattleOwnershipHistory record not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_cattle_ownership_history(db: AsyncSession, ownership_id: int) -> CattleOwnershipHistory:
    query = select(CattleOwnershipHistory).filter_by(ownership_id=ownership_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="CattleOwnershipHistory record not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
