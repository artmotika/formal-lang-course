from project.automata import build_nfa_from_graph
from project.automata import build_min_dfa_from_regex
from project.bool_decomposed_fa import BoolDecomposedFA
from typing import Any
from scipy.sparse import csr_matrix
from typing import Union


class TensorIntersection:
    __intersection: BoolDecomposedFA
    __path_matrix: csr_matrix
    __result: set[tuple[Any, Any]]

    def __init__(
        self,
        bool_decomposed_aut1: BoolDecomposedFA,
        bool_decomposed_aut2: BoolDecomposedFA,
    ):
        self.bool_decomposed_aut1 = bool_decomposed_aut1
        self.bool_decomposed_aut2 = bool_decomposed_aut2

    def intersect(self):
        self.__intersection = self.bool_decomposed_aut1.get_intersection(
            self.bool_decomposed_aut2
        )

    def transitive_closure(self):
        if self.__intersection is None:
            raise ValueError(
                "In TensorIntersection intersection is None. Maybe intersect wasn't done before transitive_closure"
            )
        self.__path_matrix = self.__intersection.transitive_closure()

    def filter_starts_to_finals(self):
        if self.__path_matrix is None:
            raise ValueError(
                "In TensorIntersection path_matrix is None. Maybe transitive_closure wasn't done before filter_starts_to_finals"
            )
        result = set()
        for source, target in zip(*self.__path_matrix.nonzero()):
            state_source = self.__intersection.idx_to_state.get(source)
            state_target = self.__intersection.idx_to_state.get(target)
            if (
                state_source in self.__intersection.start_states
                and state_target in self.__intersection.final_states
            ):
                result.add(
                    (
                        self.bool_decomposed_aut1.tensor_intersection_dict.get(
                            state_source
                        ).value,
                        self.bool_decomposed_aut1.tensor_intersection_dict.get(
                            state_target
                        ).value,
                    )
                )
        self.__result = result

    def get_result(self) -> set[tuple[Any, Any]]:
        return self.__result


class BfsIntersection:
    _path_matrix: csr_matrix
    _result: Union[set, set[tuple[Any, Any]]]

    def __init__(
        self,
        bool_decomposed_aut1: BoolDecomposedFA,
        bool_decomposed_aut2: BoolDecomposedFA,
    ):
        self.bool_decomposed_aut1 = bool_decomposed_aut1
        self.bool_decomposed_aut2 = bool_decomposed_aut2

    def get_result(self) -> Union[set, set[tuple[Any, Any]]]:
        return self._result


class BfsIntersectionSet(BfsIntersection):
    def bfs_intersect(self):
        self._path_matrix = self.bool_decomposed_aut1.get_bfs_intersection(
            self.bool_decomposed_aut2,
            is_multiple_source=False,
        )

    def filter_finals(self):
        if self._path_matrix is None:
            raise ValueError(
                "In BfsIntersectionSet path_matrix is None. Maybe bfs_intersect wasn't done before filter_finals"
            )
        result = set()
        for i, j in zip(*self._path_matrix.nonzero()):
            aut2_state = self.bool_decomposed_aut2.idx_to_state.get(i)
            aut1_state = self.bool_decomposed_aut1.idx_to_state.get(j)
            if (
                aut2_state in self.bool_decomposed_aut2.final_states
                and aut1_state in self.bool_decomposed_aut1.final_states
            ):
                result.add(aut1_state.value)
        self._result = result


class BfsIntersectionMS(BfsIntersection):
    def bfs_intersect(self):
        self._path_matrix = self.bool_decomposed_aut1.get_bfs_intersection(
            self.bool_decomposed_aut2,
            is_multiple_source=True,
        )

    def filter_starts_to_finals(self):
        if self._path_matrix is None:
            raise ValueError(
                "In BfsIntersectionMS path_matrix is None. Maybe bfs_intersect wasn't done before filter_starts_to_finals"
            )
        result = set()
        n_states_aut2 = len(self.bool_decomposed_aut2.state_to_idx.keys())
        for i, j in zip(*self._path_matrix.nonzero()):
            aut2_state = self.bool_decomposed_aut2.idx_to_state.get(i % n_states_aut2)
            aut1_state = self.bool_decomposed_aut1.idx_to_state.get(j)
            if (
                aut2_state in self.bool_decomposed_aut2.final_states
                and aut1_state in self.bool_decomposed_aut1.final_states
            ):
                result.add(
                    (
                        self.bool_decomposed_aut1.multiple_source_dict.get(
                            i // n_states_aut2
                        ).value,
                        aut1_state.value,
                    )
                )
        self._result = result


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
