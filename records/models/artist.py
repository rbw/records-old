from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .track import TrackArtist


class ArtistModel(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=False)
    name = Column(String, nullable=False)
    albums = relationship(
        "TrackModel", secondary=TrackArtist.__table__, back_populates="artists"
    )
