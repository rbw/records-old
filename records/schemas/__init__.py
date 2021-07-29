from collections import namedtuple

from .album import AlbumBaseSchema, AlbumListSchema, AlbumNewSchema
from .track import TrackSchema

SchemaCollection = namedtuple("SchemaCollection", ["one", "many", "new"])
album_schemas = SchemaCollection(AlbumBaseSchema, AlbumListSchema, AlbumNewSchema)
