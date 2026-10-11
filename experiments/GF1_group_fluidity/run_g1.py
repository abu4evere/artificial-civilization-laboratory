"""GF1 — how fluid are ACL's groups? (questions.md, frozen as `G1-questions`). Read-only replays of control worlds
(`code_e13r`, F1's setup) with a weekly group observer.

  python experiments/GF1_group_fluidity/run_g1.py verify      # observer read-only (two seeds, 20 years)
  python experiments/GF1_group_fluidity/run_g1.py discovery   # F1's 64 seeds, checked against F1's saved populations
  python experiments/GF1_group_fluidity/run_g1.py holdout     # 64 new seeds 2601-2664 (only after findings_discovery.md)
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "F1_baseline_fragility"))
import run_f1 as F  # noqa: E402

OUT = HERE / "output"
WPY, YEARS, BLOCK = 52, 120, 4
LAGS = (1, 3, 6, 13, 26)                      # blocks: about 4, 12, 24, 52, 104 weeks
DISCOVERY = F.DISCOVERY + F.HOLDOUT           # F1's 64 seeds
HOLDOUT = tuple(range(2601, 2665))
F1OUT = EXP / "F1_baseline_fragility" / "output"


def chain(people, radius, c, distance):
    """F1's group definition: living people chained by distance <= radius. Returns a label per person."""
    parent = list(range(len(people)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            if distance(people[i].loc, people[j].loc, c.width, c.height) <= radius:
                parent[find(i)] = find(j)
    return [find(i) for i in range(len(people))]


class Groups:
    """Reads the world after each week; draws no random numbers and writes nothing to the world."""

    def __init__(self):
        self.week = []        # this block's weekly snapshots: {adult id: (group r2, group r4, seeker)}
        self.blocks = []      # per block: (present adults, seekers, co-resident pairs r2, co-resident pairs r4, groups r2)

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick
        living = world.living()
        g2 = chain(living, c.camp_radius, c, distance)
        g4 = chain(living, c.perception, c, distance)
        snap = {}
        for p, a, b in zip(living, g2, g4):
            if p.stage(tick) in ("adult", "elder"):
                snap[p.id] = (a, b, p.stage(tick) == "adult" and p.partner is None and p.years(tick) < 45)
        self.week.append(snap)
        if len(self.week) == BLOCK:
            self._close_block()

    def _close_block(self):
        seen = Counter(pid for s in self.week for pid in s)
        present = sorted(pid for pid, n in seen.items() if n >= 3)
        seekers = {pid for pid in present if sum(1 for s in self.week if pid in s and s[pid][2]) >= 3}
        co2, co4 = set(), set()
        for a, b in combinations(present, 2):
            n2 = n4 = 0
            for s in self.week:
                if a in s and b in s:
                    n2 += s[a][0] == s[b][0]
                    n4 += s[a][1] == s[b][1]
            if n2 >= 3:
                co2.add((a, b))
            if n4 >= 3:
                co4.add((a, b))
        last = self.week[-1]
        ngroups = len({v[0] for v in last.values()})
        self.blocks.append((set(present), seekers, co2, co4, ngroups))
        self.week = []

    def results(self):
        n = Counter()
        for i, (pres, seek, co2, co4, ng) in enumerate(self.blocks):
            npairs = len(pres) * (len(pres) - 1) // 2
            if npairs:
                n["blocks_with_pairs"] += 1
                n["adult_blocks"] += len(pres)
                single2 = len(co2) == npairs
                n["single_group_blocks_r2"] += single2
                n["single_group_blocks_r4"] += len(co4) == npairs
            for lag in LAGS:
                if i + lag >= len(self.blocks):
                    continue
                pres2, _, co2b, co4b, _ = self.blocks[i + lag]
                for tag, co, cob in (("r2", co2, co2b), ("r4", co4, co4b)):
                    for pair in co:
                        if pair[0] in pres2 and pair[1] in pres2:
                            kind = "seeker" if (pair[0] in seek or pair[1] in seek) else "other"
                            stay = pair in cob
                            n[f"den_{tag}_{lag}"] += 1
                            n[f"num_{tag}_{lag}"] += stay
                            n[f"den_{tag}_{lag}_{kind}"] += 1
                            n[f"num_{tag}_{lag}_{kind}"] += stay
                            if npairs and len(co) != npairs:
                                n[f"den_{tag}_{lag}_multi"] += 1
                                n[f"num_{tag}_{lag}_multi"] += stay
        return dict(n)


def run_one(seed, years=YEARS, out=None):
    F.setup()
    from run_f1 import Probe
    f0 = F.fingerprint()
    w = F.make_world(seed)
    probe, grp = Probe(), Groups()
    w.observers += [probe, grp]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "code_hash": f0, "code_hash_after": F.fingerprint(), "final_tick": w.tick,
           "world_hash": F.world_hash(w), "pops": probe.pops, "groups": grp.results()}
    f1 = F1OUT / f"seed_{seed}.json"
    if f1.exists():
        res["reproduces"] = json.loads(f1.read_text(encoding="utf-8"))["pops"] == probe.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: alive {len(w.living())}, pops {probe.pops}, reproduces F1: {res.get('reproduces')}", flush=True)


def verify(seeds=(601, 2601), years=20):
    F.setup()
    lines, ok = [], True
    for seed in seeds:
        hs = []
        for with_obs in (False, True):
            w = F.make_world(seed)
            if with_obs:
                w.observers.append(Groups())
            for _ in range(years * WPY):
                w.step()
            hs.append(w.state_hash())
        t = hs[0] == hs[1]
        ok &= t
        lines.append(f"group observer, seed {seed}, {years} years: {'READ-ONLY' if t else 'CHANGES THE WORLD'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    return ok


def batch(seeds):
    v = OUT / "checks.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the observer has not been shown read-only")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in seeds if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["one", str(s)]), todo))
    R = [json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in seeds]
    bad = [r["seed"] for r in R if r.get("reproduces") is False or r["code_hash"] != r["code_hash_after"]]
    print("ALL DONE, CODE UNCHANGED" + (", ALL REPRODUCE F1" if all("reproduces" in r for r in R) else "")
          if not bad else f"HARD STOP: {bad}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        run_one(int(sys.argv[2]))
    elif cmd == "verify":
        sys.exit(0 if verify() else 1)
    elif cmd == "discovery":
        batch(DISCOVERY)
    elif cmd == "holdout":
        if not (HERE / "findings_discovery.md").exists():
            sys.exit("ABORT: the discovery reading has not been written down")
        batch(HOLDOUT)
