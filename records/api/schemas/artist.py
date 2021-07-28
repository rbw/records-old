from marshmallow import Schema
from marshmallow.fields import Integer, String


class ArtistSchema(Schema):
    id = Integer(required=True)
    role = String(required=True)
    name = String(required=True)
