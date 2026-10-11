# GF1 — How fluid are ACL's groups? Findings

**Read-only** (questions frozen as `G1-questions`). Control worlds, 120 years, F1's group definition (people chained within
`camp_radius`, 2 tiles), co-residence in 4-week blocks (same group in at least 3 of 4 weeks). Discovery: F1's 64 seeds
(all reproduce F1's populations); holdout: 64 new seeds 2601–2664. Valid: observer read-only (state hash, seeds 601 and
2601), code unchanged in every run. Tables: `results_discovery.md`, `results_holdout.md` (from `analyse_g1.py`).

## Baseline (rule 14)

22 of 64 died out in each set (34%).

## The frozen reading, both sets

| | discovery | holdout |
|---|---|---|
| P(4 weeks): co-resident adult pairs still co-resident | 0.848 | 0.847 |
| P(12 weeks) | **0.807** | **0.806** |
| P(52 weeks) | 0.784 | 0.787 |
| P(104 weeks) | **0.777** | **0.782** |
| per-world median P(104) [IQR] | 0.670 [0.560, 0.770] | 0.654 [0.539, 0.777] |
| blocks where all adults are one group | 7.9% | 7.1% |
| sensitivity (perception-radius groups): P(12) / P(104) | 0.975 / 0.968 | 0.973 / 0.967 |
| mean adults per block (population beside it) | 17.1 | 17.1 |

P(104 weeks) ≥ 0.5 in both: by the rule frozen beforehand, **ACL's groups are more fixed than forager bands: co-residence
lasts years.** The holdout reproduces the discovery to the second decimal. The verdict stands (rule 15).

## What it shows

1. **A flat curve.** Of adults who live together, about 85% still do a month later, and about 78% two years later. Almost
   all the change happens within the first month (most likely foraging trips that split a group for a few weeks); after
   that, co-residence barely decays. Forager bands, by every account read in N9, keep their members "for months but not
   years" (Ache; Hill et al. 2014) and turn over substantially (Agta; Dyble et al. 2021).
2. **Not an artefact.** Single-group blocks are rare (7–8%); in blocks with two or more groups the reading is the same
   (P(104) ≈ 0.77); per-world medians agree; the wider group definition (perception radius) gives an even more fixed
   picture.
3. **The unpartnered do not move more.** Pairs involving a seeker (adult, unpartnered, under 45) persist as long as other
   pairs (0.786 vs 0.771 at two years). In ACL the single stay where they are, like everyone else: the same fact P2's pilot
   showed from inside the decision (the search rarely wins).

## Caps

- The benchmark is qualitative; the 0.5 cut-offs are a reading of it, frozen beforehand, not an anchored number. The gap
  is **anchored in direction only**: ACL's groups are more fixed than forager bands; by how much is not known.
- Weekly camp-radius groups include short foraging separations; this makes ACL look *more* fluid, so it does not weaken
  the reading.
- Nothing is changed in ACL by this result. Whether to act on it (and how, without a chosen number) is for new
  candidates, evidence and the creator's sign-off.

## Where this leaves the thread

F1: worlds die mainly because people cannot find partners. P2: single adults rarely search. N9: foragers visit and move
often, but no source gives how often. **G1: ACL's groups hardly mix at all over years.** The missing ingredient is
consistent from three sides: in ACL, people rarely meet anyone outside the group they already live with. **Next: the
creator decides** (for example, candidates for residential mobility between groups, with evidence first).

## Note added (rule 19), October 2026

This study was first named **G1**, but G1 was already the name of an earlier read-only study (`G1_who_receives`:
who receives the food that is given away). It is renamed **GF1**. Its git tags `G1-questions` and `G1-done` are kept
as they were; `GF1-questions` and `GF1-done` point to the same commits. Nothing in the study changed.
