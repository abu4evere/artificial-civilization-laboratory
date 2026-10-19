"""RT1b — residence time with the walk to water counted (questions_rt1b.md, frozen as `RT1b-frozen`). `code_rt1b` = `code_rt1`
+ `water_trip`. The code, zero checks and mechanism pilot were prepared before freezing (GPT's direction under the
creator's delegation); the creator signed the plan off on 18 October 2026 ("approve RT1b as is, freeze it").

  python experiments/RT1_residence_time/run_rt1b.py zero     # hard stops: water_trip 0 = code_rt1; without a base it does nothing; it acts; read-only; reload
  python experiments/RT1_residence_time/run_rt1b.py pilot    # throwaway seeds 9801-9804, 15 years, r4 and r4w: the water mechanism only
  python experiments/RT1_residence_time/run_rt1b.py run      # c, r4, r4w on seeds 5701-5956, 120 years (skips saved worlds)
  python experiments/RT1_residence_time/run_rt1b.py smoke    # throwaway: seeds 9811-9812, 8 years, every arm (code check only)
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_rt1 as R  # noqa: E402

R.CODES["rt1b"] = HERE / "code_rt1b"
OUT = HERE / "output_rt1b"
WPY, YEARS = 52, 120
SEEDS = tuple(range(5701, 5957))
PILOT_SEEDS = (9801, 9802, 9803, 9804)
SMOKE_SEEDS = (9811, 9812)
ARMS = {"c": {}, "r4": {"residence_weeks": 4}, "r4w": {"residence_weeks": 4, "water_trip": 1}}


def fingerprint():
    from run_e7 import code_hash
    return code_hash(R.CODES["rt1b"] / "acl")


class Water:
    """Read-only, after each week: of adults who ended the week's actions within sight of fresh water they could reach
    (and were then sent back to base), how many still went short of water? And of the thirsty, how many had chosen a
    destination by water (thirst_check.py's measure)?"""

    def __init__(self):
        self.c = Counter()

    def __call__(self, world, events):
        from acl import weather
        c = world.cfg
        chosen = {d.agent_id: d.chosen for d in world.week_decisions}
        went = getattr(world, "trip_end", {})
        for p in world.living():
            if p.age(world.tick) < 16 * WPY:
                continue
            g = went.get(p.id)
            if g is not None and weather.reachable_fresh(world, p, g, c.perception) is not None:
                self.c["reached_water_then_sent_back"] += 1
                self.c["of_those_still_short"] += p.thirst > 0.05
            if p.thirst <= 0.05:
                continue
            self.c["thirsty"] += 1
            _, target = chosen.get(p.id, (None, None))
            if isinstance(target, tuple) and len(target) == 2 and all(isinstance(v, int) for v in target):
                if weather.reachable_fresh(world, p, target, c.perception) is not None:
                    self.c["thirsty_but_went_to_water"] += 1


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for kw in ({}, {"residence_weeks": 4}):
        for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
            t = call("rt1b", seed, years, json.dumps(kw), 0) == call("rt1", seed, years, json.dumps(kw), 0)
            ok &= t
            lines.append(f"{kw or 'C'}, seed {seed}, {years} years: water_trip 0 = code_rt1: {'yes' if t else 'NO'}")
    t = call("rt1b", 501, 20, json.dumps({"water_trip": 1}), 0) == call("rt1b", 501, 20, json.dumps({}), 0)
    ok &= t
    lines.append(f"seed 501, 20 years: water_trip 1 without a base = C exactly (it does nothing): {'yes' if t else 'NO'}")
    t = call("rt1b", 501, 20, json.dumps(ARMS["r4w"]), 0) != call("rt1b", 501, 20, json.dumps(ARMS["r4"]), 0)
    ok &= t
    lines.append(f"seed 501, 20 years: r4w differs from r4 (it acts): {'yes' if t else 'NO'}")
    t = call("rt1b", 501, 20, json.dumps(ARMS["r4w"]), 1) == call("rt1b", 501, 20, json.dumps(ARMS["r4w"]), 0)
    ok &= t
    lines.append(f"r4w, seed 501, 20 years: identical with and without the observers: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"r4w, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    R.setup("rt1b")
    lines.append(f"code_rt1b fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def hashrun(code, seed, years, kw, observe):
    R.setup(code)
    w = R.make_world(seed, kw)
    if observe:
        w.observers += list(R.observers(w)) + [Water()]
    for _ in range(years * WPY):
        w.step()
    return R.world_hash(w)


def reload_check(seed):
    R.setup("rt1b")
    from acl.world import World
    a = R.make_world(seed, ARMS["r4w"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return R.world_hash(a) == R.world_hash(b) and bool(a.bases)


def pilot_one(arm):
    """Throwaway seeds; prints only the water mechanism, no survival, population or deaths."""
    R.setup("rt1b")
    tot = Counter()
    for seed in PILOT_SEEDS:
        w = R.make_world(seed, ARMS[arm])
        ch = Water()
        w.observers.append(ch)
        for _ in range(15 * WPY):
            w.step()
            if not w.living():
                break
        tot += ch.c
    still = tot["of_those_still_short"] / max(1, tot["reached_water_then_sent_back"])
    went = tot["thirsty_but_went_to_water"] / max(1, tot["thirsty"])
    print(f"{arm}: adult-weeks that ended the week's actions by reachable water and were sent back: "
          f"{tot['reached_water_then_sent_back']}; of those, still short of water: {still:.3f} | "
          f"of the thirsty, had chosen a destination by water: {went:.3f}", flush=True)


def run_one(arm, seed, years=YEARS, out=None):
    R.setup("rt1b")
    f0 = fingerprint()
    w = R.make_world(seed, ARMS[arm])
    probe, lin, mv = R.observers(w)
    wa = Water()
    w.observers += [probe, lin, mv, wa]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": R.world_hash(w), **probe.results(), "mb1a": lin.results(), **mv.results(), "water": dict(wa.c)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
    q = (HERE / "questions_rt1b.md").read_text(encoding="utf-8")
    if "SIGNED OFF" not in q.splitlines()[0]:
        sys.exit("ABORT: RT1b is a draft; the creator has not signed it off")
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "pilot":
        for a in ("r4", "r4w"):
            pilot_one(a)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "run":
        batch()
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, years=8, out=HERE / "output_rt1b_smoke")
