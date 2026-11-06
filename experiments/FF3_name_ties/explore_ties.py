"""Exploratory, read-only (not frozen; no reading is drawn from it): how often does each memory's eviction meet a tie
that is settled by the key's text? Counts, on nature v13, every min(..., key=...) call made inside knowhow, inquiry,
information and marks whose key returns a tuple, and whether the minimum's first part is shared (a tie). The wrapper
returns exactly what min returns and draws nothing, so the world is unchanged.

  python experiments/FF3_name_ties/explore_ties.py <seed> <years>   -> explore_ties_<seed>.json
"""
import builtins
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v13"] = HERE.parent / "NV13_nature_v13" / "code_v13"
WPY = base.WPY


def main(seed, years):
    base.setup("v13")
    import acl.information as information
    import acl.inquiry as inquiry
    import acl.knowhow as knowhow
    import acl.marks as marks
    counts = {}

    def make(name):
        def counting_min(*args, key=None, **kw):
            out = builtins.min(*args, key=key, **kw)
            if key is not None and len(args) == 1 and not kw:
                items = list(args[0])
                ks = [key(x) for x in items]
                if ks and isinstance(ks[0], tuple):
                    lo = builtins.min(k[0] for k in ks)
                    tied = sum(1 for k in ks if k[0] == lo)
                    line = sys._getframe(1).f_lineno       # the call site, so each memory is counted apart
                    c = counts.setdefault(f"{name}:{line}", [0, 0, 0])
                    c[0] += 1                      # evictions seen
                    c[1] += int(tied > 1)          # settled by the second part (the text, or a position)
                    c[2] += tied if tied > 1 else 0
            return out
        return counting_min
    for name, mod in (("knowhow", knowhow), ("inquiry", inquiry), ("information", information), ("marks", marks)):
        mod.min = make(name)
    w = base.make_world(seed, {**base.LP})
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    (HERE / f"explore_ties_{seed}.json").write_text(json.dumps({"seed": seed, "years": years, "counts": counts}),
                                                    encoding="utf-8")
    print(seed, counts)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
