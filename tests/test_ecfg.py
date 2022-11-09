from pyformlang.cfg.cfg import Variable
from project.ecfg import ECFG
from pyformlang.regular_expression.regex import Regex
from pyformlang.cfg import CFG


match_var_to_regex = {
    Variable("S"): Regex("(NP.VP)"),
    Variable("NP"): Regex("(georges|(Det.N))"),
    Variable("Det"): Regex("((a)*|the)"),
    Variable("N"): Regex("carrots"),
}

# test from pyfromlang cfg to ecfg
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
    actual_productions = ecfg.productions
    expected_productions_dict = dict()
    expected_productions_dict[Variable("Det")] = {
        Regex("a|the").get_tree_str(),
        Regex("the|a").get_tree_str(),
    }
    expected_productions_dict[Variable("VP")] = None
    expected_productions_dict[Variable("N")] = {Regex("carrots").get_tree_str()}
    expected_productions_dict[Variable("NP")] = {
        Regex("(Det.N)|georges").get_tree_str(),
        Regex("georges|(Det.N)").get_tree_str(),
    }
    expected_productions_dict[Variable("S")] = {Regex("NP.VP").get_tree_str()}

    results = []
    for k in expected_productions_dict.keys() | actual_productions.keys():
        actual_p = actual_productions.get(k)
        expected_p = expected_productions_dict.get(k)
        if actual_p is None:
            if expected_p is None:
                results.append(True)
            else:
                results.append(False)
        elif expected_p is None:
            results.append(False)
        else:
            results.append(actual_p.get_tree_str() in expected_p)

    assert all(
        (
            ecfg.start_symbol == cfg.start_symbol,
            all(tuple(results)),
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
                == match_var_to_regex.get(var).accepts(["NP", "VP"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["georges"])
                == match_var_to_regex.get(var).accepts(["georges"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["Det", "N"])
                == match_var_to_regex.get(var).accepts(["Det", "N"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["a*"])
                == match_var_to_regex.get(var).accepts(["a*"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["the"])
                == match_var_to_regex.get(var).accepts(["the"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["carrots"])
                == match_var_to_regex.get(var).accepts(["carrots"])
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
                == match_var_to_regex.get(var).accepts(["NP", "VP"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["georges"])
                == match_var_to_regex.get(var).accepts(["georges"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["Det", "N"])
                == match_var_to_regex.get(var).accepts(["Det", "N"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["a*"])
                == match_var_to_regex.get(var).accepts(["a*"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["the"])
                == match_var_to_regex.get(var).accepts(["the"])
                for var in productions.keys()
            ),
            all(
                productions.get(var).accepts(["carrots"])
                == match_var_to_regex.get(var).accepts(["carrots"])
                for var in productions.keys()
            ),
        )
    )
