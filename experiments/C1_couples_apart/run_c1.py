"""C1 — why couples drift apart (questions.md, frozen as `C1-questions`). Read-only replays of control worlds.

  python experiments/C1_couples_apart/run_c1.py verify      # observer read-only (two seeds, 20 years)
  python experiments/C1_couples_apart/run_c1.py discovery   # seeds 501-516, 40 years
  python experiments/C1_couples_apart/run_c1.py holdout     # seeds 1101-1116, 40 years (after the discovery write-up)
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
CODE = EXP / "E13R_replication" / "code_e13r"
F1OUT = EXP / "F1_baseline_fragility" / "output"
OUT = HERE / "output"
WPY, YEARS = 52, 40
DISCOVERY = tuple(range(501, 517))
HOLDOUT = tuple(range(1101, 1117))


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def bucket(d):
    return "3" if d == 3 else "4-6" if d <= 6 else "7+"


class Probe:
    """Reads the world after each week. Draws no random numbers; writes nothing to the world."""

    def __init__(self):
        self.pops = []
        self.n = Counter()                    # counts, keyed by strings
        self.spells = []                      # lengths of finished apart spells (weeks)
        self.run = {}                         # couple -> current apart run
        self.prev = {}                        # person -> location last week
        self.paired_at = {}                   # couple -> tick paired (None for pairs made before observation)

    def __call__(self, world, events):
        from acl.mind import hunger_of
        from acl.util import distance
        c, tick = world.cfg, world.tick
        t = tick - 1
        if t % 520 == 519:
            self.pops.append(len(world.living()))
        for e in events:
            if e["k"] == "pair":
                self.paired_at[tuple(sorted((e["a"], e["b"])))] = t
        season = world.season
        n = self.n
        seen = set()
        for wmn in world.living():
            if wmn.sex != "F" or not (c.fertile_from <= wmn.years(tick) < c.fertile_until) or not wmn.partner:
                continue
            man = world.people[wmn.partner]
            if not man.alive:
                continue
            key = tuple(sorted((wmn.id, man.id)))
            seen.add(key)
            d = distance(wmn.loc, man.loc, c.width, c.height)
            apart = d > c.camp_radius
            small = any(x.age(tick) < 6 * WPY for x in world.dependents(wmn.id))
            since = self.paired_at.get(key)
            yrs = "unknown" if since is None else "<2" if t - since < 2 * WPY else "2-9" if t - since < 10 * WPY else "10+"
            r = wmn.rel.get(man.id)
            aff = r.affection if r else 0.0
            affb = "<0.3" if aff < 0.3 else "0.3-0.6" if aff < 0.6 else "0.6+"
            n["couple_weeks"] += 1
            n["apart"] += apart
            for label in (f"kids:{small}", f"season:{season}", f"years:{yrs}", f"aff:{affb}"):
                n[f"cw|{label}"] += 1
                n[f"ap|{label}"] += apart
            if apart:
                n[f"dist|{bucket(d)}"] += 1
                self.run[key] = self.run.get(key, 0) + 1
            elif key in self.run:
                self.spells.append(self.run.pop(key))
            if d > c.reach:
                n["beyond"] += 1
                for p, q in ((wmn, man), (man, wmn)):
                    cons = p.considered or []
                    n["beyond_pw"] += 1
                    n["beyond_join_top4"] += any(o[0] == "join" for o in cons)
                    chosen = next((o[0] for o in cons if o[3]), "none")
                    n[f"beyond_chosen|{chosen}"] += 1
                    hu = hunger_of(world, p, sum(x.need(c, tick) for x in world.dependents(p.id)))
                    n["beyond_hunger_sum"] += hu
                    rr = p.rel.get(q.id)
                    n["beyond_aff_sum"] += rr.affection if rr else 0.0
            pw, pm = self.prev.get(wmn.id), self.prev.get(man.id)
            if pw is not None and pm is not None:
                pd = distance(pw, pm, c.width, c.height)
                mw = distance(pw, wmn.loc, c.width, c.height)
                mm = distance(pm, man.loc, c.width, c.height)
                if pd <= c.camp_radius < d:
                    n["split"] += 1
                    who = "both" if mw and mm else "woman" if mw else "man" if mm else "none"
                    n[f"split_who|{who}"] += 1
                    for p, moved in ((wmn, mw), (man, mm)):
                        if moved:
                            chosen = next((o[0] for o in (p.considered or []) if o[3]), "none")
                            n[f"split_action|{chosen}"] += 1
                elif pd > c.camp_radius >= d:
                    n["rejoin"] += 1
                    for p, moved in ((wmn, mw), (man, mm)):
                        if moved:
                            chosen = next((o[0] for o in (p.considered or []) if o[3]), "none")
                            n[f"rejoin_action|{chosen}"] += 1
        for key in [k for k in self.run if k not in seen]:
            self.spells.append(self.run.pop(key))       # couple ended (death, ageing past 45) while apart
        self.prev = {p.id: p.loc for p in world.living()}

    def results(self):
        return {"pops": self.pops, "n": dict(self.n), "spells": self.spells + list(self.run.values())}


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def run_one(seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "years": years, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **probe.results()}
    f1 = F1OUT / f"seed_{seed}.json"
    if f1.exists():
        saved = json.loads(f1.read_text(encoding="utf-8"))["pops"][: years // 10]
        res["reproduces"] = saved == probe.pops[: len(saved)] and len(probe.pops) == len(saved)
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: pops {probe.pops}, reproduces F1: {res.get('reproduces')}", flush=True)


def verify(seeds=(501, 1101), years=20):
    setup()
    lines, ok = [], True
    for seed in seeds:
        hs = []
        for with_probe in (False, True):
            w = make_world(seed)
            if with_probe:
                w.observers.append(Probe())
            for _ in range(years * WPY):
                w.step()
            hs.append(w.state_hash())
        t = hs[0] == hs[1]
        ok &= t
        lines.append(f"observer, seed {seed}, {years} years: {'READ-ONLY' if t else 'CHANGES THE WORLD'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    return ok


def batch(seeds):
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in seeds if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["one", str(s)]), todo))
    R = [json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in seeds]
    bad = [r["seed"] for r in R if r.get("reproduces") is False or r["code_hash"] != r["code_hash_after"]]
    print("ALL REPRODUCE, CODE UNCHANGED" if not bad else f"HARD STOP: {bad}", flush=True)
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        run_one(int(sys.argv[2]))
    elif cmd == "verify":
        sys.exit(0 if verify() else 1)
    elif cmd == "discovery":
        sys.exit(0 if batch(DISCOVERY) else 1)
    elif cmd == "holdout":
        sys.exit(0 if batch(HOLDOUT) else 1)
