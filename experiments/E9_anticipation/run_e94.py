"""E9.4 self-erasing lesson (E9_4_self_erasing.md). Read-only replays of E9 A2-full, seeds 301–304, 120 years.

  python experiments/E9_anticipation/run_e94.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "code_a2"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output_e94"


class Probe:
    def __init__(self):
        self.pops = []
        self.exp_at_autumn = {}          # year -> {pid: expectation at the first autumn week}
        self.max_ed = defaultdict(float)
        self.prepared = {}               # year -> set of pids that held 80+ that autumn
        self.short_weeks = defaultdict(lambda: defaultdict(int))   # year -> pid -> short weeks in that winter
        self.short_prev = {}             # year -> set of pids short in the winter ending that year
        self.cur_short = set()

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        s = wk // WPS
        year = tick // WPY
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
        if wk == 2 * WPS:
            self.exp_at_autumn[year] = {p.id: p.expect.get("short@3", 0.0) for p in adults}
            self.max_ed = defaultdict(float)
        if s == 2:
            for p in adults:
                self.max_ed[p.id] = max(self.max_ed[p.id], p.edible())
        if wk == 3 * WPS:
            self.prepared[year] = {pid for pid, v in self.max_ed.items() if v >= 80}
        if s == 3:
            for p in adults:
                if p.starving:
                    self.short_weeks[year][p.id] += 1
                    self.cur_short.add(p.id)
        if wk == WPY - 1:
            self.short_prev[year] = set(self.cur_short)
            self.cur_short = set()

    def rows(self):
        out = []
        for y, exp in self.exp_at_autumn.items():
            nxt = self.exp_at_autumn.get(y + 1)
            if not nxt:
                continue
            for pid, e0 in exp.items():
                if pid not in nxt:
                    continue
                out.append({"year": y, "e_before": round(e0, 3), "e_after": round(nxt[pid], 3),
                            "prepared": pid in self.prepared.get(y, set()),
                            "prepared_again": pid in self.prepared.get(y + 1, set()),
                            "short_weeks": self.short_weeks[y].get(pid, 0),
                            "short_prev_winter": pid in self.short_prev.get(y - 1, set())})
        return out


def run(seed):
    saved = json.loads((HERE / "output" / f"a2full_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed, anticipation_weight=1.0))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    res = {"seed": seed, "replay_matches_e9": probe.pops == saved["pops"], "rows": probe.rows()}
    OUT.mkdir(exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches E9 {res['replay_matches_e9']}, rows {len(res['rows'])}", flush=True)


def verify(seed=304, years=20):
    hs = []
    for with_probe in (False, True):
        w = World(Config(seed=seed, anticipation_weight=1.0))
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
