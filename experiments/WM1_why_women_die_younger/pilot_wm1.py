"""WM1 feasibility pilot (throwaway; not used for any result). Counts adult deaths by sex in 8 C20 worlds on live v7.

  python experiments/WM1_why_women_die_younger/pilot_wm1.py

Rule (questions.md, Revision 1): if the projected number of adult female deaths per arm (128 C20 worlds) is under
2,000, the seeds go up to 256. Adult = world-born, died aged 16-54.
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
SEEDS = range(99001, 99009)
WPY = 52


def one(seed):
    from acl.config import Config
    from acl.world import World
    w = World(Config(seed=seed, anticipation_weight=1.0))
    for _ in range(120 * WPY):
        if not w.living():
            break
        w.step()
    n = {"F": 0, "M": 0}
    for p in w.people.values():
        if p.birth >= 0 and not p.alive and 16 * WPY <= p.death_tick - p.birth < 55 * WPY:
            n[p.sex] += 1
    return seed, n


if __name__ == "__main__":
    with ProcessPoolExecutor(8) as ex:
        rows = list(ex.map(one, SEEDS))
    f = sum(r[1]["F"] for r in rows)
    m = sum(r[1]["M"] for r in rows)
    for s, n in rows:
        print(f"seed {s}: adult deaths F {n['F']}, M {n['M']}")
    proj = f / len(rows) * 128
    print(f"total F {f}, M {m}; projected adult female deaths per arm of 128 worlds: {proj:.0f}")
    print("seeds per arm: " + ("128" if proj >= 2000 else "256 (under 2,000)"))
