"""E8.4 autumn autopsy (E8_4_autumn_autopsy.md). Read-only replays of the E7 code, seeds 301–304, 120 years.

  python experiments/E8_crucible/run_e84.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
sys.path.insert(0, str(E7 / "code_e7"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
AUTUMN = 2
OUT = HERE / "output_e84"


class Probe:
    def __init__(self):
        self.pops = []
        self.cur = defaultdict(lambda: {"weeks": 0, "forage_weeks": 0, "got": 0.0, "acts": 0, "need": 0.0,
                                        "max_edible": 0.0, "chosen": Counter()})
        self.rows = []            # one per adult per autumn, finished at the first week of winter

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        season = wk // WPS
        c = world.cfg
        if season == AUTUMN:
            for e in events:
                if e["k"] == "forage" and e.get("a") in world.people:
                    r = self.cur[e["a"]]
                    r["got"] += e.get("got", 0.0)
                    r["acts"] += 1
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        if season == AUTUMN:
            for p in living:
                if p.age(world.tick) < 16 * WPY:
                    continue
                r = self.cur[p.id]
                r["weeks"] += 1
                r["need"] += p.need(c, world.tick)
                r["max_edible"] = max(r["max_edible"], p.edible())
                ch = next((x[0] for x in (p.considered or []) if x[3]), None)
                if ch:
                    r["chosen"][ch] += 1
                    if ch == "forage":
                        r["forage_weeks"] += 1
        if wk == 3 * WPS:          # the first week of winter: close the autumn
            for p in living:
                r = self.cur.pop(p.id, None)
                if not r or r["weeks"] < 10:
                    continue
                stored = 0.0
                for dy in range(-c.reach, c.reach + 1):
                    for dx in range(-c.reach, c.reach + 1):
                        t = world.tile(((p.loc[0] + dx) % c.width, (p.loc[1] + dy) % c.height))
                        stored += sum(st[1] + st[2] for st in t.stash)
                per_act = r["got"] / r["acts"] if r["acts"] else None
                self.rows.append({
                    "year": tick // WPY, "weeks": r["weeks"], "forage_weeks": r["forage_weeks"],
                    "food_per_forage": round(per_act, 2) if per_act is not None else None,
                    "possible_surplus": round(13 * per_act - r["need"] * 13 / r["weeks"], 1) if per_act is not None else None,
                    "food_in_hand": round(p.food, 1), "seeds_in_hand": round(p.seeds, 1),
                    "stored_within_reach": round(stored, 1), "max_edible_autumn": round(r["max_edible"], 1),
                    "chosen": dict(r["chosen"]),
                })
            self.cur.clear()


def run(seed):
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    sp = [s["population"] for s in saved["samples"]][: len(probe.pops)]
    res = {"seed": seed, "replay_matches_saved": probe.pops == sp, "rows": probe.rows}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches_saved']}, adult-autumns {len(probe.rows)}", flush=True)


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
