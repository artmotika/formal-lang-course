from project.automata import build_nfa_from_graph
from project.automata import build_min_dfa_from_regex
from project.bool_decomposed_fa import BoolDecomposedFA
from typing import Any


class TensorIntersection:
    pass


class BfsIntersection:
    def __init__(self, is_multiple_source):
        self.is_multiple_source = is_multiple_source


class MethodRpq:
    def __init__(self, method):
        self.method = method


def rpq(
    regex,
    graph,
    start_states: set = None,
    final_states: set = None,
    method_rpq: MethodRpq = MethodRpq(TensorIntersection()),
) -> set[tuple[Any, Any]]:
    aut1 = build_nfa_from_graph(graph, start_states, final_states)
    aut2 = build_min_dfa_from_regex(regex)
    result = set()
    if isinstance(method_rpq.method, TensorIntersection):
        bool_decomposed_fa = BoolDecomposedFA.from_fa(aut1).get_intersection(
            BoolDecomposedFA.from_fa(aut2)
        )
        for source, target in zip(*bool_decomposed_fa.transitive_closure().nonzero()):
            state_source = bool_decomposed_fa.idx_to_state.get(source)
            state_target = bool_decomposed_fa.idx_to_state.get(target)
            if (
                state_source in bool_decomposed_fa.start_states
                and state_target in bool_decomposed_fa.final_states
            ):
                result.add((state_source, state_target))
        return result
    elif isinstance(method_rpq.method, BfsIntersection):
        bool_decomposed_aut1 = BoolDecomposedFA.from_fa(aut1)
        bool_decomposed_aut2 = BoolDecomposedFA.from_fa(aut2)
        n_states_aut2 = len(aut2.states)
        if method_rpq.method.is_multiple_source:
            for i, j in zip(
                *bool_decomposed_aut1.get_bfs_intersection(
                    bool_decomposed_aut2,
                    is_multiple_source=method_rpq.method.is_multiple_source,
                ).nonzero()
            ):
                aut2_state = bool_decomposed_aut2.idx_to_state.get(i % n_states_aut2)
                aut1_state = bool_decomposed_aut1.idx_to_state.get(j)
                if (
                    aut2_state in bool_decomposed_aut2.final_states
                    and aut1_state in bool_decomposed_aut1.final_states
                ):
                    result.add(
                        (
                            bool_decomposed_aut1.multiple_source_dict.get(
                                i // n_states_aut2
                            ),
                            aut1_state,
                        )
                    )
        else:
            for i, j in zip(
                *bool_decomposed_aut1.get_bfs_intersection(
                    bool_decomposed_aut2,
                    is_multiple_source=method_rpq.method.is_multiple_source,
                ).nonzero()
            ):
                aut2_state = bool_decomposed_aut2.idx_to_state.get(i)
                aut1_state = bool_decomposed_aut1.idx_to_state.get(j)
                if (
                    aut2_state in bool_decomposed_aut2.final_states
                    and aut1_state in bool_decomposed_aut1.final_states
                ):
                    result.add(aut1_state)
        return result
    else:
        raise ValueError
