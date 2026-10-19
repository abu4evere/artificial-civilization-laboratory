"""FX2 — food that must be opened (questions.md, frozen as `FX2-frozen`). `code_fx2` = `code_v2` + `embedded_share`,
`embedded_bare`, `embedded_tool`. The code and zero checks were prepared before freezing (GPT's direction under the
creator's delegation); the creator signed the plan off on 18 October 2026 ("approve FX2 as is, freeze it").

  python experiments/FX2_embedded_food/run_fx2.py zero    # hard stops: share 0 = code_v2; E and E0 act; read-only; reload
  python experiments/FX2_embedded_food/run_fx2.py mech    # throwaway seeds 9901-9904, 10 years, E and E0: the mechanism only
  python experiments/FX2_embedded_food/run_fx2.py run     # c, e, e0 on seeds 6001-6256, 120 years (skips saved worlds)
  python experiments/FX2_embedded_food/run_fx2.py smoke   # throwaway: seeds 9911-9912, 8 years, every arm (code check only)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"fx2": HERE / "code_fx2", "v2": EXP / "NV2_nature_v2" / "code_v2"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(6001, 6257))
SMOKE_SEEDS = (9911, 9912)
MECH_SEEDS = (9901, 9902, 9903, 9904)
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
ARMS = {"c": {}, "e": {"embedded_share": 0.5, "embedded_bare": 0.2, "embedded_tool": 1},
        "e0": {"embedded_share": 0.5, "embedded_bare": 0.2, "embedded_tool": 0}}


def setup(code="fx2"):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "MB1_multi_band"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **V2, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")              # the settings list itself is left out, as every zero check has done
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["fx2"] / "acl")


class Tools:
    """Read-only, after each week: adult forage-weeks, and how many had a thing of hardness >= 40 in hand (the primary
    measure); plant food from open and embedded stands; bare-handed opening against what was wanted."""

    def __init__(self):
        self.c = Counter()

    def __call__(self, world, events):
        adult = {p.id for p in world.living() if p.age(world.tick) >= 16 * WPY}
        for e in events:
            if e["k"] == "forage" and e.get("a") in adult:
                p = world.people[e["a"]]
                self.c["adult_forage_weeks"] += 1
                self.c["with_hard_40"] += any(it.get("hard", 0) >= 40 for it in p.items)
                self.c["food_got"] += e.get("got", 0)
            elif e["k"] == "open_food" and e.get("a") in adult:
                self.c["opened"] += e["got"]
                if e["hard"] > 0:                       # FX2 sign-off: a hard thing actually used on embedded food
                    self.c["opened_with_hard"] += e["got"]
                    self.c["weeks_used_hard"] += 1
                if e["hard"] >= 0.4:
                    self.c["opened_with_hard_40"] += e["got"]
                if e["hard"] == 0 and e["left"] > 0:
                    self.c["bare_got"] += e["got"]
                    self.c["bare_left"] += e["left"]

    def results(self):
        c = self.c
        return {"tools": dict(c),
                "hard_in_hand_share": c["with_hard_40"] / c["adult_forage_weeks"] if c["adult_forage_weeks"] else None}


def observers(w):
    from run_f1 import Probe
    from run_mb1a import Lineages
    return Probe(), Lineages(w), Tools()


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers += list(observers(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def reload_check(seed):
    setup("fx2")
    from acl.world import World
    a = make_world(seed, ARMS["e"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b) and any(t.embedded > 0 for row in a.tiles for t in row)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("fx2", seed, years, "{}", 0) == call("v2", seed, years, "{}", 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: embedded_share 0 = code_v2 (settings left out): {'yes' if t else 'NO'}")
    base = call("fx2", 501, 20, "{}", 0)
    he = call("fx2", 501, 20, json.dumps(ARMS["e"]), 0)
    h0 = call("fx2", 501, 20, json.dumps(ARMS["e0"]), 0)
    for name, h in (("e", he), ("e0", h0)):
        t = h != base
        ok &= t
        lines.append(f"arm {name}, seed 501, 20 years: the setting changes the world (it acts): {'yes' if t else 'NO'}")
    t = he != h0
    ok &= t
    lines.append(f"seed 501, 20 years: e differs from e0 (the tool route acts): {'yes' if t else 'NO'}")
    for arm in ("c", "e"):
        t = call("fx2", 501, 20, json.dumps(ARMS[arm]), 1) == call("fx2", 501, 20, json.dumps(ARMS[arm]), 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without the observers: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm e, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    setup("fx2")
    lines.append(f"code_fx2 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def mech(arm):
    """Throwaway seeds, years 0-10: is embedded food met, and do bare hands open it at `embedded_bare`? Prints only
    the mechanism: no survival, population, deaths or tool use."""
    setup("fx2")
    tot = Counter()
    for seed in MECH_SEEDS:
        w = make_world(seed, ARMS[arm])
        ob = Tools()
        w.observers.append(ob)
        for _ in range(10 * WPY):
            w.step()
            if not w.living():
                break
        tot += ob.c
    share = tot["opened"] / tot["food_got"] if tot["food_got"] else 0.0
    rate = tot["bare_got"] / tot["bare_left"] if tot["bare_left"] else 0.0
    print(f"{arm}: embedded food as a share of adults' foraged food, years 0-10: {share:.3f} (check: >= 0.25) | "
          f"bare-handed opening, got per unit wanted: {rate:.3f} (check: 0.20 +- 0.05; below it only where a tile ran out)",
          flush=True)


def run_one(arm, seed, years=YEARS, out=None):
    setup("fx2")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    probe, lin, tools = observers(w)
    w.observers += [probe, lin, tools]
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **probe.results(), "mb1a": lin.results(), **tools.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
    q = (HERE / "questions.md").read_text(encoding="utf-8")
    if "SIGNED OFF" not in q.splitlines()[0]:
        sys.exit("ABORT: FX2 is a draft; the creator has not signed it off")
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
    elif cmd == "mech":
        for a in ("e", "e0"):
            mech(a)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "run":
        batch()
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, years=8, out=HERE / "output_smoke")
