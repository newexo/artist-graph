import os
import gzip
import logging
import traceback
import sqlalchemy
from sqlalchemy import exc

from art_graph import directories
from art_graph.cinema_data_providers.imbd_non_commercial.constants import (
    BLOCK_SIZE,
)
from art_graph.cinema_data_providers.imbd_non_commercial import (
    locations,
    table_builder,
    utils,
)

# how many blocks to write before logging
LOG_BLOCK_SIZE = 10

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
metadata = sqlalchemy.MetaData()


def fetch_block(fd, headers, table):
    block = []
    transformers = utils.get_data_transformers(table.name)
    for line in fd:
        info = utils.line2info(line, headers, table.name, transformers)
        block.append(info)
        if len(block) >= BLOCK_SIZE:
            yield block
            block = []
    if block:
        yield block


def import_file(fn, engine):
    logging.info(f"begin processing file {fn}")
    connection = engine.connect()
    try:
        count = 0
        fn_basename = os.path.basename(fn)
        with gzip.GzipFile(fn, "rb") as gz_file:
            line = gz_file.readline()
            headers = utils.process_tsv_gz_line(line)
            builder = table_builder.TableBuilder(fn_basename, headers)
            logging.debug(f"headers of file {fn}: {','.join(headers)}")
            table = builder.build_table()
            try:
                table.drop(bind=engine)
                logging.debug(f"table {table.name} dropped")
            except exc.SQLAlchemyError as e:
                logging.debug(f"table {table.name} not dropped: {e}")
            insert = table.insert()
            metadata.create_all(bind=engine, tables=[table])
            try:
                for block in fetch_block(gz_file, headers, table):
                    logging.debug("Starting transaction")
                    with connection.begin() as transaction:
                        try:
                            connection.execute(insert, block)
                            logging.debug("Committing transaction")
                        except Exception as e:
                            logging.error(
                                f"error processing data: {len(block)} entries lost: {e}"
                            )
                            logging.error(f"Exception: {e}")
                            logging.error(traceback.format_exc())
                            logging.debug("Rolling back transaction")
                            transaction.rollback()
                            continue
                    count += len(block)
                    if count % (BLOCK_SIZE * LOG_BLOCK_SIZE) == 0:
                        logging.info(f"processed file {fn}: {count} entries")
                    # if count >= 3 * BLOCK_SIZE:
                    #     break
            except exc.SQLAlchemyError as e:
                logging.error(f"error processing data on table {table.name}: {e}")
            logging.info(f"processed file {fn}: {count} entries")

    finally:
        connection.close()


def main():
    engine = locations.get_sqlite_engine("IM01.db")
    metadata.bind = engine
    fns = [directories.data(fn) for fn in locations.imdb_files]
    for fn in fns:
        if not os.path.isfile(fn):
            logging.debug(f"skipping file {fn}")
            continue
        import_file(fn, engine)


if __name__ == "__main__":
    main()
