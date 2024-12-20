import pytest

from ...cinema_data_providers.imdb_non_commercial import (
    imdb_non_commercial_orm_models as imdb_orm,
)
from ...cinema_data_providers.imdb_non_commercial import (
    imdb_non_commercial_pydantic_models as imdb_pyd,
)


def test_name2orm():
    assert imdb_orm.NAME2ORM["name_basics"] == imdb_orm.NameBasics
    assert imdb_orm.NAME2ORM["title_akas"] == imdb_orm.TitleAkas
    assert imdb_orm.NAME2ORM["title_basics"] == imdb_orm.TitleBasics
    assert imdb_orm.NAME2ORM["title_crew"] == imdb_orm.TitleCrew
    assert imdb_orm.NAME2ORM["title_episode"] == imdb_orm.TitleEpisode
    assert imdb_orm.NAME2ORM["title_principals"] == imdb_orm.TitlePrincipals


def test_name2pyd():
    assert set(imdb_pyd.NAME2PYD.keys()) == set(imdb_orm.NAME2ORM.keys())
    assert imdb_pyd.NAME2PYD["name_basics"] == imdb_pyd.NameBasics
    assert imdb_pyd.NAME2PYD["title_akas"] == imdb_pyd.TitleAkas
    assert imdb_pyd.NAME2PYD["title_basics"] == imdb_pyd.TitleBasics
    assert imdb_pyd.NAME2PYD["title_crew"] == imdb_pyd.TitleCrew
    assert imdb_pyd.NAME2PYD["title_episode"] == imdb_pyd.TitleEpisode
    assert imdb_pyd.NAME2PYD["title_principals"] == imdb_pyd.TitlePrincipals


def test_read_write_name_basics(name_basics_data, session):
    block = name_basics_data
    # First validate the data
    pyd_block = [imdb_pyd.NameBasics(**r) for r in block]
    # Turn into ORM objects
    orm_block = [r.to_orm() for r in pyd_block]
    try:
        # Insert the data
        session.add_all(orm_block)

        # Read data back and verify
        results = (
            session.query(imdb_orm.NameBasics)
            .order_by(imdb_orm.NameBasics.nconst)
            .all()
        )
        pyd_objs = [
            imdb_pyd.NameBasics.model_validate(r) for r in results
        ]  # convert to pydantic objects
        actual = [dict(pyd) for pyd in pyd_objs]  # convert to list of dictionaries
        assert actual == block
    except Exception as e:
        pytest.fail(f"Error inserting data: {e}")
    finally:
        session.rollback()


def test_read_write_title_basics(title_basics_data, session):
    block = title_basics_data
    # First validate the data
    pyd_block = [imdb_pyd.TitleBasics(**r) for r in block]
    # Turn into ORM objects
    orm_block = [r.to_orm() for r in pyd_block]

    try:
        session.add_all(orm_block)
        results = (
            session.query(imdb_orm.TitleBasics)
            .order_by(imdb_orm.TitleBasics.tconst)
            .all()
        )
        pyd_objs = [
            imdb_pyd.TitleBasics.model_validate(r) for r in results
        ]  # convert to pydantic objects
        actual = [
            dict(pyd_obj) for pyd_obj in pyd_objs
        ]  # convert to list of dictionaries
        assert actual == block
    except Exception as e:
        pytest.fail(f"Error inserting data: {e}")
    finally:
        session.rollback()


def test_read_write_title_ratings(title_ratings_data, session):
    block = title_ratings_data
    # First validate the data
    pyd_block = [imdb_pyd.TitleRatings(**r) for r in block]
    # Turn into ORM objects
    orm_block = [r.to_orm() for r in pyd_block]

    try:
        session.add_all(orm_block)
        results = (
            session.query(imdb_orm.TitleRatings)
            .order_by(imdb_orm.TitleRatings.tconst)
            .all()
        )
        pyd_objs = [
            imdb_pyd.TitleRatings.model_validate(r) for r in results
        ]  # convert to pydantic objects
        actual = [
            dict(pyd_obj) for pyd_obj in pyd_objs
        ]  # convert to list of dictionaries
        assert actual == block
    except Exception as e:
        pytest.fail(f"Error inserting data: {e}")
    finally:
        session.rollback()


def test_read_write_title_principals(title_principals_data, session):
    block = title_principals_data
    # First validate the data
    pyd_block = [imdb_pyd.TitlePrincipals(**r) for r in block]
    # Turn into ORM objects
    orm_block = [r.to_orm() for r in pyd_block]

    try:
        session.add_all(orm_block)
        results = (
            session.query(imdb_orm.TitlePrincipals)
            .order_by(imdb_orm.TitlePrincipals.tconst)
            .all()
        )
        pyd_objs = [
            imdb_pyd.TitlePrincipals.model_validate(r) for r in results
        ]  # convert to pydantic objects
        actual = [
            dict(pyd_obj) for pyd_obj in pyd_objs
        ]  # convert to list of dictionaries
        assert actual == block
    except Exception as e:
        pytest.fail(f"Error inserting data: {e}")
    finally:
        session.rollback()


def test_read_write_title_akas(title_akas_data, session):
    block = title_akas_data
    # First validate the data
    pyd_block = [imdb_pyd.TitleAkas(**r) for r in block]
    # Turn into ORM objects
    orm_block = [r.to_orm() for r in pyd_block]

    try:
        session.add_all(orm_block)
        results = (
            session.query(imdb_orm.TitleAkas).order_by(imdb_orm.TitleAkas.titleId).all()
        )
        pyd_objs = [imdb_pyd.TitleAkas.model_validate(r) for r in results]
        actual = [dict(pyd_obj) for pyd_obj in pyd_objs]
        assert actual == block
    except Exception as e:
        pytest.fail(f"Error inserting data: {e}")
    finally:
        session.rollback()


def test_read_write_title_crew(title_crew_data, session):
    block = title_crew_data
    # First validate the data
    pyd_block = [imdb_pyd.TitleCrew(**r) for r in block]
    # Turn into ORM objects
    orm_block = [r.to_orm() for r in pyd_block]

    try:
        session.add_all(orm_block)
        results = (
            session.query(imdb_orm.TitleCrew).order_by(imdb_orm.TitleCrew.tconst).all()
        )
        pyd_objs = [imdb_pyd.TitleCrew.model_validate(r) for r in results]
        actual = [dict(pyd_obj) for pyd_obj in pyd_objs]
        assert actual == block
    except Exception as e:
        pytest.fail(f"Error inserting data: {e}")
    finally:
        session.rollback()


def test_read_write_title_episode(title_episode_data, session):
    block = title_episode_data
    # First validate the data
    pyd_block = [imdb_pyd.TitleEpisode(**r) for r in block]
    # Turn into ORM objects
    orm_block = [r.to_orm() for r in pyd_block]

    try:
        session.add_all(orm_block)
        results = (
            session.query(imdb_orm.TitleEpisode)
            .order_by(imdb_orm.TitleEpisode.tconst)
            .all()
        )
        pyd_objs = [imdb_pyd.TitleEpisode.model_validate(r) for r in results]
        actual = [dict(pyd_obj) for pyd_obj in pyd_objs]
        assert actual == block
    except Exception as e:
        pytest.fail(f"Error inserting data: {e}")
    finally:
        session.rollback()
