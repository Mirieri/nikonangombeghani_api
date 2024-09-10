from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models import Cattle
from app.schema import schemas


async def create_cattle(db: AsyncSession, cattle: schemas.CattleCreate) -> Cattle:
    db_cattle = Cattle(
        name=cattle.name,
        breed=cattle.breed,
        birth_date=cattle.birth_date,
        gender=cattle.gender,
        quality_score=cattle.quality_score,
        status=cattle.status,
        user_id=cattle.user_id
    )
    db.add(db_cattle)
    try:
        await db.commit()
        await db.refresh(db_cattle)
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error occurred: {e}")
    return db_cattle


async def get_cattle(db: AsyncSession, cattle_id: int) -> Optional[Cattle]:
    query = select(Cattle).where(Cattle.cattle_id == cattle_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_all_cattles(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Cattle]:
    query = select(Cattle).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def update_cattle(db: AsyncSession, cattle_id: int, cattle_update: schemas.CattleUpdate) -> Optional[Cattle]:
    query = select(Cattle).where(Cattle.cattle_id == cattle_id)
    result = await db.execute(query)
    db_cattle = result.scalars().first()
    if db_cattle is None:
        return None

    for key, value in cattle_update.dict(exclude_unset=True).items():
        setattr(db_cattle, key, value)

    try:
        await db.commit()
        await db.refresh(db_cattle)
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error occurred: {e}")

    return db_cattle


async def delete_cattle(db: AsyncSession, cattle_id: int) -> Optional[Cattle]:
    query = select(Cattle).where(Cattle.cattle_id == cattle_id)
    result = await db.execute(query)
    db_cattle = result.scalars().first()
    if db_cattle is None:
        return None

    await db.delete(db_cattle)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error occurred: {e}")

    return db_cattle
