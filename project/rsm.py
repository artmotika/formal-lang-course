from collections import deque

from pyformlang.cfg.cfg import CFG, Variable
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State, Symbol


class RSM:
    def __init__(
        self,
        start_module: Variable,
        modules: dict[Variable, EpsilonNFA],
    ):
        self.start_module = start_module
        self.modules = modules
        self.stack = deque[tuple[Variable, State]]()

    # def to_ecfg(self) -> ECFG:
    #     return ECFG()
    #
    # def to_pyfl_cfg(self) -> CFG:
    #     return CFG()

    @classmethod
    def from_pyfl_cfg(cls, cfg) -> "RSM":
        modules = {p.head: EpsilonNFA(start_state={State(0)}) for p in cfg.productions}
        for p in cfg.productions:
            nfa = modules.get(p.head)
            body = p.body
            body_length = len(body)
            nfa.add_final_state(State(body_length))
            for cfg_obj_ind in range(body_length):
                nfa.add_transition(
                    State(cfg_obj_ind),
                    Symbol(body[cfg_obj_ind]),
                    State(cfg_obj_ind + 1),
                )
        return cls(start_module=cfg.start_symbol, modules=modules)

    def minimize(self) -> "RSM":
        new_modules = {
            var: self.modules.get(var).minimize() for var in self.modules.keys()
        }
        return RSM(self.start_module, new_modules)
