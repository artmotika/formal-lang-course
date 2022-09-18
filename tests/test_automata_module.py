from project.automata_module import build_min_dfa_from_regex
from project.automata_module import build_nfa_from_graph
from project.graph_module import build_two_cycles_graph_dot_format
from project.graph_module import get_graph


def test_build_min_dfa_from_regex_concatenation():
    dfa = build_min_dfa_from_regex("a.b.c")
    assert (
        dfa.accepts(["a", "b", "c"])
        and not dfa.accepts(["a", "b"])
        and dfa.is_deterministic()
        and len(dfa.states) == 4
    )


def test_build_min_dfa_from_regex_union():
    dfa = build_min_dfa_from_regex("a|b|c")
    assert (
        not dfa.accepts(["a", "b", "c"])
        and not dfa.accepts(["a", "b"])
        and not dfa.accepts(["a", "a"])
        and dfa.accepts(["a"])
        and dfa.is_deterministic()
        and len(dfa.states) == 2
    )


def test_build_min_dfa_from_regex_kleene():
    dfa = build_min_dfa_from_regex("a*")
    assert (
        dfa.accepts(["a"])
        and dfa.accepts(["a", "a"])
        and dfa.accepts([])
        and dfa.is_deterministic()
        and len(dfa.states) == 1
    )


def test_build_nfa_from_graph_from_dataset():
    nfa = build_nfa_from_graph(get_graph("wc"), {1}, {47})
    assert (
        nfa.accepts(["A"])
        and nfa.get_number_transitions() == 269
        and len(nfa.states) == 332
    )


def test_build_nfa_from_graph_from_dot_file(tmp_path):
    test_file_path = tmp_path / "test_graph.dot"
    build_two_cycles_graph_dot_format(1, 2, ("man", "woman"), test_file_path)
    nfa1 = build_nfa_from_graph(test_file_path, {"1"}, {"2"})
    nfa2 = build_nfa_from_graph(test_file_path, {"1"}, {"0"})
    nfa3 = build_nfa_from_graph(test_file_path)
    assert (
        not nfa1.accepts(["man"])
        and nfa2.accepts(["man"])
        and nfa3.accepts(["woman"])
        and not nfa3.accepts(["someone"])
        and nfa1.get_number_transitions() == 5 == nfa2.get_number_transitions()
        and len(nfa1.states) == 4 == len(nfa2.states) == len(nfa3.states)
    )
