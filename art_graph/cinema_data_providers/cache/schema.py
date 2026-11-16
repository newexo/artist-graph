"""Create the cache tables, upgrading a cache written by an older version.

The cache holds nothing that cannot be fetched from TMDb again, so a stale
schema is replaced rather than migrated.
"""

import logging

from sqlalchemy import Engine, inspect

from .orm_models import Base

logger = logging.getLogger(__name__)

_CREDIT_KEY = {"person_id", "movie_id"}


def _credit_has_unique_pair(engine: Engine) -> bool:
    inspector = inspect(engine)
    unique = list(inspector.get_unique_constraints("credit"))
    unique += [i for i in inspector.get_indexes("credit") if i.get("unique")]
    return any(set(u["column_names"]) == _CREDIT_KEY for u in unique)


def ensure_schema(engine: Engine) -> None:
    """Create the cache tables, recreating them if they predate the credit
    uniqueness constraint.

    create_all never alters an existing table, so a credit table made by an
    older version keeps allowing duplicate (person, movie) rows, and adding the
    constraint would fail on the duplicates already stored. Drop and recreate.

    On Postgres the caller should serialise this across instances (for example
    with an advisory lock); the drop and create are not safe to race.
    """
    if inspect(engine).has_table("credit") and not _credit_has_unique_pair(engine):
        logger.warning(
            "TMDb cache credit table has no unique (person_id, movie_id) "
            "constraint (written by an older version); dropping and recreating "
            "the cache tables. Cached data is refetched from TMDb on demand."
        )
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
