# NV7 — Nature version 7: twins and the sex ratio at birth (built and checked)

**The creator's decision (25 October 2026):** "yea go with a, make v7". This followed TW1's frozen rule: TW1 was
valid and its manipulation checks passed (`../TW1_twins_sex_ratio/findings.md`). GPT's view (opinion, not sign-off;
`../TW1_twins_sex_ratio/gpt_view_tw1.md`) was to adopt it, after an integrity audit. GPT also independently recomputed
the numbers from the raw files, and they matched (`../TW1_twins_sex_ratio/recompute_tw1.md`).

**v7 = v6 + `twins` + `sex_ratio_birth` + the nursing fix.**
- Each delivery is identical twins with chance 0.004, fraternal twins with chance 0.010, otherwise one child. This is
  one random draw that reads nothing else.
- A newborn is a boy with chance 105/205.
- A mother cannot conceive while any child of her latest delivery lives (in the nursing weeks).
- One childbirth-death draw per delivery, unchanged.

`code_v7` is `code_tw1` unchanged; the difference is `v6_to_v7.diff`.

**Costs recorded (described in TW1, not tested):**
- Twins die more than singletons with no extra rule (to age 5: 0.66 fraternal, 0.56 identical, 0.84 single).
- Adult women are scarcer (men per 100 women reaching 50: 166, vs 141 on v6).
- More worlds died out (97 vs 83 of 256; paired, McNemar p = 0.16, not clear).
- The body has no prematurity or birth weight. Why women die younger than men is not yet analysed; sex was not
  logged with deaths.

## Checks (`zero.txt`, `run_nv7.py zero`): **All PASS**

- `code_v7` with both settings at 0 equals `code_v6`.
- v7 equals `code_tw1`'s T arm.
- The live package `acl/` with its own defaults equals v7.
- The settings act.
- Reload is exact.
- New reference fingerprints "v7"; the live package's fingerprints are regenerated. All 62 tests pass.

## From now

Future studies run on v7. TW1's T worlds (seeds 16101–16356) are the first v7 control set. M1 and RH1 stay on v6, as
frozen. Tag `nature-v7`.
