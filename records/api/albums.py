from sqlalchemy import select

from records.models import AlbumModel, AlbumTrackModel
from records.utils import body_deserialize, response_json
from .schemas import AlbumBaseSchema, AlbumListSchema, AlbumNewSchema


async def get_many(request):
    stmt = select(AlbumModel)
    result = await request.app.db.get_list(stmt)
    return response_json(result, schema=AlbumListSchema, many=True)


async def get_one(request):
    stmt = select(AlbumModel).where(AlbumModel.upc == request.path_params["album_upc"])
    result = await request.app.db.get_one(stmt)
    return response_json(result, schema=AlbumBaseSchema)


async def create(request):
    data = await request.body()
    loaded = body_deserialize(data, AlbumNewSchema)
    tracks = loaded.pop("tracks")

    # Insert album
    await request.app.db.insert(AlbumModel(**loaded))

    # Associate with tracks
    [
        await request.app.db.insert(
            AlbumTrackModel(track=track_id, album=loaded["upc"])
        )
        for track_id in tracks
    ]

    return response_json(None, status=201)
