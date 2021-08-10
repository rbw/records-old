import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from records.model import Base
from .track import TrackArtistTable


class ArtistRole(enum.Enum):
    SINGER = 1
    DRUMMER = 2
    BASSIST = 3

    def __str__(self):
        return self.name


class ArtistTable(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Enum(ArtistRole))
    name = Column(String, nullable=False)
    albums = relationship(
        "TrackTable", secondary=TrackArtistTable.__table__, back_populates="artists"
    )
