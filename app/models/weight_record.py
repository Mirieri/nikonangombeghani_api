from sqlalchemy import Column, BigInteger, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base

class WeightRecord(Base):
    __tablename__ = 'weight_records'

    weight_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=False)
    weight_date = Column(Date, nullable=False)
    weight = Column(DECIMAL(10, 2), nullable=False)  # Weight in kg

    # Relationships
    cattle = relationship('Cattle', back_populates='weight_records')
