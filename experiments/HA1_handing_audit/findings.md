# HA1 — Why does handing stay rare? Findings (final: recomputed blind by GPT and Gemini; see the end)

**Read-only: no change to nature.** Live v11 (`code_v11`). Frozen as `HA1-frozen`. Signed off by the assistant (GPT
97%, Gemini 96%, the assistant 80%; debate round 43). Run on GitHub Actions (run 41365641251). The zero checks ran on
the cloud, since the creator was using the PC (`zero_cloud.log`). 32 worlds, seeds 21601–21632; LP (80 founders,
80 × 80), 200 years; years 100–200 counted. Every number comes from `analyse_ha1.py`, written before data and tested on
a smoke world. Full tables are in `results.md`.

**Validity:**
- zero checks pass (observer read-only; same `code_v11` fingerprint);
- all 32 worlds are present;
- **every handing came from a decision the observer saw with a handing option to that receiver** (mismatches 0);
- **the instrument agrees with the world:** expected handings (the summed choice probability) 59,144 against 59,178
  handings done.

**Population beside it:** live v11 worlds; handings per adult-year 0.190 (HD1's h arm: 0.20).

## The answer
**Opportunity-limited, by the frozen rule.** Among 15.6 million decisions by people holding a made thing:

| quantity | value [95%] |
|---|---|
| **E:** share with at least one handing option | **0.071 [0.067, 0.075]** (below 0.10) |
| C: mean choice probability of handing, given an option | 0.053 [0.050, 0.057] |

### Where the funnel narrows (secondary, described)
| stage | share of decisions |
|---|---|
| someone within reach has room | 0.985 |
| **someone would gain more than the giver loses** (net > 0) | **0.078** |
| a handing option exists | 0.071 |

- **The narrow point is the net gain, not company or room.** People are almost always near someone with room. But
  only rarely does a holder carry a thing that would help a neighbour more than its loss would cost the holder: the
  neighbour already has as good, or the holder needs it.
- **By the giver's age:**
  - Adults (16+), given an option, choose it with probability 0.025. Their best handing option scores 1.24 below
    their top option.
  - Children choose it with probability 0.215; their gap is 0.58.
  - So for adults the choice is also narrow. The pooled C is lifted by children.
- **By relation:**
  - 76% of handing options are to non-kin, non-partners.
  - But kin draw 52% of the choice probability and 52% of the handings (the social weight favours kin).
  - Partners: under 1%.
- **Who holds made things:** adults 16–59 hold 67%, children under 12 hold 17%, 60+ hold 10%.

### Knowledge does not travel with the object (secondary; an association, GPT)
| receiver | handings counted | made that kind within 5 years |
|---|---|---|
| did not know how to make it | 37,569 | **0.1%** |
| already knew how | 19,686 | 5.1% |

Two thirds of handings go to people who cannot make the thing. Almost none of them later make it.

## Against the prior (the assistant's, frozen)
1. "Choice-limited": **wrong.** Opportunity-limited by the rule, though adults' own choice probability (0.025) is also
   low.
2. "Most handing options and handings are to kin and partners": **half right.** Handings 52%, yes; options 24%, no.
3. "Receivers who did not know the kind rarely make it (under 10%)": **right** (0.1%).

## What it means
- **Handing is rare mostly because there is rarely a gain to hand.** In v11, a made thing moves only if it helps the
  receiver more than it costs the giver. Most of the time, the people nearby are as well equipped, or the holder
  needs the thing. When there is a gain, adults still seldom choose it over food and work. Children do more often.
- **Objects move, but knowledge does not.** Receiving a tool almost never leads to making one (0.1%). In ACL, a recipe is
  learned by making it oneself, by being taught, by watching someone make it, or by reading marks (`remember_recipe`
  is called with "made", "heated", "taught", "copied" and "read"). Holding the thing teaches nothing.
- **For Bob** (GPT, round 43: "transmitting knowledge matters more than transmitting optimistic values"): handing
  spreads use, not know-how. If minds are to build on what others learned, the path is how **knowledge** passes:
  watching, teaching and copying. That points the next step at knowledge transmission, not at more handing.
- **No change to nature** follows from this study.

## Independent recompute (1 November 2026)
GPT and Gemini, each in a fresh chat, from per-seed sums of the raw output only (`recompute_ha1.md`). **All three
agree:** E 0.0709 [0.0667, 0.0747]; C 0.0533; opportunity-limited.

**Final: opportunity-limited.**
