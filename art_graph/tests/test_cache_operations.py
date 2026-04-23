from datetime import date

import sqlalchemy
from sqlalchemy.orm import Session

from art_graph.cinema_data_providers.cache.orm_models import (
    Base,
    PersonRecord,
    MovieRecord,
)
from art_graph.cinema_data_providers.cache.operations import (
    upsert_person,
    upsert_movie,
    upsert_credit,
    store_person_movies,
    store_movie_cast,
    get_cached_person_movies,
    get_cached_movie_cast,
)
from art_graph.cinema_data_providers.tmdb_models import (
    CastMember,
    MovieCreditRole,
    Person,
    Movie,
)


def in_memory_engine():
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


class TestUpsert:
    def test_upsert_person_insert(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            upsert_person(session, 6193, "Leonardo DiCaprio", popularity=80.0)
            session.commit()

        with Session(bind=engine) as session:
            person = session.get(PersonRecord, 6193)
            assert person.name == "Leonardo DiCaprio"
            assert person.popularity == 80.0

    def test_upsert_person_update(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            upsert_person(session, 6193, "Leonardo DiCaprio", popularity=80.0)
            session.commit()

        with Session(bind=engine) as session:
            upsert_person(session, 6193, "Leonardo DiCaprio", popularity=85.0)
            session.commit()

        with Session(bind=engine) as session:
            person = session.get(PersonRecord, 6193)
            assert person.popularity == 85.0

    def test_upsert_movie_insert(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            upsert_movie(session, 27205, "Inception", release_date=date(2010, 7, 16))
            session.commit()

        with Session(bind=engine) as session:
            movie = session.get(MovieRecord, 27205)
            assert movie.title == "Inception"
            assert movie.release_date == date(2010, 7, 16)

    def test_upsert_movie_update(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            upsert_movie(session, 27205, "Inception", popularity=80.0)
            session.commit()

        with Session(bind=engine) as session:
            upsert_movie(session, 27205, "Inception", popularity=90.0)
            session.commit()

        with Session(bind=engine) as session:
            movie = session.get(MovieRecord, 27205)
            assert movie.popularity == 90.0

    def test_upsert_credit_insert(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            upsert_person(session, 6193, "Leonardo DiCaprio")
            upsert_movie(session, 27205, "Inception")
            upsert_credit(session, 6193, 27205, character="Cobb", credit_order=0)
            session.commit()

        with Session(bind=engine) as session:
            credits = get_cached_movie_cast(session, 27205)
            assert len(credits) == 1
            assert credits[0].character == "Cobb"

    def test_upsert_credit_update(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            upsert_person(session, 6193, "Leonardo DiCaprio")
            upsert_movie(session, 27205, "Inception")
            upsert_credit(session, 6193, 27205, character="Cobb", credit_order=0)
            session.commit()

        with Session(bind=engine) as session:
            upsert_credit(session, 6193, 27205, character="Dom Cobb", credit_order=0)
            session.commit()

        with Session(bind=engine) as session:
            credits = get_cached_movie_cast(session, 27205)
            assert len(credits) == 1
            assert credits[0].character == "Dom Cobb"


class TestStorePersonMovies:
    def test_stores_person_and_movies(self):
        engine = in_memory_engine()
        person = Person(id=6193, name="Leonardo DiCaprio", popularity=80.0)
        movies = [
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

        with Session(bind=engine) as session:
            store_person_movies(session, person, movies)

        with Session(bind=engine) as session:
            cached = get_cached_person_movies(session, 6193)
            assert len(cached) == 2
            titles = {c.movie.title for c in cached}
            assert titles == {"Inception", "Titanic"}

    def test_returns_none_for_uncached_person(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            assert get_cached_person_movies(session, 9999) is None


class TestStoreMovieCast:
    def test_stores_movie_and_cast(self):
        engine = in_memory_engine()
        movie = Movie(id=27205, title="Inception", release_date=date(2010, 7, 16))
        cast = [
            CastMember(id=6193, name="Leonardo DiCaprio", character="Cobb", order=0),
            CastMember(
                id=24045, name="Joseph Gordon-Levitt", character="Arthur", order=1
            ),
        ]

        with Session(bind=engine) as session:
            store_movie_cast(session, movie, cast)

        with Session(bind=engine) as session:
            cached = get_cached_movie_cast(session, 27205)
            assert len(cached) == 2
            names = {c.person.name for c in cached}
            assert names == {"Leonardo DiCaprio", "Joseph Gordon-Levitt"}

    def test_returns_none_for_uncached_movie(self):
        engine = in_memory_engine()
        with Session(bind=engine) as session:
            assert get_cached_movie_cast(session, 9999) is None


class TestOverlappingData:
    def test_shared_movie_across_two_people(self):
        """Two actors in the same movie — the movie record should be shared."""
        engine = in_memory_engine()
        person_a = Person(id=6193, name="Leonardo DiCaprio")
        person_b = Person(id=24045, name="Joseph Gordon-Levitt")
        inception_a = MovieCreditRole(
            id=27205,
            title="Inception",
            character="Cobb",
            order=0,
        )
        inception_b = MovieCreditRole(
            id=27205,
            title="Inception",
            character="Arthur",
            order=1,
        )

        with Session(bind=engine) as session:
            store_person_movies(session, person_a, [inception_a])
            store_person_movies(session, person_b, [inception_b])

        with Session(bind=engine) as session:
            cast = get_cached_movie_cast(session, 27205)
            assert len(cast) == 2

            person_a_movies = get_cached_person_movies(session, 6193)
            assert len(person_a_movies) == 1
            assert person_a_movies[0].character == "Cobb"
