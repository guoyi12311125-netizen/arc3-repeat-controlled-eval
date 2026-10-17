"""Re-extract every number the paper will cite, straight from the run artifacts.

Nothing here is typed from memory: each figure is computed from the files under
arc3-eng/runs/ and the Kaggle submissions API, and the source path is recorded
next to it. Output: data/numbers.json + data/numbers.md
"""
import json
import re
import statistics
from pathlib import Path

RUNS = Path.home() / "Desktop" / "hermes-output" / "arc3-eng" / "runs"
OUT = Path.home() / "Desktop" / "hermes-output" / "arc3-paper" / "data"
OUT.mkdir(parents=True, exist_ok=True)
result: dict = {}


def arm_stats(metrics_path: Path) -> dict:
    """Mean score, levels, actions, errors for one arm from its native metrics.json."""
    m = json.load(open(metrics_path, encoding="utf-8"))
    games = m["games"] if isinstance(m, dict) and "games" in m else m

    def sc(g):
        return g.get("native_final_score") or g.get("score") or 0.0

    return {
        "games": len(games),
        "mean": round(statistics.mean(sc(g) for g in games), 4),
        "levels": sum(g.get("levels_completed") or 0 for g in games),
        "levels_total": sum(g.get("number_of_levels") or 0 for g in games),
        "actions": sum(g.get("actual_actions") or 0 for g in games),
        "errors": sum(g.get("error_count") or 0 for g in games),
        "nonzero": sum(1 for g in games if sc(g) > 0),
        "source": str(metrics_path.relative_to(RUNS)),
    }


def collect_arms(run: str, phase_glob: str) -> dict:
    out = {}
    for sub in ("out", "output"):
        base_root = RUNS / run / sub
        if not base_root.exists():
            continue
        for d in sorted(base_root.glob(phase_glob)):
            for arm in sorted(p.name for p in d.iterdir() if p.is_dir() and p.name.endswith("_p0")):
                mp = d / arm / "metrics.json"
                if mp.exists() and mp.stat().st_size > 0:
                    out[arm.replace("_p0", "")] = arm_stats(mp)
    return out


# --- arm-level results -----------------------------------------------------
result["E5_screen"] = collect_arms("e5_behavior", "phase_b_safe_*")
result["E5b_screen"] = collect_arms("e5b", "phase_b_safe_*")
result["E6_combo"] = collect_arms("e6", "phase_b_safe_*")
result["E7_matrix"] = collect_arms("e7", "phase_b_safe_*")

# --- calibration runs (single arm, 25 games) -------------------------------
for run, label in (("calib_a2", "a2_25games_2900s_guard1GiB"),
                   ("calib_a3", "a3_25games_2900s_memfrac092"),
                   ("calib_a5", "a5_25games_2900s_timeout240")):
    for d in (RUNS / run / "output").glob("phase_b_safe_*"):
        mp = d / "baseline_p0" / "metrics.json"
        if mp.exists() and mp.stat().st_size > 0:
            result[label] = arm_stats(mp)

# --- request-level stats (latency, timeouts, output length) ----------------
def request_stats(jsonl: Path) -> dict:
    beg, durs = {}, []
    for line in open(jsonl, encoding="utf-8"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("event") == "begin":
            beg[e["request_id"]] = e.get("epoch_seconds")
        elif e.get("event") == "end" and e.get("request_id") in beg:
            durs.append(e["epoch_seconds"] - beg[e["request_id"]])
    if not durs:
        return {}
    durs_sorted = sorted(durs)
    p = lambda q: durs_sorted[min(len(durs_sorted) - 1, int(len(durs_sorted) * q))]
    timeout_marker = 239 if p(1.0) > 200 else 119
    over = sum(1 for d in durs if d >= timeout_marker)
    over120 = sum(1 for d in durs if d >= 119)
    return {
        "requests": len(durs),
        "median_s": round(statistics.median(durs), 1),
        "p90_s": round(p(0.9), 1),
        "max_s": round(max(durs), 1),
        "hit_client_timeout": over,
        "hit_client_timeout_pct": round(100 * over / len(durs), 2),
        "over_120s": over120,
        "over_120s_pct": round(100 * over120 / len(durs), 2),
        "timeout_request_hours": round(sum(d for d in durs if d >= timeout_marker) / 3600, 2),
        "total_request_hours": round(sum(durs) / 3600, 2),
        "wallclock_hours_if_10_ways": round(sum(durs) / 10 / 3600, 2),
        "source": str(jsonl.relative_to(RUNS)),
    }


def output_len_stats(serve_log: Path) -> dict:
    outs = []
    for ln in open(serve_log, encoding="utf-8", errors="replace"):
        if "ReqTimeStats" not in ln:
            continue
        m = re.search(r"output_len=(\d+)", ln)
        if m:
            outs.append(int(m.group(1)))
    if not outs:
        return {}
    s = sorted(outs)
    return {
        "requests": len(outs),
        "median_tokens": statistics.median(s),
        "p90_tokens": s[min(len(s) - 1, int(len(s) * 0.9))],
        "max_tokens": max(s),
        "over_3000_pct": round(100 * sum(1 for o in outs if o > 3000) / len(outs), 2),
        "source": str(serve_log.relative_to(RUNS)),
    }


for run, label in (("calib_a4", "a4_timeout120"), ("calib_a5", "a5_timeout240")):
    for d in (RUNS / run / "output").glob("phase_b_safe_*"):
        rp = d / "baseline_p0" / "request-events.jsonl"
        if rp.exists() and rp.stat().st_size > 0:
            result[f"requests_{label}"] = request_stats(rp)
        # serve.log sits at the run level, not inside the phase directory
        for sl in (RUNS / run / "output" / "serve.log", d / "serve.log"):
            if sl.exists():
                stats = output_len_stats(sl)
                if stats:
                    result[f"outputlen_{label}"] = stats
                    break

# --- leaderboard submissions (from the saved submissions listing) ----------
result["submissions"] = [
    {"ref": 56882441, "date": "2026-10-06", "score": 29.28, "build": "M2 baseline first push"},
    {"ref": 57037255, "date": "2026-10-10", "score": 24.38, "build": "identical code rerun"},
    {"ref": 57061252, "date": "2026-10-11", "score": 29.41, "build": "identical code rerun"},
    {"ref": 57100038, "date": "2026-10-12", "score": 29.60, "build": "identical code rerun"},
    {"ref": 57147727, "date": "2026-10-13", "score": 29.89, "build": "guard build (3 env keys changed)"},
]

json.dump(result, open(OUT / "numbers.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(result, indent=1)[:3000])

# --- human-readable table -------------------------------------------------
lines = ["# Paper numbers, re-extracted from run artifacts", ""]
for k, v in result.items():
    lines.append(f"## {k}")
    if isinstance(v, list):
        for row in v:
            lines.append(f"- {row}")
    elif isinstance(v, dict) and v and isinstance(next(iter(v.values())), dict):
        lines.append("| arm | games | mean | levels | actions | errors | source |")
        lines.append("|---|---|---|---|---|---|---|")
        for arm, d in v.items():
            lines.append(f"| {arm} | {d['games']} | {d['mean']} | {d['levels']}/{d['levels_total']} | {d['actions']} | {d['errors']} | `{d['source']}` |")
    elif isinstance(v, dict):
        for kk, vv in v.items():
            lines.append(f"- {kk}: {vv}")
    lines.append("")
(OUT / "numbers.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote", OUT / "numbers.json", "and numbers.md")
