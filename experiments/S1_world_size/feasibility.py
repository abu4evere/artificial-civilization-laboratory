"""S1 feasibility check (feasibility_plan.md, tag `S1-feasibility-plan`). Control code (code_e13r), settings only.
Records initialization, comparability and manipulation measures at week one, and run time over 10 years.
Population, births, deaths and extinction are deliberately not recorded.

  python experiments/S1_world_size/feasibility.py          # all arms x seeds 9001-9004, four workers
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "E13R_replication" / "code_e13r"
OUT = HERE / "output_feasibility"
ARMS = {"C": {"width": 40, "height": 40, "founders": 20},
        "L": {"width": 80, "height": 80, "founders": 20},
        "LP": {"width": 80, "height": 80, "founders": 80}}
SEEDS = (9001, 9002, 9003, 9004)
YEARS, WPY = 10, 52


def one(arm: str, seed: int) -> dict:
    sys.path.insert(0, str(CODE))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()
    from acl.config import Config
    from acl.util import distance
    from acl.world import World
    t0 = time.perf_counter()
    w = World(Config(seed=seed, anticipation_weight=1.0, **ARMS[arm]))
    t_init = time.perf_counter() - t0
    c = w.cfg
    land = [t for row in w.tiles for t in row if not t.water]
    founders = list(w.people.values())
    # founding bands: founders who start with ties to each other (the code gives each band mutual relations)
    band, bands = {}, []
    for p in founders:
        if p.id in band:
            continue
        members = [p] + [w.people[q] for q in p.rel if q in w.people]
        k = len(bands)
        bands.append(members)
        for m in members:
            band[m.id] = k

    def centre(members):
        x0, y0 = members[0].loc
        xs = [x0 + ((m.loc[0] - x0 + c.width // 2) % c.width - c.width // 2) for m in members]
        ys = [y0 + ((m.loc[1] - y0 + c.height // 2) % c.height - c.height // 2) for m in members]
        return (round(sum(xs) / len(xs)) % c.width, round(sum(ys) / len(ys)) % c.height)
    centres = [centre(b) for b in bands]
    gaps = [distance(a, b, c.width, c.height) for i, a in enumerate(centres) for b in centres[i + 1:]]
    elig = [[q for q in founders if q.sex != p.sex and w.kinship(p, q) == 0 and abs(p.birth - q.birth) <= 15 * WPY]
            for p in founders]
    res = {
        "arm": arm, "seed": seed, "init_seconds": round(t_init, 2),
        "land_share": round(len(land) / (c.width * c.height), 3),
        "mean_land_fertility": round(statistics.mean(t.fertility for t in land), 3),
        "islands": len(w.landmasses()),
        "animal_groups_per_100_land": round(100 * len(w.animals) / len(land), 2),
        "founders": len(founders), "founder_food": c.founder_food,
        "land_per_founder": round(len(land) / len(founders), 1),
        "bands": len(bands), "band_sizes": sorted(len(b) for b in bands),
        "mean_gap_between_band_centres": round(statistics.mean(gaps), 1) if gaps else None,
        "eligible_founders_per_founder": round(statistics.mean(len(e) for e in elig), 1),
        "eligible_in_sight_per_founder": round(statistics.mean(
            sum(1 for q in e if distance(p.loc, q.loc, c.width, c.height) <= c.perception) for p, e in zip(founders, elig)), 2),
    }
    t1 = time.perf_counter()
    error = None
    try:
        for _ in range(YEARS * WPY):
            w.step()
            if not w.living():
                break       # not recorded: extinction is an outcome, not a feasibility measure
    except Exception as e:  # noqa: BLE001
        error = repr(e)
    res["ran_without_error"] = error is None
    res["error"] = error
    res["seconds_per_world_year"] = round((time.perf_counter() - t1) / YEARS, 2)
    return res


def main():
    OUT.mkdir(exist_ok=True)
    me = [sys.executable, str(Path(__file__).resolve())]
    jobs = [(a, s) for a in ARMS for s in SEEDS]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.run(me + ["one", j[0], str(j[1])]), jobs))
    R = [json.loads((OUT / f"{a}_{s}.json").read_text(encoding="utf-8")) for a, s in jobs]
    L = ["# S1 feasibility check: results\n", "Plan: `feasibility_plan.md` (tag `S1-feasibility-plan`). Seeds 9001–9004, "
         "10 years, control code. Population, births, deaths and extinction were not recorded.\n"]
    keys = ["ran_without_error", "land_share", "mean_land_fertility", "islands", "animal_groups_per_100_land", "founders",
            "founder_food", "land_per_founder", "bands", "band_sizes", "mean_gap_between_band_centres",
            "eligible_founders_per_founder", "eligible_in_sight_per_founder", "init_seconds", "seconds_per_world_year"]
    L.append("| measure | " + " | ".join(ARMS) + " |")
    L.append("|---|" + "---|" * len(ARMS))
    for k in keys:
        cells = []
        for a in ARMS:
            vals = [r[k] for r in R if r["arm"] == a]
            if isinstance(vals[0], bool):
                cells.append(f"{sum(vals)} of {len(vals)}")
            elif isinstance(vals[0], list):
                cells.append("; ".join(str(v) for v in vals[:2]))
            else:
                cells.append(f"{statistics.median(vals)}" + (f" ({min(vals)}–{max(vals)})" if min(vals) != max(vals) else ""))
        L.append(f"| {k} | " + " | ".join(cells) + " |")
    spy = {a: statistics.median(r["seconds_per_world_year"] for r in R if r["arm"] == a) for a in ARMS}
    hours = sum(spy.values()) * 120 * 256 / 4 / 3600
    L.append(f"\n**Runtime estimate** for a main run of 256 seeds × C, L, LP (+ sham at C's cost) × 120 years on four "
             f"workers: about **{hours + spy['C'] * 120 * 256 / 4 / 3600:.0f} hours** (seconds per world-year: "
             + ", ".join(f"{a} {v}" for a, v in spy.items()) + "). Early years only; later years may differ as populations change.")
    errors = [f"{r['arm']} {r['seed']}: {r['error']}" for r in R if r["error"]]
    if errors:
        L.append("\nErrors: " + "; ".join(errors))
    text = "\n".join(L) + "\n"
    (HERE / "feasibility_results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    if sys.argv[1:2] == ["one"]:
        r = one(sys.argv[2], int(sys.argv[3]))
        OUT.mkdir(exist_ok=True)
        (OUT / f"{sys.argv[2]}_{sys.argv[3]}.json").write_text(json.dumps(r), encoding="utf-8")
        print(r["arm"], r["seed"], "ok" if r["ran_without_error"] else r["error"], flush=True)
    else:
        main()
