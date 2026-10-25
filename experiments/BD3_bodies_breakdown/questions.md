# BD3 — What in a body keeps more people alive? A breakdown of the bodies' remaining gain (SIGNED OFF 24 October 2026; frozen as `BD3-frozen` before any code or data)

**Why.** BD2 found that with realistic rot (now nature v6), worlds where the dead leave bodies hold **+7.7% more
people** over 120 years than worlds where the dead vanish (95% interval +2.3% to +13.4%; 512 paired seeds), though
not measurably fewer extinctions. With rot so fast, the cause is not settled. BD1's exploratory breakdown (64 seeds,
slow rot, after the results) pointed to disgust at rot, but that was on v4's two-year rot, where the living met
rotting bodies sixteen times more often. GPT advised this breakdown before TG1 (`../BD2_realistic_rot/gpt_view_after_bd2.md`;
`../../docs/gpt_handoff_2026-10-24.md`), with GPT's strongest suspicion that avoidance changes where people spend
their time (a hypothesis).

**Why it matters for the road ahead.** Nature v6 now includes bodies. If its gain comes from a mechanism we
understand (people learning from what they find on the land), that is a real channel of experience worth keeping and
building on. If it comes from something nobody meant (food that sits where the dead fall, a side effect of
bookkeeping), we should know before more is built on it.

**What it can and cannot say (GPT's point, adopted).** Removing one part while the rest stay on answers "what changes
when this part is gone". It does not by itself say how much of the gain each part causes alone: parts that depend on
each other can each show a large removal effect. Shares are therefore described, not tested.

## What a body does in nature v6 (read from the code, `acl/biology.py` `_leave_body`, `bodies_week`; `acl/actions.py` `_take`, `_ate_from_body`; `acl/mind.py` take options)

When a person dies and a body stays (`bodies_stay` = 1):

| part | what it does in v6 | what happens instead with no bodies (v3) |
|---|---|---|
| **eat** | the body's meat (18 food for an adult, less for a child) lies where they fell as food anyone hungry may take (the scruple for taking from the dead is low); rotten meat makes the eater ill 30% of the time | no meat |
| **carried** | if no relative took it at death, the food and seeds the dead carried lie with the body in the same store, still "theirs", rotting as stored food | it goes into the tile's plants, foraged by anyone |
| **foul** | each week a body is rotten (40% of the flesh gone by warmth), anyone 3 years or older within one tile finds the place foul (place memory −0.3) | nothing |
| **seen** | anyone close to the dead who did not yet know of the death learns it from the sight, with grief and the usual reactions | they learn only by the other channels |
| **tools** | if no relative took them at death, the dead's tools stay with the body until a partner or grown child stands there and takes them | the tools are gone |
| **bones** | when the flesh is gone, a "bones:person" trace is left on the land | nothing |

Meat and carried food share one store entry (`tile.stash`), and a hungry person's choice to take from it is scored
on the whole amount. So the switches below must separate them by source.

## Design

- **Code:** `code_bd3` = `code_v6` + five switches, each default 0 (= nature v6 exactly), plus a read-only record of
  each body store's two sources (meat, carried), kept beside the store and updated as it rots and is eaten (eating
  takes from both in proportion, as now). Plus BD1/BD2's read-only body logging and the new measures below.
  - `bd3_no_eat`: **only the meat** cannot be taken; the carried food can, as in v6. The take option is scored on
    the takeable amount only, so a store of meat alone draws nobody. The body still rots, is foul and is seen.
  - `bd3_no_carried`: what the dead carried goes to the tile's plants (as with no bodies); the meat stays.
  - `bd3_no_foul`: no disgust at rot.
  - `bd3_no_seen`: no learning of a death from the sight of a body.
  - `bd3_no_tools`: the tools are gone at death (as with no bodies).
- **Arms (9):** **F** (v6), **N** (v6 without bodies), **F−eat**, **F−carried**, **F−foul**, **F−seen**,
  **F−tools**, **F−eat−carried** (both food parts off: for the interaction GPT advised), and **F−all** (all five
  off). F−all still has a body that lies there, rots and leaves bones. **F−all against N is reported as "what remains",
  not as "the bones"**: before the run, the code is searched for everything else that still reads a body (listed in
  the zero-check record); a remainder is itself a finding.
- **Seeds:** **1,024 new seeds, 15001–16024**, used by no study; 20 founders, 120 years. **9,216 worlds** on GitHub's
  machines (`cloud-run`; the repository is public, so the minutes are free; roughly 10 hours). Fixed now; no
  extension after seeing results. *Why 1,024:* BD2's interval at 512 was about ±5.5%; at 1,024 F/N should be about
  ±3.9% if variance is similar. That may still be too wide to settle parts of 1–2%; such parts will read
  "inconclusive", and that is reported as it is.
- **Zero checks (hard stops):**
  1. With every switch 0, `code_bd3` gives **exactly** `code_v6`'s worlds: full state hash and random-number state,
     seeds 11 and 501 at 5 years, 501 and 601 at 20.
  2. Observers, logging and the source record change nothing in all nine arms; reload exact.
  3. **Source unit tests:** mixed stores, partial takes, rotten meat, a relative reclaiming at death, and conservation
     (in `no_carried`, food leaving the dead equals food added to plants).
  4. Each switch acts (below).
- **Manipulation check (hard stop), absence and opportunity:** in each F−x arm the part's events are 0 (meals of
  meat; food left with bodies; foul person-weeks; deaths learned by sight; tools taken from bodies), **and the
  opportunity was there**: bodies with meat, bodies with carried food, rotten bodies with people within one tile,
  close ones in sight of a fresh body, and bodies with tools are all above 0 in that arm.

## Primary: time-averaged population (the mean of the 12 ten-yearly counts, 0 after dying out)

All arms are bootstrapped **together by seed** (10,000 resamples of the 1,024 seeds; each resample carries all nine
arms).

1. **The gain on fresh seeds (gate):** F / N − 1, 95% interval. If its lower bound is not above 0, BD2's gain did not
   replicate, and everything below is described only.
2. **Each part (five comparisons, Holm-corrected across the five):** for each part x, **F / (F−x) − 1**, with its
   Holm-adjusted interval:
   - wholly above +2%: "**carries a meaningful part of the gain**";
   - above 0 but reaching below +2%: "**carries part of the gain; size uncertain**";
   - wholly below 0: "**works against the gain**";
   - wholly inside −2% to +2%: "**small, if any**";
   - anything else: "**inconclusive**" (never read as "no effect").
   The ±2% is relative change in time-averaged population, with (F−x) as the denominator, about a quarter of BD2's gain.
3. **Described, not tested:** each part's share of the gain, (F − F−x) / (F − N), with its interval (shares need not
   add up); the **eat × carried interaction** F − F−eat − F−carried + F−eat−carried; and **F−all against N**.

**Survival (secondary):** died out by year 120 in each arm. Each F−x against F: paired risk difference, discordant
pairs, and exact McNemar test (the same as the sign test on discordant pairs used in BD1 and BD2).

## Described measures

- **Food:** meals from bodies by source (meat, carried), fresh or rotten, by kin or not, and the eater's hunger;
  illness from rotten meat; food from the dead added to plants (F−carried, N).
- **Avoidance (GPT's hypothesis), measured directly:** foul exposures and the place-memory penalties actually
  applied; among people who met a foul body, how often they are back within one tile of it within 4, 14, 52 and 104
  weeks, against the same in F−foul for people who stood as close to a rotten body without the penalty; and when
  such a place is among a person's move options, how often it is chosen. By weeks since death (0–4, 5–14, 15–52,
  53–104). Movement is the possible mechanism, so it is never adjusted out of the primary.
- **Kin and bodies:** visits by partners and children to a body; tools taken; how long after death.
- Deaths by cause; median population at years 60 and 120; foul person-weeks; deaths learned by sight.

## What this study does not decide

Nothing here changes nature. Every switch is a probe. A part found to carry the gain is not removed or strengthened
by this study; any change to v6 would be a separate proposal, for the creator.

## The assistant's prior (before any data)

- F / N stays positive, about +6%.
- **Removing meat (F−eat) gives the largest drop** (meat feeds the hungry nearby in bad weeks).
- Foul: small at realistic rot. Seen and tools: "small, if any". Carried: small, either way.
- If F−foul gives the largest drop instead, GPT's avoidance suspicion and BD1's exploratory reading hold even at
  realistic rot speed, and the avoidance measures should show it.

## Revision 1 (24 October 2026, before any code or data)

After GPT's review (`gpt_review_bd3.md`), adopted: meat and carried food separated by source, and the take option
scored on what can be taken; F−all read as "what remains", with the code searched for other body effects; readings
reworded (inconclusive is not no effect); Holm correction; joint bootstrap by seed; McNemar for extinction;
manipulation checks for opportunity as well as absence; exact parity of switches-off with v6 (state and random
numbers); direct avoidance measures; and a ninth arm, F−eat−carried, for the interaction. Not adopted: add-one arms
(not needed until the leave-one-out results are in).

## Sign-off (24 October 2026)

The creator: "yes go ahead, freeze it and run", on Revision 1 as written (1,024 seeds, nine arms). Frozen as
`BD3-frozen` before any code or data.

## Operational amendment 1 (24 October 2026, while building, before any data)

The zero check "each switch acts" was run on seed 501 only. There, `bd3_no_eat` left the world identical, because in
that world's first 20 years nobody ate from a body (0 meat meals; seed 601 had 2, seed 11 had 1): the switch had
nothing to act on, which is not a fault. The check now asks that each switch change the world on **at least one of
seeds 501 and 601** (20 years). Nothing else changed; the source tests already show that no meal takes meat in F-eat.

## Operational note 2 (24 October 2026, while building, before any data)

- **The two sources of a body's food** are not kept in a separate record: they are read from v6's own accounting
  (`biology._rot_by_warmth`), where a body's flesh is what warmth has left of its meat, capped by the store, and the
  rest is what the dead carried. So in v6, a meal from a body takes the carried food first. `bd3_no_eat` blocks only
  the flesh, and a hungry person's take option is scored on the takeable amount (a body with only flesh left is not
  an option at all). A meal of carried food alone does not make anyone ill (illness is from rotten meat).
- **What F-all still has (searched in the code before any data):** the body's store still exists on the tile, so a
  passer-by can notice "food" at that place (`marks.around`) and it counts as a store in a place's situation
  (`stage.py`); storms and floods wet it as any store; when flesh is gone a "bones:person" trace is left, which can be
  noticed like other traces (`marks.py`). Anything F-all against N shows comes from these, or from something not found.
- **Running on GitHub:** 9,216 worlds in 120 chunks of about 77 (BD2's chunks of 77 took about 100 minutes), at most
  20 at once.
