"""G1 — who receives the food (questions.md). Read-only replays of E13R's control (Arm A), seeds 501-516, classifying
every gift from the world's own `give` events and the state at that moment.

  python experiments/G1_who_receives/run_g1.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E13R = HERE.parent / "E13R_replication"
CODE = E13R / "code_e13r"
SEEDS = tuple(range(501, 517))
WPY, WPS = 52, 13
OUT = HERE / "output"


def setup():
    sys.path.insert(0, str(CODE))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def tie(world, p, q):
    """The recipient's tie to the giver, before this gift (the gift itself raised the giver's affection by 0.03 and
    familiarity by 0.05; those are taken back out)."""
    if p.partner == q.id:
        return "partner"
    if p.id in (q.mother, q.father):
        st = q.stage(world.tick)
        return "own child, " + ("young" if st in ("infant", "child") else st)
    if q.id in (p.mother, p.father):
        return "parent"
    k = world.kinship(p, q)
    if k >= 0.8:
        return "sibling"
    if k > 0:
        return "other kin"
    r = p.rel.get(q.id)
    aff = (r.affection - 0.03) if r else 0.0
    fam = (r.familiarity - 0.05) if r else 0.0
    if aff >= 0.3:
        return "friend"
    if fam > 0.0:
        return "acquaintance"
    return "stranger"


class Probe:
    def __init__(self):
        self.pops = []
        self.by = defaultdict(lambda: defaultdict(lambda: [0, 0.0]))   # dimension -> "season|label" -> [gifts, food]
        self.received = defaultdict(float)                            # recipient -> food, whole run
        self.pair_year = defaultdict(float)                           # (year, giver, recipient) -> food
        self.giver_year = defaultdict(float)                          # (year, giver) -> food

    def add(self, dim, s, label, amount):
        for key in (f"{s}|{label}", f"all|{label}"):
            row = self.by[dim][key]
            row[0] += 1
            row[1] += amount

    def __call__(self, world, events):
        tick = world.tick - 1
        s = (tick % WPY) // WPS
        year = tick // WPY
        if tick % 520 == 519:
            self.pops.append(len(world.living()))
        gifts = [e for e in events if e["k"] == "give"]
        if not gifts:
            return
        c = world.cfg
        living = world.living()
        adults = [x for x in living if x.age(world.tick) >= 16 * WPY]
        respect = {x.id: sum(o.rel[x.id].respect for o in living if x.id in o.rel and o.id != x.id) for x in living}
        ranked = sorted(respect[x.id] for x in adults)
        for e in gifts:
            p, q = world.people.get(e["a"]), world.people.get(e.get("b"))
            if p is None or q is None:
                continue
            amt = e.get("amount", 0.0)
            self.add("tie", s, tie(world, p, q), amt)
            st = q.stage(world.tick)
            if st in ("infant", "child"):
                st += ", in giver's care" if q.caregiver == p.id else (", in another's care" if q.caregiver else ", no carer")
            self.add("stage", s, st, amt)
            weeks = max(0.0, q.edible() - amt) / q.need(c, world.tick)
            self.add("hunger", s, "under 0.5 weeks" if weeks < 0.5 else "0.5–1" if weeks < 1 else "1–2" if weeks < 2
                     else "2–4" if weeks < 4 else "4+ weeks", amt)
            if ranked and q.age(world.tick) >= 16 * WPY:
                # computed directly: the recipient may have died later in the same week
                mine = sum(o.rel[q.id].respect for o in living if q.id in o.rel and o.id != q.id)
                pc = sum(1 for v in ranked if v < mine) / len(ranked)
                self.add("status", s, "bottom quarter" if pc < 0.25 else "second quarter" if pc < 0.5
                         else "third quarter" if pc < 0.75 else "top quarter", amt)
            self.add("repay", s, "paying back" if e.get("returned") else "not paying back", amt)
            self.received[q.id] += amt
            self.pair_year[(year, p.id, q.id)] += amt
            self.giver_year[(year, p.id)] += amt

    def results(self):
        top_share = defaultdict(float)
        for (y, g, r), a in self.pair_year.items():
            top_share[(y, g)] = max(top_share[(y, g)], a)
        giver_rows = [[self.giver_year[k], top_share[k]] for k in self.giver_year]
        pairs_per_giver = defaultdict(int)
        for (y, g, r) in self.pair_year:
            pairs_per_giver[(y, g)] += 1
        return {"pops": self.pops, "by": {d: {k: v for k, v in rows.items()} for d, rows in self.by.items()},
                "received": sorted(self.received.values(), reverse=True), "giver_years": giver_rows,
                "recipients_per_giver_year": list(pairs_per_giver.values())}


def run(seed):
    setup()
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


def verify(seed=501, years=20):
    setup()
    hs = []
    for with_probe in (False, True):
        w = make_world(seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "verify.txt").write_text(f"seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n",
                                    encoding="utf-8")
    print("verify:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        if subprocess.call(me + ["verify"]) != 0:
            sys.exit("ABORT: probe changes the world")
        jobs = [s for s in SEEDS if not (OUT / f"seed_{s}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), jobs))
        print("ALL DONE", flush=True)
    elif sys.argv[1] == "verify":
        sys.exit(0 if verify() else 1)
    else:
        run(int(sys.argv[1]))
