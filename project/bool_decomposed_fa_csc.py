from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from scipy.sparse import csc_matrix
from scipy.sparse import kron
from pyformlang.finite_automaton import EpsilonNFA
from numpy import array


class BoolDecomposedFA:
    state_to_idx: dict[State, int]
    idx_to_state: dict[int, State]
    start_states: set[State]
    final_states: set[State]
    adjacency_matrices: dict[Symbol, csc_matrix]
    tensor_intersection_dict: dict[
        State, State
    ]  # Сопоставление состоянию из пересечения состояния из графа
    multiple_source_dict: dict[int, State]

    def __init__(
        self,
        state_to_idx: dict[State, int],
        idx_to_state: dict[int, State],
        start_states: set[State],
        final_states: set[State],
        adjacency_matrices: dict[Symbol, csc_matrix],
    ):
        self.state_to_idx = state_to_idx
        self.idx_to_state = idx_to_state
        self.start_states = start_states
        self.final_states = final_states
        self.adjacency_matrices = adjacency_matrices

    # fa from pyformlang
    @classmethod
    def from_fa(cls, fa: EpsilonNFA):
        state_to_idx, idx_to_state = {}, {}
        for idx, state in enumerate(fa.states.copy()):
            state_to_idx[state] = idx
            idx_to_state[idx] = state

        return cls(
            state_to_idx=state_to_idx,
            idx_to_state=idx_to_state,
            start_states=fa.start_states.copy(),
            final_states=fa.final_states.copy(),
            adjacency_matrices=cls.get_adjacency_matrices(fa, state_to_idx),
        )

    @staticmethod
    def get_adjacency_matrices(
        fa: EpsilonNFA, state_to_idx: dict[State, int]
    ) -> dict[Symbol, csc_matrix]:
        n = len(fa.states)
        symbols = fa.symbols.copy()
        symbols.add(Symbol("epsilon"))
        data = {symbol: [] for symbol in symbols}
        row = {symbol: [] for symbol in symbols}
        col = {symbol: [] for symbol in symbols}
        for (source, symbol, target) in fa:
            data_by_symbol = data.get(symbol)
            row_by_symbol = row.get(symbol)
            col_by_symbol = col.get(symbol)
            data_by_symbol.append(True)
            row_by_symbol.append(state_to_idx[source])
            col_by_symbol.append(state_to_idx[target])
            data[symbol] = data_by_symbol
            row[symbol] = row_by_symbol
            col[symbol] = col_by_symbol
        for state in fa.start_states:
            if state in fa.final_states:
                symbol = Symbol("epsilon")
                data_by_symbol = data.get(symbol)
                row_by_symbol = row.get(symbol)
                col_by_symbol = col.get(symbol)
                data_by_symbol.append(True)
                row_by_symbol.append(state_to_idx[state])
                col_by_symbol.append(state_to_idx[state])
                data[symbol] = data_by_symbol
                row[symbol] = row_by_symbol
                col[symbol] = col_by_symbol
        return {
            symbol: csc_matrix(
                (
                    array(data.get(symbol)),
                    (array(row.get(symbol)), array(col.get(symbol))),
                ),
                shape=(n, n),
                dtype=bool,
            )
            for symbol in symbols
        }

    def get_intersection(self, other: "BoolDecomposedFA") -> "BoolDecomposedFA":
        all_state_to_idx, all_idx_to_state = {}, {}
        inter_start_states, inter_final_states = set(), set()
        other_states = other.state_to_idx.keys()
        self.tensor_intersection_dict = {}
        for state1 in self.state_to_idx.keys():
            for state2 in other_states:
                state = State(str(state1.value) + ":" + str(state2.value))
                self.tensor_intersection_dict[state] = state1
                idx = self.state_to_idx.get(state1) * len(
                    other_states
                ) + other.state_to_idx.get(state2)
                all_state_to_idx[state] = idx
                all_idx_to_state[idx] = state
                if state1 in self.start_states and state2 in other.start_states:
                    inter_start_states.add(state)
                if state1 in self.final_states and state2 in other.final_states:
                    inter_final_states.add(state)

        inter_symbols = self.adjacency_matrices.keys() & other.adjacency_matrices.keys()
        inter_adjacency_matrices = {
            symbol: kron(
                self.adjacency_matrices.get(symbol),
                other.adjacency_matrices.get(symbol),
            ).tocsc()
            for symbol in inter_symbols
        }
        return BoolDecomposedFA(
            state_to_idx=all_state_to_idx,
            idx_to_state=all_idx_to_state,
            start_states=inter_start_states,
            final_states=inter_final_states,
            adjacency_matrices=inter_adjacency_matrices,
        )

    def to_fa(self) -> EpsilonNFA:
        enfa = EpsilonNFA(
            states=self.state_to_idx.keys(),
            start_state=self.start_states,
            final_states=self.final_states,
        )

        for symbol in self.adjacency_matrices.keys():
            enfa.add_transitions(
                [
                    (
                        self.idx_to_state.get(source),
                        symbol,
                        self.idx_to_state.get(target),
                    )
                    for source, target in zip(
                        *self.adjacency_matrices.get(symbol).nonzero()
                    )
                ]
            )
        return enfa

    def transitive_closure(self) -> csc_matrix:
        n = len(self.idx_to_state.keys())
        result = sum(
            self.adjacency_matrices.values(),
            start=csc_matrix((n, n)),
        )
        previous_not_zero = 0
        cur_not_zero = result.count_nonzero()
        while previous_not_zero != cur_not_zero:
            result += result @ result
            previous_not_zero = cur_not_zero
            cur_not_zero = result.count_nonzero()
        return result

    def get_bfs_intersection(
        self, other: "BoolDecomposedFA", is_multiple_source: bool = False
    ) -> csc_matrix:
        self_states = self.state_to_idx.keys()
        other_states = other.state_to_idx.keys()
        n_self = len(self_states)
        n_other = len(other_states)
        n_start_states_self = len(self.start_states)

        def get_ms_start_front() -> csc_matrix:
            data, row, col = [], [], []
            i = 0
            self.multiple_source_dict = {}
            for state_s in self.start_states:
                for state_o in other.start_states:
                    self.multiple_source_dict[i] = state_s
                    idx_other = other.state_to_idx.get(state_o)
                    idx_other_ms = other.state_to_idx.get(state_o) + n_other * i
                    i += 1
                    data.append(True)
                    row.append(idx_other_ms)
                    col.append(idx_other)
                    idx_self = self.state_to_idx.get(state_s)
                    data.append(True)
                    row.append(idx_other_ms)
                    col.append(idx_self + n_other)
            return csc_matrix(
                (
                    array(data),
                    (array(row), array(col)),
                ),
                shape=(n_other * i, n_other + n_self),
                dtype=bool,
            )

        def get_start_front() -> csc_matrix:
            data, row, col = [], [], []
            for state_o in other.start_states:
                idx_other = other.state_to_idx.get(state_o)
                data.append(True)
                row.append(idx_other)
                col.append(idx_other)
                for state_s in self.start_states:
                    idx_self = self.state_to_idx.get(state_s)
                    data.append(True)
                    row.append(idx_other)
                    col.append(idx_self + n_other)
            return csc_matrix(
                (
                    array(data),
                    (array(row), array(col)),
                ),
                shape=(n_other, n_other + n_self),
                dtype=bool,
            )

        def get_direct_sum(matrix1: csc_matrix, matrix2: csc_matrix) -> csc_matrix:
            data, row, col = [], [], []
            for i, j in zip(*matrix1.nonzero()):
                data.append(True)
                row.append(i)
                col.append(j)
            shape1 = matrix1.shape[0]
            shape2 = matrix2.shape[0]
            shape = shape1 + shape2
            for i, j in zip(*matrix2.nonzero()):
                data.append(True)
                row.append(i + shape1)
                col.append(j + shape1)
            return csc_matrix(
                (
                    array(data),
                    (array(row), array(col)),
                ),
                shape=(shape, shape),
                dtype=bool,
            )

        def get_submatrix(
            matrix: csc_matrix, range1: tuple, range2: tuple
        ) -> csc_matrix:
            data, row, col = [], [], []
            shape1 = range1[1] - range1[0]
            shape2 = range2[1] - range2[0]
            for i, j in zip(*matrix.nonzero()):
                if range1[0] <= i < range1[1] and range2[0] <= j < range2[1]:
                    data.append(True)
                    row.append(i - range1[0])
                    col.append(j - range2[0])
            return csc_matrix(
                (
                    array(data),
                    (array(row), array(col)),
                ),
                shape=(shape1, shape2),
                dtype=bool,
            )

        def transform_rows(
            matrix: csc_matrix, is_ms: bool = is_multiple_source
        ) -> csc_matrix:
            count_f = 2
            if is_ms:
                count_f = n_start_states_self + 1
            data, row, col = [], [], []
            for c in range(1, count_f):
                for i, j in zip(*matrix.nonzero()):
                    if n_other * (c - 1) <= i < n_other * c and 0 <= j < n_other:
                        for k, l in zip(*matrix.nonzero()):
                            if k == i and n_other <= l < n_self + n_other:
                                data.append(True)
                                row.append(n_other * (c - 1) + j)
                                col.append(j)
                                data.append(True)
                                row.append(n_other * (c - 1) + j)
                                col.append(l)
            return csc_matrix(
                (
                    array(data),
                    (array(row), array(col)),
                ),
                shape=matrix.shape,
                dtype=bool,
            )

        if is_multiple_source:
            front = get_ms_start_front()
            cur_visited = front.copy()
            previous_visited = cur_visited.copy()
            while True:
                new_front = csc_matrix(
                    (n_other * n_start_states_self, n_other + n_self), dtype=bool
                )
                inter_symbols = set(other.adjacency_matrices.keys()).intersection(
                    self.adjacency_matrices.keys()
                )
                for symbol in inter_symbols:
                    next_front = front @ get_direct_sum(
                        other.adjacency_matrices.get(symbol),
                        self.adjacency_matrices.get(symbol),
                    )
                    transformed_next_front = transform_rows(next_front)
                    new_front = new_front + transformed_next_front
                front = new_front.copy()
                cur_visited = cur_visited + front
                if cur_visited.count_nonzero() <= previous_visited.count_nonzero():
                    break
                previous_visited = cur_visited.copy()
            return get_submatrix(
                cur_visited,
                (0, n_other * n_start_states_self),
                (n_other, n_self + n_other),
            )
        else:
            front = get_start_front()
            cur_visited = front.copy()
            previous_visited = cur_visited.copy()
            while True:
                new_front = csc_matrix((n_other, n_other + n_self), dtype=bool)
                inter_symbols = set(other.adjacency_matrices.keys()).intersection(
                    self.adjacency_matrices.keys()
                )
                for symbol in inter_symbols:
                    next_front = front @ get_direct_sum(
                        other.adjacency_matrices.get(symbol),
                        self.adjacency_matrices.get(symbol),
                    )
                    transformed_next_front = transform_rows(next_front)
                    new_front = new_front + transformed_next_front
                front = new_front.copy()
                cur_visited = cur_visited + front
                if cur_visited.count_nonzero() <= previous_visited.count_nonzero():
                    break
                previous_visited = cur_visited.copy()
            return get_submatrix(cur_visited, (0, n_other), (n_other, n_self + n_other))
