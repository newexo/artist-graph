import pytest
from unittest.mock import AsyncMock, patch

from ..cinema_data_providers.tmdb.client import TMDbClient
from ..cinema_data_providers.tmdb.config import (
    TMDbConfig,
    build_image_url,
    DEFAULT_TMDB_IMAGE_BASE,
)


@pytest.fixture
def client():
    return TMDbClient(TMDbConfig(api_key="test-key"))


def person_payload(**overrides) -> dict:
    """Fields required by the rich Person model; override per test."""
    base = {
        "adult": False,
        "gender": 2,
        "id": 287,
        "known_for_department": "Acting",
        "name": "Brad Pitt",
        "original_name": "Brad Pitt",
        "popularity": 25.3,
        "profile_path": None,
    }
    base.update(overrides)
    return base


def movie_payload(**overrides) -> dict:
    """Fields required by the rich Movie model; override per test."""
    base = {
        "adult": False,
        "backdrop_path": None,
        "id": 550,
        "original_language": "en",
        "original_title": "Fight Club",
        "overview": "An insomniac office worker...",
        "popularity": 50.0,
        "poster_path": None,
        "release_date": None,
        "title": "Fight Club",
        "video": False,
        "vote_average": 8.4,
        "vote_count": 25000,
    }
    base.update(overrides)
    return base


class TestSearchPerson:
    async def test_returns_first_result(self, client):
        mock_response = {
            "results": [
                person_payload(
                    profile_path="/abc.jpg",
                    known_for=[movie_payload(title="Fight Club")],
                )
            ]
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.search_person("Brad Pitt")

        assert result.id == 287
        assert result.name == "Brad Pitt"
        assert result.popularity == 25.3
        assert result.profile_path == "/abc.jpg"
        assert result.known_for[0].title == "Fight Club"

    async def test_returns_none_when_no_results(self, client):
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value={"results": []}
        ):
            result = await client.search_person("Nonexistent Person")

        assert result is None

    async def test_missing_profile_path(self, client):
        mock_response = {"results": [person_payload(id=1, name="Test")]}
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.search_person("Test")

        assert result.profile_path is None
        assert result.known_for == []


class TestGetPersonMovies:
    async def test_returns_sorted_by_popularity(self, client):
        mock_response = {
            "id": 287,
            "cast": [
                movie_payload(
                    id=1,
                    title="Unpopular",
                    original_title="Unpopular",
                    popularity=2.0,
                    release_date="2020-01-01",
                ),
                movie_payload(
                    id=2,
                    title="Popular",
                    original_title="Popular",
                    popularity=50.0,
                    release_date="2019-06-15",
                ),
            ],
            "crew": [],
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_person_movies(287)

        assert result[0].title == "Popular"
        assert result[1].title == "Unpopular"

    async def test_respects_limit(self, client):
        mock_response = {
            "id": 287,
            "cast": [
                movie_payload(
                    id=i,
                    title=f"Movie {i}",
                    original_title=f"Movie {i}",
                    popularity=float(i),
                )
                for i in range(10)
            ],
            "crew": [],
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_person_movies(287, limit=3)

        assert len(result) == 3

    async def test_empty_release_date_becomes_none(self, client):
        mock_response = {
            "id": 287,
            "cast": [
                movie_payload(
                    id=1,
                    title="Test",
                    original_title="Test",
                    release_date="",
                )
            ],
            "crew": [],
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_person_movies(287)

        assert result[0].release_date is None

    async def test_raw_image_paths_preserved(self, client):
        mock_response = {
            "id": 287,
            "cast": [
                movie_payload(
                    id=1,
                    title="Test",
                    original_title="Test",
                    poster_path="/poster.jpg",
                    backdrop_path="/backdrop.jpg",
                )
            ],
            "crew": [],
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_person_movies(287)

        assert result[0].poster_path == "/poster.jpg"
        assert result[0].backdrop_path == "/backdrop.jpg"

    async def test_cast_entries_carry_credit_fields(self, client):
        mock_response = {
            "id": 287,
            "cast": [
                movie_payload(
                    id=1,
                    title="Test",
                    original_title="Test",
                    character="Tyler Durden",
                    credit_id="abc123",
                    order=0,
                )
            ],
            "crew": [],
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_person_movies(287)

        assert result[0].character == "Tyler Durden"
        assert result[0].credit_id == "abc123"
        assert result[0].order == 0


class TestSearchMovie:
    async def test_returns_first_result(self, client):
        mock_response = {
            "results": [
                movie_payload(
                    id=76203,
                    title="12 Years a Slave",
                    original_title="12 Years a Slave",
                    release_date="2013-10-18",
                    poster_path="/poster.jpg",
                    backdrop_path="/backdrop.jpg",
                )
            ]
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.search_movie("12 Years a Slave")

        assert result.id == 76203
        assert result.title == "12 Years a Slave"
        assert result.release_date.year == 2013

    async def test_returns_none_when_no_results(self, client):
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value={"results": []}
        ):
            result = await client.search_movie("xyznonexistent")

        assert result is None

    async def test_passes_year_param(self, client):
        mock_get = AsyncMock(
            return_value={
                "results": [
                    movie_payload(
                        id=1,
                        title="Test",
                        original_title="Test",
                        release_date="2013-01-01",
                    )
                ]
            }
        )
        with patch.object(client, "_get", mock_get):
            await client.search_movie("Test", year=2013)

        args, kwargs = mock_get.call_args
        passed_params = args[1] if len(args) > 1 else kwargs.get("params", {})
        # search_movie builds a dict and passes it positionally
        assert passed_params.get("year") == 2013


class TestGetMovieCast:
    async def test_returns_cast_list(self, client):
        mock_response = {
            "id": 76203,
            "cast": [
                person_payload(
                    id=287,
                    name="Brad Pitt",
                    original_name="Brad Pitt",
                    profile_path="/brad.jpg",
                    cast_id=1,
                    character="Edwin Epps",
                    credit_id="xyz",
                    order=0,
                ),
                person_payload(
                    id=17288,
                    name="Michael Fassbender",
                    original_name="Michael Fassbender",
                    cast_id=2,
                    character="Bass",
                    credit_id="pqr",
                    order=1,
                ),
            ],
            "crew": [],
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_movie_cast(76203)

        assert len(result) == 2
        assert result[0].name == "Brad Pitt"
        assert result[0].character == "Edwin Epps"
        assert result[0].order == 0
        assert result[0].profile_path == "/brad.jpg"
        assert result[1].profile_path is None

    async def test_empty_cast(self, client):
        with patch.object(
            client,
            "_get",
            new_callable=AsyncMock,
            return_value={"id": 99999, "cast": [], "crew": []},
        ):
            result = await client.get_movie_cast(99999)

        assert result == []


class TestGetMovieCredits:
    async def test_returns_cast_and_crew(self, client):
        mock_response = {
            "id": 550,
            "cast": [
                person_payload(
                    id=287,
                    name="Brad Pitt",
                    original_name="Brad Pitt",
                    character="Tyler Durden",
                    credit_id="c1",
                    order=0,
                ),
            ],
            "crew": [
                person_payload(
                    id=7467,
                    name="David Fincher",
                    original_name="David Fincher",
                    known_for_department="Directing",
                    department="Directing",
                    job="Director",
                    credit_id="c2",
                ),
            ],
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_movie_credits(550)

        assert result.id == 550
        assert len(result.cast) == 1
        assert result.cast[0].character == "Tyler Durden"
        assert len(result.crew) == 1
        assert result.crew[0].job == "Director"
        assert result.crew[0].department == "Directing"


class TestGetPersonDetails:
    async def test_returns_details(self, client):
        mock_response = person_payload(
            id=287,
            name="Brad Pitt",
            original_name="Brad Pitt",
            profile_path="/brad.jpg",
        )
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_person_details(287)

        assert result.id == 287
        assert result.name == "Brad Pitt"
        assert result.popularity == 25.3
        assert result.known_for == []

    async def test_returns_none_on_error(self, client):
        with patch.object(
            client, "_get", new_callable=AsyncMock, side_effect=Exception("Not found")
        ):
            result = await client.get_person_details(99999)

        assert result is None


class TestGetPopularPeople:
    async def test_returns_people_list(self, client):
        mock_response = {
            "results": [
                person_payload(
                    id=287,
                    name="Brad Pitt",
                    original_name="Brad Pitt",
                    profile_path="/brad.jpg",
                    known_for=[movie_payload(title="Fight Club")],
                ),
                person_payload(
                    id=1891,
                    name="Colin Firth",
                    original_name="Colin Firth",
                    popularity=12.1,
                    profile_path=None,
                    known_for=[],
                ),
            ]
        }
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value=mock_response
        ):
            result = await client.get_popular_people(page=1)

        assert len(result) == 2
        assert result[0].name == "Brad Pitt"
        assert result[1].known_for == []

    async def test_empty_results(self, client):
        with patch.object(
            client, "_get", new_callable=AsyncMock, return_value={"results": []}
        ):
            result = await client.get_popular_people()

        assert result == []


class TestBuildImageUrl:
    def test_with_path(self):
        assert (
            build_image_url("/abc.jpg", DEFAULT_TMDB_IMAGE_BASE)
            == "https://image.tmdb.org/t/p/w500/abc.jpg"
        )

    def test_with_none(self):
        assert build_image_url(None, DEFAULT_TMDB_IMAGE_BASE) is None

    def test_with_custom_base(self):
        assert (
            build_image_url("/abc.jpg", "https://example.com")
            == "https://example.com/abc.jpg"
        )


class TestTMDbConfig:
    def test_defaults(self):
        config = TMDbConfig(api_key="abc")
        assert config.api_key == "abc"
        assert config.base_url == "https://api.themoviedb.org/3"
        assert config.image_base == "https://image.tmdb.org/t/p/w500"
        assert config.backdrop_base == "https://image.tmdb.org/t/p/w1280"
        assert config.timeout == 10.0

    def test_overrides(self):
        config = TMDbConfig(
            api_key="abc",
            base_url="https://custom.example",
            image_base="https://img.example",
            backdrop_base="https://bg.example",
            timeout=5.0,
        )
        assert config.base_url == "https://custom.example"
        assert config.image_base == "https://img.example"
        assert config.backdrop_base == "https://bg.example"
        assert config.timeout == 5.0
