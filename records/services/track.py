from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from records.database.service import DatabaseService
from records.database.tables import TrackModel, TrackArtistModel


class TrackService(DatabaseService):
    async def get_one(self, track_id):
        stmt = select(TrackModel).where(TrackModel.isrc == track_id)
        return await self._get_one(stmt)

    async def get_many(self):
        stmt = select(TrackModel)
        return await self._get_many(stmt)

    async def create(self, data):
        tracks = data.pop("tracks", [])
        track = TrackModel(**data)
        async with self.db_session as s:
            # Insert album
            s.add(track)

            # Associate with artists
            [
                s.add(TrackArtistModel(track=track_id, album=track.isrc))
                for track_id in tracks
            ]

            try:
                await s.commit()
            except IntegrityError as e:
                self.log.warning(f"Error creating new track: {e.orig}")
                raise IntegrityError

        return None
