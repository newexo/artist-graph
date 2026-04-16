"""Async HTTP client for the TMDb API.

Returns the rich pydantic models defined in ``tmdb_models``. Image paths are
returned as raw TMDb paths; callers can prefix them with ``config.image_base``
or ``config.backdrop_base`` via ``build_image_url``.
"""

from typing import List, Optional

import httpx

from ..tmdb_models import (
    CastMember,
    Movie,
    MovieCreditRole,
    MovieCredits,
    Person,
    PersonMovieCredits,
)
from .config import TMDbConfig


class TMDbClient:
    def __init__(self, config: TMDbConfig):
        self.config = config

    async def _get(self, path: str, params: Optional[dict] = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.config.base_url}{path}",
                params={"api_key": self.config.api_key, **(params or {})},
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            return response.json()

    async def search_person(self, name: str) -> Optional[Person]:
        data = await self._get("/search/person", {"query": name})
        results = data.get("results", [])
        if not results:
            return None
        return Person(**results[0])

    async def get_person_movies(
        self, person_id: int, limit: int = 20
    ) -> List[MovieCreditRole]:
        data = await self._get(f"/person/{person_id}/movie_credits")
        credits = PersonMovieCredits(**data)
        credits.cast.sort(key=lambda m: m.popularity, reverse=True)
        return credits.cast[:limit]

    async def search_movie(
        self, title: str, year: Optional[int] = None
    ) -> Optional[Movie]:
        params = {"query": title}
        if year:
            params["year"] = year
        data = await self._get("/search/movie", params)
        results = data.get("results", [])
        if not results:
            return None
        return Movie(**results[0])

    async def get_movie_cast(self, movie_id: int) -> List[CastMember]:
        credits = await self.get_movie_credits(movie_id)
        return credits.cast

    async def get_movie_credits(self, movie_id: int) -> MovieCredits:
        data = await self._get(f"/movie/{movie_id}/credits")
        return MovieCredits(**data)

    async def get_person_details(self, person_id: int) -> Optional[Person]:
        try:
            data = await self._get(f"/person/{person_id}")
            return Person(**data)
        except Exception:
            return None

    async def get_popular_people(self, page: int = 1) -> List[Person]:
        data = await self._get("/person/popular", {"page": page})
        return [Person(**p) for p in data.get("results", [])]
