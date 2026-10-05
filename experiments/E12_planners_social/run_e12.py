"""E12 planners' social world (E12_preregistration.md). Read-only replays of E9 A2-full, seeds 301–304, 120 years.

  python experiments/E12_planners_social/run_e12.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E9 = HERE.parent / "E9_anticipation"
sys.path.insert(0, str(E9 / "code_a2"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output"


def standing(world, pid):
    resp = trust = 0.0
    for q in world.living():
        r = q.rel.get(pid)
        if r is not None:
            resp += r.respect
            trust += r.trust
    return resp, trust


class Probe:
    def __init__(self):
        self.pops = []
        self.max_ed = defaultdict(float)
        self.seen = defaultdict(int)          # pid -> adult-sightings in autumn
        self.near = defaultdict(lambda: defaultdict(int))   # pid -> other pid -> autumn weeks within sight
        self.start_standing = {}
        self.short_now, self.short_prev = set(), set()
        self.planned = defaultdict(set)       # pid -> years
        self.forage = defaultdict(lambda: [0, 0])   # (year, pid) -> [forage weeks, weeks] in autumn
        self.cohort = {}
        self.rows = []
        self.children_of = defaultdict(set)   # (year, carer) -> child ids
        self.adult_planners_ever = set()

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        c = world.cfg
        for e in events:
            if e["k"] == "give" and e.get("a") in self.cohort:
                r = self.cohort[e["a"]]
                r["given"] += e.get("amount", 0.0)
                r["recipients"].add(e.get("b"))
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        if wk == 2 * WPS:                                   # first autumn week: note standing of everyone
            self.start_standing = {p.id: standing(world, p.id) for p in adults}
            self.max_ed = defaultdict(float)
            self.seen = defaultdict(int)
            self.near = defaultdict(lambda: defaultdict(int))
        if s == 2:
            for p in adults:
                self.max_ed[p.id] = max(self.max_ed[p.id], p.edible())
                others = [q.id for q in world.people_near(p.loc, c.perception, exclude=p.id)
                          if q.age(world.tick) >= 16 * WPY]
                self.seen[p.id] += len(others)
                for q in others:
                    self.near[p.id][q] += 1
                f = self.forage[(year, p.id)]
                f[1] += 1
                f[0] += next((x[0] for x in (p.considered or []) if x[3]), None) == "forage"
        if s == 3:
            for p in adults:
                if p.starving:
                    self.short_now.add(p.id)
        if wk == 3 * WPS:                                   # first winter week: form the cohort
            self.cohort = {}
            for p in adults:
                planner = self.max_ed.get(p.id, 0) >= 80
                if planner:
                    self.planned[p.id].add(year)
                    self.adult_planners_ever.add(p.id)
                if planner or p.id in self.short_prev:
                    nb = [q for q, wks in self.near[p.id].items() if wks >= 4]
                    self.cohort[p.id] = {"pid": p.id, "year": year, "planner": planner,
                                         "seen_per_week": round(self.seen[p.id] / 13, 2),
                                         "standing_start": self.start_standing.get(p.id, (0.0, 0.0)),
                                         "given": 0.0, "recipients": set(), "neighbours": nb,
                                         "children": [d.id for d in world.dependents(p.id)]}
        if wk == WPY - 1:                                   # end of winter
            for pid, r in self.cohort.items():
                r["standing_end"] = standing(world, pid)
                r["recipients"] = len(r["recipients"])
                self.rows.append(r)
            self.cohort = {}
            self.short_prev, self.short_now = self.short_now, set()

    def results(self, world):
        out = []
        for r in self.rows:
            y = r["year"]
            nb = []
            for q in r["neighbours"]:
                f = self.forage.get((y + 1, q))
                nb.append({"forage_next": round(f[0] / f[1], 3) if f and f[1] >= 10 else None,
                           "planned_next": (y + 1) in self.planned.get(q, set())})
            kids = r["children"]
            out.append({**{k: v for k, v in r.items() if k not in ("neighbours", "children")},
                        "neighbours": nb,
                        "children_n": len(kids),
                        "children_planned_as_adults": sum(1 for k in kids if k in self.adult_planners_ever)})
        return out


def run(seed):
    saved = json.loads((E9 / "output" / f"a2full_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed, anticipation_weight=1.0))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    res = {"seed": seed, "replay_matches_e9": probe.pops == saved["pops"], "rows": probe.results(w)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches E9 {res['replay_matches_e9']}, rows {len(res['rows'])}", flush=True)


def verify(seed=304, years=20):
    hs = []
    for with_probe in (False, True):
        w = World(Config(seed=seed, anticipation_weight=1.0))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    print("verify:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(0 if verify() else 1)
    elif sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        if subprocess.call(me + ["verify"]) != 0:
            sys.exit("ABORT")
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), SEEDS))
    else:
        run(int(sys.argv[1]))
