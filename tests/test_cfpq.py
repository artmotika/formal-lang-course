from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.cfpq import helings, cfpq


def test_cfpq():
    cfg = CFG.from_text(
        """S -> A B | A S1
    S1 -> S B
    A -> a
    B -> b
    """
    )
    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 0, label="a")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(3, 2, label="b")
    assert cfpq(cfg, graph, start_nodes={0, 1}, final_nodes={1, 2, 3}) == {
        (0, 2),
        (1, 3),
        (1, 2),
        (0, 3),
    }


def test_helings():
    cfg = CFG.from_text(
        """S -> A B | A S1
    S1 -> S B
    A -> a
    B -> b
    """
    )

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 0, label="a")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(3, 2, label="b")
    assert helings(cfg, graph) == {
        (Variable("A"), 0, 1),
        (Variable("A"), 1, 2),
        (Variable("A"), 2, 0),
        (Variable("B"), 2, 3),
        (Variable("B"), 3, 2),
        (Variable("S"), 1, 3),
        (Variable("S1"), 1, 2),
        (Variable("S"), 0, 2),
        (Variable("S1"), 0, 3),
        (Variable("S"), 2, 3),
        (Variable("S1"), 2, 2),
        (Variable("S"), 1, 2),
        (Variable("S1"), 1, 3),
        (Variable("S"), 0, 3),
        (Variable("S1"), 0, 2),
        (Variable("S"), 2, 2),
        (Variable("S1"), 2, 3),
    }
