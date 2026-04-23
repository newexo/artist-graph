import sqlalchemy
from sqlalchemy.orm import Session

from art_graph import directories
from .orm_models import Base


def db_path(db_filename="tmdb_cache.db") -> str:
    return directories.data(db_filename)


def get_engine(db_filename="tmdb_cache.db") -> sqlalchemy.Engine:
    absolute_path = db_path(db_filename=db_filename)
    return sqlalchemy.create_engine(f"sqlite:///{absolute_path}")


def create_tables(engine: sqlalchemy.Engine):
    Base.metadata.create_all(bind=engine)


def get_session(engine: sqlalchemy.Engine) -> Session:
    return Session(bind=engine)
