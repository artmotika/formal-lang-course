from networkx.drawing.nx_pydot import read_dot
from networkx.classes.multidigraph import MultiDiGraph
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.regular_expression import Regex
from project.BoolDecomposedFA import BoolDecomposedFA

# Builds minimal dfa from given regex with rules from pyformlang.regular_expression
def build_min_dfa_from_regex(regex_string):
    return Regex(regex_string).to_epsilon_nfa().minimize()


# Builds nfa from given graph whether it's a networkx graph or the path to the dot file
def build_nfa_from_graph(graph, start_states: set = None, final_states: set = None):
    multi_di_graph = graph if isinstance(graph, MultiDiGraph) else read_dot(graph)

    enfa = EpsilonNFA(
        states={State(state) for state in multi_di_graph.nodes},
        start_state={State(state) for state in multi_di_graph.nodes}
        if start_states is None
        else start_states,
        final_states={State(state) for state in multi_di_graph.nodes}
        if final_states is None
        else final_states,
    )

    enfa.add_transitions(
        [
            (State(state1), Symbol(symbol["label"]), State(state2))
            for (state1, state2, symbol) in multi_di_graph.edges(data=True)
        ]
    )
    return enfa


def cross_two_automata(aut1, aut2):
    return (
        BoolDecomposedFA.from_fa(aut1)
        .get_intersection(BoolDecomposedFA.from_fa(aut2))
        .to_fa()
    )
