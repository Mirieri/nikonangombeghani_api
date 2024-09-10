from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.notification import Notification

async def create_notification(db: AsyncSession, obj_in: dict) -> Notification:
    new_obj = Notification(**obj_in)
    async with db.begin():
        db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj

async def get_notification(db: AsyncSession, notification_id: int) -> Notification:
    query = select(Notification).filter_by(notification_id=notification_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Notification record not found")
    return obj

async def update_notification(db: AsyncSession, notification_id: int, obj_in: dict) -> Notification:
    query = select(Notification).filter_by(notification_id=notification_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Notification record not found")

    for key, value in obj_in.items():
        setattr(obj, key, value)

    async with db.begin():
        await db.commit()
        await db.refresh(obj)
    return obj

async def delete_notification(db: AsyncSession, notification_id: int) -> Notification:
    query = select(Notification).filter_by(notification_id=notification_id)
    result = await db.execute(query)
    obj = result.scalars().first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Notification record not found")

    async with db.begin():
        await db.delete(obj)
        await db.commit()
    return obj
