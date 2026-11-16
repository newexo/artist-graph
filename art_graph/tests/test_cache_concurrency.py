"""Concurrency and efficiency tests for the TMDb cache.

The races are forced, not timed: a barrier on the first INSERT into a table
holds both writers until each has finished its reads, which is exactly the
window a read-then-insert write path loses. Each test runs on SQLite (a file,
since the writers need separate connections) and, when TEST_DATABASE_URL points
at Postgres, on Postgres. The Postgres runs drop the cache tables, so use a
scratch database.
"""

import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import date

import pytest
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from art_graph.cinema_data_providers.cache.operations import (
    get_cached_movie_cast,
    get_cached_person_movies,
    store_movie_cast,
    store_person_movies,
    upsert_movie,
    upsert_person,
)
from art_graph.cinema_data_providers.cache.orm_models import (
    Base,
    CreditRecord,
    MovieRecord,
    PersonRecord,
)
from art_graph.cinema_data_providers.tmdb_models import (
    CastMember,
    Movie,
    MovieCreditRole,
    Person,
)

PERSON = Person(id=6193, name="Leonardo DiCaprio", popularity=80.0)
MOVIE = Movie(id=27205, title="Inception", popularity=90.0)


def filmography(n):
    return [
        MovieCreditRole(
            id=1000 + i,
            title=f"Movie {i}",
            release_date=date(2000, 1, 1),
            popularity=float(i),
            character=f"Role {i}",
            order=i,
        )
        for i in range(n)
    ]


def cast(n):
    return [
        CastMember(id=2000 + i, name=f"Actor {i}", character=f"Role {i}", order=i)
        for i in range(n)
    ]


@pytest.fixture(params=["sqlite", "postgres"])
def engine(request, tmp_path):
    if request.param == "sqlite":
        eng = create_engine(
            f"sqlite:///{tmp_path / 'cache.db'}", connect_args={"timeout": 30}
        )
    else:
        url = os.getenv("TEST_DATABASE_URL", "")
        if not url.startswith("postgres"):
            pytest.skip("needs a real Postgres in TEST_DATABASE_URL")
        eng = create_engine(url)
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


def rendezvous(engine, table, timeout=3):
    """Hold each thread's first INSERT INTO <table> until both have reached it.

    If one writer cannot reach the INSERT because the database has serialised
    them earlier (row or file locks), the wait times out and it proceeds, so
    the test still checks the outcome.
    """
    barrier = threading.Barrier(2)
    seen = threading.local()

    @event.listens_for(engine, "before_cursor_execute")
    def _hold(conn, cursor, statement, params, context, executemany):
        if statement.lstrip().startswith(f"INSERT INTO {table} ") and not getattr(
            seen, "held", False
        ):
            seen.held = True
            try:
                barrier.wait(timeout=timeout)
            except threading.BrokenBarrierError:
                pass


def run_together(engine, fn):
    def worker(_):
        with Session(bind=engine) as session:
            fn(session)

    with ThreadPoolExecutor(2) as pool:
        for future in [pool.submit(worker, i) for i in range(2)]:
            future.result()  # re-raises a writer's failure


def count(engine, model):
    with Session(bind=engine) as session:
        return session.scalar(select(func.count()).select_from(model))


class TestConcurrentWriters:
    def test_two_writers_caching_the_same_new_person(self, engine):
        rendezvous(engine, "person")
        movies = filmography(5)

        run_together(engine, lambda s: store_person_movies(s, PERSON, movies))

        assert count(engine, PersonRecord) == 1
        assert count(engine, MovieRecord) == 5
        assert count(engine, CreditRecord) == 5

    def test_two_writers_caching_the_same_new_movie_cast(self, engine):
        rendezvous(engine, "movie")
        members = cast(5)

        run_together(engine, lambda s: store_movie_cast(s, MOVIE, members))

        assert count(engine, MovieRecord) == 1
        assert count(engine, PersonRecord) == 5
        assert count(engine, CreditRecord) == 5

    def test_credits_are_not_duplicated_when_people_and_movies_exist(self, engine):
        movies = filmography(5)
        # Cache people and movies with exactly the values the writers will send,
        # so neither writer updates (and so row-locks) them before its credits.
        with Session(bind=engine) as session:
            upsert_person(
                session,
                PERSON.id,
                PERSON.name,
                profile_path=None,
                popularity=PERSON.popularity,
                has_full_filmography=True,
            )
            for m in movies:
                upsert_movie(
                    session,
                    m.id,
                    m.title,
                    release_date=m.release_date,
                    poster_path=m.poster_path,
                    popularity=m.popularity,
                )
            session.commit()
        rendezvous(engine, "credit")

        run_together(engine, lambda s: store_person_movies(s, PERSON, movies))

        assert count(engine, CreditRecord) == 5

    def test_a_person_and_a_movie_written_in_opposite_orders_do_not_deadlock(
        self, engine
    ):
        # store_person_movies and store_movie_cast touch the same rows; a
        # deadlock would surface as an OperationalError from one of them.
        movies = filmography(5)
        members = [
            CastMember(id=PERSON.id, name=PERSON.name, character="x", order=0)
        ] + cast(4)
        movie = Movie(id=movies[0].id, title=movies[0].title)

        def person_side(_):
            with Session(bind=engine) as session:
                for _ in range(20):
                    store_person_movies(session, PERSON, movies)

        def movie_side(_):
            with Session(bind=engine) as session:
                for _ in range(20):
                    store_movie_cast(session, movie, members)

        with ThreadPoolExecutor(2) as pool:
            futures = [pool.submit(person_side, 0), pool.submit(movie_side, 0)]
            for future in futures:
                future.result()

        with Session(bind=engine) as session:
            pairs = session.execute(
                select(CreditRecord.person_id, CreditRecord.movie_id)
            ).all()
        assert len(pairs) == len(set(pairs))


class TestCreditUniqueness:
    def test_duplicate_credit_is_rejected(self, engine):
        with Session(bind=engine) as session:
            upsert_person(session, 1, "A")
            upsert_movie(session, 2, "M")
            session.add(CreditRecord(person_id=1, movie_id=2))
            session.commit()
            session.add(CreditRecord(person_id=1, movie_id=2))
            with pytest.raises(IntegrityError):
                session.commit()

    def test_storing_twice_keeps_one_credit_per_pair(self, engine):
        movies = filmography(3)
        for _ in range(2):
            with Session(bind=engine) as session:
                store_person_movies(session, PERSON, movies)
        assert count(engine, CreditRecord) == 3

    def test_repeated_ids_in_one_response_collapse(self, engine):
        """TMDb can list a person twice in a cast; the last entry wins."""
        members = [
            CastMember(id=1, name="A", character="First", order=0),
            CastMember(id=1, name="A", character="Second", order=1),
        ]
        with Session(bind=engine) as session:
            store_movie_cast(session, MOVIE, members)
            credits = get_cached_movie_cast(session, MOVIE.id)
            assert [(c.character, c.credit_order) for c in credits] == [("Second", 1)]


class TestUpsertSemantics:
    def test_storing_a_cast_does_not_reset_has_full_filmography(self, engine):
        with Session(bind=engine) as session:
            store_person_movies(session, PERSON, filmography(2))
            store_movie_cast(
                session,
                Movie(id=1000, title="Movie 0"),
                [CastMember(id=PERSON.id, name=PERSON.name, character="x", order=0)],
            )
            person = session.get(PersonRecord, PERSON.id)
            session.refresh(person)
            assert person.has_full_filmography is True

    def test_storing_a_filmography_does_not_reset_has_full_cast(self, engine):
        with Session(bind=engine) as session:
            store_movie_cast(session, Movie(id=1000, title="Movie 0"), cast(2))
            store_person_movies(session, PERSON, filmography(2))
            movie = session.get(MovieRecord, 1000)
            session.refresh(movie)
            assert movie.has_full_cast is True

    def test_a_restore_updates_existing_rows(self, engine):
        with Session(bind=engine) as session:
            store_person_movies(session, PERSON, filmography(1))
            changed = [filmography(1)[0].model_copy(update={"popularity": 99.0})]
            store_person_movies(session, PERSON, changed)
            movie = session.get(MovieRecord, 1000)
            session.refresh(movie)
            assert movie.popularity == 99.0


class TestStatementCounts:
    @staticmethod
    def statements(engine):
        seen = []
        event.listen(
            engine,
            "before_cursor_execute",
            lambda conn, cur, stmt, params, ctx, many: seen.append(stmt),
        )
        return seen

    def test_caching_a_20_movie_filmography(self, engine):
        movies = filmography(20)
        seen = self.statements(engine)
        with Session(bind=engine) as session:
            store_person_movies(session, PERSON, movies)
        assert len(seen) <= 3, seen  # was 82

    def test_caching_a_cast(self, engine):
        members = cast(20)
        seen = self.statements(engine)
        with Session(bind=engine) as session:
            store_movie_cast(session, MOVIE, members)
        assert len(seen) <= 3, seen

    def test_reading_a_cached_filmography(self, engine):
        with Session(bind=engine) as session:
            store_person_movies(session, PERSON, filmography(20))
        seen = self.statements(engine)
        with Session(bind=engine) as session:
            credits = get_cached_person_movies(session, PERSON.id)
            assert len(credits) == 20
            assert [c.movie.title for c in credits]  # already loaded
        assert len(seen) <= 2, seen  # was 22

    def test_reading_a_cached_cast(self, engine):
        with Session(bind=engine) as session:
            store_movie_cast(session, MOVIE, cast(20))
        seen = self.statements(engine)
        with Session(bind=engine) as session:
            credits = get_cached_movie_cast(session, MOVIE.id)
            assert len(credits) == 20
            assert [c.person.name for c in credits]
        assert len(seen) <= 2, seen
