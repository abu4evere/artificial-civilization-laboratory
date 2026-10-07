"""HF2 — the household food balance (questions.md, frozen as `HF2-questions`). Read-only replays, first 40 years, arms H
(HB1, home_base = 1) and C (the same code, settings off).

  python experiments/HF2_household_food/run_hf2.py verify      # observer read-only (H and C, two seeds, 20 years)
  python experiments/HF2_household_food/run_hf2.py discovery   # seeds 501-516, checked against HB1's and F1's runs
  python experiments/HF2_household_food/run_hf2.py holdout     # new seeds 1401-1416 (after the discovery write-up)

Approximation (written before data): a hunter's meat is counted as the hunt's meat divided equally by the party, as the
code splits it; the code also caps each share by what the hunter can carry, which the observer cannot see.
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "HB1_home_base"))
import run_hb1 as HB  # noqa: E402

OUT = HERE / "output"
WPY, YEARS = 52, 40
DISCOVERY = tuple(range(501, 517))
HOLDOUT = tuple(range(1401, 1417))
ARMS = {"h": {"home_base": 1}, "c": {}}
SAVED = {"h": EXP / "HB1_home_base" / "output", "c": EXP / "F1_baseline_fragility" / "output"}
GROUPS = ("carer", "partnered", "single")


class Probe:
    """Reads the world after each week; draws no random numbers; writes nothing to the world."""

    def __init__(self):
        self.pops = []
        self.n = Counter()
        self.group = {}                      # adult id -> group last week (for deaths)

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick
        t = tick - 1
        living = world.living()
        if t % 520 == 519:
            self.pops.append(len(living))
        n = self.n
        n["person_weeks"] += len(living)
        adult = lambda p: p.age(tick) >= 16 * WPY
        food_in = Counter()
        # food in and out, from the week's events
        for e in events:
            k = e["k"]
            if k == "forage" and "a" in e:
                food_in[(e["a"], "forage")] += e.get("got", 0.0)
            elif k == "hunt":
                n["hunts"] += 1
                party = e.get("party") or []
                if party:
                    share = e.get("meat", 0.0) / len(party)
                    for h in party:
                        food_in[(h, "hunt")] += share
                        n["hunter_hunts"] += 1
                        n["hunter_meat"] += share
                        hp = world.people.get(h)
                        if hp is not None and hp.partner and world.people[hp.partner].alive:
                            home = world.couple_home(hp, world.people[hp.partner])
                            if home is not None and "at" in e:
                                n["hunt_dist_sum"] += distance(tuple(e["at"]), home, c.width, c.height)
                                n["hunt_dist_n"] += 1
            elif k == "take" and "a" in e:
                food_in[(e["a"], "take")] += e.get("food", 0.0)
            elif k == "give" and "a" in e and "b" in e:
                amt = e.get("amount", 0.0)
                food_in[(e["b"], "gift")] += amt
                giver, getter = world.people[e["a"]], world.people[e["b"]]
                to = "partner" if giver.partner == getter.id else "kin" if world.kinship(giver, getter) > 0 else "other"
                if adult(giver):
                    n["given"] += amt
                    n[f"given_{to}"] += amt
            elif k == "steal" and "a" in e:
                amt = e.get("amount", 0.0)
                food_in[(e["a"], "steal")] += amt
                if "b" in e:
                    n["stolen_from"] += amt
            elif k == "death" and e.get("cause") == "starvation" and (e.get("age") or 0) >= 16:
                g = self.group.get(e["a"], "single")
                n[f"starve_death_{g}"] += 1
        # adults: groups, starving, food in, mouths
        group = {}
        for p in living:
            if not adult(p):
                continue
            deps = world.dependents(p.id)
            partnered = bool(p.partner) and world.people[p.partner].alive
            g = "carer" if deps else "partnered" if partnered else "single"
            group[p.id] = g
            n["adult_weeks"] += 1
            n[f"aw_{g}"] += 1
            n["starving"] += bool(p.starving)
            n[f"starving_{g}"] += bool(p.starving)
            for src in ("forage", "hunt", "take", "gift", "steal"):
                v = food_in.get((p.id, src), 0.0)
                n[f"in_{src}"] += v
                n["in_total"] += v
            if p.id in {h for e in events if e["k"] == "hunt" for h in (e.get("party") or [])}:
                n["adult_weeks_hunting"] += 1
            if deps:
                n["carer_weeks"] += 1
                n["dependants"] += len(deps)
                dep_need = sum(d.need(c, tick) for d in deps)
                got = sum(food_in.get((p.id, s), 0.0) for s in ("forage", "hunt", "take", "gift", "steal"))
                n["dep_need"] += dep_need
                n["carer_in"] += got
                deps_fed = not any(d.starving for d in deps)
                n["carer_starving_deps_fed"] += bool(p.starving) and deps_fed
        self.group = group

    def results(self):
        return {"pops": self.pops, "n": dict(self.n)}


def run_one(arm, seed, years=YEARS, out=None):
    HB.setup("hb1")
    f0 = HB.fingerprint()
    w = HB.make_world(seed, **ARMS[arm])
    probe = Probe()
    w.observers.append(probe)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": HB.fingerprint(),
           **probe.results()}
    saved = SAVED[arm] / (f"h_seed_{seed}.json" if arm == "h" else f"seed_{seed}.json")
    if saved.exists():
        res["reproduces"] = json.loads(saved.read_text(encoding="utf-8"))["pops"][: years // 10] == probe.pops
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: pops {probe.pops}, reproduces saved: {res.get('reproduces')}", flush=True)


def verify(seeds=(501, 1401), years=20):
    HB.setup("hb1")
    lines, ok = [], True
    for arm, kw in ARMS.items():
        for seed in seeds:
            hs = []
            for with_probe in (False, True):
                w = HB.make_world(seed, **kw)
                if with_probe:
                    w.observers.append(Probe())
                for _ in range(years * WPY):
                    w.step()
                hs.append(w.state_hash())
            t = hs[0] == hs[1]
            ok &= t
            lines.append(f"observer, arm {arm}, seed {seed}, {years} years: {'READ-ONLY' if t else 'CHANGES THE WORLD'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    return ok


def batch(seeds):
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for a in ARMS for s in seeds if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), todo))
    R = [json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in ARMS for s in seeds]
    bad = [(r["arm"], r["seed"]) for r in R if r.get("reproduces") is False or r["code_hash"] != r["code_hash_after"]]
    print("ALL REPRODUCE, CODE UNCHANGED" if not bad else f"HARD STOP: {bad}", flush=True)
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "verify":
        sys.exit(0 if verify() else 1)
    elif cmd in ("discovery", "holdout"):
        sys.exit(0 if batch(DISCOVERY if cmd == "discovery" else HOLDOUT) else 1)
