from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.calving import Calving
from app.schema.schemas import CalvingCreate, CalvingOut
from app.models.database import get_db

router = APIRouter()

@router.post("/calvings/", response_model=CalvingOut)
def create_calving(calving: CalvingCreate, db: Session = Depends(get_db)):
    db_calving = Calving(**calving.dict())
    db.add(db_calving)
    db.commit()
    db.refresh(db_calving)
    return db_calving

@router.get("/calvings/{calving_id}", response_model=CalvingOut)
def read_calving(calving_id: int, db: Session = Depends(get_db)):
    db_calving = db.query(Calving).filter(Calving.calving_id == calving_id).first()
    if db_calving is None:
        raise HTTPException(status_code=404, detail="Calving not found")
    return db_calving

@router.put("/calvings/{calving_id}", response_model=CalvingOut)
def update_calving(calving_id: int, calving: CalvingCreate, db: Session = Depends(get_db)):
    db_calving = db.query(Calving).filter(Calving.calving_id == calving_id).first()
    if db_calving is None:
        raise HTTPException(status_code=404, detail="Calving not found")
    for key, value in calving.dict().items():
        setattr(db_calving, key, value)
    db.commit()
    db.refresh(db_calving)
    return db_calving

@router.delete("/calvings/{calving_id}", response_model=CalvingOut)
def delete_calving(calving_id: int, db: Session = Depends(get_db)):
    db_calving = db.query(Calving).filter(Calving.calving_id == calving_id).first()
    if db_calving is None:
        raise HTTPException(status_code=404, detail="Calving not found")
    db.delete(db_calving)
    db.commit()
    return db_calving
