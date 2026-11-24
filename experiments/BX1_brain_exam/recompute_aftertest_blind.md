# BX1 after-school test and school: blind recompute

- Written 2026-11-24 08:19 EST on User-PC (Windows) by a fresh assistant session acting as independent recomputer.
- Blind: I did not open any `analyse_*.py`, `phaseA_findings.md` or any `*.txt` in `output/`. I read only the raw JSONL logs listed below and the plan text quoted in the task.
- Age null is treated as 0 (there were no null ages). Bootstrap: resample worlds (seeds) with replacement, 10,000 resamples, a fresh `numpy.random.default_rng(1)` for each comparison, percentiles 2.5 and 97.5 of the resampled mean paired difference.

## Part 1: after-school test (seeds 20001-20150)

Files: OLD = `baseline_test{0,1,2}_log.jsonl`; MBB = `fixed_mbb_seed1_test{0,1,2}_log.jsonl`; SCHOOL = `fixed_school_brain_300_test{0,1,2}_log.jsonl`.
Each arm: 150 lines, 150 unique seeds 20001-20150, no duplicates, no missing seeds, no null ages. Seeds in all three arms: **n = 150**.

| Arm | n | Mean age | Median age | Lives age >= 16 |
|---|---|---|---|---|
| OLD | 150 | 26.665 | 23.35 | 88 / 150 |
| MBB | 150 | 19.873 | 14.45 | 69 / 150 |
| SCHOOL | 150 | 27.832 | 20.40 | 86 / 150 |

Death causes (n = 150 each; "null" = `died` is null, all at age 80.0):

| Cause | OLD | MBB | SCHOOL |
|---|---|---|---|
| starvation | 58 | 74 | 45 |
| thirst | 30 | 41 | 43 |
| illness | 22 | 12 | 28 |
| neglect | 17 | 13 | 10 |
| old age | 15 | 7 | 20 |
| killed | 4 | 2 | 0 |
| childbirth | 2 | 0 | 1 |
| null (alive at 80) | 2 | 1 | 3 |

Paired differences (by seed, n = 150):

| Comparison | Mean diff (years) | 95% bootstrap CI | First arm longer | Shorter | Ties |
|---|---|---|---|---|---|
| SCHOOL - OLD | +1.167 | [-2.458, +4.733] | 70 | 67 | 13 |
| SCHOOL - MBB | +7.959 | [+4.394, +11.552] | 84 | 52 | 14 |
| MBB - OLD | -6.792 | [-10.376, -3.369] | 49 | 89 | 12 |

**Reading under the plan's rule:**
- SCHOOL - OLD: the interval [-2.458, +4.733] includes 0, so by the plan's rule SCHOOL is **"as good as the old mind"**.
- SCHOOL - MBB: the lower bound +4.394 is above 0, so by the plan's rule **"the school helped"**.

## Part 2: the school (seeds 10001-10300)

`school_log.jsonl`: 300 lines, 300 unique seeds; line order equals seed order 10001-10300 and the `life` field runs 1..300 in line order. No nulls in age or died.

Mean age of the school brain in blocks of 50 lives (line order):

| Lives | n | Mean age | Age >= 16 |
|---|---|---|---|
| 1-50 | 50 | 18.880 | 28 |
| 51-100 | 50 | 15.872 | 21 |
| 101-150 | 50 | 19.232 | 23 |
| 151-200 | 50 | 27.776 | 30 |
| 201-250 | 50 | 22.058 | 25 |
| 251-300 | 50 | 35.010 | 37 |

Paired brain minus old mind (same seeds):

| Seeds | Old-mind file(s) | n | Brain mean | Old mean | Mean diff | 95% bootstrap CI | Brain longer | Shorter | Ties |
|---|---|---|---|---|---|---|---|---|---|
| (a) 10001-10112 | `baseline_log.jsonl` | 112 | 18.201 | 29.835 | -11.634 | [-15.993, -7.195] | 34 | 63 | 15 |
| (b) 10201-10300 | `baseline_oci{0,1,2,3}_log.jsonl` | 100 | 28.534 | 30.496 | -1.962 | [-6.783, +2.996] | 41 | 51 | 8 |

## Data notes (no causes inferred)
- No missing seeds and no duplicate seeds in any arm or file used; no null ages anywhere.
- `died` is null in 10 lines, all with age exactly 80.0 (about 4200 weeks): OLD seeds 20033, 20148; MBB 20121; SCHOOL 20105, 20131, 20150; baseline_log 10021, 10104; baseline_oci 10247, 10278. Counted as "null" above; their age 80.0 is used as is.
- The minimum age in each test file is identical across the three arms (test0 0.9, test1 0.2, test2 1.5), and 12-14 worlds per comparison are exact ties.
- `fixed_school_brain_300_smoke_log.jsonl` (1 line) exists and was not used.
- Old-mind lives for seeds 10113-10200 are not present in the files given, so Part 2 pairs cover 212 of the 300 school lives.

## Code used

```python
import json, collections, numpy as np
D = r"D:\acl\experiments\BX1_brain_exam\output\\"

def load(names):
    rows = []
    for n in names:
        with open(D + n, encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line: continue
                r = json.loads(line); r["_file"] = n; rows.append(r)
    return rows

def audit(label, rows):
    seeds = [r["seed"] for r in rows]
    c = collections.Counter(seeds)
    dups = {s: k for s, k in c.items() if k > 1}
    nulls_age = sum(1 for r in rows if r.get("age") is None)
    nulls_died = sum(1 for r in rows if r.get("died") is None)
    print(f"  [{label}] lines={len(rows)} unique seeds={len(c)} min={min(c)} max={max(c)} dups={dups} null_age={nulls_age} null_died={nulls_died}")

def age(r): return 0.0 if r.get("age") is None else float(r["age"])

def bystamp(rows):
    return {r["seed"]: r for r in rows}

def boot(d):
    rng = np.random.default_rng(1)
    d = np.asarray(d, float); n = len(d)
    idx = rng.integers(0, n, size=(10000, n))
    m = d[idx].mean(axis=1)
    return d.mean(), np.percentile(m, 2.5), np.percentile(m, 97.5)

print("PART 1")
arms = {
 "OLD": load([f"baseline_test{i}_log.jsonl" for i in range(3)]),
 "MBB": load([f"fixed_mbb_seed1_test{i}_log.jsonl" for i in range(3)]),
 "SCHOOL": load([f"fixed_school_brain_300_test{i}_log.jsonl" for i in range(3)]),
}
for k, v in arms.items(): audit(k, v)
maps = {k: bystamp(v) for k, v in arms.items()}
common = sorted(set.intersection(*[set(m) for m in maps.values()]))
expected = set(range(20001, 20151))
print("  common n =", len(common), " missing from expected:", sorted(expected - set(common)), " extra:", sorted(set(common) - expected))
for k in arms:
    a = np.array([age(maps[k][s]) for s in common])
    ge16 = int((a >= 16).sum())
    dc = collections.Counter(str(maps[k][s].get("died")) for s in common)
    print(f"  {k}: mean age={a.mean():.3f} median={np.median(a):.2f} age>=16: {ge16}/{len(a)} deaths={dict(sorted(dc.items(), key=lambda x:-x[1]))}")
for x, y in [("SCHOOL","OLD"),("SCHOOL","MBB"),("MBB","OLD")]:
    d = np.array([age(maps[x][s]) - age(maps[y][s]) for s in common])
    m, lo, hi = boot(d)
    print(f"  {x}-{y}: mean diff={m:.3f} 95% CI [{lo:.3f}, {hi:.3f}]  longer={int((d>0).sum())} shorter={int((d<0).sum())} ties={int((d==0).sum())}")

print("PART 2")
school = load(["school_log.jsonl"]); audit("school", school)
old1 = load(["baseline_log.jsonl"]); audit("baseline", old1)
old2 = load([f"baseline_oci{i}_log.jsonl" for i in range(4)]); audit("baseline_oci", old2)
lifes = [r.get("life") for r in school]
print("  school 'life' field sequential 1..300 in line order:", lifes == list(range(1, 301)))
print("  school seed == 10000+line#:", [r["seed"] for r in school] == list(range(10001, 10301)))
sa = np.array([age(r) for r in school])
for b in range(6):
    blk = sa[b*50:(b+1)*50]
    print(f"  block {b*50+1}-{(b+1)*50}: n={len(blk)} mean age={blk.mean():.3f} age>=16: {int((blk>=16).sum())}")
sm = bystamp(school)
for label, om, lo_s, hi_s in [("(a) 10001-10112", bystamp(old1), 10001, 10112), ("(b) 10201-10300", bystamp(old2), 10201, 10300)]:
    seeds = [s for s in range(lo_s, hi_s+1) if s in sm and s in om]
    miss = [s for s in range(lo_s, hi_s+1) if s not in sm or s not in om]
    extra_old = sorted(s for s in om if not (lo_s <= s <= hi_s))
    d = np.array([age(sm[s]) - age(om[s]) for s in seeds])
    m, lo, hi = boot(d)
    bm = np.mean([age(sm[s]) for s in seeds]); oldm = np.mean([age(om[s]) for s in seeds])
    print(f"  {label}: n={len(seeds)} missing={miss} old-seeds-outside-range={extra_old} brain mean={bm:.3f} old mean={oldm:.3f} diff={m:.3f} CI [{lo:.3f}, {hi:.3f}] longer={int((d>0).sum())} shorter={int((d<0).sum())} ties={int((d==0).sum())}")
```
