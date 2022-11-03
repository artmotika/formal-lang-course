from project.bool_decomposed_fa_csr import BoolDecomposedFA
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol


def get_test_fa(states, start_states, final_states, transitions):
    test_fa = EpsilonNFA(
        states={State(state) for state in states},
        start_state={State(state) for state in start_states},
        final_states={State(state) for state in final_states},
    )
    test_fa.add_transitions(
        [
            (State(state1), Symbol(symbol), State(state2))
            for (state1, symbol, state2) in transitions
        ]
    )
    return test_fa


def test_from_fa1():
    states = {1, 2}
    start_states = {1}
    final_states = {1, 2}
    transitions = {(1, "a", 2)}
    bool_decomposed_fa = BoolDecomposedFA.from_fa(
        get_test_fa(states, start_states, final_states, transitions)
    )
    assert all(
        (
            bool_decomposed_fa.state_to_idx.keys() == states,
            len(bool_decomposed_fa.idx_to_state.keys()) == len(states),
            bool_decomposed_fa.start_states == start_states,
            bool_decomposed_fa.final_states == final_states,
            len(bool_decomposed_fa.adjacency_matrices.keys()) == 2,
            bool_decomposed_fa.adjacency_matrices.get(State("a")).toarray().tolist()
            == [[0, 1], [0, 0]],
        )
    )


def test_from_fa2():
    states = {3, 4, 6}
    start_states = {3}
    final_states = {3, 4, 6}
    transitions = {(3, "b", 4), (4, "c", 6), (6, "a", 3), (3, "a", 6)}
    bool_decomposed_fa = BoolDecomposedFA.from_fa(
        get_test_fa(states, start_states, final_states, transitions)
    )
    symbol1 = Symbol("b")
    symbol2 = Symbol("c")
    symbol3 = Symbol("a")
    expected_adjacency_matrices = {
        symbol3: [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
        symbol2: [[0, 0, 0], [0, 0, 1], [0, 0, 0]],
        symbol1: [[0, 1, 0], [0, 0, 0], [0, 0, 0]],
    }
    assert all(
        (
            bool_decomposed_fa.state_to_idx.keys() == states,
            len(bool_decomposed_fa.idx_to_state.keys()) == len(states),
            bool_decomposed_fa.start_states == start_states,
            bool_decomposed_fa.final_states == final_states,
            len(bool_decomposed_fa.adjacency_matrices.keys()) == 4,
            bool_decomposed_fa.adjacency_matrices.get(symbol1).toarray().tolist()
            == expected_adjacency_matrices.get(symbol1),
            bool_decomposed_fa.adjacency_matrices.get(symbol2).toarray().tolist()
            == expected_adjacency_matrices.get(symbol2),
            bool_decomposed_fa.adjacency_matrices.get(symbol3).toarray().tolist()
            == expected_adjacency_matrices.get(symbol3),
        )
    )


def test_get_intersection():
    states1 = {1, 2}
    start_states1 = {1}
    final_states1 = {1, 2}
    transitions1 = {(1, "a", 2)}
    states2 = {3, 4, 6}
    start_states2 = {3}
    final_states2 = {3, 4, 6}
    transitions2 = {(3, "b", 4), (4, "c", 6), (6, "a", 3), (3, "a", 6)}
    bool_decomposed_fa1 = BoolDecomposedFA.from_fa(
        get_test_fa(states1, start_states1, final_states1, transitions1)
    )
    bool_decomposed_fa2 = BoolDecomposedFA.from_fa(
        get_test_fa(states2, start_states2, final_states2, transitions2)
    )
    inter_bool_decomposed_fa = bool_decomposed_fa1.get_intersection(bool_decomposed_fa2)
    symbol1 = Symbol("b")
    symbol2 = Symbol("c")
    symbol3 = Symbol("a")
    expected_state_to_idx = {
        State("1:3"): 0,
        State("1:4"): 1,
        State("1:6"): 2,
        State("2:3"): 3,
        State("2:4"): 4,
        State("2:6"): 5,
    }
    assert all(
        (
            len(inter_bool_decomposed_fa.state_to_idx.keys())
            == len(states1) * len(states2)
            == len(inter_bool_decomposed_fa.idx_to_state.keys()),
            inter_bool_decomposed_fa.start_states == {"1:3"},
            inter_bool_decomposed_fa.final_states
            == {"1:3", "1:4", "1:6", "2:3", "2:4", "2:6"},
            len(inter_bool_decomposed_fa.adjacency_matrices.keys()) == 2,
            inter_bool_decomposed_fa.adjacency_matrices.get(symbol1) is None,
            inter_bool_decomposed_fa.adjacency_matrices.get(symbol2) is None,
            inter_bool_decomposed_fa.adjacency_matrices.get(symbol3).toarray().tolist()
            == [
                [0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ],
            inter_bool_decomposed_fa.state_to_idx == expected_state_to_idx,
        )
    )
