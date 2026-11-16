"""ensure_schema upgrades a cache written before credits were unique."""

import logging

import pytest
from sqlalchemy import create_engine, inspect, text

from art_graph.cinema_data_providers.cache.orm_models import Base
from art_graph.cinema_data_providers.cache.schema import ensure_schema


@pytest.fixture
def engine(tmp_path):
    eng = create_engine(f"sqlite:///{tmp_path / 'cache.db'}")
    yield eng
    eng.dispose()


def make_old_schema(engine):
    """The tables as 0.3.0 created them: no unique constraint on credit."""
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE person (tmdb_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, profile_path VARCHAR, popularity FLOAT, has_full_filmography BOOLEAN NOT NULL)"
            )
        )
        conn.execute(
            text(
                "CREATE TABLE movie (tmdb_id INTEGER PRIMARY KEY, title VARCHAR NOT NULL, release_date DATE, poster_path VARCHAR, popularity FLOAT, has_full_cast BOOLEAN NOT NULL)"
            )
        )
        conn.execute(
            text(
                "CREATE TABLE credit (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL REFERENCES person (tmdb_id), movie_id INTEGER NOT NULL REFERENCES movie (tmdb_id), character VARCHAR, credit_order INTEGER)"
            )
        )
        conn.execute(text("INSERT INTO person VALUES (1, 'A', NULL, 0, 1)"))
        conn.execute(text("INSERT INTO movie VALUES (2, 'M', NULL, NULL, 0, 1)"))
        # the duplicates that made the old schema a problem
        conn.execute(
            text("INSERT INTO credit (person_id, movie_id) VALUES (1, 2), (1, 2)")
        )


def unique_columns(engine):
    return [
        set(u["column_names"]) for u in inspect(engine).get_unique_constraints("credit")
    ]


def test_fresh_database_gets_the_constraint(engine):
    ensure_schema(engine)
    assert {"person_id", "movie_id"} in unique_columns(engine)


def test_old_schema_is_recreated_with_the_constraint(engine, caplog):
    make_old_schema(engine)

    with caplog.at_level(logging.WARNING):
        ensure_schema(engine)

    assert {"person_id", "movie_id"} in unique_columns(engine)
    with engine.connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM credit")).scalar() == 0
    assert "dropping and recreating" in caplog.text


def test_current_schema_is_left_alone(engine, caplog):
    ensure_schema(engine)
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO person VALUES (1, 'A', NULL, 0, 1)"))

    with caplog.at_level(logging.WARNING):
        ensure_schema(engine)

    with engine.connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM person")).scalar() == 1
    assert "dropping" not in caplog.text


def test_metadata_matches_what_is_created(engine):
    ensure_schema(engine)
    assert set(inspect(engine).get_table_names()) == set(Base.metadata.tables)


@pytest.fixture
def postgres_engine():
    import os

    url = os.getenv("TEST_DATABASE_URL", "")
    if not url.startswith("postgres"):
        pytest.skip("needs a real Postgres in TEST_DATABASE_URL")
    eng = create_engine(url)
    Base.metadata.drop_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


def test_old_schema_is_recreated_on_postgres(postgres_engine):
    Base.metadata.create_all(postgres_engine)
    with postgres_engine.begin() as conn:
        conn.execute(text("ALTER TABLE credit DROP CONSTRAINT uq_credit_person_movie"))
        conn.execute(text("INSERT INTO person VALUES (1, 'A', NULL, 0, true)"))
        conn.execute(text("INSERT INTO movie VALUES (2, 'M', NULL, NULL, 0, true)"))
        conn.execute(
            text("INSERT INTO credit (person_id, movie_id) VALUES (1, 2), (1, 2)")
        )
    assert {"person_id", "movie_id"} not in unique_columns(postgres_engine)

    ensure_schema(postgres_engine)

    assert {"person_id", "movie_id"} in unique_columns(postgres_engine)
    with postgres_engine.connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM credit")).scalar() == 0
