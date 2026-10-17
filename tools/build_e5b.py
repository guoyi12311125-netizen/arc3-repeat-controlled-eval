"""Build E5b: same six-arm screen as E5, plus a patient shared-cache flush.

E5 stopped after two arms because the 15 s isolation probe failed while the
just-stopped worker still left the service busy (BLOCKED_CACHE_ISOLATION ->
CLEANUP_FAILED -> batch aborted). The patch wraps legacy.flush_shared_cache
with bounded retries so a busy service no longer kills the batch.
"""
import json
import pathlib

SRC = pathlib.Path("e5_behavior/kernel")
DST = pathlib.Path("e5b/kernel")
DST.mkdir(parents=True, exist_ok=True)

PATCH = '''

# The stock isolation probe gives the shared service one 15 s budget; a worker
# that has just been stopped can leave it busy, and a failed probe aborts the
# whole batch (E5 lost four arms that way). Retry the same probe with bounded
# patience instead of failing the batch.
_original_flush_shared_cache = batch_tools.legacy.flush_shared_cache
def _patient_flush_shared_cache(server_root, output, timeout=150.0):
    delay = 5.0
    last_error = None
    for _attempt in range(4):
        try:
            return _original_flush_shared_cache(server_root, output, timeout=timeout)
        except RuntimeError as exc:
            last_error = exc
            time.sleep(delay)
            delay *= 2
    raise last_error
batch_tools.legacy.flush_shared_cache = _patient_flush_shared_cache
'''

nb = json.load(open(SRC / "notebook.ipynb", encoding="utf-8"))
cell1 = "".join(nb["cells"][1]["source"])
anchor = "import safe_batch_experiment as batch_tools\n"
assert cell1.count(anchor) == 1, cell1.count(anchor)
cell1 = cell1.replace(anchor, anchor + PATCH)
lines = cell1.split("\n")
nb["cells"][1]["source"] = [ln + "\n" for ln in lines[:-1]] + ([""] if lines[-1] == "" else [lines[-1]])
compile(cell1, "<cell1>", "exec")

nb["cells"][0]["source"] = [
    "# E5b behavior screen — E5 repeated with a patient cache-isolation probe\n",
    "\n",
    "Same six arms, same frozen first-10 public games, same 2000 s/game, same production-like\n",
    "serving settings as E5, which stopped after two arms when the 15 s shared-cache isolation\n",
    "probe failed while the service was still busy. The probe now retries with bounded patience.\n",
    "\n",
    "| arm | override |\n",
    "|---|---|\n",
    "| baseline | none (exact submission env) |\n",
    "| noop_guard | ARC3_NOOP_REPEAT_GUARD=1, ARC3_DEATH_LEDGER=1, ARC3_DEATH_REPEAT_GUARD=1 |\n",
    "| inventory | ARC3_LEVEL_INVENTORY=1 |\n",
    "| memory_slim | ARC3_MEMORY_SECTIONS=slim |\n",
    "| drain60 | ARC3_HISTORY_TURN_DRAIN=60 |\n",
    "| baseline_rep | none, run last: session-drift control |\n",
    "\n",
    "E5 first pass (10 games each): baseline mean 12.91, 17/73 levels, 552 actions;\n",
    "noop_guard mean 22.04, 24/73 levels, 658 actions, 5 games improved and none worse.\n",
    "E5b repeats the pair and adds the four arms E5 never reached.\n",
    "No promotion; scores are not comparable with 2900 s/game runs.\n",
    "Pinned Python 3.12 image, RTX PRO 6000, private and offline; competition reruns refused.\n",
]
json.dump(nb, open(DST / "notebook.ipynb", "w", encoding="utf-8"), ensure_ascii=False)

meta = json.load(open(SRC / "kernel-metadata.json", encoding="utf-8"))
meta.update(id="zgyyyl/arc3-e5b-behavior", title="ARC3 E5b Behavior")
json.dump(meta, open(DST / "kernel-metadata.json", "w", encoding="utf-8"), indent=2)

# ------------------------------------------------------------- self-check
back = json.load(open(DST / "notebook.ipynb", encoding="utf-8"))
j = "".join(back["cells"][1]["source"])
assert j.count("_patient_flush_shared_cache") == 2, j.count("_patient_flush_shared_cache")
assert all(el.endswith("\n") for el in back["cells"][1]["source"][:-1])
print("E5b built:", DST / "notebook.ipynb", (DST / "notebook.ipynb").stat().st_size, "bytes")
print("arms:", json.loads(back["cells"][1]["source"][11].split(" = ")[1].replace("'", '"')) if False else "same as E5")
