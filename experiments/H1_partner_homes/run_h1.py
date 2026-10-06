"""H1 — partners' homes (questions.md, frozen as `H1-questions`). Read-only replays of control worlds, first 40 years.
Reuses C1's setup, world, fingerprint and checks; only the observer differs.

  python experiments/H1_partner_homes/run_h1.py verify | discovery | holdout
  python experiments/H1_partner_homes/analyse_h1.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "C1_couples_apart"))
import run_c1 as C  # noqa: E402

OUT = HERE / "output"
DISCOVERY, HOLDOUT = C.DISCOVERY, C.HOLDOUT


def band(d):
    return "0-2" if d <= 2 else "3" if d == 3 else "4-6" if d <= 6 else "7+"


class Probe:
    """Reads the world after each week; draws no random numbers; writes nothing to the world."""

    def __init__(self):
        self.pops = []
        self.n = Counter()
        self.last_home = {}

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick
        t = tick - 1
        living = world.living()
        if t % 520 == 519:
            self.pops.append(len(living))
        n = self.n
        dist = lambda a, b: distance(a, b, c.width, c.height)
        homes = {}
        for p in living:
            h = p.home()
            homes[p.id] = h
            if p.age(tick) >= 16 * 52:
                n["adult_weeks"] += 1
                if h is None:
                    n["adult_homeless"] += 1
                elif p.id in self.last_home and self.last_home[p.id] not in (None, h):
                    n["adult_home_changed"] += 1
        self.last_home = homes
        for w in living:
            if w.sex != "F" or not (c.fertile_from <= w.years(tick) < c.fertile_until) or not w.partner:
                continue
            m = world.people[w.partner]
            if not m.alive:
                continue
            n["couple_weeks"] += 1
            hw, hm = homes.get(w.id), homes.get(m.id)
            apart = dist(w.loc, m.loc) > c.camp_radius
            n["apart"] += apart
            if hw is None or hm is None:
                n["either_homeless"] += 1
                continue
            n["both_home"] += 1
            n[f"homes|{band(dist(hw, hm))}"] += 1
            for p, h in ((w, hw), (m, hm)):
                d = dist(p.loc, h)
                n[f"pos|{'at' if d == 0 else 'near' if d <= 2 else 'away'}"] += 1
            if apart:
                n["apart_both_home"] += 1
                aw, am = dist(w.loc, hw) <= 2, dist(m.loc, hm) <= 2
                n["apart_both_near_own_home"] += aw and am
                n["apart_one_away"] += (not aw) or (not am)

    def results(self):
        return {"pops": self.pops, "n": dict(self.n)}


def run_one(seed, years=C.YEARS, out=None):
    C.setup()
    f0 = C.fingerprint()
    w = C.make_world(seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(years * 52):
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "years": years, "code_hash": f0, "code_hash_after": C.fingerprint(), **probe.results()}
    saved = json.loads((C.F1OUT / f"seed_{seed}.json").read_text(encoding="utf-8"))["pops"][: years // 10]
    res["reproduces"] = saved == probe.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: pops {probe.pops}, reproduces F1: {res['reproduces']}", flush=True)


def verify(seeds=(501, 1101), years=20):
    C.setup()
    lines, ok = [], True
    for seed in seeds:
        hs = []
        for with_probe in (False, True):
            w = C.make_world(seed)
            if with_probe:
                w.observers.append(Probe())
            for _ in range(years * 52):
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
    bad = [r["seed"] for r in R if not r["reproduces"] or r["code_hash"] != r["code_hash_after"]]
    print("ALL REPRODUCE, CODE UNCHANGED" if not bad else f"HARD STOP: {bad}", flush=True)
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        run_one(int(sys.argv[2]))
    elif cmd == "verify":
        sys.exit(0 if verify() else 1)
    elif cmd in ("discovery", "holdout"):
        sys.exit(0 if batch(DISCOVERY if cmd == "discovery" else HOLDOUT) else 1)
