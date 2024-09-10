from typing import List
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.schema.schemas import CattleImageCreate, CattleImageResponse
from app.crud.cattle_image import create_cattle_image, get_cattle_images, get_cattle_image, delete_cattle_image
from app.auth.auth import get_db

router = APIRouter()

@router.post("/cattle/{cattle_id}/images/", response_model=CattleImageResponse)
async def upload_cattle_image(
    cattle_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db)
):
    return await create_cattle_image(db, cattle_id, file)

@router.get("/cattle/{cattle_id}/images/", response_model=List[CattleImageResponse])
async def list_cattle_images(
    cattle_id: int,
    db: AsyncSession = Depends(get_db)
):
    images = await get_cattle_images(db, cattle_id)
    return images

@router.get("/cattle/images/{image_id}", response_model=CattleImageResponse)
async def read_cattle_image(
    image_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_cattle_image(db, image_id)

@router.delete("/cattle/images/{image_id}", response_model=CattleImageResponse)
async def remove_cattle_image(
    image_id: int,
    db: AsyncSession = Depends(get_db)
):
    await delete_cattle_image(db, image_id)
    return {"detail": "Image deleted successfully"}
