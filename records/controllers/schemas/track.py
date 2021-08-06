from marshmallow import Schema, validate
from marshmallow.fields import String, Boolean, List, Nested

from records.models.track import TrackVersion
from .artist import ArtistSchema


class TrackBaseSchema(Schema):
    isrc = String(required=True)
    title = String(required=True)
    version = String(validate=validate.OneOf([a.name for a in TrackVersion]))
    explicit = Boolean(required=True)
    audio_file = String(required=True)
    artists = List(Nested(ArtistSchema))


class TrackListSchema(TrackBaseSchema):
    class Meta:
        exclude = ["artists"]


class TrackNewSchema(TrackBaseSchema):
    tracks = List(String, load_only=True)
