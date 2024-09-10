from sqlalchemy import Column, BigInteger, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .user import User

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
