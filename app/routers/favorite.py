from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.favorite import Favorite
from app.schema.schemas import FavoriteCreate, FavoriteOut
from app.models.database import get_db

router = APIRouter()

@router.post("/favorites/", response_model=FavoriteOut)
def create_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    db_favorite = Favorite(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

@router.get("/favorites/{favorite_id}", response_model=FavoriteOut)
def read_favorite(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = db.query(Favorite).filter(Favorite.favorite_id == favorite_id).first()
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return db_favorite

@router.put("/favorites/{favorite_id}", response_model=FavoriteOut)
def update_favorite(favorite_id: int, favorite: FavoriteCreate, db: Session = Depends(get_db)):
    db_favorite = db.query(Favorite).filter(Favorite.favorite_id == favorite_id).first()
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    for key, value in favorite.dict().items():
        setattr(db_favorite, key, value)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

@router.delete("/favorites/{favorite_id}", response_model=FavoriteOut)
def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = db.query(Favorite).filter(Favorite.favorite_id == favorite_id).first()
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(db_favorite)
    db.commit()
    return db_favorite
