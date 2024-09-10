from sqlalchemy import Column, BigInteger, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from .database import Base

class Insemination(Base):
    __tablename__ = 'insemination'

    insemination_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=False)
    insemination_date = Column(Date, nullable=False)
    insemination_method = Column(String(100), nullable=True)
    bull_id = Column(BigInteger, nullable=True)  # Reference to the bull, if applicable

    # Relationships
    cattle = relationship('Cattle', back_populates='inseminations')
