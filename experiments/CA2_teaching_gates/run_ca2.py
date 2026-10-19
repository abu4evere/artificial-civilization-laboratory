"""CA2 — why does teaching pass on so little? (questions.md, frozen as `CA2-frozen`). `code_ca2` = `code_v2` + logging
lines only (to `world.ca2log`, not saved, read by nothing in the world). CA1's observer, loaded unchanged.

  python experiments/CA2_teaching_gates/run_ca2.py zero     # hard stop: code_ca2 with logging = code_v2
  python experiments/CA2_teaching_gates/run_ca2.py pilot    # throwaway seed 9931, 10 years: the log's working only
  python experiments/CA2_teaching_gates/run_ca2.py run      # CA1's seeds 6301-6332, 120 years (2 workers); each replay checked
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"ca2": HERE / "code_ca2", "v2": EXP / "NV2_nature_v2" / "code_v2"}
OUT = HERE / "output"
CA1_OUT = EXP / "CA1_chain_audit" / "output"
WPY, YEARS = 52, 120
DISCOVERY = tuple(range(6301, 6317))
HOLDOUT = tuple(range(6317, 6333))
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
GATES = ("G1 meets", "G2 valued", "G3 offered", "G4 chosen", "G5 new to the learner", "G6 believed", "G7 followable")


def setup(code="ca2"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "CA1_chain_audit"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **V2))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["ca2"] / "acl")


class Deaths:
    def __init__(self):
        self.at = {}

    def __call__(self, world, events):
        for e in events:
            if e["k"] == "death" and e.get("a"):
                self.at[e["a"]] = e["t"]


def hashrun(code, seed, years):
    setup(code)
    w = make_world(seed)
    if code == "ca2":
        w.ca2log = []
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
    for seed in (501, 601):
        t = call("ca2", seed, 20) == call("v2", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: code_ca2 with logging on = code_v2: {'yes' if t else 'NO'}")
    setup()
    lines.append(f"code_ca2 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def summarise(kinds, log, deaths, end_tick):
    """Turn the log into the frozen measures, per world."""
    useful = {k["sig"] for k in kinds if k["max_factor"] is not None and k["max_factor"] >= 1.05}
    first = {k["sig"]: k["first_by"] for k in kinds}
    never = {s for s in useful if not next(k for k in kinds if k["sig"] == s)["transmitted"]}
    level = {s: 0 for s in never}            # gates passed: 0 none ... 7 taken (as a changed kind)
    watch = Counter()
    taken = []                               # (tick, learner, sig learned) for G8
    dropped = defaultdict(list)              # (person, sig) -> ticks dropped, with why
    unmatched = 0
    for rec in log:
        t, kind = rec[0], rec[1]
        if kind == "talk":
            _, _, p, q, recipes = rec
            for s in recipes:
                if s in level and first[s] == p and level[s] < 1:
                    level[s] = 1
        elif kind == "offers":
            _, _, teacher, learner, valued, top3, chosen = rec
            for s in valued:
                if s in level and first[s] == teacher:
                    level[s] = max(level[s], 2)
            for s in top3:
                if s in level and first[s] == teacher:
                    level[s] = max(level[s], 3)
            if chosen in level and first[chosen] == teacher:
                level[chosen] = max(level[chosen], 4)
        elif kind == "hear":
            _, _, learner, teacher, meant, sig, outcome = rec
            if outcome == "taken" and sig in useful:
                taken.append((t, learner, sig))
            if meant in level and first[meant] == teacher:
                lv = {"known": 4, "refused_no_good": 5, "not_believed": 5, "not_followable": 6, "taken": 7}.get(outcome)
                if lv is None:
                    unmatched += 1
                else:
                    level[meant] = max(level[meant], lv)
        elif kind == "watch":
            _, _, watcher, maker, sig, outcome, copy = rec
            if sig in never and first[sig] == maker:
                watch[outcome] += 1
            if outcome == "taken" and copy in useful:
                taken.append((t, watcher, copy))
        elif kind in ("evict", "forget"):
            _, _, p, sig = rec
            dropped[(p, sig)].append((t, kind))
        else:
            unmatched += 1
    stopped = Counter()
    for s, lv in level.items():
        stopped["taken, but changed in the showing" if lv == 7 else GATES[lv]] += 1    # lv 0: stopped at G1, never met
    kept = Counter()
    for t, who, sig in taken:
        if t + WPY > end_tick:
            kept["not testable (world ended)"] += 1
            continue
        d = [x for x in dropped.get((who, sig), ()) if t < x[0] <= t + WPY]
        dt = deaths.get(who)
        if d:
            kept["pushed out by the 12-recipe limit" if d[0][1] == "evict" else "forgotten as useless"] += 1
        elif dt is not None and dt <= t + WPY:
            kept["died"] += 1
        else:
            kept["kept a year"] += 1
    return {"n_useful": len(useful), "n_never": len(never), "levels": Counter(level.values()),
            "stopped": stopped, "watch": watch, "kept": kept, "unmatched": unmatched}


def who_built(kinds, learners):
    """CA1's link-5 pairs (part X, better kind Y): who first knew Y, and was Y passed on."""
    ks = {k["sig"]: k for k in kinds}
    out = Counter()
    for y in kinds:
        for x in y["parts"]:
            xk = ks.get(x)
            if not xk or y["max_factor"] is None or xk["max_factor"] is None or y["max_factor"] <= xk["max_factor"]:
                continue
            if xk["max_factor"] < 1.05:
                continue
            who = ("the inventor" if y["first_by"] == xk["first_by"] else
                   "a learner" if y["first_by"] in learners.get(x, ()) else "unclear")
            out[f"{who}, {'passed on' if y['transmitted'] else 'not passed on'}"] += 1
    return out


def run_world(seed, years):
    setup()
    from run_ca1 import Chain
    from run_f1 import Probe
    w = make_world(seed)
    w.ca2log = []
    probe, ch, dz = Probe(), Chain(), Deaths()
    w.observers += [probe, ch, dz]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    kinds = ch.results(w)
    for k in kinds:
        k["first_by"] = ch.kinds[k["sig"]]["first_by"]
    learners = {s: list(k["learners"]) for s, k in ch.kinds.items()}
    return w, probe, kinds, learners, dz.at


def run_one(seed, years, out):
    setup()
    f0 = fingerprint()
    w, probe, kinds, learners, deaths = run_world(seed, years)
    f1 = CA1_OUT / f"seed_{seed}.json"
    ca1 = json.loads(f1.read_text(encoding="utf-8")) if f1.exists() else {"world_hash": None}   # pilot seeds: none
    s = summarise(kinds, w.ca2log, deaths, w.tick)
    res = {"seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "same_as_ca1": world_hash(w) == ca1["world_hash"], "pops": probe.pops,
           "log_records": len(w.ca2log), **{k: dict(v) if isinstance(v, Counter) else v for k, v in s.items()},
           "who_built": dict(who_built(kinds, learners))}
    res["levels"] = {str(k): v for k, v in res["levels"].items()}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: done, same as CA1: {res['same_as_ca1']}", flush=True)


def pilot():
    setup()
    from run_ca1 import Chain
    w = make_world(9931)
    w.ca2log = []
    ch, dz = Chain(), Deaths()
    w.observers += [ch, dz]
    for _ in range(10 * WPY):
        w.step()
    kinds = ch.results(w)
    for k in kinds:
        k["first_by"] = ch.kinds[k["sig"]]["first_by"]
    s = summarise(kinds, w.ca2log, dz.at, w.tick)
    print(f"pilot seed 9931, 10 years: {len(w.ca2log)} log records, by kind "
          f"{dict(Counter(r[1] for r in w.ca2log))}; unmatched {s['unmatched']}", flush=True)


def batch():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero check has not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in DISCOVERY + HOLDOUT if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(2) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["one", str(s), str(YEARS), str(OUT)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
    elif cmd == "one":
        run_one(int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4]))
    elif cmd == "pilot":
        pilot()
    elif cmd == "run":
        batch()
