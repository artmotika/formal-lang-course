from tests.test_rpq_tensor_intersection import get_graph
from project.rpq import MethodRpq
from project.rpq import BfsIntersection
from project.rpq import rpq


def test_rpq1():
    assert rpq(
        "a.b",
        get_graph(
            {
                (1, 2, "a"),
                (2, 3, "b"),
            }
        ),
        start_states={1},
        final_states={1, 2, 3},
        method_rpq=MethodRpq(BfsIntersection(is_multiple_source=True)),
    ) == {(1, 3)}


def test_rpq2():
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
        method_rpq=MethodRpq(BfsIntersection(is_multiple_source=True)),
    ) == {(2, 10), (1, 10)}


def test_rpq3():
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
        start_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        final_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        method_rpq=MethodRpq(BfsIntersection(is_multiple_source=True)),
    ) == {(3, 10), (1, 7), (2, 7), (2, 10), (6, 10), (1, 10), (4, 10)}


def test_rpq4():
    assert rpq(
        "a.(a+d).(a+b)",
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
        start_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        final_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        method_rpq=MethodRpq(BfsIntersection(is_multiple_source=True)),
    ) == {(1, 8), (2, 8), (2, 9), (2, 10)}


def test_rpq5():
    assert rpq(
        "a*.(a+d+e)*",
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
        start_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        final_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        method_rpq=MethodRpq(BfsIntersection(is_multiple_source=True)),
    ) == {
        (3, 9),
        (3, 7),
        (2, 2),
        (3, 4),
        (1, 2),
        (1, 9),
        (1, 5),
        (1, 6),
        (3, 6),
        (3, 3),
        (2, 8),
        (2, 5),
        (2, 7),
        (1, 7),
        (2, 9),
        (9, 9),
        (6, 9),
        (7, 7),
        (7, 8),
        (10, 10),
        (7, 9),
        (10, 11),
        (1, 8),
        (5, 9),
        (11, 11),
        (5, 5),
        (4, 4),
        (6, 6),
        (5, 8),
        (3, 8),
        (1, 1),
        (8, 8),
        (8, 9),
        (6, 8),
        (6, 7),
        (2, 6),
    }


def test_rpq6():
    assert rpq(
        "(a+d+e)*.c",
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
        start_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        final_states={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        method_rpq=MethodRpq(BfsIntersection(is_multiple_source=True)),
    ) == {(5, 5), (6, 5), (1, 5), (9, 5), (7, 5), (2, 5), (8, 5), (3, 5)}
