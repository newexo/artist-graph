from dataclasses import dataclass
from typing import List
import sqlalchemy

from art_graph.cinema_data_providers.imdb_non_commercial.constants import TSV_EXT

from imdb.parser.s3.utils import DB_TRANSFORM


@dataclass
class TableBuilder:
    fn: str
    headers: List[str]

    @property
    def table_name(self) -> str:
        """Generate the table name by removing the extension and replacing dots."""
        return self.fn.replace(TSV_EXT, "").replace(".", "_")

    @property
    def table_map(self) -> dict:
        """Fetch column transformation rules from DB_TRANSFORM for the table."""
        return DB_TRANSFORM.get(self.table_name, {})

    def col_args(self, header: str) -> dict:
        """Generate column arguments for a header."""
        col_info = self.table_map.get(header) or {}
        col_type = col_info.get("type") or sqlalchemy.UnicodeText
        if "length" in col_info and col_type is sqlalchemy.String:
            col_type = sqlalchemy.String(length=col_info["length"])
        col_args = {
            "name": header,
            "type_": col_type,
            "index": col_info.get("index", False),
        }
        return col_args

    def col_obj(self, header: str) -> sqlalchemy.Column:
        """Create a column object for a header."""
        col_args = self.col_args(header)
        return sqlalchemy.Column(**col_args)

    def build_table(self, metadata: sqlalchemy.MetaData) -> sqlalchemy.Table:
        columns = [self.col_obj(header) for header in self.headers]
        return sqlalchemy.Table(self.table_name, metadata, *columns)
