from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import schemas
from app.crud import cattle_crud
from app.auth.auth import get_db

router = APIRouter()

@router.post("/cattles/", response_model=schemas.CattleOut)
async def create_cattle(cattle: schemas.CattleCreate, db: AsyncSession = Depends(get_db)):
    return await cattle_crud.create_cattle(db=db, cattle=cattle)

@router.get("/cattles/{cattle_id}", response_model=schemas.CattleOut)
async def read_cattle(cattle_id: int, db: AsyncSession = Depends(get_db)):
    db_cattle = await cattle_crud.get_cattle(db, cattle_id=cattle_id)
    if db_cattle is None:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return db_cattle

@router.get("/cattles/", response_model=List[schemas.CattleOut])
async def read_all_cattles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await cattle_crud.get_all_cattles(db=db, skip=skip, limit=limit)

@router.put("/cattles/{cattle_id}", response_model=schemas.CattleOut)
async def update_cattle(
    cattle_id: int,
    cattle_update: schemas.CattleUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_cattle = await cattle_crud.update_cattle(db, cattle_id=cattle_id, cattle_update=cattle_update)
    if updated_cattle is None:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return updated_cattle

@router.delete("/cattles/{cattle_id}", response_model=schemas.CattleOut)
async def delete_cattle(cattle_id: int, db: AsyncSession = Depends(get_db)):
    deleted_cattle = await cattle_crud.delete_cattle(db, cattle_id=cattle_id)
    if deleted_cattle is None:
        raise HTTPException(status_code=404, detail="Cattle not found")
    return deleted_cattle
