from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import schemas
from app.crud import cattle
from app.auth.auth import get_db
from sqlalchemy.exc import NoResultFound

router = APIRouter()

@router.post("/cattles/", response_model=schemas.CattleOut)
async def create_cattle(cattle_new: schemas.CattleCreate, db: AsyncSession = Depends(get_db)):
    try:
        created_cattle = await cattle.create_cattle(db=db, cattle_data=cattle_new)
        return created_cattle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating cattle: {e}")

@router.get("/cattles/{cattle_id}", response_model=schemas.CattleOut)
async def read_cattle(cattle_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_cattle = await cattle.get_cattle(db, cattle_id=cattle_id)
        return db_cattle
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Cattle not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving cattle: {e}")

@router.get("/cattles/", response_model=List[schemas.CattleOut])
async def read_all_cattles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        return await cattle.get_all_cattles(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving cattles: {e}")

@router.put("/cattles/{cattle_id}", response_model=schemas.CattleOut)
async def update_cattle(cattle_id: int, cattle_update: schemas.CattleUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_cattle = await cattle.update_cattle(db, cattle_id=cattle_id, cattle_update=cattle_update)
        return updated_cattle
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Cattle not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating cattle: {e}")

@router.delete("/cattles/{cattle_id}", response_model=schemas.CattleOut)
async def delete_cattle(cattle_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted_cattle = await cattle.delete_cattle(db, cattle_id=cattle_id)
        return deleted_cattle
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Cattle not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting cattle: {e}")
