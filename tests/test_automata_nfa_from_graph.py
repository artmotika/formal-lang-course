from networkx.algorithms.isomorphism.isomorph import is_isomorphic
from networkx.algorithms.isomorphism.matchhelpers import categorical_multiedge_match
from networkx.algorithms.isomorphism.matchhelpers import categorical_node_match
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State

from project.automata import build_nfa_from_graph
from project.graph_utilities import build_two_cycles_graph_dot_format
from project.graph_utilities import get_graph


# def test_build_nfa_from_graph_from_dataset():
#     networkx_graph = get_graph("wc")
#     nfa = build_nfa_from_graph(networkx_graph, {1}, {47})
#     assert all(
#         (
#             nfa.accepts(["A"]),
#             nfa.get_number_transitions() == 269,
#             len(nfa.states) == 332,
#         )
#     )


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
