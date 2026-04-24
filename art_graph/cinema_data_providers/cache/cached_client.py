"""A TMDb client that caches results in a database.

The caller provides a SQLAlchemy engine — this module has no opinion about
which database backend is used or how it is configured.
"""

from typing import List, Optional

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from ..tmdb.client import TMDbClient
from ..tmdb.config import TMDbConfig
from ..tmdb_models import CastMember, Movie, MovieCreditRole, Person
from .orm_models import Base, PersonRecord, MovieRecord
from .operations import (
    get_cached_movie_cast,
    get_cached_person_movies,
    store_movie_cast,
    store_person_movies,
)


class CachedTMDbClient(TMDbClient):
    def __init__(self, config: TMDbConfig, engine: Engine):
        super().__init__(config)
        self.engine = engine
        Base.metadata.create_all(bind=engine)

    async def get_person_movies(
        self, person_id: int, limit: int = 20, trust_cache: bool = False
    ) -> List[MovieCreditRole]:
        if trust_cache:
            with Session(bind=self.engine) as session:
                person = session.get(PersonRecord, person_id)
                if person is not None and person.has_full_filmography:
                    cached = get_cached_person_movies(session, person_id)
                    if cached:
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

        movies = await super().get_person_movies(person_id, limit=limit)

        person = await self.search_person_by_id(person_id)
        if person is not None:
            with Session(bind=self.engine) as session:
                store_person_movies(session, person, movies)

        return movies

    async def get_movie_cast(
        self, movie_id: int, trust_cache: bool = True
    ) -> List[CastMember]:
        if trust_cache:
            with Session(bind=self.engine) as session:
                movie = session.get(MovieRecord, movie_id)
                if movie is not None and movie.has_full_cast:
                    cached = get_cached_movie_cast(session, movie_id)
                    if cached:
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

        cast = await super().get_movie_cast(movie_id)

        movie = await self.search_movie_by_id(movie_id)
        if movie is not None:
            with Session(bind=self.engine) as session:
                store_movie_cast(session, movie, cast)

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
