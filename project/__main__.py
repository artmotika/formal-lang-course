from pyformlang.cfg import CFG
from project.extended_context_free_grammar import ECFG
from project.rsm import RSM

print("exec sources directory")
cfg = CFG.from_text(
    """
    S -> NP VP PUNC
    PUNC -> . | !
    VP -> V NP
    V -> buys | touches | sees
    NP -> georges | jacques | leo | Det N
    Det -> a | an | the
    N -> gorilla | dog | carrots"""
)

# for p in cfg.productions:
#     print("---------")
#     print(p.head)
#     print(p.body)
#     print("---------")

# ecfg = ECFG.from_pyfl_cfg(cfg)
# print(ecfg.start_symbol)
# print(ecfg.productions)
# rsm = ecfg.to_rsm()
rsm = RSM.from_pyfl_cfg(cfg)
print(rsm.start_module)
modules = rsm.modules
for k in modules.keys():
    for x, y, z in modules.get(k):
        print(
            f"\n{k}:   {x} - {y} -> {z}  start_states = {modules.get(k).start_states} final_states = {modules.get(k).final_states}\n"
        )


# print(cfg.get_generating_symbols())
