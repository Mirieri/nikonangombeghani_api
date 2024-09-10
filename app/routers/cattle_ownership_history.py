from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.cattle_ownership_history import CattleOwnershipHistory
from app.schema.schemas import CattleOwnershipHistoryCreate, CattleOwnershipHistoryOut
from app.models.database import get_db

router = APIRouter()

@router.post("/cattle_ownership_histories/", response_model=CattleOwnershipHistoryOut)
def create_cattle_ownership_history(cattle_ownership_history: CattleOwnershipHistoryCreate, db: Session = Depends(get_db)):
    db_cattle_ownership_history = CattleOwnershipHistory(**cattle_ownership_history.dict())
    db.add(db_cattle_ownership_history)
    db.commit()
    db.refresh(db_cattle_ownership_history)
    return db_cattle_ownership_history

@router.get("/cattle_ownership_histories/{ownership_id}", response_model=CattleOwnershipHistoryOut)
def read_cattle_ownership_history(ownership_id: int, db: Session = Depends(get_db)):
    db_cattle_ownership_history = db.query(CattleOwnershipHistory).filter(CattleOwnershipHistory.ownership_id == ownership_id).first()
    if db_cattle_ownership_history is None:
        raise HTTPException(status_code=404, detail="Cattle Ownership History not found")
    return db_cattle_ownership_history

@router.put("/cattle_ownership_histories/{ownership_id}", response_model=CattleOwnershipHistoryOut)
def update_cattle_ownership_history(ownership_id: int, cattle_ownership_history: CattleOwnershipHistoryCreate, db: Session = Depends(get_db)):
    db_cattle_ownership_history = db.query(CattleOwnershipHistory).filter(CattleOwnershipHistory.ownership_id == ownership_id).first()
    if db_cattle_ownership_history is None:
        raise HTTPException(status_code=404, detail="Cattle Ownership History not found")
    for key, value in cattle_ownership_history.dict().items():
        setattr(db_cattle_ownership_history, key, value)
    db.commit()
    db.refresh(db_cattle_ownership_history)
    return db_cattle_ownership_history

@router.delete("/cattle_ownership_histories/{ownership_id}", response_model=CattleOwnershipHistoryOut)
def delete_cattle_ownership_history(ownership_id: int, db: Session = Depends(get_db)):
    db_cattle_ownership_history = db.query(CattleOwnershipHistory).filter(CattleOwnershipHistory.ownership_id == ownership_id).first()
    if db_cattle_ownership_history is None:
        raise HTTPException(status_code=404, detail="Cattle Ownership History not found")
    db.delete(db_cattle_ownership_history)
    db.commit()
    return db_cattle_ownership_history