# L1 — No growth in winter: pre-registration (FROZEN)

**Status:** signed off by the creator and frozen as `L1-frozen` before the survival pilot, the probe or any run. Not to
be edited after the results. The creator's decisions: A2-full people, 16 seeds, the pilot stop rule and the
falsification thresholds as drafted.

## 1. Why

The evidence chain from E13R to N3: storage is absent not because people fail to learn (D2), and not because sowing is
objectively bad (D1, D2), but, on the leading hypothesis, because **the world stays productive through winter, and
immediate-return living fits it** (W1, U1, D1, N2). The N3 evidence review found that temperate plants are dormant in
winter: ACL's winter, in which wild plants still regrow at 15% of their spring rate, is not a realistic winter. L1 tests
whether the immediate-return way of life survives contact with a leaner, realistic winter, by the smallest change the
evidence supports.

## 2. The change, exactly

One setting: the winter season factor for plant regrowth, `season_growth[3]`, from **0.15 to 0**. Read from the code:
it is used in one place only, the weekly regrowth of wild plants (fibre does not grow in winter anyway). Wild plants then
do not regrow in winter; winter dieback (2.4% to 3.9% a week) is unchanged. Nothing else changes: no rule, no person, no
other number. **No code is changed**: both arms run the identical E13R code; L1 differs only in this one setting.

The value 0 is not chosen; it is the realistic value for a temperate winter (N3 evidence: Polgar and Primack 2011;
Vitasse et al. 2014; Bowling et al. 2024). It will not be tuned.

## 3. Arms and worlds

| arm | world | people |
|---|---|---|
| **C** control | as now (winter regrowth factor 0.15) | as in E13R's control (A2-full, anticipation 1.0) |
| **L** L1 | winter regrowth factor **0** | same |

The people are A2-full, as in every analysis since E9 (W1, S1, G1, P1, U1, D1, D2 were all on it), so L1's results can
be read against that chain. (The creator: switching people now would leave it unknown whether a result came from the
lean season or from different people.)

**Seeds:** 16 new seeds, **601–616**, both arms, 120 years. A world that dies out counts as it falls. (A surprising
result can be replicated later with more seeds.)

## 4. Survival pilot (before the experiment, read only for survival)

A harder world that simply dies out teaches nothing (E6: four of eight harsher worlds died out). Before the experiment:
L1 on four pilot seeds, **701–704**, 120 years. **Read only population every ten years and whether the world died out.**
Nothing else from the pilot is looked at. **Stop rule:** if two or more of the four pilot worlds die out, the experiment
does not run, and the design returns to the creator.

## 5. Validity

- Probe read-only in both arms (state hash, 20 years).
- Code fingerprint unchanged during runs; no crashes.
- **Arm C reproduces itself on rerun** (it is the existing world on new seeds; there is no saved run to compare with, so
  one control seed is run twice and must match exactly).

## 6. Measures (the same as the read-only investigations, so the chain can be read across)

**Manipulation check (does winter get leaner?)**
- **M1** Plant food on land per person, mid-winter, L against C (from D1's measure).
- **M2** Food gathered per forage week in winter, L against C (from U1's measure).

**Delayed return (the headline)**
- **D-a** Median household stock at the start of winter ÷ the household's winter need (W1's measure; control in E13R
  0.11).
- **D-b** Share of carers with any food in their own stashes at the start of winter (W1; control 6.9%).
- **D-c** Autumn specificity: adults' share of autumn weeks spent foraging ÷ their share of summer weeks (U1's measure).
- **D-d** Seed sown per person per year (D1).

**How people meet the winter (descriptive)**
- Winter: food given away (G1, P1), going short, adult starvation deaths, population; hunting's share of food gathered
  (W1); stashes; seed held.

**Last, read only if the links before it hold:** children's winter starvation.

## 7. Order of reading (binding)

Validity → manipulation check → the frozen hypothesis test (section 8) → how people met the winter → population →
children's deaths last.

## 8. What would falsify the immediate-return hypothesis (frozen)

**The immediate-return hypothesis, as the creator stated it:** ACL's people live the immediate-return life their world
rewards. **Its prediction for L1:** removing winter growth alone will **not** create substantial delayed-return
behaviour.

**"Substantial delayed-return behaviour"** means **at least two** of these three, in L against C, pooled over the seeds:
1. **D-a** median household stock ÷ winter need at least **2×** C's;
2. **D-b** share of carers with food stashed at the start of winter at least **3×** C's **and** at least 10%;
3. **D-c** autumn-to-summer foraging ratio at least **1.2×** C's.

The thresholds are set high on purpose: a nudge in stashing from 7% to 9% is noise around the existing equilibrium,
not delayed return emerging.

- **If two or more are met:** the immediate-return hypothesis takes a serious hit. A realistic winter alone moved ACL's
  people toward delayed return with the capacities they already have.
- **If fewer than two are met:** the hypothesis survives this test. It does not prove it: L1 may simply not have bitten
  (section 9).

**Reading a null (frozen, the creator's words):** "Failure to create delayed-return behaviour is not evidence that lean
seasons are irrelevant. It is evidence only that removing winter growth alone is insufficient under ACL's current world
structure." **And a null is read only after the manipulation check:** if M1 and M2 show winter did not get leaner in L
(outcome A), a null says nothing about lean seasons at all, only that this setting did not make one. Only if winter did
get leaner may a null be read as evidence that the absence of storage is not mainly caused by mild winters.

## 9. The outcomes, written before any data

| outcome | what it would look like | reading |
|---|---|---|
| **A. Little changes** | M1 and M2 barely lower in L; D-a to D-c near C | no winter growth is not enough scarcity in ACL (N3's arithmetic: tiles stay above a week's foraging). A useful result; L6 or a stronger winter would be next |
| **B. Storage emerges** | two or more of section 8 met | the hypothesis takes a serious hit |
| **C. People survive through sharing** | winter leaner (M1, M2), giving rises, stores do not | the immediate-return answer holds under stress |
| **D. Another strategy** | winter leaner; hunting, moving, sowing or something else rises instead of stores | a non-storage answer, counted as a finding (N3 evidence: foragers meet lean seasons with meat, weight loss, moving and stores) |
| **E. Collapse** | populations fall or die out | the winter is too hard for ACL's people; the design returns to the creator |

## 10. What L1 can and cannot conclude

The strongest permitted conclusion is about ACL: "in a world with no winter growth, ACL's people, with the capacities
they have, do (or do not) turn to delayed return". Not that humans needed lean seasons, and not that the immediate-return
hypothesis is proven. The control is the existing world on the same seeds; every earlier finding (E8 to D2) describes
the existing world.

## 11. After sign-off

1. Freeze and tag `L1-frozen`.
2. Write the probe and the analysis script, tested on fake data, committed before any data.
3. Survival pilot (section 4). Report survival only.
4. If the pilot passes: run, then report in the order of section 7.
