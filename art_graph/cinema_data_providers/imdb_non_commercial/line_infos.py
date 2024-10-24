import gzip

from art_graph.cinema_data_providers.imdb_non_commercial import utils


class LineInfos:
    fd: gzip.GzipFile
    headers: list[str]

    def __init__(self, fd, headers):
        self.fd = fd
        self.headers = headers

    def info(self):
        for line in self.fd:
            yield utils.line2info(line, self.headers)
