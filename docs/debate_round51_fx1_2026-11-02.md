# Council round 51: the fault fixes (FX1) and the order of work (2 November 2026, about 22:00 New York)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The first round with three advisors:** DeepSeek was added at the creator's request this evening
  (`docs/deepseek_intro_2026-11-02.md`).
- **The question** (the same file to all three): `docs/debate_round51_question_2026-11-02.md`.
- **What it covers:** the three faults found in the rules review (`docs/rules_review_2026-11-02.md`), the proposed FX1
  harm-check study, and the order of work.
- **The chats:**
  - GPT: the main chat;
  - Gemini 3.1 Pro (High): the round-50 chat `d5ecc8b87be7ae89`;
  - DeepSeek (DeepThink): `2552dbba-6c74-4cc4-b613-2228b137c47f`.

## First answers (summarised from the pages; key sentences quoted)
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| F1–F3 real faults? | yes ("Confirmed") | yes | yes (F3 "real, minor") |
| leave F4 for now? | yes (measure first; AF1's K may change it) | yes | yes |
| harm-only check, no confirmatory run? | yes ("corrections to existing rules rather than new hypotheses") | yes ("the correct epistemology for bug fixes") | yes ("a fix restores what the rule already says") |
| amendments | F1's floor must stay exact; specify whose values and which ties for "least valued" and conserve the item record; report each fault's effect separately; flag any large unexpected change | none | report F1's effect explicitly; autonomy measures must first tell v11 from a more constrained control; if F1 moves skip rates materially, check the mechanism before stacking openings |
| autonomy measures now? | yes, read-only; "distinguish novel action sequences from genuinely new action capabilities. Diversity alone is not autonomy" | yes | yes (its own proposal) |
| estimate | 91% | 98% | about 94% |

**GPT's bottom line:** "Fix incorrect implementation before interpreting further cognitive results, but don't mistake
successful bug repair for progress toward Bob."

## Checked against the code
- **Gemini wrote that F1 "systematically penalizes older recipes".** That is wrong. A recipe later in the learned order
  must exceed k times the earlier best, so F1 favours *older* recipes. Gemini was told, in the follow-up to all three.
- **GPT's floor concern is already met.** Under the fix a recipe is skipped at v ≤ 0.05, and u must still exceed
  `best_u`, which starts at 0.05. So both v11 floors stay exactly as they are for the first eligible recipe.

## The merged design (sent to all three)
1. **F1:** a recipe is skipped if v ≤ 0.05, and u must still exceed `best_u` (which starts at 0.05). The highest u wins.
2. **F2 and F3:** the thing that goes is the least valued by the holder's own item values, with ties broken exactly as
   in `_keep` (the most recently added goes first). Its record goes to the ground unchanged (identity, uses, wetness,
   contents), at the holder's tile, through `drop_on_ground`.
3. **Two settings,** `fix_make_choice` and `fix_overflow`.
   - **Arms:** v11, f (both), f1 (F1 only), f23 (F2 and F3 only) and the sham, on the same 32 seeds.
   - The decision is on f; f1 and f23 are described.
4. **Any large unexpected change** in behaviour is flagged for investigation, even if no guard is raised.
5. **The read-only autonomy-measures work starts now.** The measures must first show that they tell v11 apart from a
   deliberately more constrained control.
6. **If F1 moves the skip rates materially,** a short check of the mechanism comes before the next openings are
   stacked on top.

## Final answers
- **GPT: 97%.** "Yes, I support the merged FX1 design; my confidence rises from 91% to 97%." The remaining 3% "reflects
  implementation and unforeseen interaction risks, not objections to the design".
- **Gemini: 99%.** "The merged design has my full support". The split arms and the constrained control "protect the
  causal interpretation of the fault fixes".
- **DeepSeek: about 95%.** "Support: yes, the merged design is stronger than my original". The estimate is "unchanged
  at ~94%, perhaps nudged to ~95%".

## Decision
The assistant's estimate is **85%**. FX1 goes ahead under the creator's permission of 2 November ("If you find
something fix it"), as frozen in `experiments/FX1_fault_fixes/questions.md`.
