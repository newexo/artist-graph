import pytest
from datetime import date
import json

from ..cinema_data_providers.tmdb_models import (
    Movie,
    Actor,
    ActorSearchResults,
    BelongsToCollection,
    Genre,
    ProductionCompany,
    ProductionCountry,
    SpokenLanguage,
    MovieSearchResults,
)
from .. import directories


@pytest.fixture
def movie_data():
    return {
        "adult": False,
        "backdrop_path": "/w5IDXtifKntw0ajv2co7jFlTQDM.jpg",
        "genre_ids": [878, 9648, 12],
        "id": 62,
        "original_language": "en",
        "original_title": "2001: A Space Odyssey",
        "overview": "Humanity finds a mysterious object buried beneath the lunar surface and sets off to find its origins with the help of HAL 9000, the world's most advanced super computer.",
        "popularity": 383.111,
        "poster_path": "/ve72VxNqjGM69Uky4WTo2bK6rfq.jpg",
        "release_date": "1968-04-02",
        "title": "2001: A Space Odyssey",
        "video": False,
        "vote_average": 8.078,
        "vote_count": 11139,
    }


def test_movie_initialization(movie_data):
    movie = Movie(**movie_data)
    assert movie.adult == movie_data["adult"]
    assert movie.backdrop_path == movie_data["backdrop_path"]
    assert movie.genre_ids == movie_data["genre_ids"]
    assert movie.id == movie_data["id"]
    assert movie.original_language == movie_data["original_language"]
    assert movie.original_title == movie_data["original_title"]
    assert movie.overview == movie_data["overview"]
    assert movie.popularity == movie_data["popularity"]
    assert movie.poster_path == movie_data["poster_path"]
    assert movie.release_date == date.fromisoformat(movie_data["release_date"])
    assert movie.release_date.year == 1968
    assert movie.release_date.month == 4
    assert movie.release_date.day == 2
    assert movie.title == movie_data["title"]
    assert movie.video == movie_data["video"]
    assert movie.vote_average == movie_data["vote_average"]
    assert movie.vote_count == movie_data["vote_count"]


@pytest.fixture
def actor_data():
    return {
        "adult": False,
        "gender": 2,
        "id": 4724,
        "known_for_department": "Acting",
        "name": "Kevin Bacon",
        "original_name": "Kevin Bacon",
        "popularity": 104.131,
        "profile_path": "/rjX2Oz3tCZMfSwOoIAyEhdtXnTE.jpg",
        "known_for": [
            {
                "backdrop_path": "/bMiOfPhplZu1Lql3hGTRV087QA.jpg",
                "id": 49538,
                "original_title": "X-Men: First Class",
                "overview": "Before Charles Xavier and Erik Lensherr took the names Professor X and Magneto, they were two young men discovering their powers for the first time. Before they were arch-enemies, they were closest of friends, working together with other mutants (some familiar, some new), to stop the greatest threat the world has ever known.",
                "poster_path": "/vUvlOY575rztBuJV3a0dbHW5MQR.jpg",
                "media_type": "movie",
                "adult": False,
                "title": "X-Men: First Class",
                "original_language": "en",
                "genre_ids": [28, 878, 12],
                "popularity": 2.555,
                "release_date": "2011-06-01",
                "video": False,
                "vote_average": 7.299,
                "vote_count": 12410,
            },
            {
                "backdrop_path": "/w2rWEjAMYErpNfoK2Z0GFh1LFhN.jpg",
                "id": 819,
                "original_title": "Sleepers",
                "overview": "Two gangsters seek revenge on the state jail worker who during their stay at a youth prison sexually abused them. A sensational court hearing takes place to charge him for the crimes.",
                "poster_path": "/yUpiEk2EojS9ZEXb3nIQonQCYYF.jpg",
                "media_type": "movie",
                "adult": False,
                "title": "Sleepers",
                "original_language": "en",
                "genre_ids": [80, 18, 53],
                "popularity": 34.851,
                "release_date": "1996-10-18",
                "video": False,
                "vote_average": 7.601,
                "vote_count": 3410,
            },
            {
                "backdrop_path": "/3L3DUwfRLW18OUiLSdmovfICyY3.jpg",
                "id": 9362,
                "original_title": "Tremors",
                "overview": "Val McKee and Earl Bassett are in a fight for their lives when they discover that their desolate town has been infested with gigantic, man-eating creatures that live below the ground.",
                "poster_path": "/cA4ggkZ3r1d5r9hOAUWC8x5ul2i.jpg",
                "media_type": "movie",
                "adult": False,
                "title": "Tremors",
                "original_language": "en",
                "genre_ids": [27, 28, 878, 35],
                "popularity": 76.06,
                "release_date": "1990-01-19",
                "video": False,
                "vote_average": 6.895,
                "vote_count": 3111,
            },
        ],
    }


def test_actor_initialization(actor_data):
    actor = Actor(**actor_data)
    assert actor.adult == actor_data["adult"]
    assert actor.gender == actor_data["gender"]
    assert actor.id == actor_data["id"]
    assert actor.known_for_department == actor_data["known_for_department"]
    assert actor.name == actor_data["name"]
    assert actor.original_name == actor_data["original_name"]
    assert actor.popularity == actor_data["popularity"]
    assert actor.profile_path == actor_data["profile_path"]
    assert len(actor.known_for) == len(actor_data["known_for"])
    for idx, known_for_movie_data in enumerate(actor_data["known_for"]):
        known_for_movie = actor.known_for[idx]
        assert known_for_movie.backdrop_path == known_for_movie_data["backdrop_path"]
        assert known_for_movie.id == known_for_movie_data["id"]
        assert known_for_movie.original_title == known_for_movie_data["original_title"]
        assert known_for_movie.overview == known_for_movie_data["overview"]
        assert known_for_movie.poster_path == known_for_movie_data["poster_path"]
        assert known_for_movie.adult == known_for_movie_data["adult"]
        assert known_for_movie.title == known_for_movie_data["title"]
        assert (
            known_for_movie.original_language
            == known_for_movie_data["original_language"]
        )
        assert known_for_movie.genre_ids == known_for_movie_data["genre_ids"]
        assert known_for_movie.popularity == known_for_movie_data["popularity"]
        assert known_for_movie.release_date == date.fromisoformat(
            known_for_movie_data["release_date"]
        )
        assert known_for_movie.video == known_for_movie_data["video"]
        assert known_for_movie.vote_average == known_for_movie_data["vote_average"]
        assert known_for_movie.vote_count == known_for_movie_data["vote_count"]


@pytest.fixture
def movie_details_data():
    return {
        "adult": False,
        "backdrop_path": "/w5IDXtifKntw0ajv2co7jFlTQDM.jpg",
        "belongs_to_collection": {
            "id": 4438,
            "name": "The Space Odyssey Series",
            "poster_path": "/bxQaNDuSLCllnMSQ0ZLg7e6HrMW.jpg",
            "backdrop_path": "/15FumSExI9SRoL7QJWZAsA0b10c.jpg",
        },
        "budget": 12000000,
        "genres": [
            {"id": 878, "name": "Science Fiction"},
            {"id": 9648, "name": "Mystery"},
            {"id": 12, "name": "Adventure"},
        ],
        "homepage": "http://2001spaceodysseymovie.com",
        "id": 62,
        "imdb_id": "tt0062622",
        "original_language": "en",
        "original_title": "2001: A Space Odyssey",
        "overview": "Humanity finds a mysterious object buried beneath the lunar surface and sets off to find its origins with the help of HAL 9000, the world's most advanced super computer.",
        "popularity": 57.456,
        "poster_path": "/ve72VxNqjGM69Uky4WTo2bK6rfq.jpg",
        "production_companies": [
            {
                "id": 385,
                "logo_path": None,
                "name": "Stanley Kubrick Productions",
                "origin_country": "GB",
            },
            {
                "id": 21,
                "logo_path": "/usUnaYV6hQnlVAXP6r4HwrlLFPG.png",
                "name": "Metro-Goldwyn-Mayer",
                "origin_country": "US",
            },
        ],
        "production_countries": [
            {"iso_3166_1": "GB", "name": "United Kingdom"},
            {"iso_3166_1": "US", "name": "United States of America"},
        ],
        "release_date": "1968-04-02",
        "revenue": 71923560,
        "runtime": 149,
        "spoken_languages": [
            {"english_name": "English", "iso_639_1": "en", "name": "English"},
            {"english_name": "Russian", "iso_639_1": "ru", "name": "Pусский"},
        ],
        "status": "Released",
        "tagline": "The ultimate trip.",
        "title": "2001: A Space Odyssey",
        "video": False,
        "vote_average": 8.076,
        "vote_count": 10994,
    }


def test_movie_details_initialization(movie_details_data):
    movie_details = Movie(**movie_details_data)
    assert movie_details.adult == movie_details_data["adult"]
    assert movie_details.backdrop_path == movie_details_data["backdrop_path"]
    assert movie_details.belongs_to_collection == BelongsToCollection(
        **movie_details_data["belongs_to_collection"]
    )
    assert movie_details.budget == movie_details_data["budget"]
    assert movie_details.genres == [Genre(**g) for g in movie_details_data["genres"]]
    assert movie_details.homepage == movie_details_data["homepage"]
    assert movie_details.id == movie_details_data["id"]
    assert movie_details.imdb_id == movie_details_data["imdb_id"]
    assert movie_details.original_language == movie_details_data["original_language"]
    assert movie_details.original_title == movie_details_data["original_title"]
    assert movie_details.overview == movie_details_data["overview"]
    assert movie_details.popularity == movie_details_data["popularity"]
    assert movie_details.poster_path == movie_details_data["poster_path"]
    assert movie_details.production_companies == [
        ProductionCompany(**pc) for pc in movie_details_data["production_companies"]
    ]
    assert movie_details.production_countries == [
        ProductionCountry(**pc) for pc in movie_details_data["production_countries"]
    ]
    assert movie_details.release_date == date(1968, 4, 2)
    assert movie_details.revenue == movie_details_data["revenue"]
    assert movie_details.runtime == movie_details_data["runtime"]
    assert movie_details.spoken_languages == [
        SpokenLanguage(**sl) for sl in movie_details_data["spoken_languages"]
    ]
    assert movie_details.status == movie_details_data["status"]
    assert movie_details.tagline == movie_details_data["tagline"]
    assert movie_details.title == movie_details_data["title"]
    assert movie_details.video == movie_details_data["video"]
    assert movie_details.vote_average == movie_details_data["vote_average"]
    assert movie_details.vote_count == movie_details_data["vote_count"]


@pytest.fixture
def odyssey_search():
    with open(directories.test_data("tmdb_2001_search.json")) as f:
        return json.load(f)


@pytest.fixture
def odyssey_details():
    with open(directories.test_data("tmdb_2001_details.json")) as f:
        return json.load(f)


@pytest.fixture
def bacon_search():
    with open(directories.test_data("tmdb_bacon_search.json")) as f:
        return json.load(f)


@pytest.fixture
def bacon_details():
    with open(directories.test_data("tmdb_bacon_details.json")) as f:
        return json.load(f)


def test_load_movie_search(odyssey_search):
    assert len(odyssey_search["results"]) == 6
    movie = odyssey_search["results"][0]
    assert movie["id"] == 62
    assert movie["title"] == "2001: A Space Odyssey"
    assert movie["release_date"] == "1968-04-02"
    assert (
        movie["overview"]
        == "Humanity finds a mysterious object buried beneath the lunar surface and sets off to find its origins with the help of HAL 9000, the world's most advanced super computer."
    )
    assert movie["poster_path"] == "/ve72VxNqjGM69Uky4WTo2bK6rfq.jpg"
    assert movie["backdrop_path"] == "/w5IDXtifKntw0ajv2co7jFlTQDM.jpg"
    assert movie["popularity"] == 383.111
    assert movie["vote_count"] == 11139
    assert movie["vote_average"] == 8.078

    search_results = MovieSearchResults(**odyssey_search)
    assert search_results.page == 1
    assert search_results.total_pages == 1
    assert search_results.total_results == 6
    assert len(search_results.results) == 6

    odyssey_movie = search_results.results[0]
    assert odyssey_movie.id == 62
    assert odyssey_movie.title == "2001: A Space Odyssey"
    assert odyssey_movie.release_date == date(1968, 4, 2)
    assert (
        odyssey_movie.overview
        == "Humanity finds a mysterious object buried beneath the lunar surface and sets off to find its origins with the help of HAL 9000, the world's most advanced super computer."
    )

    movie_no_release_date = search_results.results[1]
    assert movie_no_release_date.release_date is None


@pytest.fixture
def actor_search_data():
    return {
        "page": 1,
        "results": [
            {
                "adult": False,
                "gender": 2,
                "id": 4724,
                "known_for_department": "Acting",
                "name": "Kevin Bacon",
                "original_name": "Kevin Bacon",
                "popularity": 104.131,
                "profile_path": "/rjX2Oz3tCZMfSwOoIAyEhdtXnTE.jpg",
                "known_for": [
                    {
                        "backdrop_path": "/bMiOfPhplZu1Lql3hGTRV087QA.jpg",
                        "id": 49538,
                        "original_title": "X-Men: First Class",
                        "overview": "Before Charles Xavier and Erik Lensherr took the names Professor X and Magneto...",
                        "poster_path": "/vUvlOY575rztBuJV3a0dbHW5MQR.jpg",
                        "media_type": "movie",
                        "adult": False,
                        "title": "X-Men: First Class",
                        "original_language": "en",
                        "genre_ids": [28, 878, 12],
                        "popularity": 2.555,
                        "release_date": "2011-06-01",
                        "video": False,
                        "vote_average": 7.299,
                        "vote_count": 12410,
                    },
                    # Add more movies if needed
                ],
            },
            # Add more actors if needed
        ],
        "total_pages": 1,
        "total_results": 6,
    }


def test_actor_search_results_initialization(actor_search_data):
    actor_search_results = ActorSearchResults(**actor_search_data)
    assert actor_search_results.page == actor_search_data["page"]
    assert len(actor_search_results.results) == len(actor_search_data["results"])
    assert actor_search_results.total_pages == actor_search_data["total_pages"]
    assert actor_search_results.total_results == actor_search_data["total_results"]

    for idx, actor_data in enumerate(actor_search_data["results"]):
        actor = actor_search_results.results[idx]
        assert actor.adult == actor_data["adult"]
        assert actor.gender == actor_data["gender"]
        assert actor.id == actor_data["id"]
        assert actor.known_for_department == actor_data["known_for_department"]
        assert actor.name == actor_data["name"]
        assert actor.original_name == actor_data["original_name"]
        assert actor.popularity == actor_data["popularity"]
        assert actor.profile_path == actor_data["profile_path"]
        assert len(actor.known_for) == len(actor_data["known_for"])

        for movie_idx, known_for_data in enumerate(actor_data["known_for"]):
            known_for_movie = actor.known_for[movie_idx]
            assert known_for_movie.backdrop_path == known_for_data["backdrop_path"]
            assert known_for_movie.id == known_for_data["id"]
            assert known_for_movie.original_title == known_for_data["original_title"]
            assert known_for_movie.overview == known_for_data["overview"]
            assert known_for_movie.poster_path == known_for_data["poster_path"]
            assert known_for_movie.media_type == known_for_data["media_type"]
            assert known_for_movie.adult == known_for_data["adult"]
            assert known_for_movie.title == known_for_data["title"]
            assert (
                known_for_movie.original_language == known_for_data["original_language"]
            )
            assert known_for_movie.genre_ids == known_for_data["genre_ids"]
            assert known_for_movie.popularity == known_for_data["popularity"]
            assert known_for_movie.video == known_for_data["video"]
            assert known_for_movie.vote_average == known_for_data["vote_average"]
            assert known_for_movie.vote_count == known_for_data["vote_count"]


def test_load_actor_search(bacon_search):
    assert len(bacon_search["results"]) == 6
    actor = bacon_search["results"][0]
    assert actor["id"] == 4724
    assert actor["name"] == "Kevin Bacon"
    assert actor["known_for_department"] == "Acting"
    assert actor["popularity"] == 104.131
    assert actor["profile_path"] == "/rjX2Oz3tCZMfSwOoIAyEhdtXnTE.jpg"
    assert len(actor["known_for"]) == 3

    search_results = ActorSearchResults(**bacon_search)
    assert search_results.page == 1
    assert search_results.total_pages == 1
    assert search_results.total_results == 6
    assert len(search_results.results) == 6

    bacon = search_results.results[0]
    assert bacon.id == 4724
    assert bacon.name == "Kevin Bacon"
    assert bacon.known_for_department == "Acting"
    assert bacon.popularity == 104.131
    assert bacon.profile_path == "/rjX2Oz3tCZMfSwOoIAyEhdtXnTE.jpg"
    assert len(bacon.known_for) == 3

    first_movie = bacon.known_for[0]
    assert first_movie.id == 49538
    assert first_movie.title == "X-Men: First Class"
    assert first_movie.release_date == date(2011, 6, 1)
    assert first_movie.overview.startswith(
        "Before Charles Xavier and Erik Lensherr took"
    )
    assert first_movie.poster_path == "/vUvlOY575rztBuJV3a0dbHW5MQR.jpg"
    assert first_movie.popularity == 2.555
    assert first_movie.vote_count == 12410
    assert first_movie.vote_average == 7.299
    assert first_movie.media_type == "movie"
    assert not first_movie.adult
    assert first_movie.original_language == "en"
    assert first_movie.genre_ids == [28, 878, 12]
