from datetime import date

from records.models.schemas import (
    TrackTable,
    TrackVersion,
    ArtistRole,
    ArtistTable,
    AlbumTable,
    AlbumStore,
)

artists = [
    ArtistTable(id=1, name="Singer Sam", role=ArtistRole.SINGER),
    ArtistTable(id=2, name="Bassist Bob", role=ArtistRole.BASSIST),
    ArtistTable(id=3, name="Drummer Don", role=ArtistRole.DRUMMER),
    ArtistTable(id=4, name="Singer Simpson", role=ArtistRole.SINGER),
]

tracks = [
    TrackTable(
        isrc="TEST000000001",
        title="Test Track #1",
        version=TrackVersion.RADIO,
        explicit=True,
        audio_file="track1.mp3",
        artists=artists[1:3],
    ),
    TrackTable(
        isrc="TEST000000002",
        title="Test Track #2",
        version=TrackVersion.ORIGINAL,
        explicit=True,
        audio_file="track2.mp3",
        artists=[artists[0], artists[3]],
    ),
    TrackTable(
        isrc="TEST000000003",
        title="Test Track #3",
        version=TrackVersion.ORIGINAL,
        explicit=False,
        audio_file="track3.mp3",
        artists=artists[3:4],
    ),
]

albums = [
    AlbumTable(
        upc="00000000000001",
        title="Test Album #1",
        artwork_file="album1.jpg",
        release_date=date.fromisoformat("2020-03-01"),
        stores=[AlbumStore.APPLE, AlbumStore.SPOTIFY, AlbumStore.YOUTUBE],
        tracks=tracks[0:2],
    ),
    AlbumTable(
        upc="00000000000002",
        title="Test Album #2",
        artwork_file="album2.jpg",
        release_date=date.fromisoformat("2035-08-01"),
        stores=[AlbumStore.APPLE, AlbumStore.YOUTUBE],
        tracks=tracks[2:3],
    ),
    AlbumTable(
        upc="00000000000003",
        title="Test Album #3",
        artwork_file="album3.jpg",
        release_date=date.fromisoformat("2025-02-01"),
        stores=[AlbumStore.SPOTIFY],
        tracks=[tracks[0], tracks[2]],
    ),
]
