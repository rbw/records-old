from abc import abstractmethod
from json.decoder import JSONDecodeError
from typing import Type, Any

from sqlalchemy.engine import ScalarResult
from starlette.requests import Request
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response
from marshmallow.schema import Schema, EXCLUDE
from marshmallow.exceptions import ValidationError
from records.exceptions import (
    PayloadValidationError,
    PayloadDecodeError,
)


class BaseEndpoint(HTTPEndpoint):
    @property
    @abstractmethod
    def service_cls(self):
        pass

    async def dispatch(self) -> None:
        request = Request(self.scope, receive=self.receive)
        handler_name = "get" if request.method == "HEAD" else request.method.lower()
        handler = getattr(self, handler_name, self.method_not_allowed)
        service = self.service_cls(request.app)
        response = await handler(request, service)
        await response(self.scope, self.receive, self.send)

    @staticmethod
    def deserialize(data: Any, schema: Type[Schema]):
        try:
            return schema(unknown=EXCLUDE).loads(data.decode())
        except ValidationError as e:
            raise PayloadValidationError(e.messages)
        except JSONDecodeError as e:
            raise PayloadDecodeError(e)

    @staticmethod
    def serialize(data: Any, schema: Type[Schema], many: bool):
        return schema(many=many).dumps(data, indent=4)

    def json_response(self, data, status, schema=None):
        content = self.serialize(data, schema, many=isinstance(data, ScalarResult)) if schema else data
        return Response(content, status_code=status, media_type="application/json")
