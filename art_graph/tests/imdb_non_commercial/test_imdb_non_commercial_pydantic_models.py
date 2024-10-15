import pytest
from pydantic import ValidationError
from ...cinema_data_providers.imdb_non_commercial.imdb_non_commercial_pydantic_models import (
    NameBasics,
    TitleAkas,
    TitleBasics,
    TitleCrew,
    TitleEpisode,
    TitlePrincipals,
    TitleRatings,
)


def test_name_basics_happy_path():
    """Test that the NameBasics model initializes correctly with valid data."""
    data = {
        "nconst": 1234567,
        "primaryName": "John Doe",
        "birthYear": 1970,
        "deathYear": 2020,
        "primaryProfession": "actor,producer",
        "knownForTitles": "tt1234567,tt2345678",
    }
    name = NameBasics(**data)
    assert name.nconst == 1234567
    assert name.primaryName == "John Doe"
    assert name.birthYear == 1970
    assert name.deathYear == 2020
    assert name.primaryProfession == "actor,producer"
    assert name.knownForTitles == "1234567,2345678"


def test_name_basics_optional_fields():
    """Test that the NameBasics model can initialize with optional fields omitted."""
    data = {"nconst": "nm1234567", "primaryName": "Jane Doe"}
    name = NameBasics(**data)
    assert name.nconst == 1234567
    assert name.primaryName == "Jane Doe"
    assert name.birthYear is None
    assert name.deathYear is None
    assert name.primaryProfession is None
    assert name.knownForTitles is None


def test_name_basics_missing_required_field():
    """Test that the NameBasics model raises a ValidationError if a required field is missing."""
    data = {"primaryName": "John Doe"}
    with pytest.raises(ValidationError) as excinfo:
        NameBasics(**data)
    assert "nconst" in str(excinfo.value)


def test_name_basics_invalid_type_for_birth_year():
    """Test that the NameBasics model raises a ValidationError for invalid birthYear type."""
    data = {
        "nconst": "nm1234567",
        "primaryName": "John Doe",
        "birthYear": "nineteen-seventy",  # Invalid type
    }
    with pytest.raises(ValidationError) as excinfo:
        NameBasics(**data)
    assert "birthYear" in str(excinfo.value)


def test_name_basics_empty_professions():
    """Test that the NameBasics model accepts an empty list for primaryProfession."""
    data = {"nconst": "nm1234567", "primaryName": "John Doe", "primaryProfession": None}
    name = NameBasics(**data)
    assert name.primaryProfession is None


def test_name_basics_known_for_titles_invalid_type():
    """Test that the NameBasics model raises a ValidationError if knownForTitles is not a list."""
    data = {
        "nconst": "nm1234567",
        "primaryName": "John Doe",
        "knownForTitles": 5.5,  # Invalid type, should be a string
    }
    with pytest.raises(TypeError):
        NameBasics(**data)


# NameBasics Tests
def test_name_basics_valid():
    data = {
        "nconst": "nm1234567",
        "primaryName": "John Doe",
        "birthYear": 1970,
        "deathYear": 2020,
        "primaryProfession": "actor,director",
        "knownForTitles": "tt1234567,tt2345678",
    }
    model = NameBasics(**data)
    assert model.nconst == 1234567


# TitleAkas Tests
def test_title_akas_valid():
    data = {
        "titleId": "tt1234567",
        "ordering": 1,
        "title": "Movie Title",
        "region": "US",
        "isOriginalTitle": True,
    }
    model = TitleAkas(**data)
    assert model.titleId == 1234567
    assert model.isOriginalTitle is True


# TitleBasics Tests
def test_title_basics_valid():
    data = {
        "tconst": "tt1234567",
        "titleType": "movie",
        "primaryTitle": "Movie Title",
        "originalTitle": "Original Movie Title",
        "isAdult": False,
        "startYear": 2000,
        "runtimeMinutes": 120,
        "genres": "Action,Adventure",
    }
    model = TitleBasics(**data)
    assert model.tconst == 1234567
    assert model.genres == "Action,Adventure"


def test_title_basics_optional_fields():
    data = {
        "tconst": "tt1234567",
        "titleType": "movie",
        "primaryTitle": "Movie Title",
        "originalTitle": "Original Movie Title",
        "isAdult": False,
    }
    model = TitleBasics(**data)
    assert model.startYear is None
    assert model.genres is None


# TitleCrew Tests
def test_title_crew_valid():
    data = {
        "tconst": "tt1234567",
        "directors": "nm1234567,nm2345678",
        "writers": "nm3456789",
    }
    model = TitleCrew(**data)
    assert model.tconst == 1234567
    assert model.directors == "1234567,2345678"


def test_title_crew_optional_fields():
    data = {"tconst": "tt1234567"}
    model = TitleCrew(**data)
    assert model.directors is None
    assert model.writers is None


# TitleEpisode Tests
def test_title_episode_valid():
    data = {
        "tconst": "tt1234567",
        "parentTconst": "tt7654321",
        "seasonNumber": 3,
        "episodeNumber": 10,
    }
    model = TitleEpisode(**data)
    assert model.seasonNumber == 3
    assert model.episodeNumber == 10


def test_title_episode_optional_fields():
    data = {"tconst": "tt1234567", "parentTconst": "tt7654321"}
    model = TitleEpisode(**data)
    assert model.seasonNumber is None
    assert model.episodeNumber is None


# TitlePrincipals Tests
def test_title_principals_valid():
    data = {
        "tconst": "tt1234567",
        "ordering": 1,
        "nconst": "nm1234567",
        "category": "actor",
        "job": "lead actor",
        "characters": "John Doe",
    }
    model = TitlePrincipals(**data)
    assert model.characters == "John Doe"


def test_title_principals_optional_fields():
    data = {
        "tconst": "tt1234567",
        "ordering": 1,
        "nconst": "nm1234567",
        "category": "actor",
    }
    model = TitlePrincipals(**data)
    assert model.job is None
    assert model.characters is None


# TitleRatings Tests
def test_title_ratings_valid():
    data = {"tconst": "tt1234567", "averageRating": 8.5, "numVotes": 15000}
    model = TitleRatings(**data)
    assert model.tconst == 1234567
    assert model.averageRating == 8.5


def test_title_ratings_invalid_data():
    data = {
        "tconst": "tt1234567",
        "averageRating": "high",  # Invalid type
        "numVotes": 15000,
    }
    with pytest.raises(ValidationError):
        TitleRatings(**data)
