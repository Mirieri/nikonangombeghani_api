import enum
from sqlalchemy import Column, String, DateTime, BigInteger, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from .database import Base

class UserRole(enum.Enum):
    Farmer = "Farmer"
    Client = "Client"
    Admin = "Admin"

class UserStatus(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Suspended = "Suspended"

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.Client)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime, nullable=True)
    status = Column(SQLEnum(UserStatus), default=UserStatus.Active)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)

    # Relationships
    location = relationship('Location', uselist=False, back_populates='user')
    cattle = relationship('Cattle', back_populates='farmer')
    trades_as_seller = relationship('Trade', foreign_keys='Trade.seller_id', back_populates='seller', lazy='joined')
    trades_as_buyer = relationship('Trade', foreign_keys='Trade.buyer_id', back_populates='buyer', lazy='joined')
    messages_sent = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    messages_received = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')
    notifications = relationship('Notification', back_populates='user')
    favorites = relationship('Favorite', back_populates='user')

