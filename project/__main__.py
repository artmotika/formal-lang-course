from pyformlang.cfg import CFG
from project.ecfg import ECFG
from project.rsm import RSM
from pyformlang.regular_expression.regex import Regex
from networkx.algorithms.isomorphism.isomorph import is_isomorphic
from networkx.algorithms.isomorphism.matchhelpers import categorical_multiedge_match
from networkx.algorithms.isomorphism.matchhelpers import categorical_node_match

print("exec sources directory")
cfg = CFG.from_text(
    """
    S -> NP VP
    NP -> georges | Det N
    Det -> a | the
    N -> carrots"""
)

# for p in cfg.productions:
#     print("---------")
#     print(p.head)
#     print(p.body)
#     print("---------")
#
# print(Regex("12 2 3 "))
ecfg = ECFG.from_pyfl_cfg(cfg)
productions = ecfg.productions
for ph in productions.keys():
    print(f"\n{ph} -> {productions.get(ph)}\n")

print("---------")
set1 = set()

rsm = RSM.from_ecfg(ecfg)

print(rsm.start_module)
modules = rsm.modules
for k in modules.keys():
    for x, y, z in modules.get(k):
        set1.add(
            f"\n{k}:   {x} - {y} -> {z}  start_states = {modules.get(k).start_states} final_states = {modules.get(k).final_states}\n"
        )

print("--------")

print("-------------")
for info in set1:
    print(info)
print("-------------")

for p in Regex("(a|b)* c").to_cfg().productions:
    print(p)
