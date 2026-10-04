# E4 — Replication: E1 code against E2 code on new worlds · Predictions (FROZEN)

**Question:** Did the four changes (E2) make the world worse, or did E2 draw unlucky histories?
- **A, a real effect:** water barriers cause demographic harm; infant starvation rises consistently; population is
  lower on average.
- **B, noise:** seeds 106 and 107 were unusual; over many worlds E1 and E2 perform similarly.

**Design:** 16 new seeds (201–216), never run before, 200 years each, under E1's code and under E2's code. Both
codes are frozen: E1's was rebuilt and verified to reproduce E1 exactly; E2's is the current code. The same
observers and measures as E1/E2. The worlds alternate E1 then E2. Nothing is changed during the run: no
features, laws, fixes, balancing or tweaks. Where a measure exists for seeds 101–108 too, it is pooled over all
24 worlds; the 16 new worlds are also reported alone.

**Written:** 2026-10-02, before any E4 run.

## Decision rule (fixed in advance)

Compared per world (same seed, same map and founders, two codes):

- **A is supported** if E2's population at year 100 is lower in at least 17 of 24 worlds (one-sided sign test,
  p < 0.05), **and** the mean difference's 95% bootstrap interval over worlds excludes zero.
- **B is supported** if that interval includes zero **and** the mean gap shrinks below 10% of E1's mean.
- Otherwise: **unresolved.** Report the size and interval as they are.
- The same rule applies, separately, to **infant starvation deaths per 1000 infant-years** (pooled per world;
  "higher in E2" in place of "lower").

## Predictions (Claude)

1. Population at year 100 is lower under E2 on average, but by less than in the first 8 worlds (under 25%);
   the decision rule ends **unresolved** or **A**. Confidence 60% that the gap is real, 40% that it is mostly
   noise.
2. Infant starvation per 1000 infant-years is higher under E2 by less than in the first 8 (under +40%).
3. Island mixing at year 100 is lower under E2 in most worlds whose islands are more than 3 tiles apart.
4. E2 keeps its gains in every world: claims tested at least 10 per world-year; reputation tracks accuracy
   (pooled r ≥ 0.4); open-water crossings happen; techniques are taken up from marks.
5. Techniques tried and their median life are similar under both codes (within 20%).
6. At least one new world under E2 shows the seed-105 pattern: no possible mates on the home island, births
   collapsing.

## Kill criterion (this experiment is invalid if…)

- any run crashes, or the two codes are found to differ in anything but the four changes (the E1 code is
  re-verified on one E1 seed before the new runs start);
- fewer than 12 new worlds finish under both codes.
