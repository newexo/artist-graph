# Artist graph

This project is a set of Python tools for creating graphs of artists and collaborators. It is based on NetworkX, which
creates an annotated graph whose nodes are people and works of art. Examples of this include the following:

- Citation graphs of scholars and their academic papers
- Movies and the actors, writers, directors and producers who make them
- Music, and the musicians, composers, and producers who create it
- Open source software projects and their contributors

## Docker

Build the image:

```
DOCKER_BUILDKIT=1 docker build --target=runtime -f Dockerfile . -t artist-graph
```

Run the image with a shell:

```
docker run --name artist-graph -v /some/host/machine/directory:/app/data/:rw -it artist-graph sh
```

Remove the container:

```
docker container rm artist-graph
```

Download the IMDb data:

```
docker run --name artist-graph -v /some/host/machine/directory/:/app/data/:rw -it artist-graph python scripts/imdb_download.py
```

Build the SQLite database:

```
docker run --name artist-graph -v /some/host/machine/directory/:/app/data/:rw -it artist-graph python scripts/s3_2db.py
```

## Acknowledgements

This project began with code originally part of the [Cinema Game](https://github.com/ChiPowers/cinema_game) project,
which was developed by Chivon Powers and Reuben Brasher. That project relied on a graph of movies and people, which can
now be constructed using the tools in this project.
