from records.service import BaseService, ServiceMeta
from records.exceptions import (
    NoSuchRecord,
    NoDatabaseAccess,
    IneffectiveDelete
)


class DatabaseService(BaseService, metaclass=ServiceMeta):
    @property
    def db_session(self):
        if not self.app.db:
            raise NoDatabaseAccess(f"No database attached to {self}")

        return self.app.db.make_session()

    async def _insert(self, items):
        async with self.db_session as s:
            s.add_all(items)
            await s.commit()

    async def _delete(self, stmt):
        async with self.db_session as s:
            async with s.begin():
                result = await s.execute(stmt)
                if result.rowcount == 0:
                    raise IneffectiveDelete("Ineffective delete")

    async def _get_one(self, stmt):
        async with self.db_session as s:
            result = (await s.execute(stmt)).scalar()
            if not result:
                raise NoSuchRecord("No such record")

            return result

    async def _get_many(self, stmt):
        async with self.db_session as s:
            return (await s.execute(stmt)).scalars().unique()
