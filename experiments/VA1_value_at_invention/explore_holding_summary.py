"""Exploratory summary of explore_holding_<seed>.json (not frozen; no reading is drawn from it).

  python experiments/VA1_value_at_invention/explore_holding_summary.py [folder]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE


def q(xs, f):
    xs = sorted(xs)
    return xs[int(f * (len(xs) - 1))] if xs else None


def main():
    rows = []
    for f in sorted(glob.glob(str(DIR / "explore_holding_98*.json"))):
        r = json.load(open(f))
        rows += r
        print(Path(f).name, "kinds", len(r))
    n = len(rows)
    gone = [x for x in rows if x["first_not_holding"] is not None]
    print(f"kinds {n}; the thing no longer held by its living inventor within 5 years: {len(gone)} ({len(gone) / n:.3f})")
    w = [x["first_not_holding"] for x in gone]
    print(f"  weeks until then: median {q(w, .5)}, quartiles {q(w, .25)} and {q(w, .75)}")
    kept = [x for x in gone if x["recipe_when_not_holding"]]
    print(f"  recipe still known then: {len(kept)} of {len(gone)}; valued above 0.05: "
          f"{sum(1 for x in kept if x['value_when_not_holding'] > 0.05)}")
    if "full" in rows[0]:
        full = [x for x in rows if x["full"]]
        print(f"memory full at invention: {len(full)} of {n}; never held at a week's end (first = 0): "
              f"{sum(1 for x in rows if x['first'] == 0)}")
        lost = [x for x in gone if not x["recipe_when_not_holding"]]
        print(f"of the {len(lost)} recipes gone before the thing: memory full at invention {sum(x['full'] for x in lost)}; "
              f"lost in week 0 {sum(1 for x in lost if x['lost_at'] == 0)}; lost later {sum(1 for x in lost if x['lost_at'] not in (None, 0))}")
        later = [x["lost_at"] for x in lost if x["lost_at"] not in (None, 0)]
        print(f"  weeks to a later loss: median {q(later, .5)}, quartiles {q(later, .25)} and {q(later, .75)}")
        print(f"used at least once: {sum(1 for x in rows if x['n_uses'] > 0)} of {n}")
    print(f"funnel: inputs in hand while the recipe was known {sum(x['inputs'] for x in rows)}; free (not holding, valued) "
          f"{sum(x['free'] for x in rows)}; offered {sum(x['offered'] for x in rows)}; remade {sum(x['remade'] for x in rows)}")


if __name__ == "__main__":
    main()
