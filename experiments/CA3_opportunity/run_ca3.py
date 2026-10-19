"""CA3 — opportunity or availability (questions.md, frozen as `CA3-frozen`). `code_ca3` = `code_ca2` + the learner's recipes
in each teaching-possible talk; logging only, to `world.ca2log` (not saved, read by nothing in the world).

  python experiments/CA3_opportunity/run_ca3.py zero     # hard stop: code_ca3 with logging = code_v2
  python experiments/CA3_opportunity/run_ca3.py pilot    # throwaway seed 9941, 10 years: the log's working only
  python experiments/CA3_opportunity/run_ca3.py run      # CA1's seeds 6301-6332, 120 years (2 workers); each replay checked
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "CA2_teaching_gates"))
import run_ca2 as C2  # noqa: E402

C2.CODES["ca3"] = HERE / "code_ca3"
OUT = HERE / "output"
WPY, YEARS = 52, 120
DISCOVERY, HOLDOUT = C2.DISCOVERY, C2.HOLDOUT
LINE = 13                                    # availability line, weeks (frozen)


def setup():
    C2.setup("ca3")


def fingerprint():
    from run_e7 import code_hash
    return code_hash(C2.CODES["ca3"] / "acl")


def levels(kinds, log):
    """CA2's gate levels for useful never-passed kinds, by CA2's rule (talk records here carry one more field)."""
    useful = {k["sig"] for k in kinds if k["max_factor"] is not None and k["max_factor"] >= 1.05}
    first = {k["sig"]: k["first_by"] for k in kinds}
    never = {k["sig"] for k in kinds if k["sig"] in useful and not k["transmitted"]}
    lv = {s: 0 for s in never}
    for rec in log:
        kind = rec[1]
        if kind == "talk":
            p, recipes = rec[2], rec[4]
            for s in recipes:
                if s in lv and first[s] == p and lv[s] < 1:
                    lv[s] = 1
        elif kind == "offers":
            _, _, teacher, _, valued, top3, chosen = rec
            for s in valued:
                if s in lv and first[s] == teacher:
                    lv[s] = max(lv[s], 2)
            for s in top3:
                if s in lv and first[s] == teacher:
                    lv[s] = max(lv[s], 3)
            if chosen in lv and first[chosen] == teacher:
                lv[chosen] = max(lv[chosen], 4)
        elif kind == "hear":
            _, _, _, teacher, meant, _, outcome = rec
            if meant in lv and first[meant] == teacher:
                lv[meant] = max(lv[meant], {"known": 4, "refused_no_good": 5, "not_believed": 5,
                                            "not_followable": 6, "taken": 7}[outcome])
    return useful, lv


def summarise(kinds, log, deaths, born, end_tick):
    useful, lv = levels(kinds, log)
    ks = {k["sig"]: k for k in kinds}
    first = {s: k["first_by"] for s, k in ks.items()}
    dropped = {}                                    # (person, sig) -> (tick, why), first drop
    for rec in log:
        if rec[1] in ("evict", "forget"):
            key = (rec[2], rec[3])
            if key not in dropped:
                dropped[key] = (rec[0], "pushed out by the 12-recipe limit" if rec[1] == "evict" else "forgotten as useless")
    talks = defaultdict(list)                       # sig -> [(tick, learner, learner recipes)] by its first knower
    valued_ever = set()
    for rec in log:
        if rec[1] == "talk":
            t, _, p, q, recipes, lrec = rec
            for s in recipes:
                if s in useful and first[s] == p:
                    talks[s].append((t, q, lrec))
        elif rec[1] == "offers" and rec[2] is not None:
            for s in rec[4]:
                if s in useful and first[s] == rec[2]:
                    valued_ever.add(s)
    out = {"g1_stopped": 0, "availability": 0, "opportunity": 0, "lost_how": Counter(), "no_birth": 0,
           "composite_talks": 0, "composite_followable": 0, "groups": {}}
    groups = {"passed on": [], "never passed on": []}
    for s in useful:
        k = ks[s]
        fb, t0 = first[s], k["first_tick"]
        cands = []
        if (fb, s) in dropped:
            cands.append(dropped[(fb, s)])
        if fb in deaths:
            cands.append((deaths[fb], "the first knower died"))
        end, how = min(cands) if cands else (end_tick, "held to the end")
        hold = max(0, end - t0)
        while_held = [x for x in talks.get(s, ()) if t0 <= x[0] <= end]
        age = (t0 - born[fb]) / WPY if fb in born else None
        groups["passed on" if k["transmitted"] else "never passed on"].append(
            (hold, len(while_held), len({x[1] for x in while_held}), age, s in valued_ever))
        if s in lv and lv[s] == 0:
            out["g1_stopped"] += 1
            out["lost_how"][how] += 1
            out["availability" if hold < LINE else "opportunity"] += 1
        if s in lv:
            made_parts = [x for x in k["parts"]]
            if made_parts:
                for _, _, lrec in while_held:
                    out["composite_talks"] += 1
                    out["composite_followable"] += all(x in lrec for x in made_parts)
        if fb not in born:
            out["no_birth"] += 1
    for g, rows in groups.items():
        ages = [r[3] for r in rows if r[3] is not None]
        out["groups"][g] = {"n": len(rows), "hold_weeks_median": statistics.median([r[0] for r in rows]) if rows else None,
                            "talks_median": statistics.median([r[1] for r in rows]) if rows else None,
                            "learners_median": statistics.median([r[2] for r in rows]) if rows else None,
                            "inventor_child_share": sum(a < 16 for a in ages) / len(ages) if ages else None,
                            "valued_share": sum(r[4] for r in rows) / len(rows) if rows else None}
    out["lost_how"] = dict(out["lost_how"])
    return out


def run_world(seed, years):
    setup()
    from run_ca1 import Chain
    from run_f1 import Probe
    w = C2.make_world(seed)
    w.ca2log = []
    probe, ch, dz = Probe(), Chain(), C2.Deaths()
    w.observers += [probe, ch, dz]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    kinds = ch.results(w)
    for k in kinds:
        k["first_by"] = ch.kinds[k["sig"]]["first_by"]
    born = {pid: p.birth for pid, p in w.people.items()}
    return w, probe, kinds, dz.at, born


def hashrun(code, seed, years):
    C2.setup(code)
    w = C2.make_world(seed)
    if code == "ca3":
        w.ca2log = []
    for _ in range(years * WPY):
        w.step()
    return C2.world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed in (501, 601):
        t = call("ca3", seed, 20) == call("v2", seed, 20)
        ok &= t
        lines.append(f"seed {seed}, 20 years: code_ca3 with logging on = code_v2: {'yes' if t else 'NO'}")
    setup()
    lines.append(f"code_ca3 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(seed, years, out):
    setup()
    f0 = fingerprint()
    w, probe, kinds, deaths, born = run_world(seed, years)
    f1 = C2.CA1_OUT / f"seed_{seed}.json"
    ca1 = json.loads(f1.read_text(encoding="utf-8")) if f1.exists() else {"world_hash": None}
    s = summarise(kinds, w.ca2log, deaths, born, w.tick)
    res = {"seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": C2.world_hash(w), "same_as_ca1": C2.world_hash(w) == ca1["world_hash"], "pops": probe.pops,
           "log_records": len(w.ca2log), **s}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: done, same as CA1: {res['same_as_ca1']}", flush=True)


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
        run_one(9941, 10, HERE / "output_pilot")
    elif cmd == "run":
        batch()
