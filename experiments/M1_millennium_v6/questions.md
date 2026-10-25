# M1 — A thousand years on today's nature: do they keep, lose, or build? (DRAFT, Revision 1, 25 October 2026, sleep mode; not signed off, not frozen)

**Why.** The creator's yardstick (24 October 2026): the first generations will hardly pass anything on, and that is
fine; but a world at year 1,000 must differ from its start, as human history does, with nothing handed to its people.
The mission (the creator's words): "to create a world with minimum laws and a period that produce an autonomous and
cognitive mind". The only millennium runs so far (E5, E6, E7) were on very early nature and showed **decline**: every
kind of thing appeared in the first 11 years; by year 1,000 best crafting skill was about a tenth of the founders',
known recipes fell four- to eightfold, deliberate making fortyfold (E7.6). Since then nature has changed (v2 no
shortcuts; v3 parts-first teaching; v4–v6 bodies, digging, realistic rot), and we learned that 20-founder worlds often
die out while 80-founder worlds rarely do. **No thousand-year run exists on today's nature.** GPT's design is the base
(`../../docs/gpt_view_millennium_2026-10-24.md`).

**What it is.** Read-only: nature v6 unchanged; observers only. It describes the trajectory and tests three separate
outcomes against frozen readings. It changes nothing.

**What it is not.** Not a test of intelligence. Following GPT: it distinguishes **historical persistence, independent
rediscovery and cumulative improvement**, and does not treat change over time alone as evidence of a growing mind.

## Design

- **Code:** live `acl/` at nature v6 (fingerprinted; `code_v6`), plus read-only observers: E7.6's sampler (skills,
  recipes held, making by decade), CA1's chain observer (each kind: first maker, learners, route, retained after its
  maker's death, generations), and new ones below. Zero checks: observers change nothing (state and random numbers at
  20 years, and once at 100 years on an LP world, for memory and logging over long runs); reload exact; the observers'
  memory use stays bounded over a 1,000-year smoke run.
- **Arms:** **LP**, 80 founders on 80 × 80 (primary: survived best in WS1, grows to ~110 by year 60; about 1.5–2 hours
  per thousand-year world, measured 25 October 2026); **D80**, 80 founders on 40 × 40 (secondary, descriptive: same
  founders, four times the density; about 35 minutes per world); **C20**, 20 founders on 40 × 40 (secondary,
  descriptive: today's standard world). **64 new seeds per arm, 16801–16864, the same in every arm**; 1,000 years;
  192 worlds on GitHub. LP's bands rarely meet (MB1a), so a decline in LP alone would not show v6 cannot keep
  knowledge; D80 is there to show whether density changes the answer.
- **Windows:** year 0 (founding snapshot); **early = years 20–50**; **late = years 950–1,000**; the whole trajectory
  every 25 years. The world is the unit; people within a world are not independent.

## Three outcomes, reported separately (no combined score)

**A. What they can do (functional capability).** Performance, not labels:
- A1: the best tool held by anyone alive, by its strongest use factor (`matter.factor`), and the median over adults of
  each person's best held factor;
- A2: the number of distinct uses (forage, hunt, cut, fight, carry, warmth) for which some living person holds a thing
  that helps (factor > 1);
- A3: best and mean crafting skill among adults (E7.6's measures);
- **A4: what they actually accomplish**: food per forage-week per adult and the share of it owed to tools (E8.2's
  measure, rebuilt as a read-only observer), set beside the food on the land within reach, so better land is not read
  as better skill. Holding a good tool (A1) is not using it well (A4).

**B. What they keep (retention).** For useful kinds (factor > 1) invented in each era: the share ever learned by
someone other than its inventor (CA1's first hand-over), and of those whose inventor has died, the share still known
by someone alive a generation (25 years) later. Plus recipes known at once (unique), and deliberate making per person
per decade.

**C. What lasts that nobody gave them.** Lasting novelty after year 100, each case checked against GPT's ladder
(new property combination → made again → better or different use → adopted by others → outlives its inventor →
improved again) so a duller copy (E7.5) never counts. **A tradition** (defined now): a technique, belief or mark held
by 3 or more living people in every 10-year sample for at least 50 years, with at least one recorded passing between
people (taught, told or read from a mark), and still held after everyone who held it at its start has died. Shared
marks (historian) are described, and not called language.

**The cohort test (GPT's "final test", observational; two views).** For everyone who reaches age 30: compare those born in years
0–50 with those born in years 900–950, on recipes known at 30 that are useful, the share of those learned from
others, the best tool factor they hold, and their crafting skill at 30. Does being born into a long history give a
person more than being born at its start? View 1: as lived (no adjustment). View 2, described only:
the same within comparable population, contacts, food and teaching chances during ages 0–30. Never read causally: these
are different people, and population may itself be a product of culture. The world stays the unit.

## Primary outcomes (named now, so no metric can be picked afterwards)

**Co-primary, LP:** (1) **B-retained**: of useful kinds whose inventor died, the share still known 25 years later
(only deaths followed by 25 years of observation count; this is GPT's decisive line, keeping against rebuilding from
scratch); (2) **A4**: food per adult forage-week owed to tools. Everything else is secondary.

## Frozen readings (late / early, per world, bootstrapped over worlds; LP primary)

For A1, A3 and B (first hand-over share and retained share): the ratio late ÷ early, 95% interval over worlds:
"**builds**" if the lower bound is above 1.10; "**declines**" if the upper bound is below 0.90; "**holds**" if the
interval lies inside 0.90–1.10; an interval wholly inside 1.00–1.10 is "**increase, below the meaningful margin**"
(and 0.90–1.00 the same for a decrease); otherwise "**unclear**" (never "flat"). Absolute changes are reported beside
every ratio. **Zero early values:** where a world's early value is zero, that world reports the absolute difference and
whether the thing is present late; no constant is added to make a ratio. C: count of ladder-checked lasting novelties after year 100,
described. The cohort test: late-born ÷ early-born, the same four readings. A trajectory class per world (GPT's list:
improvement with transmission; stable maintenance; stable by constant rediscovery; change without improvement;
erosion; extinction), assigned by rules written into the analysis before data.

**Two views, never mixed:** unconditional (all 64 worlds, with extinction and its timing; dead worlds have no late
window and are reported as extinct, not as zero capability) and conditional (worlds alive at year 1,000).
**Population beside every measure.** C20 is read the same way, described, not compared for a verdict.

## What would change the plan

- If LP keeps or builds (not "declines"): the next step is a causal test of how it keeps (GPT's order), and a
  10,000-year run only for a stated question.
- If LP declines: a study of loss (where retention breaks, with CA1–CA3's methods), not a longer run.

## The assistant's prior (before any data)

LP still **declines** on A3 (skill) and on deliberate making, but **less** than E7.6 (parts-first teaching and larger
bands); B "holds" (first hand-over stays about one in ten, as in CA1); A1 "holds" (the simple carrier and flake are
always re-found); C: no ladder-checked lasting novelty after year 100. Cohort test: late-born ≈ early-born ("holds").
Co-primary: B-retained "holds" at a low level; A4 "holds" (tools add little to food, as E8.2 found). D80: keeps a
little more than LP (bands meet). C20: many worlds extinct; survivors decline.

## Revision 1 (25 October 2026, sleep mode, before any code or data)

After GPT's review (`gpt_review_m1.md`): A4 (performance, not possession) added; co-primary outcomes named
(B-retained and A4); zero-baseline and censoring rules; traditions defined before data; "increase below the margin"
reading; D80 added as a secondary arm (192 worlds); two views of the cohort test; long-run observer checks.

## Sign-off

Not yet. Drafted in sleep mode from GPT's design; GPT's review to follow; the creator decides.
