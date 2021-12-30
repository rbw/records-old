from marshmallow import Schema, validate
from marshmallow.fields import String, Date, List, Nested

from records.database.tables import AlbumStore
from .track import Track


class Album(Schema):
    upc = String(required=True)
    title = String(required=True)
    artwork_file = String()
    release_date = Date(required=True)
    tracks = List(Nested(Track), dump_only=True)
    stores = List(String(validate=validate.OneOf([a.name for a in AlbumStore])))


class Albums(Album):
    class Meta:
        exclude = ["tracks"]


class AlbumPayload(Album):
    tracks = List(String, load_only=True)
