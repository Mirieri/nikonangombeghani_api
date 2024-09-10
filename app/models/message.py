from sqlalchemy import Column, BigInteger, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base
from .user import User

class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    sender_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    receiver_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    message_content = Column(String(1000), nullable=False)
    sent_at = Column(DateTime, server_default=func.now())

    # Relationships
    sender = relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='messages_received')
