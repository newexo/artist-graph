import os
import gzip
import argparse
import logging
import traceback
import sqlalchemy
from sqlalchemy import exc

from art_graph import directories
from art_graph.cinema_data_providers.imdb_non_commercial.constants import (
    BLOCK_SIZE,
)
from art_graph.cinema_data_providers.imdb_non_commercial import (
    locations,
    table_builder,
    utils,
)

# how many blocks to write before logging
LOG_BLOCK_SIZE = 10

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


def main(db_name):
    engine = locations.get_sqlite_engine(db_name)
    metadata.bind = engine
    fns = [directories.data(fn) for fn in locations.imdb_files]
    for fn in fns:
        if not os.path.isfile(fn):
            logging.debug(f"skipping file {fn}")
            continue
        import_file(fn, engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and import IMDb data with optional debug logging.")

    # Add a command-line option for setting the logging level to DEBUG
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging."
    )

    # Add a command-line option for specifying the database name
    parser.add_argument(
        "--db-name",
        type=str,
        default="IM01.db",  # Default value
        help="Specify the SQLite database name (default: IM01.db)."
    )

    args = parser.parse_args()

    # Configure logging
    if args.debug:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    main(args.db_name)
