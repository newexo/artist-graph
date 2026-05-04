# Artist Graph

A Python library for creating graphs of artists and collaborators. Built on
NetworkX, it creates annotated graphs whose nodes are people and works of art.
Examples include:

- Movies and the actors, writers, directors and producers who make them
- Citation graphs of scholars and their academic papers
- Music and the musicians, composers and producers who create it
- Open source software projects and their contributors

## TMDb Integration

The `cinema_data_providers` package provides an async client for the
[TMDb API](https://www.themoviedb.org/documentation/api):

- **`TMDbClient`** -- async HTTP client for searching people, movies, credits
- **`CachedTMDbClient`** -- wraps `TMDbClient` with SQLAlchemy-backed caching
  (person, movie, and credit tables). The caller provides the database engine.
- **`MovieFilter`** -- client-side filtering for movies by language, rating,
  vote count, popularity, and genre

See [docs/tmdb_fields.md](docs/tmdb_fields.md) for field descriptions and
typical value ranges.

### Cache behaviour

Movie casts are essentially immutable once fetched. Actor filmographies grow
over time. The cache tracks this with `has_full_cast` and
`has_full_filmography` flags, and both `get_movie_cast` and
`get_person_movies` accept a `trust_cache` parameter:

- `get_movie_cast(movie_id, trust_cache=True)` -- trusts cache by default
- `get_person_movies(person_id, trust_cache=False)` -- hits API by default

## Installation

```bash
pip install art-graph
```

Or from source:

```bash
poetry install
```

## Development

```bash
poetry install --with dev
```

### Make targets

| Target | Description |
|---|---|
| `make test` | Run the test suite |
| `make lint` | Lint with ruff |
| `make format` | Format with ruff |
| `make check` | Format + lint + test |

### Running tests

```bash
make test
```

## Acknowledgements

This project began with code originally part of the
[Cinema Game](https://github.com/ChiPowers/cinema_game) project, developed by
Chivon Powers and Reuben Brasher.

Movie and actor data provided by [TMDb](https://www.themoviedb.org). This
product uses the TMDb API but is not endorsed or certified by TMDb.
