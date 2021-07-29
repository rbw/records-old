from marshmallow import Schema
from marshmallow.fields import String, Boolean, List, Nested

from .artist import ArtistSchema


class TrackSchema(Schema):
    isrc = String(required=True)
    title = String(required=True)
    version = String()
    explicit = Boolean(required=True)
    audio_file = String(required=True)
    artists = List(Nested(ArtistSchema))
