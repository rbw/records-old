import uvicorn
from os import environ as env

from . import app_make
from extras import seed

# Set up config from environment
listen_host, listen_port = env.get("RCRD_LISTEN", "127.0.0.1:5000").split(":")
pg_username = env.get("RCRD_PG_USERNAME", "records")
pg_password = env.get("RCRD_PG_PASSWORD", "all")
pg_address = env.get("RCRD_PG_ADDRESS", "localhost:5432")
pg_database = env.get("RCRD_PG_DATABASE", "records")
debug_enable = env.get("RCRD_DEBUG", "1") == "1"


def main():
    return app_make(
        db_url=f"postgresql+asyncpg://{pg_username}:{pg_password}@{pg_address}/{pg_database}",
        debug=debug_enable,
        db_seed=seed
    )


if __name__ == "__main__":
    uvicorn.run(
        f"{__name__}:main",
        factory=True,
        log_config="logging.conf",
        host=listen_host,
        port=int(listen_port),
        log_level="debug" if debug_enable else "info",
    )
