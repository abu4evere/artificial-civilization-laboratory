# UP1 — Why is a new kind never made again? Findings (final: recomputed blind by GPT and Gemini; see the end)

**Read-only: no change to nature.** Live v11 (`code_v11`).
- **Frozen** as `UP1-frozen`. Signed off by the assistant under the creator's sleep-mode autonomy (GPT 95%, Gemini
  95%, the assistant 80%; debate round 48).
- **Its origin:** SC1 found that no kind invented after year 100 is ever made again within five years. An exploratory
  check then showed most such kinds are kept, used and valued.

**The run:**
- GitHub Actions run 41450747356; the zero checks ran locally (`zero_local.log`).
- 32 worlds, seeds 22101–22132; LP, 200 years; years 100–200 counted.
- Every number comes from `analyse_up1.py`, written before data. Full tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 32 worlds are present under `code_v11`'s fingerprint;
- **the observer's reproduced make option equaled the code's at every decision** (mismatches 0, about 172 million
  person × kind × decisions).

## The answer
**Mainly blocked at step 3, "cannot make".** In 86.7% [85.2%, 88.3%] of the cases where an adult knows a new kind, they
do not have its materials or made parts in hand. It is also the step where new kinds differ most from old ones.

| step | new kinds [95%] | old kinds | new − old [95%] |
|---|---|---|---|
| 1. holding (as the code skips) | 0.001 | 0.050 | −0.050 |
| 2. value at or below 0.05 | 0.132 [0.116, 0.147] | 0.418 | −0.286 |
| **3. cannot make** | **0.867 [0.852, 0.883]** | 0.411 | **+0.456 [+0.438, +0.475]** |
| 4a. skipped by the running best | 0.000 | 0.040 | −0.040 |
| 4b. beaten by another recipe | 0.000 | 0.016 | −0.016 |
| 5. eligible, not chosen | 0.000 | 0.064 | −0.064 |
| made | 0.000 | 0.000 | 0.000 |

The sample is 4,977,150 person × kind × decisions for new kinds and 166,823,584 for old.
- **The kind count:** `results.md` prints "New kinds: 2,540". That figure merges kinds with the same name in different
  worlds. The count of new kinds with any decisions is **2,862** (the kind-weighted line).

### Secondary (described, not decisive)
- **New kinds are nested.**
  - 99.5% of new-kind decisions concern nested kinds: things whose recipe needs a made part.
  - For nested new kinds, 87.2% are "cannot make". Old nested kinds: 68.4%.
  - **The few simple new kinds** stop instead at the value floor (97.5%): they are not valued enough to make again.
- **Over time:**
  - In the first five years after invention, the inventor is often still holding the thing (14.9% at step 1), and 69.8%
    "cannot make".
  - After that, holding vanishes and "cannot make" reaches 86.8%.
- **Each new kind counted once** (kind-weighted): 86.4% "cannot make", 13.4% value floor.
- **Uptake:** only **34 of 2,862** new kinds were ever the make option, and **4** were ever made.
- **When a new kind passes steps 1–3,** an old kind wins the make choice (step 4: 1,213 cases, all old). Even as the
  make option, it is chosen with a mean probability of 0.004 (old kinds: 0.002).

## Against the prior (the assistant's, frozen)
1. **"Mixed bottlenecks, step 3 largest, then step 1": partly wrong.** Step 3 is not just the largest; it is a clear
   majority. Step 1 is small overall, though present in the first five years.
2. **"The main difference from old kinds is at step 3": right** (+0.456).
3. **"Step 4a is present": hardly.** For new kinds it is 0.01%. The order quirk matters only for old kinds (4.0%).

## What it means
- **New inventions die because they cannot be rebuilt.**
  - Late inventions are combinations of made things, and remaking one needs those made parts in hand.
  - People carry at most 3 made things, and the parts were used up in the first making.
  - So the recipe stays in the head (KL1, SC1), but the hands never hold what it needs.
- **ACL's make choice offers only what can be made right now.**
  - There is no way to work toward a goal: first make part A, then part B, then the whole.
  - The only bridge is the "wanted part" value (0.8 × the whole's value), which makes a missing part worth making for
    itself. UP1 shows this bridge rarely closes the chain for new kinds.
- **This connects three of the creator's capacities:**
  - **planning (5):** making the parts in order;
  - **working memory (round 46):** holding a goal across weeks;
  - **cumulative culture (10):** building on what was made.

  The gap UP1 found is exactly where a goal that persists across steps would act.
- **Not a proposal.** Any change here would be a nature-change test in a copy, chosen by the creator. Possible
  conditions, all general and none naming an invention:
  1. a little more carrying room, if forager evidence supports it;
  2. remembering an unfinished goal across weeks;
  3. the "wanted part" bridge reaching more than one step back.

## Blind recompute (`recompute_up1.md`)
GPT (chat `6ae89f21`) and Gemini 3.1 Pro (chat `003f78c1d7b2d7f3`) recomputed UP1 from the per-world step counts,
blind, with the prompt written before the data. **Both match every point value and both readings** (mainly blocked at
step 3; the largest difference from old kinds at step 3). Interval ends differ by at most 0.0006. **UP1 is final.**

## Addendum (2 November 2026, about 10:20): what is missing (exploratory; outside the frozen plan)
`explore/check_missing.py` (`explore/check_missing.json`) replays world 22101 to year 130.
- **What it counts:** for each "cannot make" case of a nested kind invented from year 100 that the person values above
  0.05 and is not holding (its value v omits the puzzle pull), it records what is missing.
- **One world, 46 new kinds, described only:**

| what is missing | cases |
|---|---|
| raw materials only | 0 |
| **a made part, whose recipe the person knows, but that part cannot be made now either** | **15,513 (88.8%)** |
| a made part whose recipe the person does not know | 1,909 (10.9%) |
| a made part they could make right now | 41 (0.2%); in none of these was it the make option |

In 1,149 of these cases (6.6%) the person's hands were already full (3 made things).

**A lead from the code, not yet a finding:**
- Wanting **does** reach one step back for making. A part of a valued thing gets 0.8 of its value (`_wanted_parts`).
- It **does not** reach into gathering. The pull to gather a material (`_material_wants`) counts only recipes valued by
  their own use (`itemval`), not parts wanted for something else.
- So the chain can break at the part's ingredients: the whole is wanted, the part is wanted, but nothing pulls the
  person to gather what the part needs.

This is a written-law detail, and only a frozen study can say whether it is the cause.
