from sqlalchemy import select, delete
from sqlalchemy.exc import DatabaseError

from records.model import Model
from .schemas import AlbumTable, AlbumTrackTable


class AlbumModel(Model):
    async def album_get(self, album_id):
        stmt = select(AlbumTable).where(AlbumTable.upc == album_id)
        return await self._get_one(stmt)

    async def albums_get(self):
        stmt = select(AlbumTable)
        return await self._get_many(stmt)

    async def album_create(self, data, tracks):
        album = AlbumTable(**data)
        album_tracks = [
            AlbumTrackTable(track=track_id, album=album.upc) for track_id in tracks
        ]

        try:
            await self._insert([album, *album_tracks])
        except DatabaseError as e:
            self.log.warning(f"Error creating album: {e.orig}")
            raise

    async def track_add(self, album_id, track_id):
        try:
            await self._insert([AlbumTrackTable(album=album_id, track=track_id)])
        except DatabaseError as e:
            self.log.warning(f"Error adding track to album: {e}")
            raise

    async def track_remove(self, album_id, track_id):
        stmt = delete(AlbumTrackTable).where(
            AlbumTrackTable.album == album_id, AlbumTrackTable.track == track_id
        )

        async with self.db_session as s:
            async with s.begin():
                await s.execute(stmt)

        """async with self.db_session as s:
            await self._delete()
            try:
                await s.commit()
            except DatabaseError as e:
                self.log.warning(f"Error removing track from album: {e.orig}")
                raise"""
