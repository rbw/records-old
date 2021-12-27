import uvicorn
from os import environ as env

from extras import seed
from .controllers import AlbumController, TrackController
from .app import Application

# Set up config from environment
listen_host, listen_port = env.get("RCRD_LISTEN", "127.0.0.1:5000").split(":")
pg_username = env.get("RCRD_PG_USERNAME", "records")
pg_password = env.get("RCRD_PG_PASSWORD", "all")
pg_address = env.get("RCRD_PG_ADDRESS", "localhost:5432")
pg_database = env.get("RCRD_PG_DATABASE", "records")
log_config = env.get("RCRD_LOG_CONFIG", "logging.conf")
log_debug = env.get("RCRD_LOG_DEBUG", "1") == "1"


def main():
    return Application(
        db_url=f"postgresql+asyncpg://{pg_username}:{pg_password}@{pg_address}/{pg_database}",
        debug=log_debug,
        controllers=[AlbumController, TrackController],
        db_seed=seed,
    )


if __name__ == "__main__":
    uvicorn.run(
        f"{__name__}:main",
        factory=True,
        log_config=log_config,
        host=listen_host,
        port=int(listen_port),
        log_level="debug" if log_debug else "info",
    )
