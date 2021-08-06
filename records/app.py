import logging.config

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware


from records.controllers import controllers_enabled
from records.db import Database
from records.exceptions import RequestError
from records.errors import request_error


class Application(Starlette):
    log = logging.getLogger("records")

    def __init__(self, db_url, *args, debug=False, **kwargs):
        logging.config.fileConfig(
            "logging.conf",
            defaults={"level": "DEBUG" if debug else "INFO"},
            disable_existing_loggers=True,
        )

        super(Application, self).__init__(*args, **kwargs)

        # Initialize database
        self.db = Database(db_url, debug)

        # Init controllers
        for ctrl_cls in controllers_enabled:
            ep = ctrl_cls(app=self)
            path_base, routes = ep.routes_make()
            # Load routes
            for path_rel, methods, handler in routes:
                path_rel = path_rel.rstrip("/")
                self.add_route(path_base + path_rel, handler, methods)

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

    async def on_app_stop(self):
        pass
