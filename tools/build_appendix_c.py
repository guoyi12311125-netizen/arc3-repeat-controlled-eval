# -*- coding: utf-8 -*-
"""Appendix C generator: experiment registry.
Curated rows (purpose, design, disposition) + auto-filled kernel slugs and dir checks.
"""
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "arc3-eng" / "runs"
OUT = Path(__file__).resolve().parent.parent / "data" / "appendix-c-registry.md"

def slug(run):
    meta = RUNS / run / "kernel" / "kernel-metadata.json"
    try:
        d = json.load(open(meta, encoding="utf-8"))
        return d.get("id") or d.get("slug") or "?"
    except Exception:
        return "-"

ROWS = [
    # (id, dir, purpose, design, state, disposition)
    ("E4", "e5_drain",
     "Serving-stack throughput probe",
     "archived notebook and module only",
     "code archived, no retained run artifacts",
     "informed the calibration-run design; not an analysis input"),
    ("a1", "calib_a",
     "First calibration probe, 25 games, single arm",
     "single execution",
     "all 25 game records cancelled with zero actions",
     "excluded: no usable play records"),
    ("a2", "calib_a2",
     "Calibration follow-up, 25 games, single arm",
     "single execution",
     "complete (2026-10-12), mean 14.72",
     "latency context; Appendix B"),
    ("a3", "calib_a3",
     "Calibration run, 25 games, stock 120-second analyzer timeout",
     "single execution",
     "complete (2026-10-12), mean 27.40",
     "member of the timeout pair (a3 vs a5), Table 2"),
    ("a4", "calib_a4",
     "Calibration run, 25 games, widened per-game ceiling and session count",
     "single execution",
     "complete (2026-10-12), mean 25.36",
     "latency anatomy pair (a4 vs a5); queue-delay statistics"),
    ("a5", "calib_a5",
     "Calibration run, 25 games, doubled analyzer timeout 240 seconds",
     "single execution",
     "complete (2026-10-12), mean 24.20",
     "member of the timeout pair and the latency pair"),
    ("E5", "e5_behavior",
     "Behavior screen: baseline vs no-op guard",
     "bracketed screen, batch aborted",
     "two of the planned arms completed; batch stopped by a watcher failure",
     "both completed arms enter Table 1, Table 4 and the ft09 count; the lost arms were re-run as E5b"),
    ("E5b", "e5b",
     "Behavior screen re-run: six arms including inventory, memory slim, drain and a repeat baseline",
     "fully bracketed screen, six arms",
     "complete (2026-10-13)",
     "main screen for the guard, inventory, memory-slim and drain readings, Tables 1-4"),
    ("E6", "e6",
     "Second behavior screen: baseline, guard, drain, combo, repeat baseline",
     "fully bracketed screen, five arms",
     "complete (2026-10-14); the first kernel build failed before running and was rebuilt",
     "second controlled guard reading and the drain/combo candidates, Tables 1-4"),
    ("E6-b1", "e6",
     "E6 kernel, first build: failed before any run (serialization error in one arm's configuration)",
     "build only",
     "failed at build stage; no records produced",
     "rebuilt as E6; the failed build contributes nothing to the analysis"),
    ("E7-b1", "e7",
     "E7 kernel, first build: failed budget validation before any run",
     "build only",
     "failed at build stage; no records produced",
     "rebuilt as E7; the failed build contributes nothing to the analysis"),
    ("E7", "e7",
     "Alternating repeat matrix: three baseline and three guard arms interleaved",
     "A-B-A-B-A-B, six arms, ten games each",
     "complete (2026-10-15); the first kernel build failed budget validation and was rebuilt",
     "same-configuration spread for both arms of a pair, Section 4 and the guard paragraphs"),
    ("S-noop", "submission-noop",
     "Submission build: baseline plus no-op guard only",
     "local build of the competition kernel",
     "built and locally verified",
     "not submitted; superseded by the three-switch guard build"),
    ("S-guard", "submission-guards",
     "Submission build: three guard switches on",
     "local build of the competition kernel",
     "submitted twice: 57147727 (2026-10-13) and 57174905 (2026-10-14)",
     "the linked submission of this paper, Table 3a"),
    ("S-drain", "submission-drain60",
     "Submission build: guard build plus history turn drain at 60 turns",
     "local build of the competition kernel",
     "built and locally verified; local deltas +5.19 (E6) and +2.00 (end-control view)",
     "not submitted: daily submission limit and an unresolved reading"),
    ("S-combo", "submission-combo",
     "Submission build: guards plus drain combined",
     "local build of the competition kernel",
     "built and locally verified",
     "not submitted: weak local reading"),
    ("N1", "night-chain-20261013.log",
     "Overnight orchestration script (downloads, pushes, watchers)",
     "infrastructure, not an experiment",
     "log retained",
     "not an analysis input"),
]

def main():
    lines = ["# Appendix C. Experiment registry", "",
             "Every experiment started over the competition, its state, and why it did or did not enter the analysis. Kernel slugs point at the pushed notebooks in the release.", ""]
    lines.append("| id | kernel | purpose | design | state | disposition |")
    lines.append("|---|---|---|---|---|---|")
    for rid, run, purpose, design, state, disp in ROWS:
        exists = (RUNS / run).exists()
        s = slug(run) if (RUNS / run / "kernel").exists() else "-"
        mark = "" if exists else " (artifacts not retained locally)"
        lines.append(f"| {rid} | `{s}` | {purpose} | {design} | {state}{mark} | {disp} |")
    lines.append("")
    lines.append("The two failed builds above never produced records: the failure happened before the batch started, so neither screen contains partial arms from them.")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"已写 {OUT}")
    for rid, run, *_ in ROWS:
        print(f"  {rid:8s} {run:28s} exists={ (RUNS/run).exists() }")

if __name__ == "__main__":
    main()
