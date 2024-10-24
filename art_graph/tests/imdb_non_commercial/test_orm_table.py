from sqlalchemy.sql import sqltypes
from sqlalchemy import inspect


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


def test_indexes_name_basics(session, engine):
    inspector = inspect(engine)

    # Get index details for the 'name_basics' table
    indexes = inspector.get_indexes("name_basics")

    assert len(indexes) == 1
    assert indexes[0]["name"] == "ix_name_basics_nconst"


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


def test_indexes_title_basics(session, engine):
    inspector = inspect(engine)

    # Get index details for the 'title_basics' table
    indexes = inspector.get_indexes("title_basics")

    assert len(indexes) == 1
    assert indexes[0]["name"] == "ix_title_basics_tconst"


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
