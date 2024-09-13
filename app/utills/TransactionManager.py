from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

class TransactionManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def __aenter__(self):
        await self.db.begin()
        return self.db

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self.db.commit()
        else:
            await self.db.rollback()
        # Ensure the session is closed properly
        await self.db.close()
