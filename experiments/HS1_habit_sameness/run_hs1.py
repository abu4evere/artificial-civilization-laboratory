"""HS1 — habit sameness: same world or same nature? (questions.md, frozen as `HS1-frozen`.) Read-only replays of TC1's
code and worlds (arms W and N) with an observer that keeps habit tables; the analysis pairs children with strangers
from their own world and from another world.

  python experiments/HS1_habit_sameness/run_hs1.py zero     # observer leaves the world unchanged (hard stop)
  python experiments/HS1_habit_sameness/run_hs1.py run      # 2 arms x 32 seeds, 80 years (skips saved worlds)
  python experiments/HS1_habit_sameness/run_hs1.py smoke    # throwaway: seeds 9601-9602, 25 years, both arms
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "TC1_talk_copying"))
import run_tc1 as T  # noqa: E402

R = T.R
OUT = HERE / "output"
SEEDS = R.DISCOVERY
ARMS = {"w": T.ARMS["w"], "n": T.ARMS["n"]}
YEARS = 80
WPY = R.WPY
POOL = 8


def tab(q):
    return [float(f"{v:.6g}") for v in q]


class Obs:
    """Reads the world after each week; its own random stream; writes nothing to the world."""

    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.kids = {}        # child id -> [birth year, parents' mean table, same-world stranger table or None]
        self.done = []        # [birth year, child at 20, parents, same-world stranger]
        self.pool = {}        # year -> [tables]
        self.seen = set()

    def __call__(self, world, events):
        tick = world.tick - 1
        for e in events:
            if e["k"] == "birth" and e.get("b") not in self.seen:
                self.birth(world, e)
        for pid in list(self.kids):
            p = world.people[pid]
            if not p.alive:
                del self.kids[pid]
            elif world.tick - p.birth == 20 * WPY:
                by, par, sham = self.kids.pop(pid)
                self.done.append([by, tab(p.q), par, sham])
        if tick % WPY == WPY - 1:
            adults = sorted((q for q in world.living() if q.years(world.tick) >= 16), key=lambda q: q.id)
            pick = self.rng.sample(adults, min(POOL, len(adults))) if adults else []
            self.pool[tick // WPY] = [tab(q.q) for q in pick]

    def birth(self, world, e):
        child = world.people.get(e.get("b"))
        if child is None:
            return
        self.seen.add(child.id)
        mother = world.people[e["a"]]
        father = world.people.get(e.get("father")) if e.get("father") else None
        f = father if father is not None and father.alive else mother      # as the birth rule does
        # Read at the week's end: a parent who died that week has an empty table; use the other, or none.
        tabs = [np.asarray(x.q) for x in (mother, f) if len(x.q)]
        par = tab(sum(tabs) / len(tabs)) if tabs else None
        cands = sorted((q for q in world.living() if q.id not in (mother.id, f.id, child.id)
                        and q.years(world.tick) >= 16 and world.kinship(child, q) == 0 and world.kinship(q, child) == 0),
                       key=lambda q: q.id)
        sham = tab(cands[self.rng.randrange(len(cands))].q) if cands else None
        self.kids[child.id] = [(world.tick - 1) // WPY, par, sham]


def run(arm, seed, years, observe):
    R.setup("tc1")
    w = T.make_world(seed, ARMS[arm])
    o = Obs(seed) if observe else None
    if o:
        w.observers.append(o)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    return w, o


def one(arm, seed, years=YEARS, out=OUT):
    w, o = run(arm, seed, years, True)
    out.mkdir(parents=True, exist_ok=True)
    res = {"arm": arm, "seed": seed, "years": years, "final_tick": w.tick, "alive_end": len(w.living()),
           "world_hash": R.world_hash(w) if hasattr(R, "world_hash") else w.state_hash(),
           "children": o.done, "pool": {str(k): v for k, v in o.pool.items()}}
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: {len(o.done)} children reached 20; alive {len(w.living())}", flush=True)


def _hash(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode or not r.stdout.split():
        sys.exit("hash run failed: " + " ".join(cmd[2:]) + chr(10) + r.stderr[-2000:])
    return r.stdout.split()[-1]


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]
    lines, ok = [], True
    for arm in ARMS:
        for seed in (501, 601):
            a, b = (_hash(me + ["hash", arm, str(seed), obs]) for obs in ("1", "0"))
            t = a == b
            ok &= t
            lines.append(f"arm {arm}, seed {seed}, 20 years: identical with and without the observer: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}")
    return ok


def batch(seeds, years=YEARS, out=OUT):
    if not (OUT / "zero.txt").exists() or "All: PASS" not in (OUT / "zero.txt").read_text(encoding="utf-8"):
        sys.exit("ABORT: zero check has not passed")
    me = [sys.executable, str(Path(__file__).resolve())]
    jobs = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    list(ThreadPoolExecutor(2).map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), jobs))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hash":
        w, _ = run(sys.argv[2], int(sys.argv[3]), 20, sys.argv[4] == "1")
        print(w.state_hash())
    elif cmd == "one":
        one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "run":
        batch(SEEDS)
    elif cmd == "smoke":
        batch((9601, 9602), years=25, out=HERE / "output_smoke")
