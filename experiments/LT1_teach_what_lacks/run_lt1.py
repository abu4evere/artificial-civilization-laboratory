"""LT1 — teach what the learner lacks (questions.md, frozen as `LT1-frozen`). `code_lt1` = `code_v3` +
`teach_what_lacks` (T), default 0, + LU1's read-only lesson logging to `world.lu1log`. The full difference is
`v3_to_lt1.diff`.

  python experiments/LT1_teach_what_lacks/run_lt1.py zero    # hard stops: off = code_v3; T acts; read-only; reload
  python experiments/LT1_teach_what_lacks/run_lt1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"lt1": HERE / "code_lt1", "v3": EXP / "NV3_nature_v3" / "code_v3"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(11001, 11513))       # 512 new seeds, used by no study
SMOKE_SEEDS = (9997, 9998)
V3 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1}
ARMS = {"c": {}, "t": {"teach_what_lacks": 1}}
OUTCOMES = ("known", "own_bad", "not_open", "part_shown", "cannot_follow", "taken")


def setup(code="lt1"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "CA1_chain_audit", "LM1_memory_and_parts"):
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
    return code_hash(CODES["lt1"] / "acl")


class Weeks:
    """Read-only: living person-weeks."""

    def __init__(self):
        self.n = 0

    def __call__(self, world, events):
        self.n += len(world.living())


def observers(w):
    from run_ca1 import Chain
    from run_f1 import Probe
    from run_lm1 import Makes
    w.lu1log = []
    w.lm1log = []
    return Probe(), Chain(), Makes(), Weeks()


def summarise(w, ch, mk, wk):
    from run_lm1 import summarise as lm1_summarise
    base = lm1_summarise(w, ch, mk, w.lm1log)
    kinds = ch.results(w)
    useful = {k["sig"] for k in kinds if k["max_factor"] is not None and k["max_factor"] >= 1.05}
    first = {s: k["first_by"] for s, k in ch.kinds.items()}
    c = Counter()
    lo = Counter()
    for (t, learner, teacher, meant, sig, out, cred, op, parent, part, age, claim) in w.lu1log:
        grp = "useful" if meant in useful else "other"
        c[f"{grp}:{out}"] += 1
        c[f"{grp}:{'parent' if parent else 'other_teacher'}:{out}"] += 1
        c[f"{grp}:{'child' if age < 16 * WPY else 'adult'}:{out}"] += 1
        c[f"{grp}:{'inventor' if first.get(meant) == teacher else 'not_inventor'}:{out}"] += 1
        if part:
            c[f"{grp}:part_lesson:{out}"] += 1
        if out == "not_open":
            lo[f"{grp}:chance_bin{min(9, int(cred * op * 10))}"] += 1     # the chance of taking it, in tenths
            lo[f"{grp}:cred_sum"] += cred
            lo[f"{grp}:open_sum"] += op
        if out == "taken" and grp == "useful":
            c["useful:taken_made_later"] += learner in mk.by.get(sig, ())
    taken = [(r[1], r[4]) for r in w.lu1log if r[5] == "taken" and r[4] in useful]
    py = wk.n / WPY
    offered = sum(1 for r in w.lu1log if r[3] in useful)
    known = sum(1 for r in w.lu1log if r[3] in useful and r[5] == "known")
    return {"lessons": dict(c), "not_open": dict(lo), "useful_kinds": len(useful), "person_years": py,
            "learned_py": len(set(taken)) / py if py else None, "repeat_acq": len(taken) - len(set(taken)),
            "offered_py": offered / py if py else None, "taken_py": len(taken) / py if py else None,
            "take_rate": len(taken) / offered if offered else None,
            "known_share": known / offered if offered else None,
            "link3": base["link3"], "useful": base["useful"], "passed": base["passed"]}


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("lt1")
    from acl.world import World
    a = make_world(seed, ARMS["t"])
    a.lu1log = []
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    b.lu1log = []
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    held = sum(len(p.told_known) for p in a.people.values())
    return held > 0 and world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("lt1", seed, years, "{}", 0) == call("v3", seed, years, "{}", 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: teach_what_lacks 0 = code_v3: {'yes' if t else 'NO'}")
    t = call("lt1", 501, 20, json.dumps(ARMS["t"]), 0) != call("lt1", 501, 20, "{}", 0)
    ok &= t
    lines.append(f"arm t, seed 501, 20 years: the setting changes the world (it acts): {'yes' if t else 'NO'}")
    for arm in ("c", "t"):
        t = call("lt1", 501, 20, json.dumps(ARMS[arm]), 1) == call("lt1", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without observers and logging: "
                     f"{'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm t, seed 501: saved at year 10 (teachers' memories held) and reloaded, continues exactly to year 15: "
                 f"{'yes' if t else 'NO'}")
    setup("lt1")
    lines.append(f"code_lt1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("lt1")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, ch, mk, wk = observers(w)
    w.observers += [probe, ch, mk, wk]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v3", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "pops": probe.pops, "deaths": probe.results().get("deaths"), **summarise(w, ch, mk, wk)}
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
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
