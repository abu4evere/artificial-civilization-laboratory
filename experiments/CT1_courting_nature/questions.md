# CT1 — Courting as nature: does knowing someone, or longing for company, help couples form? (DRAFT for the creator; nothing built or run)

**Why.** Every study of partners points to the same step:
- **PF1:** in about half of a single woman's weeks, a suitable man is within reach and **neither courts**. A stranger
  can almost never be accepted.
- **PF2:** courting is on the table about nine weeks in ten but has a median **one chance in a thousand**; food wins
  about three choices in four.
- **TP1:** small total size carries the risk of dying out.
- **TL1:** when the last child is born, an eligible man is usually still alive in the world.
- **F2:** pairing people up "by oracle" cut extinction from 22 to 7 of 64 worlds. So the partner step matters, but
  F2 wrote in an outcome, not a nature.

CT1 asks whether a **general human tendency**, not a custom, changes this. It is a **Law 126 study**: two candidate
changes to nature, tested like LM1. Nothing is adopted by this study; adoption follows a rule fixed before data.

## How courting works today (read from `acl/`, nature v3, 22 October 2026)

- **Choosing to court** (`mind.py`): for two single, unrelated adults within 15 years of age, the score is
  (0.35 + 0.4 × sociability) × (0.5 + 0.5 × affection) × (1 − 0.5 × hunger). Loneliness is not in it, though it is in
  talking's score. The choice is a softmax at temperature 0.2 among about a dozen options.
- **Accepting** (`actions._court`): the one courted accepts (with chance 0.6) if attraction > 0.55, where
  attraction = 0.25 + 0.2 × sociability + affection + 0.2 × respect + 0.1 × health/100. **Familiarity is not in it.**
  A stranger scores about 0.45 at average sociability and at most 0.53, so is never accepted. A refused suit adds about 0.02 affection, so it takes many refusals before a suitor can be accepted.
- Familiarity grows with every talk (+0.08), gift (+0.05), care (+0.05) and courting (+0.03). It fades only after a
  year apart.

## The candidates (general tendencies; each one setting, defaulting to v3's behaviour)

| setting | v3 | candidate | the change | why it could be nature (evidence, to be checked before freezing) |
|---|---|---|---|---|
| `familiar_attraction` (K1) | 0 | **0.3** | attraction gains 0.3 × familiarity (someone well known, familiarity ≥ 0.35, can pass 0.55 without prior affection) | "mere exposure": repeated contact raises liking (Zajonc 1968); nearness predicts friendship and marriage (Festinger, Schachter & Back 1950; Bossard 1932). Among foragers, spouses mostly come from people already known through kin and camp networks (`../PF2_instead_of_courting/evidence_courtship.md`) |
| `lonely_courting` (K2) | 0 | **1** | courting's score is multiplied by (1 + loneliness), as talking's score already rises with loneliness | the wish for company and attachment is a general human motive. Foragers spend much of their time socially (Lee; Sayre et al. 2023), so food need not crowd out courtship (evidence weaker; to check) |

**Not candidates.** These must not be written in, because they are **culture**: arranged marriage, bride service,
exchange between families, any rule about who marries whom. So are "oracle" pairing (F2) and any change that sets
an outcome. The 12-person attention limit and the choice temperature act on every decision, not on courting, so
they are left alone.

**The 0.3 and the (1 + loneliness) are not anchored to measurements** of real people. No source gives a size in
ACL's units. They are set so the change is large enough to act (K1: well-known people become possible partners; K2:
a lonely person's courting score at most doubles), and they are a decision for the creator.

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
- **Manipulation checks** (no outcome shown if they fail):
  - K1: acceptances of suitors with no prior affection rise against C.
  - K2: courting attempts per single adult-year rise against C.
- **Primary (survival):** extinction, each arm against C, paired by seed. Exact sign test, Holm over the three; effect
  = C's extinction share − the arm's, 95% bootstrap (10,000, `random.Random(2026)`). Yardstick ±0.117 (half of F2's
  effect). Readings as every study: "changes survival" (with size label), "no meaningful effect", "unresolved".
- **Secondary:** births per woman-year (F1's pooled rate); share of fertile woman-weeks single; couples formed.
- **Watched for harm** (described): couples that split; children born to very young or much older parents; deaths;
  whether courting crowds out feeding children (infant deaths).
- **Interaction:** (K12 − K2) − (K1 − C), described.

## The adoption rule (fixed now, before any data)

- **Adopt a candidate into nature (v4)** only if: it "changes survival" with fewer worlds dying out, **and** its
  manipulation check passes, **and** births per woman-year rise (p < 0.05), **and** no harm measure worsens by more
  than half again over C.
- If both K1 and K2 qualify, adopt **K12 only if** it beats each one alone on survival (paired, p < 0.05). Otherwise
  adopt the one with the larger effect.
- "No meaningful effect" or "unresolved": **do not adopt**; report.
- Before any adoption, the creator decides, as with LX1.

## The assistant's prior (to be frozen at sign-off; held loosely)

- **K1 changes survival** (fewer worlds die out), because PF1's refusals of near-strangers become acceptances among
  people who know each other.
- **K2 alone has no meaningful effect.** More courting of strangers is still refused, as PF1 found when bands were
  made smaller.
- **K12 is no better than K1.**

## Before freezing (the research rule)

GPT is asked for objections, missing evidence and better candidates. Its answer is recorded as `gpt_review_ct1.md`.
Every source above is checked, and how much of it was read is labelled, before the creator signs.

## Decisions for the creator

1. The two candidates (**K1 familiarity in attraction, K2 loneliness in courting**), and their sizes (0.3; × (1 +
   loneliness)).
2. Seeds: **256 new (8201–8456), four arms, 1,024 worlds on GitHub** (recommended), or 512 seeds (more precise, about
   twice the time).
3. The adoption rule, fixed as written.
4. The prior, frozen as written.
