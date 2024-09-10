from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.notification import Notification
from app.schema.schemas import NotificationCreate, NotificationOut
from app.models.database import get_db

router = APIRouter()

@router.post("/notifications/", response_model=NotificationOut)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/notifications/{notification_id}", response_model=NotificationOut)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.put("/notifications/{notification_id}", response_model=NotificationOut)
def update_notification(notification_id: int, notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    for key, value in notification.dict().items():
        setattr(db_notification, key, value)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/notifications/{notification_id}", response_model=NotificationOut)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notification)
    db.commit()
    return db_notification
