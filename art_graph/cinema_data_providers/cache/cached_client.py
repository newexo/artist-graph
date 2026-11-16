"""A TMDb client that caches results in a database.

The caller provides a SQLAlchemy engine — this module has no opinion about
which database backend is used or how it is configured (PostgreSQL and SQLite
are supported).

Database work is synchronous, so the async methods run it in a worker thread
with ``asyncio.to_thread`` rather than blocking the caller's event loop. Worker
threads need their own connections: an in-memory SQLite engine must use
``StaticPool`` (and ``check_same_thread=False``), or each thread sees its own
empty database.
"""

import asyncio
from typing import List, Optional

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from ..tmdb.client import TMDbClient
from ..tmdb.config import TMDbConfig
from ..tmdb_models import CastMember, Movie, MovieCreditRole, Person
from .orm_models import PersonRecord, MovieRecord
from .operations import (
    get_cached_movie_cast,
    get_cached_person_movies,
    store_movie_cast,
    store_person_movies,
)
from .schema import ensure_schema


class CachedTMDbClient(TMDbClient):
    def __init__(self, config: TMDbConfig, engine: Engine):
        super().__init__(config)
        self.engine = engine
        ensure_schema(engine)

    # -- synchronous database work, run in a worker thread ------------------

    def _read_person_movies(
        self, person_id: int, limit: int
    ) -> Optional[List[MovieCreditRole]]:
        with Session(bind=self.engine) as session:
            person = session.get(PersonRecord, person_id)
            if person is None or not person.has_full_filmography:
                return None
            cached = get_cached_person_movies(session, person_id)
            if not cached:
                return None
            results = [
                MovieCreditRole(
                    id=credit.movie.tmdb_id,
                    title=credit.movie.title,
                    release_date=credit.movie.release_date,
                    poster_path=credit.movie.poster_path,
                    popularity=credit.movie.popularity,
                    character=credit.character,
                    order=credit.credit_order,
                )
                for credit in cached
            ]
            results.sort(key=lambda m: m.popularity, reverse=True)
            return results[:limit]

    def _write_person_movies(
        self, person: Person, movies: List[MovieCreditRole]
    ) -> None:
        with Session(bind=self.engine) as session:
            store_person_movies(session, person, movies)

    def _read_movie_cast(self, movie_id: int) -> Optional[List[CastMember]]:
        with Session(bind=self.engine) as session:
            movie = session.get(MovieRecord, movie_id)
            if movie is None or not movie.has_full_cast:
                return None
            cached = get_cached_movie_cast(session, movie_id)
            if not cached:
                return None
            return [
                CastMember(
                    id=credit.person.tmdb_id,
                    name=credit.person.name,
                    profile_path=credit.person.profile_path,
                    popularity=credit.person.popularity,
                    character=credit.character,
                    order=credit.credit_order,
                )
                for credit in cached
            ]

    def _write_movie_cast(self, movie: Movie, cast: List[CastMember]) -> None:
        with Session(bind=self.engine) as session:
            store_movie_cast(session, movie, cast)

    # -- API ----------------------------------------------------------------

    async def get_person_movies(
        self, person_id: int, limit: int = 20, trust_cache: bool = False
    ) -> List[MovieCreditRole]:
        if trust_cache:
            cached = await asyncio.to_thread(self._read_person_movies, person_id, limit)
            if cached is not None:
                return cached

        movies = await super().get_person_movies(person_id, limit=limit)

        person = await self.search_person_by_id(person_id)
        if person is not None:
            await asyncio.to_thread(self._write_person_movies, person, movies)

        return movies

    async def get_movie_cast(
        self, movie_id: int, trust_cache: bool = True
    ) -> List[CastMember]:
        if trust_cache:
            cached = await asyncio.to_thread(self._read_movie_cast, movie_id)
            if cached is not None:
                return cached

        cast = await super().get_movie_cast(movie_id)

        movie = await self.search_movie_by_id(movie_id)
        if movie is not None:
            await asyncio.to_thread(self._write_movie_cast, movie, cast)

        return cast

    async def search_person_by_id(self, person_id: int) -> Optional[Person]:
        """Get person details by ID, used to populate cache records."""
        return await self.get_person_details(person_id)

    async def search_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        """Get movie details by ID, used to populate cache records."""
        try:
            data = await self._get(f"/movie/{movie_id}")
            return Movie(**data)
        except Exception:
            return None
