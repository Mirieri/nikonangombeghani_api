from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.insemination import Insemination
from app.schema.schemas import InseminationCreate, InseminationOut
from app.models.database import get_db

router = APIRouter()

@router.post("/inseminations/", response_model=InseminationOut)
def create_insemination(insemination: InseminationCreate, db: Session = Depends(get_db)):
    db_insemination = Insemination(**insemination.dict())
    db.add(db_insemination)
    db.commit()
    db.refresh(db_insemination)
    return db_insemination

@router.get("/inseminations/{insemination_id}", response_model=InseminationOut)
def read_insemination(insemination_id: int, db: Session = Depends(get_db)):
    db_insemination = db.query(Insemination).filter(Insemination.insemination_id == insemination_id).first()
    if db_insemination is None:
        raise HTTPException(status_code=404, detail="Insemination not found")
    return db_insemination

@router.put("/inseminations/{insemination_id}", response_model=InseminationOut)
def update_insemination(insemination_id: int, insemination: InseminationCreate, db: Session = Depends(get_db)):
    db_insemination = db.query(Insemination).filter(Insemination.insemination_id == insemination_id).first()
    if db_insemination is None:
        raise HTTPException(status_code=404, detail="Insemination not found")
    for key, value in insemination.dict().items():
        setattr(db_insemination, key, value)
    db.commit()
    db.refresh(db_insemination)
    return db_insemination

@router.delete("/inseminations/{insemination_id}", response_model=InseminationOut)
def delete_insemination(insemination_id: int, db: Session = Depends(get_db)):
    db_insemination = db.query(Insemination).filter(Insemination.insemination_id == insemination_id).first()
    if db_insemination is None:
        raise HTTPException(status_code=404, detail="Insemination not found")
    db.delete(db_insemination)
    db.commit()
    return db_insemination
