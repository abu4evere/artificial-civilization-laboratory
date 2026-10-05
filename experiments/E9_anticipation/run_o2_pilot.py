"""O2 feasibility pilot (read-only, descriptive; no predictions, no mechanism). Replays the E7 code (E9 Arm 0),
seeds 301–304, 120 years. For every child (under 12) who starves: who was caring for them, in which season, whether
that carer is alive at the next autumn, and whether they then still care for children.

  python experiments/E9_anticipation/run_o2_pilot.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
sys.path.insert(0, str(E7 / "code_e7"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output_o2_pilot"


class Probe:
    def __init__(self):
        self.pops = []
        self.carer_of = {}
        self.losses = []          # [tick, season, carer]
        self.pending = []

    def __call__(self, world, events):
        tick = world.tick - 1
        s = (tick % WPY) // WPS
        for e in events:
            if e["k"] == "death" and e.get("cause") == "starvation" and e.get("a") in world.people:
                p = world.people[e["a"]]
                if p.age(tick) < 12 * WPY:
                    carer = self.carer_of.get(p.id)
                    self.losses.append({"tick": tick, "season": s, "carer": carer, "carer_alive_next_autumn": None,
                                        "dependents_next_autumn": None})
        living = world.living()
        for p in living:
            if p.age(world.tick) < 12 * WPY:
                self.carer_of[p.id] = p.caregiver or p.mother
        if tick % 520 == 519:
            self.pops.append(len(living))
        if tick % WPY == 2 * WPS:                 # first week of autumn: settle losses from the past year
            for L in self.losses:
                if L["carer_alive_next_autumn"] is None and tick - L["tick"] < WPY and tick > L["tick"]:
                    c = world.people.get(L["carer"]) if L["carer"] else None
                    L["carer_alive_next_autumn"] = bool(c and c.alive)
                    L["dependents_next_autumn"] = len(world.dependents(c.id)) if c and c.alive else 0


def run(seed):
    saved = json.loads((HERE / "output" / f"arm0_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    res = {"seed": seed, "replay_matches_e9": probe.pops == saved["pops"], "losses": probe.losses}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches_e9']}, child starvation deaths {len(probe.losses)}", flush=True)


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
