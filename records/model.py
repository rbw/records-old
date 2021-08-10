import logging
from abc import ABC, ABCMeta
from sqlalchemy.ext.declarative import declarative_base

from records.exceptions import (
    NoSuchRecord,
    NoDatabaseAccess,
)


Base = declarative_base()


class ModelMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ModelMeta, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Model(ABC, metaclass=ModelMeta):
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

    async def _insert(self, objects):
        async with self.db_session as s:
            s.add_all(objects)
            await s.commit()

    async def _delete(self, objects):
        async with self.db_session as s:
            async with s.begin():
                for o in objects:
                    await s.delete(o)

    async def _get_one(self, stmt):
        async with self.db_session as s:
            # @TODO: s.one() scalar?
            result = (await s.execute(stmt)).scalar()
            if not result:
                raise NoSuchRecord("No such record")

            return result

    async def _get_many(self, stmt):
        async with self.db_session as s:
            # @TODO: s.many() scalar?
            return (await s.execute(stmt)).scalars().unique()
