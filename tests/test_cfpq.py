from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.cfpq import helings, matrix, tensor, cfpq, CFPQAlgorithm


def test_cfpq_tensor():
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
    assert cfpq(
        cfg, graph, start_nodes={0, 1}, final_nodes={1, 2, 3}, algo=CFPQAlgorithm.TENSOR
    ) == {
        (0, 2),
        (1, 3),
        (1, 2),
        (0, 3),
    }


def test_cfpq_matrix():
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
    assert cfpq(
        cfg, graph, start_nodes={0, 1}, final_nodes={1, 2, 3}, algo=CFPQAlgorithm.MATRIX
    ) == {
        (0, 2),
        (1, 3),
        (1, 2),
        (0, 3),
    }


def test_cfpq_helings():
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


def test_tensor():
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
    print(tensor(cfg, graph))
    assert tensor(cfg, graph) == {
        (0, Variable("A"), 1),
        (1, Variable("A"), 2),
        (2, Variable("A"), 0),
        (2, Variable("B"), 3),
        (3, Variable("B"), 2),
        (1, Variable("S"), 3),
        (1, Variable("S1"), 2),
        (0, Variable("S"), 2),
        (0, Variable("S1"), 3),
        (2, Variable("S"), 3),
        (2, Variable("S1"), 2),
        (1, Variable("S"), 2),
        (1, Variable("S1"), 3),
        (0, Variable("S"), 3),
        (0, Variable("S1"), 2),
        (2, Variable("S"), 2),
        (2, Variable("S1"), 3),
        (2, Variable("epsilon"), 2),
        (0, Variable("epsilon"), 0),
        (3, Variable("epsilon"), 3),
        (1, Variable("epsilon"), 1),
        (0, Variable("a"), 1),
        (2, Variable("b"), 3),
        (3, Variable("b"), 2),
        (2, Variable("a"), 0),
        (1, Variable("a"), 2),
    }


def test_matrix():
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
    assert matrix(cfg, graph) == {
        (0, Variable("A"), 1),
        (1, Variable("A"), 2),
        (2, Variable("A"), 0),
        (2, Variable("B"), 3),
        (3, Variable("B"), 2),
        (1, Variable("S"), 3),
        (1, Variable("S1"), 2),
        (0, Variable("S"), 2),
        (0, Variable("S1"), 3),
        (2, Variable("S"), 3),
        (2, Variable("S1"), 2),
        (1, Variable("S"), 2),
        (1, Variable("S1"), 3),
        (0, Variable("S"), 3),
        (0, Variable("S1"), 2),
        (2, Variable("S"), 2),
        (2, Variable("S1"), 3),
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
        (0, Variable("A"), 1),
        (1, Variable("A"), 2),
        (2, Variable("A"), 0),
        (2, Variable("B"), 3),
        (3, Variable("B"), 2),
        (1, Variable("S"), 3),
        (1, Variable("S1"), 2),
        (0, Variable("S"), 2),
        (0, Variable("S1"), 3),
        (2, Variable("S"), 3),
        (2, Variable("S1"), 2),
        (1, Variable("S"), 2),
        (1, Variable("S1"), 3),
        (0, Variable("S"), 3),
        (0, Variable("S1"), 2),
        (2, Variable("S"), 2),
        (2, Variable("S1"), 3),
    }
