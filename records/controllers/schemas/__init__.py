from collections import namedtuple

from .album import AlbumBaseSchema, AlbumListSchema, AlbumNewSchema
from .track import TrackBaseSchema, TrackListSchema, TrackNewSchema

SchemaCollection = namedtuple("SchemaCollection", ["one", "many", "new"])
album_schemas = SchemaCollection(AlbumBaseSchema, AlbumListSchema, AlbumNewSchema)
track_schemas = SchemaCollection(TrackBaseSchema, TrackListSchema, TrackNewSchema)
