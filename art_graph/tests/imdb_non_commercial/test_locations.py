import sqlalchemy

from ...cinema_data_providers.imbd_non_commercial import locations


def test_imdb_files():
    assert set(locations.imdb_files) == {
        "name.basics.tsv.gz",
        "title.akas.tsv.gz",
        "title.basics.tsv.gz",
        "title.crew.tsv.gz",
        "title.episode.tsv.gz",
        "title.principals.tsv.gz",
        "title.ratings.tsv.gz",
    }


def test_db_path_for_sqlite():
    assert locations.db_path_for_sqlite().endswith("data/IM.db")

    assert locations.db_path_for_sqlite("foo-bar.db").endswith("data/foo-bar.db")


def test_get_sqlite_engine():
    engine = locations.get_sqlite_engine()
    assert isinstance(engine, sqlalchemy.engine.base.Engine)
    assert engine.url.database.endswith("data/IM.db")

    assert locations.get_sqlite_engine("foo-bar.db").url.database.endswith(
        "data/foo-bar.db"
    )
