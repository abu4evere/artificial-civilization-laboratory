# CT1 — Courting as nature: does knowing someone, or longing for company, help couples form? (Revision 1 after GPT's review; SIGNED OFF 22 October 2026; frozen as `CT1-frozen` before any code or data)

**Why.** Every study of partners points to the same step:
- **PF1:** in about half of a single woman's weeks, a suitable man is within reach and **neither courts**. A stranger
  can almost never be accepted.
- **PF2:** courting is on the table about nine weeks in ten but has a median **one chance in a thousand**; food wins
  about three choices in four.
- **TP1:** small total size carries the risk of dying out.
- **TL1:** when the last child is born, an eligible man is usually still alive in the world.
- **F2:** pairing people up "by oracle" cut extinction from 22 to 7 of 64 worlds. So the partner step matters, but
  F2 wrote in an outcome, not a nature.

CT1 asks whether an **individual-level human tendency**, not a custom, changes this. It is a **Law 126 study**: two
candidate changes to nature, tested like LM1. Nothing is adopted by this study; adoption follows a rule fixed before
data, and the creator decides.

## How courting works today (read from `acl/`, nature v3, 22 October 2026)

- **Choosing to court** (`mind.py`): for two single, unrelated adults within 15 years of age, the score is
  (0.35 + 0.4 × sociability) × (0.5 + 0.5 × affection) × (1 − 0.5 × hunger). Loneliness is not in it, though it is in
  talking's score. The choice is a softmax at temperature 0.2 among about a dozen options.
- **Accepting** (`actions._court`): the one courted accepts (with chance 0.6) if attraction > 0.55, where
  attraction = 0.25 + 0.2 × sociability + affection + 0.2 × respect + 0.1 × health/100. **Familiarity is not in it.**
  A stranger scores about 0.45 at average sociability and at most 0.53, so is never accepted. A refused suit adds
  about 0.02 affection, so it takes many refusals before a suitor can be accepted.
- Familiarity grows with every talk (+0.08), gift (+0.05), care (+0.05) and courting (+0.03). It fades only after a
  year apart.

## The candidates (individual-level mechanisms; each one setting, defaulting to v3's behaviour)

| setting | v3 | candidate | the change |
|---|---|---|---|
| `familiar_attraction` (K1) | 0 | **0.3** | attraction gains 0.3 × familiarity. Someone well known (familiarity ≥ about 0.35) can pass 0.55 without prior affection |
| `lonely_courting` (K2) | 0 | **1** | courting's score is multiplied by (1 + loneliness), as talking's score already rises with loneliness |

**Evidence (each source to be checked, and how much was read labelled, before the creator signs):**
- **K1, a defensible hypothesis.**
  - Repeated contact can raise liking ("mere exposure": Zajonc 1968).
  - Nearness predicts friendship (Festinger, Schachter & Back 1950) and marriage (Bossard 1932, Philadelphia marriage
    licences).
  - Among foragers, spouses mostly come from people already known through kin and camp networks
    (`../PF2_instead_of_courting/evidence_courtship.md`).
  - But (GPT) liking is not accepting a partner. Familiarity can also *undermine* attraction, depending on whether
    contact is mere awareness, surface contact or mutual (Finkel et al. 2015, named by GPT). So K1's threshold effect,
    where familiarity alone overcomes refusal, is a stronger claim than the evidence makes.
- **K2, weaker; a secondary candidate.** The wish for company is a general motive. But no source here shows that
  loneliness raises *courting* in particular, rather than other social contact. Sayre et al. 2023 measured physical
  activity, so it is withdrawn as support (GPT's check).
- **Individual-level, not "pure nature"** (GPT). Familiarity, attraction and social motivation are shaped by culture
  in real people. ACL models the individual level only, and leaves institutions to emerge or not.

**Not candidates.** These are culture or outcomes, and must not be written in:
- arranged marriage, bride service, exchange between families, any rule about who marries whom;
- "oracle" pairing (F2), or any change that sets an outcome.

The 12-person attention limit and the choice temperature act on every decision, not only courting, so they are left
alone.

**The sizes are exploratory, not measured.** No source gives the 0.3 or the (1 + loneliness) in ACL's units, and no
behavioural target exists to calibrate them against. So CT1 tests **these particular implementations**, not human
psychology in general. The sizes are set so the change is large enough to act: under K1, well-known people become
possible partners; under K2, a lonely person's courting score at most doubles. They are fixed before data and
**never retuned** after seeing which saves more worlds.

## Design (the assistant's recommendation; decisions marked)

- **Code:** `code_ct1` = `code_v3` + the two settings (default 0 = v3 exactly) + a read-only log of courting attempts
  and acceptances (not saved; read by nothing in the world).
- **Arms:** C (v3), K1, K2, K12 (both). **Seeds (Decision 2): 256 new, 8201–8456**; 20 founders, 40 × 40, 120 years;
  1,024 worlds, on GitHub's machines. Zero checks there and here first.
- **Zero checks (hard stops):**
  - both settings 0 equals `code_v3` (seeds 11 and 501 at 5 years, 501 and 601 at 20 years);
  - each setting acts;
  - logging changes nothing;
  - reload is exact.
- **Manipulation checks** (hard stops; no outcome is shown if they fail):
  - K1: acceptances of suitors with no prior affection rise against C.
  - K2: courting attempts per single adult-year rise against C.
- **Mechanism, described** (to see that the mechanism acts, not just that the code changed something):
  - acceptance by familiarity level;
  - courting by loneliness level;
  - whether different people are approached;
  - whether the change acts mostly on people who would otherwise rarely pair.
- **Primary (survival):** extinction, each arm against C, paired by seed. Exact sign test, Holm over the three; effect
  = C's extinction share − the arm's, 95% bootstrap (10,000, `random.Random(2026)`). Readings as every study:
  "changes survival" (with size label), "no meaningful effect" (p ≥ 0.05 and the interval inside ±0.117),
  "unresolved".
- **Mechanism outcomes** (they show the process; they are not conditions for adopting): births per woman-year (F1's
  pooled rate); share of fertile woman-weeks single; couples formed.
- **Harm outcomes** (each with the absolute and relative change against C and a 95% paired bootstrap interval):
  - infant deaths per birth;
  - adult deaths by starvation;
  - couples that split;
  - births to mothers under 18, or with a father more than 15 years older.
- **Interaction:** (K12 − K2) − (K1 − C), described. K12 asks whether the two act together; finding the "best"
  combination is not CT1's purpose.
- **Pairing is by seed.** Once the arms differ they draw random numbers in different orders, so a pair shares a
  start, not a path. The paired tests are used as in every study.

## The adoption rule (fixed now, before any data)

**Principle (GPT's, adopted):** saving worlds is a consequence of a mechanism, not evidence that it is right. A
candidate enters nature because its evidence supports it and it works as intended, **not** because it saves worlds.
LX1 used the same rule.

A candidate (K1 or K2) may be **proposed for adoption into nature (v4)** only if all of these hold:

1. Its manipulation check passes.
2. **It does not cost survival:** against C it reads "no meaningful effect", or "changes survival" with fewer worlds
   dying out. If it reads "changes survival" with **more** worlds dying out, it is **not adopted**, whatever the
   size.
3. **No serious harm:** infant deaths per birth and adult starvation deaths do not rise (paired test, p < 0.05). The
   other harms are reported for the creator to weigh.
4. The creator accepts its evidence (above) as enough for nature.

Further rules:
- **Unresolved survival:** not adopted now; the creator decides whether to run more seeds.
- **K12** is proposed only if K1 and K2 each qualify on their own.
- **The yardstick ±0.117** is half of F2's effect, and F2 wrote in an outcome, so it is a rough scale of a large
  change, not a measured benefit. It **only defines "no meaningful effect"**; no candidate has to reach it.
- **Births and couples** should move the way the mechanism says (that is the mechanism's evidence), but no p-value
  on them is a condition.
- Whatever the result, every arm is reported, including effects on survival in either direction.

## The assistant's prior (to be frozen at sign-off; held loosely)

- **K1 reads "changes survival", with fewer worlds dying out.** PF1's refusals of near-strangers become acceptances
  among people who know each other. Its manipulation check passes, with no serious harm.
- **K2 alone has no meaningful effect.** More courting of strangers is still refused, as PF1 found when bands were
  made smaller.
- **K12 is no better than K1.**

## Before freezing (the research rule)

GPT reviewed Draft 0 (`gpt_review_ct1.md`). This revision adopts its points:
- survival is not the reason to adopt;
- the sizes are exploratory;
- K2's evidence is weaker, and Sayre et al. is withdrawn;
- the yardstick's role is stated;
- births show the mechanism and are not a condition;
- harms are reported with absolute changes and intervals;
- K12 is only for the interaction.

Its better candidate, **courting that responds to visible interest returned**, is left for a later study. A read-only
look first has to check whether ACL's relationship changes already act like it (a refused suit still adds a little
affection).

## Decisions for the creator

1. The two candidates (**K1 familiarity in attraction, K2 loneliness in courting**), with their **exploratory** sizes
   (0.3; × (1 + loneliness)), accepted as tests of these implementations, not of human psychology in general. Or
   drop K2 (weaker evidence) and run C against K1 only (512 worlds).
2. Seeds: **256 new (8201–8456), four arms, 1,024 worlds on GitHub** (recommended), or 512 seeds (more precise,
   about twice the time).
3. The adoption rule, fixed as written.
4. The prior, frozen as written.

## Sign-off (22 October 2026)

The creator: "approve all recommendations, freeze it". So:
- both candidates (K1, K2) with their exploratory sizes;
- 256 new seeds (8201–8456), four arms, 1,024 worlds on GitHub;
- the adoption rule and the prior, as written.

## Operational note (22 October 2026, while building, before any data; rule 19)

Reading the code while building showed three things. Nothing else changes.
- **Couples part only at death** (`biology.die` frees the survivor); nothing else ends a couple. So the harm measure
  "couples that split" is zero by construction in every arm. It is reported as such.
- **K2 applies to courting someone not yet a partner** (the branch PF2 measured). Courting one's own partner keeps an
  existing couple going, not partner-finding, so it is left as in v3.
- **The courting log** (`world.ct1log`, not saved) records each attempt on someone not yet a partner: week, suitor,
  courted, the courted one's affection and familiarity toward the suitor, the suitor's familiarity toward them, the
  suitor's loneliness, and attraction. An attempt counts as accepted when a "pair" event between the two follows in
  the same week. The full code difference is `v3_to_ct1.diff`.
