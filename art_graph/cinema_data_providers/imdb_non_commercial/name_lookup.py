from . import imdb_non_commercial_orm_models as imdb_orm


from art_graph.cinegraph.node_types import ProfessionalNode


class NameNotFound(Exception):
    pass


class TitleNotFound(Exception):
    pass


def name_lookup(session, nconst):
    query = session.query(imdb_orm.NameBasics).filter(
        imdb_orm.NameBasics.nconst == nconst
    )
    results = query.all()
    if len(results) == 0:
        raise NameNotFound(f"Name with nconst {nconst} not found")
    result: imdb_orm.NameBasics = results[0]
    return result.primaryName


def title_lookup(session, tconst):
    query = session.query(imdb_orm.TitleBasics).filter(
        imdb_orm.TitleBasics.tconst == tconst
    )
    results = query.all()
    if len(results) == 0:
        raise TitleNotFound(f"Title with tconst {tconst} not found")
    result: imdb_orm.TitleBasics = results[0]
    return result.originalTitle


def node_lookup(session, node: ProfessionalNode):
    if node.is_person:
        return name_lookup(session, node.id)
    else:
        return title_lookup(session, node.id)
