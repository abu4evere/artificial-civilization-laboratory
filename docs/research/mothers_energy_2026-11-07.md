# Forager mothers' time and energy, for the women 30–49 gap in EG1 (7 November 2026)

**Why:** EG1 found women aged 30–49 blocked from food by energy alone in 11.9% of their starving weeks, against men's
5.4% (`experiments/EG1_energy_gate/findings.md`). Gemini (round 76) guessed that carrying infants restricts mothers. A
source suggests; only a frozen study decides.

## Jang, Janmaat, Kandza & Boyette 2022 — **read in large part** (through a web-fetch agent)
Jang H, Janmaat KRL, Kandza V, Boyette AH (2022). Girls in early childhood increase food returns of nursing women
during subsistence activities of the BaYaka in the Republic of Congo. *Proc. R. Soc. B* 289(1987): 20221407.

**What was read:**
- the abstract, introduction, results, discussion, Tables 1–2 and the first methods sections, verbatim;
- the rest of the methods, only as a machine summary;
- the supplementary model estimates were **not** seen.

**What it reports:**
- **The trade-off.** "Nursing mothers face an energetic trade-off between infant care and work" (the abstract). The
  introduction, citing others, calls carrying infants one of the biggest drains on a mother's energy.
- **The sample:** 4 nursing BaYaka mothers, 199 expeditions in 2015–16, 140 with food weighed; returns are measured in
  kcal per minute of collecting.
- **Infants on expeditions:**
  - nursing children went along on 109 of 199 expeditions;
  - others carried them 40% of the travel and work time;
  - groups averaged 7.9 people, mostly women and children; men averaged 0.11.
- **Returns:**
  - more adults and more children in the group raised nursing mothers' returns, especially when the infant was along;
  - **each additional girl aged 4–7** raised returns more than an adult woman did;
  - men and boys had no positive effect.
- **The limits:**
  - nursing and non-nursing women are not compared;
  - what each helper did was not recorded;
  - effect sizes are in the supplement, which was not seen.

## Seen only as search-result snippets (not read)
- Hurtado, Hill, Hurtado & Kaplan 1992 (Human Nature), "Trade-offs between female food acquisition and child care
  among Hiwi and Ache foragers": mothers with nursing infants forage less and acquire less.
- Among the Hadza, child helpers are reported to be over 60% of childcare providers, and husbands' provisioning may
  matter most during lactation (Marlowe; record only).

## Checked against ACL (v15, the code)
- **ACL has no time or energy cost of nursing or carrying infants.** `nursing_weeks` (78) only blocks a new pregnancy
  (`biology.py`). Infants drink "at the breast" (water only). So **Gemini's guess cannot be ACL's mechanism.**
- **What ACL does have:** a parent's dependents' need is added to the parent's hunger (`decide`'s `dep_need`), and
  dependents are fed from the parent's food in the body phase. Feeding children can drive the parent short, and
  starving halves energy recovery. Which parent feeds, and whether it falls on mothers, is the open question.
- **So the gap is likely about who feeds the children, not about carrying.** The evidence says real mothers' burden is
  eased by helpers (girls, kin) and by men's provisioning. ACL's people can give food to kin's children (a guard in
  CI1, LW1 and FF4), but no one minds or carries an infant so that its mother can forage.

## For the council (later)
- A read-only look at which parent feeds dependents in ACL, and how often that drives each parent short, by sex.
- FF4 re-measures the gap in every arm.
- Only then, if anything, a general ability to help with a child (minding, carrying), with no named role.
