from starlette.routing import Route

from . import album

routes = [
    Route("/albums", endpoint=album.get_many, methods=["GET"]),
    Route("/albums", endpoint=album.create, methods=["POST"]),
    Route("/albums/{album_upc}", endpoint=album.get_one, methods=["GET"]),
]
