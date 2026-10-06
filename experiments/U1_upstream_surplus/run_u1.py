"""U1 — why there is no surplus to store (questions.md). Read-only replays of E13R's control (Arm A), seeds 501-516.

  python experiments/U1_upstream_surplus/run_u1.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E13R = HERE.parent / "E13R_replication"
CODE = E13R / "code_e13r"
SEEDS = tuple(range(501, 517))
WPY, WPS = 52, 13
AUTUMN = 2
OUT = HERE / "output"
FOOD_BANDS = ("under 0.5", "0.5-1", "1-2", "2-4", "4+")


def setup():
    sys.path.insert(0, str(CODE))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def fband(weeks):
    return ("under 0.5" if weeks < 0.5 else "0.5-1" if weeks < 1 else "1-2" if weeks < 2
            else "2-4" if weeks < 4 else "4+")


class Probe:
    def __init__(self):
        self.pops = []
        self.actions = defaultdict(Counter)          # season -> chosen action counts (adults)
        self.n = defaultdict(lambda: defaultdict(float))
        self.by_band = defaultdict(lambda: [0, 0])  # autumn: food band -> [forage weeks, weeks]
        self.potential = defaultdict(float)          # (year, pid) -> autumn potential from non-forage weeks
        self.gathered = defaultdict(float)           # (year, pid) -> autumn gathered
        self.land = []                               # autumn start/end: reachable plant food per adult
        self.last_loc = {}
        self.last_food = {}                          # pid -> food held at the end of last week (at decision)

    def reachable_food(self, world, adults):
        c = world.cfg
        seen = set()
        for p in adults:
            x0, y0 = p.loc
            for dy in range(-c.reach, c.reach + 1):
                for dx in range(-c.reach, c.reach + 1):
                    seen.add(((x0 + dx) % c.width, (y0 + dy) % c.height))
        food = sum(world.tile(t).plants + world.tile(t).crop for t in seen)
        return food, len(seen)

    def __call__(self, world, events):
        from acl.matter import carry_capacity
        from acl.mind import forage_rate
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        if tick % 520 == 519:
            self.pops.append(len(world.living()))
        c = world.cfg
        adults = [p for p in world.living() if p.age(world.tick) >= 16 * WPY]
        got = defaultdict(float)
        for e in events:
            if e["k"] == "forage":
                got[e["a"]] += e.get("got", 0.0)
        n = self.n[s]
        for p in adults:
            chosen = next((x[0] for x in (p.considered or []) if x[3]), None)
            self.actions[s][chosen or "none"] += 1
            n["weeks"] += 1
            prev = self.last_loc.get(p.id)
            if prev is not None:
                dx = min(abs(p.loc[0] - prev[0]), c.width - abs(p.loc[0] - prev[0]))
                dy = min(abs(p.loc[1] - prev[1]), c.height - abs(p.loc[1] - prev[1]))
                n["moved"] += max(dx, dy)
            rate = forage_rate(world, p)
            cap = carry_capacity(world, p)
            if p.id in got:
                n["forage_weeks"] += 1
                n["forage_got"] += got[p.id]
                n["forage_rate"] += rate
            if s == AUTUMN:
                deps = world.dependents(p.id)
                need = p.need(c, world.tick) + sum(d.need(c, world.tick) for d in deps)
                held = self.last_food.get(p.id, p.edible())      # what they held when they chose
                b = self.by_band[fband(held / need)]
                b[1] += 1
                b[0] += chosen == "forage"
                n["near_cap"] += p.edible() >= 0.9 * cap
                if p.id in got:
                    self.gathered[(year, p.id)] += got[p.id]
                else:
                    t = world.tile(p.loc)
                    room = max(0.0, cap - held)
                    self.potential[(year, p.id)] += min(rate, t.plants + t.crop, room)
        self.last_loc = {p.id: p.loc for p in adults}
        self.last_food = {p.id: p.edible() for p in adults}
        if s == AUTUMN and wk in (2 * WPS, 3 * WPS - 1) and adults:
            food, tiles = self.reachable_food(world, adults)
            self.land.append({"when": "start" if wk == 2 * WPS else "end", "food_per_adult": round(food / len(adults), 1),
                              "tiles": tiles, "adults": len(adults)})

    def results(self):
        keys = set(self.potential) | set(self.gathered)
        rows = [[round(self.gathered.get(k, 0.0), 1), round(self.potential.get(k, 0.0), 1)] for k in keys]
        return {"pops": self.pops, "actions": {str(s): dict(v) for s, v in self.actions.items()},
                "n": {str(s): dict(v) for s, v in self.n.items()}, "by_band": dict(self.by_band),
                "autumn_rows": rows, "land": self.land}


def run(seed):
    setup()
    w = make_world(seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((E13R / "output" / f"a_seed_{seed}.json").read_text(encoding="utf-8"))
    res = {"seed": seed, "replay_matches": probe.pops == saved["pops"], **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches']}", flush=True)


def verify(seed=501, years=20):
    setup()
    hs = []
    for with_probe in (False, True):
        w = make_world(seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "verify.txt").write_text(f"seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n",
                                    encoding="utf-8")
    print("verify:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        if subprocess.call(me + ["verify"]) != 0:
            sys.exit("ABORT: probe changes the world")
        jobs = [s for s in SEEDS if not (OUT / f"seed_{s}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), jobs))
        print("ALL DONE", flush=True)
    elif sys.argv[1] == "verify":
        sys.exit(0 if verify() else 1)
    else:
        run(int(sys.argv[1]))
