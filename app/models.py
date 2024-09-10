import enum

from sqlalchemy import Column, String, Date, BigInteger, Enum as SQLEnum, ForeignKey, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base


# Enum definitions
class UserRole(enum.Enum):
    Farmer = "Farmer"
    Client = "Client"
    Admin = "Admin"

class UserStatus(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Suspended = "Suspended"

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"

class CattleStatusEnum(enum.Enum):
    Available = "Available"
    Sold = "Sold"
    NotAvailable = "Not Available"

# User Model
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
    phone = Column(String(20), unique=True, nullable=True)
    address = Column(String(255), nullable=True)

    # Relationships
    location = relationship('Location', uselist=False, back_populates='user')
    cattle = relationship('Cattle', back_populates='farmer')
    trades_as_seller = relationship('Trade', foreign_keys='Trade.seller_id', back_populates='seller')
    trades_as_buyer = relationship('Trade', foreign_keys='Trade.buyer_id', back_populates='buyer')

# Location Model
class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    farmer_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    latitude = Column(DECIMAL(9, 6), nullable=True)
    longitude = Column(DECIMAL(9, 6), nullable=True)
    climate_zone = Column(String(100), nullable=True)
    updated_at = Column(Date, nullable=True)

    # Relationships
    user = relationship('User', back_populates='location')

# Trade Model
class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    seller_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    buyer_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id'), nullable=True)
    trade_date = Column(Date)
    price = Column(DECIMAL(10, 2))
    status = Column(SQLEnum('Pending', 'Completed', 'Cancelled', name='trade_status_enum'))
    delivery_date = Column(Date)

    # Relationships
    seller = relationship('User', foreign_keys=[seller_id], back_populates='trades_as_seller')
    buyer = relationship('User', foreign_keys=[buyer_id], back_populates='trades_as_buyer')
    cattle = relationship('Cattle', back_populates='trades')

# Cattle Model
class Cattle(Base):
    __tablename__ = 'cattle'

    cattle_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    farmer_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    breed = Column(String(100), nullable=True)
    birth_date = Column(Date)
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    quality_score = Column(DECIMAL(5, 2))
    status = Column(SQLEnum(CattleStatusEnum), default=CattleStatusEnum.Available)

    # Relationships
    farmer = relationship('User', back_populates='cattle')
    images = relationship('CattleImage', back_populates='cattle', cascade="all, delete-orphan")
    trades = relationship('Trade', back_populates='cattle')

# CattleImage Model
class CattleImage(Base):
    __tablename__ = 'cattle_images'

    image_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())

    # Relationships
    cattle = relationship('Cattle', back_populates='images')
