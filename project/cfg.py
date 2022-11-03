from pathlib import Path
from typing import Union
from pyformlang.cfg.cfg import CFG, Variable


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
