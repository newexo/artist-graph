import pytest

from ...cinema_data_providers.imdb_non_commercial import (
    imdb_non_commercial_orm_models as imdb_orm,
)
from ...cinema_data_providers.imdb_non_commercial import (
    imdb_non_commercial_pydantic_models as imdb_pyd,
)


@pytest.fixture
def connection(engine):
    return engine.connect()


def test_read_write_name_basics(
    table_name_basics, connection, name_basics_data, session
):
    block = name_basics_data
    insert = table_name_basics.insert()
    with connection.begin() as transaction:
        try:
            connection.execute(insert, block)
        except Exception as e:
            pytest.fail(f"Error inserting data: {e}")
        finally:
            results = (
                session.query(imdb_orm.NameBasics)
                .order_by(imdb_orm.NameBasics.nconst)
                .all()
            )
            pyd_objs = [
                imdb_pyd.NameBasics(**r.__dict__) for r in results
            ]  # convert to pydantic objects
            actual = [
                dict(pyd_obj) for pyd_obj in pyd_objs
            ]  # convert to list of dictionaries
            assert actual == block
            transaction.rollback()


def test_read_write_title_basics(
    table_title_basics, connection, title_basics_data, session
):
    block = title_basics_data
    insert = table_title_basics.insert()
    with connection.begin() as transaction:
        try:
            connection.execute(insert, block)
        except Exception as e:
            pytest.fail(f"Error inserting data: {e}")
        finally:
            results = (
                session.query(imdb_orm.TitleBasics)
                .order_by(imdb_orm.TitleBasics.tconst)
                .all()
            )
            pyd_objs = [
                imdb_pyd.TitleBasics(**r.__dict__) for r in results
            ]  # convert to pydantic objects
            actual = [
                dict(pyd_obj) for pyd_obj in pyd_objs
            ]  # convert to list of dictionaries
            assert actual == block
            transaction.rollback()


def test_read_write_title_ratings(
    table_title_ratings, connection, title_ratings_data, session
):
    block = title_ratings_data
    insert = table_title_ratings.insert()
    with connection.begin() as transaction:
        try:
            connection.execute(insert, block)
        except Exception as e:
            pytest.fail(f"Error inserting data: {e}")
        finally:
            results = (
                session.query(imdb_orm.TitleRatings)
                .order_by(imdb_orm.TitleRatings.tconst)
                .all()
            )
            pyd_objs = [
                imdb_pyd.TitleRatings(**r.__dict__) for r in results
            ]  # convert to pydantic objects
            actual = [
                dict(pyd_obj) for pyd_obj in pyd_objs
            ]  # convert to list of dictionaries
            assert actual == block
            transaction.rollback()


def test_read_write_title_principals(
    table_title_principals, connection, title_principals_data, session
):
    block = title_principals_data
    insert = table_title_principals.insert()
    with connection.begin() as transaction:
        try:
            connection.execute(insert, block)
        except Exception as e:
            pytest.fail(f"Error inserting data: {e}")
        finally:
            results = (
                session.query(imdb_orm.TitlePrincipals)
                .order_by(imdb_orm.TitlePrincipals.tconst)
                .all()
            )
            pyd_objs = [
                imdb_pyd.TitlePrincipals(**r.__dict__) for r in results
            ]  # convert to pydantic objects
            actual = [
                dict(pyd_obj) for pyd_obj in pyd_objs
            ]  # convert to list of dictionaries
            assert actual == block
            transaction.rollback()


def test_read_write_title_akas(table_title_akas, connection, title_akas_data, session):
    block = title_akas_data
    insert = table_title_akas.insert()
    with connection.begin() as transaction:
        try:
            connection.execute(insert, block)
        except Exception as e:
            pytest.fail(f"Error inserting data: {e}")
        finally:
            results = (
                session.query(imdb_orm.TitleAkas)
                .order_by(imdb_orm.TitleAkas.titleId)
                .all()
            )
            pyd_objs = [imdb_pyd.TitleAkas(**r.__dict__) for r in results]
            actual = [dict(pyd_obj) for pyd_obj in pyd_objs]
            assert actual == block
            transaction.rollback()


def test_read_write_title_crew(table_title_crew, connection, title_crew_data, session):
    block = title_crew_data
    insert = table_title_crew.insert()
    with connection.begin() as transaction:
        try:
            connection.execute(insert, block)
        except Exception as e:
            pytest.fail(f"Error inserting data: {e}")
        finally:
            results = (
                session.query(imdb_orm.TitleCrew)
                .order_by(imdb_orm.TitleCrew.tconst)
                .all()
            )
            pyd_objs = [imdb_pyd.TitleCrew(**r.__dict__) for r in results]
            actual = [dict(pyd_obj) for pyd_obj in pyd_objs]
            assert actual == block
            transaction.rollback()


def test_read_write_title_episode(
    table_title_episode, connection, title_episode_data, session
):
    block = title_episode_data
    insert = table_title_episode.insert()
    with connection.begin() as transaction:
        try:
            connection.execute(insert, block)
        except Exception as e:
            pytest.fail(f"Error inserting data: {e}")
        finally:
            results = (
                session.query(imdb_orm.TitleEpisode)
                .order_by(imdb_orm.TitleEpisode.tconst)
                .all()
            )
            pyd_objs = [imdb_pyd.TitleEpisode(**r.__dict__) for r in results]
            actual = [dict(pyd_obj) for pyd_obj in pyd_objs]
            assert actual == block
            transaction.rollback()
