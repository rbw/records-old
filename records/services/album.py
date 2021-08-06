from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from records.exceptions import DatabaseInsertError
from records.models import AlbumModel, AlbumTrackModel
from records.service import Service


class AlbumService(Service):
    async def get_one(self, album_id):
        stmt = select(AlbumModel).where(AlbumModel.upc == album_id)
        return await self._get_one(stmt)

    async def get_many(self):
        stmt = select(AlbumModel)
        return await self._get_many(stmt)

    async def create(self, data):
        tracks = data.pop("tracks", [])
        album = AlbumModel(**data)
        async with self.db_session as s:
            # Insert album
            s.add(album)

            # Associate with tracks
            [
                s.add(AlbumTrackModel(track=track_id, album=album.upc))
                for track_id in tracks
            ]

            try:
                await s.commit()
            except IntegrityError as e:
                self.log.warning(f"Error creating new album: {e.orig}")
                raise DatabaseInsertError(e.orig.__class__.__name__)

        return None
