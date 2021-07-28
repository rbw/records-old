# Records

An example application demonstrating how Starlette can be used with SQLAlchemy to
create a high-performance, highly concurrent Web API backend.

**Tech used**
- Python3
- Starlette
- Uvicorn
- Sqlalchemy (1.4 asyncio)
- Marshmallow


Structure
---

The project structure and application architecture should be suitable for larger projects. It hopes to provide a good decomposition and clear separation between data and presentation layers.

```
.
├── docker-compose.yml [postgres compose]
├── logging.conf [Python logging config]
├── poetry.lock [Resolved dependencies]
├── pyproject.toml [Project meta]
├── README.md
├── records
│   ├── api
│   │   ├── albums.py [Albums API endpoints]
│   │   ├── __init__.py
│   │   └── schemas [API-related schemas]
│   │       ├── album.py
│   │       ├── artist.py
│   │       ├── __init__.py
│   │       └── track.py
│   ├── app.py
│   ├── db.py [Database interface]
│   ├── errors.py [API errors]
│   ├── exceptions.py
│   ├── __init__.py
│   ├── __main__.py [App entry point]
│   ├── models [ORM Models]
│   │   ├── album.py
│   │   ├── artist.py
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── track.py
│   └── utils.py
└── seed.sql
```

Data persistence
---

Currently, the database is recreated and seeded on application startup.



Setting up
---

Requires Python 3.9+, git and poetry.

**Building**

```
$ git clone https://github.com/rbw/records.git
$ cd records
$ poetry update
```

**Starting Postgres**

The application requires an SQLAlchemy-supported relational database. Currently, it uses pg.ARRAY in AlbumModel, making it compatible Postgres only.

A docker-compose file for running a Postgres server is available in the project root.

```
$ docker-compose up
```

**Starting Records** 

```
$ poetry shell
$ python -m records
```

Usage
---

**Get all albums**
```
$ curl http://localhost:5000/albums
```

**Show an album**
```
$ curl http://localhost:5000/albums/00000000000002
```

**Create an album**
```
$ curl -X POST --data '{"title": "test", "release_date": "2035-01-20", "stores": 
["apple", "youtube"], "upc": "00000000000005"}' http://localhost:5000/albums
```


Todo
---

- Add Tracks API `[GET/POST/DELETE => /tracks,/tracks:trackid:]`
- Implement add-track-to-album `[POST => /albums/:albumid:/tracks]`
- Implement del-track-from-album `[DELETE => /albums/:albumid:/tracks/:trackid:]`
- Implement query filtering
- Project docs
- Code docs
- Automated tests
