# ID1 — What makes an ACL person who they are? (questions, DRAFT for the creator's sign-off; nothing frozen or run)

**Asked by the creator (October 2026),** from the idea "is memory the foundation of identity?". In ACL a person is made of
separate parts, each a different kind of state in the code. ID1 asks which parts make a person behave as **that** person.
It changes no rule of nature: it works on **copies** of worlds, never on ACL's own worlds, and the copies are discarded.

## What an ACL person is made of (from `acl/person.py`)

| part | in the code | what it is |
|---|---|---|
| **Temperament** | `genes` | eight inborn traits (curiosity, kindness, temper, …), fixed for life |
| **Habits** | `q` | the 32 × 19 table of learned habits (the brain scan's 608 connections) |
| **Memories** | `memories` | remembered events: births, deaths, gifts, attacks, pairings |
| **Relationships** | `rel` | affection, trust, familiarity, grudges toward each other person |
| **Know-how** | `recipes`, `itemval`, `skills` | what they can make, how much they value it, how skilled they are |
| **Beliefs** | `beliefs`, `expect`, `heard`, `records` | what they believe about practices and seasons, what they were told, whom they trust as a source |
| **Places** | `places`, `springs`, `sightings`, `shores` | where life has been good, water, animals, land across the sea |

The body (age, health, food, position) and family ties (partner, children) stay the focal person's own throughout.

## The method

Worlds are fully deterministic: a snapshot holds every number, including the random-number generator's state. So a
world can be copied and run forward twice from the identical moment. In one copy nothing is touched (the **original**);
in the other, one part of one person is replaced (the **swap**).

- **Focal person and donor:** in a control world at a fixed year, pick a grown person (focal) and another grown person of
  the same sex and similar age (donor). The focal person receives the donor's part.
- **Arms per focal person:** swap one part at a time (seven arms), swap everything except temperament (one arm), and a
  **sham**: the world perturbed by one random draw with the person untouched. The sham measures how much a person's
  behaviour changes just because the world's future has changed. Any change to any person makes everyone's futures
  diverge, so the sham is the yardstick.
- **Restore:** after the swap has run for a while, put the focal person's own parts back. Does their behaviour return?

## Questions

1. **Which parts move a person's behaviour away from who they were?** For each part: how far the focal person's actions
   drift from the original copy, compared with the sham.
2. **Which parts make them behave like the donor?** Do they become more like the donor than like themselves?
3. **Is temperament enough?** With everything swapped except temperament: do they become the donor, or stay themselves?
4. **Does restoring bring them back?** After restoring, does the behaviour return to the original, or have the weeks
   lived in between already changed them?

## Measures (definitions for the creator to approve)

- **Behaviour:** how often the person chooses each of the 19 actions over a window of weeks.
- **Drift:** difference between two people's action mixes (Jensen–Shannon divergence, 0 = identical, 1 = completely
  different), focal-swapped vs focal-original, against the same measure in the sham.
- **Pull toward the donor:** whether the focal-swapped person's action mix is closer to the donor's original mix than to
  their own original mix.
- Beside each: the world's population and the focal person's age, partner and survival through the window.

## Decisions for the creator

1. **Window:** behaviour over (a) 13 weeks, (b) 26 weeks, or (c) 52 weeks after the swap. Longer shows lasting effects but
   lets the world's chaos grow.
2. **Restore after:** (a) 26 weeks, or (b) 52 weeks.
3. **Sample:** focal persons in (a) 64 control worlds, 2 each (128), or (b) 32 worlds, 2 each (64). Runs are short (weeks,
   not 120 years), so either is cheap.
4. **Discovery and holdout (rule 15):** half of the worlds first, the reading written down, then the other half.
5. **When:** while WS1 is running (it would slow WS1 a little), or after WS1 finishes.

## What it cannot show

How human identity works. ACL's "memory" and "habits" are far simpler than a human mind. ID1 shows which parts of an
**ACL** mind drive behaviour, and whether swapping them changes who a person behaves as.

## Assistant's prior (written before any run; not a prediction to test)

Habits and temperament will matter most; memories (episodic) the least, because in the code memories mostly colour
feelings, not choices; restoring will mostly bring people back, but not completely, because the weeks lived in between
change their habits too. Held loosely.
