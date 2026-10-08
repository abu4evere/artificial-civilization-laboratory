"""HF4 — the hunger ledger (questions.md, frozen as `HF4-questions`). Arms H (home_base = 1) and C (settings off), first 40
years, run on an instrumented logging copy of HB1's code (`code_hf4`) that records, at the moment of eating, each
person's need, food held, shortfall and food just given to dependants, into a list outside the world's state.

  python experiments/HF4_hunger_ledger/run_hf4.py zero        # the log changes nothing (state hash vs code_hb1)
  python experiments/HF4_hunger_ledger/run_hf4.py discovery   # seeds 501-516, checked against HB1's and F1's runs
  python experiments/HF4_hunger_ledger/run_hf4.py holdout     # new seeds 1601-1616 (after the discovery write-up)
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
CODES = {"hf4": HERE / "code_hf4", "hb1": EXP / "HB1_home_base" / "code_hb1"}
OUT = HERE / "output"
WPY, YEARS = 52, 40
DISCOVERY = tuple(range(501, 517))
HOLDOUT = tuple(range(1601, 1617))
ARMS = {"h": {"home_base": 1}, "c": {}}
SAVED = {"h": EXP / "HB1_home_base" / "output", "c": EXP / "F1_baseline_fragility" / "output"}
BIN = 0.01                      # coverage histogram bin width; coverage ≥ 5 goes in the last bin
NBINS = 501


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, **kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


class Ledger:
    """Holds the instrumented copy's log for one week and summarises it; reads nothing else from the world."""

    def __init__(self):
        self.buf = []
        self.pops = []
        self.n = Counter()
        self.hist = [0] * NBINS
        self.hist_starving = [0] * NBINS

    def __call__(self, world, events):
        t = world.tick - 1
        if t % 520 == 519:
            self.pops.append(len(world.living()))
        n = self.n
        for pid, adult, need, held, deficit, fed in self.buf:
            if not adult or need <= 0:
                continue
            cov = held / need
            b = min(NBINS - 1, int(cov / BIN))
            starving = deficit > 0.05
            n["aw"] += 1
            self.hist[b] += 1
            n["starving"] += starving
            if starving:
                self.hist_starving[b] += 1
                n["starving_deep"] += cov < 0.5
            for lo, hi, lab in ((0, 0.5, "lt05"), (0.5, 0.95, "05_095"), (0.95, 1.05, "095_105"), (1.05, 1.5, "105_15"),
                                (1.5, 3.0, "15_3"), (3.0, 1e9, "ge3")):
                if lo <= cov < hi:
                    n[f"band_{lab}"] += 1
            if fed > 0:
                n["carer_weeks"] += 1
                n["fed_share_sum"] += fed / (fed + held) if fed + held > 0 else 0.0
        self.buf.clear()

    def results(self):
        return {"pops": self.pops, "n": dict(self.n), "hist": self.hist, "hist_starving": self.hist_starving}


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["hf4"] / "acl")


def hash_run(code, arm, seed, years, log):
    setup(code)
    w = make_world(seed, **ARMS[arm])
    if log:
        lg = Ledger()
        w.ledger = lg.buf
        w.observers.append(lg)
    for _ in range(years * WPY):
        w.step()
    return w.state_hash()


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]
    lines, ok = [], True
    for arm in ARMS:
        for seed in (501, 1601):
            a = subprocess.run(me + ["hashrun", "hb1", arm, str(seed), "0"], capture_output=True, text=True).stdout.split()[-1]
            b = subprocess.run(me + ["hashrun", "hf4", arm, str(seed), "1"], capture_output=True, text=True).stdout.split()[-1]
            t = a == b
            ok &= t
            lines.append(f"arm {arm}, seed {seed}, 20 years: logging copy with the log on equals HB1's code: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("hf4")
    f0 = fingerprint()
    w = make_world(seed, **ARMS[arm])
    lg = Ledger()
    w.ledger = lg.buf
    w.observers.append(lg)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": fingerprint(), **lg.results()}
    saved = SAVED[arm] / (f"h_seed_{seed}.json" if arm == "h" else f"seed_{seed}.json")
    if saved.exists():
        res["reproduces"] = json.loads(saved.read_text(encoding="utf-8"))["pops"][: years // 10] == lg.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: pops {lg.pops}, reproduces saved: {res.get('reproduces')}", flush=True)


def batch(seeds):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the log has not been shown to change nothing")
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
    if cmd == "hashrun":
        print(hash_run(sys.argv[2], sys.argv[3], int(sys.argv[4]), 20, sys.argv[5] == "1"))
    elif cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd in ("discovery", "holdout"):
        sys.exit(0 if batch(DISCOVERY if cmd == "discovery" else HOLDOUT) else 1)
