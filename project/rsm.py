from collections import deque

from pyformlang.cfg.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA, State

from project.ecfg import ECFG


class RSM:
    def __init__(
        self,
        start_module: Variable,
        modules: dict[Variable, EpsilonNFA],
    ):
        self.start_module = start_module
        self.modules = modules
        self.stack = deque[tuple[Variable, State]]()

    @classmethod
    def from_ecfg(cls, ecfg) -> "RSM":
        modules = {}
        productions = ecfg.productions
        for var in productions.keys():
            production = productions.get(var)
            if production is not None:
                modules[var] = production.to_epsilon_nfa().minimize()
        return cls(start_module=ecfg.start_symbol, modules=modules)

    def to_ecfg(self) -> ECFG:
        productions = {}
        modules = self.modules
        for var in modules.keys():
            productions[var] = modules.get(var).to_regex()
        return ECFG(start_symbol=self.start_module, productions=productions)

    def minimize(self) -> "RSM":
        new_modules = {
            var: self.modules.get(var).minimize() for var in self.modules.keys()
        }
        return RSM(self.start_module, new_modules)
