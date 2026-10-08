"""MC1 — a camp that goes where the couple goes (preregistration.md, frozen as `MC1-frozen`). Arms on F1's 64 seeds,
120 years, in one copy of the code (`code_mc1`: HF4's logging copy plus the `moving_camp` setting):
c (settings off, must reproduce F1), m (moving_camp = 1), s (sham_draw = 1). Observers: F1's (whole run), C1's (first 40
years) and HF4's ledger (whole run).

  python experiments/MC1_moving_camp/run_mc1.py zero    # off + log reproduces the control; m and s differ
  python experiments/MC1_moving_camp/run_mc1.py pilot   # feasibility: m on seeds 1701-1704, 20 years
  python experiments/MC1_moving_camp/run_mc1.py run     # c, m, s on the 64 seeds (only after the pilot passes)
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
CODES = {"mc1": HERE / "code_mc1", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS, C1_YEARS = 52, 120, 40
SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))
PILOT = tuple(range(1701, 1705))
ARMS = {"c": {}, "m": {"moving_camp": 1}, "s": {"sham_draw": 1}}
F1OUT = EXP / "F1_baseline_fragility" / "output"


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "C1_couples_apart", "HF4_hunger_ledger"):
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


def hash_run(code, seed, years, kw, log):
    setup(code)
    w = make_world(seed, **kw)
    if log:
        from run_hf4 import Ledger
        lg = Ledger()
        w.ledger = lg.buf
        w.observers.append(lg)
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
    for seed in (601, 811):
        base[seed] = call("e13r", seed, {}, False)
        t = base[seed] == call("mc1", seed, {}, True)
        ok &= t
        lines.append(f"settings off, ledger on, seed {seed}, 20 years: copy reproduces the control world: {'yes' if t else 'NO'}")
    for arm in ("m", "s"):
        t = call("mc1", 601, ARMS[arm], True) != base[601]
        ok &= t
        lines.append(f"arm {arm} on, seed 601, 20 years: the world differs from the control: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["mc1"] / "acl")


def run_one(arm, seed, years=YEARS, out=None, c1_only=False):
    setup("mc1")
    import run_c1
    from run_f1 import Probe as F1Probe
    from run_hf4 import Ledger
    f0 = fingerprint()
    w = make_world(seed, **ARMS[arm])
    f1p, c1p, lg = F1Probe(), run_c1.Probe(), Ledger()
    w.ledger = lg.buf
    w.observers += [lg, c1p] if c1_only else [lg, f1p, c1p]
    for week in range(years * WPY):
        if week == C1_YEARS * WPY and c1p in w.observers:
            w.observers.remove(c1p)
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "c1": c1p.results(), "ledger": lg.results()}
    if not c1_only:
        res.update(f1p.results())
        if arm == "c":
            res["reproduces"] = json.loads((F1OUT / f"seed_{seed}.json").read_text(encoding="utf-8"))["pops"] == f1p.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {f1p.pops}, reproduces F1: {res.get('reproduces')}", flush=True)


def pilot():
    me = [sys.executable, str(Path(__file__).resolve())]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["pilotone", str(s)]), PILOT))
    n = Counter()
    for s in PILOT:
        n.update(json.loads((OUT / "pilot" / f"m_seed_{s}.json").read_text(encoding="utf-8"))["c1"]["n"])
    share = n["apart"] / n["couple_weeks"] if n["couple_weeks"] else 1.0
    ok = share <= 0.24
    line = (f"MC1 feasibility pilot, seeds {PILOT[0]}-{PILOT[-1]}, 20 years: couples apart in {share:.1%} of "
            f"{n['couple_weeks']:,} couple-weeks (must be at most 24%): {'PASS' if ok else 'STOP'}")
    (OUT / "pilot" / "verdict.txt").write_text(line + "\n", encoding="utf-8")
    print(line, flush=True)
    return ok


def run_all():
    for f, word in ((OUT / "zero.txt", "All: PASS"), (OUT / "pilot" / "verdict.txt", "PASS")):
        if not f.exists() or word not in f.read_text(encoding="utf-8"):
            sys.exit(f"ABORT: {f.name} has not passed")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for a in ARMS for s in SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), todo))
    R = [json.loads((OUT / f"c_seed_{s}.json").read_text(encoding="utf-8")) for s in SEEDS]
    bad = [r["seed"] for r in R if not r.get("reproduces")]
    print("ALL DONE; control reproduces F1" if not bad else f"HARD STOP: control does not reproduce F1 on {bad}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "hashrun":
        print(hash_run(sys.argv[2], int(sys.argv[3]), 20, json.loads(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "pilotone":
        run_one("m", int(sys.argv[2]), years=20, out=OUT / "pilot", c1_only=True)
    elif cmd == "pilot":
        sys.exit(0 if pilot() else 1)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run_all()
