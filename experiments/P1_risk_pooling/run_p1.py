"""P1 — risk pooling or spreading scarcity (questions.md). Read-only replays of E13R arms A and B, seeds 501-516.

  python experiments/P1_risk_pooling/run_p1.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E13R = HERE.parent / "E13R_replication"
CODE = E13R / "code_e13r"
ARMS = {"a": {}, "b": {"b2_mode": 1}}
SEEDS = tuple(range(501, 517))
WPY, WPS = 52, 13
WINTER = 3 * WPS
OUT = HERE / "output"


def setup():
    sys.path.insert(0, str(CODE))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **ARMS[arm]))


def band(weeks):
    return "under 0.5" if weeks < 0.5 else "0.5-2" if weeks < 2 else "2+"


def close_kin(world, p, living):
    return [q for q in living if q.id != p.id and (q.id == p.partner or world.kinship(p, q) >= 0.5)]


class Probe:
    def __init__(self):
        self.pops = []
        self.start = {}            # pid -> row, this winter
        self.rows = []             # one row per person-winter
        self.deaths = []           # winter starvation deaths
        self.recent_gift = {}      # pid -> last tick they received a gift
        self.weeks = defaultdict(list)    # pid -> [(band, gave, short)] over winter weeks (adults)
        self.short_rows = []       # adult short-weeks: (band, received, died within 4 weeks)
        self.give_rows = []        # adult winter-weeks: (band, gave, short within next 4 weeks)
        self.died_at = {}

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        if tick % 520 == 519:
            self.pops.append(len(world.living()))
        c = world.cfg
        living = world.living()
        received_now = set()
        gave_now = set()
        for e in events:
            if e["k"] == "give":
                received_now.add(e.get("b"))
                gave_now.add(e["a"])
                self.recent_gift[e.get("b")] = world.tick
            elif e["k"] == "death":
                self.died_at[e.get("a")] = world.tick
                if s == 3 and e.get("cause") == "starvation":
                    p = world.people.get(e["a"])
                    if p is None:
                        continue
                    kin = close_kin(world, p, living)
                    near = world.people_near(p.loc, c.perception) if p.loc else []
                    near_ids = {q.id for q in near}
                    rich_near = any(q.id in near_ids and q.edible() >= 2 * q.need(c, world.tick) for q in kin)
                    self.deaths.append({"age": round(p.years(world.tick), 1), "kin": len(kin),
                                        "kin_food": round(sum(q.edible() for q in kin), 1),
                                        "kin_rich_near": rich_near,
                                        "gift_4w": world.tick - self.recent_gift.get(p.id, -999) <= 4})
        if wk == WINTER:
            self.start = {}
            for p in living:
                kin = close_kin(world, p, living)
                need = p.need(c, world.tick)
                fam_need = need + sum(q.need(c, world.tick) for q in kin)
                fam_food = p.edible() + sum(q.edible() for q in kin)
                self.start[p.id] = {"own": band(p.edible() / need), "fam": band(fam_food / fam_need), "kin": len(kin),
                                    "adult": p.age(world.tick) >= 16 * WPY, "short": False, "died": False}
            self.weeks = defaultdict(list)
        if s == 3 and self.start:
            for p in living:
                row = self.start.get(p.id)
                if row is None:
                    continue
                row["short"] |= bool(p.starving)
                if row["adult"]:
                    self.weeks[p.id].append((band(p.edible() / p.need(c, world.tick)), p.id in gave_now,
                                             bool(p.starving), p.id in received_now, world.tick))
            for e in events:
                if e["k"] == "death" and e.get("cause") == "starvation" and e.get("a") in self.start:
                    self.start[e["a"]]["died"] = True
        if wk == WPY - 1 and self.start:
            self.rows.extend(self.start.values())
            for pid, wks in self.weeks.items():
                for i, (b, gave, short, received, t) in enumerate(wks):
                    later = wks[i + 1:i + 5]
                    self.give_rows.append((b, gave, any(x[2] for x in later)))
                    if short:
                        d = self.died_at.get(pid)
                        self.short_rows.append((b, received, d is not None and t < d <= t + 4))
            self.start = {}

    def results(self):
        return {"pops": self.pops, "rows": self.rows, "deaths": self.deaths,
                "short_rows": self.short_rows, "give_rows": self.give_rows}


def run(arm, seed):
    setup()
    w = make_world(arm, seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((E13R / "output" / f"{arm}_seed_{seed}.json").read_text(encoding="utf-8"))
    res = {"arm": arm, "seed": seed, "replay_matches": probe.pops == saved["pops"], **probe.results()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: replay matches {res['replay_matches']}", flush=True)


def verify(arm, seed=501, years=20):
    setup()
    hs = []
    for with_probe in (False, True):
        w = make_world(arm, seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "verify.txt", "a", encoding="utf-8") as f:
        f.write(f"arm {arm} seed {seed}, {years} years: {'READ-ONLY' if ok else 'CHANGES THE WORLD'}\n")
    print(f"verify {arm}:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        for arm in ARMS:
            if subprocess.call(me + ["verify", arm]) != 0:
                sys.exit("ABORT: probe changes the world")
        jobs = [(a, s) for a in ARMS for s in SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()]
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
        print("ALL DONE", flush=True)
    elif sys.argv[1] == "verify":
        sys.exit(0 if verify(sys.argv[2]) else 1)
    else:
        run(sys.argv[1], int(sys.argv[2]))
