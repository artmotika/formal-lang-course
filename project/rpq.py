from project.automata import build_nfa_from_graph
from project.automata import build_min_dfa_from_regex
from project.bool_decomposed_fa_csr import BoolDecomposedFA
from typing import Any
from typing import Union
from project.bool_decomposed_intersection_csr import (
    TensorIntersectionCsr,
    BfsIntersectionCsrMS,
    BfsIntersectionCsrSS,
)

from project.bool_decomposed_intersection_csc import (
    TensorIntersectionCsc,
    BfsIntersectionCscMS,
    BfsIntersectionCscSS,
)


class MethodTensor:
    pass


class MethodBfs:
    def __init__(self, is_single_source):
        self.is_single_source = is_single_source


class MethodRpq:
    def __init__(self, method: Union[MethodTensor, MethodBfs]):
        self.method = method


def rpq(
    regex,
    graph,
    start_states: set = None,
    final_states: set = None,
    method_rpq: MethodRpq = MethodRpq(MethodTensor()),
    csr: bool = True,
) -> Union[set[tuple[Any, Any]], set]:
    bool_decomposed_aut1 = BoolDecomposedFA.from_fa(
        build_nfa_from_graph(graph, start_states, final_states)
    )
    bool_decomposed_aut2 = BoolDecomposedFA.from_fa(build_min_dfa_from_regex(regex))
    if csr:
        if isinstance(method_rpq.method, MethodTensor):
            result = TensorIntersectionCsr(bool_decomposed_aut1, bool_decomposed_aut2)
            result.intersect()
            result.transitive_closure()
            result.filter_starts_to_finals()
            return result.get_result()
        elif isinstance(method_rpq.method, MethodBfs):
            if method_rpq.method.is_single_source:
                result = BfsIntersectionCsrSS(
                    bool_decomposed_aut1, bool_decomposed_aut2
                )
                result.bfs_intersect()
                result.filter_starts_to_finals()
                return result.get_result()
            else:
                result = BfsIntersectionCsrMS(
                    bool_decomposed_aut1, bool_decomposed_aut2
                )
                result.bfs_intersect()
                result.filter_finals()
                return result.get_result()

        else:
            raise ValueError("In rpq() incorrect method_rpq")
    else:
        if isinstance(method_rpq.method, MethodTensor):
            result = TensorIntersectionCsc(bool_decomposed_aut1, bool_decomposed_aut2)
            result.intersect()
            result.transitive_closure()
            result.filter_starts_to_finals()
            return result.get_result()
        elif isinstance(method_rpq.method, MethodBfs):
            if method_rpq.method.is_single_source:
                result = BfsIntersectionCscSS(
                    bool_decomposed_aut1, bool_decomposed_aut2
                )
                result.bfs_intersect()
                result.filter_starts_to_finals()
                return result.get_result()
            else:
                result = BfsIntersectionCscMS(
                    bool_decomposed_aut1, bool_decomposed_aut2
                )
                result.bfs_intersect()
                result.filter_finals()
                return result.get_result()

        else:
            raise ValueError("In rpq() incorrect method_rpq")
