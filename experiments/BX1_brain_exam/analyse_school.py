"""BX1 Phase A2 (exploratory, labelled): the learning brain's school vs the old mind on the same first babies.

Reads output/school_log.jsonl and output/baseline_log.jsonl (the same school worlds, seeds 10001+, life i = seed 10000+i).
Prints the learning curve (mean age at death per block of lives, with population beside each), a trend (slope of age
on life number, with a bootstrap interval), and the paired comparison on the lives both ran.

  python analyse_school.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

OUT = Path(__file__).parent / "output"
BLOCK = 50


def read(name):
    f = OUT / name
    return [json.loads(x) for x in open(f)] if f.exists() else []


def age(r):
    return float(r["age"] or 0.0)


def boot_ci(stat, n, reps=10000, seed=1):
    rng = np.random.default_rng(seed)
    vals = [stat(rng.integers(0, n, n)) for _ in range(reps)]
    return np.percentile(vals, [2.5, 97.5])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    s, b = read("school_log.jsonl"), read("baseline_log.jsonl")
    print(f"school lives: {len(s)}; old-mind lives: {len(b)}")
    print("learning curve (mean age at death, n lives per block):")
    for i in range(0, len(s), BLOCK):
        c = s[i:i + BLOCK]
        mse = [r["mse"] for r in c if r["mse"] is not None]
        print(f"  lives {i + 1:3d}-{i + len(c):3d}: age {np.mean([age(r) for r in c]):5.1f} (n={len(c)}), "
              f"reached 16: {sum(age(r) >= 16 for r in c)}/{len(c)}, prediction error {np.mean(mse):.4f}")
    x = np.array([r["life"] for r in s], float)
    y = np.array([age(r) for r in s])
    slope = np.polyfit(x, y, 1)[0]
    lo, hi = boot_ci(lambda k: np.polyfit(x[k], y[k], 1)[0], len(s))
    print(f"trend: {slope * 100:+.2f} years per 100 lives (95% bootstrap {lo * 100:+.2f} to {hi * 100:+.2f}; n={len(s)})")
    n = min(len(s), len(b))
    assert all(s[i]["seed"] == b[i]["seed"] for i in range(n)), "school and baseline lives are not the same worlds"
    d = np.array([age(s[i]) - age(b[i]) for i in range(n)])
    lo, hi = boot_ci(lambda k: d[k].mean(), n)
    print(f"paired lives 1-{n}: brain {np.mean([age(r) for r in s[:n]]):.1f} y vs old mind "
          f"{np.mean([age(r) for r in b[:n]]):.1f} y; difference {d.mean():+.1f} (95% bootstrap {lo:+.1f} to {hi:+.1f}); "
          f"brain longer in {int((d > 0).sum())}/{n}, shorter in {int((d < 0).sum())}/{n}")
    xd = np.arange(1, n + 1, dtype=float)      # the gap's trend: world difficulty cancels within each paired world
    sl = np.polyfit(xd, d, 1)[0]
    lo, hi = boot_ci(lambda k: np.polyfit(xd[k], d[k], 1)[0], n)
    print(f"trend of the gap (brain - old mind) over lives 1-{n}: {sl * 100:+.2f} years per 100 lives "
          f"(95% bootstrap {lo * 100:+.2f} to {hi * 100:+.2f})")
    late = {}                                  # the old mind on school lives 201-300 (Oracle; plan addendum)
    for f in sorted(OUT.glob("baseline_oci*_log.jsonl")):
        for x in open(f):
            r = json.loads(x)
            late[r["seed"]] = r
    if late:
        sb = {r["seed"]: r for r in s}
        ks = sorted(k for k in late if k in sb)
        dl = np.array([age(sb[k]) - age(late[k]) for k in ks])
        lo, hi = boot_ci(lambda k: dl[k].mean(), len(dl))
        print(f"school lives {ks[0] - 10000}-{ks[-1] - 10000} (n={len(ks)}): brain {np.mean([age(sb[k]) for k in ks]):.1f} y vs "
              f"old mind {np.mean([age(late[k]) for k in ks]):.1f} y; difference {dl.mean():+.1f} (95% bootstrap "
              f"{lo:+.1f} to {hi:+.1f}); old mind on Oracle (Linux), the school on the PC: not bit-identical worlds")
    for tag, rows in (("brain", s[:n]), ("old mind", b[:n])):
        print(f"  {tag}: reached 16 {sum(age(r) >= 16 for r in rows)}/{n}; deaths {dict(Counter(r['died'] for r in rows).most_common(5))}")


if __name__ == "__main__":
    main()
