from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.models import Cattle
from app.schema import schemas
from app.utills.TransactionManager import TransactionManager

async def create_cattle(db: AsyncSession, cattle_data: schemas.CattleCreate) -> schemas.CattleOut:
    async with TransactionManager(db) as session:
        db_cattle = Cattle(**cattle_data.model_dump())
        session.add(db_cattle)
        await session.commit()
        await session.refresh(db_cattle)
        return db_cattle

async def get_cattle(db: AsyncSession, cattle_id: int) -> schemas.CattleOut:
    async with TransactionManager(db) as session:
        result = await session.execute(select(Cattle).filter(Cattle.cattle_id == cattle_id))
        db_cattle = result.scalars().first()
        if db_cattle is None:
            raise NoResultFound("Cattle not found")
        return db_cattle

async def get_all_cattles(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[schemas.CattleOut]:
    async with TransactionManager(db) as session:
        result = await session.execute(select(Cattle).offset(skip).limit(limit))
        return result.scalars().all()

async def update_cattle(db: AsyncSession, cattle_id: int, cattle_update: schemas.CattleUpdate) -> schemas.CattleOut:
    async with TransactionManager(db) as session:
        result = await session.execute(select(Cattle).filter(Cattle.cattle_id == cattle_id))
        db_cattle = result.scalars().first()
        if db_cattle is None:
            raise NoResultFound("Cattle not found")
        for key, value in cattle_update.model_dump(exclude_unset=True).items():  # Use model_dump() instead of dict()
            setattr(db_cattle, key, value)
        session.add(db_cattle)
        await session.commit()
        await session.refresh(db_cattle)
        return db_cattle

async def delete_cattle(db: AsyncSession, cattle_id: int) -> schemas.CattleOut:
    async with TransactionManager(db) as session:
        result = await session.execute(select(Cattle).filter(Cattle.cattle_id == cattle_id))
        db_cattle = result.scalars().first()
        if db_cattle is None:
            raise NoResultFound("Cattle not found")
        await session.delete(db_cattle)
        await session.commit()
        return db_cattle
