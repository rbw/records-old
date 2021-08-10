from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from records.model import Model
from .schemas import TrackTable, TrackArtistTable


class TrackModel(Model):
    async def get_one(self, track_id):
        stmt = select(TrackTable).where(TrackTable.isrc == track_id)
        return await self._get_one(stmt)

    async def get_many(self):
        stmt = select(TrackTable)
        return await self._get_many(stmt)

    async def create(self, data):
        tracks = data.pop("tracks", [])
        track = TrackTable(**data)
        async with self.db_session as s:
            # Insert album
            s.add(track)

            # Associate with artists
            [
                s.add(TrackArtistTable(track=track_id, album=track.isrc))
                for track_id in tracks
            ]

            try:
                await s.commit()
            except IntegrityError as e:
                self.log.warning(f"Error creating new track: {e.orig}")
                raise IntegrityError

        return None
