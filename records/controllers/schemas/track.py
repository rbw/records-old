from marshmallow import Schema, validate
from marshmallow.fields import String, Boolean, List, Nested

from records.database.tables import TrackVersion
from .artist import ArtistSchema


class Track(Schema):
    isrc = String(required=True)
    title = String(required=True)
    version = String(validate=validate.OneOf([a.name for a in TrackVersion]))
    explicit = Boolean(required=True)
    audio_file = String(required=True)
    artists = List(Nested(ArtistSchema))


class Tracks(Track):
    class Meta:
        exclude = ["artists"]


class TrackPayload(Track):
    tracks = List(String, load_only=True)
