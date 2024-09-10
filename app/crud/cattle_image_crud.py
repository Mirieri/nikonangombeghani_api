from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile, HTTPException
from ..models import CattleImage
from app.schema.schemas import CattleImageResponse
from app.utills.image_utill import save_image_to_storage


def create_cattle_image(db: Session, cattle_id: int, file: UploadFile) -> CattleImageResponse:
    try:
        # Save the image to a storage and get the URL
        image_url = save_image_to_storage(file.file, file.filename)

        # Create a new CattleImage instance
        new_image = CattleImage(
            cattle_id=cattle_id,
            image_url=image_url
        )

        # Add the new image to the session and commit
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return CattleImageResponse.from_orm(new_image)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Cattle ID does not exist or other integrity error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_cattle_images(db: Session, cattle_id: int):
    return db.query(CattleImage).filter(CattleImage.cattle_id == cattle_id).all()


def get_cattle_image(db: Session, image_id: int) -> CattleImageResponse:
    image = db.query(CattleImage).filter(CattleImage.image_id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return CattleImageResponse.from_orm(image)


def delete_cattle_image(db: Session, image_id: int):
    image = db.query(CattleImage).filter(CattleImage.image_id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
