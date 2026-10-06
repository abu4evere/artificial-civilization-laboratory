"""V1 — what do ACL's existing bad years do? (questions.md). Read-only replays of E13R's control (Arm A), seeds 501-516,
recording one row per year.

  python experiments/V1_bad_years/run_v1.py all
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E13R = HERE.parent / "E13R_replication"
CODE = E13R / "code_e13r"
SEEDS = tuple(range(501, 517))
WPY, WPS = 52, 13
OUT = HERE / "output"


def setup():
    sys.path.insert(0, str(CODE))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


class Probe:
    def __init__(self):
        self.pops = []
        self.years = []
        self.cur = None
        self.land = None
        self.max_ed = defaultdict(float)

    def new_row(self, world, year, living):
        return {"year": year, "weather": world.weather, "wet": world.sky.get("wet"), "hard": world.sky.get("hard"),
                "pop_start": len(living), "autumn_tile": None, "winter_tile": None, "autumn_pp": None, "winter_pp": None,
                "adult_starved_winter": 0, "child_starved_winter": 0, "starved_all": 0, "short_weeks": 0,
                "adult_winter_weeks": 0, "planners": 0, "adults_autumn": 0, "stock_need": None, "carers_stash": [0, 0],
                "seed_sown": 0.0, "expect_short_winter": None}

    def __call__(self, world, events):
        c = world.cfg
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        if self.land is None:
            self.land = [t for row in world.tiles for t in row if not t.water]
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        if wk == 0:
            if self.cur is not None:
                self.years.append(self.cur)
            self.cur = self.new_row(world, year, living)
            self.max_ed = defaultdict(float)
        r = self.cur
        if r is None:
            return
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        for e in events:
            if e["k"] == "death" and e.get("cause") == "starvation":
                r["starved_all"] += 1
                if s == 3:
                    if e.get("age", 0) >= 16:
                        r["adult_starved_winter"] += 1
                    elif e.get("age", 99) < 12:
                        r["child_starved_winter"] += 1
            elif e["k"] == "put" and e.get("thing") == "seeds" and e.get("into") == "ground":
                r["seed_sown"] += e.get("amount", 0.0) * 0.85
        if s == 3:
            r["adult_winter_weeks"] += len(adults)
            r["short_weeks"] += sum(1 for p in adults if p.starving)
        if s == 2:
            for p in adults:
                self.max_ed[p.id] = max(self.max_ed[p.id], p.edible())
        if wk % WPS == 6 and s in (2, 3):
            total = sum(t.plants + t.crop for t in self.land)
            r["autumn_tile" if s == 2 else "winter_tile"] = round(total / len(self.land), 3)
            r["autumn_pp" if s == 2 else "winter_pp"] = round(total / len(living), 1) if living else None
        if wk == 3 * WPS:
            r["planners"] = sum(1 for v in self.max_ed.values() if v >= 80)
            r["adults_autumn"] = len(self.max_ed)
            stash = defaultdict(float)
            for row in world.tiles:
                for t in row:
                    for st in t.stash or ():
                        stash[st[0]] += st[1] + st[2]
            ratios = []
            for p in adults:
                deps = world.dependents(p.id)
                if deps:
                    r["carers_stash"][1] += 1
                    r["carers_stash"][0] += stash.get(p.id, 0.0) > 0
                    stock = p.edible() + sum(d.edible() for d in deps) + stash.get(p.id, 0.0)
                    need = 13 * (p.need(c, world.tick) + sum(d.need(c, world.tick) for d in deps))
                    ratios.append(stock / need)
            r["stock_need"] = round(statistics.median(ratios), 4) if ratios else None
            ex = [p.expect.get("short@3", 0.0) for p in adults]
            r["expect_short_winter"] = round(statistics.mean(ex), 4) if ex else None

    def results(self):
        if self.cur is not None:
            self.years.append(self.cur)
        return {"pops": self.pops, "years": self.years}


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
