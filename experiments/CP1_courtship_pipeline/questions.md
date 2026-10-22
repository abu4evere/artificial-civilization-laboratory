# CP1 — Courtship-to-pairing pipeline audit: where do potential partnerships fail? (SIGNED OFF 21 October 2026; frozen as `CP1-frozen` before any analysis)

**Why.** TL1 (`../TL1_extinct_timelines/findings.md`) settled that extinction in ACL's baseline is almost never acute
demographic catastrophe. Births stop a median 46–49 years before the final death; eligible pairs still share the world
when births cease (mean eligible share 61–68%, median 95–100%); a 10-year birth hiatus is recoverable in ~23% of
worlds. TL1's own verdict: *"eligible pairs that still share the world fail to court and co-reside"*. PF1 and PF2
mapped exactly that failure on MB1b's 80-founder worlds (bottleneck `S5 courting-not-tried`; subsistence wins ~¾ of
those weeks). CP1 asks whether the same funnel breaks the same way in the saved **20-founder** v2 controls that TL1
read — and whether the shape of the funnel differs between worlds that reproduce successfully and worlds that go
extinct.

**Read-only:** no new runs; reads existing saved control worlds from RT1b, FX2, and FX3 (nature v2). This is an audit
of saved v2 cohort; it does not touch nature v3.

**Pipeline the creator asked to be tracked:** availability → encounter → courtship → acceptance → co-residence → birth.
On saved worlds the simulation already records a canonical, mutually exclusive, weekly bucketing of every fertile
woman-week into one of {`pregnant`, `no_partner`, `partner_dead`, `apart`, `low_health`, `starving`, `partner_child`,
`nursing`, `eligible`}. CP1 reorders those buckets into the funnel the creator named, and uses two additional snapshot
counts (`women_single_no_mate`, `women_single_no_mate_near`) to split `no_partner` into **availability** and
**encounter**. Courtship and acceptance cannot be separated from saved worlds (that needs a logging replay — PF1 and
PF2 did it on MB1b). CP1 collapses them into one measurable step and names the limitation.

---

## 1. Worlds and Data (Decision 1)

Same cohort as TL1, same split: control worlds saved under nature v2.
- **Discovery:** RT1b's C (`output_rt1b`, seeds 5701–5956) and FX2's C (`output`, seeds 6001–6256): 512 worlds
  (187 extinct, 325 surviving).
- **Holdout:** FX3's C (`output`, seeds 7301–7556): 256 worlds (80 extinct, 176 surviving), read only after discovery
  results are written and committed.

All world files record annual snapshots (`years`), weekly woman-week state buckets (`r_*`), birth and death events,
and the pair stock (`pairs`). Extinction uses the project rule: `r["final_tick"] < 120 * 52`.

---

## 2. The Funnel (fixed in advance)

### Unit of measurement
**Fertile woman-weeks** (women aged `[fertile_from, fertile_until)`), the native unit the simulation records.
Every fertile woman-week falls into exactly one of the recorded buckets (sum of `r_*` equals `woman_weeks`).

### The six gates (and how saved worlds measure each)

CP1 uses the natively recorded buckets and the single-woman snapshot splits.

| Gate | Name | Measure (per world, pooled over years 0–119) | Source |
|---|---|---|---|
| **G1** | Availability (mate pool exists) | share of **single** fertile woman-weeks where **no eligible man** is alive anywhere in the world. Approximation: `women_single_no_mate / women_single` (snapshot, once per year, treated as representative). | snapshot |
| **G2** | Encounter (eligible man within sight) | share of **single** fertile woman-weeks where an eligible man exists somewhere but **none within `perception`**. Approximation: `(women_single_no_mate_near − women_single_no_mate) / women_single`. | snapshot |
| **G3** | Courtship + acceptance (collapsed) | share of **single** fertile woman-weeks where an eligible man is **within sight** and she is **still single**. Approximation: `(women_single − women_single_no_mate_near) / women_single`. Cannot be split into offer vs refuse on saved worlds. | snapshot |
| **G4** | Co-residence (partnered, together) | share of **all** fertile woman-weeks in `r_apart` (partner alive, beyond `camp_radius`). | weekly sum |
| **G5** | Fertility blockers (physiological) | share of **all** fertile woman-weeks in `r_starving + r_nursing` (partnered-together but blocked). `r_pregnant` is counted as a **success** of G6, not a leak. | weekly sum |
| **G6** | Birth throughput | share of **all** fertile woman-weeks in `r_eligible`, i.e. all gates passed and a conception could happen that week; plus **births per fertile woman-year** (`Σ births ÷ Σ woman_weeks ÷ 52`). | weekly sum |

**Scope note (frozen, before any data).** G3 is a black box on saved worlds: we cannot say whether courting was offered
and refused, or never attempted. PF1 and PF2 on MB1b (80 founders) found courting is almost always on the table and
almost always loses to subsistence (~0.1% of the choice). CP1 does not re-measure that; it measures only whether G3 is
the biggest leak in these 20-founder cohorts, extinct vs surviving.

### Secondary measures (reported for context, not for the frozen reading)

- Share of fertile woman-weeks with **no partner at all** (`r_no_partner / woman_weeks`).
- `r_pregnant / woman_weeks` and `r_eligible / woman_weeks`.
- Births per **partnered** fertile woman-year, where partnered = `woman_weeks − r_no_partner`
  (partner_dead is left as part of "partnered-but-blocked" since on these saved worlds it is not stored separately but
  is dropped into the residual; see note below).
- Residual woman-weeks = `woman_weeks − (r_no_partner + r_apart + r_pregnant + r_nursing + r_starving + r_eligible)`.
  This captures `r_partner_dead + r_low_health + r_partner_child` (not stored as separate keys in these saved worlds;
  known to sum to a small share from the F1 run definition). Reported in both sets.

---

## 3. The Frozen Reading (the bottleneck)

**Primary comparison:** per-world average share of fertile woman-weeks at each gate (G1–G6) in two cohorts:
*extinct* worlds and *surviving* worlds, each set reported separately.

**The bottleneck gate** of extinct worlds is the single gate with the **largest absolute increase**
(extinct share − surviving share) **among G1, G2, G3, G4** (the four behavioural/demographic gates). G5 and G6 are
reported but not candidates: G5 are physiological states and G6 is the success terminal.

**Reading rules (frozen):**
- **Discovery:** declare a gate the bottleneck if its (extinct − surviving) excess is **≥ 5 percentage points** and
  strictly greater than any other gate's excess.
- **Holdout stands if:** on the holdout, (a) the same gate has the **largest** excess among G1–G4, and (b) the
  excess is **≥ 3 percentage points** and (c) the gap is within **±5 percentage points** of the discovery value.
- **If the discovery excess is < 5 pp or no single gate dominates, declare "mixed"** and recommend a logging replay
  (as PF1/PF2 did on MB1b).

**Secondary verdict (same frozen rules, reported alongside):**
- **Births per partnered fertile woman-year** in extinct vs surviving, both sets. Reported but not read for the
  bottleneck verdict.

---

## 4. Prior (written before looking at data; held loosely)

1. **G3 (mate near, still single)** will be the biggest leak in extinct worlds, extending PF1/PF2's MB1b finding to
   20-founder worlds. Expected excess 10–20 percentage points.
2. **G1 (no mate alive anywhere)** will be a small share overall (< 10%) and only marginally larger in extinct worlds
   (TL1 found eligible pairs were still present at the last birth in 69–75% of extinct worlds).
3. **G2 (mate alive but not in sight)** will show a modest excess in extinct worlds (small worlds spread thin).
4. **G4 (co-residence apart)** will be a sizeable share in both cohorts (C1 showed ~48% of partnered weeks were apart)
   but **not** the biggest excess in extinct worlds.
5. **G5 and G6** will show little excess in extinct worlds (consistent with TL1's "extinction is not acute").

---

## 5. Statistical Rules and Holdout Confirmation

- All discovery results are committed before the holdout files are touched (`analyse_cp1.py` refuses to run
  holdout until `results_discovery.md` exists on disk).
- World counts and total woman-weeks are reported beside every share.
- Per-world shares are the pooled sum over years 0–119. Worlds with fewer than 100 fertile woman-weeks total are
  reported but excluded from the cohort averages (the woman-weeks they contribute are near-noise).
- Averages are **per-world means** (one row per world weighted equally), not pooled woman-week averages: a small
  world's leak counts as much as a large one, which is the right unit for a bottleneck-of-worlds question.

---

## 6. Decisions for the Creator

1. **Scope:** 512 discovery / 256 holdout, same cohort as TL1 (RT1b, FX2, FX3 controls under nature v2).
2. **Unit and funnel:** fertile woman-weeks; G1–G6 as defined in section 2.
3. **Reading:** per section 3, bottleneck among G1–G4 by absolute (extinct − surviving) excess, discovery ≥ 5 pp,
   holdout ≥ 3 pp and within ±5 pp.
4. **Priors:** frozen as written in section 4.
5. **Scope limitation stated up front:** G3 is a collapsed black box on saved worlds; PF1/PF2 already split it on
   MB1b (80 founders).

---

## Sign-off (21 October 2026)

The creator: "Run CP1 — a frozen, read-only audit of the courtship-to-pairing pipeline. (1) Saved v2 worlds only. No new
simulations and no changes to nature. (2) Track where potential partnerships fail: availability → encounter →
courtship → acceptance → co-residence → birth. (3) Compare worlds that reproduce successfully with worlds that
eventually go extinct. (4) Identify the biggest measurable bottleneck and document the results. (5) Don't design an
intervention until CP1 is complete." All five constraints encoded above; sections 1–6 frozen as written.

## Correction appended before any analysis (same day)

TL1 had corrections appended after this plan was frozen (`c57fbfd`): Q2 shows availability of an eligible man
*somewhere in the world* at the year of the last birth; it does not count distance and does not show that failing to
court **caused** extinction. The quoted TL1 line in the "Why" ("eligible pairs that still share the world fail to
court and co-reside") is TL1's withdrawn causal claim.

CP1 is **unaffected by this correction**: its reading is descriptive. It compares pipeline-gate shares between
extinct and surviving cohorts, and names the gate with the largest excess. CP1 does **not** claim causation. If G3
(mate near, still single) is the biggest leak in extinct worlds, that locates where the funnel differs; what moves
extinction remains a question for later work (an intervention after CP1, as section 5 of the creator's instruction
requires). G1 vs G2 vs G3 are *all* under the "no partner" umbrella TL1 inspected; CP1 is exactly the distance-aware
split TL1's Q2 could not give.
