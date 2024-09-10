from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.pedigree import Pedigree
from app.schema.schemas import PedigreeCreate, PedigreeOut
from app.models.database import get_db

router = APIRouter()

@router.post("/pedigrees/", response_model=PedigreeOut)
def create_pedigree(pedigree: PedigreeCreate, db: Session = Depends(get_db)):
    db_pedigree = Pedigree(**pedigree.dict())
    db.add(db_pedigree)
    db.commit()
    db.refresh(db_pedigree)
    return db_pedigree

@router.get("/pedigrees/{id}", response_model=PedigreeOut)
def read_pedigree(id: int, db: Session = Depends(get_db)):
    db_pedigree = db.query(Pedigree).filter(Pedigree.id == id).first()
    if db_pedigree is None:
        raise HTTPException(status_code=404, detail="Pedigree not found")
    return db_pedigree

@router.put("/pedigrees/{id}", response_model=PedigreeOut)
def update_pedigree(id: int, pedigree: PedigreeCreate, db: Session = Depends(get_db)):
    db_pedigree = db.query(Pedigree).filter(Pedigree.id == id).first()
    if db_pedigree is None:
        raise HTTPException(status_code=404, detail="Pedigree not found")
    for key, value in pedigree.dict().items():
        setattr(db_pedigree, key, value)
    db.commit()
    db.refresh(db_pedigree)
    return db_pedigree

@router.delete("/pedigrees/{id}", response_model=PedigreeOut)
def delete_pedigree(id: int, db: Session = Depends(get_db)):
    db_pedigree = db.query(Pedigree).filter(Pedigree.id == id).first()
    if db_pedigree is None:
        raise HTTPException(status_code=404, detail="Pedigree not found")
    db.delete(db_pedigree)
    db.commit()
    return db_pedigree
