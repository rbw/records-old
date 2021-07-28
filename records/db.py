import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from records.models.base import Base
from records.exceptions import DatabaseInsertError, NoSuchRecord


log = logging.getLogger(__name__)


class Database:
    def __init__(self, url, debug):
        # Create engine with logging of sql statements
        self.engine = create_async_engine(url, echo=debug)

        # Create session with `expire_on_commit` set to False, as we don't want SQLAlchemy
        # to issue new SQL queries to the database when accessing already committed objects
        self.make_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def __aenter__(self):
        return self.make_session()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_one(self, stmt):
        async with self.make_session() as s:
            content = (await s.execute(stmt)).scalar()
            if not content:
                raise NoSuchRecord("No such record")

            return content

    async def get_list(self, stmt):
        async with self.make_session() as s:
            return (await s.execute(stmt)).scalars().unique()

    async def insert(self, obj):
        async with self.make_session() as session:
            session.add(obj)
            try:
                await session.commit()
            except IntegrityError as e:
                log.warning(f"Error creating new record: {e.orig}")
                raise DatabaseInsertError(e.orig.__class__.__name__)

    async def reset(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

            # @TODO: Load seed from JSON file and bulk-insert via ORM instead
            with open("seed.sql") as file:
                for line in file.read().split("\n"):
                    if not line.strip():
                        continue
                    await conn.execute(text(line))
