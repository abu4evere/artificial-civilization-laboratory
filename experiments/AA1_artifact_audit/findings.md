# AA1 — Do ACL's people exploit flaws in the simulation? Findings (12 October 2026)

Frozen as `AA1-frozen`. Read-only: a logging copy of the control code (`code_aa1`). In every world the state hash was
identical with and without the logging, and the code fingerprint (`e2d3e1d8…`) was unchanged before and after.
Discovery: seeds 501–516 (56,555 person-years). Holdout: 601–616 (43,200). 120 years each. The discovery reading
(`findings_discovery.md`, tag `AA1-discovery`) was written and committed before the holdout ran. Numbers:
`results_discovery.md` and `results_holdout.md`, both from `analyse_aa1.py` (frozen, unchanged).

## The frozen reading: material if at least 5% in discovery and holdout

| | shortcut | discovery | holdout | intended? | reading |
|---|---|---|---|---|---|
| **A1** | corner crossings, share of all water crossings | 82.9% [12.5–92.5] (21,452 of 25,866) | 30.2% [3.2–58.3] (1,325 of 4,387) | **no** | **material, unintended** |
| A2 | wrapping-edge crossings | 0.0% (0 of 25,866) | 0.0% (0 of 4,387) | yes | below 5% |
| A3 | food foraged from the dead, share of wild food | 0.0% | 0.0% | unclear | below 5% |
| **A5** | "go to" moves toward an out-of-sight loved one | 30.7% [29.2–32.1] | 29.4% [27.2–31.4] | not stated | **material** |
| **A6a** | food given on the receiver's exact food, share of wild food | 13.8% [12.5–15.1] | 13.3% [10.8–15.5] | not stated | **material** |
| A6b | food stolen on the victim's exact food | 0.0% | 0.0% | not stated | below 5% |
| **A6c** | partner-search moves toward someone beyond sight | 56.6% [52.7–61.2] | 56.3% [53.1–60.4] | not stated | **material** |
| **A6d** | dryness judgements resting on water beyond sight | 6.6% [5.9–7.3] | 7.0% [5.8–8.2] | not stated | **material** |

**Discovery and holdout agree on every shortcut.**

- **One is unintended: A1.** Water is meant to stop anyone without something that floats.
- **Four are "not stated": A5, A6a, A6c, A6d.** No written rule says whether people may know these things. N8 found no
  evidence that real people track where absent acquaintances are.
- **Negligible: A2** (intended, and never over water), **A3** and **A6b**.

## A1 is concentrated, not general (descriptive)

- Corner crossings occur in **11 of the 32 worlds** (6 in discovery, 5 in holdout).
- Within those, a few worlds carry almost all of them: 503 and 510 hold 20,499 of discovery's 21,452; 613, 614 and 615
  hold 1,248 of holdout's 1,325.
- In such a world, a corner gap joins two inhabited stretches of land, and people cross it as part of daily life. In
  the other two-thirds of worlds the shortcut does not occur at all.
- So the honest summary: **about one world in three has a hidden land bridge, and where it has one, most crossing uses it.**

## The information shortcuts are general

A5, A6a, A6c and A6d are in every world and steady across both sets:

- **A5.** About **30%** of all "go to" moves aim at a loved one the person cannot see, about 6 tiles away. That is two
  thirds of all moves toward loved ones. The person walks toward where that loved one is *now*, which nobody in the
  world could know.
- **A6c.** Over **half** of partner-search moves go toward someone beyond sight.
- **A6a.** About **13%** of all wild food passes as gifts, sized on the receiver's exact stores.
- **A6d.** About **7%** of dryness judgements use water the person cannot see.

## What they could touch (frozen question 3; read-only list)

| shortcut | findings whose measures could include it |
|---|---|
| A1 | contact between founding bands meant to be on separate islands (MB1a; the book's "Two Peoples Who Never Met"); partner supply and extinction where a bridge joins settled land (F1, WS1); group fluidity (GF1). Only the worlds that have such a bridge. |
| A5 | couples and families staying together across distance (C1, GF1, MC1, MC1-L); ID1's relationships |
| A6c | partner search and pairing (F1, F2, P2, N8, WS1): every study of why worlds die out |
| A6a | giving and sharing (the HF series, G1) |
| A6d | where people go when it is dry |

**What this does not say.** None of these is shown to have *changed* a finding. A shortcut can be large and still leave a
comparison between arms unchanged, because every arm has it equally (all of WS1's arms, for example). Whether removing
any one would change a result is a separate, controlled question.

## Priors (written before any run) against the result

- **Assistant: "A1 happens, perhaps often."** Right, but concentrated in about a third of worlds.
- **"A2 is rare."** Right: none over water.
- **"A3 is small."** Right: about 0.05% of wild food.
- The information shortcuts (added at sign-off) had no prior. They are larger and more general than A1.

## For the creator (nothing is fixed here)

As frozen, a material unintended shortcut goes to the creator; any fix is a **new version of nature**, compared against
the original, which is kept. Decisions to take:

1. **A1** (unintended): treat it as a flaw to fix in the new version? (For example, a diagonal step is allowed only if at
   least one of the two side tiles is passable, so water that touches only at a corner still blocks.)
2. **A5, A6c** (not stated, large, at the heart of partner finding): should people know where absent others are? The
   alternative N8 points to is that people remember where they last saw someone. Because these touch every study of
   extinction, a fix should first be tested as its own controlled comparison, not folded silently into a new baseline.
3. **A6a, A6d** (not stated, moderate): keep as intended "knowledge of those close by", or limit to what is in sight?
