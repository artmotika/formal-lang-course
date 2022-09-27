from project.automata import build_nfa_from_graph
from project.automata import build_min_dfa_from_regex
from project.bool_decomposed_fa import BoolDecomposedFA
from typing import Any


def rpq(
    regex, graph, start_states: set = None, final_states: set = None
) -> set[tuple[Any, Any]]:
    aut1 = build_nfa_from_graph(graph, start_states, final_states)
    aut2 = build_min_dfa_from_regex(regex)
    bool_decomposed_fa = BoolDecomposedFA.from_fa(aut1).get_intersection(
        BoolDecomposedFA.from_fa(aut2)
    )
    result = set()
    for source, target in zip(*bool_decomposed_fa.transitive_closure().nonzero()):
        state_source = bool_decomposed_fa.idx_to_state.get(source)
        state_target = bool_decomposed_fa.idx_to_state.get(target)
        if (
            state_source in bool_decomposed_fa.start_states
            and state_target in bool_decomposed_fa.final_states
        ):
            result.add((state_source, state_target))
    return result
