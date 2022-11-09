from pyformlang.regular_expression.regex import Regex

from pyformlang.cfg.cfg import Variable


class ECFG:
    def __init__(
        self,
        start_symbol: Variable,
        productions: dict[Variable, Regex],
    ):
        self.start_symbol = start_symbol
        self.productions = productions

    @classmethod
    def from_pyfl_cfg(cls, cfg) -> "ECFG":
        productions = {var: None for var in cfg.variables}
        for p in cfg.productions:
            production = productions.get(p.head)
            body = p.body
            regex = ""
            for pb in body:
                regex += f"{pb.value} "
            if production is None:
                productions[p.head] = Regex(regex[:-1])
            else:
                productions[p.head] = production | Regex(regex[:-1])
        return cls(start_symbol=cfg.start_symbol, productions=productions)

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")) -> "ECFG":
        productions = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            head, body = line.split("->")
            productions[Variable(head.strip())] = Regex(body.strip())
        return cls(start_symbol=start_symbol, productions=productions)

    @classmethod
    def from_file(cls, file_path, start_symbol=Variable("S")) -> "ECFG":
        with open(file_path, "r") as file:
            ecfg = cls.from_text(file.read(), start_symbol)
        return ecfg
