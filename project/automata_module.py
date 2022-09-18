from networkx.drawing.nx_pydot import read_dot
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.regular_expression import Regex


# Builds minimal dfa from given regex with rules from pyformlang.regular_expression
def build_min_dfa_from_regex(regex_string):
    return Regex(regex_string).to_epsilon_nfa().minimize()


# Builds nfa from given graph whether it's a networkx graph or the path to the dot file
def build_nfa_from_graph(graph, start_states: set = None, final_states: set = None):
    multi_di_graph = (
        graph
        if str(type(graph)) == "<class 'networkx.classes.multidigraph.MultiDiGraph'>"
        else read_dot(graph)
    )

    nfa = NondeterministicFiniteAutomaton(
        states={State(state) for state in multi_di_graph.nodes},
        input_symbols={
            Symbol(edge["label"]) for (_, _, edge) in multi_di_graph.edges(data=True)
        },
        start_state={State(state) for state in multi_di_graph.nodes}
        if start_states is None
        else start_states,
        final_states={State(state) for state in multi_di_graph.nodes}
        if final_states is None
        else final_states,
    )

    nfa.add_transitions(
        [
            (state1, symbol["label"], state2)
            for (state1, state2, symbol) in multi_di_graph.edges(data=True)
        ]
    )
    return nfa
