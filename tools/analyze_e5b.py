"""E5b six-arm analysis: per-arm scores/levels/actions + drift + E5 replication.

Usage: python analyze_e5b.py <phase_dir>
"""
import json
import statistics
import sys
from pathlib import Path

ARMS = ["baseline", "noop_guard", "inventory", "memory_slim", "drain60", "baseline_rep"]


def load_arm(phase: Path, arm: str):
    for name in (f"{arm}_p0",):
        d = phase / name
        if not (d / "metrics.json").exists():
            continue
        m = json.load(open(d / "metrics.json", encoding="utf-8"))
        games = m["games"] if isinstance(m, dict) and "games" in m else m
        by_id = {g["game_id"]: g for g in games}
        def sc(g):
            return g.get("native_final_score") or g.get("score") or 0.0
        return {
            "games": by_id,
            "mean": statistics.mean(sc(g) for g in games),
            "levels": sum(g.get("levels_completed") or 0 for g in games),
            "total_levels": sum(g.get("number_of_levels") or 0 for g in games),
            "actions": sum(g.get("actual_actions") or 0 for g in games),
            "errors": sum(g.get("error_count") or 0 for g in games),
            "nonzero": sum(1 for g in games if sc(g) > 0),
            "state": None,
        }
    return None


def main():
    phase = Path(sys.argv[1])
    st_path = phase / "batch-status.json"
    if not st_path.exists():
        st_path = phase.parent / "batch-status-from-log.json"
    st = json.load(open(st_path, encoding="utf-8"))
    print(f"批次状态: {st['status']} | complete={st['complete']} | 总耗时 {st.get('whole_batch_elapsed_seconds', 0):.0f}s")
    for w in st.get("workers", []):
        print(f"   {w['worker']['profile']:14s} {w['status']:28s} rows={w.get('row_count')} finished={w.get('native_finished_games')}")
    data = {}
    for arm in ARMS:
        d = load_arm(phase, arm)
        if d:
            data[arm] = d
    print(f"\n{'arm':14s} {'均值':>7s} {'关卡':>9s} {'动作':>6s} {'错误':>6s} {'非0局':>5s}")
    for arm in ARMS:
        if arm in data:
            d = data[arm]
            print(f"{arm:14s} {d['mean']:7.3f} {d['levels']:4d}/{d['total_levels']:<4d} {d['actions']:6d} {d['errors']:6d} {d['nonzero']:5d}")
        else:
            print(f"{arm:14s}   ——")
    if "baseline" in data and "baseline_rep" in data:
        b, r = data["baseline"], data["baseline_rep"]
        print(f"\n漂移对照: baseline {b['mean']:.3f} vs baseline_rep {r['mean']:.3f} → 差 {r['mean']-b['mean']:+.3f}（|差|≥3 说明整场漂移大）")
    if "baseline" in data:
        print("\n候选 vs baseline（逐局）:")
        b = data["baseline"]["games"]
        for arm in ARMS:
            if arm in ("baseline",) or arm not in data:
                continue
            wins = ties = losses = 0
            rows = []
            for gid in sorted(b):
                if gid not in data[arm]["games"]:
                    continue
                sb = b[gid].get("native_final_score") or b[gid].get("score") or 0.0
                sa = data[arm]["games"][gid].get("native_final_score") or data[arm]["games"][gid].get("score") or 0.0
                if abs(sa - sb) < 0.01:
                    ties += 1
                elif sa > sb:
                    wins += 1
                else:
                    losses += 1
                if abs(sa - sb) > 5:
                    rows.append(f"      {gid}: {sb:.1f} -> {sa:.1f}")
            print(f"  {arm:14s} 胜 {wins} 平 {ties} 负 {losses} | 均值差 {data[arm]['mean']-data['baseline']['mean']:+.3f} | 关卡差 {data[arm]['levels']-data['baseline']['levels']:+d}")
            for r_ in rows:
                print(r_)


if __name__ == "__main__":
    main()
