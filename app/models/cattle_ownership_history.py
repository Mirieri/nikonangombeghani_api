from sqlalchemy import Column, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class CattleOwnershipHistory(Base):
    __tablename__ = 'cattle_ownership_history'

    ownership_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=True)
    previous_owner_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    new_owner_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    ownership_change_date = Column(Date, nullable=True)

    # Relationships
    cattle = relationship('Cattle', back_populates='ownership_history')
    previous_owner = relationship('User', foreign_keys=[previous_owner_id])
    new_owner = relationship('User', foreign_keys=[new_owner_id])
