from project.automata import build_nfa_from_graph
from project.automata import build_min_dfa_from_regex
from project.bool_decomposed_fa import BoolDecomposedFA
from typing import Any
from typing import Union
from project.bool_decomposed_intersection import (
    TensorIntersection,
    BfsIntersectionSet,
    BfsIntersectionMS,
)


class MethodTensor:
    pass


class MethodBfs:
    def __init__(self, is_multiple_source):
        self.is_multiple_source = is_multiple_source


class MethodRpq:
    def __init__(self, method: Union[MethodTensor, MethodBfs]):
        self.method = method


def rpq(
    regex,
    graph,
    start_states: set = None,
    final_states: set = None,
    method_rpq: MethodRpq = MethodRpq(MethodTensor()),
) -> Union[set[tuple[Any, Any]], set]:
    bool_decomposed_aut1 = BoolDecomposedFA.from_fa(
        build_nfa_from_graph(graph, start_states, final_states)
    )
    bool_decomposed_aut2 = BoolDecomposedFA.from_fa(build_min_dfa_from_regex(regex))
    if isinstance(method_rpq.method, MethodTensor):
        result = TensorIntersection(bool_decomposed_aut1, bool_decomposed_aut2)
        result.intersect()
        result.transitive_closure()
        result.filter_starts_to_finals()
        return result.get_result()
    elif isinstance(method_rpq.method, MethodBfs):
        if method_rpq.method.is_multiple_source:
            result = BfsIntersectionMS(bool_decomposed_aut1, bool_decomposed_aut2)
            result.bfs_intersect()
            result.filter_starts_to_finals()
            return result.get_result()
        else:
            result = BfsIntersectionSet(bool_decomposed_aut1, bool_decomposed_aut2)
            result.bfs_intersect()
            result.filter_finals()
            return result.get_result()
    else:
        raise ValueError("In rpq() incorrect method_rpq")
