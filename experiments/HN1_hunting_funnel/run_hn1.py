"""HN1 — where do v11's hunts fail? (questions.md, frozen as `HN1-frozen`). Read-only on live nature v11 (`code_v11`).
ES2's runner supplies the set-up (`../ES2_realized_lookahead/run_es2.py`). HN1's observer records, for adults aged 16-49
in years 100-200:
  hunts     every hunter-week at resolution: prey on the tile or not, success, armed or bare-handed, the meat share,
            the meat kept, party size, species taken, the tile's plant-stock band, person, year, season
  forage    every forage-week: food gained (food + seeds), the tile's plant-stock band, person, year, season (pooled
            sums, and per person-year-season-band sums kept only where a hunter-week needs a match)
  species   attempts on tiles with a single prey species, and successes, by species (F7)

  python experiments/HN1_hunting_funnel/run_hn1.py zero
  python experiments/HN1_hunting_funnel/run_hn1.py one c <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

CODE = "v11"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(22601, 22633))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9903, 9902)
ARMS = {"c": {**base.LP}}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
ADULT, OLD = 16 * WPY, 50 * WPY
LATE = [100 * WPY, 200 * WPY]


def band(tile) -> int:
    v = tile.plants + tile.crop
    return 0 if v < 10 else (1 if v <= 40 else 2)


class HN1Obs:
    def __init__(self, w):
        self.w = w
        self.s = Counter()
        self.hunts = []            # [pid, year, season, band, no_prey, success, armed, share, kept, n, species]
        self.fsum = defaultdict(lambda: [0.0, 0])     # (pid, year, season, band) -> [food, weeks]
        self.sp_try = Counter()
        self.sp_hit = Counter()

    def counted(self, p, tick):
        return LATE[0] <= tick < LATE[1] and ADULT <= p.age(tick) < OLD

    def hunts_resolved(self, world, before, events):
        """before: {loc: [(person, food+seeds before, armed, prey_here, species present)]}; events: this call's."""
        tick = world.tick
        ev = {}
        for e in events:
            if e["k"] == "hunt":
                ev[e["a"]] = e
        for loc, rows in before.items():
            if not rows:
                continue
            first = rows[0][0].id
            e = ev.get(first)
            if e is None:
                continue
            n = len(rows)
            success = bool(e.get("success"))
            meat = float(e.get("meat", 0.0))
            sp = e.get("animal", "") or ""
            species = rows[0][4]
            if rows[0][3] >= 1 and len(species) == 1:
                self.sp_try[species[0]] += 1
                self.sp_hit[species[0]] += success and sp == species[0]
            for p, f0, armed, prey, _ in rows:
                if not self.counted(p, tick):
                    continue
                kept = max(0.0, (p.food + p.seeds) - f0)
                share = meat / n
                tile = world.tile(loc)
                self.hunts.append([p.id, tick // WPY, world.season, band(tile), int(prey < 1), int(success), int(armed),
                                   round(share, 3), round(kept, 3), n, sp])
                k = "armed" if armed else "bare"
                self.s["hunter_weeks"] += 1
                self.s[f"hunter_weeks_{k}"] += 1
                if prey < 1:
                    self.s["no_prey"] += 1
                    self.s[f"no_prey_{k}"] += 1
                elif not success:
                    self.s["roll_failed"] += 1
                    self.s[f"roll_failed_{k}"] += 1
                else:
                    self.s["success"] += 1
                    self.s[f"success_{k}"] += 1
                    self.s["share_sum"] += share
                    self.s["kept_sum_success"] += kept
                    self.s["expected_sum"] += (world.cfg.hunt_prey_base + world.cfg.hunt_prey_per_hunter * min(n, 5)) / n
                self.s["kept_sum"] += kept
                self.s[f"kept_sum_{k}"] += kept

    def foraged(self, world, p, got, b):
        tick = world.tick
        if not self.counted(p, tick):
            return
        self.s["forage_weeks"] += 1
        self.s["forage_sum"] += got
        f = self.fsum[(p.id, tick // WPY, world.season, b)]
        f[0] += got
        f[1] += 1

    def __call__(self, world, events):
        tick = world.tick - 1
        if LATE[0] <= tick < LATE[1]:
            living = world.living()
            self.s["living_weeks"] += len(living)
            self.s["adult_weeks"] += sum(1 for p in living if ADULT <= p.age(world.tick) < OLD)

    def results(self):
        need = {(h[0], h[1], h[2], h[3]) for h in self.hunts}
        matched = [[k[0], k[1], k[2], k[3], round(v[0], 3), v[1]] for k, v in self.fsum.items() if k in need]
        return {"sums": dict(self.s), "hunt_fields": ["person", "year", "season", "band", "no_prey", "success",
                                                       "armed", "share", "kept", "party", "species"],
                "hunts": self.hunts, "forage_match_fields": ["person", "year", "season", "band", "food", "weeks"],
                "forage_match": matched, "species_try": dict(self.sp_try), "species_hit": dict(self.sp_hit)}


def install(w, obs):
    from acl import actions, fauna
    from acl.matter import best_item
    o_resolve, o_forage = actions.resolve_hunts, actions.HANDLERS["forage"]

    def resolve_hunts(world):
        if world is not w:
            return o_resolve(world)
        before = {}
        for loc, ids in world.hunts.items():
            rows = []
            prey = fauna.prey_here(world, loc)
            present = sorted({g["sp"] for g in fauna.near(world, loc, 0) if g["sp"] in fauna.PREY and g["n"] > 0})
            fish = fauna.fish_by(world, loc)
            if fish is not None and fish["n"] > 0 and "fish" not in present:
                present.append("fish")
            for i in ids:
                h = world.people[i]
                if h.alive:
                    rows.append((h, h.food + h.seeds, best_item(h, "hunt")[1] > 1.0, prey, tuple(present)))
            before[loc] = rows
        n0 = len(world.events)
        out = o_resolve(world)
        obs.hunts_resolved(world, before, world.events[n0:])
        return out

    def forage(world, p, target, eff):
        if world is not w:
            return o_forage(world, p, target, eff)
        b = band(world.tile(p.loc))
        f0 = p.food + p.seeds
        out = o_forage(world, p, target, eff)
        obs.foraged(world, p, (p.food + p.seeds) - f0, b)
        return out
    actions.resolve_hunts = resolve_hunts
    actions.HANDLERS["forage"] = forage


def hashrun(seed, years, observe):
    LATE[0], LATE[1] = 0, years * WPY       # zero checks: every year counted
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        obs = HN1Obs(w)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({k: obs.s[k] for k in ("hunter_weeks", "no_prey", "roll_failed", "success",
                                                        "forage_weeks")}, sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def adds_up(seed):
    """The funnel adds up: (a) + (b) + (c) = all adult hunter-weeks, counted independently from the hunt events."""
    LATE[0], LATE[1] = 0, 30 * WPY
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = HN1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    independent = 0
    for _ in range(30 * WPY):
        evs = w.step()
        for e in evs:
            if e["k"] == "hunt":
                for pid in e.get("party", []):
                    q = w.people[pid]
                    if ADULT <= q.age(w.tick - 1) < OLD:
                        independent += 1
    s = obs.s
    total = s["no_prey"] + s["roll_failed"] + s["success"]
    return total == s["hunter_weeks"] == independent and total > 0, total, independent


def reload_check(seed):
    base.setup(CODE)
    from acl.world import World
    a = base.make_world(seed, ARMS["c"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(a) == base.world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]

    def hs(x):
        return x.split(":")[:2]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        side = list(ex.map(lambda a: subprocess.run(me + a, capture_output=True, text=True).stdout.split(),
                           [["reload", "501"], ["addsup", "701"]]))
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        ok &= ro
        lines.append(f"seed {seed}, {years} years: observer read-only: {'yes' if ro else 'NO'}; "
                     f"{got[(seed, years, 1)].split(':', 2)[2]}")
    t = side[0][-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    out = side[1]
    t = len(out) >= 3 and out[-3] == "True"
    ok &= t
    lines.append(f"seed 701, 30 years: the funnel adds up (a + b + c = adult hunter-weeks = the count from the hunt "
                 f"events; {out[-2] if out else '?'} and {out[-1] if out else '?'}): {'yes' if t else 'NO'}")
    lines.append(f"code_v11 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = HN1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v11", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, hunter-weeks {obs.s['hunter_weeks']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "addsup":
        ok, a, b = adds_up(int(sys.argv[2]))
        print(ok, a, b)
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: every year counted; never study data
        LATE[0], LATE[1] = 0, int(sys.argv[4]) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
