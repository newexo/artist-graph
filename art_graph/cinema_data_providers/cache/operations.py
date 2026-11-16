"""Read/write operations for the TMDb cache.

All writes are upserts: if a person, movie or credit already exists it is
updated with the latest data. They are single ``INSERT ... ON CONFLICT DO
UPDATE`` statements, never a read followed by an insert, so two writers caching
the same rows at once converge instead of one failing with a unique violation
or both inserting the same credit. Only the columns a caller supplies are
updated, so storing a cast does not reset ``has_full_filmography`` and storing a
filmography does not reset ``has_full_cast``.

Postgres and SQLite are supported.
"""

from typing import Any, Dict, List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.orm import Session, joinedload

from .orm_models import PersonRecord, MovieRecord, CreditRecord
from ..tmdb_models import (
    CastMember,
    MovieCreditRole,
    Person,
    Movie,
)


# ---------------------------------------------------------------------------
# Write helpers
# ---------------------------------------------------------------------------


def _insert_for(session: Session):
    dialect = session.get_bind().dialect.name
    if dialect == "postgresql":
        return postgresql.insert
    if dialect == "sqlite":
        return sqlite.insert
    raise NotImplementedError(
        f"The TMDb cache needs ON CONFLICT upserts; {dialect!r} is not supported "
        "(use PostgreSQL or SQLite)."
    )


def _bulk_upsert(
    session: Session, model, rows: Sequence[Dict[str, Any]], key: Sequence[str]
) -> None:
    """Upsert rows (all with the same columns) on the ``key`` columns.

    Repeated keys within ``rows`` collapse to the last one, as TMDb sometimes
    lists a person twice in a cast and Postgres rejects a statement that would
    update the same row twice. Rows go out sorted by key so that concurrent
    writers lock overlapping rows in the same order and cannot deadlock.
    """
    if not rows:
        return
    latest = {tuple(row[col] for col in key): row for row in rows}
    ordered = [latest[k] for k in sorted(latest)]
    table = model.__table__
    stmt = _insert_for(session)(table)
    update = {col: stmt.excluded[col] for col in ordered[0] if col not in key}
    if update:
        stmt = stmt.on_conflict_do_update(index_elements=list(key), set_=update)
    else:
        stmt = stmt.on_conflict_do_nothing(index_elements=list(key))
    session.execute(stmt, ordered)


def _reload(session: Session, model, **key):
    """The row as the database now has it (the ORM copy is stale after a Core
    upsert)."""
    stmt = select(model).filter_by(**key).execution_options(populate_existing=True)
    return session.execute(stmt).scalar_one()


def upsert_person(session: Session, person_id: int, name: str, **kwargs):
    _bulk_upsert(
        session,
        PersonRecord,
        [{"tmdb_id": person_id, "name": name, **kwargs}],
        key=["tmdb_id"],
    )
    return _reload(session, PersonRecord, tmdb_id=person_id)


def upsert_movie(session: Session, movie_id: int, title: str, **kwargs):
    _bulk_upsert(
        session,
        MovieRecord,
        [{"tmdb_id": movie_id, "title": title, **kwargs}],
        key=["tmdb_id"],
    )
    return _reload(session, MovieRecord, tmdb_id=movie_id)


def upsert_credit(
    session: Session,
    person_id: int,
    movie_id: int,
    character: Optional[str] = None,
    credit_order: Optional[int] = None,
):
    _bulk_upsert(
        session,
        CreditRecord,
        [
            {
                "person_id": person_id,
                "movie_id": movie_id,
                "character": character,
                "credit_order": credit_order,
            }
        ],
        key=["person_id", "movie_id"],
    )
    return _reload(session, CreditRecord, person_id=person_id, movie_id=movie_id)


# ---------------------------------------------------------------------------
# Store API responses
# ---------------------------------------------------------------------------
#
# Both store functions write people, then movies, then credits. Keeping the
# table order the same in both, and key order within a table (see
# _bulk_upsert), is what keeps concurrent writers from deadlocking.


def store_person_movies(
    session: Session, person: Person, movies: List[MovieCreditRole]
):
    """Cache a person and their filmography (from get_person_movies)."""
    _bulk_upsert(
        session,
        PersonRecord,
        [
            {
                "tmdb_id": person.id,
                "name": person.name,
                "profile_path": person.profile_path,
                "popularity": person.popularity,
                "has_full_filmography": True,
            }
        ],
        key=["tmdb_id"],
    )
    _bulk_upsert(
        session,
        MovieRecord,
        [
            {
                "tmdb_id": m.id,
                "title": m.title,
                "release_date": m.release_date,
                "poster_path": m.poster_path,
                "popularity": m.popularity,
            }
            for m in movies
        ],
        key=["tmdb_id"],
    )
    _bulk_upsert(
        session,
        CreditRecord,
        [
            {
                "person_id": person.id,
                "movie_id": m.id,
                "character": m.character,
                "credit_order": m.order,
            }
            for m in movies
        ],
        key=["person_id", "movie_id"],
    )
    session.commit()


def store_movie_cast(session: Session, movie: Movie, cast: List[CastMember]):
    """Cache a movie and its cast (from get_movie_cast)."""
    _bulk_upsert(
        session,
        PersonRecord,
        [
            {
                "tmdb_id": c.id,
                "name": c.name,
                "profile_path": c.profile_path,
                "popularity": c.popularity,
            }
            for c in cast
        ],
        key=["tmdb_id"],
    )
    _bulk_upsert(
        session,
        MovieRecord,
        [
            {
                "tmdb_id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date,
                "poster_path": movie.poster_path,
                "popularity": movie.popularity,
                "has_full_cast": True,
            }
        ],
        key=["tmdb_id"],
    )
    _bulk_upsert(
        session,
        CreditRecord,
        [
            {
                "person_id": c.id,
                "movie_id": movie.id,
                "character": c.character,
                "credit_order": c.order,
            }
            for c in cast
        ],
        key=["person_id", "movie_id"],
    )
    session.commit()


# ---------------------------------------------------------------------------
# Read helpers
# ---------------------------------------------------------------------------


def get_cached_person_movies(
    session: Session, person_id: int
) -> Optional[List[CreditRecord]]:
    """Return cached credits for a person, or None if the person isn't cached.

    Each credit's ``movie`` is loaded in the same query.
    """
    if session.get(PersonRecord, person_id) is None:
        return None
    stmt = (
        select(CreditRecord)
        .where(CreditRecord.person_id == person_id)
        .options(joinedload(CreditRecord.movie))
    )
    return list(session.scalars(stmt))


def get_cached_movie_cast(
    session: Session, movie_id: int
) -> Optional[List[CreditRecord]]:
    """Return cached credits for a movie, or None if the movie isn't cached.

    Each credit's ``person`` is loaded in the same query.
    """
    if session.get(MovieRecord, movie_id) is None:
        return None
    stmt = (
        select(CreditRecord)
        .where(CreditRecord.movie_id == movie_id)
        .options(joinedload(CreditRecord.person))
    )
    return list(session.scalars(stmt))
