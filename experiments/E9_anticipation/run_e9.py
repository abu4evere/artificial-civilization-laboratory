"""E9 runner (E9_preregistration.md). Arms: arm0 (E7 code), a2low (A2 code, 0.375), a2full (A2 code, 1.0),
plus the zero-weight check (A2 code, 0.0, seed 304). Seeds 301–304, 120 years. Read-only probe.

  python experiments/E9_anticipation/run_e9.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
ARMS = {"arm0": (E7 / "code_e7", None), "a2low": (HERE / "code_a2", 0.375), "a2full": (HERE / "code_a2", 1.0),
        "zero": (HERE / "code_a2", 0.0)}
SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output"


def setup(arm):
    sys.path.insert(0, str(ARMS[arm][0]))
    sys.path.insert(1, str(E7))
    import acl
    assert Path(acl.__file__).resolve().parent == (ARMS[arm][0] / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    w = ARMS[arm][1]
    return World(Config(seed=seed) if w is None else Config(seed=seed, anticipation_weight=w))


class Probe:
    def __init__(self):
        from acl.historian import classify
        self.classify = classify
        self.pops = []
        self.deaths = Counter()             # (cause, season) and infant deaths
        self.carriers_made = Counter()      # decade -> count
        self.short_winter_prev = {}         # pid -> went short in the winter just ended
        self.cur_winter = defaultdict(bool)
        self.ever_short_winter = set()
        self.autumn = defaultdict(lambda: {"weeks": 0, "forage": 0, "max_edible": 0.0})
        self.rows = []
        self.samples = []
        self.end_autumn_plants = []

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        c = world.cfg
        for e in events:
            if e["k"] == "death":
                self.deaths[f"{e.get('cause')}@{s}"] += 1
                if e.get("age", 99) < 1:
                    self.deaths["infant"] += 1
            elif e["k"] in ("make", "play") and e.get("thing"):
                props = {k: e[k] for k in ("edge", "reach", "hard", "contain", "warm", "float") if k in e}
                if props and "carrier" in self.classify(props):
                    self.carriers_made[tick // 520] += 1
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
            self._sample(world, tick, living)
        for p in living:
            if s == 3 and p.starving:
                self.cur_winter[p.id] = True
                self.ever_short_winter.add(p.id)
            if s == 2 and p.age(world.tick) >= 16 * WPY:
                a = self.autumn[p.id]
                a["weeks"] += 1
                a["max_edible"] = max(a["max_edible"], p.edible())
                ch = next((x[0] for x in (p.considered or []) if x[3]), None)
                a["forage"] += ch == "forage"
        if wk == WPY - 1:                    # end of winter (the year's last week): note who went short
            self.short_winter_prev = {pid: True for pid, v in self.cur_winter.items() if v}
            self.cur_winter.clear()
        if wk == 3 * WPS - 1:                # end of autumn: plants left
            self.end_autumn_plants.append(round(sum(t.plants + t.crop for row in world.tiles for t in row), 1))
        if wk == 3 * WPS:                    # first week of winter: close the autumn
            for p in living:
                a = self.autumn.pop(p.id, None)
                if not a or a["weeks"] < 10:
                    continue
                stored = 0.0
                for dy in range(-c.reach, c.reach + 1):
                    for dx in range(-c.reach, c.reach + 1):
                        t = world.tile(((p.loc[0] + dx) % c.width, (p.loc[1] + dy) % c.height))
                        stored += sum(st[1] + st[2] for st in t.stash)
                self.rows.append({"year": tick // WPY, "forage_share": round(a["forage"] / a["weeks"], 3),
                                  "short_prev_winter": bool(self.short_winter_prev.get(p.id)),
                                  "ever_short_winter": p.id in self.ever_short_winter,
                                  "max_edible": round(a["max_edible"], 1),
                                  "winter_entry": round(p.food + p.seeds + stored, 1)})
            self.autumn.clear()

    def _sample(self, world, tick, living):
        later = [p for p in living if p.birth > 30 * WPY and p.age(world.tick) >= 16 * WPY]
        held = Counter(sig for p in living for sig in p.recipes)
        carrier_worth = []
        for p in living:
            for sig in p.recipes:
                rec = world.knowledge.get(sig) or {}
                if rec.get("props") and "carrier" in self.classify(rec["props"]):
                    carrier_worth.append(p.itemval.get(sig, 0.0))
        self.samples.append({"year": tick // WPY + 1, "population": len(living),
                             "later_skill_mean": round(sum(p.skills["crafting"] for p in later) / len(later), 3) if later else None,
                             "recipes_unique": len(held),
                             "carrier_worth_mean": round(sum(carrier_worth) / len(carrier_worth), 4) if carrier_worth else None})


def fp(arm):
    from run_e7 import code_hash
    return code_hash(ARMS[arm][0] / "acl")


def run(arm, seed):
    setup(arm)
    f0 = fp(arm)
    w = make_world(arm, seed)
    probe = Probe()
    w.observers.append(probe)
    t0 = time.time()
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    sp = [x["population"] for x in saved["samples"]][: len(probe.pops)]
    res = {"arm": arm, "seed": seed, "years": w.year, "code_hash": f0, "code_hash_after": fp(arm),
           "matches_saved_e7": probe.pops == sp, "pops": probe.pops, "deaths": dict(probe.deaths),
           "carriers_made": {str(k): v for k, v in sorted(probe.carriers_made.items())}, "rows": probe.rows,
           "samples": probe.samples, "end_autumn_plants": probe.end_autumn_plants, "seconds": round(time.time() - t0)}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: {w.year} years, alive {len(w.living())}, matches saved E7 {res['matches_saved_e7']}, {res['seconds']}s", flush=True)


def verify(arm, seed=304, years=20):
    setup(arm)
    hs = []
    for with_probe in (False, True):
        w = make_world(arm, seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(exist_ok=True)
    with open(OUT / "verify.txt", "a", encoding="utf-8") as f:
        f.write(f"{arm} seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
    print(f"verify {arm}:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(0 if verify(sys.argv[2]) else 1)
    elif sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        for arm in ("arm0", "a2full"):
            if subprocess.call(me + ["verify", arm]) != 0:
                sys.exit("ABORT: probe changes the world")
        jobs = [("zero", 304)] + [(a, s) for a in ("arm0", "a2low", "a2full") for s in SEEDS]
        jobs = [j for j in jobs if not (OUT / f"{j[0]}_seed_{j[1]}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
        print("ALL DONE", flush=True)
    else:
        run(sys.argv[1], int(sys.argv[2]))
