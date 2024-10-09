from art_graph import directories


def db_path() -> str:
    return directories.data("IM.db")


imdb_files = [
    "name.basics.tsv.gz",
    "title.basics.tsv.gz",
    "title.ratings.tsv.gz",
    "title.principals.tsv.gz",
    "title.akas.tsv.gz",  # Add additional files if necessary
    "title.crew.tsv.gz",  # Add title.crew.tsv.gz
    "title.episode.tsv.gz",  # Add title.episode.tsv.gz
]
