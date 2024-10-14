# Scripts to construct and use artist graphs

## IMDb S3 data

Note that these scripts should be used for academic purposes only according to IMDb's terms of service. See 
[IMDb_DISCLAMER.md](IMDb_DISCLAMER.md).

### IMDb data download

From the root of the repository, run the following command to download IMDb data from S3:

```bash
python scripts/imdb_download.py
```

### Import IMDb non-commercial data into SQLite database

Use `s3_2db.py` to import the downloaded IMDb data into a local SQLite database located in the `data/` directory.

To run the `s3_2db.py` script with the default settings (database name: `IM01.db` and logging level: `INFO`):

```bash
python scripts/s3_2db.py
```

#### Optional Arguments

- `--debug`: Enable `DEBUG` level logging for more detailed output.
- `--db-name`: Specify SQLite database filename. Defaults to database`IM01.db`.
