from .manager import DatabaseManager
from .service import DatabaseService
from .table import BaseModel


async def db_reset(db):
    async with db.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
