import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from records.model import Model
from .track import TrackArtistModel


class ArtistRole(enum.Enum):
    SINGER = 1
    DRUMMER = 2
    BASSIST = 3

    def __str__(self):
        return self.name


class ArtistModel(Model):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Enum(ArtistRole))
    name = Column(String, nullable=False)
    albums = relationship(
        "TrackModel", secondary=TrackArtistModel.__table__, back_populates="artists"
    )
