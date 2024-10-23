from sqlalchemy.orm import Session

from art_graph.cinema_data_providers.imdb_non_commercial import (
    imdb_non_commercial_pydantic_models as imdb_pyd,
    utils,
    key_validator,
)
from art_graph.cinema_data_providers.imdb_non_commercial.line_infos import LineInfos
from logging import Logger


class BlockFetcher:
    table_name: str
    headers: list[str]
    infos: LineInfos
    block_size: int
    session: Session

    def __init__(
        self,
        table_name: str,
        headers: list[str],
        infos: LineInfos,
        session,
        block_size: int,
        logger: Logger,
    ):
        self.table_name = table_name
        self.headers = headers
        self.infos = infos
        self.session = session
        self.block_size = block_size
        self.logger = logger

    def clean_block(self, block):
        return block

    def fetch_block(self, fd):
        pyd_cls = imdb_pyd.NAME2PYD[self.table_name]
        block = []
        for line in fd:
            info = utils.line2info(line, self.headers)
            pyd = pyd_cls(**info)
            orm = pyd.to_orm()
            block.append(orm)
            if len(block) >= self.block_size:
                self.logger.debug(f"block size: {len(block)}")
                block = self.clean_block(block)
                if block:
                    self.logger.debug(f"yielding block: {len(block)}")
                else:
                    self.logger.debug("block is empty")
                yield block
                block = []
        self.logger.debug(f"almost done: {len(block)}")
        block = self.clean_block(block)
        if block:
            yield block


class BlockFetcherTitleAkas(BlockFetcher):
    session: Session

    def filter_missing_title_id(self, block, session):
        tconsts = [r.titleId for r in block]
        missing_tconsts = key_validator.missing_tconst(tconsts, session)
        self.logger.debug(f"missing tconsts from {self.table_name}: {missing_tconsts}")
        return [r for r in block if r.titleId not in missing_tconsts]

    def clean_block(self, block):
        return self.filter_missing_title_id(block, self.session)


class BlockFetcherWithTitles(BlockFetcher):
    session: Session

    def filter_missing_tconsts(self, block, session):
        tconsts = [r.tconst for r in block]
        missing_tconsts = key_validator.missing_tconst(tconsts, session)
        self.logger.debug(f"missing tconsts from {self.table_name}: {missing_tconsts}")
        return [r for r in block if r.tconst not in missing_tconsts]

    def clean_block(self, block):
        return self.filter_missing_tconsts(block, self.session)


class BlockFetcherTitlePrincipals(BlockFetcherWithTitles):
    def filter_missing_nconsts(self, block, session):
        nconsts = [r.nconst for r in block]
        missing_nconsts = key_validator.missing_nconst(nconsts, session)
        for nconst in missing_nconsts:
            self.logger.debug(f"missing nconst from {self.table_name}: {nconst}")
        return [r for r in block if r.nconst not in missing_nconsts]

    def clean_block(self, block):
        block = self.filter_missing_tconsts(block, self.session)
        return self.filter_missing_nconsts(block, self.session)


def get_block_fetcher(
    table_name, headers, session: Session, infos: LineInfos, block_size, logger: Logger
) -> BlockFetcher:
    if table_name == "title_basics" or table_name == "name_basics":
        cls = BlockFetcher
    elif table_name == "title_principals":
        cls = BlockFetcherTitlePrincipals
    elif table_name == "title_akas":
        cls = BlockFetcherTitleAkas
    else:
        cls = BlockFetcherWithTitles
    return cls(
        table_name, headers, infos, session, block_size=block_size, logger=logger
    )
