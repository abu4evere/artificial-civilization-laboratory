"""HF1 — did food run short around HB1's homes? (questions.md, frozen as `HF1-questions`). Read-only replays, first 40
years, arms H (HB1, home_base = 1) and C (the same code, settings off), with an observer that measures wild plant
fullness around each couple's home, foraging returns, load near home, and food around adults before starvation deaths.

  python experiments/HF1_home_food/run_hf1.py verify       # observer read-only (H and C, two seeds, 20 years)
  python experiments/HF1_home_food/run_hf1.py discovery    # seeds 501-516, checked against HB1's and F1's saved runs
  python experiments/HF1_home_food/run_hf1.py holdout      # seeds 1301-1316 (after the discovery write-up)
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "HB1_home_base"))
import run_hb1 as HB  # noqa: E402

OUT = HERE / "output"
WPY, YEARS = 52, 40
DISCOVERY = tuple(range(501, 517))
HOLDOUT = tuple(range(1301, 1317))
ARMS = {"h": {"home_base": 1}, "c": {}}
SAVED = {"h": EXP / "HB1_home_base" / "output", "c": EXP / "F1_baseline_fragility" / "output"}


class Probe:
    """Reads the world after each week; draws no random numbers; writes nothing to the world."""

    def __init__(self):
        self.pops = []
        self.n = Counter()
        self.recent = {}                      # adult id -> last 8 weeks of fullness within 3 tiles of where they were
        self.week_mean = deque(maxlen=8)      # mean of that measure over all adults, last 8 weeks

    def fullness(self, world, centre, r0, r1):
        """Mean plants ÷ cap over land tiles with a cap whose distance from centre is in [r0, r1]. The cap is the code's,
        read live (plant_cap × the tile's fertility now: floods raise fertility). Food dropped by the dead is added to
        plants and can take a tile above its cap; such values are kept, as the frozen definition is plants ÷ cap."""
        c = world.cfg
        tot = k = 0
        for dy in range(-r1, r1 + 1):
            for dx in range(-r1, r1 + 1):
                if max(abs(dx), abs(dy)) < r0:
                    continue
                x, y = (centre[0] + dx) % c.width, (centre[1] + dy) % c.height
                tl = world.tiles[y][x]
                cap = 0.0 if tl.water else c.plant_cap * tl.fertility
                if cap > 0:
                    tot += tl.plants / cap
                    k += 1
        return (tot / k if k else None), k

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick
        t = tick - 1
        living = world.living()
        if t % 520 == 519:
            self.pops.append(len(living))
        n = self.n
        season = world.season
        adult = lambda p: p.age(tick) >= 16 * WPY
        n["person_weeks"] += len(living)
        # couples and their homes
        homes = {}
        for p in living:
            if not adult(p) or not p.partner or p.id in homes:
                continue
            q = world.people[p.partner]
            if not q.alive or not adult(q):
                continue
            h = world.couple_home(p, q)
            homes[p.id] = homes[q.id] = h
            if h is None:
                continue
            n["couple_weeks"] += 1
            f_in, k_in = self.fullness(world, h, 0, c.reach)
            f_ring, _ = self.fullness(world, h, 4, 6)
            if f_in is not None:
                n["full_in_sum"] += f_in
                n["full_in_n"] += 1
                n[f"full_in_s{season}_sum"] += f_in
                n[f"full_in_s{season}_n"] += 1
            if f_ring is not None:
                n["full_ring_sum"] += f_ring
                n["full_ring_n"] += 1
            people = sum(1 for x in living if distance(x.loc, h, c.width, c.height) <= c.reach)
            if k_in:
                n["load_sum"] += people / k_in
                n["load_n"] += 1
        # foraging returns
        for e in events:
            if e["k"] == "hunt":
                n["hunts"] += 1
            if e["k"] != "forage" or "a" not in e:
                continue
            p = world.people[e["a"]]
            if not adult(p):
                continue
            got = e.get("got", 0.0)
            at = tuple(e["at"])
            h = homes.get(p.id)
            where = "nohome" if h is None else "near" if distance(at, h, c.width, c.height) <= c.reach else "far"
            n["forage_n"] += 1
            n["forage_got"] += got
            n[f"forage_{where}_n"] += 1
            n[f"forage_{where}_got"] += got
            n["forage_emptied"] += world.tiles[at[1]][at[0]].plants < 1.0
        # before starvation deaths
        for e in events:
            if e["k"] == "death" and e.get("cause") == "starvation" and (e.get("age") or 0) >= 16:
                hist = self.recent.get(e["a"])
                if hist and self.week_mean:
                    n["starved_n"] += 1
                    n["starved_full_sum"] += sum(hist) / len(hist)
                    n["all_full_sum"] += sum(self.week_mean) / len(self.week_mean)
        vals = []
        for p in living:
            if adult(p):
                f, _ = self.fullness(world, p.loc, 0, c.reach)
                if f is not None:
                    self.recent.setdefault(p.id, deque(maxlen=8)).append(f)
                    vals.append(f)
        if vals:
            self.week_mean.append(sum(vals) / len(vals))
        alive = {p.id for p in living}
        for pid in [k for k in self.recent if k not in alive]:
            del self.recent[pid]              # deaths were read above, before this cleanup

    def results(self):
        return {"pops": self.pops, "n": dict(self.n)}


def run_one(arm, seed, years=YEARS, out=None):
    HB.setup("hb1")
    f0 = HB.fingerprint()
    w = HB.make_world(seed, **ARMS[arm])
    probe = Probe()
    w.observers.append(probe)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": HB.fingerprint(),
           **probe.results()}
    saved = SAVED[arm] / (f"h_seed_{seed}.json" if arm == "h" else f"seed_{seed}.json")
    if saved.exists():
        sp = json.loads(saved.read_text(encoding="utf-8"))["pops"][: years // 10]
        res["reproduces"] = sp == probe.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: pops {probe.pops}, reproduces saved: {res.get('reproduces')}", flush=True)


def verify(seeds=(501, 1301), years=20):
    HB.setup("hb1")
    lines, ok = [], True
    for arm, kw in ARMS.items():
        for seed in seeds:
            hs = []
            for with_probe in (False, True):
                w = HB.make_world(seed, **kw)
                if with_probe:
                    w.observers.append(Probe())
                for _ in range(years * WPY):
                    w.step()
                hs.append(w.state_hash())
            t = hs[0] == hs[1]
            ok &= t
            lines.append(f"observer, arm {arm}, seed {seed}, {years} years: {'READ-ONLY' if t else 'CHANGES THE WORLD'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    return ok


def batch(seeds):
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for a in ARMS for s in seeds if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), todo))
    R = [json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in ARMS for s in seeds]
    bad = [(r["arm"], r["seed"]) for r in R if r.get("reproduces") is False or r["code_hash"] != r["code_hash_after"]]
    print("ALL REPRODUCE, CODE UNCHANGED" if not bad else f"HARD STOP: {bad}", flush=True)
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "verify":
        sys.exit(0 if verify() else 1)
    elif cmd in ("discovery", "holdout"):
        sys.exit(0 if batch(DISCOVERY if cmd == "discovery" else HOLDOUT) else 1)
