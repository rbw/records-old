from starlette.routing import Route

from . import albums

routes = [
    Route("/albums", endpoint=albums.get_many, methods=["GET"]),
    Route("/albums", endpoint=albums.create, methods=["POST"]),
    Route("/albums/{album_upc}", endpoint=albums.get_one, methods=["GET"]),
]
