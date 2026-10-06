"""S1 — why stashing almost never wins (questions.md). Read-only replays of E13R's control (Arm A), seeds 501-516, on a
copy of the E13R code that records each person's options and choice.

Checks first: the instrumented code with its probe leaves the world exactly as the E13R code does (state hash, 20
years); each replay's population must equal the saved E13R run.

  python experiments/S1_stash_decisions/run_s1.py all
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E13R = HERE.parent / "E13R_replication"
CODES = {"s1": HERE / "code_s1", "e13r": E13R / "code_e13r"}
SEEDS = tuple(range(501, 517))
WPY = 52
T = 0.2                                        # choice_temperature
OUT = HERE / "output"
FOODISH = ("food", "seeds")


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def dd():
    return defaultdict(float)


class Probe:
    def __init__(self):
        self.pops = []
        self.n = defaultdict(dd)                # season -> counter name -> count / sum
        self.winners = defaultdict(Counter)     # season -> winning action when put-food/seed offered and not chosen
        self.prob_bins = Counter()              # probability of putting, when offered
        self.learn = []                         # owner took own stash back after 2+ weeks: belief before, after
        self.found_gone = 0
        self.told = Counter()                   # "learn" events about food/seed beliefs, by how
        self.holders = []                       # decade samples: adults with a positive food/seed belief
        self.prev = {}

    def __call__(self, world, events):
        tick = world.tick - 1
        if tick % 520 == 519:
            self.pops.append(len(world.living()))
        log = getattr(world, "s1_log", None)
        if log is None:
            world.s1_log = []
            log = []
        for d in log:
            q = world.people.get(d["pid"])
            if q is None or q.age(world.tick) < 16 * WPY:
                continue
            s = d["season"]
            n = self.n[s]
            n["weeks"] += 1
            if d["food"] - d["line"] >= 1:
                n["elig_food"] += 1
            if d["seeds"] - (d["line"] - d["food"] if d["food"] < d["line"] else 0.0) >= 1:
                n["elig_seeds"] += 1
            opts = d["options"]
            scores = [o[0] for o in opts]
            put = next((k for k, o in enumerate(opts) if o[1] == "put"), None)
            fk = next((k for k, o in enumerate(opts) if o[1] == "forage"), None)
            chosen = opts[d["chosen"]][1]
            if put is None:
                continue
            n["put_offered"] += 1
            if opts[put][2] not in FOODISH:
                n["put_material"] += 1
                if d["food"] - d["line"] >= 1:
                    n["material_while_food_eligible"] += 1
                continue
            n["put_food_offered"] += 1
            top = max(scores)
            ws = [math.exp((x - top) / T) for x in scores]
            prob = ws[put] / sum(ws)
            n["prob_sum"] += prob
            self.prob_bins[min(9, int(prob * 10))] += 1
            n["put_score"] += opts[put][0]
            n["put_habit"] += d["q_put"]
            n["gap"] += top - opts[put][0]
            if fk is not None:
                n["with_forage"] += 1
                n["forage_score"] += opts[fk][0]
                n["forage_habit"] += d["q_forage"]
            b = d["b_food"] if opts[put][2] == "food" else d["b_seeds"]
            h = d["h_food"] if opts[put][2] == "food" else d["h_seeds"]
            n["has_belief"] += b is not None
            n["belief_sum"] += b or 0.0
            n["heard_only"] += (b is None and h)
            if d["chosen"] == put:
                n["put_food_chosen"] += 1
            else:
                self.winners[s][chosen] += 1
        log.clear()
        for e in events:
            k = e["k"]
            if k == "take" and e.get("own") and e.get("weeks", 0) >= 2:
                p = world.people.get(e["a"])
                if p is not None:
                    s = world.season
                    before = self.prev.get(p.id, {})
                    self.learn.append({"weeks": e["weeks"], "got": e.get("food", 0.0),
                                       "before": {key: before.get(key) for key in before},
                                       "after": {key: v for key, v in p.beliefs.items() if key.split("@")[0] in FOODISH}})
            elif k == "found_gone":
                self.found_gone += 1
            elif k == "learn" and str(e.get("belief", "")).split("@")[0] in FOODISH:
                self.told[e.get("how", "?")] += 1
        self.prev = {p.id: {key: v for key, v in p.beliefs.items() if key.split("@")[0] in FOODISH}
                     for p in world.living()}
        if tick % 520 == 519:
            adults = [p for p in world.living() if p.age(world.tick) >= 16 * WPY]
            own = sum(1 for p in adults if any(v > 0 for key, v in p.beliefs.items() if key.split("@")[0] in FOODISH))
            told = sum(1 for p in adults if any(h[0] > 0 for key, h in p.heard.items()
                                                if key.startswith("b:") and key[2:].split("@")[0] in FOODISH))
            self.holders.append({"adults": len(adults), "own_positive": own, "told_positive": told})

    def results(self):
        return {"pops": self.pops, "n": {str(s): dict(v) for s, v in self.n.items()},
                "winners": {str(s): dict(v) for s, v in self.winners.items()}, "prob_bins": dict(self.prob_bins),
                "learn": self.learn, "found_gone": self.found_gone, "told": dict(self.told), "holders": self.holders}


def run(seed):
    setup("s1")
    w = make_world(seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((E13R / "output" / f"a_seed_{seed}.json").read_text(encoding="utf-8"))
    res = {"seed": seed, "replay_matches": probe.pops == saved["pops"], **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches']}", flush=True)


def state_hash(code, probe, seed=501, years=20):
    setup(code)
    w = make_world(seed)
    if probe:
        w.observers.append(Probe())
    for _ in range(years * WPY):
        w.step()
    return w.state_hash()


if __name__ == "__main__":
    cmd = sys.argv[1]
    me = [sys.executable, str(Path(__file__).resolve())]
    if cmd == "hash":
        print(state_hash(sys.argv[2], sys.argv[3] == "1"))
    elif cmd == "all":
        h0 = subprocess.run(me + ["hash", "e13r", "0"], capture_output=True, text=True).stdout.strip()
        h1 = subprocess.run(me + ["hash", "s1", "1"], capture_output=True, text=True).stdout.strip()
        ok = bool(h0) and h0 == h1
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "verify.txt").write_text(f"seed 501, 20 years: instrumented code with probe "
                                        f"{'EQUALS' if ok else 'DIFFERS FROM'} the E13R code\n", encoding="utf-8")
        print("verify:", "EQUAL" if ok else "DIFFERENT", flush=True)
        if not ok:
            sys.exit("ABORT: the instrumented code or the probe changes the world")
        jobs = [s for s in SEEDS if not (OUT / f"seed_{s}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), jobs))
        print("ALL DONE", flush=True)
    else:
        run(int(cmd))
