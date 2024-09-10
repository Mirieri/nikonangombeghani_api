from sqlalchemy import Column, BigInteger, Date, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .database import Base
from .cattle import GenderEnum

class Calving(Base):
    __tablename__ = 'calving'

    calving_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=True)
    calving_date = Column(Date, nullable=True)
    calf_gender = Column(SQLEnum(GenderEnum), nullable=True)
    calf_health_status = Column(String(100), nullable=True)

    # Relationships
    cattle = relationship('Cattle', back_populates='calvings')
