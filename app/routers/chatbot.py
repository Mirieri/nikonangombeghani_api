from fastapi import  HTTPException


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.auth import get_db
from app.models import User, Message
from app.schema.schemas import MessageCreate
from app.utills.whatsapp.whatsapp import WhatsAppAPI

router = APIRouter()

@router.post("/messages/send")
async def send_whatsapp_message(message: MessageCreate, db: Session = Depends(get_db)):
    # Get sender and receiver users
    sender = db.query(User).filter(User.user_id == message.sender_id).first()
    receiver = db.query(User).filter(User.user_id == message.receiver_id).first()

    if not sender or not receiver:
        raise HTTPException(status_code=400, detail="Sender or receiver not found")

    # Send WhatsApp message
    whatsapp_api = WhatsAppAPI()
    whatsapp_response = whatsapp_api.send_message(
        to=receiver.phone,
        message=message.message_content
    )

    # Save message to the database
    db_message = Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        message_content=message.message_content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return {
        "message": db_message,
        "whatsapp_response": whatsapp_response
    }

