"""PF1 — where partner finding stops (questions.md, frozen as `PF1-frozen`). Read-only.

`code_pf1` = `code_mb1b` + logging in `actions._court` only: each courting attempt between two people who are not
already partners, and its result, appended to `world.pf1log` (not saved, read by nothing in the world). A read-only
weekly observer assigns each fertile single woman-week (aged 16-45, no partner at the end of the week; MB1b's unit)
the first step it fails:

  S1 no match alive   no single, unrelated adult man born within 15 years of her (and not her ward or guardian)
  S2 none in sight    such men exist, but none within perception + 2 tiles
  S3 none in reach    one in sight, none within reach (3 tiles: the only people who are options)
  S4 disliked         one in reach, but her feeling for him or his for her is at or below -0.2 for every one
  S5 not tried        a man she could court and who could court her is in reach, but neither chose `court`
  S6 refused          courting was tried that week (by her or to her) and did not end in a pair

MB1b's own worlds are replayed exactly: each replay's final state hash must equal the saved one.

  python experiments/PF1_partner_pipeline/run_pf1.py zero     # logging + observer change nothing (vs code_mb1b)
  python experiments/PF1_partner_pipeline/run_pf1.py run      # discovery 5301-5316, then holdout 5317-5332; p4, b8, b16
  python experiments/PF1_partner_pipeline/run_pf1.py smoke    # throwaway: seed 9701, 6 years, p4 and b16
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"pf1": HERE / "code_pf1", "mb1b": EXP / "MB1_multi_band" / "code_mb1b"}
SAVED = EXP / "MB1_multi_band" / "output_mb1b"
OUT = HERE / "output"
WPY, YEARS = 52, 120
DISCOVERY = tuple(range(5301, 5317))
HOLDOUT = tuple(range(5317, 5333))
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
ARMS = {"p4": {}, "b8": {"founding_bands": 8}, "b16": {"founding_bands": 16}}
STEPS = ("S1_no_match_alive", "S2_none_in_sight", "S3_none_in_reach", "S4_disliked", "S5_not_tried", "S6_refused")
AGES = ((16, 26), (26, 36), (36, 45))


def setup(code="pf1"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw, founders=80):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, founders=founders, **V2, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["pf1"] / "acl")


class Audit:
    """Read-only: reads the world after each week and the week's courting log; changes nothing in the world."""

    def __init__(self):
        self.steps = Counter()
        self.by_age = Counter()
        self.woman_weeks = 0
        self.single_men_weeks = 0
        self.person_weeks = 0
        self.attempts = Counter()

    def __call__(self, world, events):
        from acl.config import WEEKS_PER_YEAR
        c, tick = world.cfg, world.tick
        log = getattr(world, "pf1log", None) or []
        tried = {}
        for _t, a, b, res in log:
            self.attempts[res] += 1
            for x, y in ((a, b), (b, a)):
                tried.setdefault(x, set()).add(y)
        if getattr(world, "pf1log", None) is not None:
            world.pf1log.clear()
        living = world.living()
        self.person_weeks += len(living)
        men = [q for q in living if q.sex == "M" and q.stage(tick) == "adult" and q.partner is None]
        self.single_men_weeks += len(men)
        for p in living:
            if p.sex != "F" or p.partner is not None:
                continue
            yrs = (tick - p.birth) / WEEKS_PER_YEAR
            if not (c.fertile_from <= yrs < c.fertile_until):
                continue
            self.woman_weeks += 1
            step = self.classify(world, p, men, tried.get(p.id, set()))
            self.steps[step] += 1
            band = next((f"{a}-{b}" for a, b in AGES if a <= yrs < b), "other")
            self.by_age[f"{band}|{step}"] += 1

    @staticmethod
    def classify(world, p, men, tried_with):
        c, tick = world.cfg, world.tick
        match = [q for q in men if world.kinship(p, q) == 0 and abs(p.birth - q.birth) <= 15 * WPY
                 and q.id not in p.wards and p.id not in q.wards]
        if not match:
            return STEPS[0]
        ids = {q.id for q in match}
        sight = {q.id for q in world.people_near(p.loc, c.perception + 2, exclude=p.id)} & ids
        if not sight:
            return STEPS[1]
        reach = [q for q in world.people_near(p.loc, c.reach, exclude=p.id) if q.id in ids]
        if not reach:
            return STEPS[2]

        def aff(a, b):
            r = a.rel.get(b.id)
            return r.affection if r else 0.0
        open_ = [q for q in reach if aff(p, q) > -0.2 and aff(q, p) > -0.2]
        if not open_:
            return STEPS[3]
        if not (tried_with & ids):
            return STEPS[4]
        return STEPS[5]

    def results(self):
        return {"woman_weeks": self.woman_weeks, "steps": dict(self.steps), "by_age": dict(self.by_age),
                "single_men_weeks": self.single_men_weeks, "person_weeks": self.person_weeks,
                "attempts": dict(self.attempts)}


def hashrun(code, seed, years, kw, observe, founders):
    setup(code)
    w = make_world(seed, kw, founders)
    if observe:
        w.pf1log = []
        w.observers.append(Audit())
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for founders in (20, 80):
        for seed in (501, 601):
            for kw in ({}, {"founding_bands": 16}):
                ref = call("mb1b", seed, 20, json.dumps(kw), 0, founders)
                for obs in (0, 1):
                    t = call("pf1", seed, 20, json.dumps(kw), obs, founders) == ref
                    ok &= t
                    lines.append(f"{founders} founders, seed {seed}, 20 years, {kw or 'p4'}, logging+observer "
                                 f"{'on' if obs else 'off'}: = code_mb1b: {'yes' if t else 'NO'}")
    setup("pf1")
    lines.append(f"code_pf1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("pf1")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    w.pf1log = []
    audit = Audit()
    w.observers.append(audit)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "alive_end": len(w.living()), **audit.results()}
    saved = SAVED / f"{arm}_seed_{seed}.json"
    if saved.exists() and years == YEARS:
        res["reproduces"] = json.loads(saved.read_text(encoding="utf-8"))["world_hash"] == res["world_hash"]
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: reproduces {res.get('reproduces')}, woman-weeks {audit.woman_weeks}, "
          f"steps {dict(audit.steps)}", flush=True)


def batch(seeds, years=YEARS, out=OUT, workers=2):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), todo))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1",
                      int(sys.argv[7])))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "run":
        batch(DISCOVERY)
        print("DISCOVERY DONE", flush=True)
        batch(HOLDOUT)
        print("ALL DONE", flush=True)
    elif cmd == "smoke":
        batch((9701,), years=6, out=HERE / "output_smoke")
        print("SMOKE DONE", flush=True)
