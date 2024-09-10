from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.milk_production import MilkProduction
from app.schema.schemas import MilkProductionCreate, MilkProductionOut
from app.models.database import get_db

router = APIRouter()

@router.post("/milk_productions/", response_model=MilkProductionOut)
def create_milk_production(milk_production: MilkProductionCreate, db: Session = Depends(get_db)):
    db_milk_production = MilkProduction(**milk_production.dict())
    db.add(db_milk_production)
    db.commit()
    db.refresh(db_milk_production)
    return db_milk_production

@router.get("/milk_productions/{production_id}", response_model=MilkProductionOut)
def read_milk_production(production_id: int, db: Session = Depends(get_db)):
    db_milk_production = db.query(MilkProduction).filter(MilkProduction.production_id == production_id).first()
    if db_milk_production is None:
        raise HTTPException(status_code=404, detail="Milk production not found")
    return db_milk_production

@router.put("/milk_productions/{production_id}", response_model=MilkProductionOut)
def update_milk_production(production_id: int, milk_production: MilkProductionCreate, db: Session = Depends(get_db)):
    db_milk_production = db.query(MilkProduction).filter(MilkProduction.production_id == production_id).first()
    if db_milk_production is None:
        raise HTTPException(status_code=404, detail="Milk production not found")
    for key, value in milk_production.dict().items():
        setattr(db_milk_production, key, value)
    db.commit()
    db.refresh(db_milk_production)
    return db_milk_production

@router.delete("/milk_productions/{production_id}", response_model=MilkProductionOut)
def delete_milk_production(production_id: int, db: Session = Depends(get_db)):
    db_milk_production = db.query(MilkProduction).filter(MilkProduction.production_id == production_id).first()
    if db_milk_production is None:
        raise HTTPException(status_code=404, detail="Milk production not found")
    db.delete(db_milk_production)
    db.commit()
    return db_milk_production
