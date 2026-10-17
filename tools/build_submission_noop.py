"""Stage a guard-enabled build of the submission notebook (no push).

Same kernel id as the live submission (zgyyyl/arc-agi-3-daniel-m2-baseline), one
version newer, with the three repeat/death-guard switches E5 tested turned on in
the 'guards' section of the env cell. Nothing is pushed here: pushing starts a
full kernel run and consumes GPU quota, so that step waits for the E5b verdict.
"""
import json
import pathlib
import re

PULLED = pathlib.Path(r"C:\Users\86157\AppData\Local\Temp\subm")
SRC_NB = PULLED / "arc-agi-3-daniel-m2-baseline.ipynb"
SRC_META = PULLED / "kernel-metadata.json"
DST = pathlib.Path("submission-noop") / "kernel"
DST.mkdir(parents=True, exist_ok=True)

nb = json.load(open(SRC_NB, encoding="utf-8"))
meta = json.load(open(SRC_META, encoding="utf-8"))

GUARDS = {
    "ARC3_NOOP_REPEAT_GUARD": "1",
    "ARC3_DEATH_LEDGER": "1",
    "ARC3_DEATH_REPEAT_GUARD": "1",
}

env_cell = None
for i, cell in enumerate(nb["cells"]):
    s = "".join(cell.get("source", []))
    if "'ARC3_GUARDS_FROM_LEVEL'" in s:
        env_cell = i
        break
assert env_cell is not None, "env cell with guards section not found"

s = "".join(nb["cells"][env_cell]["source"])
anchor = "    'ARC3_GUARDS_FROM_LEVEL': 2,\n"
assert s.count(anchor) == 1, s.count(anchor)
added = "".join(f"    '{k}': '{v}',\n" for k, v in GUARDS.items())
s = s.replace(anchor, anchor + added)
lines = s.split("\n")
nb["cells"][env_cell]["source"] = [ln + "\n" for ln in lines[:-1]] + ([""] if lines[-1] == "" else [lines[-1]])
# The cell mixes IPython magics (!cmd) with Python, so validate the inserted block only.
compile("\n".join(f"{k} = {v!r}" for k, v in GUARDS.items()), "<guards>", "exec")

# sanity: names exist and nothing else changed
assert s.count("ARC3_NOOP_REPEAT_GUARD") == 1 and s.count("ARC3_DEATH_LEDGER") == 1
assert s.count("ARC3_DEATH_REPEAT_GUARD") == 1
assert "harness-changes.patch" in "".join("".join(c.get("source", [])) for c in nb["cells"])

meta["title"] = "ARC-AGI-3 Daniel M2 Baseline"
json.dump(nb, open(DST / "arc-agi-3-daniel-m2-baseline.ipynb", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(meta, open(DST / "kernel-metadata.json", "w", encoding="utf-8"), indent=2)
print("staged:", DST, "cells:", len(nb["cells"]), "env cell:", env_cell)
print("guards now:", re.findall(r"ARC3_(?:NOOP_REPEAT_GUARD|DEATH_LEDGER|DEATH_REPEAT_GUARD)': '[01]'", s))
