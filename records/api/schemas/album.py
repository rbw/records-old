from marshmallow import Schema
from marshmallow.fields import String, Date, List, Nested

from .track import TrackSchema


class AlbumSchema(Schema):
    class Meta:
        dump_only = ["tracks"]

    upc = String(required=True)
    title = String(required=True)
    artwork_file = String()
    release_date = Date(required=True)
    tracks = List(Nested(TrackSchema))
    stores = List(String, required=True)


class AlbumsSchema(AlbumSchema):
    class Meta:
        exclude = ["tracks"]
