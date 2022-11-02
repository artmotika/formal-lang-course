from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State, Symbol

from project.rsm import RSM
from pyformlang.cfg.cfg import CFG, Variable, Production


class ECFG:
    def __init__(
        self,
        start_symbol: Variable,
        productions: set[Production],
    ):
        self.start_symbol = start_symbol
        self.productions = productions

    @classmethod
    def from_pyfl_cfg(cls, cfg) -> "ECFG":
        return cls(start_symbol=cfg.start_symbol, productions=cfg.productions)

    # @classmethod
    # def from_text(cls, text, start_symbol=Variable("S")) -> "ECFG":
    #     return cls()
    #
    # @classmethod
    # def from_file(cls, file_path, start_symbol=Variable("S")) -> "ECFG":
    #     return cls()

    def to_rsm(self) -> RSM:
        modules = {p.head: EpsilonNFA(start_state={State(0)}) for p in self.productions}
        for p in self.productions:
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
        return RSM(start_module=self.start_symbol, modules=modules)

    # def to_pyfl_cfg(self) -> CFG:
    #     return CFG()
    #
    # def to_text(self) -> str:
    #     return ""
