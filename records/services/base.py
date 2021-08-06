import logging
from records.exceptions import (
    NoSuchRecord,
    NoDatabaseAccess,
)


class ServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ServiceMeta, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class BaseService(metaclass=ServiceMeta):
    app = None

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def bind(self, app):
        self.app = app

    @property
    def db_session(self):
        if not self.app.db:
            raise NoDatabaseAccess(f"No database attached to {self}")

        return self.app.db.make_session()

    async def _get_one(self, stmt):
        async with self.db_session as s:
            result = (await s.execute(stmt)).scalar()
            if not result:
                raise NoSuchRecord("No such record")

            return result

    async def _get_many(self, stmt):
        async with self.db_session as s:
            return (await s.execute(stmt)).scalars().unique()
