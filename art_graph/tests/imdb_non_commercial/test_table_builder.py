import pytest

from imdb.parser.s3.utils import DB_TRANSFORM
from sqlalchemy.sql import sqltypes


from ...cinema_data_providers.imbd_non_commercial import table_builder


@pytest.fixture
def table_builder_principals():
    """Fixture to create a TableBuilder for the 'title.principals.tsv.gz' file."""
    fn = "title.principals.tsv.gz"
    headers = ["tconst", "ordering", "nconst", "category", "job", "characters"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


# Example test function using the fixture
def test_table_builder_principals(table_builder_principals):
    assert table_builder_principals.fn == "title.principals.tsv.gz"
    assert table_builder_principals.headers == [
        "tconst",
        "ordering",
        "nconst",
        "category",
        "job",
        "characters",
    ]
    assert table_builder_principals.table_name == "title_principals"
    assert table_builder_principals.table_map == DB_TRANSFORM["title_principals"]
    assert table_builder_principals.all_headers == {
        "tconst",
        "ordering",
        "nconst",
        "category",
        "job",
        "characters",
    }

    table_builder = table_builder_principals
    expected = {"name": "nconst", "type_": sqltypes.Integer, "index": True}
    actual = table_builder.col_args("nconst")
    assert actual == expected

    expected = {
        "name": "characters",
        "type_": sqltypes.String(length=1024),
        "index": False,
    }
    actual = table_builder.col_args("characters")
    assert repr(expected) == repr(actual)

    expected = {"name": "job", "type_": sqltypes.String(length=1024), "index": False}
    actual = table_builder.col_args("job")
    assert repr(expected) == repr(actual)

    expected = {"name": "tconst", "type_": sqltypes.Integer, "index": True}
    actual = table_builder.col_args("tconst")
    assert actual == expected

    expected = {"name": "category", "type_": sqltypes.String(length=64), "index": False}
    actual = table_builder.col_args("category")
    assert repr(expected) == repr(actual)

    expected = {"name": "ordering", "type_": sqltypes.Integer, "index": False}
    actual = table_builder.col_args("ordering")
    assert actual == expected


def print_assertions(table_builder: table_builder.TableBuilder):
    for header in table_builder.all_headers:
        col_args = table_builder.col_args(header)
        col_args = repr(col_args)
        print(f"    expected =  {col_args}")
        print(f"    actual = table_builder.col_args('{header}')")
        print("    assert actual == expected\n\n")


@pytest.fixture
def table_builder_name_basics():
    """Fixture to create a TableBuilder for the 'name.basics.tsv.gz' file."""
    fn = "name.basics.tsv.gz"
    headers = [
        "nconst",
        "primaryName",
        "birthYear",
        "deathYear",
        "primaryProfession",
        "knownForTitles",
    ]
    return table_builder.TableBuilder(fn=fn, headers=headers)


def test_table_builder_name_basics(table_builder_name_basics):
    assert table_builder_name_basics.fn == "name.basics.tsv.gz"
    assert table_builder_name_basics.headers == [
        "nconst",
        "primaryName",
        "birthYear",
        "deathYear",
        "primaryProfession",
        "knownForTitles",
    ]
    assert table_builder_name_basics.table_name == "name_basics"
    assert table_builder_name_basics.table_map == DB_TRANSFORM["name_basics"]
    assert table_builder_name_basics.all_headers == {
        "nconst",
        "primaryName",
        "birthYear",
        "deathYear",
        "primaryProfession",
        "knownForTitles",
        "ns_soundex",
        "sn_soundex",
        "s_soundex",
    }

    expected = {"index": True, "name": "nconst", "type_": sqltypes.Integer}
    actual = table_builder_name_basics.col_args("nconst")
    assert actual == expected

    expected = {"index": False, "name": "primaryName", "type_": sqltypes.UnicodeText}
    actual = table_builder_name_basics.col_args("primaryName")
    assert expected == actual


@pytest.fixture
def table_builder_title_basics():
    """Fixture to create a TableBuilder for the 'title.basics.tsv.gz' file."""
    fn = "title.basics.tsv.gz"
    headers = [
        "tconst",
        "titleType",
        "primaryTitle",
        "originalTitle",
        "isAdult",
        "startYear",
        "endYear",
        "runtimeMinutes",
        "genres",
    ]
    return table_builder.TableBuilder(fn=fn, headers=headers)


def test_table_builder_title_basics(table_builder_title_basics):
    assert table_builder_title_basics.fn == "title.basics.tsv.gz"
    assert table_builder_title_basics.headers == [
        "tconst",
        "titleType",
        "primaryTitle",
        "originalTitle",
        "isAdult",
        "startYear",
        "endYear",
        "runtimeMinutes",
        "genres",
    ]
    assert table_builder_title_basics.table_name == "title_basics"
    assert table_builder_title_basics.table_map == DB_TRANSFORM["title_basics"]
    assert table_builder_title_basics.all_headers == {
        "tconst",
        "titleType",
        "primaryTitle",
        "originalTitle",
        "isAdult",
        "startYear",
        "endYear",
        "runtimeMinutes",
        "genres",
        "t_soundex",
    }

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_basics.col_args("tconst")
    assert actual == expected

    expected = {
        "name": "titleType",
        "type_": sqltypes.String(length=16),
        "index": True,
    }
    actual = table_builder_title_basics.col_args("titleType")
    assert repr(expected) == repr(actual)


@pytest.fixture
def table_builder_title_ratings():
    """Fixture to create a TableBuilder for the 'title.ratings.tsv.gz' file."""
    fn = "title.ratings.tsv.gz"
    headers = ["tconst", "averageRating", "numVotes"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


def test_table_builder_title_ratings(table_builder_title_ratings):
    assert table_builder_title_ratings.fn == "title.ratings.tsv.gz"
    assert table_builder_title_ratings.headers == [
        "tconst",
        "averageRating",
        "numVotes",
    ]
    assert table_builder_title_ratings.table_name == "title_ratings"
    assert table_builder_title_ratings.table_map == DB_TRANSFORM["title_ratings"]
    assert table_builder_title_ratings.all_headers == {
        "tconst",
        "averageRating",
        "numVotes",
    }

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_ratings.col_args("tconst")
    assert actual == expected

    expected = {"index": True, "name": "averageRating", "type_": sqltypes.Float}
    actual = table_builder_title_ratings.col_args("averageRating")
    assert actual == expected


@pytest.fixture
def table_builder_title_akas():
    """Fixture to create a TableBuilder for the 'title.akas.tsv.gz' file."""
    fn = "title.akas.tsv.gz"
    headers = [
        "titleId",
        "ordering",
        "title",
        "region",
        "language",
        "types",
        "attributes",
        "isOriginalTitle",
    ]
    return table_builder.TableBuilder(fn=fn, headers=headers)


def test_table_builder_title_akas(table_builder_title_akas):
    assert table_builder_title_akas.fn == "title.akas.tsv.gz"
    assert table_builder_title_akas.headers == [
        "titleId",
        "ordering",
        "title",
        "region",
        "language",
        "types",
        "attributes",
        "isOriginalTitle",
    ]
    assert table_builder_title_akas.table_name == "title_akas"
    assert table_builder_title_akas.table_map == DB_TRANSFORM["title_akas"]
    assert table_builder_title_akas.all_headers == {
        "titleId",
        "ordering",
        "title",
        "region",
        "language",
        "types",
        "attributes",
        "isOriginalTitle",
        "t_soundex",
    }


@pytest.fixture
def table_builder_title_crew():
    """Fixture to create a TableBuilder for the 'title.crew.tsv.gz' file."""
    fn = "title.crew.tsv.gz"
    headers = ["tconst", "directors", "writers"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


def test_table_builder_title_crew(table_builder_title_crew):
    assert table_builder_title_crew.fn == "title.crew.tsv.gz"
    assert table_builder_title_crew.headers == ["tconst", "directors", "writers"]
    assert table_builder_title_crew.table_name == "title_crew"
    assert table_builder_title_crew.table_map == DB_TRANSFORM["title_crew"]
    assert table_builder_title_crew.all_headers == {"tconst", "directors", "writers"}

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_crew.col_args("tconst")
    assert actual == expected

    expected = {"index": False, "name": "directors", "type_": sqltypes.UnicodeText}
    actual = table_builder_title_crew.col_args("directors")
    assert actual == expected


@pytest.fixture
def table_builder_title_episode():
    """Fixture to create a TableBuilder for the 'title.episode.tsv.gz' file."""
    fn = "title.episode.tsv.gz"
    headers = ["tconst", "parentTconst", "seasonNumber", "episodeNumber"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


def test_table_builder_title_episode(table_builder_title_episode):
    assert table_builder_title_episode.fn == "title.episode.tsv.gz"
    assert table_builder_title_episode.headers == [
        "tconst",
        "parentTconst",
        "seasonNumber",
        "episodeNumber",
    ]
    assert table_builder_title_episode.table_name == "title_episode"
    assert table_builder_title_episode.table_map == DB_TRANSFORM["title_episode"]
    assert table_builder_title_episode.all_headers == {
        "tconst",
        "parentTconst",
        "seasonNumber",
        "episodeNumber",
    }

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_episode.col_args("tconst")
    assert actual == expected

    expected = {"index": False, "name": "seasonNumber", "type_": sqltypes.Integer}
    actual = table_builder_title_episode.col_args("seasonNumber")
    assert actual == expected
