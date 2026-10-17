# -*- coding: utf-8 -*-
"""Generate the four paper figures from artifacts. Outputs figures/fig1..4 .png/.svg"""
import json, glob, re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PAPER = Path(__file__).resolve().parent.parent
RUNS = PAPER.parent / "arc3-eng" / "runs"
FIG = PAPER / "figures"
FIG.mkdir(exist_ok=True)

def load_arm(metrics_path):
    m = json.load(open(metrics_path, encoding="utf-8"))
    per = {}
    for g in m.get("games") or []:
        per[str(g.get("game_id", "")).split("-")[0]] = float(g.get("native_final_score") or 0.0)
    return per

def arms_of(run):
    phases = sorted(glob.glob(str(RUNS / run / "out" / "phase_b_safe_*"))) + \
             sorted(glob.glob(str(RUNS / run / "output" / "phase_b_safe_*")))
    arms = {}
    for p in glob.glob(phases[-1] + "/*/metrics.json"):
        arms[Path(p).parent.name.replace("_p0", "")] = load_arm(p)
    return arms

# ---------- Figure 1: same-configuration variation ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

sessions = {
    "E5b": [("base", 14.90, "tab:blue"), ("guard", 20.43, "tab:red"), ("rpt\nbase", 18.22, "tab:blue")],
    "E6": [("base", 11.52, "tab:blue"), ("guard", 20.42, "tab:red"), ("rpt\nbase", 14.71, "tab:blue")],
    "E7": [("b1", 12.71, "tab:blue"), ("g1", 15.43, "tab:red"), ("b2", 13.53, "tab:blue"),
           ("g2", 18.66, "tab:red"), ("b3", 12.30, "tab:blue"), ("g3", 12.43, "tab:red")],
}
x0 = 0
xticks, xlabels = [], []
session_centers = {}
for sname, pts in sessions.items():
    xs = np.arange(len(pts)) + x0
    for (lab, val, col), x in zip(pts, xs):
        ax1.scatter([x], [val], color=col, zorder=3, s=45)
    # first-last bracket line for the bracketed sessions
    if sname in ("E5b", "E6"):
        first, last = pts[0][1], pts[-1][1]
        ax1.plot([xs[0], xs[-1]], [first, last], color="0.6", lw=1, ls=":", zorder=1)
        ax1.annotate(f"+{last-first:.2f}", (xs[-1], last), textcoords="offset points",
                     xytext=(6, -3), fontsize=9, color="0.35")
    xticks += list(xs); xlabels += [p[0] for p in pts]
    session_centers[sname] = float(np.mean(xs))
    x0 += len(pts) + 1.0
for sname, c in session_centers.items():
    ax1.text(c, 38.2, sname, fontsize=9.5, color="0.25", ha="center")
ax1.annotate("baseline spread 1.23 vs guard spread 6.23", (x0 - 0.5, 36.2),
             fontsize=8.5, color="0.35", ha="right")
ax1.set_xticks(xticks); ax1.set_xticklabels(xlabels, fontsize=8.5)
ax1.set_ylim(0, 40); ax1.set_xlim(-0.6, x0 - 0.3)
ax1.set_ylabel("local mean score (10 games)")
ax1.set_title("Within-session arms, same 10-game set", fontsize=10)
ax1.grid(axis="y", alpha=0.25)

lb = [29.28, 24.38, 29.41, 29.60]
grd = [29.89, 30.21]
ax2.scatter(np.zeros(len(lb)), lb, color="tab:blue", s=45, zorder=3)
ax2.scatter(np.ones(len(grd)) - 0.35, grd, color="tab:red", s=45, zorder=3)
ax2.axhline(np.mean(lb), color="tab:blue", lw=1, ls="--", alpha=0.6)
ax2.axhline(np.mean(grd), color="tab:red", lw=1, ls="--", alpha=0.6)
ax2.annotate(f"mean {np.mean(lb):.2f}", (-0.55, np.mean(lb)), fontsize=9, color="tab:blue", va="bottom")
ax2.annotate(f"mean {np.mean(grd):.2f}", (0.02, np.mean(grd)), fontsize=9, color="tab:red", va="bottom")
ax2.set_xticks([0, 0.65]); ax2.set_xticklabels(["one build,\n4 submissions", "guard build,\n2 submissions"], fontsize=9)
ax2.set_ylim(20, 34); ax2.set_xlim(-0.6, 1.15); ax2.set_ylabel("leaderboard score")
ax2.set_title("Leaderboard reruns", fontsize=10)
ax2.grid(axis="y", alpha=0.25)
fig.suptitle("Same configuration, different scores", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(FIG / "fig1-variation.png", dpi=200)
fig.savefig(FIG / "fig1-variation.svg")
plt.close(fig)

# ---------- Figures 2 and 3: request duration and output length (a4 vs a5) ----------
def serve_requests(run):
    rows = []
    for p in sorted(glob.glob(str(RUNS / run / "output" / "serve.log"))) + \
             sorted(glob.glob(str(RUNS / run / "out" / "phase_b_safe_*" / "serve.log"))):
        for line in open(p, encoding="utf-8", errors="replace"):
            m = re.search(r"output_len=(\d+).*?queue_duration=([\d.]+)ms, initial_prefill_elapsed=([\d.]+)ms, post_prefill_elapsed=([\d.]+)ms", line)
            if m:
                out_len = int(m.group(1))
                ms = float(m.group(2)) + float(m.group(3)) + float(m.group(4))
                rows.append((ms / 1000.0, out_len))
    return rows

r4 = serve_requests("calib_a4")
r5 = serve_requests("calib_a5")
print("a4 请求数:", len(r4), "| a5 请求数:", len(r5))

fig, ax = plt.subplots(figsize=(6.5, 4.2))
for rows, lab, col in ((r4, "a4: 120 s cap", "tab:orange"), (r5, "a5: 240 s cap", "tab:green")):
    d = np.sort(np.array([r[0] for r in rows]))
    y = np.arange(1, len(d) + 1) / len(d)
    ax.plot(d, 1 - y, label=lab, color=col, lw=1.5)  # survival function
ax.axvline(120, color="tab:orange", ls=":", lw=1)
ax.axvline(240, color="tab:green", ls=":", lw=1)
ax.text(112, 0.5, "120 s cap", color="tab:orange", fontsize=8.5, ha="right", rotation=90)
ax.text(255, 0.5, "240 s cap", color="tab:green", fontsize=8.5, ha="left", rotation=90)
ax.legend(fontsize=9)
ax.set_xscale("log"); ax.set_xlim(1, 400)
ax.set_xlabel("request duration (s, log scale)"); ax.set_ylabel("fraction of requests longer than x")
ax.set_title("Request duration survival, two calibration runs", fontsize=10)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(FIG / "fig2-duration.png", dpi=200)
fig.savefig(FIG / "fig2-duration.svg")
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 4.2))
for rows, lab, col in ((r4, "a4: 120 s cap", "tab:orange"), (r5, "a5: 240 s cap", "tab:green")):
    arr = np.array(rows)
    ax.scatter(arr[:, 0], arr[:, 1], s=4, alpha=0.25, color=col, label=lab)
ax.set_xlim(0, 260); ax.set_ylim(0, 13000)
ax.set_xlabel("request duration (s)"); ax.set_ylabel("generated tokens")
ax.set_title("Generated tokens against request duration", fontsize=10)
ax.legend(markerscale=3, fontsize=9)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(FIG / "fig3-tokens.png", dpi=200)
fig.savefig(FIG / "fig3-tokens.svg")
plt.close(fig)

# ---------- Figure 4: per-game guard deltas ----------
e5b, e6, e7 = arms_of("e5b"), arms_of("e6"), arms_of("e7")
games = sorted(e5b["baseline"].keys())
d5b = [e5b["noop_guard"].get(g, 0) - e5b["baseline"].get(g, 0) for g in games]
d6 = [e6["noop_guard"].get(g, 0) - e6["baseline"].get(g, 0) for g in games]
d7 = [( (e7["guard_1"].get(g,0)+e7["guard_2"].get(g,0)+e7["guard_3"].get(g,0))/3
       - (e7["base_1"].get(g,0)+e7["base_2"].get(g,0)+e7["base_3"].get(g,0))/3 ) for g in games]

fig, ax = plt.subplots(figsize=(7.5, 4.4))
xs = np.arange(len(games))
for off, d, lab, col, mk in ((-0.22, d5b, "E5b (guard vs baseline)", "tab:blue", "o"),
                             (0.0, d6, "E6 (guard vs baseline)", "tab:purple", "s"),
                             (0.22, d7, "E7 (mean 3 guards vs mean 3 baselines)", "tab:red", "^")):
    ax.scatter(xs + off, d, label=lab, color=col, marker=mk, s=38, zorder=3)
ax.axhline(0, color="0.4", lw=1)
ax.set_xticks(xs); ax.set_xticklabels(games, fontsize=9)
ax.set_ylabel("guard minus control, game score")
ax.set_title("Per-game guard effect across three sessions", fontsize=10)
ax.legend(fontsize=8.5)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(FIG / "fig4-pergame.png", dpi=200)
fig.savefig(FIG / "fig4-pergame.svg")
plt.close(fig)

print("四张图已生成:", [p.name for p in sorted(FIG.glob('*.png'))])
