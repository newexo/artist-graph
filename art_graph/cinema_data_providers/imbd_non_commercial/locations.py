import sqlalchemy

from art_graph import directories


def db_path_for_sqlite() -> str:
    return directories.data("IM.db")


def get_sqlite_engine() -> sqlalchemy.Engine:
    absolute_path = db_path_for_sqlite()
    return sqlalchemy.create_engine(f"sqlite:////{absolute_path}")


imdb_files = [
    "name.basics.tsv.gz",
    "title.basics.tsv.gz",
    "title.ratings.tsv.gz",
    "title.principals.tsv.gz",
    "title.akas.tsv.gz",  # Add additional files if necessary
    "title.crew.tsv.gz",  # Add title.crew.tsv.gz
    "title.episode.tsv.gz",  # Add title.episode.tsv.gz
]
