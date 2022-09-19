from networkx.algorithms.isomorphism.isomorph import is_isomorphic
from networkx.algorithms.isomorphism.matchhelpers import categorical_multiedge_match
from networkx.algorithms.isomorphism.matchhelpers import categorical_node_match
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton.deterministic_finite_automaton import (
    DeterministicFiniteAutomaton,
)
from project.automata_module import build_min_dfa_from_regex
from project.automata_module import build_nfa_from_graph
from project.graph_module import build_two_cycles_graph_dot_format
from project.graph_module import get_graph


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


def test_build_nfa_from_graph_from_dataset():
    networkx_graph = get_graph("wc")
    nfa = build_nfa_from_graph(networkx_graph, {1}, {47})
    assert (
        nfa.accepts(["A"])
        and nfa.get_number_transitions() == 269
        and len(nfa.states) == 332
    )


def test_build_nfa_from_graph_from_dot_file(tmp_path):
    test_file_path = tmp_path / "test_graph.dot"
    build_two_cycles_graph_dot_format(1, 2, ("man", "woman"), test_file_path)
    actual_nfa1 = build_nfa_from_graph(test_file_path, {"1"}, {"2"})
    actual_nfa2 = build_nfa_from_graph(test_file_path)
    expected_nfa1 = EpsilonNFA()
    expected_nfa2 = EpsilonNFA()
    expected_nfa1.add_transitions(
        [
            (3, "woman", 0),
            (2, "woman", 3),
            (0, "man", 1),
            (0, "woman", 2),
            (1, "man", 0),
        ]
    )
    expected_nfa2.add_transitions(
        [
            (3, "woman", 0),
            (2, "woman", 3),
            (0, "man", 1),
            (0, "woman", 2),
            (1, "man", 0),
        ]
    )
    expected_nfa1.add_start_state(State(1))
    expected_nfa1.add_final_state(State(2))
    expected_nfa2.add_start_state(State(0))
    expected_nfa2.add_start_state(State(1))
    expected_nfa2.add_start_state(State(2))
    expected_nfa2.add_start_state(State(3))
    expected_nfa2.add_final_state(State(0))
    expected_nfa2.add_final_state(State(1))
    expected_nfa2.add_final_state(State(2))
    expected_nfa2.add_final_state(State(3))
    assert is_isomorphic(
        G1=expected_nfa1.to_networkx(),
        G2=actual_nfa1.to_networkx(),
        node_match=categorical_node_match(["is_start", "is_final"], [None, None]),
        edge_match=categorical_multiedge_match("label", None),
    ) and is_isomorphic(
        G1=expected_nfa2.to_networkx(),
        G2=actual_nfa2.to_networkx(),
        node_match=categorical_node_match(["is_start", "is_final"], [None, None]),
        edge_match=categorical_multiedge_match("label", None),
    )
