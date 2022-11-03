from pyformlang.cfg.cfg import Variable
from pyformlang.finite_automaton import State, EpsilonNFA, Symbol
from project.ecfg import ECFG
from project.rsm import RSM
from pyformlang.regular_expression.regex import Regex

expected_productions = set()
expected_start_states_dict = {}
expected_final_states_dict = {}
expected_productions.add("NP:   6;7 - N -> 1;3;1;5")
expected_productions.add("NP:   0;2;4 - georges -> 1;3;1;5")
expected_productions.add("NP:   0;2;4 - Det -> 6;7")
expected_productions.add("N:   0 - carrots -> 1")
expected_productions.add("S:   2;3 - VP -> 1")
expected_productions.add("Det:   0;1;2;3;4;6 - the -> 1;7")
expected_productions.add("Det:   1;3;4;5 - a -> 1;3;4;5")
expected_productions.add("Det:   0;1;2;3;4;6 - a -> 1;3;4;5")
expected_productions.add("S:   0 - NP -> 2;3")
expected_start_states_dict[Variable("NP")] = {State("0;2;4")}
expected_final_states_dict[Variable("NP")] = {State("1;3;1;5")}
expected_start_states_dict[Variable("N")] = {State("0")}
expected_final_states_dict[Variable("N")] = {State("1")}
expected_start_states_dict[Variable("S")] = {State("0")}
expected_final_states_dict[Variable("S")] = {State("1")}
expected_start_states_dict[Variable("Det")] = {State("0;1;2;3;4;6")}
expected_final_states_dict[Variable("Det")] = {
    State("0;1;2;3;4;6"),
    State("1;7"),
    State("1;3;4;5"),
}


def get_test_rsm():
    modules = {}
    enfa = EpsilonNFA(start_state={State("0;0")}, final_states={State("3;0")})
    enfa.add_transitions(
        [
            (State("0;0"), Symbol("a"), State("1;0")),
            (State("0;0"), Symbol("a"), State("1;1")),
            (State("1;0"), Symbol("A"), State("2;0")),
            (State("1;1"), Symbol("B"), State("2;1")),
            (State("2;0"), Symbol("b"), State("3;0")),
            (State("2;1"), Symbol("b"), State("3;0")),
        ]
    )
    modules[Variable("A")] = enfa
    enfa = EpsilonNFA(start_state={State("0;0")}, final_states={State("1;0")})
    enfa.add_transitions([(State("0;0"), Symbol("c"), State("1;0"))])
    modules[Variable("B")] = enfa
    return RSM(start_module=Variable("A"), modules=modules)


def test_from_ecfg():
    ecfg = ECFG.from_text(
        """
        S -> NP VP
        NP -> georges | Det N
        Det -> a* | the
        N -> carrots"""
    )
    rsm = RSM.from_ecfg(ecfg)
    actual_productions = set()
    actual_start_states_dict = {}
    actual_final_states_dict = {}
    modules = rsm.modules
    for var in modules.keys():
        for x, y, z in modules.get(var):
            actual_productions.add(f"{var}:   {x} - {y} -> {z}")
            actual_start_states_dict[var] = modules.get(var).start_states
            actual_final_states_dict[var] = modules.get(var).final_states

    assert all(
        (
            rsm.start_module == Variable("S"),
            actual_productions == expected_productions,
            all(
                (
                    actual_start_states_dict.get(var)
                    == expected_start_states_dict.get(var)
                    for var in modules.keys()
                )
            ),
            all(
                (
                    actual_final_states_dict.get(var)
                    == expected_final_states_dict.get(var)
                    for var in modules.keys()
                )
            ),
        )
    )


def test_to_ecfg():
    rsm = get_test_rsm()
    actual_ecfg = rsm.to_ecfg()
    expected_productions = {}
    expected_productions[Variable("A")] = Regex("(a.B.b) | (a.A.b)")
    expected_productions[Variable("B")] = Regex("c")
    actual_productions = actual_ecfg.productions

    assert all(
        (
            actual_ecfg.start_symbol == Variable("A"),
            all(
                (
                    actual_productions.get(var).accepts(["a", "B", "b"])
                    == expected_productions.get(var).accepts(["a", "B", "b"])
                    for var in (actual_productions.keys() | expected_productions.keys())
                )
            ),
            all(
                (
                    actual_productions.get(var).accepts([("c")])
                    == expected_productions.get(var).accepts([("c")])
                    for var in (actual_productions.keys() | expected_productions.keys())
                )
            ),
            all(
                (
                    actual_productions.get(var).accepts(["a", "A", "b"])
                    == expected_productions.get(var).accepts(["a", "A", "b"])
                    for var in (actual_productions.keys() | expected_productions.keys())
                )
            ),
        )
    )
