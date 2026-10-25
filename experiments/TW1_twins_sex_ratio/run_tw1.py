"""TW1 — twins and the sex ratio at birth (questions.md, frozen as `TW1-frozen`). `code_tw1` = `code_v6` + `twins`,
`sex_ratio_birth` (each default 0) + the nursing fix ("while any child of her latest delivery lives") + read-only
delivery logging (`world.tw1log`). The full difference is `v6_to_tw1.diff`.

  python experiments/TW1_twins_sex_ratio/run_tw1.py zero    # hard stops (writes output/zero.txt)
  python experiments/TW1_twins_sex_ratio/run_tw1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"tw1": HERE / "code_tw1", "v6": EXP / "NV6_nature_v6" / "code_v6"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(16101, 16357))       # 256 new seeds, used by no study
SMOKE_SEEDS = (9965, 9964)
V6 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1}
ARMS = {"c": {}, "t": {"twins": 1, "sex_ratio_birth": 1}}


def setup(code="tw1"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V6, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["tw1"] / "acl")


def observers(w):
    from run_f1 import Probe
    w.tw1log = []
    return [Probe()]


def summarise(w):
    """Deliveries and, for children with full follow-up, survival to 1, 5 and 15 by delivery kind."""
    log = w.tw1log
    end = w.tick
    surv = {k: {a: [0, 0] for a in (1, 5, 15)} for k in ("single", "identical", "fraternal")}
    for r in log:
        kind, ids = r[5], [r[7]] + ([r[8]] if r[8] else [])
        for pid in ids:
            p = w.people[pid]
            for a in (1, 5, 15):
                if p.birth + a * WPY <= end:
                    surv[kind][a][1] += 1
                    lived = p.alive or (p.death_tick - p.birth >= a * WPY)
                    surv[kind][a][0] += int(lived)
    mothers = {}
    for r in log:
        if r[5] != "single":
            m = w.people[r[1]]
            mothers[r[1]] = {"tick": r[0], "died_within_year": (not m.alive) and m.death_tick - r[0] <= WPY}
    reached = {a: {"M": 0, "F": 0} for a in (16, 30, 50)}         # born in the world, seen alive at age a
    for p in w.people.values():
        if p.birth < 0:
            continue
        last = end if p.alive else p.death_tick
        for a in reached:
            if p.birth + a * WPY <= last:
                reached[a][p.sex] += 1
    pairs16 = sum(1 for r in log if r[5] == "identical" and r[8]
                  and all((w.people[x].alive and end - w.people[x].birth >= 16 * WPY)
                          or (not w.people[x].alive and w.people[x].death_tick - w.people[x].birth >= 16 * WPY)
                          for x in (r[7], r[8])))
    return {"deliveries": [[r[0], r[2], r[3], r[4], r[5], r[6]] for r in log], "survival": surv,
            "twin_mothers": list(mothers.values()), "reached_by_sex": reached, "identical_pairs_both_16": pairs16}


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += observers(w)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + ":" + rng_state(w)


def reload_check(seed):
    setup("tw1")
    from acl.world import World
    a = make_world(seed, ARMS["t"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b)


class Forced(random.Random):
    """A random source that returns given values for its next plain random() calls (tests only)."""

    def __init__(self, base):
        super().__init__()
        self.setstate(base.getstate())
        self.queue = []
        self.armed = False

    def random(self):
        if self.armed and self.queue:
            return self.queue.pop(0)
        return super().random()


def unit_tests():
    """Whole-birth tests on a real world (no run is saved): identical, fraternal, single, mother dying, nursing."""
    setup("tw1")
    from acl import biology
    from acl.config import CHILD_END
    lines, ok = [], True

    def delivery(kind_u, death_u=None):
        w = make_world(11, ARMS["t"])
        for _ in range(3):
            w.step()
        mums = [p for p in w.living() if p.sex == "F" and p.age(w.tick) >= CHILD_END]
        dads = [p for p in w.living() if p.sex == "M" and p.age(w.tick) >= CHILD_END]
        mum, dad = mums[0], dads[0]
        mum.pregnant = dad.id
        rng = Forced(w.rng)
        w.rng = rng
        real_born = biology._born
        calls = []

        def born(*a, **k):
            child = real_born(*a, **k)
            calls.append(child)
            if len(calls) == 1:                    # the twin draw comes right after the first child
                rng.queue = [kind_u]
                rng.armed = True
            elif rng.queue == [] and death_u is None:
                rng.armed = False
            return child
        biology._born = born
        try:
            if death_u is not None:
                rng.queue = [kind_u]
            biology.give_birth(w, mum)
            if death_u is not None:
                pass
        finally:
            biology._born = real_born
        return w, mum, dad, calls

    w, mum, dad, kids = delivery(0.001)
    a, b = kids if len(kids) == 2 else (kids[0], None)
    t = (b is not None and a.genes == b.genes and a.sex == b.sex and a.id != b.id
         and a.id in mum.children and b.id in mum.children and a.id in dad.children and b.id in dad.children
         and w.kinship(a, b) == 0.8 and a.id in w.people and b.id in w.people)
    lines.append(f"identical twins: two people, same temperament and sex, siblings (0.8), both parents' children: "
                 f"{'yes' if t else 'NO'}")
    ok &= t
    t2 = biology._youngest_alive(w, mum)
    b.alive = False
    t3 = biology._youngest_alive(w, mum)
    a.alive = False
    t4 = not biology._youngest_alive(w, mum)
    a.alive = b.alive = True
    b.alive = True
    t = t2 and t3 and t4
    lines.append(f"nursing: blocked while either twin lives (second-born dead: still blocked), free when both die: "
                 f"{'yes' if t else 'NO'}")
    ok &= t
    w, mum, dad, kids = delivery(0.010)
    t = len(kids) == 2 and kids[0].genes != kids[1].genes and kids[0].id != kids[1].id
    lines.append(f"fraternal twins: two people, separate temperament draws: {'yes' if t else 'NO'}")
    ok &= t
    w, mum, dad, kids = delivery(0.5)
    t = len(kids) == 1
    lines.append(f"no twins (draw 0.5): one child: {'yes' if t else 'NO'}")
    ok &= t
    # the mother dies in delivery: both births are recorded first
    w = make_world(11, ARMS["t"])
    for _ in range(3):
        w.step()
    mum = [p for p in w.living() if p.sex == "F" and p.age(w.tick) >= CHILD_END][0]
    dad = [p for p in w.living() if p.sex == "M" and p.age(w.tick) >= CHILD_END][0]
    mum.pregnant = dad.id
    rng = Forced(w.rng)
    w.rng = rng
    real_born = biology._born
    seen = []

    def born2(*a, **k):
        child = real_born(*a, **k)
        seen.append(child)
        if len(seen) == 1:
            rng.queue = [0.001]
            rng.armed = True
        elif len(seen) == 2:
            rng.queue = [0.0]                        # the childbirth draw: below 0.01, she dies
            rng.armed = True
        return child
    biology._born = born2
    try:
        biology.give_birth(w, mum)
    finally:
        biology._born = real_born
    t = len(seen) == 2 and not mum.alive and all(c.id in w.people for c in seen) and mum.death_cause == "childbirth"
    lines.append(f"mother dies in delivery: both twins born and recorded first, one death draw: {'yes' if t else 'NO'}")
    ok &= t
    return ok, lines


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("tw1", seed, years, json.dumps(ARMS["c"]), 0) == call("v6", seed, years, json.dumps(ARMS["c"]), 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: settings off (with the nursing fix) = code_v6, state and random "
                     f"numbers: {'yes' if t else 'NO'}")
    t = any(call("tw1", s, 20, json.dumps(ARMS["t"]), 0) != call("tw1", s, 20, json.dumps(ARMS["c"]), 0)
            for s in (501, 601))
    ok &= t
    lines.append(f"arm t, seeds 501/601, 20 years: the settings change the world (they act): {'yes' if t else 'NO'}")
    for arm in ARMS:
        t = call("tw1", 501, 20, json.dumps(ARMS[arm]), 1) == call("tw1", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers and logging: "
                     f"{'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm t, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["units"], capture_output=True, text=True)
    t = r.returncode == 0 and "All units: PASS" in r.stdout
    ok &= t
    lines += [ln for ln in r.stdout.splitlines() if ln.strip() and not ln.startswith("All units")] or [r.stderr[-1500:]]
    lines.append(f"unit tests: {'yes' if t else 'NO'}")
    setup("tw1")
    lines.append(f"code_tw1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("tw1")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = observers(w)
    probe = obs[0]
    w.observers += obs
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v6", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "pops": probe.pops,
           "deaths": probe.results().get("deaths"), **summarise(w)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "units":
        ok, lines = unit_tests()
        print("\n".join(lines))
        print(f"All units: {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
