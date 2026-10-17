"""Build the E5 behavior-screen kernel from the a5 calibration notebook.

E5 asks: which *agent-behavior* switches (all default-OFF in the submission)
move completed levels / score, at production-like serving settings?

Arms (one fresh worker each, same frozen first-10 public games, 2000 s/game):
  baseline      reference (exact submission env)
  noop_guard    ARC3_NOOP_REPEAT_GUARD + DEATH_LEDGER + DEATH_REPEAT_GUARD
  inventory     ARC3_LEVEL_INVENTORY (START-vs-START inventory on new levels)
  memory_slim   ARC3_MEMORY_SECTIONS=slim (World model + Plan sections)
  drain60       ARC3_HISTORY_TURN_DRAIN=60 (E4's only positive throughput arm)
  baseline_rep  drift control, identical to baseline, run last
"""
import ast
import json
import pathlib
import re

SRC = pathlib.Path("calib_a5/kernel")
DST = pathlib.Path("e5_behavior/kernel")
DST.mkdir(parents=True, exist_ok=True)

nb = json.load(open(SRC / "notebook.ipynb", encoding="utf-8"))

# ---------------------------------------------------------------- cell 0
nb["cells"][0]["source"] = [
    "# E5 behavior screen — six arms, production-like settings\n",
    "\n",
    "One question: which agent-behavior switches (default OFF in the submission) raise\n",
    "completed levels / native score at production-like serving settings?\n",
    "\n",
    "Arms run sequentially, each in a fresh worker over the same sorted first-10 public\n",
    "games, one pass, 2000 s per game. Serving stays fixed (shared MAXREQ 10, MEMFRAC 0.92,\n",
    "context 131072, output 12288, analyzer timeout 120 s) and no arm changes a serving knob,\n",
    "so no restart is required and every arm sees the same server and the same games.\n",
    "\n",
    "| arm | override |\n",
    "|---|---|\n",
    "| baseline | none (exact submission env) |\n",
    "| noop_guard | ARC3_NOOP_REPEAT_GUARD=1, ARC3_DEATH_LEDGER=1, ARC3_DEATH_REPEAT_GUARD=1 |\n",
    "| inventory | ARC3_LEVEL_INVENTORY=1 |\n",
    "| memory_slim | ARC3_MEMORY_SECTIONS=slim |\n",
    "| drain60 | ARC3_HISTORY_TURN_DRAIN=60 |\n",
    "| baseline_rep | none, run last as a session-drift control |\n",
    "\n",
    "Read-out: per-arm completed levels, engine actions, per-level efficiency and native\n",
    "RHAE, plus per-game native scores. baseline_rep vs baseline bounds session drift, so a\n",
    "candidate is only interesting if it beats BOTH baselines by more than that spread.\n",
    "No promotion. Scores are not comparable with 2900 s/game runs.\n",
    "Pinned Python 3.12 image, RTX PRO 6000, private and offline; competition reruns refused.\n",
]

# ------------------------------------------------------- cell 1: settings
cell1 = "".join(nb["cells"][1]["source"])

def to_source(text: str) -> list[str]:
    """nbformat needs each source line to keep its trailing newline."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        return [ln + "\n" for ln in lines[:-1]] + [""]
    return [ln + "\n" for ln in lines[:-1]] + [lines[-1]]


E5_SETTINGS = {
    "arms": ["baseline", "noop_guard", "inventory", "memory_slim", "drain60", "baseline_rep"],
    "passes": 1,
    "game_count": 10,
    "solver_concurrency": 10,
    "admission": 10,
    "maxreq": 10,
    "cudagraph_maxbs": 10,
    "context_tokens": 131072,
    "max_output_tokens": 12288,
    "game_seconds": 2000,
    "analyzer_timeout_seconds": 120,
    "setup_limit_seconds": 3600,
    "global_limit_seconds": 17500,
    "final_artifact_seconds": 180,
    "worker_overhead_seconds": 260,
    "restart_between_passes": False,
    "restart_limit_seconds": 900,
    "poll_interval_seconds": 5,
    "graceful_stop_seconds": 130,
    "require_gpu": True,
    "host_min_available_bytes": 8589934592,
    "host_max_used_percent": 90,
    "cgroup_max_used_percent": 90,
    "gpu_min_free_bytes": 1073741824,
    "gpu_max_used_percent": 98,
}

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
old_settings = ast.literal_eval(blob[:end])
assert old_settings["arms"] == ["baseline"], old_settings["arms"]
cell1 = cell1[:i] + "SAFE_SETTINGS = " + repr(E5_SETTINGS) + cell1[i + len("SAFE_SETTINGS = ") + end:]

# ------------------------------------- cell 1: helper sources (arm registry)
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
m = re.search(r"ARMS = \{.*?\}\n", be, re.S)
assert m, "ARMS literal not found"
arms = ast.literal_eval(m.group(0)[len("ARMS = "):].strip())
added = {
    "noop_guard": {"ARC3_NOOP_REPEAT_GUARD": "1", "ARC3_DEATH_LEDGER": "1", "ARC3_DEATH_REPEAT_GUARD": "1"},
    "inventory": {"ARC3_LEVEL_INVENTORY": "1"},
    "drain60": {"ARC3_HISTORY_TURN_DRAIN": "60"},
    "baseline_rep": {},
}
for name, overrides in added.items():
    assert name not in arms, name
    arms[name] = (1, 1500, overrides)
assert "memory_slim" in arms, "memory_slim missing from base registry"
helpers["batch_experiment.py"] = be[:m.start()] + "ARMS = " + repr(arms) + "\n" + be[m.end():]
cell1 = cell1[:j] + "SAFE_HELPER_SOURCES = " + repr(helpers) + cell1[j + len("SAFE_HELPER_SOURCES = ") + end2:]
nb["cells"][1]["source"] = to_source(cell1)

# ------------------------------------------------------------- metadata
meta = {
    "id": "zgyyyl/arc3-e5-behavior",
    "title": "ARC3 E5 Behavior",
    "code_file": "notebook.ipynb",
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": True,
    "enable_tpu": False,
    "enable_internet": False,
    "machine_shape": "NvidiaRtxPro6000",
    "competition_sources": ["arc-prize-2026-arc-agi-3"],
    "dataset_sources": ["dfranzen/pennyroyal-v253", "dfranzen/taaf-kaggle-source-bundle-copy"],
    "kernel_sources": [],
    "model_sources": [
        "dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/Transformers/default/1",
        "dfranzen/albucino-qwen3-8-flash-next-drafter/Transformers/default/1",
    ],
    "docker_image": "gcr.io/kaggle-private-byod/python@sha256:57e612b484cf3df5026ee4dcc3cb176974b22b2bc0937fb1e16132a8be4cb13c",
}

json.dump(nb, open(DST / "notebook.ipynb", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(meta, open(DST / "kernel-metadata.json", "w", encoding="utf-8"), indent=2)

# ------------------------------------------------------------- self-check
back = json.load(open(DST / "notebook.ipynb", encoding="utf-8"))
c1 = "".join(back["cells"][1]["source"])
k = c1.find("SAFE_HELPER_SOURCES = {")
b = c1[k + len("SAFE_HELPER_SOURCES = "):]
depth = 0
for kk, ch in enumerate(b):
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            e = kk + 1
            break
h2 = ast.literal_eval(b[:e])
compile(c1, "<cell1>", "exec")          # syntax check
arms2 = ast.literal_eval(re.search(r"ARMS = \{.*?\}\n", h2["batch_experiment.py"], re.S).group(0)[len("ARMS = "):].strip())
budget = 3600 + len(E5_SETTINGS["arms"]) * (E5_SETTINGS["game_seconds"] + E5_SETTINGS["worker_overhead_seconds"]) + 180
print("arms:", list(arms2))
print("budget total:", budget, "<= global", E5_SETTINGS["global_limit_seconds"], budget <= E5_SETTINGS["global_limit_seconds"])
print("settings arms:", E5_SETTINGS["arms"])
print("wrote:", DST / "notebook.ipynb", (DST / "notebook.ipynb").stat().st_size, "bytes")
