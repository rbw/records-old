import json
from http import HTTPStatus

from starlette.responses import Response
from sqlalchemy.exc import DatabaseError
from records.exceptions import (
    PayloadValidationError,
    NoSuchRecord,
    PayloadDecodeError,
    RequestError,
    IneffectiveDelete,
)


class Error:
    def __init__(self, status, detail=None):
        self.status = status
        self.detail = detail
        self.reason = HTTPStatus(self.status).phrase

    @property
    def __dict__(self):
        return dict(code=self.status, reason=self.reason, message=self.detail)

    @property
    def response(self):
        return Response(
            content=json.dumps(self.__dict__, indent=4), status_code=self.status
        )


async def on_error(_, exc):
    status = 500
    detail = None

    if issubclass(exc.__class__, RequestError):
        detail = exc.detail
        if isinstance(exc, PayloadValidationError):
            status = 422
        elif isinstance(exc, NoSuchRecord):
            status = 404
        elif isinstance(exc, PayloadDecodeError):
            status = 400
            detail = str(detail)
        elif isinstance(exc, IneffectiveDelete):
            status = 400
            detail = str(detail)
    elif isinstance(exc, DatabaseError):
        status = 400
        detail = f"Database operation failed with code {exc.code}"

    return Error(status, detail).response
