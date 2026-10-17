# -*- coding: utf-8 -*-
"""Appendix B generator: per-game tables for all screens + ft09 detail.
Reads runs/ dirs directly; writes data/appendix-b-per-game.md.
"""
import json, glob, sys
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent.parent / "arc3-eng" / "runs"
OUT = Path(__file__).resolve().parent.parent / "data" / "appendix-b-per-game.md"

def load_arm(metrics_path):
    m = json.load(open(metrics_path, encoding="utf-8"))
    games = m.get("games") or []
    per = {}
    for g in games:
        name = str(g.get("game_id", "")).split("-")[0]
        per[name] = dict(
            score=float(g.get("native_final_score") or 0.0),
            levels=int(g.get("levels_completed") or 0),
            actions=int(g.get("actual_actions") or 0),
            errors=int(g.get("error_count") or 0),
            state=g.get("state") or "",
        )
    return per

def fmt_cell(d):
    if d is None:
        return "-"
    return f"{d['score']:.1f} L{d['levels']} A{d['actions']} E{d['errors']}"

def screen_arms(run, phase_pref=None):
    """Return [(arm_name, per_game_dict)] sorted with baseline first."""
    phases = sorted(glob.glob(str(RUNS / run / "out" / "phase_b_safe_*"))) + \
             sorted(glob.glob(str(RUNS / run / "output" / "phase_b_safe_*")))
    if not phases:
        return None, None
    phase = phases[-1]
    arms = {}
    for p in glob.glob(phase + "/*/metrics.json"):
        arms[Path(p).parent.name.replace("_p0", "")] = load_arm(p)
    return Path(phase).name, arms

def main():
    screens = [("E5", "e5_behavior"), ("E5b", "e5b"), ("E6", "e6"), ("E7", "e7")]
    lines = ["# Appendix B. Per-game tables",
             "",
             "Generated from the run artifacts by `tools/build_appendix_b.py`. Cells read",
             "`score  L levels  A actions  E errors`. Means are calculated from unrounded scores, so a mean can differ by 0.01 to 0.02 from the average of the displayed one-decimal cells. The full JSON for every arm is in the release.",
             ""]
    ft09_rows = []
    guard_tot = non_guard_tot = 0
    guard_solves = non_guard_solves = 0

    for label, run in screens:
        phase, arms = screen_arms(run)
        if not arms:
            lines.append(f"## Screen {label}: artifacts not found")
            continue
        games = sorted({g for a in arms.values() for g in a})
        order = sorted(arms.keys(), key=lambda a: (not a.startswith("baseline"), a))
        lines.append(f"### Screen {label} (`{phase}`)")
        lines.append("")
        lines.append("| Game | " + " | ".join(order) + " |")
        lines.append("|---" * (len(order) + 1) + "|")
        for game in games:
            cells = [fmt_cell(arms[a].get(game)) for a in order]
            lines.append(f"| {game} | " + " | ".join(cells) + " |")
        means = []
        for a in order:
            vals = [arms[a][g]["score"] for g in games if g in arms[a]]
            means.append(f"{sum(vals)/len(vals):.2f}" if vals else "-")
        lines.append("| **Mean** | " + " | ".join(f"**{m}**" for m in means) + " |")
        lines.append("")
        for a in order:
            isg = "guard" in a
            tot = guard_tot if isg else non_guard_tot
            if isg: guard_tot += 1
            else: non_guard_tot += 1
            ft = arms[a].get("ft09")
            if ft:
                solve = ft["score"] >= 100
                if isg: guard_solves += solve
                else: non_guard_solves += solve
                ft09_rows.append((label, a, "guard" if isg else "non-guard", ft["score"], ft["levels"], "solve" if solve else ""))

    lines.append("### ft09 per arm across all four screens")
    lines.append("")
    lines.append("| Screen | Arm | Group | ft09 score | Levels | Outcome |")
    lines.append("|---|---|---|---|---|---|")
    for label, a, grp, sc, lv, out in sorted(ft09_rows, key=lambda r: (r[0], r[2], r[1])):
        lines.append(f"| {label} | {a} | {grp} | {sc:.2f} | {lv} | {out} |")
    lines.append("")
    lines.append(f"Guard arms: {guard_tot}, ft09 solves: {guard_solves}. Non-guard arms: {non_guard_tot}, ft09 solves: {non_guard_solves}. Inclusion rule for the second denominator: every arm of the four screens with a per-game record (E5 has two completed arms; E5b six; E6 five; E7 six).")
    lines.append("")

    # Calibration runs (single baseline arms)
    cal = [("a1", "calib_a"), ("a2", "calib_a2"), ("a3", "calib_a3"), ("a4", "calib_a4"), ("a5", "calib_a5")]
    lines.append("### Calibration runs (25 games each)")
    lines.append("")
    lines.append("| Game | " + " | ".join(c[0] for c in cal) + " |")
    lines.append("|---" * (len(cal) + 1) + "|")
    cal_arms = {}
    for name, run in cal:
        phase, arms = screen_arms(run)
        if arms:
            cal_arms[name] = next(iter(arms.values()))
    games = sorted({g for a in cal_arms.values() for g in a})
    for game in games:
        cells = [fmt_cell(cal_arms[c].get(game)) if c in cal_arms else "-" for c, _ in cal]
        lines.append(f"| {game} | " + " | ".join(cells) + " |")
    means = []
    for c, _ in cal:
        a = cal_arms.get(c)
        if a:
            vals = [a[g]["score"] for g in games if g in a]
            means.append(f"{sum(vals)/len(vals):.2f} ({len(vals)} games)")
        else:
            means.append("-")
    lines.append("| **Mean** | " + " | ".join(f"**{m}**" for m in means) + " |")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"已写 {OUT} ({len(lines)} 行)")
    print(f"守卫 {guard_tot} 臂 / 解出 {guard_solves}; 非守卫 {non_guard_tot} 臂 / 解出 {non_guard_solves}")

if __name__ == "__main__":
    main()
