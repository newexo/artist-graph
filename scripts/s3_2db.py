import os
import gzip
import argparse
import time
import logging
import traceback
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.orm import Session


from art_graph import directories
from art_graph.cinema_data_providers.imdb_non_commercial import (
    locations,
    utils,
    imdb_non_commercial_orm_models as imdb_orm,
)
from art_graph.cinema_data_providers.imdb_non_commercial.block_fetcher import (
    get_block_fetcher,
)
from art_graph.cinema_data_providers.imdb_non_commercial.line_infos import LineInfos

# how many blocks to write before logging
BLOCK_SIZE = 10000
LOG_BLOCK_SIZE = 10

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def import_file(fn, engine):
    logging.info(f"begin processing file {fn}")

    processed_count = 0
    inserted_count = 0
    fn_basename = os.path.basename(fn)
    with gzip.GzipFile(fn, "rb") as gz_file, Session(bind=engine) as session:
        line = gz_file.readline()
        headers = utils.process_tsv_gz_line(line)
        table_name = utils.table_name_from_file(fn_basename)
        infos = LineInfos(gz_file, headers)
        fetcher = get_block_fetcher(
            table_name, headers, session, infos, BLOCK_SIZE, logger
        )
        logging.debug(f"headers of file {fn}: {','.join(headers)}")
        try:
            for block in fetcher.fetch_block(gz_file):
                session.add_all(block)
                session.commit()
                processed_count += BLOCK_SIZE
                inserted_count += len(block)
                if processed_count % (BLOCK_SIZE * LOG_BLOCK_SIZE) == 0:
                    logging.info(
                        f"processing file {fn}: {processed_count} entries processed, {len(block)} inserted"
                    )
                # if processed_count >= 3 * BLOCK_SIZE:
                #     break
        except exc.SQLAlchemyError as e:
            logging.error(f"error processing data on table {table_name}")
            logging.error(f"Exception: {e}")
            logging.error(traceback.format_exc())
            logging.debug("Rolling back transaction")
            session.rollback()
        finally:
            logging.info(
                f"processed file {fn}: {processed_count} entries processed, {inserted_count} inserted"
            )


def main(db_name, db_uri=None):
    t0 = time.time()
    if db_uri:
        engine = sqlalchemy.create_engine(db_uri, echo=False)
    else:
        engine = locations.get_sqlite_engine(db_name)

    imdb_orm.Base.metadata.drop_all(bind=engine)
    imdb_orm.Base.metadata.create_all(bind=engine)

    fns = [directories.data(fn) for fn in locations.imdb_files]
    for fn in fns:
        if not os.path.isfile(fn):
            logging.debug(f"skipping file {fn}")
            continue
        t1 = time.time()
        import_file(fn, engine)
        logging.info(f"total time for file {fn}: {(time.time() - t1) / 60:.2f} minutes")
    logging.info(f"total time: {(time.time() - t0) / 60:.2f} minutes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process and import IMDb data with optional debug logging."
    )

    # Add a command-line option for setting the logging level to DEBUG
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")

    # Add a command-line option for specifying the database name
    parser.add_argument(
        "--db-name",
        type=str,
        default="IM01.db",  # Default value
        help="Specify the SQLite database name (default: IM01.db).",
    )

    # Add a command-line option for specifying the database URI
    parser.add_argument(
        "--db-uri",
        type=str,
        default=None,  # Default value
        help="Specify the database URI.",
    )

    args = parser.parse_args()

    # Configure logging
    if args.debug:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    main(args.db_name, args.db_uri)
