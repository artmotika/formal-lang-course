from tests.test_rpq_tensor_intersection import get_graph
from project.rpq import MethodRpq
from project.rpq import MethodBfs
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
        method_rpq=MethodRpq(MethodBfs(is_multiple_source=False)),
    ) == {3}


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
        method_rpq=MethodRpq(MethodBfs(is_multiple_source=False)),
    ) == {10}


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
        method_rpq=MethodRpq(MethodBfs(is_multiple_source=False)),
    ) == {10, 7}


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
        method_rpq=MethodRpq(MethodBfs(is_multiple_source=False)),
    ) == {8, 9, 10}


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
        method_rpq=MethodRpq(MethodBfs(is_multiple_source=False)),
    ) == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}


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
        method_rpq=MethodRpq(MethodBfs(is_multiple_source=False)),
    ) == {5}
