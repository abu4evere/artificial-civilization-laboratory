"""CT1 — courting as nature (questions.md, frozen as `CT1-frozen`). `code_ct1` = `code_v3` + `familiar_attraction` (K1)
and `lonely_courting` (K2), both default 0, plus read-only logging to `world.ct1log` (not saved; read by nothing in the
world). The full difference is `v3_to_ct1.diff`.

  python experiments/CT1_courting_nature/run_ct1.py zero    # hard stops: off = code_v3; each acts; read-only; reload
  python experiments/CT1_courting_nature/run_ct1.py smoke   # throwaway seeds 9971-9972, 8 years, every arm (code check only)
  python experiments/CT1_courting_nature/run_ct1.py run     # c, k1, k2, k12 on seeds 8201-8456, 120 years (skips saved)
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
CODES = {"ct1": HERE / "code_ct1", "v3": EXP / "NV3_nature_v3" / "code_v3"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(8201, 8457))
SMOKE_SEEDS = (9971, 9972)
V3 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1}
ARMS = {"c": {}, "k1": {"familiar_attraction": 0.3}, "k2": {"lonely_courting": 1},
        "k12": {"familiar_attraction": 0.3, "lonely_courting": 1}}
LONELY_BINS = (0.25, 0.5, 0.75, 1.01)                  # upper edges
FAM_BINS = (0.05, 0.15, 0.35, 0.6, 1.01)


def setup(code="ct1"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **V3, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["ct1"] / "acl")


def _bin(x, edges):
    return next(i for i, e in enumerate(edges) if x < e)


class Courting:
    """Read-only, after each week: courting attempts on someone not yet a partner (from `world.ct1log`), whether each
    was accepted (a 'pair' event between the two the same week), single adult-weeks by loneliness, and births with
    both parents' ages."""

    def __init__(self):
        self.c = Counter()
        self.seen = 0

    def __call__(self, world, events):
        tick = world.tick - 1
        pairs = {(e.get("a"), e.get("b")) for e in events if e["k"] == "pair"}
        log = world.ct1log
        for t, a, b, aff, fam_q, fam_p, lonely, attr in log[self.seen:]:
            ok = (a, b) in pairs
            self.c["attempts"] += 1
            self.c["accepted"] += ok
            if aff < 0.05:
                self.c["attempts_no_aff"] += 1
                self.c["accepted_no_aff"] += ok
            fb = _bin(fam_q, FAM_BINS)
            self.c[f"att_fam{fb}"] += 1
            self.c[f"acc_fam{fb}"] += ok
            self.c[f"att_lonely{_bin(lonely, LONELY_BINS)}"] += 1
            self.c["att_known"] += fam_p >= 0.35            # the suitor knows the one they court well
        self.seen = len(log)
        for p in world.living():
            if p.age(world.tick) >= 16 * WPY and p.partner is None:
                self.c["single_adult_weeks"] += 1
                self.c[f"single_weeks_lonely{_bin(p.loneliness, LONELY_BINS)}"] += 1
        for e in events:
            if e["k"] == "birth":
                m = world.people[e["a"]]
                f = world.people.get(e.get("father")) if e.get("father") else None
                self.c["births"] += 1
                if m.years(world.tick) < 18:
                    self.c["births_mother_under_18"] += 1
                if f is not None and f.birth < m.birth - 15 * WPY:
                    self.c["births_father_15_older"] += 1
            elif e["k"] == "pair":
                self.c["pairs"] += 1
        _ = tick

    def results(self):
        return {"courting": dict(self.c)}


def observers(w):
    from run_f1 import Probe
    w.ct1log = []
    return Probe(), Courting()


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("ct1")
    from acl.world import World
    a = make_world(seed, ARMS["k12"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("ct1", seed, years, "{}", 0) == call("v3", seed, years, "{}", 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: both settings 0 = code_v3: {'yes' if t else 'NO'}")
    base = call("ct1", 501, 20, "{}", 0)
    for arm in ("k1", "k2", "k12"):
        t = call("ct1", 501, 20, json.dumps(ARMS[arm]), 0) != base
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: the setting changes the world (it acts): {'yes' if t else 'NO'}")
    for arm in ("c", "k12"):
        t = call("ct1", 501, 20, json.dumps(ARMS[arm]), 1) == call("ct1", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers and logging: "
                     f"{'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm k12, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    setup("ct1")
    lines.append(f"code_ct1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("ct1")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, court = observers(w)
    w.observers += [probe, court]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v3", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), **probe.results(), **court.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
    q = (HERE / "questions.md").read_text(encoding="utf-8")
    if "SIGNED OFF" not in q.splitlines()[0]:
        sys.exit("ABORT: CT1 is not signed off")
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, 8, HERE / "output_smoke")
    elif cmd == "run":
        batch()
