# Internet Movie Database Inc. makes publicly available a limited dataset for academic purposes.
# See https://www.imdb.com/interfaces/
# Carefully check license to make sure this is matches you intended use.

import os
from tqdm import tqdm
import requests

from art_graph import directories
from art_graph.cinema_data_providers.imbd_non_commercial.locations import (
    imdb_files,
)


def retrieve_imdb_data(filename):
    path = directories.data(filename)
    print(path)
    if os.path.exists(path):
        print("{} already exists".format(path))
        return
    url = "https://datasets.imdbws.com/{}".format(filename)
    print("Down loading {}".format(url))
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    with open(path, "wb") as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()


def main():
    print("Downloading data")

    # Iterate over each file and download it using retrieve_imdb_data
    for file_name in imdb_files:
        retrieve_imdb_data(file_name)


if __name__ == "__main__":
    main()
