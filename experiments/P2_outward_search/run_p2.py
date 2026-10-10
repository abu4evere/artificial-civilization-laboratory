"""P2 — leave when there is no one: outward search by the unpartnered (preregistration.md, frozen as `P2-frozen`).
One copy of the code (`code_p2`: MC1's copy, which carries HF4's ledger, plus the `outward_search` setting and a
logging-only P2 log): c (settings off), p (outward_search = 1), s (sham_draw = 1). Observers: F1's, HF4's ledger, and
P2's Encounters (weekly, read-only).

  python experiments/P2_outward_search/run_p2.py zero    # off + log + observers reproduce the control; p and s differ
  python experiments/P2_outward_search/run_p2.py pilot   # feasibility: c and p on seeds 2513-2516, 20 years
  python experiments/P2_outward_search/run_p2.py run     # c, p, s on seeds 2257-2512 (only after the pilot passes)
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
CODES = {"p2": HERE / "code_p2", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(2257, 2513))
PILOT = tuple(range(2513, 2517))
ARMS = {"c": {}, "p": {"outward_search": 1}, "s": {"sham_draw": 1}}
PILOT_GATE = 0.05


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "HF4_hunger_ledger"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, **kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["p2"] / "acl")


class Encounters:
    """Read-only, weekly. Seekers as the code defines them (adult, no partner, under 45); eligible as in the code's
    join branch (adult, other sex, no partner, not kin, within 15 years of age). Also holds the P2 log for the week."""

    def __init__(self):
        self.buf = []
        self.n = Counter()
        self.partnered = None

    def __call__(self, world, events):
        from acl.util import distance
        c, tick, n = world.cfg, world.tick, self.n
        living = world.living()
        singles = [q for q in living if q.stage(tick) == "adult" and q.partner is None]
        for p in singles:
            if p.years(tick) >= 45:
                continue
            n["seeker_weeks"] += 1
            n[f"seeker_weeks_{p.sex}"] += 1
            if any(q.sex != p.sex and world.kinship(p, q) == 0 and abs(p.birth - q.birth) <= 15 * WPY
                   and distance(p.loc, q.loc, c.width, c.height) <= c.perception for q in singles):
                n["seeker_weeks_eligible_in_sight"] += 1
                n[f"seeker_weeks_eligible_in_sight_{p.sex}"] += 1
        now = {p.id for p in living if p.partner is not None}
        if self.partnered is None:
            n["partnered_after_week1"] = len(now)     # founders' pairs: not counted as new pairings
        else:
            n["new_partnered_people"] += len(now - self.partnered)
        self.partnered = now
        for kind, taken in self.buf:
            n[f"trigger_{kind}"] += 1
            n[f"taken_{kind}"] += taken
        self.buf.clear()

    def results(self):
        return dict(self.n)


def hash_run(code, seed, years, kw, log):
    setup(code)
    w = make_world(seed, **kw)
    if log:
        from run_f1 import Probe as F1Probe
        from run_hf4 import Ledger
        lg, enc = Ledger(), Encounters()
        w.ledger, w.p2log = lg.buf, enc.buf
        w.observers += [lg, F1Probe(), enc]
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(code, seed, kw, log):
        out = subprocess.run(me + ["hashrun", code, str(seed), json.dumps(kw), "1" if log else "0"],
                             capture_output=True, text=True).stdout
        return out.strip().splitlines()[-1]
    lines, ok, base = [], True, {}
    for seed in (2257, 2258):
        base[seed] = call("e13r", seed, {}, False)
        t = base[seed] == call("p2", seed, {}, True)
        ok &= t
        lines.append(f"settings off, log and observers on, seed {seed}, 20 years: copy reproduces the control world: "
                     f"{'yes' if t else 'NO'}")
    for arm in ("p", "s"):
        t = call("p2", 2257, ARMS[arm], True) != base[2257]
        ok &= t
        lines.append(f"arm {arm} on, seed 2257, 20 years: the world differs from the control: {'yes' if t else 'NO'}")
    setup("p2")
    lines.append(f"code_p2 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("p2")
    from run_f1 import Probe as F1Probe
    from run_hf4 import Ledger
    f0 = fingerprint()
    w = make_world(seed, **ARMS[arm])
    f1p, lg, enc = F1Probe(), Ledger(), Encounters()
    w.ledger, w.p2log = lg.buf, enc.buf
    w.observers += [lg, f1p, enc]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "ledger": lg.results(), "enc": enc.results(),
           **f1p.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {f1p.pops}", flush=True)


def pilot():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: zero checks have not passed")
    po = HERE / "output_pilot"
    me = [sys.executable, str(Path(__file__).resolve())]
    jobs = [(a, s) for a in ("c", "p") for s in PILOT]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["pilotone", j[0], str(j[1])]), jobs))
    n = {a: Counter() for a in ("c", "p")}
    for a, s in jobs:
        n[a].update(json.loads((po / f"{a}_seed_{s}.json").read_text(encoding="utf-8"))["enc"])
    L = ["# P2 feasibility pilot (seeds 2513-2516, 20 years; behaviour only, extinction not looked at)\n"]
    for a in ("c", "p"):
        x = n[a]
        trig = sum(v for k, v in x.items() if k.startswith("trigger_"))
        taken = sum(v for k, v in x.items() if k.startswith("taken_"))
        L.append(f"- {a}: seeker-weeks {x['seeker_weeks']}, with an eligible single in sight "
                 f"{x['seeker_weeks_eligible_in_sight'] / max(1, x['seeker_weeks']):.3f}; trigger weeks {trig} "
                 f"({', '.join(f'{k[8:]} {v}' for k, v in sorted(x.items()) if k.startswith('trigger_'))}); "
                 f"explore step taken {taken} ({taken / max(1, trig):.3f}); people newly partnered {x['new_partnered_people']}")
    p = n["p"]
    trig = sum(v for k, v in p.items() if k.startswith("trigger_"))
    share = p["taken_outward"] / trig if trig else 0.0
    passed = share >= PILOT_GATE
    L.append(f"\nOutward step taken in {p['taken_outward']} of {trig} trigger weeks in P ({share:.3f}); gate "
             f"{PILOT_GATE:.2f}: **{'PASS' if passed else 'STOP'}**\n")
    (po / "pilot.md").write_text("\n".join(L), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L), flush=True)


def run_all():
    pf = HERE / "output_pilot" / "pilot.md"
    if not pf.exists() or "**PASS**" not in pf.read_text(encoding="utf-8"):
        sys.exit("ABORT: the pilot has not passed")
    setup("p2")
    fp = fingerprint()
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for a in ("c", "p", "s") for s in SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), todo))
    bad = [(a, s) for a in ("c", "p", "s") for s in SEEDS
           if json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8"))["code_hash"] != fp]
    print("ALL DONE; code fingerprint unchanged" if not bad else f"HARD STOP: fingerprint changed in {bad[:5]}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hash_run(sys.argv[2], int(sys.argv[3]), 20, json.loads(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "pilot":
        pilot()
    elif cmd == "pilotone":
        run_one(sys.argv[2], int(sys.argv[3]), years=20, out=HERE / "output_pilot")
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run_all()
