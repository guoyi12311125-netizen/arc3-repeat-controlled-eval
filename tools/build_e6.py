"""Build E6: five-arm run that re-tests noop_guard and drain60 against ONE baseline
and adds the combination arm.

Arms (fresh worker each, frozen first-10 public games, 2000 s/game, production-like
serving): baseline, noop_guard, drain60, combo (guards + drain60), baseline_rep.
"""
import ast
import json
import pathlib

SRC = pathlib.Path("e5b/kernel")
DST = pathlib.Path("e6/kernel")
DST.mkdir(parents=True, exist_ok=True)

ARMS = ["baseline", "noop_guard", "drain60", "combo", "baseline_rep"]
GLOBAL_LIMIT = 17200
BUDGET = 3600 + len(ARMS) * (2000 + 260) + 180
assert BUDGET <= GLOBAL_LIMIT, (BUDGET, GLOBAL_LIMIT)

nb = json.load(open(SRC / "notebook.ipynb", encoding="utf-8"))
cell1 = "".join(nb["cells"][1]["source"])

# --- SAFE_SETTINGS.arms / global budget
i = cell1.find("SAFE_SETTINGS = {")
blob = cell1[i + len("SAFE_SETTINGS = "):]
depth = 0
for k, ch in enumerate(blob):
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            end = k + 1
            break
settings = ast.literal_eval(blob[:end])
settings["arms"] = ARMS
settings["global_limit_seconds"] = GLOBAL_LIMIT
# model shard loading was measured at ~2 min/shard under storage contention on
# 10-13 (38 shards => ~75 min), so give setup a wider deadline than the 3600 s used
# by every earlier run
settings["setup_limit_seconds"] = 5400
cell1 = cell1[:i] + "SAFE_SETTINGS = " + repr(settings) + cell1[i + len("SAFE_SETTINGS = ") + end:]

# --- arm registry
j = cell1.find("SAFE_HELPER_SOURCES = {")
blob2 = cell1[j + len("SAFE_HELPER_SOURCES = "):]
depth = 0
for k, ch in enumerate(blob2):
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            end2 = k + 1
            break
helpers = ast.literal_eval(blob2[:end2])
be = helpers["batch_experiment.py"]
m = be.find("ARMS = {")
# ARMS literal runs to end of its line
line_end = be.find("\n", m)
arms = ast.literal_eval(be[m + len("ARMS = "):line_end].strip())
assert "noop_guard" in arms and "drain60" in arms and "combo" not in arms, list(arms)[:12]
arms["combo"] = (1, 1500, {"ARC3_NOOP_REPEAT_GUARD": "1", "ARC3_DEATH_LEDGER": "1",
                           "ARC3_DEATH_REPEAT_GUARD": "1", "ARC3_HISTORY_TURN_DRAIN": "60"})
helpers["batch_experiment.py"] = be[:m] + "ARMS = " + repr(arms) + be[line_end:]
cell1 = cell1[:j] + "SAFE_HELPER_SOURCES = " + repr(helpers) + cell1[j + len("SAFE_HELPER_SOURCES = ") + end2:]
lines = cell1.split("\n")
nb["cells"][1]["source"] = [ln + "\n" for ln in lines[:-1]] + ([""] if lines[-1] == "" else [lines[-1]])

nb["cells"][0]["source"] = [
    "# E6 — guards, drain, and both together against one shared baseline\n",
    "\n",
    "Five arms, frozen first-10 public games, 2000 s per game, production-like serving\n",
    "(shared MAXREQ 10, MEMFRAC 0.92, context 131072, output 12288, analyzer timeout 120 s).\n",
    "No arm touches a serving knob, so no restart is needed and every arm sees the same\n",
    "server, the same games and the same order. The patient flush probe from E5b is kept.\n",
    "\n",
    "| arm | override |\n",
    "|---|---|\n",
    "| baseline | none (exact submission env) |\n",
    "| noop_guard | ARC3_NOOP_REPEAT_GUARD=1, ARC3_DEATH_LEDGER=1, ARC3_DEATH_REPEAT_GUARD=1 |\n",
    "| drain60 | ARC3_HISTORY_TURN_DRAIN=60 |\n",
    "| combo | both of the above |\n",
    "| baseline_rep | none, run last: session-drift control |\n",
    "\n",
    "Prior evidence: noop_guard +9.12 (E5) and +5.54 (E5b) vs its concurrent baseline;\n",
    "drain60 +6.02 (E5b) with 14 % fewer actions; drift control +3.33 (E5b).\n",
    "This run gives noop_guard a third sample, drain60 a second, and the combo its first,\n",
    "all against the same baseline. No promotion; not comparable with 2900 s/game runs.\n",
    "Pinned Python 3.12 image, RTX PRO 6000, private and offline; competition reruns refused.\n",
]
json.dump(nb, open(DST / "notebook.ipynb", "w", encoding="utf-8"), ensure_ascii=False)

meta = json.load(open(SRC / "kernel-metadata.json", encoding="utf-8"))
meta.update(id="zgyyyl/arc3-e6-combo", title="ARC3 E6 Combo")
json.dump(meta, open(DST / "kernel-metadata.json", "w", encoding="utf-8"), indent=2)

# --- self-check
back = json.load(open(DST / "notebook.ipynb", encoding="utf-8"))
j2 = "".join(back["cells"][1]["source"])
assert all(el.endswith("\n") for el in back["cells"][1]["source"][:-1])
assert "'combo'" in j2 and j2.count('"combo"') <= 3
s2 = ast.literal_eval(j2[j2.find("SAFE_SETTINGS = {") + len("SAFE_SETTINGS = "):j2.find("\n", j2.find("SAFE_SETTINGS = {"))])
print("arms:", s2["arms"], "| global:", s2["global_limit_seconds"], "| budget:", BUDGET)
print("E6 built:", DST / "notebook.ipynb", (DST / "notebook.ipynb").stat().st_size)
