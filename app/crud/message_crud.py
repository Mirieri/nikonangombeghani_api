from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Message, User
from app.schema.schemas import MessageCreate
from app.whatsapp.whatsapp import WhatsAppAPI
from app.config.whatsapp_settings import AppSettings

def get_user_phone_number(db: Session, receiver_id: int) -> str:
    user = db.query(User).filter(User.user_id == receiver_id).first()
    return user.phone if user else ""

async def create_message(db: Session, message: MessageCreate):
    # Initialize the settings
    settings = AppSettings()  # Use AppSettings here
    whatsapp_client = WhatsAppAPI(api_url=settings.api_url, api_key=settings.api_key)

    # Create the message in the database
    db_message = Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        message_content=message.message_content,
        sent_at=func.now()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # Send the message via WhatsApp API
    receiver_phone_number = get_user_phone_number(db, message.receiver_id)
    whatsapp_response = whatsapp_client.send_message(
        to=receiver_phone_number,
        message=message.message_content
    )

    return {
        "db_message": db_message,
        "whatsapp_response": whatsapp_response
    }
