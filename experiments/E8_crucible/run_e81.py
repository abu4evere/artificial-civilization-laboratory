"""E8.1 value autopsy (E8_1_value_autopsy.md). Read-only replays of the E7 code, seeds 301–304, 120 years.

  python experiments/E8_crucible/run_e81.py all      # verify the probe, then 4 seeds in parallel; then analyse
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
E7 = HERE.parent / "E7_passive"
sys.path.insert(0, str(E7 / "code_e7"))
sys.path.insert(1, str(E7))
from acl import mind  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY = 52
OUT = HERE / "output_e81"


def gen_bucket(g):
    return str(g) if g < 3 else "3+"


class Probe:
    def __init__(self):
        self.rows = defaultdict(lambda: {"held": [], "best_known": [], "weeks": 0, "can_make": 0,
                                         "make_weighed": 0, "make_chosen": 0, "chosen_instead": Counter(),
                                         "ratio": []})
        self.pops = []

    def __call__(self, world, events):
        tick = world.tick - 1
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        if tick % 4:
            return
        c = world.cfg
        for p in living:
            if p.age(world.tick) < 16 * WPY:
                continue
            for key in (gen_bucket(p.generation), f"decade {tick // 520}"):
                r = self.rows[key]
                r["weeks"] += 1
                r["held"].extend(p.itemval.get(it["sig"], 0.0) for it in p.items)
                r["best_known"].append(max((p.itemval.get(s, 0.0) for s in p.recipes), default=0.0))
                makeable = [s for s, rec in p.recipes.items() if mind.can_make(p, rec)]
                if not makeable:
                    continue
                r["can_make"] += 1
                considered = p.considered or []
                if any(x[0] == "make" for x in considered):
                    r["make_weighed"] += 1
                chosen = next((x for x in considered if x[3]), None)
                if chosen is None:
                    continue
                if chosen[0] == "make":
                    r["make_chosen"] += 1
                else:
                    r["chosen_instead"][chosen[0]] += 1
                hunger = min(1.0, max(0.0, 1.0 - p.edible() / max(1e-9, p.need(c, world.tick) * 4)))
                best_v = max(p.itemval.get(s, 0.0) for s in makeable)
                make_u = c.worth_weight * best_v * (0.6 + 0.4 * p.genes["diligence"]) * (1 - 0.5 * hunger)
                r["ratio"].append(chosen[2] / make_u if make_u > 0 else float("inf"))


def summarise(rows):
    out = {}
    for k, r in rows.items():
        held = r["held"]
        ratios = [x for x in r["ratio"]]
        finite = [x for x in ratios if x != float("inf")]
        out[k] = {
            "adult_weeks_sampled": r["weeks"],
            "held_things": len(held),
            "held_worth_mean": round(statistics.mean(held), 4) if held else None,
            "held_worth_share_le0": round(sum(1 for v in held if v <= 0) / len(held), 3) if held else None,
            "best_known_worth_mean": round(statistics.mean(r["best_known"]), 4) if r["best_known"] else None,
            "weeks_could_make": r["can_make"],
            "make_weighed": r["make_weighed"],
            "make_chosen": r["make_chosen"],
            "chosen_instead": dict(r["chosen_instead"].most_common(10)),
            "ratio_median": (round(statistics.median(finite), 2) if finite else None),
            "ratio_infinite_share": round(sum(1 for x in ratios if x == float("inf")) / len(ratios), 3) if ratios else None,
            "ratio_values": len(ratios),
        }
    return out


def run(seed):
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    sp = [s["population"] for s in saved["samples"]][: len(probe.pops)]
    res = {"seed": seed, "replay_matches_saved": probe.pops == sp, "rows": summarise(probe.rows)}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches_saved']}", flush=True)


def verify(seed=304, years=20):
    hs = []
    for with_probe in (False, True):
        w = World(Config(seed=seed))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(exist_ok=True)
    (OUT / "verify.txt").write_text(f"seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
    print("verify:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(0 if verify() else 1)
    elif sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        if subprocess.call(me + ["verify"]) != 0:
            sys.exit("ABORT")
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), SEEDS))
    else:
        run(int(sys.argv[1]))
