# SA1 — How much do ACL's findings rest on numbers nobody anchored? (SIGNED OFF and frozen as `SA1-frozen`; nothing run)

**Why.** Law 126 (World Bible v8.2) requires every unanchored number a finding rests on to be **tested for sensitivity**,
and defines how: one value at a time, × 0.5 and × 2, on F1's 64 control seeds, 120 years; flag a value **sensitive** if
extinction changes by more than half of F2's effect. It has never been done. The NL1 register lists 85 settings, none
anchored. An outside review (October 2026) put a sensitivity audit above any new experiment. This is that audit, for
the settings the headline findings rest on most directly.

**Not tuning.** No value found here is adopted. A sweep result changes no setting of nature; it changes only how
strongly a finding may be stated ("rests on an unanchored value" is written beside any finding that does). Every arm is
reported, whatever it shows.

## The six settings (chosen before any sweep; all are settings in the frozen control code, so SA1 needs no new code)

| setting | value | what it does in the code (read 12 October 2026) | finding it bears on | × 0.5 | × 2 |
|---|---|---|---|---|---|
| `conception_chance` | 0.04 | chance per week that a couple living together conceives (1 use) | extinction (F1) | 0.02 | 0.08 |
| `perception` | 4 tiles | how far a person sees: partners, people, food, water, fire, threats (**14 uses**) | partners not found (F1, P2, AA1's A6c) | 2 | 8 |
| `reach` | 3 tiles | how far a person can travel and still act that week: every action's range (**29 uses**) | movement, meeting, separation (C1, GF1, MC1) | 1.5 → **2** | 6 |
| `camp_radius` | 2 tiles | how close partners must be to count as living together, and so to conceive (4 uses) | couples apart (C1), births | 1 | 4 |
| `mortality_base` | 1.5 × 10⁻⁵ | Gompertz scale: weekly risk of death at every age, × the base (1 use) | turnover, the reproductive window | 0.75 × 10⁻⁵ | 3.0 × 10⁻⁵ |
| `forage_base` | 12 | food a week of foraging brings before skill and tools (`mind.forage_rate`, used in the harvest and in choosing) | abundance, and why tools barely matter (E8.2: tools ≤ 2% of food) | 6 | 24 |

**Choices to note:**
- **Integer settings.** `reach` × 0.5 is 1.5, rounded **up** to 2 (a person must be able to move).
- **Ageing.** The ageing *scale* (`mortality_base`) is varied, not its *rate* (`mortality_rate`). Doubling the rate would
  halve how fast risk doubles with age (from 8 years to 4), killing almost everyone young. Doubling the scale is the
  same as being about 8 years older at every age.
- **Broad settings.** `perception` and `reach` act in many places at once. A change in them says the findings rest on
  sight or range *in general*, not on one rule.

## Arms and worlds

- **12 arms** (6 settings × 2 directions), plus a **sham** (one extra random draw, as in every study). Control code
  (`code_e13r`, `anticipation_weight = 1.0`, as F1).
- **Control:** F1's 64 saved worlds. Each run's control is checked first: F1's seeds are replayed under the control
  settings and must reproduce F1's saved populations exactly, or it is a hard stop.
- **Seeds:** F1's 64 (501–516, 601–616, 811–818, 1101–1124). Cost: 13 × 64 = 832 worlds ≈ **11 hours** on four workers,
  after LK1.

## Measures (population beside every measure)

- **Primary: extinction**, per arm against the control, paired by seed (exact sign test; effect = control extinction
  share minus the arm's, with a 95% bootstrap interval, 10,000 resamples, `random.Random(2026)`).
- **Secondary** (described, paired Wilcoxon):
  - population at year 119;
  - births per woman-year;
  - share of decisions blocked for want of a partner (F1's measure);
  - for `forage_base` only: **tools' share of foraged food**, by E8.2's measure (`E8_crucible/run_e82.py`, `Probe`: an
    upper bound, food foraged × (1 − 1 ÷ the best foraging tool's factor), adults only). **Checked 12 October 2026:**
    the probe reads only the world's `forage` events and each person's items through `matter.best_item`, both present
    unchanged in the control code, so it can run there. Its read-only status is confirmed in SA1's zero check (state
    hash identical with and without it) before any run.

## Reading (decision rules, as BL0's: they fix what each result leads to, and claim no truth)

Half of F2's effect on F1's seeds is **0.117** (F1: 22 of 64 died out; F2: 7).

- **Sensitive:** p < 0.05 and |effect| > 0.117. Every finding that rests on that setting is marked "rests on an
  unanchored value that moves survival strongly". The setting goes first in line for an evidence review (anchor it, if
  evidence exists).
- **Moves survival:** p < 0.05 and |effect| ≤ 0.117. Reported, with its direction.
- **No sign at this sample:** p ≥ 0.05. **Not** read as "robust". With 64 worlds the interval is about ±0.12, about
  the size of the threshold itself, so 64 worlds can find strong sensitivity but cannot show its absence. Proving
  robustness would need about 256 seeds per arm; that is a follow-up, if wanted, only for the settings that matter.
- **Multiplicity:** 12 comparisons. Holm-adjusted p-values beside the raw ones; a reading that does not survive the
  adjustment is marked so.
- **The sham** should not reach p < 0.05; if it does, every reading carries that caveat.

## What it cannot show

- Whether any value is *right*. Only evidence can show that (Law 126).
- How settings interact (one at a time only).
- The ~1,340 constants inside formulas; those need classifying first (Law 126, register).

## Decisions for the creator (before freezing)

1. **The six settings** as listed, or swap any.
2. **64 seeds as a screen** (as Law 126 states, recommended), or 256 from the start (about 4 × the time, ~44 hours).
3. **Order:** after LK1, before BL0 (recommended), or after BL0.
4. **Thresholds** as above (decision rules).

## Assistant's prior (written before any run; held loosely)

- `conception_chance`, `camp_radius` and `perception` sensitive: they sit directly on the partner-finding chain behind
  extinction.
- `mortality_base` moves survival in the obvious direction.
- `forage_base`: halving it raises extinction. Doubling it changes little, since food is already abundant (E8.2).
- `reach`: unclear, because it acts in 29 places at once.

## Sign-off (12 October 2026)

The creator: **"freeze SA1"**, after recommendations that matched the draft on every decision:

1. All six settings as listed.
2. **64 seeds as a screen**; a 256-seed follow-up only for settings that turn out sensitive or near the line.
3. **Run after LK1, before BL0.**
4. Thresholds as drafted (decision rules).

## Operational details (fixed at freezing, before any code)

- **Control re-run.** F1's saved outputs lack the E8.2 tool measure, so the control is **re-run**, not read: arm
  **C** = control settings, F1's 64 seeds, with the same observers as every arm. **Hard stop:** C's population at every
  decade mark must equal F1's saved `pops`, seed for seed. Arms: C, 12 sweep arms, S (sham): 14 × 64 = 896 worlds, about
  12 hours.
- **Observers (read-only):**
  - F1's probe (`F1_baseline_fragility/run_f1.py`, `Probe`): populations, births, rates, decisions blocked.
  - E8.2's probe, **loaded unchanged from `E8_crucible/run_e82.py`** (the `recipe_material_units` helper and the
    `Probe` class, executed against the control code's `acl.matter`). It cannot simply be imported, because that file
    binds E7's code copy when imported.
- **Zero check (hard stop):** on seeds 501 and 601, 20 years, the control code's state hash with both observers attached
  equals its hash without them.
- **Analysis script** written and smoke-tested before any main-run data.
- **Start:** automatically after LK1's 768 worlds are saved (a waiter, as AA1 waited for WS1).

