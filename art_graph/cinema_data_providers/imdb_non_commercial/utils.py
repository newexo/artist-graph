from typing import Any, List, Dict, Optional

from .constants import TSV_EXT


def table_name_from_file(fn: str) -> str:
    return fn.replace(TSV_EXT, "").replace(".", "_")


def process_tsv_gz_line(line: bytes) -> List[str]:
    """Process a line from a .tsv.gz file (expected to be a byte string)."""
    return line.decode("utf-8").strip().split("\t")


def tsv_line_info(
    line_parts: List[str], headers: List[str]
) -> Dict[str, Optional[str]]:
    """Convert a list of line parts and headers into a dictionary, replacing '\\N' with None."""
    return dict(zip(headers, [x if x != r"\N" else None for x in line_parts]))


def line2info(
    line: bytes,
    headers: List[str],
) -> Dict[str, Optional[str]]:
    parts = process_tsv_gz_line(line)
    info = tsv_line_info(parts, headers)
    return info
