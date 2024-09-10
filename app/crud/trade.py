from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.trade import Trade

async def create_trade(db: AsyncSession, obj_in: dict) -> Trade:
    new_obj = Trade(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_trade(db: AsyncSession, trade_id: int) -> Trade:
    query = select(Trade).filter_by(trade_id=trade_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Trade record not found")
    return obj

async def update_trade(db: AsyncSession, trade_id: int, obj_in: dict) -> Trade:
    query = select(Trade).filter_by(trade_id=trade_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Trade record not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_trade(db: AsyncSession, trade_id: int) -> Trade:
    query = select(Trade).filter_by(trade_id=trade_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Trade record not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
