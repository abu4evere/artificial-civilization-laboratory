"""MB1a — do ACL's bands meet? (questions.md, Stage A, frozen as `MB1a-frozen`; correction of 12 October appended.)
Read-only replays of saved worlds with an observer that measures contact between founding-band lineages. Nothing in
ACL's code changes: control worlds replay in the control code (`code_e13r`, as F1), WS1's 80-founder worlds in WS1's
code copy and settings (`code_p2`, every setting off).

  python experiments/MB1_multi_band/run_mb1a.py zero        # the observer leaves the world unchanged (two seeds per code copy)
  python experiments/MB1_multi_band/run_mb1a.py discovery   # c: 501-516 + 601-616; p, lp: 3001-3032
  python experiments/MB1_multi_band/run_mb1a.py holdout     # c: 811-818 + 1101-1124; p, lp: 3033-3064 (after the discovery reading)
  python experiments/MB1_multi_band/run_mb1a.py smoke       # throwaway: one control world, 5 years, seed 9301 (code check only)

Every replay is checked against its saved world (F1's or WS1's output): decade populations (the frozen check), and also
the final week and the world's state hash. A replay that does not reproduce is a hard stop: no new worlds are started,
and the analysis reports the set as not valid.

Operational notes written before any data (the frozen text leaves these open; each is the most literal reading):
- Lineage: read from the world as built, before its first week. Founders who start with ties to each other (the world
  gives each founding band mutual ties and nobody else) form one lineage. Everyone born later takes their mother's
  lineage when first seen; anyone without a known mother's lineage is counted, and left out of every pair.
- Adult: alive and 16 or older (`years(tick) >= 16`). Within sight: Chebyshev distance on the torus <= `perception`
  (the world's own `distance`).
- Per pair-year: a pair of adults of different lineages is *exposed* in a year (52 weeks from week 0) if both are adults
  in the same week at least once that year; it *met* if, in at least one such week, they were within sight. A world's rate
  = met pair-years / exposed pair-years over the whole run. The same-sex subset (Hill et al.'s sample) is kept beside it.
- Interacting: in a week in which both are adults, one *chose* to talk to, give to or court the other. Choices are read
  from `world.week_decisions` (the read-only record the world keeps of every decision), because a courtship that fails
  leaves no event; the counts of talks and gifts that actually happened (events) are kept beside it as a description.
- Pairing: `pair` events. Learning: `learn` events with how = "taught" or "copied" (watching), whose event names the
  source; "read" (from marks) is not learning from a person and is left out.
- Population: F1's decade populations; also the number of lineages among the living, at each decade.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"e13r": EXP / "E13R_replication" / "code_e13r", "p2": EXP / "P2_outward_search" / "code_p2"}
ARMS = {"c": ("e13r", {}),
        "p": ("p2", {"width": 40, "height": 40, "founders": 80}),
        "lp": ("p2", {"width": 80, "height": 80, "founders": 80})}
SEEDS = {"discovery": {"c": tuple(range(501, 517)) + tuple(range(601, 617)), "p": tuple(range(3001, 3033)),
                       "lp": tuple(range(3001, 3033))},
         "holdout": {"c": tuple(range(811, 819)) + tuple(range(1101, 1125)), "p": tuple(range(3033, 3065)),
                     "lp": tuple(range(3033, 3065))}}
F1_OUT = EXP / "F1_baseline_fragility" / "output"
WS1_OUT = EXP / "WS1_world_size" / "output"
OUT = HERE / "output_mb1a"
WPY, YEARS, ADULT = 52, 120, 16
SMOKE_SEED = 9301


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint(code):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


def saved(arm, seed):
    f = F1_OUT / f"seed_{seed}.json" if arm == "c" else WS1_OUT / f"{arm}_seed_{seed}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


class Lineages:
    """Reads the world after each week; draws no random numbers and writes nothing to the world."""

    def __init__(self, world):
        founders = list(world.people.values())
        self.of, k = {}, 0
        for p in founders:                      # founding bands = groups joined by the ties the world gives at start
            if p.id in self.of:
                continue
            stack = [p]
            self.of[p.id] = k
            while stack:
                a = stack.pop()
                for qid in a.rel:
                    if qid not in self.of and qid in world.people:
                        self.of[qid] = k
                        stack.append(world.people[qid])
            k += 1
        self.n_founding = k
        self.band_sizes = [sum(1 for v in self.of.values() if v == i) for i in range(k)]
        self.unknown = 0
        self.pops, self.lineages_alive = [], []
        self.year = 0
        self.exposed, self.met, self.inter = set(), set(), set()
        self.exposed_ss, self.met_ss, self.inter_ss = set(), set(), set()
        self.per_year = []                      # [year, exposed, met, interacted, exposed same-sex, met same-sex]
        self.tot = defaultdict(int)

    def lineage(self, world, p):
        if p.id not in self.of:
            m = self.of.get(p.mother) if p.mother else None
            if m is None:
                self.unknown += 1
            self.of[p.id] = m
        return self.of[p.id]

    def _close_year(self):
        self.per_year.append([self.year, len(self.exposed), len(self.met), len(self.inter),
                              len(self.exposed_ss), len(self.met_ss)])
        t = self.tot
        t["exposed"] += len(self.exposed)
        t["met"] += len(self.met)
        t["interacted"] += len(self.inter)
        t["exposed_ss"] += len(self.exposed_ss)
        t["met_ss"] += len(self.met_ss)
        t["interacted_ss"] += len(self.inter_ss)
        for s in (self.exposed, self.met, self.inter, self.exposed_ss, self.met_ss, self.inter_ss):
            s.clear()

    def __call__(self, world, events):
        from acl.util import distance
        c = world.cfg
        tick = world.tick - 1
        yr = tick // WPY
        if yr != self.year:
            self._close_year()
            self.year = yr
        living = world.living()
        for p in living:
            self.lineage(world, p)
        if tick % 520 == 519:
            self.pops.append(len(living))
            self.lineages_alive.append(len({self.of.get(p.id) for p in living} - {None}))
        adults = [(p, self.of[p.id]) for p in living if p.years(world.tick) >= ADULT and self.of[p.id] is not None]
        sexes = {p.id: p.sex for p, _ in adults}
        lin = {p.id: g for p, g in adults}
        for i, (p, g) in enumerate(adults):
            for q, h in adults[i + 1:]:
                if g == h:
                    continue
                key = (p.id, q.id) if p.id < q.id else (q.id, p.id)
                same = p.sex == q.sex
                self.exposed.add(key)
                if same:
                    self.exposed_ss.add(key)
                if key not in self.met and distance(p.loc, q.loc, c.width, c.height) <= c.perception:
                    self.met.add(key)
                    if same:
                        self.met_ss.add(key)
        for d in world.week_decisions:
            act, aim = d.chosen if d.chosen else (None, None)
            if act in ("talk", "give", "court") and aim in lin and d.agent_id in lin and lin[aim] != lin[d.agent_id]:
                key = (d.agent_id, aim) if d.agent_id < aim else (aim, d.agent_id)
                self.inter.add(key)
                self.tot["chose_" + act] += 1
                if sexes[aim] == sexes[d.agent_id]:
                    self.inter_ss.add(key)
        t = self.tot
        for e in events:
            k = e["k"]
            if k in ("talk", "give", "pair"):
                a, b = self.of.get(e.get("a")), self.of.get(e.get("b"))
                cross = a is not None and b is not None and a != b
                t[k] += 1
                t[k + "_cross"] += cross
            elif k == "learn" and e.get("how") in ("taught", "copied"):
                a, b = self.of.get(e.get("a")), self.of.get(e.get("b"))
                t["learn_" + e["how"]] += 1
                if a is not None and b is not None and a != b:
                    t["learn_cross"] += 1
                    t["learn_cross_" + e["how"]] += 1

    def results(self):
        self._close_year()
        return {"founding_bands": self.band_sizes, "unknown_lineage": self.unknown, "pops": self.pops,
                "lineages_alive": self.lineages_alive, "per_year": self.per_year, "tot": dict(self.tot)}


def hash_run(arm, seed, years, observe):
    code, kw = ARMS[arm]
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers.append(Lineages(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]
    call = lambda arm, seed, obs: subprocess.run(me + ["hashrun", arm, str(seed), "1" if obs else "0"],  # noqa: E731
                                                 capture_output=True, text=True).stdout.strip().splitlines()[-1]
    lines, ok = [], True
    for arm, seed in (("c", 501), ("c", 601), ("p", 3001), ("p", 3002)):
        t = call(arm, seed, False) == call(arm, seed, True)
        ok &= t
        lines.append(f"{arm} ({ARMS[arm][0]}), seed {seed}, 20 years: world unchanged by the observer: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    code, kw = ARMS[arm]
    setup(code)
    f0 = fingerprint(code)
    w = make_world(seed, kw)
    obs = Lineages(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code": code, "code_hash": f0, "code_hash_after": fingerprint(code),
           "final_tick": w.tick, "world_hash": world_hash(w), **obs.results()}
    ref = saved(arm, seed) if out is None else None
    if ref is not None:
        res["saved_code_hash"] = ref["code_hash"]
        res["reproduces"] = ref["pops"] == res["pops"]
        res["reproduces_hash"] = ref["world_hash"] == res["world_hash"] and ref["final_tick"] == res["final_tick"]
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    flag = "" if out != OUT else ("" if res.get("reproduces") else "  HARD STOP: does not reproduce its saved world")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {res['pops']}{flag}", flush=True)


def batch(which):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the observer has not been shown to leave the world unchanged (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for a, seeds in SEEDS[which].items() for s in seeds if not (OUT / f"{a}_seed_{s}.json").exists()]
    todo.sort(key=lambda t: t[0] != "lp")       # the slowest worlds first, so the batch ends evenly
    stop = []

    def go(t):
        if stop:
            return
        subprocess.call(me + ["one", t[0], str(t[1])])
        f = OUT / f"{t[0]}_seed_{t[1]}.json"
        if not f.exists() or not json.loads(f.read_text(encoding="utf-8")).get("reproduces"):
            stop.append(t)

    with ThreadPoolExecutor(4) as pool:
        list(pool.map(go, todo))
    print(f"HARD STOP: {stop[0]} did not reproduce its saved world" if stop else "ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hash_run(sys.argv[2], int(sys.argv[3]), 20, sys.argv[4] == "1"))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "smoke":
        run_one("c", SMOKE_SEED, years=5, out=HERE / "output_mb1a_smoke")
    elif cmd == "discovery":
        batch("discovery")
    elif cmd == "holdout":
        if not (HERE / "findings_mb1a_discovery.md").exists():
            sys.exit("ABORT: the discovery reading has not been written down")
        batch("holdout")
