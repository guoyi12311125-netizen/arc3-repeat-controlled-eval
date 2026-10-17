"""Build a submission variant (guards / drain60 / combo) from the pulled v2 notebook.

The live submission (version 3) enables the three guard keys. This script produces
further variants off the same base, so a new version is one `kaggle kernels push`
away once the local screen says which knob to ship.

Usage:
    python build_submission_variant.py drain60
    python build_submission_variant.py combo
    python build_submission_variant.py guards     # reproduces current v3
"""
import json
import pathlib
import sys

PULLED = pathlib.Path(r"C:\Users\86157\AppData\Local\Temp\subm")
BASE_NOTEBOOK = PULLED / "arc-agi-3-daniel-m2-baseline.ipynb"
BASE_META = PULLED / "kernel-metadata.json"

VARIANTS = {
    "guards": {
        "ARC3_NOOP_REPEAT_GUARD": "1",
        "ARC3_DEATH_LEDGER": "1",
        "ARC3_DEATH_REPEAT_GUARD": "1",
    },
    "drain60": {
        "ARC3_HISTORY_TURN_DRAIN": "60",
    },
    "combo": {
        "ARC3_NOOP_REPEAT_GUARD": "1",
        "ARC3_DEATH_LEDGER": "1",
        "ARC3_DEATH_REPEAT_GUARD": "1",
        "ARC3_HISTORY_TURN_DRAIN": "60",
    },
}


def build(variant: str) -> pathlib.Path:
    if variant not in VARIANTS:
        raise SystemExit(f"unknown variant {variant!r}; choose from {sorted(VARIANTS)}")
    overrides = VARIANTS[variant]
    nb = json.load(open(BASE_NOTEBOOK, encoding="utf-8"))
    meta = json.load(open(BASE_META, encoding="utf-8"))

    cell = None
    for i, c in enumerate(nb["cells"]):
        if "'ARC3_GUARDS_FROM_LEVEL'" in "".join(c.get("source", [])):
            cell = i
            break
    assert cell is not None, "env cell not found"
    s = "".join(nb["cells"][cell]["source"])

    anchor = "    'ARC3_GUARDS_FROM_LEVEL': 2,\n"
    assert s.count(anchor) == 1
    # drop any guard lines a previous variant run put in, then re-add this variant's set.
    # HISTORY_TURN_DRAIN is edited in place further down (the base notebook already sets it),
    # so it must not also be appended here: a duplicate dict key would silently shadow.
    for key in ("ARC3_NOOP_REPEAT_GUARD", "ARC3_DEATH_LEDGER", "ARC3_DEATH_REPEAT_GUARD"):
        s = "\n".join(ln for ln in s.split("\n") if f"'{key}'" not in ln)
    guard_keys = {k: v for k, v in overrides.items() if k != "ARC3_HISTORY_TURN_DRAIN"}
    added = "".join(f"    '{k}': '{v}',\n" for k, v in guard_keys.items())
    s = s.replace(anchor, anchor + added)

    if "ARC3_HISTORY_TURN_DRAIN" in overrides:
        # the base notebook sets 30; a variant that wants another value must not double-set
        old = "    'ARC3_HISTORY_TURN_DRAIN': 30,\n"
        assert s.count(old) == 1, s.count(old)
        s = s.replace(old, f"    'ARC3_HISTORY_TURN_DRAIN': {overrides['ARC3_HISTORY_TURN_DRAIN']},\n")

    lines = s.split("\n")
    nb["cells"][cell]["source"] = [ln + "\n" for ln in lines[:-1]] + ([""] if lines[-1] == "" else [lines[-1]])

    dest = pathlib.Path("submission-" + variant) / "kernel"
    dest.mkdir(parents=True, exist_ok=True)
    json.dump(nb, open(dest / "arc-agi-3-daniel-m2-baseline.ipynb", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(meta, open(dest / "kernel-metadata.json", "w", encoding="utf-8"), indent=2)
    print(f"{variant}: wrote {dest} | env keys added: {list(overrides)}")
    return dest


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "guards")
