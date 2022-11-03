from project.cfg import cfg_from_file
from project.cfg import cfg_to_weakened_form_chomsky
from pyformlang.cfg.cfg import CFG, Variable, Terminal, Production, Epsilon


def test_cfg_from_file(tmp_path):
    actual_file_path = tmp_path / "actual_test_cfg.txt"
    expected_cfg = CFG(
        start_symbol=Variable("S"),
        productions={
            Production(
                Variable("S"),
                [Terminal("a"), Variable("S"), Terminal("b"), Variable("S")],
            ),
            Production(Variable("S"), [Epsilon()]),
        },
    )
    with open(actual_file_path, "w") as file:
        file.write("S -> a S b S | ε")
    actual_cfg = cfg_from_file(actual_file_path)
    assert all(
        (
            actual_cfg.start_symbol == expected_cfg.start_symbol,
            actual_cfg.productions == expected_cfg.productions,
        )
    )


def test_cfg_to_weakened_form_chomsky():
    cfg = CFG.from_text(
        """S -> a S b S | ε | N
    N -> c
    """
    )
    actual_cfg = cfg_to_weakened_form_chomsky(cfg)
    expected_cfg = CFG(
        start_symbol=Variable("S"),
        productions={
            Production(Variable("a#CNF#"), [Terminal("a")]),
            Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
            Production(Variable("S"), [Epsilon()]),
            Production(Variable("C#CNF#1"), [Variable("S"), Variable("C#CNF#2")]),
            Production(Variable("b#CNF#"), [Terminal("b")]),
            Production(Variable("C#CNF#2"), [Variable("b#CNF#"), Variable("S")]),
            Production(Variable("S"), [Terminal("c")]),
        },
    )
    assert all(
        (
            actual_cfg.start_symbol == expected_cfg.start_symbol,
            actual_cfg.productions == expected_cfg.productions,
        )
    )
