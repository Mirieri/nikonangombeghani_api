from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

class CattleImage(Base):
    __tablename__ = 'cattle_images'

    image_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())

    # Relationships
    cattle = relationship('Cattle', back_populates='images')
