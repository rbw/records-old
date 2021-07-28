from sqlalchemy import select

from records.models import AlbumModel
from records.utils import body_deserialize, response_json
from .schemas import AlbumSchema, AlbumsSchema


async def get_many(request):
    stmt = select(AlbumModel)
    result = await request.app.db.get_list(stmt)
    return response_json(result, schema=AlbumsSchema, many=True)


async def get_one(request):
    stmt = select(AlbumModel).where(AlbumModel.upc == request.path_params["album_upc"])
    result = await request.app.db.get_one(stmt)
    return response_json(result, schema=AlbumSchema)


async def create(request):
    data = await request.body()
    album = AlbumModel(**body_deserialize(data, AlbumSchema))
    await request.app.db.insert(album)
    return response_json(None, status=201)
