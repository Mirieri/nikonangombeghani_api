from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Pedigree(Base):
    __tablename__ = "pedigree"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey("cattle.cattle_id"), nullable=False)
    dam_id = Column(BigInteger, ForeignKey("cattle.cattle_id"), nullable=True)
    sire_id = Column(BigInteger, ForeignKey("cattle.cattle_id"), nullable=True)

    # Relationships
    cattle = relationship("Cattle", foreign_keys=[cattle_id], back_populates='pedigrees')
    dam = relationship("Cattle", foreign_keys=[dam_id], back_populates='offspring_dam')
    sire = relationship("Cattle", foreign_keys=[sire_id], back_populates='offspring_sire')
