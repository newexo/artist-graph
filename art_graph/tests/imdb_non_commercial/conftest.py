import pytest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from art_graph.cinema_data_providers.imdb_non_commercial import table_builder


@pytest.fixture
def engine():
    """Fixture to create a SQLAlchemy engine."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="function")
def session(engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        yield session


@pytest.fixture
def metadata():
    return sqlalchemy.MetaData()


@pytest.fixture
def table_builder_title_principals():
    """Fixture to create a TableBuilder for the 'title.principals.tsv.gz' file."""
    fn = "title.principals.tsv.gz"
    headers = ["tconst", "ordering", "nconst", "category", "job", "characters"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


@pytest.fixture
def table_title_principals(engine, metadata, table_builder_title_principals):
    table = table_builder_title_principals.build_table(metadata)
    metadata.create_all(bind=engine, tables=[table])
    return table


@pytest.fixture
def table_builder_name_basics():
    """Fixture to create a TableBuilder for the 'name.basics.tsv.gz' file."""
    fn = "name.basics.tsv.gz"
    headers = [
        "nconst",
        "primaryName",
        "birthYear",
        "deathYear",
        "primaryProfession",
        "knownForTitles",
    ]
    return table_builder.TableBuilder(fn=fn, headers=headers)


@pytest.fixture
def table_name_basics(engine, metadata, table_builder_name_basics):
    table = table_builder_name_basics.build_table(metadata)
    metadata.create_all(bind=engine, tables=[table])
    return table


@pytest.fixture
def table_builder_title_basics():
    """Fixture to create a TableBuilder for the 'title.basics.tsv.gz' file."""
    fn = "title.basics.tsv.gz"
    headers = [
        "tconst",
        "titleType",
        "primaryTitle",
        "originalTitle",
        "isAdult",
        "startYear",
        "endYear",
        "runtimeMinutes",
        "genres",
    ]
    return table_builder.TableBuilder(fn=fn, headers=headers)


@pytest.fixture
def table_title_basics(engine, metadata, table_builder_title_basics):
    table = table_builder_title_basics.build_table(metadata)
    metadata.create_all(bind=engine, tables=[table])
    return table


@pytest.fixture
def table_builder_title_ratings():
    """Fixture to create a TableBuilder for the 'title.ratings.tsv.gz' file."""
    fn = "title.ratings.tsv.gz"
    headers = ["tconst", "averageRating", "numVotes"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


@pytest.fixture
def table_title_ratings(engine, metadata, table_builder_title_ratings):
    table = table_builder_title_ratings.build_table(metadata)
    metadata.create_all(bind=engine, tables=[table])
    return table


@pytest.fixture
def table_builder_title_akas():
    """Fixture to create a TableBuilder for the 'title.akas.tsv.gz' file."""
    fn = "title.akas.tsv.gz"
    headers = [
        "titleId",
        "ordering",
        "title",
        "region",
        "language",
        "types",
        "attributes",
        "isOriginalTitle",
    ]
    return table_builder.TableBuilder(fn=fn, headers=headers)


@pytest.fixture
def table_title_akas(engine, metadata, table_builder_title_akas):
    table = table_builder_title_akas.build_table(metadata)
    metadata.create_all(bind=engine, tables=[table])
    return table


@pytest.fixture
def table_builder_title_crew():
    """Fixture to create a TableBuilder for the 'title.crew.tsv.gz' file."""
    fn = "title.crew.tsv.gz"
    headers = ["tconst", "directors", "writers"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


@pytest.fixture
def table_title_crew(engine, metadata, table_builder_title_crew):
    table = table_builder_title_crew.build_table(metadata)
    metadata.create_all(bind=engine, tables=[table])
    return table


@pytest.fixture
def table_builder_title_episode():
    """Fixture to create a TableBuilder for the 'title.episode.tsv.gz' file."""
    fn = "title.episode.tsv.gz"
    headers = ["tconst", "parentTconst", "seasonNumber", "episodeNumber"]
    return table_builder.TableBuilder(fn=fn, headers=headers)


@pytest.fixture
def table_title_episode(engine, metadata, table_builder_title_episode):
    table = table_builder_title_episode.build_table(metadata)
    metadata.create_all(bind=engine, tables=[table])
    return table


@pytest.fixture
def name_basics_data():
    return [
        {
            "nconst": 1001,
            "knownForTitles": "0000001,0000002",
            "primaryName": "John Doe",
            "primaryProfession": "actor,producer",
            "deathYear": 1990,
            "birthYear": 1940,
        },
        {
            "nconst": 1002,
            "knownForTitles": "0000003,0000004",
            "primaryName": "Jane Smith",
            "primaryProfession": "director",
            "deathYear": None,
            "birthYear": 1980,
        },
        {
            "nconst": 1003,
            "knownForTitles": "0000005",
            "primaryName": "Alice Johnson",
            "primaryProfession": "writer",
            "deathYear": None,
            "birthYear": 1975,
        },
        {
            "nconst": 1004,
            "knownForTitles": "0000006",
            "primaryName": "Bob Brown",
            "primaryProfession": "actor",
            "deathYear": None,
            "birthYear": 1965,
        },
        {
            "nconst": 1005,
            "knownForTitles": "0000007,0000008",
            "primaryName": "Charlie Davis",
            "primaryProfession": "producer",
            "deathYear": 2020,
            "birthYear": 1950,
        },
    ]


@pytest.fixture
def title_akas_data():
    return [
        {
            "titleId": 2001,
            "ordering": 1,
            "attributes": None,
            "types": "alternative",
            "title": "Alt Title One",
            "isOriginalTitle": True,
            "language": "en",
            "region": "US",
        },
        {
            "titleId": 2002,
            "ordering": 1,
            "attributes": None,
            "types": "dvd",
            "title": "Alt Title Two",
            "isOriginalTitle": False,
            "language": "fr",
            "region": "FR",
        },
        {
            "titleId": 2003,
            "ordering": 1,
            "attributes": "festival",
            "types": "festival",
            "title": "Alt Title Three",
            "isOriginalTitle": True,
            "language": "en",
            "region": "UK",
        },
        {
            "titleId": 2004,
            "ordering": 1,
            "attributes": "imdbDisplay",
            "types": "tv",
            "title": "Alt Title Four",
            "isOriginalTitle": False,
            "language": "es",
            "region": "ES",
        },
        {
            "titleId": 2005,
            "ordering": 1,
            "attributes": None,
            "types": "video",
            "title": "Alt Title Five",
            "isOriginalTitle": True,
            "language": "en",
            "region": "US",
        },
    ]


@pytest.fixture
def title_basics_data():
    return [
        {
            "tconst": 3001,
            "primaryTitle": "Movie One",
            "originalTitle": "Original Movie One",
            "titleType": "movie",
            "isAdult": False,
            "startYear": 1999,
            "endYear": None,
            "runtimeMinutes": 120,
            "genres": "Drama",
        },
        {
            "tconst": 3002,
            "primaryTitle": "Movie Two",
            "originalTitle": "Original Movie Two",
            "titleType": "movie",
            "isAdult": True,
            "startYear": 2005,
            "endYear": None,
            "runtimeMinutes": 95,
            "genres": "Action",
        },
        {
            "tconst": 3003,
            "primaryTitle": "TV Show One",
            "originalTitle": "Original TV Show One",
            "titleType": "tv series",
            "isAdult": False,
            "startYear": 2010,
            "endYear": 2015,
            "runtimeMinutes": 45,
            "genres": "Comedy",
        },
        {
            "tconst": 3004,
            "primaryTitle": "TV Show Two",
            "originalTitle": "Original TV Show Two",
            "titleType": "tv series",
            "isAdult": False,
            "startYear": 2018,
            "endYear": None,
            "runtimeMinutes": 30,
            "genres": "Documentary",
        },
        {
            "tconst": 3005,
            "primaryTitle": "Documentary One",
            "originalTitle": "Original Documentary One",
            "titleType": "documentary",
            "isAdult": False,
            "startYear": 2021,
            "endYear": None,
            "runtimeMinutes": 90,
            "genres": "Documentary",
        },
    ]


@pytest.fixture
def title_crew_data():
    return [
        {"tconst": 4001, "writers": "1001,1002", "directors": "1003"},
        {"tconst": 4002, "writers": "1004", "directors": "1005"},
        {"tconst": 4003, "writers": "1006,1007", "directors": "1008,1009"},
        {"tconst": 4004, "writers": "1010", "directors": "1011"},
        {"tconst": 4005, "writers": "1012", "directors": "1013,1014"},
    ]


@pytest.fixture
def title_episode_data():
    return [
        {"tconst": 5001, "parentTconst": 3003, "seasonNumber": 1, "episodeNumber": 1},
        {"tconst": 5002, "parentTconst": 3003, "seasonNumber": 1, "episodeNumber": 2},
        {"tconst": 5003, "parentTconst": 3004, "seasonNumber": 1, "episodeNumber": 1},
        {"tconst": 5004, "parentTconst": 3004, "seasonNumber": 1, "episodeNumber": 2},
        {"tconst": 5005, "parentTconst": 3004, "seasonNumber": 2, "episodeNumber": 1},
    ]


@pytest.fixture
def title_principals_data():
    return [
        {
            "tconst": 6001,
            "nconst": 1001,
            "ordering": 1,
            "job": "actor",
            "category": "actor",
            "characters": "Character One",
        },
        {
            "tconst": 6002,
            "nconst": 1002,
            "ordering": 1,
            "job": "director",
            "category": "director",
            "characters": None,
        },
        {
            "tconst": 6003,
            "nconst": 1003,
            "ordering": 1,
            "job": "producer",
            "category": "producer",
            "characters": None,
        },
        {
            "tconst": 6004,
            "nconst": 1004,
            "ordering": 1,
            "job": "writer",
            "category": "writer",
            "characters": None,
        },
        {
            "tconst": 6005,
            "nconst": 1005,
            "ordering": 1,
            "job": "cinematographer",
            "category": "cinematographer",
            "characters": None,
        },
    ]


@pytest.fixture
def title_ratings_data():
    return [
        {"tconst": 7001, "averageRating": 8.5, "numVotes": 1500},
        {"tconst": 7002, "averageRating": 7.2, "numVotes": 3000},
        {"tconst": 7003, "averageRating": 6.9, "numVotes": 2000},
        {"tconst": 7004, "averageRating": 9.1, "numVotes": 5000},
        {"tconst": 7005, "averageRating": 5.4, "numVotes": 800},
    ]
