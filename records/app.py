import logging.config

from sqlalchemy.exc import DatabaseError
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from records.database import DatabaseManager
from records.exceptions import RequestError
from records.errors import on_error
from records.protocol import HttpMethod
from records.database import db_reset


class Application(Starlette):
    log = logging.getLogger("records")

    def __init__(self, db_url, controllers, *args, debug=False, db_seed=None, **kwargs):
        logging.config.fileConfig(
            "logging.conf",
            defaults={"level": "DEBUG" if debug else "INFO"},
            disable_existing_loggers=True,
        )

        super(Application, self).__init__(*args, **kwargs)

        # Register controllers with app
        for ctrl_cls in controllers:
            self._controller_register(ctrl_cls)

        # Set module to seed from
        self.seed = db_seed

        # Initialize database
        self.db = DatabaseManager(db_url, debug)

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
        self.add_exception_handler(RequestError, on_error)
        self.add_exception_handler(DatabaseError, on_error)
        self.add_exception_handler(Exception, on_error)

    def _controller_register(self, ctrl_cls):
        ctrl = ctrl_cls.init(app=self)
        path_base, routes = ctrl.routes_make()

        # Load routes
        for path_rel, method, handler in routes:
            method = HttpMethod(method.upper()).value
            path = path_base + path_rel.rstrip("/")
            self.log.info(f"Adding route: {method} {path} [{handler}]")
            self.add_route(path, handler, [method])

    async def on_app_start(self):
        # @TODO Move to cli
        await db_reset(self.db)

        if self.seed:
            await self.db.seed_load(self.seed)

    async def on_app_stop(self):
        pass
