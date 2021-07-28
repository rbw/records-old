import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from .base import Base


class Version(enum.Enum):
    radio = 1
    original = 2


class TrackArtist(Base):
    __tablename__ = "track_artist"

    artist = Column(Integer, ForeignKey("artist.id"), primary_key=True)
    track = Column(String, ForeignKey("track.isrc"), primary_key=True)


class TrackModel(Base):
    __tablename__ = "track"

    isrc = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    version = Column(Enum(Version, create_constraint=False, native_enum=False))
    explicit = Column(Boolean, nullable=False)
    audio_file = Column(String, nullable=False)
    artists = relationship("ArtistModel", secondary=TrackArtist.__table__, lazy=False)
