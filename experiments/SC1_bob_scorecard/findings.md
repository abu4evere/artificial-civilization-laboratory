# SC1 — A scorecard of the creator's twelve capacities on live v11: findings (final: recomputed blind by GPT and Gemini; see the end)

**Read-only: no change to nature.** Live v11 (`code_v11`).
- **Frozen** as `SC1-frozen`, with two operational notes made before any study data.
- **Signed off** by the assistant with the creator present (debate rounds 46 and 47: GPT 86%, Gemini 94%, the
  assistant 70%).
- **What it is:** a **baseline**, not a measure of Bob, not an intelligence score, and never a claim that a capacity is
  absent.

**The run:**
- GitHub Actions run 41424864945; the zero checks ran locally (`zero_local.log`).
- 32 worlds, seeds 22001–22032; LP, 200 years; years 100–200 counted.
- Every number comes from `analyse_sc1.py`, written before data. Full tables are in `results.md`.

**Validity:**
- the zero checks pass, including the observer's own random stream;
- all 32 worlds are present under `code_v11`'s fingerprint;
- every habit update replays exactly.

## The scorecard
| # | capacity | label | primary contrast [95%] | reading |
|---|---|---|---|---|
| 1 | Perception | given | — (98.6% of adult decisions have company in reach) | described |
| 2 | Memory, retrieval when relevant | not measurable | — (45 memories held; 36% told) | described |
| 3 | Learning (the written rule) | measured | **−0.081 [−0.101, −0.064]** (k 0–19 minus k 80+) | inconclusive |
| 3 | Transfer | not measurable | — | — |
| 4 | Causal understanding (proxy) | measured | −0.038 [−0.147, +0.028] | inconclusive |
| 5 | Planning (at most "organized production") | measured | +0.011 [+0.009, +0.050] | inconclusive |
| 6 | Invention with selection by use | measured | **0.000 [0.000, 0.000]** | inconclusive |
| 7 | Own goals (proxy) | measured → **not measurable** (op. note 2) | — (2 told puzzles of matching size) | not measurable |
| 8 | Self-model | not measurable | — | — |
| 9 | **Communication** | measured | **+0.410 [+0.393, +0.428]** | **positive contrast detected** |
| 10a | Social cognition | not measurable (social learning described) | — | — |
| 10b | Cumulative culture (building on others) | measured | −0.038 [−0.045, −0.031] | inconclusive |
| 11 | Motivation | given | — (mean mood 0.76, loneliness 0.29) | described |
| 12 | **Stable behavioural individuality** | measured | **+0.078 [+0.072, +0.084]** | **positive contrast detected** |

## What each reading says
- **9, communication: told places beat chance by a wide margin.**
  - Water told is there when checked 99.98% of the time, against 73.5% for a random tile at the same distance.
  - Game told is there 90.4% of the time, against 39.3%.
  - The sample is 396,764 checks.
  - **The channel is written** (`tell_place`), but what it carries is real: information about things out of sight
    that other people act on.
- **12, individuality: a person's own past actions predict their actions five years later beyond everything in
  Model A.** Model A has temperament, age, sex, the later situations, and **their habit values**. Adding the past
  actions cuts held-out error by 7.8% (56,353 person pairs).
  - **Gemini's cross-situation test** (secondary) agrees. A person's choice bias in familiar situations correlates
    0.32 with their bias in rare ones, against 0.01 for shuffled people.
  - **What it is:** a stable personal style, carried by more than the habit table (perhaps skills, holdings, places,
    ties or attention).
  - **What it is not:** self-chosen goals, or identity in the full sense.
- **3, the learning rule: not shown by this measure, and the sign is the opposite of the prior.**
  - Experienced habits (k 80+) have **larger** absolute error than new ones (k 0–19): −0.081.
  - UV1 found the **signed** bias shrinking with experience. Together, the two suggest experienced habits are less
    biased but more spread out around what follows, or that values keep climbing (UV3).
  - **This is not explained here.** It is an open question, not a finding about learning.
- **4, causal understanding:** after a surprising test, people switch to an alternative recipe **no more often**
  than after a confirming one. The puzzle law pulls toward trying the same thing again.
- **5, planning:** the written want covers nearly every gather of a needed material. Only 61 of 1,316,610 gathers by
  recipe holders were not wanted. Production follows the written pulls; nothing beyond them is shown.
- **6, invention: none of the 3,883 kinds first made in years 100–195 was ever made again by choice within five
  years.** That holds for the more useful and the less useful alike.
  - **New things are one-off.** They are invented, held, and dropped.
  - **An exploratory check confirms it is real, not a counting error** (outside the frozen plan:
    `explore/check_remakes.py`, `explore/check_remakes.json`). World 22001 was replayed to year 130 with only that
    check attached. **All 421 makes in years 100–130 were of kinds first invented before year 100.** None of the 72
    kinds invented in those years was made again.
  - **Every made thing of the late centuries is an old kind.**
- **7, own goals: not measurable in v11.** A lesson's puzzle almost never starts as large as a person's own surprise
  (2 of 29,745 in the matching range).
- **10b, cumulative culture: inventions almost never build on what the inventor learned from someone.**
  - Only 35 of 3,989 new nested kinds (0.9%) use a part the inventor was taught, copied or read. That is less than the
    taught share of their repertoire (−0.038).
  - **Secondary:**
    - holders per new kind: mean 1.18, median 1;
    - 67% of alive kind-years are kinds that outlived their first maker; these are the old, well-shared kinds;
    - the deepest known kind per adult fell from 2.92 (years 100–125) to 2.45 (years 175–200);
    - 69% of new nested kinds beat their best part on its best use.
- **10a, social learning (described):** recipe gains are made 69%, taught 12% (plus 6% taught with an error), read
  from marks 9%, heated by chance 4%.

## Against the prior (the assistant's, frozen)
- **Positive contrast for C3, C9 and C12:** C9 and C12 **right**. C3 **wrong**: the contrast was negative.
- **Inconclusive for C4, C5, C6, C7 and C10b:** C4, C5, C6 and C10b **right**. C7 came out **not measurable** rather
  than inconclusive.
- **The picture** ("individual learning, honest communication and stable individuality, but little evidence of
  goals, planning or building on others"): **mostly right.** The learning rule's effect did not show as predicted.

## What it means for Bob (the assistant's reading; the creator decides)
- **ACL's people today:**
  - **Strong:** passing true information about the world, and having stable personal styles.
  - **Weak:** goals and planning cannot be told apart from the written pulls, or cannot be measured at all.
  - **Missing:** cumulative building. Late inventions are never taken up, and new kinds rarely build on others'.
- **The clearest gap for a cumulative mind is uptake.** New things are made once and never made again, by the inventor
  or anyone else, and inventions rarely build on what others taught. KL1 found most know-how dies with its one holder.
  SC1 adds that late inventions are not taken up at all. **Why is open.** A thing's value comes from using it
  (`judge_item`). A remake needs a value above 0.05 and the parts in hand (`mind.decide`), and lessons offer only things
  valued above 0.15.
- **Possible next questions for the council** (each a frozen study first; nothing changes without the creator):
  1. **Why is a new kind never made again?** A read-only audit of the make choice for new kinds: value never proven,
     parts not in hand, or the 3-item limit. Uptake is the first link in any cumulative chain.
  2. **The C3 puzzle:** why are experienced habits more spread around what follows? (Read-only, from existing data
     where possible.)
  3. **Relevant memory retrieval and working memory,** missing by the code (round 46): candidates for a later
     nature-change test, chosen by the creator.

## Blind recompute (`recompute_sc1.md`)
- **GPT** (chat `6ae86e86`) recomputed every primary contrast from the per-world sums, blind, with the prompt written
  before the data. **It matches every point value and every label**; interval ends differ by at most 0.0025.
- **Gemini:** Flash could not run its code tool (four attempts in three chats). **Gemini 3.1 Pro** then recomputed it
  in a fresh chat (`1f6d665aeec0d48a`) and **matches every point value and reading**. It called C7 "not measurable" and
  also labelled it "inconclusive"; no number differs.
- **SC1 is final.**

## Addendum (2 November 2026, about 07:50): what happens to a new kind (exploratory; outside the frozen plan)
`explore/check_new_kind_fate.py` (`explore/check_new_kind_fate.json`) replays world 22001 to year 130 and follows the
66 kinds invented in play in years 100–130. **One world, described only:**

| fate | kinds |
|---|---|
| dropped at once: the inventor already held 12 recipes, and a new kind starts at value 0 | 14 (21%) |
| kept | 52 |
| — the made thing was used | 47 |
| — its value rose above 0.05 (the make choice's floor) | 41 |
| — still held at year 130 | 45 |
| — lost when the inventor died | 6 |
| — dropped later | 1 |

**So the 12-recipe cap explains only part of the zero.** Most new kinds are kept, used and valued, and still nobody makes
them again. The block must lie in the make choice itself, which offers only the single most valued recipe that the
person can make and is not already holding (`mind.decide`). Possible blocks:
- the person is still holding the one they made;
- the parts are not in hand (a nested kind needs made parts, and only 3 things can be carried);
- an older kind is valued more;
- "make" loses to other actions.

**This is a lead for UP1, not a finding.**
