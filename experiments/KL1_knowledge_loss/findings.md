# KL1 — Does know-how outlive its holders? Findings (final: recomputed blind by GPT and Gemini; see the end)

**Read-only: no change to nature.** Live v11 (`code_v11`). Frozen as `KL1-frozen`, with two operational notes made
before any study data (the revival order; transmission errors as a revival path). Signed off by the assistant with
the creator present (GPT 91%, Gemini 75%, the assistant 80%; debate round 44).

**IQ1-H3, step 1:** inspired by Q 96:4 and Sahih Muslim 1631. That is inspiration only; this study says nothing
about those sources.

**The run:** GitHub Actions run 41384817251 (the first run, 41380622576, was cancelled under operational note 1). The
zero checks ran on the cloud (`zero_cloud.log`). 32 worlds, seeds 21701–21732; LP, 200 years; years 100–200 counted.
Every number comes from `analyse_kl1.py`, written before data and tested on a smoke world. Full tables are in
`results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under `code_v11`'s fingerprint;
- **the observer's record of who knows what matched everyone's actual recipes at every check**;
- every world-level loss and revival matched the world's own register;
- no loss without a cause, and no impossible revival (mismatches 0).

## The answer
**Death is the main road of loss; marks do not (yet) revive lost know-how.**

| quantity | value [95%] | count |
|---|---|---|
| **D:** share of world-level losses by death | **0.903 [0.891, 0.913]** | 10,447 of 11,576 |
| **R_markable:** share of markable revivals through marks | **0.020 [0.000, 0.052]** | 2 of 99 |

### Secondary (described, not decisive)
- **Know-how lives in few heads.** Each year a world holds about 211 recipe kinds, known by 6.2 people on average.
  But **61% of kinds are known by a single person.** Kinds that are lost had lasted a median of 2,795 weeks (about 54
  years).
- **When a knower dies, most of what they knew survives:** 90% of their kinds live on in someone else. The 10% that
  die with them make up 90% of all losses.
- **Minds lose know-how by death (82%) or by the 12-recipe cap (18%).** Dropping a recipe as useless **never
  happened** (0). In these worlds no recipe was ever valued below −0.15.
- **How know-how is gained:**

  | path | share |
  |---|---|
  | made | 67% |
  | taught | 13.5% |
  | read from marks | 8.4% (8,892 gains, nearly all simple strike recipes) |
  | taught with an error | 7.6% |
  | copied by watching | almost never (10 gains) |

- **How lost kinds come back:**
  - Other kinds: mostly made again (3,490), or by an error in teaching (483).
  - Markable kinds: almost all by an error in teaching (95 of 99); marks revived 2.
  - **Re-invention, not preservation, is what revives lost know-how.**

## Against the prior (the assistant's, frozen)
1. "Forgetting is the main road of loss": **wrong.** Death is, at 90%, and value-based forgetting never fired.
2. "Marks do not (yet) revive lost know-how": **right** (2%).
3. "At a knower's death, most of their kinds survive in someone else": **right** (90%).

## What it means
- **In ACL, know-how mostly outlives single deaths but not lone knowers.** Most kinds are well shared. But most
  *kinds* are held by one person, and those die with that person. This matches the shape of Henrich's (2004)
  argument, as far as it is known here: skills held by few are lost when transmission is imperfect and populations
  are small.
  - **Only the bibliographic record** was confirmed for that paper. Its text is not yet read, so this is a
    resemblance, not a test.
- **Marks carry know-how to the living** (8% of gains), **but rarely across a gap** when nobody alive knows it (2 of
  99 revivals). The pen-like medium works as a teacher, not yet as a memory that outlasts everyone.
- **Teaching passes know-how on, and its errors also create.** Error-variants of teaching revived most lost markable
  kinds. That is transmission as variation, close to Deutsch's account of copying as re-creation (study note, three
  books).
- **For Bob:**
  - Cumulative culture needs know-how to outlive its holders.
  - In ACL, broadly shared know-how does, but rare know-how does not.
  - The open question is whether rare know-how is valuable or mostly minor variants. KL1 did not measure value.
- **No change to nature** follows from this study.

## Independent recompute (2 November 2026)
GPT and Gemini, each in a fresh chat, from per-seed counts of the raw output only (`recompute_kl1.md`). **All
three agree:** D 0.9025 [0.891, 0.913]; R_markable 0.0202 (2 of 99); death is the main road of loss; marks do not
(yet).

**Final.**
