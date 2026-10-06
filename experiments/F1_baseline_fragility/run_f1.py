"""F1 — baseline fragility (questions.md, frozen as `F1-questions`). Read-only replays of control worlds with an observer.

  python experiments/F1_baseline_fragility/run_f1.py verify      # observer read-only (two seeds, 20 years)
  python experiments/F1_baseline_fragility/run_f1.py discovery   # the 40 saved control worlds, checked against saved pops
  python experiments/F1_baseline_fragility/run_f1.py holdout     # 24 new seeds, 1101-1124 (only after discovery is written up)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "E13R_replication" / "code_e13r"
OUT = HERE / "output"
WPY, YEARS = 52, 120
SAVED = {**{s: EXP / "E13R_replication" / "output" / f"zero_seed_{s}.json" for s in range(501, 517)},
         **{s: EXP / "L1_no_winter_growth" / "output" / f"c_seed_{s}.json" for s in range(601, 617)},
         **{s: EXP / "N4_uncertain_winters" / "output" / "pilot" / f"c_seed_{s}.json" for s in range(811, 819)}}
DISCOVERY = tuple(SAVED)
HOLDOUT = tuple(range(1101, 1125))
SNAP_WEEK = 26                      # mid-year: groups, mate supply, ages, genes
AUTUMN_WEEK = 2 * 13 + 6            # mid-autumn: food on the land (as V1, U)
BAD = ("starvation", "thirst", "cold")


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


class Probe:
    """Reads the world after each week; draws no random numbers and writes nothing to the world."""

    def __init__(self):
        self.pops = []
        self.years = defaultdict(lambda: defaultdict(float))
        self.births = []                 # [year, mother's age]
        self.deaths = []                 # [year, cause, age, stage]
        self.land = None

    def __call__(self, world, events):
        from acl.biology import _youngest_alive
        from acl.config import CHILD_END
        from acl.util import distance
        c = world.cfg
        tick = world.tick - 1
        yr, wk = tick // WPY, tick % WPY
        Y = self.years[yr]
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        for e in events:
            k = e["k"]
            if k == "birth":
                m = world.people[e["a"]]
                self.births.append([yr, round(m.years(world.tick), 1)])
                Y["births"] += 1
            elif k == "death":
                p = world.people[e["a"]]
                self.deaths.append([yr, e.get("cause", "?"), e.get("age"), p.stage(p.death_tick)])
                Y["deaths"] += 1
                Y["d_" + e.get("cause", "?")] += 1
            elif k == "pair":
                Y["pairs"] += 1
        # every week
        Y["person_weeks"] += len(living)
        for p in living:
            Y["health"] += p.health
            if p.starving:
                Y["starving_weeks"] += 1
            if p.age(world.tick) < 6 * WPY and p.caregiver is None:
                Y["no_carer_weeks"] += 1
            if p.sex == "F" and c.fertile_from <= p.years(world.tick) < c.fertile_until:
                Y["woman_weeks"] += 1
                Y["r_" + self.block(world, p, _youngest_alive, distance, CHILD_END)] += 1
        if wk == AUTUMN_WEEK:
            if self.land is None:
                self.land = [t for row in world.tiles for t in row if not t.water]
            food = sum(t.plants + t.crop for t in self.land)
            Y["autumn_tile"] = food / len(self.land)
            Y["autumn_pp"] = food / len(living) if living else 0.0
        if wk == SNAP_WEEK:
            self.snapshot(world, Y, living, distance)

    @staticmethod
    def block(world, p, youngest_alive, distance, child_end):
        """The code's conditions for conception (biology.body_phase), in its order, without its random draw."""
        c, tick = world.cfg, world.tick
        if p.pregnant is not None:
            return "pregnant"
        if p.partner is None:
            return "no_partner"
        mate = world.people[p.partner]
        if not mate.alive:
            return "partner_dead"
        if distance(p.loc, mate.loc, c.width, c.height) > c.camp_radius:
            return "apart"
        if p.health < 50:
            return "low_health"
        if p.starving:
            return "starving"
        if mate.age(tick) < child_end:
            return "partner_child"
        if tick - p.last_birth < c.nursing_weeks and youngest_alive(world, p):
            return "nursing"
        return "eligible"

    @staticmethod
    def snapshot(world, Y, living, distance):
        c, tick = world.cfg, world.tick
        st = Counter((p.stage(tick), p.sex) for p in living)
        for (s, sx), n in st.items():
            Y[f"n_{s}_{sx}"] = n
        Y["n"] = len(living)
        Y["mean_age"] = sum(p.years(tick) for p in living) / len(living) if living else 0.0
        women = [p for p in living if p.sex == "F" and c.fertile_from <= p.years(tick) < c.fertile_until]
        Y["women"] = len(women)
        single_w = [p for p in women if p.partner is None]
        Y["women_single"] = len(single_w)
        men = [q for q in living if q.sex == "M" and q.stage(tick) == "adult" and q.partner is None]
        no_mate = no_mate_near = 0
        for wmn in single_w:
            ok = [q for q in men if world.kinship(wmn, q) == 0 and abs(wmn.birth - q.birth) <= 15 * WPY]
            no_mate += not ok
            no_mate_near += not any(distance(wmn.loc, q.loc, c.width, c.height) <= c.perception for q in ok)
        Y["women_single_no_mate"] = no_mate
        Y["women_single_no_mate_near"] = no_mate_near
        Y["adult_men"] = sum(1 for q in living if q.sex == "M" and q.stage(tick) == "adult")
        Y["adult_women"] = sum(1 for q in living if q.sex == "F" and q.stage(tick) == "adult")
        # groups: people within camp radius, chained
        parent = list(range(len(living)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for i in range(len(living)):
            for j in range(i + 1, len(living)):
                if distance(living[i].loc, living[j].loc, c.width, c.height) <= c.camp_radius:
                    parent[find(i)] = find(j)
        Y["groups"] = len({find(i) for i in range(len(living))})
        adults = [p for p in living if p.age(tick) >= 16 * WPY]
        nn = [min((distance(a.loc, b.loc, c.width, c.height) for b in adults if b is not a), default=None) for a in adults]
        nn = [x for x in nn if x is not None]
        Y["nearest_adult"] = sum(nn) / len(nn) if nn else None
        if living:
            for g in living[0].genes:
                Y["gene_" + g] = sum(p.genes[g] for p in living) / len(living)

    def results(self):
        return {"pops": self.pops, "births": self.births, "deaths": self.deaths,
                "years": {str(y): dict(v) for y, v in sorted(self.years.items())}}


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def run_one(seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **probe.results()}
    if seed in SAVED:
        saved = json.loads(SAVED[seed].read_text(encoding="utf-8"))["pops"]
        res["saved_pops"] = saved
        res["reproduces"] = saved == probe.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: alive {len(w.living())}, pops {probe.pops}"
          + (f", reproduces saved: {res['reproduces']}" if seed in SAVED else ""), flush=True)


def verify(seeds=(601, 811), years=20):
    setup()
    lines, ok = [], True
    for seed in seeds:
        hs = []
        for with_probe in (False, True):
            w = make_world(seed)
            if with_probe:
                w.observers.append(Probe())
            for _ in range(years * WPY):
                w.step()
            hs.append(w.state_hash())
        t = hs[0] == hs[1]
        ok &= t
        lines.append(f"observer, seed {seed}, {years} years: {'READ-ONLY' if t else 'CHANGES THE WORLD'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    return ok


def batch(seeds):
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in seeds if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["one", str(s)]), todo))
    R = [json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in seeds]
    bad = [r["seed"] for r in R if r.get("reproduces") is False or r["code_hash"] != r["code_hash_after"]]
    print("ALL REPRODUCE, CODE UNCHANGED" if not bad else f"HARD STOP: {bad}", flush=True)
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        run_one(int(sys.argv[2]))
    elif cmd == "verify":
        sys.exit(0 if verify() else 1)
    elif cmd == "discovery":
        sys.exit(0 if batch(DISCOVERY) else 1)
    elif cmd == "holdout":
        sys.exit(0 if batch(HOLDOUT) else 1)
