from pyformlang.finite_automaton import State
from typing import Any
from scipy.sparse import csr_array
from pyformlang.finite_automaton import EpsilonNFA


class BoolDecomposedFA:
    state_to_idx: dict[State, int]
    start_states: set[State]
    final_states: set[State]
    b_mtx: dict[Any, csr_array]

    def __init__(
        self,
        state_to_idx: dict[State, int],
        start_states: set[State],
        final_states: set[State],
        b_mtx: dict[Any, csr_array],
    ):
        self.state_to_idx = state_to_idx
        self.start_states = start_states
        self.final_states = final_states
        self.b_mtx = b_mtx

    # fa from pyformlang
    def from_fa(fa: EpsilonNFA):
        state_to_idx = {state: idx for idx, state in enumerate(fa.states)}
        return BoolDecomposedFA(
            state_to_idx=state_to_idx,
            start_states=fa.start_states.copy(),
            final_states=fa.final_states.copy(),
            b_mtx=dict(),
        )
