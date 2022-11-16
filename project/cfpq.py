from pyformlang.cfg.cfg import CFG, Variable
from networkx.classes.multidigraph import MultiDiGraph
from typing import Any
from collections import deque


def cfpq(
    cfg: CFG,
    graph: MultiDiGraph,
    start_nodes: set = None,
    final_nodes: set = None,
) -> set[tuple[Any, Any]]:
    result = set()
    start_nodes_is_none = start_nodes is None
    final_nodes_is_none = final_nodes is None
    for (e1, e2, e3) in helings(cfg, graph):
        if (
            (start_nodes_is_none or e2 in start_nodes)
            and (final_nodes_is_none or e3 in final_nodes)
            and e1 == cfg.start_symbol
        ):
            result.add((e2, e3))
    return result


def helings(cfg, graph) -> deque[tuple[Variable, Any, Any]]:
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

    r = deque(
        [
            (p.head, node1, node2)
            for (node1, node2, symbol) in graph.edges(data=True)
            for p in one_var_productions
            if symbol["label"] == p.body[0].value
        ]
    )

    for head in epsilon_var_heads:
        for node in graph.nodes:
            r.append((head, node, node))

    m = r.copy()
    while m:
        (Ni, v, u) = m.pop()
        for (Nj, nv, v_old) in list(r):
            if v_old == v:
                for p in two_var_productions:
                    head = p.head
                    if (
                        Nj == p.body[0].value
                        and Ni == p.body[1].value
                        and (head, nv, u) not in r
                    ):
                        m.append((head, nv, u))
                        r.append((head, nv, u))
        for (Nj, u_old, nv) in list(r):
            if u_old == u:
                for p in two_var_productions:
                    head = p.head
                    if (
                        Ni == p.body[0].value
                        and Nj == p.body[1].value
                        and (head, v, nv) not in r
                    ):
                        m.append((head, v, nv))
                        r.append((head, v, nv))
    return r
