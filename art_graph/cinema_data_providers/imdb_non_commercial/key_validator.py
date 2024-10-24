from sqlalchemy.orm import Session

from . import imdb_non_commercial_orm_models as imdb_orm


def missing_nconst(nconsts, session: Session):
    block = [imdb_orm.NConstTemp(nconst=nconst) for nconst in nconsts]
    session.add_all(block)
    missing_nconst_query = (
        session.query(imdb_orm.NConstTemp.nconst)
        .outerjoin(
            imdb_orm.NameBasics,
            imdb_orm.NConstTemp.nconst == imdb_orm.NameBasics.nconst,
        )
        .filter(imdb_orm.NameBasics.nconst.is_(None))
    )
    results = missing_nconst_query.all()
    session.query(imdb_orm.NConstTemp).delete()
    return {r.nconst for r in results}


def missing_tconst(tconsts, session: Session):
    block = [imdb_orm.TConstTemp(tconst=tconst) for tconst in tconsts]
    session.add_all(block)
    missing_tconst_query = (
        session.query(imdb_orm.TConstTemp.tconst)
        .outerjoin(
            imdb_orm.TitleBasics,
            imdb_orm.TConstTemp.tconst == imdb_orm.TitleBasics.tconst,
        )
        .filter(imdb_orm.TitleBasics.tconst.is_(None))
    )
    results = missing_tconst_query.all()
    session.query(imdb_orm.TConstTemp).delete()
    return {r.tconst for r in results}
