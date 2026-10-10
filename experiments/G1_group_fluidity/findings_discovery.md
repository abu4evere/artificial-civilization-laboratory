# G1 — Discovery reading (written before the holdout is run)

**Data:** F1's 64 control seeds, 120 years, read-only (`results_discovery.md`, from `analyse_g1.py discovery`). Valid:
observer read-only (seeds 601, 2601), code unchanged, all 64 reproduce F1's populations. Baseline: 22 of 64 died out.

## The frozen reading

Co-residence persistence (camp-radius groups, pooled): **P(12 weeks) = 0.807, P(104 weeks) = 0.777.** P(104) ≥ 0.5, so
by the rule frozen in `questions.md`: **ACL's groups are more fixed than forager bands (co-residence lasts years).** The
sensitivity measure (perception-radius groups) gives the same reading (0.975, 0.968).

## What the discovery shows (descriptive)

1. **The curve is flat.** Of adult pairs living together, 85% still are 4 weeks later, 81% after 12 weeks, 78% after two
   years. Almost all the change happens within the first month (most of it probably foraging trips that split a group
   for a few weeks), and after that co-residence hardly decays at all. The forager benchmark ("stable over months but
   not years") describes a curve that keeps falling over years; ACL's does not.
2. **Not an artefact of single-group worlds.** Only 7.9% of blocks have all adults in one camp-radius group (29.9% at
   perception radius); in blocks with two or more groups the reading is the same (P(104) = 0.763).
3. **Per world, the same.** Median across worlds P(104) = 0.670 (IQR 0.560–0.770): above 0.5 in most worlds. The pooled
   figure weights larger worlds more; the per-world figure is lower but gives the same reading.
4. **Seekers do not move more.** Pairs involving an unpartnered adult under 45 persist as long as other pairs (0.783 vs
   0.761 at two years). In ACL, the unpartnered stay where they are, like everyone else: consistent with P2's pilot.
5. Population beside it: about 17 adults per block on average (per-world median 15.8).

## Caps

- The benchmark is qualitative (Ache, Hill et al. 2014) and the 0.5 cut-offs are a reading of it, frozen beforehand,
  not an anchored number. The gap is anchored **in direction only**.
- Camp-radius groups computed weekly include short foraging separations; the 4-week majority rule damps but does not
  remove them. This makes ACL look *more* fluid, not less, so it does not weaken the reading.
- Nothing is changed in ACL by this result.

The holdout (seeds 2601–2664) is run next; the verdict stands only if it gives the same reading.
