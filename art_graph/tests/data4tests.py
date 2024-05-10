import pickle
import numpy as np
import json
import networkx as nx
from dataclasses import dataclass

from .. import directories
from ..cinegraph.node_types import PersonNode, WorkNode


class MockImdbObject(dict):
    def __init__(self, *args, default=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default

    def __missing__(self, key):
        return self.default

    def getID(self):
        return self["id"]

    @property
    def r(self):
        return np.random.RandomState(self.getID())

    @staticmethod
    def mock_object(node):
        m = MockImdbObject()
        m["id"] = node.id
        return m

    @staticmethod
    def mock_actor(person_node):
        p = MockImdbObject.mock_object(person_node)
        p["name"] = str(p.getID())
        pay = 100 * p.r.rand()
        p["pay"] = pay
        return p

    @staticmethod
    def mock_known_for(p, person_node, g):
        # Those actors who earn less than 10 will be known for nothing
        if p["pay"] > 10:
            # known for top four movies by rating
            movies = [
                MockImdbObject.mock_movie(movie) for movie in g.neighbors(person_node)
            ]
            movies.sort(key=lambda m: m["rating"], reverse=True)
            p["known for"] = list(movies[:4])

    @staticmethod
    def mock_movie(movie_node):
        m = MockImdbObject.mock_object(movie_node)
        m["title"] = str(m.getID())
        r = m.r
        m["votes"] = r.randint(1, 1000)
        m["rating"] = 10 * r.rand()
        return m

    @staticmethod
    def mock_cast(m, movie_node, g):
        # cast is top four actors by pay
        actors = [MockImdbObject.mock_actor(movie) for movie in g.neighbors(movie_node)]
        actors.sort(key=lambda a: a["pay"], reverse=True)
        m["cast"] = list(actors[:4])


@dataclass
class MockNode:
    id: str

    def getID(self):
        return self.id


@dataclass
class MockPerson(MockNode):
    filmography: dict

    def __getitem__(self, key):
        if key == "filmography":
            return self.filmography

    @staticmethod
    def mock_filmography(d):
        return {key: [MockNode(id) for id in ids] for key, ids in d.items()}


class MockIMBD:
    def __init__(self, g):
        self.g = g

    def get_person(self, id):
        person_node = PersonNode(id)
        p = MockImdbObject.mock_actor(person_node)
        MockImdbObject.mock_known_for(p, person_node, self.g)
        return p

    def get_movie(self, id):
        movie_node = WorkNode(id)
        m = MockImdbObject.mock_movie(movie_node)
        MockImdbObject.mock_cast(m, movie_node, self.g)
        return m


# Kevin Bacon
def get_bacon():
    with open(directories.test_data("bacon_filmography.json")) as f:
        filmography = json.load(f)
        return MockPerson("0000102", MockPerson.mock_filmography(filmography))


# Natalie Portman
def get_natalie():
    with open(directories.test_data("natalie_filmography.json")) as f:
        filmography = json.load(f)
        return MockPerson("0000204", MockPerson.mock_filmography(filmography))


# Sarah Michelle Gellar
def get_sarah():
    with open(directories.test_data("sarah_filmography.json")) as f:
        filmography = json.load(f)
    return MockPerson("0001264", MockPerson.mock_filmography(filmography))


def get_small_graph():
    path = directories.test_data("small_professional_graph.json")
    with open(path, "r") as f:
        d = json.load(f)
    with open(directories.test_data("small_professional_graph.json"), "w") as f:
        json.dump(d, f, indent=4)
    people = [PersonNode(id) for id in d["people"]]
    works = [WorkNode(id) for id in d["works"]]
    edges = [(PersonNode(e["person"]), WorkNode(e["work"])) for e in d["edges"]]
    g = nx.Graph()
    g.add_nodes_from(people)
    g.add_nodes_from(works)
    g.add_edges_from(edges)
    for e in d["edges"]:
        g.edges[(PersonNode(e["person"]), WorkNode(e["work"]))]["job"] = e["job"]
    return g
