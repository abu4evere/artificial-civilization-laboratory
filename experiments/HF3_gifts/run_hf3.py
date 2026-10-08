"""HF3 — why gifts fell under HB1 (questions.md, frozen as `HF3-questions`). Read-only replays, first 40 years, arms H
(HB1, home_base = 1) and C (the same code, settings off).

  python experiments/HF3_gifts/run_hf3.py verify | discovery | holdout

Approximations (written before data): "at the time of deciding" is the end-of-last-week snapshot (positions and food in
hand before anyone acted this week); the code considers only the twelve nearest people within reach, while the observer
counts everyone within reach.
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "HB1_home_base"))
import run_hb1 as HB  # noqa: E402

OUT = HERE / "output"
WPY, YEARS = 52, 40
DISCOVERY = tuple(range(501, 517))
HOLDOUT = tuple(range(1501, 1517))
ARMS = {"h": {"home_base": 1}, "c": {}}
SAVED = {"h": EXP / "HB1_home_base" / "output", "c": EXP / "F1_baseline_fragility" / "output"}


class Probe:
    """Reads the world after each week; draws no random numbers; writes nothing to the world."""

    def __init__(self):
        self.pops = []
        self.n = Counter()
        self.snap = None                    # id -> (loc, edible, need, dep_need, young_dep_ids, adult)
        self.last_gift = {}                 # id -> week of the last gift received

    def take_snapshot(self, world):
        c, tick = world.cfg, world.tick
        snap = {}
        for p in world.living():
            deps = world.dependents(p.id)
            young = {d.id for d in deps if d.stage(tick) in ("infant", "child")}
            snap[p.id] = (p.loc, p.edible(), p.need(c, tick), sum(d.need(c, tick) for d in deps), young,
                          p.age(tick) >= 16 * WPY)
        return snap

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick
        t = tick - 1
        living = world.living()
        if t % 520 == 519:
            self.pops.append(len(living))
        n = self.n
        S = self.snap
        dist = lambda a, b: distance(a, b, c.width, c.height)
        gives = [e for e in events if e["k"] == "give" and "a" in e and "b" in e]
        given_by = Counter(e["a"] for e in gives)
        for e in gives:
            self.last_gift[e["b"]] = t
            g, r = world.people[e["a"]], world.people[e["b"]]
            if g.age(tick) < 16 * WPY:
                continue
            amt = e.get("amount", 0.0)
            rel = "partner" if g.partner == r.id else "kin" if world.kinship(g, r) > 0 else "other"
            n[f"gift_{rel}"] += amt
            hg = world.couple_home(g, world.people[g.partner]) if g.partner and world.people[g.partner].alive else None
            hr = world.couple_home(r, world.people[r.partner]) if r.partner and world.people[r.partner].alive else None
            if hg is not None and hr is not None:
                same = hg == hr
                n[f"gift_samehome_{same}"] += amt
                if not same:
                    n["gift_homes_dist_sum"] += dist(hg, hr)
                    n["gift_homes_dist_n"] += 1
        if S is not None:
            for pid, (loc, edible, need, dep_need, young, adult) in S.items():
                if not adult:
                    continue
                p = world.people[pid]
                n["adult_weeks"] += 1
                surplus = edible - need * 2.0 - dep_need > 1.0
                short_near = any(qid != pid and qid not in young and qe < qn and dist(loc, ql) <= c.reach
                                 for qid, (ql, qe, qn, _, _, _) in S.items())
                n["g1_short_near"] += short_near
                n["g2_surplus"] += surplus
                if surplus and short_near:
                    n["opportunity"] += 1
                    n["gifts_in_opportunity"] += given_by.get(pid, 0)
                n["gifts_given"] += given_by.get(pid, 0)
                if p.alive:
                    starving = bool(p.starving)
                    recent = pid in self.last_gift and t - self.last_gift[pid] <= 8
                    n[f"aw_recent_{recent}"] += 1
                    n[f"starving_recent_{recent}"] += starving
                    if starving:
                        n["starving"] += 1
                        giver = any(qid != pid and qa and dist(loc, ql) <= c.reach and qe - qn * 2.0 - qd > 1.0
                                    for qid, (ql, qe, qn, qd, _, qa) in S.items())
                        n["starving_giver_near"] += giver
        for e in gives:
            g = world.people[e["a"]]
            if g.age(tick) >= 16 * WPY:
                n["gift_food_given"] += e.get("amount", 0.0)
        for e in gives:
            r = world.people[e["b"]]
            if r.age(tick) >= 16 * WPY:
                n["gift_food_received_by_adults"] += e.get("amount", 0.0)
        self.snap = self.take_snapshot(world)

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
        res["reproduces"] = json.loads(saved.read_text(encoding="utf-8"))["pops"][: years // 10] == probe.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: pops {probe.pops}, reproduces saved: {res.get('reproduces')}", flush=True)


def verify(seeds=(501, 1501), years=20):
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
