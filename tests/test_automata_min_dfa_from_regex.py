from networkx.algorithms.isomorphism.isomorph import is_isomorphic
from networkx.algorithms.isomorphism.matchhelpers import categorical_multiedge_match
from networkx.algorithms.isomorphism.matchhelpers import categorical_node_match
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton.deterministic_finite_automaton import (
    DeterministicFiniteAutomaton,
)

from project.automata import build_min_dfa_from_regex


def test_build_min_dfa_from_regex_concatenation():
    actual_dfa = build_min_dfa_from_regex("a.b.c")
    expected_dfa = DeterministicFiniteAutomaton()
    expected_dfa.add_transitions(
        [("4;5", "c", 1), ("2;3", "b", "4;5"), (0, "a", "2;3")]
    )
    expected_dfa.add_start_state(State(0))
    expected_dfa.add_final_state(State(1))
    assert is_isomorphic(
        G1=expected_dfa.to_networkx(),
        G2=actual_dfa.to_networkx(),
        node_match=categorical_node_match(["is_start", "is_final"], [None, None]),
        edge_match=categorical_multiedge_match("label", None),
    )


def test_build_min_dfa_from_regex_union():
    actual_dfa = build_min_dfa_from_regex("a|b|c")
    expected_dfa = DeterministicFiniteAutomaton()
    expected_dfa.add_transitions(
        [
            ("0;2;4;6;8", "c", "1;3;1;5;7;1;5;9"),
            ("0;2;4;6;8", "b", "1;3;1;5;7;1;5;9"),
            ("0;2;4;6;8", "a", "1;3;1;5;7;1;5;9"),
        ]
    )
    expected_dfa.add_start_state(State("0;2;4;6;8"))
    expected_dfa.add_final_state(State("1;3;1;5;7;1;5;9"))
    assert is_isomorphic(
        G1=expected_dfa.to_networkx(),
        G2=actual_dfa.to_networkx(),
        node_match=categorical_node_match(["is_start", "is_final"], [None, None]),
        edge_match=categorical_multiedge_match("label", None),
    )


def test_build_min_dfa_from_regex_kleene():
    actual_dfa = build_min_dfa_from_regex("a*")
    expected_dfa = DeterministicFiniteAutomaton()
    expected_dfa.add_transitions([("0;1;2;1;2;3", "a", "0;1;2;1;2;3")])
    expected_dfa.add_start_state(State("0;1;2;1;2;3"))
    expected_dfa.add_final_state(State("0;1;2;1;2;3"))
    assert is_isomorphic(
        G1=expected_dfa.to_networkx(),
        G2=actual_dfa.to_networkx(),
        node_match=categorical_node_match(["is_start", "is_final"], [None, None]),
        edge_match=categorical_multiedge_match("label", None),
    )
