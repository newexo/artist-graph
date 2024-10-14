from typing import Any, List, Dict, Optional, Callable
from imdb.parser.s3.utils import DB_TRANSFORM, title_soundex, name_soundexes


def process_tsv_gz_line(line: bytes) -> List[str]:
    """Process a line from a .tsv.gz file (expected to be a byte string)."""
    return line.decode("utf-8").strip().split("\t")


def tsv_line_info(
    line_parts: List[str], headers: List[str]
) -> Dict[str, Optional[str]]:
    """Convert a list of line parts and headers into a dictionary, replacing '\\N' with None."""
    return dict(zip(headers, [x if x != r"\N" else None for x in line_parts]))


def get_data_transformers(table_name: str) -> Dict[str, Callable[[str], Any]]:
    data_transf = {}
    for column, conf in DB_TRANSFORM.get(table_name, {}).items():
        if "transform" in conf:
            data_transf[column] = conf["transform"]
    return data_transf


def process_line_info(
    info: Dict[str, Optional[str]],
    data_transf: Dict[str, Callable[[str], str]],
    table_name: str,
):
    for key, tranf in data_transf.items():
        if key not in info:
            continue
        info[key] = tranf(info[key])
    if table_name == "title_basics":
        info["t_soundex"] = title_soundex(info["primaryTitle"])
    elif table_name == "title_akas":
        info["t_soundex"] = title_soundex(info["title"])
    elif table_name == "name_basics":
        info["ns_soundex"], info["sn_soundex"], info["s_soundex"] = name_soundexes(
            info["primaryName"]
        )


def line2info(
    line: bytes,
    headers: List[str],
    table_name: str,
    data_transf: Dict[str, Callable[[str], Any]] = None,
) -> Dict[str, Optional[str]]:
    if data_transf is None:
        data_transf = get_data_transformers(table_name)
    parts = process_tsv_gz_line(line)
    info = tsv_line_info(parts, headers)
    process_line_info(info, data_transf, table_name)
    return info
