import logging
from json.decoder import JSONDecodeError
from typing import Type

from starlette.responses import Response
from marshmallow.schema import Schema, EXCLUDE
from marshmallow.exceptions import ValidationError
from sqlalchemy.engine.result import ScalarResult

from records.models.base import Base
from records.schemas import SchemaCollection
from records.exceptions import (
    PayloadValidationError,
    PayloadDecodeError,
    NoSuchRecord,
    NoDatabaseAccess,
)


class BaseService:
    schemas: SchemaCollection

    def __init__(self, db=None):
        self.db = db
        self.log = logging.getLogger(__name__)

    @property
    def db_session(self):
        if not self.db:
            raise NoDatabaseAccess(f"No database attached to {self}")

        return self.db.make_session()

    @staticmethod
    def deserialize(body, schema: Type[Schema]):
        try:
            return schema(unknown=EXCLUDE).loads(body.decode())
        except ValidationError as e:
            raise PayloadValidationError(e.messages)
        except JSONDecodeError as e:
            raise PayloadDecodeError(e)

    @staticmethod
    def serialize(data, schema_cls, many):
        return schema_cls(many=many).dumps(data, indent=4)

    def json_response(self, data, status):
        if isinstance(data, ScalarResult) and self.schemas.many:
            content = self.serialize(data, self.schemas.many, True)
        elif isinstance(data, Base) and self.schemas.one:
            content = self.serialize(data, self.schemas.one, False)
        else:
            content = data

        return Response(content, status_code=status, media_type="application/json")

    async def get_one(self, stmt):
        async with self.db_session as s:
            result = (await s.execute(stmt)).scalar()
            if not result:
                raise NoSuchRecord("No such record")

            return result

    async def get_many(self, stmt):
        async with self.db_session as s:
            return (await s.execute(stmt)).scalars().unique()
