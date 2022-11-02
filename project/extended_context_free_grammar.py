from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State, Symbol

from project.rsm import RSM
from pyformlang.cfg.cfg import CFG, Variable, Production
from pyformlang.cfg.cfg_object import CFGObject


class ECFG:
    def __init__(
        self,
        start_symbol: Variable,
        productions: dict[Variable, list[list[CFGObject]]],
    ):
        self.start_symbol = start_symbol
        self.productions = productions

    @classmethod
    def from_pyfl_cfg(cls, cfg) -> "ECFG":
        productions = {var: [] for var in cfg.variables}
        for p in cfg.productions:
            list_productions = productions.get(p.head)
            list_productions.append(p.body)
            productions[p.head] = list_productions
        return cls(start_symbol=cfg.start_symbol, productions=productions)

    # @classmethod
    # def from_text(cls, text, start_symbol=Variable("S")) -> "ECFG":
    #     return cls()
    #
    # @classmethod
    # def from_file(cls, file_path, start_symbol=Variable("S")) -> "ECFG":
    #     return cls()

    def to_rsm(self) -> RSM:
        modules = {}
        productions = self.productions.copy()
        for p in productions.keys():
            nfa = EpsilonNFA(start_state={State(0)})
            production = productions.get(p)
            for b in production:
                body_length = len(b)
                nfa.add_final_state(State(body_length))
                for cfg_obj_ind in range(body_length):
                    nfa.add_transition(
                        State(cfg_obj_ind),
                        Symbol(b[cfg_obj_ind]),
                        State(cfg_obj_ind + 1),
                    )
            modules[p] = nfa
        return RSM(start_module=self.start_symbol, modules=modules)

    # def to_pyfl_cfg(self) -> CFG:
    #     return CFG()
    #
    # def to_text(self) -> str:
    #     return ""
