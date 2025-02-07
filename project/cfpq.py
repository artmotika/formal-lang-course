from pyformlang.cfg.cfg import CFG, Variable
from networkx.classes.multidigraph import MultiDiGraph
from typing import Any
from collections import deque
from project.cfg_utilities import cfg_to_weakened_form_chomsky
from enum import Enum
from scipy.sparse import dok_matrix, eye, bsr_matrix, csr_matrix
from project.ecfg import ECFG
from project.rsm import RSM
from project.bool_decomposed_fa_csr import BoolDecomposedFA
from project.automata import build_nfa_from_graph
from pyformlang.finite_automaton import Symbol


class CFPQAlgorithm(Enum):
    HELINGS = 0
    MATRIX = 1
    TENSOR = 2


def cfpq(
    cfg: CFG,
    graph: MultiDiGraph,
    start_nodes: set = None,
    final_nodes: set = None,
    algo: CFPQAlgorithm = CFPQAlgorithm.HELINGS,
) -> set[tuple[Any, Any]]:
    result = set()
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    for (e1, e2, e3) in [helings, matrix, tensor][algo.value](cfg, graph):
        if e2 == cfg.start_symbol and e1 in start_nodes and e3 in final_nodes:
            result.add((e1, e3))
    return result


def tensor(cfg: CFG, graph: MultiDiGraph) -> set[tuple[Any, Variable, Any]]:
    rsm = RSM.from_ecfg(ECFG.from_pyfl_cfg(cfg)).minimize()
    fa = build_nfa_from_graph(graph)

    rsm_mtx = BoolDecomposedFA.from_rsm(rsm)
    graph_mtx = BoolDecomposedFA.from_fa(fa)

    n = len(graph)

    for p in cfg.productions:
        head = p.head
        len_p_body = len(p.body)
        if len_p_body == 0:
            graph_mtx[Symbol(head.value)] += eye(n, dtype=bool, format="csr")

    last_nonzero_indices_count = 0
    while True:
        intersection = rsm_mtx.get_intersection(graph_mtx)
        transactive_closure = intersection.transitive_closure().todok()

        nonzero_indices = list(zip(*transactive_closure.nonzero()))
        if len(nonzero_indices) == last_nonzero_indices_count:
            break
        last_nonzero_indices_count = len(nonzero_indices)
        for i, j in nonzero_indices:
            rsm_i, rsm_j = i // n, j // n
            graph_i, graph_j = (
                i % n,
                j % n,
            )
            state_from, state_to = (
                rsm_mtx.idx_to_state[rsm_i],
                rsm_mtx.idx_to_state[rsm_j],
            )
            symbol, _ = state_from.value
            if (
                transactive_closure[i, j]
                and state_from in rsm_mtx.start_states
                and state_to in rsm_mtx.final_states
            ):
                graph_adjacency_mtx = graph_mtx.adjacency_matrices.get(Symbol(symbol))
                if graph_adjacency_mtx is not None:
                    graph_mtx.adjacency_matrices[Symbol(symbol)][
                        graph_i, graph_j
                    ] = True
                else:
                    new_mtx = dok_matrix((n, n), dtype=bool)
                    new_mtx[graph_i, graph_j] = True
                    graph_mtx.adjacency_matrices[Symbol(symbol)] = new_mtx.copy()

    return {
        (
            graph_mtx.idx_to_state[graph_i],
            Variable(var),
            graph_mtx.idx_to_state[graph_j],
        )
        for var, mtx in graph_mtx.adjacency_matrices.items()
        for graph_i, graph_j in zip(*mtx.nonzero())
    }


def matrix(cfg: CFG, graph: MultiDiGraph) -> set[tuple[Any, Variable, Any]]:
    cfg = cfg_to_weakened_form_chomsky(cfg)
    (
        epsilon_var_heads,
        one_var_productions,
        two_var_productions,
    ) = _get_weakened_form_productions(cfg)

    n = len(graph.nodes)

    bool_decomposed_graph_mtx = {
        var: dok_matrix((n, n), dtype=bool) for var in cfg.variables
    }

    nodes = list(graph.nodes)
    node_to_int = {node: idx for idx, node in enumerate(graph.nodes)}

    for (node1, node2, symbol) in graph.edges(data=True):
        for p in one_var_productions:
            if symbol["label"] == p.body[0].value:
                bool_decomposed_graph_mtx[p.head][
                    node_to_int.get(node1), node_to_int.get(node2)
                ] = True
    for var in bool_decomposed_graph_mtx.keys():
        bool_decomposed_graph_mtx[var] = bool_decomposed_graph_mtx[var].tocsr()
    for head in epsilon_var_heads:
        bool_decomposed_graph_mtx[head] += eye(n, dtype=bool, format="csr")
    changed = True
    while changed:
        changed = False
        for p in two_var_productions:
            old_mtx_cnz = bool_decomposed_graph_mtx[p.head].count_nonzero()
            bool_decomposed_graph_mtx[p.head] += (
                bool_decomposed_graph_mtx[p.body[0]]
                @ bool_decomposed_graph_mtx[p.body[1]]
            )
            changed |= old_mtx_cnz != bool_decomposed_graph_mtx[p.head].count_nonzero()
    return {
        (nodes[i], var, nodes[j])
        for var in bool_decomposed_graph_mtx.keys()
        for i, j in zip(*bool_decomposed_graph_mtx[var].nonzero())
    }


def helings(cfg: CFG, graph: MultiDiGraph) -> set[tuple[Any, Variable, Any]]:
    cfg = cfg_to_weakened_form_chomsky(cfg)
    (
        epsilon_var_heads,
        one_var_productions,
        two_var_productions,
    ) = _get_weakened_form_productions(cfg)

    one_var = {
        (node1, p.head, node2)
        for (node1, node2, symbol) in graph.edges(data=True)
        for p in one_var_productions
        if symbol["label"] == p.body[0].value
    }
    eps_var = {(node, head, node) for head in epsilon_var_heads for node in graph.nodes}

    r = one_var | eps_var
    m = deque(r.copy())
    while m:
        (v, Ni, u) = m.pop()
        temp_r = r.copy()
        for (nv, Nj, v_old) in temp_r:
            if v_old == v:
                for p in two_var_productions:
                    head = p.head
                    if (
                        Nj == p.body[0].value
                        and Ni == p.body[1].value
                        and (nv, head, u) not in r
                    ):
                        m.appendleft((nv, head, u))
                        r.add((nv, head, u))
        for (u_old, Nj, nv) in temp_r:
            if u_old == u:
                for p in two_var_productions:
                    head = p.head
                    if (
                        Ni == p.body[0].value
                        and Nj == p.body[1].value
                        and (v, head, nv) not in r
                    ):
                        m.appendleft((v, head, nv))
                        r.add((v, head, nv))
    return r


def _get_weakened_form_productions(cfg: CFG) -> tuple[set, set, set]:
    epsilon_var_heads = set()
    one_var_productions = set()
    two_var_productions = set()
    for p in cfg.productions:
        head = p.head
        len_p_body = len(p.body)
        if len_p_body == 0:
            epsilon_var_heads.add(head)
        elif len_p_body == 1:
            one_var_productions.add(p)
        elif len_p_body == 2:
            two_var_productions.add(p)
        else:
            raise ValueError("Cfg in helings() is not in weakened form Chomsky")
    return (epsilon_var_heads, one_var_productions, two_var_productions)
