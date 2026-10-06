"""D1 — is delayed return adaptive in ACL's world? (questions.md). Read-only replays of E13R's control (Arm A),
seeds 501-516.

  python experiments/D1_delayed_return_world/run_d1.py all
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
OUT = HERE / "output"


def setup():
    sys.path.insert(0, str(CODE))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def corr(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    if va <= 0 or vb <= 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (va * vb) ** 0.5


class Probe:
    def __init__(self):
        self.pops = []
        self.land = None
        self.samples = []                 # mid-season: year, season, top-10% share, total, people
        self.autumn_prev = None
        self.autumn_r = []                # year-to-year correlation of tiles' mid-autumn plant food
        self.sown_prev = {}               # tile -> seed in the ground after last week
        self.crop_prev = {}
        self.sowings = []                 # open and closed sowing records
        self.sown_by_season = Counter()
        self.sowers = set()
        self.crop_grown = 0.0
        self.crop_rotted = 0.0
        self.harvest = Counter()          # "sower" / "sower's kin" / "others" -> crop harvested from recently sown tiles
        self.recent_sowers = defaultdict(dict)   # tile -> {pid: last tick sown}

    def __call__(self, world, events):
        c = world.cfg
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        if self.land is None:
            self.land = [t for row in world.tiles for t in row if not t.water]
        if tick % 520 == 519:
            self.pops.append(len(world.living()))
        new_seed = defaultdict(float)
        for e in events:
            k = e["k"]
            if k == "put" and e.get("thing") == "seeds" and e.get("into") == "ground":
                loc = tuple(e["at"])
                amt = e.get("amount", 0.0) * 0.85          # 85% of seed put on open ground is sown
                new_seed[loc] += amt
                p = world.people.get(e["a"])
                self.sown_by_season[s] += amt
                self.sowers.add(e["a"])
                self.recent_sowers[loc][e["a"]] = world.tick
                self.sowings.append({"t": world.tick, "pid": e["a"], "loc": loc, "amt": round(amt, 2), "season": s,
                                     "b0": p.beliefs.get(f"seeds@{s}") if p else None, "returned": False,
                                     "first_crop": None, "crop_52": 0.0, "again": False, "b52": None, "open": True})
            elif k == "harvest":
                loc = tuple(e["at"])
                sowers = {pid for pid, t in self.recent_sowers.get(loc, {}).items() if world.tick - t <= WPY}
                if sowers:
                    a = e["a"]
                    q = world.people.get(a)
                    who = ("sower" if a in sowers else
                           "sower's kin" if q is not None and any(world.people.get(x) is not None and
                                                                  world.kinship(q, world.people[x]) >= 0.5 for x in sowers)
                           else "others")
                    self.harvest[who] += e.get("crop", 0.0)
        # crop grown this week, from the world's own rule, on every tile with seed in the ground
        growing = s in (0, 1)
        added = {}
        tiles = set(self.sown_prev) | set(new_seed)
        for loc in tiles:
            t = world.tile(loc)
            before = self.sown_prev.get(loc, 0.0) + new_seed.get(loc, 0.0)
            gone = max(0.0, before - t.sown)
            if growing and gone > 0:
                grown = gone * c.seed_multiplier * (0.4 + 0.6 * t.fertility)
                added[loc] = grown
                self.crop_grown += grown
        if s == 3:
            self.crop_rotted += sum(v for v in self.crop_prev.values()) * c.crop_rot
        self.sown_prev = {loc: world.tile(loc).sown for loc in tiles if world.tile(loc).sown > 0.01}
        self.crop_prev = {loc: world.tile(loc).crop for loc in set(self.crop_prev) | set(added) if world.tile(loc).crop > 0.01}
        # follow each sowing for a year
        for r in self.sowings:
            if not r["open"]:
                continue
            dt = world.tick - r["t"]
            if r["loc"] in added:
                r["crop_52"] += added[r["loc"]]
                if r["first_crop"] is None:
                    r["first_crop"] = dt
            p = world.people.get(r["pid"])
            if p is not None and p.alive and 4 <= dt <= WPY and tuple(p.loc) == r["loc"]:
                r["returned"] = True
            if dt >= WPY:
                r["b52"] = p.beliefs.get(f"seeds@{r['season']}") if p is not None and p.alive else None
                r["open"] = False
        if events:
            for e in events:
                if e["k"] == "put" and e.get("thing") == "seeds" and e.get("into") == "ground":
                    for r in self.sowings:
                        if r["pid"] == e["a"] and 13 <= world.tick - r["t"] <= 65:
                            r["again"] = True
        # the world's food, mid-season
        if wk % WPS == 6:
            vals = sorted((t.plants + t.crop for t in self.land), reverse=True)
            total = sum(vals)
            k = max(1, len(vals) // 10)
            self.samples.append({"year": year, "season": s, "top10": round(sum(vals[:k]) / total, 4) if total else None,
                                 "total": round(total, 1), "people": len(world.living())})
            if s == 2:
                vec = [t.plants + t.crop for t in self.land]
                if self.autumn_prev is not None:
                    r = corr(self.autumn_prev, vec)
                    if r is not None:
                        self.autumn_r.append(round(r, 4))
                self.autumn_prev = vec

    def results(self):
        closed = [r for r in self.sowings if not r["open"]]
        for r in closed:
            for key in ("open",):
                r.pop(key, None)
        return {"pops": self.pops, "samples": self.samples, "autumn_r": self.autumn_r,
                "sown_by_season": dict(self.sown_by_season), "sowers": len(self.sowers),
                "crop_grown": round(self.crop_grown, 1), "crop_rotted": round(self.crop_rotted, 1),
                "harvest": dict(self.harvest), "sowings": closed}


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
