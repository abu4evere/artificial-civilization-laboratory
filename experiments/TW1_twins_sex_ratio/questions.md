# TW1 — Twins and the sex ratio at birth: a change to nature (SIGNED OFF 25 October 2026; frozen as `TW1-frozen` before any code or data)

**Why.** The creator decided (24 October 2026) to add **twins at a fixed, low, purely random chance** and to make the
**sex ratio at birth 105 boys to 100 girls**, as in real humans (`../../docs/gpt_view_twins_2026-10-24.md`). Today
every birth makes exactly one child, a boy or a girl with equal chance (`acl/biology.py` `give_birth`). Both are body,
so nature under Law 126: evidence first, one plan, frozen, checked, the creator signs off.

**What this study is not.** It is not a survival study and not a rescue: the creator and GPT agree twins should not be
added or tuned to help worlds live. Population and survival are reported, never used to accept or refuse.

## The evidence (checked by the assistant, 25 October 2026; search results and abstracts)

- Identical (monozygotic) twins about **3.5–4 per 1,000 births**, roughly constant across human populations; fraternal
  (dizygotic) twins vary widely (all twins from about 6 per 1,000 in Asia to about 40 in parts of Africa) (Smits &
  Monden 2011; Monden, Pison & Smits 2021). A natural-fertility example: rural Gambia about 14–16 per 1,000 (Sear et
  al. 2001, via GPT; not yet read by the assistant). No reliable forager figure exists.
- Without modern medicine twins die far more often: under-five mortality 213 per 1,000 for twins in sub-Saharan Africa
  2009–14, about three times singletons, not explained by birth weight alone (Monden & Smits 2017).
- Sex ratio at birth about **1.05** (natural range about 1.03–1.07) (UNFPA 2012; WHO).

## The candidate (two settings, each default 0 = nature v6 exactly)

- **`sex_ratio_birth`**: when on, a newborn is a boy with chance 105/205 (0.512), a girl otherwise.
- **`twins`**: when on, each delivery is, by one random draw that depends on nothing else (not age, previous births,
  population or any person): **identical twins with chance 0.004**, **fraternal twins with chance 0.010**, otherwise one
  child (about 14 twin deliveries per 1,000, close to rural Gambia; identical near the human constant). The fraternal
  rate is the assistant's operational choice inside the observed human range (6–40 per 1,000 all twins), fixed now and
  never tuned.
  - **Identical twins**: one temperament draw (parents' average plus drift) given to both, and the same sex.
  - **Fraternal twins**: two ordinary, separate draws, as two siblings; sex drawn for each.
  - Both are born in the same week to the same parents, are ordinary siblings to each other and to everyone else, have
    their own names, histories and memories, start with the same blend of the parents' habits, and have the mother as
    carer. **Nothing else knows they are twins**: no special bond, feeling, memory or treatment.
  - **One delivery:** one pregnancy, one nursing clock for the mother, one draw for the risk of dying in childbirth
    (unchanged). No extra death risk is added for twins: the current body has no prematurity or birth weight, and that
    limit is reported, not patched with an invented number.
  - **Feeding and care** through the existing rules: the carer's food is shared among dependants as it is today, so two
    infants cost more than one.
- **The nursing rule, fixed for twins:** today a mother cannot conceive for 78 weeks after a birth while her
  *last-listed* child lives (`_youngest_alive`). With twins that would check only one of them. The rule becomes "while
  any child of her latest delivery lives". With no twins this is the same rule (only one child per delivery), which the
  zero checks must show exactly.
- **No order bias (checked in the code):** a carer's food is shared among dependants by one common portion that never
  exceeds what the carer holds, so the first-listed twin is not fed first at the other's expense.

## Design

- **Code:** `code_tw1` = `code_v6` + the two settings + the nursing fix + read-only logging of deliveries.
- **Arms:** C (v6) and T (v6 with both settings on). **Seeds: 256 new, 16101–16356**; 20 founders, 120 years; 512
  worlds on GitHub (GPT: the code is shown by unit tests; worlds are for the rates and for description). A sham arm is
  not needed: nothing is read as an effect on survival.
- **Zero checks (hard stops):** settings off = `code_v6` exactly (state and random numbers; seeds 11 and 501 at 5
  years, 501 and 601 at 20); the nursing fix alone (no twins) = `code_v6` exactly; T acts; logging changes nothing;
  reload exact; unit tests: identical twins share all 8 traits and sex; fraternal twins draw separately; both twins are
  each other's siblings (kinship 0.8) and share both parents; one nursing clock; the mother stays unable to conceive
  while either twin lives and the other has died.
- **Manipulation checks (hard stops), pooled over T's worlds:** twin deliveries per 1,000 deliveries within the 95%
  binomial range of 14; identical share of twin deliveries within the range of 0.004/0.014; boys per 100 girls among
  newborns within the binomial range of 105; and none of these differ by mother's age, previous births or world
  population beyond chance (they must depend on nothing).

## Adoption rule (fixed now, before any data)

If the zero checks and manipulation checks pass, **both settings are proposed for nature (v7)**, because they are the
truer body and the creator has already chosen them. Their effects on population, survival, births and deaths are
**reported, not used to accept or refuse** (a rule that kept or dropped twins for their effect on survival would be
tuning nature). The creator decides.

## Described (not tested)

Twin survival to 1, 5 and 15 against singletons in the same worlds (expected lower, from shared care); mothers' food
and health in the year after twins; births per woman; deaths by cause; population at years 60 and 120; the share of
boys among adults at 16, 30 and 50; identical-twin pairs alive at 16 (for a later twin-identity study: TW-ID1, GPT's
concept, not part of this plan).

## The assistant's prior

All checks pass. Twin deliveries about 14 per 1,000; with about 3 births per woman and ~25–40 people, a world sees
roughly 3–6 twin deliveries in 120 years. No meaningful effect on survival. Twins die more often than singletons as
infants (shared care), but far less than the 3× seen in real data, because ACL's body lacks prematurity.

## Revision 1 (25 October 2026, sleep mode, before any code or data)

After GPT's review (`gpt_review_tw1.md`): rates and checks per delivery; identical twins tested directly; sex ratio
counted with identical pairs once; 99.9% intervals; independence by code and tests; whole-birth unit tests; 256 seeds
instead of 512. Twin survival is described only for what ACL represents (shared care and food), never read as human
twin mortality.

## Sign-off (25 October 2026)

The creator: "yea approve all and run them on github", on the revised drafts as written (Revision 1; 256 seeds). Frozen before any code or data.
