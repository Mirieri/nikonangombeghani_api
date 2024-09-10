from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, DECIMAL, func
from sqlalchemy.orm import relationship
from .database import Base
from .cattle import Cattle
from .user import User

class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    seller_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    buyer_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    cattle_id = Column(BigInteger, ForeignKey('cattle.cattle_id', ondelete="CASCADE"), nullable=False)
    trade_date = Column(DateTime, server_default=func.now())
    price = Column(DECIMAL(10, 2), nullable=False)  # Price in currency

    # Relationships
    cattle = relationship('Cattle', back_populates='trades')
    seller = relationship('User', foreign_keys=[seller_id], back_populates='trades_as_seller')
    buyer = relationship('User', foreign_keys=[buyer_id], back_populates='trades_as_buyer')
