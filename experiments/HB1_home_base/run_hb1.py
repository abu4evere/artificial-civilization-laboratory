"""HB1 — a shared home base (preregistration.md, frozen as `HB1-frozen`). Arms: h (home_base=1) and s (sham_draw=1),
each on F1's 64 seeds; F1's replays are the control. F1's observer for the whole run, C1's for the first 40 years.

  python experiments/HB1_home_base/run_hb1.py zero    # off reproduces the control; sham and home base each differ
  python experiments/HB1_home_base/run_hb1.py pilot   # feasibility: seeds 1201-1204, 20 years, manipulation only
  python experiments/HB1_home_base/run_hb1.py run     # both arms, 64 seeds (only after the pilot passes)
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
CODES = {"hb1": HERE / "code_hb1", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS, C1_YEARS = 52, 120, 40
SEEDS = tuple(range(501, 517)) + tuple(range(601, 617)) + tuple(range(811, 819)) + tuple(range(1101, 1125))
PILOT = tuple(range(1201, 1205))
ARMS = {"h": {"home_base": 1}, "s": {"sham_draw": 1}}


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "C1_couples_apart"):
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


def hash_run(code, seed, years, kw):
    setup(code)
    w = make_world(seed, **kw)
    for _ in range(years * WPY):
        w.step()
    return {"hash": world_hash(w)}


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(code, seed, kw):
        out = subprocess.run(me + ["hashrun", code, str(seed), json.dumps(kw)], capture_output=True, text=True).stdout
        return json.loads(out.strip().splitlines()[-1])["hash"]
    lines, ok = [], True
    base = {}
    for seed in (601, 811):
        base[seed] = call("e13r", seed, {})
        t = base[seed] == call("hb1", seed, {})
        ok &= t
        lines.append(f"settings off, seed {seed}, 20 years: copy reproduces the control world: {'yes' if t else 'NO'}")
    for arm, kw in ARMS.items():
        t = call("hb1", 601, kw) != base[601]
        ok &= t
        lines.append(f"arm {arm} on, seed 601, 20 years: the world differs from the control: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["hb1"] / "acl")


def run_one(arm, seed, years=YEARS, out=None, c1_only=False):
    setup("hb1")
    import run_c1
    from run_f1 import Probe as F1Probe
    f0 = fingerprint()
    w = make_world(seed, **ARMS[arm])
    f1p, c1p = F1Probe(), run_c1.Probe()
    w.observers += [c1p] if c1_only else [f1p, c1p]
    for week in range(years * WPY):
        if week == C1_YEARS * WPY and c1p in w.observers:
            w.observers.remove(c1p)             # observers never touch the world
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "c1": c1p.results()}
    if not c1_only:
        res.update(f1p.results())
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {f1p.pops}", flush=True)


def pilot():
    me = [sys.executable, str(Path(__file__).resolve())]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["pilotone", str(s)]), PILOT))
    n = Counter()
    for s in PILOT:
        n.update(json.loads((OUT / "pilot" / f"h_seed_{s}.json").read_text(encoding="utf-8"))["c1"]["n"])
    share = n["apart"] / n["couple_weeks"] if n["couple_weeks"] else 1.0
    ok = share <= 0.24
    line = (f"HB1 feasibility pilot, seeds {PILOT[0]}-{PILOT[-1]}, 20 years: couples apart in {share:.1%} of "
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
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "hashrun":
        print(json.dumps(hash_run(sys.argv[2], int(sys.argv[3]), 20, json.loads(sys.argv[4]))))
    elif cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "pilotone":
        run_one("h", int(sys.argv[2]), years=20, out=OUT / "pilot", c1_only=True)
    elif cmd == "pilot":
        sys.exit(0 if pilot() else 1)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run_all()
