import pytest
from project.grammar_query_language.parser import check


@pytest.mark.parametrize(
    "input, accept",
    [
        ("-1", True),
        ("1", True),
        ('"string"', True),
        ("false", True),
        ('r"a | b | c"', True),
        ('c"S -> a b | a S b"', True),
    ],
)
def test_val(input, accept):
    assert check(input, lambda p: p.val()) == accept


@pytest.mark.parametrize(
    "input, accept",
    [
        ("set_starts({3, 5, 6}, g)", True),
        ("set_starts({3, 5, 6}, lambda g -> g)", False),
        ("get_starts(g)", True),
        ("get_starts(lambda g -> g)", False),
        ("get_reachable(g1 & regex)", True),
        ("get_reachable(lambda g -> g)", False),
        ("map(lambda ((a, b), (_, _)) -> (a, b), g)", True),
        ('load("graph")', True),
        ("load(graph)", False),
        ("a & b", True),
        ("{1, 2, 3}", True),
    ],
)
def test_expr(input, accept):
    assert check(input, lambda p: p.expr()) == accept


@pytest.mark.parametrize(
    "input, accept",
    [
        ("x = 1", True),
        ("print(1)", True),
        ("g1 = star(g2) & (g3 | g4)", True),
        ("x", False),
    ],
)
def test_stmt(input, accept):
    assert check(input, lambda p: p.stmt()) == accept


@pytest.mark.parametrize(
    "input, accept",
    [
        (
            """
            g = load("graph1.dot");

            reachable_pairs = filter(lambda (a, _) -> (a in {3, 5, 6}), get_reachable(g));
            res = map(lambda (_, b) -> (b), reachable_pairs);
            print(res);

            g = set_starts({3, 5, 6}, g);
            res = map(lambda (_, b) -> (b), get_reachable(g));
            print(res);
             """,
            True,
        ),
        (
            """
            g1 = load("graph1.dot");
            regex = r"georges|(Det.N)";

            res = map(lambda ((a, b), (_, _)) -> (a, b), get_reachable(g1 & regex));
            print(res);
             """,
            True,
        ),
        (
            """
            g1 = load("graph1.dot");
            cfg = c"S -> a S b | a b";

            res = map(lambda ((a, b), (_, _)) -> (a, b), get_reachable(g1 & cfg));
            print(res);
             """,
            True,
        ),
        (
            """
                g1 = load("graph1.dot");
                cfg = c"S -> a S b | a b";

                res = map(lambda ((a, b), (_, _)) -> a, b, get_reachable(g1 & cfg));
                print(res);
                 """,
            False,
        ),
    ],
)
def test_prog(input, accept):
    assert check(input, lambda p: p.prog()) == accept
