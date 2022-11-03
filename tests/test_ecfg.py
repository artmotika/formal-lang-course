from pyformlang.cfg.cfg import Variable
from project.ecfg import ECFG
from pyformlang.regular_expression.regex import Regex
from pyformlang.cfg import CFG
from typing import Union


def match_var_to_regex(var: Variable) -> Union[Regex, None]:
    if var == Variable("S"):
        return Regex("(NP.VP)")
    elif var == Variable("NP"):
        return Regex("(georges|(Det.N))")
    elif var == Variable("Det"):
        return Regex("((a)*|the)")
    elif var == Variable("N"):
        return Regex("carrots")
    return None


def test_from_pyfl_cfg():
    cfg = CFG.from_text(
        """
            S -> NP VP
            NP -> georges | Det N
            Det -> a | the
            N -> carrots""",
        start_symbol=Variable("NP"),
    )

    ecfg = ECFG.from_pyfl_cfg(cfg)
    expended_productions = ecfg.productions
    expected_productions_str_set = set()
    for var in expended_productions.keys():
        expected_productions_str_set.add(f"{var} -> {ecfg.productions[var]}")
    actual_productions_str_set1 = set()
    actual_productions_str_set1.add("Det -> (the|a)")
    actual_productions_str_set1.add("VP -> None")
    actual_productions_str_set1.add("N -> carrots")
    actual_productions_str_set1.add("NP -> (georges|(Det.N))")
    actual_productions_str_set1.add("S -> (NP.VP)")

    actual_productions_str_set2 = set()
    actual_productions_str_set2.add("Det -> (a|the)")
    actual_productions_str_set2.add("VP -> None")
    actual_productions_str_set2.add("N -> carrots")
    actual_productions_str_set2.add("NP -> ((Det.N)|georges)")
    actual_productions_str_set2.add("S -> (NP.VP)")

    actual_productions_str_set3 = set()
    actual_productions_str_set3.add("Det -> (a|the)")
    actual_productions_str_set3.add("VP -> None")
    actual_productions_str_set3.add("N -> carrots")
    actual_productions_str_set3.add("NP -> (georges|(Det.N))")
    actual_productions_str_set3.add("S -> (NP.VP)")

    actual_productions_str_set4 = set()
    actual_productions_str_set4.add("Det -> (the|a)")
    actual_productions_str_set4.add("VP -> None")
    actual_productions_str_set4.add("N -> carrots")
    actual_productions_str_set4.add("NP -> ((Det.N)|georges)")
    actual_productions_str_set4.add("S -> (NP.VP)")

    assert all(
        (
            ecfg.start_symbol == cfg.start_symbol,
            expected_productions_str_set == actual_productions_str_set1
            or expected_productions_str_set == actual_productions_str_set2
            or expected_productions_str_set == actual_productions_str_set3
            or expected_productions_str_set == actual_productions_str_set4,
        )
    )


def test_from_text():
    ecfg = ECFG.from_text(
        """
            S -> NP VP
            NP -> georges | Det N
            Det -> a* | the
            N -> carrots""",
        start_symbol=Variable("NP"),
    )
    productions = ecfg.productions

    assert all(
        (
            ecfg.start_symbol == Variable("NP"),
            all(
                productions.get(var).accepts(["NP", "VP"])
                == match_var_to_regex(var).accepts(["NP", "VP"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["georges"])
                == match_var_to_regex(var).accepts(["georges"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["Det", "N"])
                == match_var_to_regex(var).accepts(["Det", "N"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["a*"])
                == match_var_to_regex(var).accepts(["a*"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["the"])
                == match_var_to_regex(var).accepts(["the"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["carrots"])
                == match_var_to_regex(var).accepts(["carrots"])
                for var in productions.keys()
            ),
        )
    )


def test_from_file(tmp_path):
    actual_file_path = tmp_path / "actual_test_ecfg.txt"
    with open(actual_file_path, "w") as file:
        file.write(
            """
            S -> NP VP
            NP -> georges | Det N
            Det -> a* | the
            N -> carrots"""
        )

    ecfg = ECFG.from_file(actual_file_path, start_symbol=Variable("NP"))
    productions = ecfg.productions

    assert all(
        (
            ecfg.start_symbol == Variable("NP"),
            all(
                productions.get(var).accepts(["NP", "VP"])
                == match_var_to_regex(var).accepts(["NP", "VP"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["georges"])
                == match_var_to_regex(var).accepts(["georges"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["Det", "N"])
                == match_var_to_regex(var).accepts(["Det", "N"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["a*"])
                == match_var_to_regex(var).accepts(["a*"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["the"])
                == match_var_to_regex(var).accepts(["the"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["carrots"])
                == match_var_to_regex(var).accepts(["carrots"])
                for var in productions.keys()
            ),
        )
    )
