"""Tests for CachedTMDbClient — verifies cache hit/miss behavior.

Uses an in-memory SQLite DB and patches the parent TMDbClient API methods
so no real HTTP calls are made.
"""

from datetime import date
from unittest.mock import AsyncMock, patch

import pytest
import sqlalchemy

from art_graph.cinema_data_providers.cache.cached_client import CachedTMDbClient
from art_graph.cinema_data_providers.cache.orm_models import Base
from art_graph.cinema_data_providers.tmdb.config import TMDbConfig
from art_graph.cinema_data_providers.tmdb_models import (
    CastMember,
    Movie,
    MovieCreditRole,
    Person,
)


@pytest.fixture
def engine():
    eng = sqlalchemy.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=eng)
    return eng


@pytest.fixture
def config():
    return TMDbConfig(api_key="test-key")


@pytest.fixture
def client(config, engine):
    return CachedTMDbClient(config, engine=engine)


PERSON = Person(id=6193, name="Leonardo DiCaprio", popularity=80.0)
MOVIES = [
    MovieCreditRole(
        id=27205,
        title="Inception",
        release_date=date(2010, 7, 16),
        popularity=90.0,
        character="Cobb",
        order=0,
    ),
    MovieCreditRole(
        id=597,
        title="Titanic",
        release_date=date(1997, 12, 19),
        popularity=85.0,
        character="Jack Dawson",
        order=0,
    ),
]

MOVIE = Movie(
    id=27205, title="Inception", release_date=date(2010, 7, 16), popularity=90.0
)
CAST = [
    CastMember(
        id=6193, name="Leonardo DiCaprio", character="Cobb", order=0, popularity=80.0
    ),
    CastMember(
        id=24045,
        name="Joseph Gordon-Levitt",
        character="Arthur",
        order=1,
        popularity=50.0,
    ),
]


class TestGetPersonMovies:
    @pytest.mark.asyncio
    async def test_cache_miss_calls_api(self, client):
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_person_movies",
                new_callable=AsyncMock,
                return_value=MOVIES,
            ) as mock_api,
            patch.object(
                client,
                "get_person_details",
                new_callable=AsyncMock,
                return_value=PERSON,
            ),
        ):
            result = await client.get_person_movies(6193)
            mock_api.assert_called_once_with(6193, limit=20)
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_cache_hit_skips_api(self, client):
        # Populate cache
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_person_movies",
                new_callable=AsyncMock,
                return_value=MOVIES,
            ),
            patch.object(
                client,
                "get_person_details",
                new_callable=AsyncMock,
                return_value=PERSON,
            ),
        ):
            await client.get_person_movies(6193)

        # Second call with trust_cache=True should hit cache
        with patch.object(
            client.__class__.__bases__[0],
            "get_person_movies",
            new_callable=AsyncMock,
        ) as mock_api:
            result = await client.get_person_movies(6193, trust_cache=True)
            mock_api.assert_not_called()
            assert len(result) == 2
            titles = {m.title for m in result}
            assert titles == {"Inception", "Titanic"}

    @pytest.mark.asyncio
    async def test_cached_results_sorted_by_popularity(self, client):
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_person_movies",
                new_callable=AsyncMock,
                return_value=MOVIES,
            ),
            patch.object(
                client,
                "get_person_details",
                new_callable=AsyncMock,
                return_value=PERSON,
            ),
        ):
            await client.get_person_movies(6193)

        with patch.object(
            client.__class__.__bases__[0],
            "get_person_movies",
            new_callable=AsyncMock,
        ):
            result = await client.get_person_movies(6193, trust_cache=True)
            assert result[0].title == "Inception"  # popularity 90
            assert result[1].title == "Titanic"  # popularity 85

    @pytest.mark.asyncio
    async def test_default_does_not_trust_cache(self, client):
        """get_person_movies defaults to trust_cache=False, always hitting API."""
        # Populate cache
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_person_movies",
                new_callable=AsyncMock,
                return_value=MOVIES,
            ),
            patch.object(
                client,
                "get_person_details",
                new_callable=AsyncMock,
                return_value=PERSON,
            ),
        ):
            await client.get_person_movies(6193)

        # Default call (trust_cache=False) should still hit API
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_person_movies",
                new_callable=AsyncMock,
                return_value=MOVIES,
            ) as mock_api,
            patch.object(
                client,
                "get_person_details",
                new_callable=AsyncMock,
                return_value=PERSON,
            ),
        ):
            await client.get_person_movies(6193)
            mock_api.assert_called_once()

    @pytest.mark.asyncio
    async def test_incidental_person_not_trusted(self, client):
        """A person added via store_movie_cast should not be a cache hit."""
        # Store a movie cast — this creates person records incidentally
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_movie_cast",
                new_callable=AsyncMock,
                return_value=CAST,
            ),
            patch.object(
                client,
                "search_movie_by_id",
                new_callable=AsyncMock,
                return_value=MOVIE,
            ),
        ):
            await client.get_movie_cast(27205)

        # Asking for person movies with trust_cache=True should still miss,
        # because has_full_filmography is False
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_person_movies",
                new_callable=AsyncMock,
                return_value=MOVIES,
            ) as mock_api,
            patch.object(
                client,
                "get_person_details",
                new_callable=AsyncMock,
                return_value=PERSON,
            ),
        ):
            await client.get_person_movies(6193, trust_cache=True)
            mock_api.assert_called_once()


class TestGetMovieCast:
    @pytest.mark.asyncio
    async def test_cache_miss_calls_api(self, client):
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_movie_cast",
                new_callable=AsyncMock,
                return_value=CAST,
            ) as mock_api,
            patch.object(
                client,
                "search_movie_by_id",
                new_callable=AsyncMock,
                return_value=MOVIE,
            ),
        ):
            result = await client.get_movie_cast(27205)
            mock_api.assert_called_once_with(27205)
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_cache_hit_skips_api(self, client):
        # Populate cache
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_movie_cast",
                new_callable=AsyncMock,
                return_value=CAST,
            ),
            patch.object(
                client,
                "search_movie_by_id",
                new_callable=AsyncMock,
                return_value=MOVIE,
            ),
        ):
            await client.get_movie_cast(27205)

        # Second call should hit cache
        with patch.object(
            client.__class__.__bases__[0],
            "get_movie_cast",
            new_callable=AsyncMock,
        ) as mock_api:
            result = await client.get_movie_cast(27205)
            mock_api.assert_not_called()
            assert len(result) == 2
            names = {c.name for c in result}
            assert names == {"Leonardo DiCaprio", "Joseph Gordon-Levitt"}

    @pytest.mark.asyncio
    async def test_trust_cache_false_skips_cache(self, client):
        """get_movie_cast with trust_cache=False always hits API."""
        # Populate cache
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_movie_cast",
                new_callable=AsyncMock,
                return_value=CAST,
            ),
            patch.object(
                client,
                "search_movie_by_id",
                new_callable=AsyncMock,
                return_value=MOVIE,
            ),
        ):
            await client.get_movie_cast(27205)

        # Call with trust_cache=False should still hit API
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_movie_cast",
                new_callable=AsyncMock,
                return_value=CAST,
            ) as mock_api,
            patch.object(
                client,
                "search_movie_by_id",
                new_callable=AsyncMock,
                return_value=MOVIE,
            ),
        ):
            await client.get_movie_cast(27205, trust_cache=False)
            mock_api.assert_called_once()

    @pytest.mark.asyncio
    async def test_incidental_movie_not_trusted(self, client):
        """A movie added via store_person_movies should not be a cast cache hit."""
        # Store a person's filmography — this creates movie records incidentally
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_person_movies",
                new_callable=AsyncMock,
                return_value=MOVIES,
            ),
            patch.object(
                client,
                "get_person_details",
                new_callable=AsyncMock,
                return_value=PERSON,
            ),
        ):
            await client.get_person_movies(6193)

        # Asking for movie cast should miss — has_full_cast is False
        with (
            patch.object(
                client.__class__.__bases__[0],
                "get_movie_cast",
                new_callable=AsyncMock,
                return_value=CAST,
            ) as mock_api,
            patch.object(
                client,
                "search_movie_by_id",
                new_callable=AsyncMock,
                return_value=MOVIE,
            ),
        ):
            await client.get_movie_cast(27205)
            mock_api.assert_called_once()
