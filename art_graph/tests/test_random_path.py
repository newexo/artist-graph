import pytest

import numpy as np
import networkx as nx

from .data4tests import get_small_graph
from ..cinegraph import random_path
from ..cinegraph.node_types import PersonNode


@pytest.fixture
def small_graph():
    return get_small_graph()


@pytest.fixture
def random_state():
    return np.random.RandomState(42)


@pytest.fixture
def candidates(small_graph):
    return [node for node in small_graph.nodes if node.is_person and (node.id % 3 == 0)]


def test_select_random_nodes():
    nodes = [
        PersonNode(0),
        PersonNode(1),
        PersonNode("asdf"),
        PersonNode("42"),
        PersonNode(42),
    ]
    r = np.random.RandomState(42)

    (a,) = random_path.select_random_nodes(nodes, r=r)
    assert PersonNode("asdf") == a

    (a,) = random_path.select_random_nodes(nodes, r=r)
    assert PersonNode(1) == a

    (a,) = random_path.select_random_nodes(nodes, r=r)
    assert PersonNode("asdf") == a

    a, b = random_path.select_random_nodes(nodes, size=2, r=r)
    assert PersonNode("42") == a
    assert PersonNode("asdf") == b

    a, b = random_path.select_random_nodes(nodes, size=2, r=r)
    assert PersonNode("42") == a
    assert PersonNode(0) == b

    r0 = np.random.RandomState(42)
    r1 = np.random.RandomState(42)

    # selection should be repeatable of order of nodes
    for _ in range(100):
        a, b = random_path.select_random_nodes(nodes, size=2, r=r0)
        c, d = random_path.select_random_nodes(nodes, size=2, r=r1)
        assert a == c
        assert b == d

    shuffled_nodes = nodes.copy()
    r.shuffle(shuffled_nodes)

    # selection should be independent of order of nodes
    for _ in range(100):
        a, b = random_path.select_random_nodes(nodes, size=2, r=r0)
        c, d = random_path.select_random_nodes(shuffled_nodes, size=2, r=r1)
        assert a == c
        assert b == d

    # selection should be independent of type of iterable
    for _ in range(100):
        a, b = random_path.select_random_nodes(nodes, size=2, r=r0)
        c, d = random_path.select_random_nodes(set(nodes), size=2, r=r1)
        assert a == c
        assert b == d


def test_make_people_subgraph(small_graph, candidates):
    people_subgraph = random_path.make_people_subgraph(small_graph, candidates)

    candidates = set(candidates)

    all_subgraph_nodes = set(people_subgraph.nodes)
    assert candidates.issubset(all_subgraph_nodes)

    for node in people_subgraph.nodes:
        if node.is_person:
            assert node in candidates
        else:
            assert people_subgraph.degree(node) > 0


def test_make_game_from_starting_node_fail(small_graph, candidates, random_state):
    # there is no game of length five starting from the first candidate
    with pytest.raises(random_path.CandidateNotFoundException):
        random_path.make_path_from_starting_node(
            small_graph, candidates[0], candidates, 5, r=random_state
        )


def test_make_game_from_starting_node(small_graph, candidates, random_state):
    candidates = candidates
    # find games of length 1
    a, b = random_path.make_path_from_starting_node(
        small_graph, candidates[0], candidates, 1, r=random_state
    )
    assert candidates[0] == a
    assert 2 == nx.shortest_path_length(small_graph, a, b)
    assert PersonNode(92184) == a
    assert PersonNode(2091) == b

    a, b = random_path.make_path_from_starting_node(
        small_graph, candidates[2], candidates, 1, r=random_state
    )
    assert candidates[2] == a
    assert 2 == nx.shortest_path_length(small_graph, a, b)
    assert PersonNode(345) == a
    assert PersonNode(114) == b

    # find game of length 2
    a, b = random_path.make_path_from_starting_node(
        small_graph, candidates[2], candidates, 2, r=random_state
    )
    assert candidates[2] == a
    assert 4 == nx.shortest_path_length(small_graph, a, b)
    assert PersonNode(345) == a
    assert PersonNode(246) == b

    # find game of length 4
    a, b = random_path.make_path_from_starting_node(
        small_graph, candidates[2], candidates, 4, r=random_state
    )
    assert candidates[2] == a
    assert 8 == nx.shortest_path_length(small_graph, a, b)
    assert PersonNode(345) == a
    assert PersonNode(4851) == b


def test_make_game_by_iteration_fail(small_graph, candidates, random_state):
    # there is no game of length five
    with pytest.raises(random_path.GameNotFoundException):
        random_path.make_path_by_iteration(small_graph, candidates, 5, r=random_state)


def test_make_game_by_iteration(small_graph, candidates, random_state):
    # choose actors who have been in the same movie
    a, b = random_path.make_path_by_iteration(
        small_graph, candidates, 1, r=random_state
    )
    first_choice = a.id
    assert 2 == nx.shortest_path_length(small_graph, a, b)
    assert PersonNode(7955301) == a
    assert PersonNode(147) == b

    a, b = random_path.make_path_by_iteration(
        small_graph, candidates, 1, r=random_state
    )
    assert first_choice != a.id
    assert 2 == nx.shortest_path_length(small_graph, a, b)

    # choose actors who are two movies apart
    a, b = random_path.make_path_by_iteration(
        small_graph, candidates, 2, r=random_state
    )
    assert 4 == nx.shortest_path_length(small_graph, a, b)
    assert PersonNode(111) == a
    assert PersonNode(309693) == b

    a, b = random_path.make_path_by_iteration(
        small_graph, candidates, 2, r=random_state
    )
    assert 4 == nx.shortest_path_length(small_graph, a, b)

    a, b = random_path.make_path_by_iteration(
        small_graph, candidates, 2, r=random_state
    )
    assert 4 == nx.shortest_path_length(small_graph, a, b)

    # choose some actors that are three movies apart
    a, b = random_path.make_path_by_iteration(
        small_graph, candidates, 3, r=random_state
    )
    assert 6 == nx.shortest_path_length(small_graph, a, b)

    a, b = random_path.make_path_by_iteration(
        small_graph, candidates, 3, r=random_state
    )
    assert 6 == nx.shortest_path_length(small_graph, a, b)
    assert PersonNode(1605114) == a
    assert PersonNode(261) == b


def test_random_path(small_graph, candidates, random_state):
    gm = random_path.PathMaker(small_graph, candidates)
    assert set(candidates) == gm.candidates

    # find games of length 1
    a, b = gm.make_game(1, r=random_state)
    assert 2 == nx.shortest_path_length(gm.g, a, b)
    assert PersonNode(228) == a
    assert PersonNode(396558) == b

    a, b = gm.make_game(2, r=random_state)
    assert 4 == nx.shortest_path_length(gm.g, a, b)
    assert PersonNode(168) == a
    assert PersonNode(102) == b

    a, b = gm.make_game(4, r=random_state)
    assert 8 == nx.shortest_path_length(gm.g, a, b)
    assert PersonNode(744834) == a
    assert PersonNode(7955301) == b

    with pytest.raises(random_path.GameNotFoundException):
        gm.make_game(10, r=random_state)
