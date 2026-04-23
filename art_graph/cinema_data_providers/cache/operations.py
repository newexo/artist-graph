"""Read/write operations for the TMDb cache.

All writes are upserts — if a person or movie already exists, their record is
updated with the latest data.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

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


def upsert_person(session: Session, person_id: int, name: str, **kwargs):
    record = session.get(PersonRecord, person_id)
    if record is None:
        record = PersonRecord(tmdb_id=person_id, name=name, **kwargs)
        session.add(record)
    else:
        record.name = name
        for key, value in kwargs.items():
            setattr(record, key, value)
    return record


def upsert_movie(session: Session, movie_id: int, title: str, **kwargs):
    record = session.get(MovieRecord, movie_id)
    if record is None:
        record = MovieRecord(tmdb_id=movie_id, title=title, **kwargs)
        session.add(record)
    else:
        record.title = title
        for key, value in kwargs.items():
            setattr(record, key, value)
    return record


def upsert_credit(
    session: Session,
    person_id: int,
    movie_id: int,
    character: Optional[str] = None,
    credit_order: Optional[int] = None,
):
    stmt = select(CreditRecord).where(
        CreditRecord.person_id == person_id,
        CreditRecord.movie_id == movie_id,
    )
    record = session.execute(stmt).scalar_one_or_none()
    if record is None:
        record = CreditRecord(
            person_id=person_id,
            movie_id=movie_id,
            character=character,
            credit_order=credit_order,
        )
        session.add(record)
    else:
        record.character = character
        record.credit_order = credit_order
    return record


# ---------------------------------------------------------------------------
# Store API responses
# ---------------------------------------------------------------------------


def store_person_movies(
    session: Session, person: Person, movies: List[MovieCreditRole]
):
    """Cache a person and their filmography (from get_person_movies)."""
    upsert_person(
        session,
        person.id,
        person.name,
        profile_path=person.profile_path,
        popularity=person.popularity,
    )
    for movie in movies:
        upsert_movie(
            session,
            movie.id,
            movie.title,
            release_date=movie.release_date,
            poster_path=movie.poster_path,
            popularity=movie.popularity,
        )
        upsert_credit(
            session,
            person_id=person.id,
            movie_id=movie.id,
            character=movie.character,
            credit_order=movie.order,
        )
    session.commit()


def store_movie_cast(session: Session, movie: Movie, cast: List[CastMember]):
    """Cache a movie and its cast (from get_movie_cast)."""
    upsert_movie(
        session,
        movie.id,
        movie.title,
        release_date=movie.release_date,
        poster_path=movie.poster_path,
        popularity=movie.popularity,
    )
    for member in cast:
        upsert_person(
            session,
            member.id,
            member.name,
            profile_path=member.profile_path,
            popularity=member.popularity,
        )
        upsert_credit(
            session,
            person_id=member.id,
            movie_id=movie.id,
            character=member.character,
            credit_order=member.order,
        )
    session.commit()


# ---------------------------------------------------------------------------
# Read helpers
# ---------------------------------------------------------------------------


def get_cached_person_movies(
    session: Session, person_id: int
) -> Optional[List[CreditRecord]]:
    """Return cached credits for a person, or None if the person isn't cached."""
    person = session.get(PersonRecord, person_id)
    if person is None:
        return None
    return person.credits


def get_cached_movie_cast(
    session: Session, movie_id: int
) -> Optional[List[CreditRecord]]:
    """Return cached credits for a movie, or None if the movie isn't cached."""
    movie = session.get(MovieRecord, movie_id)
    if movie is None:
        return None
    return movie.credits
