from sqlalchemy import select, delete
from sqlalchemy.exc import DatabaseError

from records.exceptions import IneffectiveDelete
from records.database.service import DatabaseService
from records.database.tables import AlbumModel, AlbumTrackModel


class AlbumService(DatabaseService):
    async def get_one(self, album_id):
        stmt = select(AlbumModel).where(AlbumModel.upc == album_id)
        return await self._get_one(stmt)

    async def get_many(self):
        stmt = select(AlbumModel)
        return await self._get_many(stmt)

    async def create(self, data, tracks):
        album = AlbumModel(**data)
        album_tracks = [
            AlbumTrackModel(track=track_id, album=album.upc) for track_id in tracks
        ]

        try:
            await self._insert([album, *album_tracks])
        except DatabaseError as e:
            self.log.warning(f"Error creating album: {e.orig}")
            raise

    async def track_add(self, album_id, track_id):
        try:
            await self._insert([AlbumTrackModel(album=album_id, track=track_id)])
        except DatabaseError as e:
            self.log.warning(f"Error adding track to album: {e}")
            raise

    async def track_remove(self, album_id, track_id):
        stmt = delete(AlbumTrackModel).where(
            AlbumTrackModel.album == album_id, AlbumTrackModel.track == track_id
        )

        try:
            await self._delete(stmt)
        except IneffectiveDelete as e:
            self.log.warning(f"Error removing track from album: {e}")
            raise
