import logging
from records.exceptions import (
    NoSuchRecord,
    NoDatabaseAccess,
)


class BaseService:
    def __init__(self, app):
        self.db = app.db
        self.log = logging.getLogger(__name__)

    @property
    def db_session(self):
        if not self.db:
            raise NoDatabaseAccess(f"No database attached to {self}")

        return self.db.make_session()

    async def _get_one(self, stmt):
        async with self.db_session as s:
            result = (await s.execute(stmt)).scalar()
            if not result:
                raise NoSuchRecord("No such record")

            return result

    async def _get_many(self, stmt):
        async with self.db_session as s:
            return (await s.execute(stmt)).scalars().unique()
