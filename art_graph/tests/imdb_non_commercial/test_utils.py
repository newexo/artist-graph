import pytest
from typing import List

from ...cinema_data_providers.imdb_non_commercial import utils


@pytest.fixture
def title_principals_line() -> bytes:
    return b'tt0000001\t1\tnm1588970\tself\t\\N\t["Self"]\n'


@pytest.fixture
def title_principals_headers() -> List[str]:
    return ["tconst", "ordering", "nconst", "category", "job", "characters"]


@pytest.fixture
def title_principals_line_parts() -> List[str]:
    return ["tt0000001", "1", "nm1588970", "self", "\\N", '["Self"]']


@pytest.fixture
def title_principals_line_raw_info() -> dict:
    return {
        "tconst": "tt0000001",
        "ordering": "1",
        "nconst": "nm1588970",
        "category": "self",
        "job": None,
        "characters": '["Self"]',
    }


def test_process_tsv_gz_line(title_principals_line, title_principals_line_parts):
    # header of title principals
    line = b"tconst\tordering\tnconst\tcategory\tjob\tcharacters\n"
    expected = ["tconst", "ordering", "nconst", "category", "job", "characters"]
    actual = utils.process_tsv_gz_line(line)
    assert actual == expected

    # a typical line from title principals
    expected = title_principals_line_parts
    actual = utils.process_tsv_gz_line(title_principals_line)
    assert actual == expected


def test_tsv_gz_line_info(
    title_principals_line_parts,
    title_principals_headers,
    title_principals_line_raw_info,
):
    expected = title_principals_line_raw_info
    actual = utils.tsv_line_info(title_principals_line_parts, title_principals_headers)
    assert actual == expected


def test_process_line_info(title_principals_line_raw_info):
    info = title_principals_line_raw_info
    table_name = "title_principals"
    data_transf = utils.get_data_transformers(table_name)
    utils.process_line_info(info, data_transf, table_name)
    expected = {
        "tconst": 1,
        "ordering": 1,
        "nconst": 1588970,
        "category": "self",
        "job": None,
        "characters": None,
    }
    actual = info
    assert actual == expected


def test_name_basics():
    table_name = "name_basics"
    header_line = b"nconst\tprimaryName\tbirthYear\tdeathYear\tprimaryProfession\tknownForTitles\n"
    expected = [
        "nconst",
        "primaryName",
        "birthYear",
        "deathYear",
        "primaryProfession",
        "knownForTitles",
    ]
    headers = utils.process_tsv_gz_line(header_line)
    assert headers == expected

    line = b"nm0000001\tFred Astaire\t1899\t1987\tactor,miscellaneous,producer\ttt0072308,tt0050419,tt0053137,tt0027125\n"
    actual = utils.line2info(line, headers, table_name)
    expected = {
        "nconst": 1,
        "primaryName": "Fred Astaire",
        "birthYear": 1899,
        "deathYear": 1987,
        "primaryProfession": "actor,miscellaneous,producer",
        "knownForTitles": "0072308,0050419,0053137,0027125",
    }
    assert actual == expected


def test_title_akas():
    table_name = "title_akas"
    header_line = b"titleId\tordering\ttitle\tregion\tlanguage\ttypes\tattributes\tisOriginalTitle\n"
    expected = [
        "titleId",
        "ordering",
        "title",
        "region",
        "language",
        "types",
        "attributes",
        "isOriginalTitle",
    ]
    headers = utils.process_tsv_gz_line(header_line)
    assert headers == expected

    line = b"tt0000001\t1\tCarmencita\t\\N\t\\N\toriginal\t\\N\t1\n"
    actual = utils.line2info(line, headers, table_name)
    expected = {
        "titleId": 1,
        "ordering": 1,
        "title": "Carmencita",
        "region": None,
        "language": None,
        "types": "original",
        "attributes": None,
        "isOriginalTitle": True
    }
    assert actual == expected

    line = b"tt0000001\t2\tCarmencita\tDE\t\\N\t\\N\tliteral title\t0\n"
    actual = utils.line2info(line, headers, table_name)
    expected = {
        "titleId": 1,
        "ordering": 2,
        "title": "Carmencita",
        "region": "DE",
        "language": None,
        "types": None,
        "attributes": "literal title",
        "isOriginalTitle": False
    }
    assert actual == expected


def test_title_basics():
    table_name = "title_basics"
    header_line = b"tconst\ttitleType\tprimaryTitle\toriginalTitle\tisAdult\tstartYear\tendYear\truntimeMinutes\tgenres\n"
    expected = [
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
    headers = utils.process_tsv_gz_line(header_line)
    assert headers == expected

    line = b"tt0000001\tshort\tCarmencita\tCarmencita\t0\t1894\t\\N\t1\tDocumentary,Short\n"
    actual = utils.line2info(line, headers, table_name)
    expected = {
        "tconst": 1,
        "titleType": "short",
        "primaryTitle": "Carmencita",
        "originalTitle": "Carmencita",
        "isAdult": False,
        "startYear": 1894,
        "endYear": None,
        "runtimeMinutes": 1,
        "genres": "Documentary,Short"
    }
    assert actual == expected


def test_title_crew():
    table_name = "title_crew"
    header_line = b"tconst\tdirectors\twriters\n"
    expected = ["tconst", "directors", "writers"]
    headers = utils.process_tsv_gz_line(header_line)
    assert headers == expected

    line = b"tt0000001\tnm0005690\t\\N\n"
    actual = utils.line2info(line, headers, table_name)
    expected = {"tconst": 1, "directors": "0005690", "writers": None}
    assert actual == expected


def test_title_episode():
    table_name = "title_episode"
    header_name = b"tconst\tparentTconst\tseasonNumber\tepisodeNumber\n"
    expected = ["tconst", "parentTconst", "seasonNumber", "episodeNumber"]
    headers = utils.process_tsv_gz_line(header_name)
    assert headers == expected

    line = b"tt0041951\ttt0041038\t1\t9\n"
    actual = utils.line2info(line, headers, table_name)
    expected = {
        "tconst": 41951,
        "parentTconst": 41038,
        "seasonNumber": 1,
        "episodeNumber": 9,
    }
    assert actual == expected


def test_title_ratings():
    table_name = "title_ratings"
    header_line = b"tconst\taverageRating\tnumVotes\n"
    expected = ["tconst", "averageRating", "numVotes"]
    headers = utils.process_tsv_gz_line(header_line)
    assert headers == expected

    line = b"tt0000001\t5.7\t2089\n"
    actual = utils.line2info(line, headers, table_name)
    expected = {"tconst": 1, "averageRating": 5.7, "numVotes": 2089}
    assert actual == expected
