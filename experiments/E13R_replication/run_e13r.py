"""E13R runner (E13R_preregistration.md). Arms: a (A2-full, E9 code), zero (E13R code, B2 off), s (sham: B2 mode 1,
writes nothing), b (B2 mode 1), n (mode 3: models under 80), p (mode 4: models 80+). Anticipation 1.0, seeds 501-516,
120 years.

The hard stop is enforced by order: V1 (probe read-only), then L2 (instrumented check), then arms a, zero and s and the
L1 check; arms b, n and p are run only if L1 and L2 both pass. If either fails, STOPPED.txt is written and nothing else
runs.

  python experiments/E13R_replication/run_e13r.py all
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
E9 = HERE.parent / "E9_anticipation"
CODE = HERE / "code_e13r"
ARMS = {"a": (E9 / "code_a2", {}), "zero": (CODE, {}), "s": (CODE, {"b2_mode": 1, "b2_write": False}),
        "b": (CODE, {"b2_mode": 1}), "n": (CODE, {"b2_mode": 3}), "p": (CODE, {"b2_mode": 4})}
MODE = {"a": 0, "zero": 0, "s": 1, "b": 1, "n": 3, "p": 4}
SEEDS = tuple(range(501, 517))
WPY, WPS = 52, 13
AUTUMN = 2
PLANNER_FOOD = 80.0
L2_YEARS, L2_MIN = 20, 1000
OUT = HERE / "output"


def setup(arm):
    sys.path.insert(0, str(ARMS[arm][0]))
    sys.path.insert(1, str(E7))
    import acl
    assert Path(acl.__file__).resolve().parent == (ARMS[arm][0] / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **ARMS[arm][1]))


def world_hash(w):
    """The world's state without its configuration (the sham's configuration differs from the control's by design)."""
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def model_of(world, p, mode):
    """The model B2 would choose for p in this arm (the same rule as the code), or None."""
    c = world.cfg
    cands = [q for q in world.people_near(p.loc, c.perception, exclude=p.id)
             if q.age(world.tick) >= 16 * WPY and q.edible() > p.edible()]
    if mode == 3:
        cands = [q for q in cands if q.edible() < PLANNER_FOOD]
    elif mode == 4:
        cands = [q for q in cands if q.edible() >= PLANNER_FOOD]
    return min(cands, key=lambda q: (-q.edible(), q.id)) if cands else None


class Probe:
    def __init__(self, mode):
        from acl.person import A, N_ACTIONS
        self.A, self.N = A, N_ACTIONS
        self.mode = mode or 1                  # arms without B2 count what mode 1 would have taught, for comparison
        self.pops = []
        self.deaths = Counter()
        self.updates = Counter()               # per observer
        self.update_kinds = Counter()          # (model food level 0-3, season, model holds 80+)
        self.autumn_from_planner = defaultdict(lambda: [0, 0])   # (year, pid) -> [from 80+ models, from others]
        self.dose = []                         # (updates so far, habit value) per adult at each 10-year sample
        self.max_ed = defaultdict(float)
        self.near = defaultdict(lambda: defaultdict(int))
        self.forage = defaultdict(lambda: [0, 0])
        self.planned = defaultdict(set)
        self.rows = []
        self.planner_neighbours = []
        self.habit = []
        self.child_cohort = {}
        self.child_rows = []

    def habit_value(self, p):
        vals = [p.q[(f * 8 + comp + AUTUMN) * self.N + self.A["forage"]] for f in (2, 3) for comp in (0, 4)]
        return sum(vals) / len(vals)

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        c = world.cfg
        for e in events:
            if e["k"] == "death":
                if e.get("cause") == "starvation" and e.get("a") in self.child_cohort:
                    self.child_cohort[e["a"]]["starved"] = True
                self.deaths[e.get("cause")] += 1
        foragers = {e["a"] for e in events if e["k"] == "forage" and e.get("a")}
        living = world.living()
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        if tick % 520 == 519:
            self.pops.append(len(living))
            if adults:
                self.habit.append(round(sum(self.habit_value(p) for p in adults) / len(adults), 4))
                self.dose.extend((self.updates[p.id], round(self.habit_value(p), 4)) for p in adults)
        for p in adults:
            m = model_of(world, p, self.mode)
            if m is not None and m.id in foragers and m.last_ctx is not None:
                self.updates[p.id] += 1
                big = m.edible() >= PLANNER_FOOD
                self.update_kinds[(m.last_ctx // 8, s, big)] += 1
                if s == 2:
                    self.autumn_from_planner[(year, p.id)][0 if big else 1] += 1
        if wk == 2 * WPS:
            self.max_ed = defaultdict(float)
            self.near = defaultdict(lambda: defaultdict(int))
        if s == 2:
            for p in adults:
                self.max_ed[p.id] = max(self.max_ed[p.id], p.edible())
                for q in world.people_near(p.loc, c.perception, exclude=p.id):
                    if q.age(world.tick) >= 16 * WPY:
                        self.near[p.id][q.id] += 1
                f = self.forage[(year, p.id)]
                f[1] += 1
                f[0] += next((x[0] for x in (p.considered or []) if x[3]), None) == "forage"
        if wk == 3 * WPS:
            for p in adults:
                if self.forage.get((year, p.id), [0, 0])[1] < 10:
                    continue
                planned = self.max_ed.get(p.id, 0) >= PLANNER_FOOD
                if planned:
                    self.planned[p.id].add(year)
                    self.planner_neighbours.append((year, [q for q, n in self.near[p.id].items() if n >= 4]))
                f = self.forage[(year, p.id)]
                fp_ = self.autumn_from_planner.get((year, p.id), [0, 0])
                self.rows.append({"pid": p.id, "year": year, "planned": planned, "forage_share": round(f[0] / f[1], 3),
                                  "from_planner": fp_[0], "from_other": fp_[1]})
            self.child_cohort = {}
            for p in living:
                if p.age(world.tick) < 12 * WPY:
                    cid = p.caregiver or p.mother
                    carer = world.people.get(cid) if cid else None
                    self.child_cohort[p.id] = {"carer_food": round(carer.food + carer.seeds, 1) if carer and carer.alive else None,
                                               "starved": False}
        if wk == WPY - 1:
            self.child_rows.extend(self.child_cohort.values())
            self.child_cohort = {}

    def results(self):
        again = sum(1 for r in self.rows if r["planned"] and (r["year"] + 1) in self.planned[r["pid"]])
        nb = []
        for y, ids in self.planner_neighbours:
            planners_y = {r["pid"] for r in self.rows if r["year"] == y and r["planned"]}
            for q in ids:
                f = self.forage.get((y + 1, q))
                if f and f[1] >= 10 and q not in planners_y:
                    nb.append(f[0] / f[1])
        return {"rows": self.rows, "planned_again": again, "neighbour_forage_next": nb, "habit": self.habit,
                "child_rows": self.child_rows, "deaths": dict(self.deaths),
                "updates_total": sum(self.updates.values()),
                "update_kinds": [[*k, v] for k, v in sorted(self.update_kinds.items())], "dose": self.dose}


def fp(arm):
    sys.path.insert(1, str(E7))
    from run_e7 import code_hash
    return code_hash(ARMS[arm][0] / "acl")


def run(arm, seed):
    setup(arm)
    f0 = fp(arm)
    w = make_world(arm, seed)
    probe = Probe(MODE[arm])
    w.observers.append(probe)
    t0 = time.time()
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fp(arm), "pops": probe.pops,
           "final_tick": w.tick, "world_hash": world_hash(w), **probe.results(), "seconds": round(time.time() - t0)}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, {res['seconds']}s", flush=True)


def verify(arm, seed=501, years=20):
    """V1: the probe does not change the world."""
    setup(arm)
    hs = []
    for with_probe in (False, True):
        w = make_world(arm, seed)
        if with_probe:
            w.observers.append(Probe(MODE[arm]))
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(exist_ok=True)
    with open(OUT / "checks.txt", "a", encoding="utf-8") as f:
        f.write(f"V1 {arm} seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
    print(f"V1 {arm}:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


def l2(seed=501, years=L2_YEARS):
    """L2: around every copying step in Arm B, the only change allowed is the observer's own forage habit entry."""
    setup("b")
    from acl import biology
    from acl.person import A, N_ACTIONS
    original = biology._follow
    stats = Counter()
    bad = []

    def snap(world):
        return json.loads(json.dumps(world.to_dict()))

    def checked(world, p):
        before = snap(world)
        original(world, p)
        after = snap(world)
        stats["calls"] += 1
        if after == before:
            return
        idx = next(i for i, d in enumerate(before["people"]) if d["id"] == p.id)
        qb, qa = before["people"][idx]["q"], after["people"][idx]["q"]
        changed = [i for i in range(len(qb)) if qb[i] != qa[i]]
        after["people"][idx]["q"] = qb
        if len(changed) == 1 and changed[0] % N_ACTIONS == A["forage"] and after == before:
            stats["updates"] += 1
        else:
            bad.append({"tick": world.tick, "pid": p.id, "q_changed": changed, "other_state_changed": after != before})

    biology._follow = checked
    w = make_world("b", seed)
    for _ in range(years * WPY):
        w.step()
    biology._follow = original
    ok = not bad and stats["updates"] >= L2_MIN
    verdict = "PASS" if ok else ("FAIL" if bad else "UNSCORABLE (counts as failed)")
    OUT.mkdir(exist_ok=True)
    with open(OUT / "checks.txt", "a", encoding="utf-8") as f:
        f.write(f"L2 arm b seed {seed}, {years} years: {stats['calls']} copying steps, {stats['updates']} habit updates "
                f"(minimum {L2_MIN}), {len(bad)} with any other change: {verdict}\n")
        for x in bad[:20]:
            f.write(f"  {x}\n")
    print(f"L2: {stats['calls']} steps, {stats['updates']} updates, {len(bad)} bad: {verdict}", flush=True)
    return ok


def l1_and_v2():
    """L1: sham world state equals the control's at the end, every seed. V2: B2-off code reproduces the control's
    population at every 10-year sample, every seed. V3: code unchanged during each run."""
    lines, ok = [], True
    for s in SEEDS:
        a, z, sh = (json.loads((OUT / f"{arm}_seed_{s}.json").read_text(encoding="utf-8")) for arm in ("a", "zero", "s"))
        l1 = sh["world_hash"] == a["world_hash"] and sh["final_tick"] == a["final_tick"]
        v2 = z["pops"] == a["pops"]
        v3 = all(r["code_hash"] == r["code_hash_after"] for r in (a, z, sh))
        ok &= l1 and v2 and v3
        lines.append(f"seed {s}: L1 sham = control {'yes' if l1 else 'NO'}; V2 zero = control {'yes' if v2 else 'NO'}; "
                     f"V3 code unchanged {'yes' if v3 else 'NO'}")
    with open(OUT / "checks.txt", "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + f"\nL1/V2/V3: {'PASS' if ok else 'FAIL'}\n")
    print("\n".join(lines), f"\nL1/V2/V3: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def stop(reason):
    (OUT / "STOPPED.txt").write_text(f"E13R terminated before any outcome arm was run: {reason}\n", encoding="utf-8")
    sys.exit(f"STOP: {reason}")


def pool_run(me, jobs):
    jobs = [j for j in jobs if not (OUT / f"{j[0]}_seed_{j[1]}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        codes = list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
    return all(c == 0 for c in codes)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        sys.exit(0 if verify(sys.argv[2]) else 1)
    elif cmd == "l2":
        sys.exit(0 if l2() else 1)
    elif cmd == "all":
        OUT.mkdir(exist_ok=True)
        me = [sys.executable, str(Path(__file__).resolve())]
        for arm in ("a", "b"):
            if subprocess.call(me + ["verify", arm]) != 0:
                stop("V1, the probe changes the world")
        if subprocess.call(me + ["l2"]) != 0:
            stop("L2, the instrumented check did not pass")
        if not pool_run(me, [(a, s) for a in ("a", "zero", "s") for s in SEEDS]):
            stop("a control, zero or sham run crashed")
        if not l1_and_v2():
            stop("L1, V2 or V3 did not pass")
        if not pool_run(me, [(a, s) for a in ("b", "n", "p") for s in SEEDS]):
            print("an outcome run crashed; see the log", flush=True)
        print("ALL DONE", flush=True)
    else:
        run(cmd, int(sys.argv[2]))
