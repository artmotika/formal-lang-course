from project.rpq import rpq
from networkx.classes.multidigraph import MultiDiGraph


def get_graph(edges):
    graph = MultiDiGraph()
    for (v1, v2, label) in edges:
        graph.add_edge(v1, v2, label=label)
    return graph


def test_rpq1():
    assert rpq(
        "a*.(d+b).a.b",
        get_graph(
            {
                (1, 2, "a"),
                (2, 3, "b"),
                (3, 6, "d"),
                (6, 7, "d"),
                (7, 8, "a"),
                (8, 10, "b"),
                (10, 11, "d"),
                (8, 9, "a"),
                (9, 5, "c"),
                (5, 8, "e"),
                (2, 5, "e"),
                (1, 4, "b"),
                (3, 4, "a"),
                (4, 7, "b"),
                (2, 6, "a"),
                (6, 8, "a"),
            }
        ),
        start_states={1, 2},
        final_states={1, 10, 3},
    ) == {
        ("1:0;10;2;3;4;8;10;2;3;4;5;8", "10:1"),
        ("2:0;10;2;3;4;8;10;2;3;4;5;8", "10:1"),
    }
