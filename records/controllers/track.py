from records.services import TrackService
from records.controller import Controller

from .schemas import track_schemas


class TrackController(Controller):
    svc = TrackService()

    def routes_make(self):
        return "/tracks", [
            ("/", ["GET"], self.get_many),
            ("/", ["POST"], self.create),
            ("/{track_id}", ["GET"], self.get_one),
        ]

    async def get_one(self, req):
        track_id = req.path_params.get("track_isrc")
        item = await self.svc.get_one(track_id)
        return self.json_response(item, 200, track_schemas.one)

    async def get_many(self, _):
        items = await self.svc.get_many()
        return self.json_response(items, 200, track_schemas.many)

    async def create(self, req):
        body = await req.body()
        track = self.deserialize(body, track_schemas.new)
        await self.svc.create(track)
        return self.json_response(None, 201)
