# -*- coding: utf-8 -*-
"""Cover card for the Kaggle Media Gallery, 1200x630."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

FIG = Path(__file__).resolve().parent.parent / "figures"
fig = plt.figure(figsize=(6.0, 3.15), dpi=200)
fig.patch.set_facecolor("#0f1b2d")
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.set_facecolor("#0f1b2d")

ax.text(0.06, 0.83, "Before Tuning the Harness", color="#ffffff", fontsize=21,
        fontweight="bold", transform=ax.transAxes)
ax.text(0.06, 0.70, "Repeat-controlled evaluation and request-level accounting\nfor ARC-AGI-3",
        color="#9fb6d4", fontsize=10.5, transform=ax.transAxes, va="top", linespacing=1.5)

ax.plot([0.06, 0.94], [0.55, 0.55], color="#31507a", lw=1.2, transform=ax.transAxes)

ax.text(0.06, 0.44, "3.33 / 3.20 / 1.23", color="#ffcf6b", fontsize=17, fontweight="bold",
        transform=ax.transAxes)
ax.text(0.06, 0.35, "same-configuration gaps in three sessions, same games, same code",
        color="#c9d6e6", fontsize=8.8, transform=ax.transAxes)

ax.text(0.06, 0.22, "37.5%", color="#ffcf6b", fontsize=17, fontweight="bold",
        transform=ax.transAxes)
ax.text(0.06, 0.13, "of one run's request time went to requests our own client cut off",
        color="#c9d6e6", fontsize=8.8, transform=ax.transAxes)

ax.text(0.94, 0.06, "Guoyi Zhang  |  Shandong First Medical University  |  ARC Prize 2026",
        color="#7f97b5", fontsize=7.6, ha="right", transform=ax.transAxes)

fig.savefig(FIG / "cover.png", facecolor=fig.get_facecolor())
print("cover:", FIG / "cover.png")
