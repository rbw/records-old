from starlette.routing import Route

from .album import AlbumEndpoint

routes = [
    Route("/albums", endpoint=AlbumEndpoint, methods=["GET", "POST"]),
    Route("/albums/{album_upc}", endpoint=AlbumEndpoint, methods=["GET"]),
]
