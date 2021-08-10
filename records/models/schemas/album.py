import enum

from sqlalchemy.dialects import postgresql as pg
from sqlalchemy import Column, ForeignKey, String, Date, Enum
from sqlalchemy.orm import relationship

from records.model import Base


class AlbumStore(enum.Enum):
    SPOTIFY = 1
    YOUTUBE = 2
    APPLE = 3

    def __str__(self):
        return self.name


class AlbumTrackTable(Base):
    __tablename__ = "album_track"

    album = Column(String, ForeignKey("album.upc"), primary_key=True)
    track = Column(String, ForeignKey("track.isrc"), primary_key=True)


class AlbumTable(Base):
    __tablename__ = "album"

    upc = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    artwork_file = Column(String)
    release_date = Column(Date, nullable=False)
    stores = Column(
        pg.ARRAY(Enum(AlbumStore, create_constraint=False, native_enum=False))
    )
    # @TODO: Enable lazy loading of tracks
    tracks = relationship(
        "TrackTable", secondary=AlbumTrackTable.__table__, lazy=False
    )
