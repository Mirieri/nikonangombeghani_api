from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class Favorite(Base):
    __tablename__ = 'favorites'

    favorite_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    client_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Define relationships
    user = relationship('User', back_populates='favorites', foreign_keys=[client_id])
    cattle = relationship('Cattle', back_populates='favorites')

