# Records

An example application demonstrating how Starlette can be used with SQLAlchemy to
provide a highly concurrent Web API backend.

**Tech used**
- Python3
- Starlette
- Sqlalchemy (1.4 asyncio)
- Marshmallow


Structure
---

The project has been given a structure suitable for larger project, that hopes
to provide a clear separation between data and presentation layers.

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

Currently, the database is recreated and seeded on startup.



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

The application requires an SQLAlchemy-supported relational database.

A docker-compose file providing a Postgres server can be started from the project root:

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
$ curl -X POST --data '{"title": "test", "release_date": "2035-01-20", 
"stores": ["apple", "youtube"], "upc": "00000000000005"}' http://localhost:5000/albums

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
