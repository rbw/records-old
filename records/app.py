from enum import Enum
import logging.config

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from records.controllers import controllers_enabled
from records.db import Database
from records.exceptions import RequestError
from records.errors import request_error


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Application(Starlette):
    log = logging.getLogger("records")

    def __init__(self, db_url, *args, debug=False, db_seed=None, **kwargs):
        logging.config.fileConfig(
            "logging.conf",
            defaults={"level": "DEBUG" if debug else "INFO"},
            disable_existing_loggers=True,
        )

        super(Application, self).__init__(*args, **kwargs)

        # Set module to seed from
        self.seed = db_seed

        # Initialize database
        self.db = Database(db_url, debug)

        # Init controllers
        for ctrl_cls in controllers_enabled:
            ep = ctrl_cls(app=self)
            path_base, routes = ep.routes_make()

            # Load routes
            for path_rel, method, handler in routes:
                method = HttpMethod(method.upper()).value
                path = path_base + path_rel.rstrip("/")
                self.log.info(f"Adding route: {method} {path} [{handler}]")
                self.add_route(path, handler, [method])

        # Set up CORS
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Event handlers
        self.add_event_handler("startup", self.on_app_start)
        self.add_event_handler("shutdown", self.on_app_stop)

        # Error handlers
        self.add_exception_handler(RequestError, request_error)
        self.add_exception_handler(Exception, request_error)

    async def on_app_start(self):
        await self.db.reset()

        if self.seed:
            await self.db.seed_load(self.seed)

    async def on_app_stop(self):
        pass
