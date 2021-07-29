from functools import wraps

from .album import AlbumService


def with_service(service_cls):
    def wrapper(fn):
        @wraps(fn)
        async def handler_fn(req):
            status = 200
            svc = service_cls(req.app.db)
            retval = await fn(req, svc)
            if isinstance(retval, tuple):
                data = retval[0]
                status = retval[1]
            else:
                data = retval

            return svc.json_response(data, status)

        return handler_fn

    return wrapper
