from datetime import date

import sqlalchemy
from sqlalchemy.orm import Session

from art_graph.cinema_data_providers.cache.orm_models import (
    Base,
    PersonRecord,
    MovieRecord,
    CreditRecord,
)


def in_memory_engine():
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


class TestTableCreation:
    def test_tables_exist(self):
        engine = in_memory_engine()
        inspector = sqlalchemy.inspect(engine)
        table_names = inspector.get_table_names()
        assert "person" in table_names
        assert "movie" in table_names
        assert "credit" in table_names

    def test_person_columns(self):
        engine = in_memory_engine()
        inspector = sqlalchemy.inspect(engine)
        columns = {c["name"] for c in inspector.get_columns("person")}
        assert columns == {"tmdb_id", "name", "profile_path", "popularity", "has_full_filmography"}

    def test_movie_columns(self):
        engine = in_memory_engine()
        inspector = sqlalchemy.inspect(engine)
        columns = {c["name"] for c in inspector.get_columns("movie")}
        assert columns == {
            "tmdb_id",
            "title",
            "release_date",
            "poster_path",
            "popularity",
            "has_full_cast",
        }

    def test_credit_columns(self):
        engine = in_memory_engine()
        inspector = sqlalchemy.inspect(engine)
        columns = {c["name"] for c in inspector.get_columns("credit")}
        assert columns == {"id", "person_id", "movie_id", "character", "credit_order"}


class TestRoundTrip:
    def test_insert_and_read_person(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            session.add(
                PersonRecord(tmdb_id=6193, name="Leonardo DiCaprio", popularity=80.0)
            )
            session.commit()

        with Session(bind=engine) as session:
            person = session.get(PersonRecord, 6193)
            assert person.name == "Leonardo DiCaprio"
            assert person.popularity == 80.0

    def test_insert_and_read_movie(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            session.add(
                MovieRecord(
                    tmdb_id=27205,
                    title="Inception",
                    release_date=date(2010, 7, 16),
                    popularity=90.0,
                )
            )
            session.commit()

        with Session(bind=engine) as session:
            movie = session.get(MovieRecord, 27205)
            assert movie.title == "Inception"
            assert movie.release_date == date(2010, 7, 16)

    def test_insert_and_read_credit(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            session.add(PersonRecord(tmdb_id=6193, name="Leonardo DiCaprio"))
            session.add(MovieRecord(tmdb_id=27205, title="Inception"))
            session.add(
                CreditRecord(
                    person_id=6193,
                    movie_id=27205,
                    character="Cobb",
                    credit_order=0,
                )
            )
            session.commit()

        with Session(bind=engine) as session:
            credit = session.query(CreditRecord).first()
            assert credit.character == "Cobb"
            assert credit.credit_order == 0
            assert credit.person.name == "Leonardo DiCaprio"
            assert credit.movie.title == "Inception"

    def test_person_credits_relationship(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            session.add(PersonRecord(tmdb_id=6193, name="Leonardo DiCaprio"))
            session.add(MovieRecord(tmdb_id=27205, title="Inception"))
            session.add(MovieRecord(tmdb_id=597, title="Titanic"))
            session.add(CreditRecord(person_id=6193, movie_id=27205, character="Cobb"))
            session.add(
                CreditRecord(person_id=6193, movie_id=597, character="Jack Dawson")
            )
            session.commit()

        with Session(bind=engine) as session:
            person = session.get(PersonRecord, 6193)
            assert len(person.credits) == 2
            titles = {c.movie.title for c in person.credits}
            assert titles == {"Inception", "Titanic"}

    def test_movie_credits_relationship(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            session.add(PersonRecord(tmdb_id=6193, name="Leonardo DiCaprio"))
            session.add(PersonRecord(tmdb_id=24045, name="Joseph Gordon-Levitt"))
            session.add(MovieRecord(tmdb_id=27205, title="Inception"))
            session.add(
                CreditRecord(
                    person_id=6193, movie_id=27205, character="Cobb", credit_order=0
                )
            )
            session.add(
                CreditRecord(
                    person_id=24045, movie_id=27205, character="Arthur", credit_order=1
                )
            )
            session.commit()

        with Session(bind=engine) as session:
            movie = session.get(MovieRecord, 27205)
            assert len(movie.credits) == 2
            names = {c.person.name for c in movie.credits}
            assert names == {"Leonardo DiCaprio", "Joseph Gordon-Levitt"}
