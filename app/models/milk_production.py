from sqlalchemy import Column, BigInteger, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base
from .cattle import Cattle

class MilkProduction(Base):
    __tablename__ = 'milk_production'

    production_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=False)
    production_date = Column(Date, nullable=False)
    volume = Column(DECIMAL(10, 2), nullable=False)  # Volume in liters

    # Relationships
    cattle = relationship('Cattle', back_populates='milk_production_records')
