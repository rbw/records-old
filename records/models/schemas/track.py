import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from records.model import Base


class TrackVersion(enum.Enum):
    RADIO = 1
    ORIGINAL = 2

    def __str__(self):
        return self.name


class TrackArtistTable(Base):
    __tablename__ = "track_artist"

    artist = Column(Integer, ForeignKey("artist.id"), primary_key=True)
    track = Column(String, ForeignKey("track.isrc"), primary_key=True)


class TrackTable(Base):
    __tablename__ = "track"

    isrc = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    version = Column(Enum(TrackVersion))
    explicit = Column(Boolean, nullable=False)
    audio_file = Column(String, nullable=False)
    artists = relationship(
        "ArtistTable", secondary=TrackArtistTable.__table__, lazy=False
    )
