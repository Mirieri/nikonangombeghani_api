from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.cattle import Cattle
from app.schema import schemas

async def create_cattle(db: AsyncSession, cattle_data: schemas.CattleCreate) -> Cattle:
    # Create an instance of the Cattle model
    db_cattle = Cattle(
        name=cattle_data.name,
        breed=cattle_data.breed,
        birth_date=cattle_data.birth_date,
        gender=cattle_data.gender,
        quality_score=cattle_data.quality_score,
        status=cattle_data.status,
        user_id=cattle_data.user_id
    )

    db.add(db_cattle)
    try:
        await db.commit()
        await db.refresh(db_cattle)
        return db_cattle
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error occurred while creating cattle: {e}")

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

    if not db_cattle:
        return None

    for key, value in cattle_update.dict(exclude_unset=True).items():
        setattr(db_cattle, key, value)

    try:
        await db.commit()
        await db.refresh(db_cattle)
        return db_cattle
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error occurred while updating cattle: {e}")

async def delete_cattle(db: AsyncSession, cattle_id: int) -> Optional[Cattle]:
    query = select(Cattle).where(Cattle.cattle_id == cattle_id)
    result = await db.execute(query)
    db_cattle = result.scalars().first()

    if not db_cattle:
        return None

    await db.delete(db_cattle)
    try:
        await db.commit()
        return db_cattle
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Integrity error occurred while deleting cattle: {e}")
