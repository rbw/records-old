from marshmallow import Schema, validate
from marshmallow.fields import String, Date, List, Nested

from records.models.album import AlbumStore
from .track import TrackSchema


class AlbumBaseSchema(Schema):
    upc = String(required=True)
    title = String(required=True)
    artwork_file = String()
    release_date = Date(required=True)
    tracks = List(Nested(TrackSchema), dump_only=True)
    stores = List(String(validate=validate.OneOf([a.name for a in AlbumStore])))


class AlbumListSchema(AlbumBaseSchema):
    class Meta:
        exclude = ["tracks"]


class AlbumNewSchema(AlbumBaseSchema):
    tracks = List(String, load_only=True)
