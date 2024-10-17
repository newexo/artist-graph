from imdb.parser.s3.utils import DB_TRANSFORM
from sqlalchemy.sql import sqltypes
from sqlalchemy import inspect


# Example test function using the fixture
def test_table_builder_title_principals(table_builder_title_principals):
    assert table_builder_title_principals.fn == "title.principals.tsv.gz"
    assert table_builder_title_principals.headers == [
        "tconst",
        "ordering",
        "nconst",
        "category",
        "job",
        "characters",
    ]
    assert table_builder_title_principals.table_name == "title_principals"
    assert table_builder_title_principals.table_map == DB_TRANSFORM["title_principals"]

    table_builder = table_builder_title_principals
    expected = {"name": "nconst", "type_": sqltypes.Integer, "index": True}
    actual = table_builder.col_args("nconst")
    assert actual == expected

    expected = {
        "name": "characters",
        "type_": sqltypes.String(length=1024),
        "index": False,
    }
    actual = table_builder.col_args("characters")
    assert type(actual["type_"]) is type(expected["type_"])
    assert actual["type_"].length == expected["type_"].length
    del actual["type_"]
    del expected["type_"]
    assert expected == actual

    expected = {"name": "tconst", "type_": sqltypes.Integer, "index": True}
    actual = table_builder.col_args("tconst")
    assert actual == expected

    expected = {"name": "ordering", "type_": sqltypes.Integer, "index": False}
    actual = table_builder.col_args("ordering")
    assert actual == expected


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

    expected = {"index": True, "name": "nconst", "type_": sqltypes.Integer}
    actual = table_builder_name_basics.col_args("nconst")
    assert actual == expected

    expected = {"index": False, "name": "primaryName", "type_": sqltypes.UnicodeText}
    actual = table_builder_name_basics.col_args("primaryName")
    assert expected == actual


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

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_basics.col_args("tconst")
    assert actual == expected

    expected = {
        "name": "titleType",
        "type_": sqltypes.String(length=16),
        "index": True,
    }
    actual = table_builder_title_basics.col_args("titleType")
    assert type(actual["type_"]) is type(expected["type_"])
    assert actual["type_"].length == expected["type_"].length
    del actual["type_"]
    del expected["type_"]
    assert expected == actual


def test_table_builder_title_ratings(table_builder_title_ratings):
    assert table_builder_title_ratings.fn == "title.ratings.tsv.gz"
    assert table_builder_title_ratings.headers == [
        "tconst",
        "averageRating",
        "numVotes",
    ]
    assert table_builder_title_ratings.table_name == "title_ratings"
    assert table_builder_title_ratings.table_map == DB_TRANSFORM["title_ratings"]

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_ratings.col_args("tconst")
    assert actual == expected

    expected = {"index": True, "name": "averageRating", "type_": sqltypes.Float}
    actual = table_builder_title_ratings.col_args("averageRating")
    assert actual == expected


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


def test_table_builder_title_crew(table_builder_title_crew):
    assert table_builder_title_crew.fn == "title.crew.tsv.gz"
    assert table_builder_title_crew.headers == ["tconst", "directors", "writers"]
    assert table_builder_title_crew.table_name == "title_crew"
    assert table_builder_title_crew.table_map == DB_TRANSFORM["title_crew"]

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_crew.col_args("tconst")
    assert actual == expected

    expected = {"index": False, "name": "directors", "type_": sqltypes.UnicodeText}
    actual = table_builder_title_crew.col_args("directors")
    assert actual == expected


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

    expected = {"index": True, "name": "tconst", "type_": sqltypes.Integer}
    actual = table_builder_title_episode.col_args("tconst")
    assert actual == expected

    expected = {"index": False, "name": "seasonNumber", "type_": sqltypes.Integer}
    actual = table_builder_title_episode.col_args("seasonNumber")
    assert actual == expected


def verify_columns(columns, expected_columns, table_name):
    assert len(columns) == len(expected_columns)
    for column in columns:
        column_name = column["name"]
        column_type = type(column["type"])
        expected_type = expected_columns.get(column_name)
        assert (
            column_name in expected_columns
        ), f"Unexpected column: {column_name} in {table_name}"
        assert (
            column_type is expected_type
        ), f"Unexpected column type for {column_name} in {table_name}"


def test_create_table_name_basics(session, engine):
    inspector = inspect(engine)

    # Get column details for the 'name_basics' table
    columns = inspector.get_columns("name_basics")

    expected_columns = {
        "nconst": sqltypes.INTEGER,
        "primaryName": sqltypes.TEXT,
        "birthYear": sqltypes.INTEGER,
        "deathYear": sqltypes.INTEGER,
        "primaryProfession": sqltypes.TEXT,
        "knownForTitles": sqltypes.TEXT,
    }

    verify_columns(columns, expected_columns, "name_basics")


def test_create_table_title_basics(session, engine):
    inspector = inspect(engine)

    # Get column details for the 'title_basics' table
    columns = inspector.get_columns("title_basics")

    expected_columns = {
        "tconst": sqltypes.INTEGER,
        "titleType": sqltypes.VARCHAR,
        "primaryTitle": sqltypes.TEXT,
        "originalTitle": sqltypes.TEXT,
        "isAdult": sqltypes.BOOLEAN,
        "startYear": sqltypes.INTEGER,
        "endYear": sqltypes.INTEGER,
        "runtimeMinutes": sqltypes.INTEGER,
        "genres": sqltypes.TEXT,
    }

    verify_columns(columns, expected_columns, "title_basics")


def test_create_table_title_ratings(session, engine):
    inspector = inspect(engine)

    # Get column details for the 'title_ratings' table
    columns = inspector.get_columns("title_ratings")

    expected_columns = {
        "tconst": sqltypes.INTEGER,
        "averageRating": sqltypes.FLOAT,
        "numVotes": sqltypes.INTEGER,
    }

    verify_columns(columns, expected_columns, "title_ratings")


def test_create_table_title_principals(session, engine):
    inspector = inspect(engine)

    # Get column details for the 'title_principals' table
    columns = inspector.get_columns("title_principals")

    expected_columns = {
        "id": sqltypes.INTEGER,
        "tconst": sqltypes.INTEGER,
        "ordering": sqltypes.INTEGER,
        "nconst": sqltypes.INTEGER,
        "category": sqltypes.VARCHAR,
        "job": sqltypes.VARCHAR,
        "characters": sqltypes.VARCHAR,
    }

    verify_columns(columns, expected_columns, "title_principals")


def test_create_table_title_akas(session, engine):
    inspector = inspect(engine)

    # Get column details for the 'title_akas' table
    columns = inspector.get_columns("title_akas")

    expected_columns = {
        "id": sqltypes.INTEGER,
        "titleId": sqltypes.INTEGER,
        "ordering": sqltypes.INTEGER,
        "title": sqltypes.TEXT,
        "region": sqltypes.VARCHAR,
        "language": sqltypes.VARCHAR,
        "types": sqltypes.VARCHAR,
        "attributes": sqltypes.VARCHAR,
        "isOriginalTitle": sqltypes.BOOLEAN,
    }

    verify_columns(columns, expected_columns, "title_akas")


def test_create_table_title_crew(session, engine):
    inspector = inspect(engine)

    # Get column details for the 'title_crew' table
    columns = inspector.get_columns("title_crew")

    expected_columns = {
        "tconst": sqltypes.INTEGER,
        "directors": sqltypes.TEXT,
        "writers": sqltypes.TEXT,
    }

    verify_columns(columns, expected_columns, "title_crew")


def test_create_table_title_episode(session, engine):
    inspector = inspect(engine)

    # Get column details for the 'title_episode' table
    columns = inspector.get_columns("title_episode")

    expected_columns = {
        "tconst": sqltypes.INTEGER,
        "parentTconst": sqltypes.INTEGER,
        "seasonNumber": sqltypes.INTEGER,
        "episodeNumber": sqltypes.INTEGER,
    }

    verify_columns(columns, expected_columns, "title_episode")
