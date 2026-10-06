"""Figures for the paper draft, from the committed outputs of F1 and F2.

    python paper/make_figures.py   -> paper/fig1_trajectories.png, fig2_timelines.png, fig3_f1_vs_f2.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
OUT = Path(__file__).parent
SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))
EXT, SUR, F2C = "#b5523b", "#3f6f8f", "#5a8a4a"
plt.rcParams.update({"font.family": "serif", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def load(out):
    R = {}
    for s in SEEDS:
        r = json.loads((out / f"seed_{s}.json").read_text(encoding="utf-8"))
        Y = {int(k): v for k, v in r["years"].items()}
        r["series"] = [Y.get(y, {}).get("n", 0) for y in range(120)]
        r["extinct"] = not (len(r["pops"]) == 12 and r["pops"][-1] > 0)
        r["E"] = (r["final_tick"] - 1) // 52 if r["extinct"] else None
        R[s] = r
    return R


C = load(EXP / "F1_baseline_fragility" / "output")
P = load(EXP / "F2_perfect_search" / "output")

# Figure 1: population trajectories of the 64 control worlds
fig, ax = plt.subplots(figsize=(6.5, 3.6))
for r in C.values():
    ax.plot(range(120), r["series"], color=EXT if r["extinct"] else SUR, alpha=0.55 if r["extinct"] else 0.35, lw=1)
ax.axhline(20, color="#888888", lw=0.8, ls="--")
ax.text(119, 21, "20 founders", ha="right", va="bottom", fontsize=8, color="#666666")
ax.set_xlabel("year")
ax.set_ylabel("population (mid-year)")
ax.plot([], [], color=SUR, label=f"survived to year 120 ({sum(not r['extinct'] for r in C.values())})")
ax.plot([], [], color=EXT, label=f"died out ({sum(r['extinct'] for r in C.values())})")
ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "fig1_trajectories.png", dpi=200)

# Figure 2: for each extinct control world, the years from its last birth to its last death
ext = sorted((r for r in C.values() if r["extinct"]), key=lambda r: r["E"])
fig, ax = plt.subplots(figsize=(6.5, 3.8))
for i, r in enumerate(ext):
    B = max(b[0] for b in r["births"])
    ax.plot([0, B], [i, i], color=SUR, lw=3, solid_capstyle="butt")
    ax.plot([B, r["E"]], [i, i], color=EXT, lw=3, solid_capstyle="butt")
ax.set_yticks(range(len(ext)))
ax.set_yticklabels([str(r["seed"]) for r in ext], fontsize=7)
ax.set_xlabel("year")
ax.set_ylabel("world (seed)")
ax.plot([], [], color=SUR, lw=3, label="births still occurring")
ax.plot([], [], color=EXT, lw=3, label="after the last birth")
ax.legend(frameon=False, fontsize=8, loc="lower right")
fig.tight_layout()
fig.savefig(OUT / "fig2_timelines.png", dpi=200)

# Figure 3: control vs perfect partner finding, same seeds
fig, axs = plt.subplots(1, 2, figsize=(6.8, 3.2))
for R, col, lab in ((C, SUR, "control (F1)"), (P, F2C, "perfect finding (F2)")):
    alive = [sum(1 for r in R.values() if r["series"][y] > 0) for y in range(120)]
    axs[0].plot(range(120), alive, color=col, lw=1.8, label=lab)
    med = [sorted(r["series"][y] for r in R.values())[len(R) // 2] for y in range(120)]
    axs[1].plot(range(120), med, color=col, lw=1.8, label=lab)
axs[0].set_xlabel("year")
axs[0].set_ylabel("worlds with anyone alive (of 64)")
axs[1].set_xlabel("year")
axs[1].set_ylabel("median population (all 64 worlds)")
axs[0].legend(frameon=False, fontsize=8, loc="lower left")
fig.tight_layout()
fig.savefig(OUT / "fig3_f1_vs_f2.png", dpi=200)
print("wrote fig1_trajectories.png, fig2_timelines.png, fig3_f1_vs_f2.png")
