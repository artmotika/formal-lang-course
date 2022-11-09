from pathlib import Path
from typing import Union
from pyformlang.cfg.cfg import CFG, Variable, Terminal
from numpy import ndarray


def cfg_from_file(
    file_path: Union[str, Path], start_symbol: Variable = Variable("S")
) -> CFG:
    with open(file_path, "r") as file:
        return CFG.from_text(file.read(), start_symbol=start_symbol)


def cfg_to_weakened_form_chomsky(cfg: CFG) -> CFG:
    # unit production: S -> N ; N -> a
    # eliminated unit production: S -> a
    cfg_eliminated_unit_productions = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    # get_productions_with_only_single_terminals() is transforming all productions to looks like S -> ε or S -> a or S -> N1 .. Nn
    new_productions = (
        cfg_eliminated_unit_productions._get_productions_with_only_single_terminals()
    )
    # decompose_productions() is transforming productions with length more than 2 to productions with length 2
    new_productions = cfg_eliminated_unit_productions._decompose_productions(
        new_productions
    )
    return CFG(
        start_symbol=cfg_eliminated_unit_productions._start_symbol,
        productions=set(new_productions),
    )


def cfg_accepts_word(cfg: CFG, word: str) -> bool:
    n = len(word)
    if n == 0:
        return cfg.generate_epsilon()

    # init 3dmatrix
    cfg = cfg.to_normal_form()
    N = len(cfg.variables)
    var_to_int = {var: num for num, var in enumerate(cfg.variables)}
    dp = ndarray(shape=(n, n, N), dtype=bool)

    for i in range(n):
        for j in range(n):
            for k in range(N):
                dp[i, j, k] = False

    for p in cfg.productions:
        if len(p.body) == 1:
            pb = p.body[0]
            if isinstance(pb, Terminal):
                terminal = pb.value
                for i in range(n):
                    if terminal == word[i]:
                        dp[i, i, var_to_int.get(p.head)] = True

    # cyk algorithm
    for m in range(1, n):
        for i in range(n - m):
            for p in cfg.productions:
                if len(p.body) == 2:
                    for k in range(i, i + m):
                        if (
                            dp[i, k, var_to_int.get(p.body[0])]
                            and dp[k + 1, i + m, var_to_int.get(p.body[1])]
                        ):
                            dp[i, i + m, var_to_int.get(p.head)] = True
                            continue

    return dp[0, n - 1, var_to_int.get(cfg.start_symbol)]
