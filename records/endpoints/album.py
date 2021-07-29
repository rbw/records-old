from sqlalchemy import select

from records.models import AlbumModel
from records.services import AlbumService, with_service


@with_service(AlbumService)
async def get_many(_, svc):
    stmt = select(AlbumModel)
    return await svc.get_many(stmt)


@with_service(AlbumService)
async def get_one(req, svc):
    stmt = select(AlbumModel).where(AlbumModel.upc == req.path_params["album_upc"])
    return await svc.get_one(stmt)


@with_service(AlbumService)
async def create(req, svc):
    album = await req.body()
    return await svc.create(album), 201
