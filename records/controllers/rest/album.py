from records.models import AlbumModel
from records.controller import Controller

from .schemas import Album, Albums, AlbumPayload


class AlbumController(Controller):
    model = AlbumModel()

    def routes_make(self):
        return "/albums", [
            ("/", "GET", self.albums_get),
            ("/", "POST", self.album_create),
            ("/{album_id}", "GET", self.album_get),
        ]

    async def album_get(self, req):
        item = await self.model.album_get(album_id=req.path_params["album_id"])
        return self.json_response(item, 200, Album)

    async def albums_get(self, _):
        items = await self.model.albums_get()
        return self.json_response(items, 200, Albums)

    async def album_create(self, req):
        body = await req.body()
        album = self.deserialize(body, AlbumPayload)
        tracks = album.pop("tracks", [])
        await self.model.album_create(album, tracks)
        return self.json_response(None, 201)


class AlbumTrackController(Controller):
    model = AlbumModel()

    def routes_make(self):
        return "/albums/{album_id}/tracks", [
            ("/{track_id}", "POST", self.track_add),
            ("/{track_id}", "DELETE", self.track_remove),
        ]

    async def track_add(self, req):
        await self.model.track_add(
            album_id=req.path_params["album_id"], track_id=req.path_params["track_id"]
        )
        return self.json_response(None, 201)

    async def track_remove(self, req):
        await self.model.track_remove(
            album_id=req.path_params["album_id"], track_id=req.path_params["track_id"]
        )
        return self.json_response(None, 204)
