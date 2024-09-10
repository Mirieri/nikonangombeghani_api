import enum

from sqlalchemy import Column, BigInteger, String, Date, DECIMAL, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class CattleStatusEnum(enum.Enum):
    Available = "Available"
    Sold = "Sold"
    NotAvailable = "Not Available"

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"

class Cattle(Base):
    __tablename__ = 'cattle'

    cattle_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=True)
    breed = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(SQLEnum(GenderEnum), nullable=True)
    quality_score = Column(DECIMAL(5, 2), nullable=True)
    status = Column(SQLEnum(CattleStatusEnum), nullable=True)

    # Relationships
    farmer = relationship('User', back_populates='cattle')
    calvings = relationship('Calving', back_populates='cattle')
    images = relationship('CattleImage', back_populates='cattle')
    ownership_history = relationship('CattleOwnershipHistory', back_populates='cattle')
    milk_production_records = relationship('MilkProduction', back_populates='cattle')
    weight_records = relationship('WeightRecord', back_populates='cattle')
    inseminations = relationship('Insemination', back_populates='cattle')
    trades = relationship('Trade', back_populates='cattle')
    favorites = relationship('Favorite', back_populates='cattle')
