# E11 — Stories that carry a hard season (O4): candidates (design document, not frozen)

**Written:** 2026-10-06, after E9.4. No E11 code exists. For the creator to choose from; the chosen version will be
frozen in a pre-registration before any code is written.

## Why

E9.3 and E9.4 measured a self-erasing lesson: a person's lesson about winter is learned from going short, preparing
stops them going short, and the lesson then falls below the threshold (about 0.4) at which anyone prepares. Whatever
keeps a lesson alive must outlast the experience that taught it. The creator's question: can the same channel that
preserves social memory preserve ecological memory?

## What already exists (pilot, read-only, `run_o4_pilot.py`)

In four control worlds over 120 years, 166 of the 195 deaths from starvation were told as stories: 55,489 tellings,
about 15% of all storytelling. Each was accepted by a median of 26 people (up to 87), and told a median of 10 years
after the death (90th percentile 26 years; the longest 53). The channel is large and long-lived. But a death memory
records who died and where, not what they died of or in which season, so none of this teaches anything about winter.

## The rule every candidate must keep (the creator's)

Stories carry **experiences**, never instructions. Allowed: "she died of hunger", "in the cold season", "we were
hungry when the cold came". Not allowed: "store food", "make a carrier", "winter is coming". The story provides
memory; the existing anticipation machinery (E10's season-ahead pull toward food) provides behaviour. Nothing else
changes.

## Candidates

### S1 — Death stories carry cause and season (recommended)
- **Change:** a memory of a death also records the cause and the season it happened in (both are already in the
  death event). When retold, they travel with it, and can be misremembered like everything else in a story. A listener
  who accepts a story of a death from hunger in season s gets a lesson for s: `expect["loss@s"]` raised to at least
  STORY × (their credence in the teller) × (the story's strength).
- **What it does not change:** nothing is said about storing, tools or what to do. The lesson uses E10's expectation,
  fading at grief's rate, felt a season early only in the pull to get food.
- **Why it might work where E9 and E10 did not:** the lesson is renewed every time the story is heard again, whether or
  not anyone is hungry now; stories are told for decades.
- **Risk:** stories are chosen by how much they matter to the teller; deaths of distant people may be told less.

### S2 — S1, plus rehearsal
- **Change:** telling a hunger story also renews the teller's own lesson for that season, as telling already renews
  the memory itself.
- **Why:** a story kept alive by telling keeps its lesson alive in the teller too; this is how memory works in the code
  already.
- **Risk:** two changes; better as a second arm beside S1.

### S3 — Hunger itself becomes a story
- **Change:** going short of food in a season leaves a memory of it ("we were hungry when the cold came") that can be
  told, so non-fatal hardship travels too, not only deaths.
- **Why:** most hard winters kill no one; their lesson would otherwise die with those who lived them.
- **Risk:** creates a new kind of memory; the most new machinery of the three.

## Numbers to fix before freezing (no precedent in the code)

- **STORY**, how strongly an accepted story of a hunger death teaches, compared with losing one's own child (1.0) and
  witnessing a death (E10: 0.25 and 0.50). Following the creator's E10 rule, it should be tested at two values rather
  than guessed once, for example 0.25 and 0.50.

## Suggested arms (for the creator to decide)

Control; **O2 + S1-low**; **O2 + S1-high** (story strength 0.25 and 0.50), all on E10's code and machinery, so the
comparison with E10's O2 arm isolates what stories add. S2 and S3 only after S1 shows whether stories can carry the
lesson at all.

## What success would mean, and the leak test

The causal links in the creator's order: autumn foraging of people who heard a hunger story but never went short
themselves; food entering winter; carers holding 20+; carrying-limit hits; carriers made. Then deaths. And the key
new measure: **does preparation persist across years**, measured as the share of planners who plan again (E9.3: 1 in
113). Leak test (hard fail): people who never heard such a story, never lost a child and never went short behave as
in the control.
