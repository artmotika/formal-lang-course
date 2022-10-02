from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from scipy.sparse import csr_matrix
from scipy.sparse import kron
from pyformlang.finite_automaton import EpsilonNFA
from numpy import array


class BoolDecomposedFA:
    state_to_idx: dict[State, int]
    idx_to_state: dict[int, State]
    start_states: set[State]
    final_states: set[State]
    adjacency_matrices: dict[Symbol, csr_matrix]

    def __init__(
        self,
        state_to_idx: dict[State, int],
        idx_to_state: dict[int, State],
        start_states: set[State],
        final_states: set[State],
        adjacency_matrices: dict[Symbol, csr_matrix],
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
    ) -> dict[Symbol, csr_matrix]:
        n = len(fa.states)
        data = {symbol: [] for symbol in fa.symbols}
        row = {symbol: [] for symbol in fa.symbols}
        col = {symbol: [] for symbol in fa.symbols}
        for (source, symbol, target) in fa:
            data_by_symbol = data.get(symbol)
            row_by_symbol = row.get(symbol)
            col_by_symbol = col.get(symbol)
            data_by_symbol.append(1)
            row_by_symbol.append(state_to_idx[source])
            col_by_symbol.append(state_to_idx[target])
            data[symbol] = data_by_symbol
            row[symbol] = row_by_symbol
            col[symbol] = col_by_symbol
        return {
            symbol: csr_matrix(
                (
                    array(data.get(symbol)),
                    (array(row.get(symbol)), array(col.get(symbol))),
                ),
                shape=(n, n),
                dtype=int,
            )
            for symbol in fa.symbols
        }

    def get_intersection(self, other: "BoolDecomposedFA") -> "BoolDecomposedFA":
        all_state_to_idx, all_idx_to_state = {}, {}
        inter_start_states, inter_final_states = set(), set()
        other_states = other.state_to_idx.keys()
        for state1 in self.state_to_idx.keys():
            for state2 in other_states:
                state = State(str(state1.value) + ":" + str(state2.value))
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
            )
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

    def transitive_closure(self) -> csr_matrix:
        n = len(self.idx_to_state.keys())
        result = sum(
            self.adjacency_matrices.values(),
            start=csr_matrix((n, n)),
        )
        previous_not_zero = 0
        cur_not_zero = result.count_nonzero()
        while previous_not_zero != cur_not_zero:
            result += result @ result
            previous_not_zero = cur_not_zero
            cur_not_zero = result.count_nonzero()
        return result

    def bfs(self, start_states_bfs: set[State] = None, is_whole_set: bool = True):

        if start_states_bfs is None:
            start_states_bfs = self.start_states.copy()

        data, row, col = [], [], []
        self_states = self.state_to_idx.keys()
        n = len(self_states)

        adjacency_matrix = sum(
            self.adjacency_matrices.values(),
            start=csr_matrix((n, n)),
        )

        for state in self.state_to_idx.keys():
            if state in start_states_bfs:
                data.append(1)
                row.append(0)
                col.append(self.state_to_idx.get(state))

        if is_whole_set:
            vertecies_vector = csr_matrix(
                (
                    array(data),
                    (array(row), array(col)),
                ),
                shape=(1, n),
                dtype=int,
            )
            visited_vertex_idx = {}
            visited_vertex_idx.update(col)
            previous_num_visited = 0
            cur_num_visited = len(visited_vertex_idx)
            while cur_num_visited != previous_num_visited:
                previous_num_visited = len(visited_vertex_idx)
                next_vertecies = vertecies_vector @ adjacency_matrix
                visited_vertex_idx.update(next_vertecies.nonzero()[1].tolist())
                cur_num_visited = len(visited_vertex_idx)
            return {self.idx_to_state.get(idx) for idx in visited_vertex_idx}
        else:
            result = {state: {} for state in start_states_bfs}
            for state in start_states_bfs:
                idx_state = self.state_to_idx.get(state)
                if idx_state is None:
                    continue
                vertex_vector = csr_matrix(
                    (
                        array([1]),
                        (array([0]), array([idx_state])),
                    ),
                    shape=(1, len(self_states)),
                    dtype=int,
                )
                visited_vertex_idx = {idx_state}
                previous_num_visited = 0
                cur_num_visited = 1
                while cur_num_visited != previous_num_visited:
                    previous_num_visited = len(visited_vertex_idx)
                    next_vertecies = vertex_vector @ adjacency_matrix
                    visited_vertex_idx.update(next_vertecies.nonzero()[1].tolist())
                    cur_num_visited = len(visited_vertex_idx)
                result[state] = {
                    self.idx_to_state.get(idx) for idx in visited_vertex_idx
                }
            return result
