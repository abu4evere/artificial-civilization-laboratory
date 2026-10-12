"""ST1 - stranded at sea: how often does someone end a week standing on water with nothing that floats?

Found by the property test `tests/test_properties.py` on GitHub's machine (world 601). Read-only: it only looks at the
world after each week; nothing is changed. ACL's own code (the live world), 20 founders, 30 years, 40 fixed seeds.

  python experiments/ST1_stranded_at_sea/check.py          (writes output/check.json)
"""
import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from acl import Config, World  # noqa: E402

SEEDS = [s for b in (600, 700, 800, 900) for s in range(b, b + 10)]
YEARS = 30
OUT = Path(__file__).with_name("output")


def one(seed: int) -> dict:
    w = World(Config(seed=seed, founders=20))
    n = Counter()
    run = {}          # person -> consecutive weeks stranded
    longest = 0
    cases = []
    for _ in range(YEARS * 52):
        if not w.living():
            break
        w.step()
        n["person_weeks"] += len(w.living())
        now = set()
        for p in w.living():
            if not w.tile(p.loc).water:
                continue
            if w.passable(p, p.loc):
                n["afloat"] += 1
                continue
            c = w.people.get(p.caregiver) if p.caregiver else None
            if c is not None and c.alive and c.loc == p.loc and w.passable(c, p.loc):
                n["carried_by_afloat_carer"] += 1      # a child in the carer's boat: intended
                continue
            n["stranded"] += 1
            n["stranded_child" if c is not None else "stranded_adult"] += 1
            now.add(p.id)
            run[p.id] = run.get(p.id, 0) + 1
            longest = max(longest, run[p.id])
            cases.append([w.tick, p.id, round(p.age(w.tick) / 52, 1)])
        for pid in list(run):
            if pid not in now:
                del run[pid]
    return {"seed": seed, "counts": dict(n), "longest_run_weeks": longest, "cases": cases}


if __name__ == "__main__":
    with ProcessPoolExecutor(4) as ex:
        rows = list(ex.map(one, SEEDS))
    tot = Counter()
    for r in rows:
        tot.update(r["counts"])
    on_water = tot["afloat"] + tot["carried_by_afloat_carer"] + tot["stranded"]
    summary = {
        "seeds": SEEDS, "years": YEARS, "founders": 20, "code": "acl (live)",
        "totals": dict(tot),
        "worlds_with_any_stranding": sum(1 for r in rows if r["counts"].get("stranded")),
        "stranded_share_of_weeks_on_water": round(tot["stranded"] / on_water, 4) if on_water else None,
        "stranded_share_of_all_person_weeks": round(tot["stranded"] / tot["person_weeks"], 6),
        "longest_run_weeks": max(r["longest_run_weeks"] for r in rows),
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "check.json").write_text(json.dumps({"summary": summary, "worlds": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
