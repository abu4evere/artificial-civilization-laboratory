"""BX1 Phase A2 after-school test (exploratory, labelled; plan: questions.md addendum, written before the data).
Reads the three arms' logs on worlds 20001-20150 (OLD = baseline_test*, MBB = fixed_mbb_seed1_test*,
SCHOOL = fixed_school_brain_300_test*), pairs them by world, prints each arm and the paired differences.

  python analyse_aftertest.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

OUT = Path(__file__).parent / "output"
ARMS = {"OLD": "baseline_test", "MBB": "fixed_mbb_seed1_test", "SCHOOL": "fixed_school_brain_300_test"}


def arm(prefix):
    rows = {}
    for f in sorted(OUT.glob(prefix + "*.jsonl")):
        for x in open(f):
            r = json.loads(x)
            rows[r["seed"]] = r
    return rows


def age(r):
    return float(r["age"] or 0.0)


def paired(a, b, seeds, reps=10000):
    d = np.array([age(a[s]) - age(b[s]) for s in seeds])
    rng = np.random.default_rng(1)
    boots = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(reps)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return d.mean(), lo, hi, int((d > 0).sum()), int((d < 0).sum()), len(d)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    data = {k: arm(v) for k, v in ARMS.items()}
    seeds = sorted(set.intersection(*(set(v) for v in data.values())))
    print(f"worlds with all three arms: {len(seeds)} ({', '.join(f'{k} {len(v)}' for k, v in data.items())})")
    for k, v in data.items():
        rows = [v[s] for s in seeds]
        print(f"  {k:6s}: mean age {np.mean([age(r) for r in rows]):5.1f}, reached 16 {sum(age(r) >= 16 for r in rows)}/"
              f"{len(rows)}; deaths {dict(Counter(r['died'] for r in rows).most_common(5))}")
    for a, b in (("SCHOOL", "OLD"), ("SCHOOL", "MBB"), ("MBB", "OLD")):
        m, lo, hi, up, dn, n = paired(data[a], data[b], seeds)
        print(f"{a} - {b}: {m:+.1f} years (95% bootstrap {lo:+.1f} to {hi:+.1f}); {a} longer in {up}/{n}, shorter in {dn}/{n}")


if __name__ == "__main__":
    main()
