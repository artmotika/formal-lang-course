from project.bool_decomposed_fa import BoolDecomposedFA
from tests.test_bool_decomposed_fa import get_test_fa
from numpy import array


def test_transactive_closure():
    states = {1, 2, 3, 4, 5}
    start_states = {1}
    final_states = {2}
    transitions = {(1, "a", 2), (2, "b", 4), (4, "c", 1), (3, "d", 5), (5, "d", 3)}
    transitive_closure_matrix = BoolDecomposedFA.from_fa(
        get_test_fa(states, start_states, final_states, transitions)
    ).transitive_closure()
    for (x, y) in zip(*transitive_closure_matrix.nonzero()):
        if not (x, y) in zip(
            array([0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4]),
            array([0, 1, 3, 1, 0, 3, 2, 4, 3, 0, 1, 2, 4]),
        ):
            assert False
    assert True
