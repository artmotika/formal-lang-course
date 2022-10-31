from pathlib import Path
from typing import Union
from pyformlang.cfg.cfg import CFG, Variable


def cfg_from_file(
    file_path: Union[str, Path], start_symbol: Variable = Variable("S")
) -> CFG:
    with open(file_path, "r") as file:
        return CFG.from_text(file.read(), start_symbol=start_symbol)


def cfg_to_weakened_form_chomsky(cfg: CFG) -> CFG:
    new_cfg = cfg.remove_useless_symbols()
    new_productions = new_cfg._get_productions_with_only_single_terminals()
    new_productions = new_cfg._decompose_productions(new_productions)
    return CFG(start_symbol=new_cfg._start_symbol, productions=set(new_productions))
