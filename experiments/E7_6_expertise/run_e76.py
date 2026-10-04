"""E7.6: expertise retention audit. Read-only replays of the E7 worlds (both arms) with a probe that only reads.

Usage:
  python experiments/E7_6_expertise/run_e76.py <arm> <seed>          # arm: baseline (E6 code) or e7
  python experiments/E7_6_expertise/run_e76.py verify <arm> <seed>   # probe is read-only: same state hash
  python experiments/E7_6_expertise/run_e76.py all                   # verify both codes, then all 16 worlds
Writes output/<arm>/seed_<n>.json. Each replay is checked against the saved E7 run (population every 10 years).
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
CODE = {"e7": E7 / "code_e7", "baseline": HERE.parent / "E6_novelty" / "code_e6"}
SEEDS = list(range(301, 309))
WPY = 52
SAMPLE = 25 * WPY
DECADE = 10 * WPY


def setup(arm: str) -> str:
    sys.path.insert(0, str(CODE[arm]))
    sys.path.insert(1, str(E7))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE[arm] / "acl").resolve()
    from run_e7 import code_hash
    return code_hash(CODE[arm] / "acl")


def watertight(props: dict) -> bool:
    return props.get("tight", 0) >= 50 and props.get("contain", 0) >= 40


class Probe:
    def __init__(self):
        self.decades = {}     # decade -> counts
        self.samples = []     # every 25 years
        self.pops = []        # every 10 years, to check the replay

    def _dec(self, tick):
        return self.decades.setdefault(tick // DECADE, Counter())

    def __call__(self, world, events):
        tick = world.tick - 1
        d = self._dec(tick)
        for e in events:
            k = e["k"]
            if k == "play":
                d["play_made" if e.get("thing") else "play_nothing"] += 1
            elif k == "make":
                d["deliberate"] += 1
            else:
                continue
            if e.get("thing") and watertight(e):
                d["watertight_made"] += 1
        living = world.living()
        d["person_weeks"] += len(living)
        if tick % DECADE == DECADE - 1:
            self.pops.append(len(living))
        if tick % SAMPLE == SAMPLE - 1:
            self._sample(world, tick, living)

    def _sample(self, world, tick, living):
        from acl import matter
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        skills = sorted((p.skills["crafting"] for p in living), reverse=True)
        held = Counter(sig for p in living for sig in p.recipes)
        carriers = [p for p in living if any(matter.can_hold(it, "water") > 0 for it in p.items)]
        self.samples.append({
            "year": tick // WPY + 1,
            "population": len(living),
            "adults": len(adults),
            "skill_best": round(skills[0], 3) if skills else None,
            "skill_top10": round(sum(skills[:10]) / len(skills[:10]), 3) if skills else None,
            "skill_mean": round(sum(skills) / len(skills), 3) if skills else None,
            "skill_mean_adults": round(sum(p.skills["crafting"] for p in adults) / len(adults), 3) if adults else None,
            "recipes_unique": len(held),
            "recipes_total": sum(held.values()),
            "recipes_mean_holders": round(sum(held.values()) / len(held), 2) if held else 0,
            "recipe_most_held": held.most_common(1)[0] if held else None,
            "watertight_carried": sum(1 for p in living for it in p.items if matter.can_hold(it, "water") > 0),
            "people_with_watertight": len(carriers),
        })


def run(arm: str, seed: int, years: int = 1000):
    fingerprint = setup(arm)
    from acl.config import Config
    from acl.world import World
    from run_e7 import code_hash
    saved = json.loads((E7 / "output" / arm / f"seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    t0 = time.time()
    for _ in range(saved["years_run"] * WPY):
        w.step()
        if not w.living():
            break
    saved_pops = [s["population"] for s in saved["samples"]]
    n = min(len(saved_pops), len(probe.pops))
    out = {
        "arm": arm, "seed": seed, "years_run": w.year, "code_hash": fingerprint,
        "code_hash_after": code_hash(CODE[arm] / "acl"),
        "replay_matches_saved": probe.pops[:n] == saved_pops[:n] and n > 0,
        "LFA": saved["LFA"],
        "samples": probe.samples,
        "decades": {str(k): dict(v) for k, v in sorted(probe.decades.items())},
        "pops_by_decade": probe.pops,
        "seconds": round(time.time() - t0),
    }
    dest = HERE / "output" / arm
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"{arm} seed {seed}: {w.year} years, replay matches: {out['replay_matches_saved']}, {out['seconds']}s",
          flush=True)


def verify(arm: str, seed: int, years: int = 20) -> bool:
    setup(arm)
    from acl.config import Config
    from acl.world import World
    hashes = []
    for with_probe in (False, True):
        w = World(Config(seed=seed))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hashes.append(w.state_hash())
    ok = hashes[0] == hashes[1]
    line = f"{arm} seed {seed}, {years} years: {hashes[0][:16]} / {hashes[1][:16]} -> {'READ-ONLY' if ok else 'CHANGES THE WORLD'}"
    print(line, flush=True)
    (HERE / "output").mkdir(exist_ok=True)
    with open(HERE / "output" / "verify.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return ok


def run_all():
    me = [sys.executable, str(Path(__file__).resolve())]
    for arm in ("e7", "baseline"):
        if subprocess.call(me + ["verify", arm, "304"]) != 0:
            print(f"ABORT: probe changes the world under {arm}", flush=True)
            return
    for arm in ("e7", "baseline"):
        for seed in SEEDS:
            if (HERE / "output" / arm / f"seed_{seed}.json").exists():
                continue
            if subprocess.call(me + [arm, str(seed)]) != 0:
                print(f"{arm} seed {seed}: CRASHED", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "all":
        run_all()
    elif sys.argv[1] == "verify":
        sys.exit(0 if verify(sys.argv[2], int(sys.argv[3])) else 1)
    else:
        run(sys.argv[1], int(sys.argv[2]))
