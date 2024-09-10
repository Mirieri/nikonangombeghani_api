from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from .. import crud
from ..models import database
from ..schema import schemas

router = APIRouter()

@router.post("/webhook")
async def handle_incoming_message(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    message = schemas.MessageCreate(
        sender_id=data.get('sender'),
        receiver_id=data.get('receiver'),
        message_content=data.get('message')
    )
    result = await crud.create_message(db, message)
    return {"status": "success", "message_id": result["db_message"].message_id}
