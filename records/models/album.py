import enum

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, ForeignKey, String, Date, Enum
from sqlalchemy.orm import relationship

from .base import Base


class Store(enum.Enum):
    spotify = 1
    youtube = 2
    apple = 3


class AlbumTrack(Base):
    __tablename__ = "album_track"

    album = Column(String, ForeignKey("album.upc"), primary_key=True)
    track = Column(String, ForeignKey("track.isrc"), primary_key=True)


class AlbumModel(Base):
    __tablename__ = "album"

    upc = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    artwork_file = Column(String)
    release_date = Column(Date, nullable=False)
    stores = Column(pg.ARRAY(Enum(Store, create_constraint=False, native_enum=False)))
    tracks = relationship("TrackModel", secondary=AlbumTrack.__table__, lazy=False)
