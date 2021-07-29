from sqlalchemy.exc import IntegrityError

from records.exceptions import DatabaseInsertError
from records.schemas import album_schemas
from records.models import AlbumModel, AlbumTrackModel
from .base import BaseService


class AlbumService(BaseService):
    schemas = album_schemas

    async def create(self, obj):
        body = self.deserialize(obj, self.schemas.new)
        tracks = body.pop("tracks", [])
        album = AlbumModel(**body)
        async with self.db_session as s:
            # Insert album
            s.add(album)

            # Associate with tracks
            [
                s.add(
                    AlbumTrackModel(track=track_id, album=album.upc)
                )
                for track_id in tracks
            ]

            try:
                await s.commit()
            except IntegrityError as e:
                self.log.warning(f"Error creating new record: {e.orig}")
                raise DatabaseInsertError(e.orig.__class__.__name__)

        return None
