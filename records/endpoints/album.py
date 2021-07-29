from records.services import AlbumService
from records.schemas import album_schemas
from records.endpoint import BaseEndpoint


class AlbumEndpoint(BaseEndpoint):
    service_cls = AlbumService

    async def get(self, req, svc):
        if album_id := req.path_params.get("album_upc"):
            item = await svc.get_one(album_id)
            return self.json_response(item, 200, album_schemas.one)

        items = await svc.get_many()
        return self.json_response(items, 200, album_schemas.many)

    async def post(self, req, svc):
        body = await req.body()
        album = self.deserialize(body, album_schemas.new)
        await svc.create(album)
        return self.json_response(None, 201)
