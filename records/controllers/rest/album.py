from records.services import AlbumService
from records.controller import Controller

from .schemas import album_schemas


class AlbumController(Controller):
    svc = AlbumService()

    def routes_make(self):
        return "/albums", [
            ("/", "GET", self.get_many),
            ("/", "POST", self.create),
            ("/{album_id}", "GET", self.get_one),
            ("/{album_id}/tracks", "POST", None),
            ("/{album_id}/tracks/{track_id}", "DELETE", None),
        ]

    async def get_one(self, req):
        album_id = req.path_params.get("album_id")
        item = await self.svc.get_one(album_id)
        return self.json_response(item, 200, album_schemas.one)

    async def get_many(self, _):
        items = await self.svc.get_many()
        return self.json_response(items, 200, album_schemas.many)

    async def create(self, req):
        body = await req.body()
        album = self.deserialize(body, album_schemas.new)
        await self.svc.create(album)
        return self.json_response(None, 201)
