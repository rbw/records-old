from json.decoder import JSONDecodeError

from starlette.responses import Response
from marshmallow.schema import EXCLUDE
from marshmallow.exceptions import ValidationError

from records.exceptions import PayloadValidationError, PayloadDecodeError


def body_deserialize(body, schema_cls):
    try:
        return schema_cls(unknown=EXCLUDE).loads(body.decode())
    except ValidationError as e:
        raise PayloadValidationError(e.messages)
    except JSONDecodeError as e:
        raise PayloadDecodeError(e)


def response_json(data, schema=None, status=200, **schema_kwargs):
    content = schema(**schema_kwargs).dumps(data, indent=4) if schema else data
    return Response(content, status_code=status, media_type="application/json")
