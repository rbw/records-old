from records.services import AlbumService
from records.controller import Controller

from .schemas import Album, Albums, AlbumPayload


class AlbumController(Controller):
    def __init__(self):
        self.alb = AlbumService(self.app)

    def routes_make(self):
        return "/albums", [
            ("/", "GET", self.albums_get),
            ("/", "POST", self.album_create),
            ("/{album_id}", "GET", self.album_get),
            ("/{album_id}/tracks/{track_id}", "POST", self.track_add),
            ("/{album_id}/tracks/{track_id}", "DELETE", self.track_remove),
        ]

    async def album_get(self, req):
        item = await self.alb.get_one(album_id=req.path_params["album_id"])
        return self.json_response(item, 200, Album)

    async def albums_get(self, _):
        items = await self.alb.get_many()
        return self.json_response(items, 200, Albums)

    async def album_create(self, req):
        body = await req.body()
        album = self.deserialize(body, AlbumPayload)
        tracks = album.pop("tracks", [])
        await self.alb.create(album, tracks)
        return self.json_response(None, 201)

    async def track_add(self, req):
        await self.alb.track_add(
            album_id=req.path_params["album_id"], track_id=req.path_params["track_id"]
        )
        return self.json_response(None, 201)

    async def track_remove(self, req):
        await self.alb.track_remove(
            album_id=req.path_params["album_id"], track_id=req.path_params["track_id"]
        )
        return self.json_response(None, 204)
