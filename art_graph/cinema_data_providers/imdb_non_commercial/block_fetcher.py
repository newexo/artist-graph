from sqlalchemy.orm import Session

from art_graph.cinema_data_providers.imdb_non_commercial import (
    imdb_non_commercial_pydantic_models as imdb_pyd,
    utils,
    key_validator,
)
from art_graph.cinema_data_providers.imdb_non_commercial.line_infos import LineInfos
from logging import Logger


class BlockProcessor:
    def clean(self, block):
        return block


class BlockValidator(BlockProcessor):
    table_name: str
    session: Session
    logger: Logger

    def __init__(self, table_name: str, session: Session, logger: Logger):
        self.table_name = table_name
        self.session = session
        self.logger = logger


class BlockValidatorWithTitles(BlockValidator):
    def filter_missing_tconsts(self, block, session):
        tconsts = [r.tconst for r in block]
        missing_tconsts = key_validator.missing_tconst(tconsts, session)
        self.logger.debug(f"missing tconsts from {self.table_name}: {missing_tconsts}")
        return [r for r in block if r.tconst not in missing_tconsts]

    def clean(self, block):
        return self.filter_missing_tconsts(block, self.session)


class BlockValidatorTitlePrincipals(BlockValidatorWithTitles):
    def filter_missing_nconsts(self, block, session):
        nconsts = [r.nconst for r in block]
        missing_nconsts = key_validator.missing_nconst(nconsts, session)
        for nconst in missing_nconsts:
            self.logger.debug(f"missing nconst from {self.table_name}: {nconst}")
        return [r for r in block if r.nconst not in missing_nconsts]

    def clean(self, block):
        block = self.filter_missing_tconsts(block, self.session)
        return self.filter_missing_nconsts(block, self.session)


class BlockValidatorTitleAkas(BlockValidator):
    def filter_missing_title_id(self, block, session):
        tconsts = [r.titleId for r in block]
        missing_tconsts = key_validator.missing_tconst(tconsts, session)
        self.logger.debug(f"missing tconsts from {self.table_name}: {missing_tconsts}")
        return [r for r in block if r.titleId not in missing_tconsts]

    def clean(self, block):
        return self.filter_missing_title_id(block, self.session)


class BlockFetcher:
    table_name: str
    headers: list[str]
    infos: LineInfos
    block_size: int
    session: Session
    block_processor: BlockProcessor

    def __init__(
        self,
        table_name: str,
        headers: list[str],
        infos: LineInfos,
        session,
        block_size: int,
        logger: Logger,
        block_processor: BlockProcessor,
    ):
        self.table_name = table_name
        self.headers = headers
        self.infos = infos
        self.session = session
        self.block_size = block_size
        self.logger = logger
        self.block_processor = block_processor

    def clean_block(self, block):
        processed_count = len(block)
        block = self.block_processor.clean(block)
        return processed_count, block

    def fetch_block(self, fd):
        pyd_cls = imdb_pyd.NAME2PYD[self.table_name]
        block = []
        for line in fd:
            info = utils.line2info(line, self.headers)
            pyd = pyd_cls(**info)
            orm = pyd.to_orm()
            block.append(orm)
            if len(block) >= self.block_size:
                yield self.clean_block(block)
                block = []
        if block:
            yield self.clean_block(block)


def get_block_fetcher(
    table_name, headers, session: Session, infos: LineInfos, block_size, logger: Logger, filter_missing_keys: bool
) -> BlockFetcher:
    if not filter_missing_keys or table_name == "title_basics" or table_name == "name_basics":
        processor = BlockProcessor()
    elif table_name == "title_principals":
        processor = BlockValidatorTitlePrincipals(table_name, session, logger)
    elif table_name == "title_akas":
        processor = BlockValidatorTitleAkas(table_name, session, logger)
    else:
        processor = BlockValidatorWithTitles(table_name, session, logger)
    return BlockFetcher(
        table_name,
        headers,
        infos,
        session,
        block_size=block_size,
        logger=logger,
        block_processor=processor,
    )
