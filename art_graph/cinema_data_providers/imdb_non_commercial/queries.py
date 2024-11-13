import networkx as nx

from art_graph.cinema_data_providers.imdb_non_commercial import (
    imdb_non_commercial_orm_models as imdb_orm,
)

from art_graph.cinegraph.node_types import PersonNode, WorkNode


def compute_graph(query) -> nx.Graph:
    g = nx.Graph()
    results = query.yield_per(100)
    for title_principal in results:
        p = PersonNode(title_principal.nconst)
        w = WorkNode(title_principal.tconst)
        g.add_node(p)
        g.add_node(w)
        g.add_edge(p, w)
    return g


def full_graph_query(session):
    return (
        session.query(imdb_orm.TitlePrincipals)
        .join(
            imdb_orm.TitleBasics,
            imdb_orm.TitleBasics.tconst == imdb_orm.TitlePrincipals.tconst,
        )
        .filter(
            imdb_orm.TitleBasics.titleType == "movie",
            imdb_orm.TitleBasics.isAdult == False,
            imdb_orm.TitlePrincipals.category.in_(["actor", "actress"]),
        )
    )


def curated_graph_query(session, primary_names, original_titles):
    return (
        session.query(imdb_orm.TitlePrincipals)
        .join(
            imdb_orm.NameBasics,
            imdb_orm.NameBasics.nconst == imdb_orm.TitlePrincipals.nconst,
        )
        .join(
            imdb_orm.TitleBasics,
            imdb_orm.TitleBasics.tconst == imdb_orm.TitlePrincipals.tconst,
        )
        .filter(
            imdb_orm.TitleBasics.titleType == "movie",
            imdb_orm.TitleBasics.isAdult == False,
            imdb_orm.NameBasics.primaryName.in_(primary_names),
            imdb_orm.TitleBasics.originalTitle.in_(original_titles),
            imdb_orm.TitlePrincipals.category.in_(["actor", "actress"]),
        )
    )


def famous_query(session):
    return (
        session.query(imdb_orm.TitlePrincipals)
        .join(
            imdb_orm.TitleRatings,
            imdb_orm.TitleBasics.tconst == imdb_orm.TitleRatings.tconst,
        )
        .join(
            imdb_orm.TitleBasics,
            imdb_orm.TitleBasics.tconst == imdb_orm.TitlePrincipals.tconst,
        )
        .filter(
            imdb_orm.TitleBasics.titleType == "movie",
            imdb_orm.TitleBasics.isAdult == False,
            imdb_orm.TitleRatings.averageRating >= 6.0,
            imdb_orm.TitleRatings.numVotes >= 10000,
            imdb_orm.TitlePrincipals.category.in_(["actor", "actress"]),
            imdb_orm.TitlePrincipals.ordering.in_([1, 2]),
        )
    )
