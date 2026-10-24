# BD2 — Bodies with realistic rot: does the bodies effect hold when the dead rot as fast as real ones? (SIGNED OFF 24 October 2026; frozen as `BD2-frozen` before any data)

**Why.** BD1 found that when bodies stay, fewer worlds die out (146 vs 189 of 512) and population is 19% higher; a
labelled exploratory breakdown put the gain on disgust at rot. Bodies were adopted into nature (v4). But in v4 (and v5)
a body rots at the rate for stored food (4% a week): about two years to bones. Real bodies go to bones in weeks to
months in warm weather and far slower in cold. GPT advised running this next, before "things on the ground"
(`../DG1_digging/gpt_view_after_dg1.md`): primary, time-averaged population; a margin and a survival criterion frozen
first; a "no bodies" reference optional; do not keep the new rule merely because a test passes.

## The candidate (one setting, `body_rot`, default 0 = nature v5 exactly)

- **A body's flesh rots by warmth:** each week the flesh loses (degree-days that week) / 1,300 of its starting
  amount, where degree-days = 7 × max(0, °C). So in 20 °C weather a body is bones in about nine weeks; at 5 °C in
  about 37; in frost it hardly rots. **Anchors:** forensic work showing decomposition follows accumulated temperature
  (Megyesi, Nawrocki and Haskell 2005, *J Forensic Sci* 50:618–626; abstract read via PubMed: accumulated
  degree-days account for about 80% of the variation in decomposition). The figure of 1,300 degree-days to bones is
  the assistant's assumption, of the order used in that literature (the abstract does not give it); it is fixed now
  and never tuned.
- **ACL's temperature in °C:** 50 × felt − 7.5, where felt is ACL's own temperature (tile + season, minus a hard
  winter). So ACL's "comfortable" (0.45) is 15 °C and its "hard winter week" (0.15) is 0 °C. An assumption.
- **Rotten** by v5's own definition: once 40% of the flesh would have gone (here, 520 degree-days).
- What the dead carried rots as stored food does (v5); eating takes from both alike. Everything else as v5.

## Design

- **Code:** `code_bd2` = `code_v5` + `body_rot` (`v5_to_bd2.diff`), with BD1's read-only body logging.
- **Arms:** C (v5: bodies rot as stored food), R (v5 + realistic rot), **N (v5 without bodies: the reference GPT
  called optional; it stands in for v3's "no bodies" on today's nature)**. **Seeds: 512 new, 14001–14512**; 20
  founders, 120 years; 1,536 worlds on GitHub.
- **Zero checks (hard stops):** `body_rot` 0 = `code_v5` (seeds 11 and 501 at 5 years, 501 and 601 at 20); R acts;
  observers and logging change nothing in all three arms; reload exact.
- **Manipulation check (hard stop):** in R, the median weeks to bones is under half of C's, and foul person-weeks per
  person-year are under half of C's.
- **Primary: time-averaged population** (the mean of the 12 ten-yearly counts, 0 after dying out), two readings:
  1. **R against C** (what realistic rot does): R / C − 1, 95% bootstrap over paired seeds; "no meaningful effect"
     inside ±5%; "R lower" if the upper bound is below −5%; "R higher" if the lower bound is above +5%; else "not
     shown".
  2. **R against N** (does bodies' gain hold with realistic rot?): "the gain holds" if the lower bound is above 0;
     "no gain" if the interval is inside ±5%; else "not shown".
  C against N is described (BD1 again, on v5).
- **Survival (major secondary):** sign test, bootstrap, yardstick ±0.117, for R against C and R against N.
- **Described:** weeks to bones, foul person-weeks, meals from bodies (rotten, kin), deaths by cause.

## The adoption rule (fixed now, before any data)

Realistic rot is **proposed for nature (v6) if the manipulation check passes**, because it is the truer physics. What
it does to population and survival is reported, not used to accept or refuse it: a rule that kept the unrealistic rot
because it helped would be tuning nature toward an answer. The creator decides.

## The assistant's prior

- Realistic rot cuts foul exposure several-fold, and **most of BD1's gain disappears**: R lower than C (about −8%),
  and R against N "not shown" or "no gain".
- If so, v4's bodies gain was mostly an artefact of the slow rot; bodies would stay in nature for their truth, not for
  their benefit.

## Sign-off (24 October 2026)

The creator: "yes" to GPT's answers (adopt digging; then BD2 with GPT's design). Taken as sign-off of BD2.

## Operational note (24 October 2026, while building, before any data)

A throwaway check (seed 9971, 25 years, not data): median weeks to bones 124 with v5's rot, 12 with realistic rot;
foul person-weeks 2,947 against 159. Nothing was changed after it.
