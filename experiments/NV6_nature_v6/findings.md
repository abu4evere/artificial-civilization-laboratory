# NV6 — Nature version 6: realistic rot for bodies (built and checked)

**The creator's decision (24 October 2026):** "yea lets put realistic rot into nature", after GPT's advice
(`../BD2_realistic_rot/gpt_view_after_bd2.md`: adopt for fidelity, not for population; label it an approximation).
BD2 met its frozen rule (the manipulation check). Its cost is recorded: against v5's slow rot, population is 10%
lower and more worlds die out (177 vs 144 of 512); against no bodies at all, population is still 7.7% higher.

**v6 = v5 + `body_rot`:** a body's flesh rots by accumulated warmth (degree-days), bones at 1,300 degree-days.
**This is a temperature-based approximation, not full decomposition** (GPT): moisture, insects, exposure and burial
are not modelled, and 1,300 is the assistant's assumption, not a published threshold (Megyesi et al. 2005 relate
scored decay stages to degree-days; they do not give a single number for bones). `code_v6` is `code_bd2` unchanged;
the difference is `v5_to_v6.diff`.

## Checks (`zero.txt`, `run_nv6.py zero`): **All PASS**

- `code_v6` with `body_rot` 0 equals `code_v5`; v6 equals `code_bd2`'s R arm; the live package `acl/` with its own
  defaults equals v6; body_rot acts; reload exact.
- New reference fingerprints "v6"; the live package's regenerated. All 61 tests pass.

## From now

Future studies run on v6; BD2's R worlds (seeds 14001–14512) are the first v6 control set. Next (GPT): a breakdown of
what causes bodies' remaining gain (frozen first), then things on the ground (TG1) and water (WA1). Tag `nature-v6`.
