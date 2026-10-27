# How can ACL's people learn "why"? (GPT's and Gemini's opinions, not sign-off)

**The creator's question (27 October 2026):** "they gotta ask why from themselves but how we gonna develop it". The same
text went to both (`docs/pending/question_why_2026-10-27.md`); Claude was council.

## GPT
- **Strong support,** with one distinction: "learning to predict usefulness from physical properties is not yet causal
  understanding. It is a foundation for it."
- **The capacity:** learn which observable properties predict outcomes, use that to predict unfamiliar things, and
  correct after wrong predictions. "We must not preload the rule that sharpness causes cutting."
- **Important:** "ACL must not give agents direct access to hidden physics calculations or the true tool factor.
  Properties must be observable, even imperfectly." Combinations of properties may matter.
- **Legitimate** against **not legitimate:** learning which properties predict results, against preloading them;
  generalising, against giving new things their true worth.
- **First, PG0, a read-only audit:** do puzzles lead to useful new things? How often do new kinds stay unused? Could
  their properties have predicted their usefulness from the person's own past experience (an offline predictor)?
- **Then PG1, a frozen experiment:**
  - primary outcome: prediction error on unseen kinds before first use;
  - an offline shuffled-property control;
  - no invention counts as criteria.
- **Chances:** audit 85%; better generalisation 65%; real causal reasoning from this alone under 20%.
- **Order:** "Prediction … Causal testing … Explanation … in that order, one law at a time."

## Gemini
- **Support:**
  - a per-person matrix W[property, use], starting at zero;
  - updated from felt yield against expectation;
  - a new kind's starting worth = the sum of property × W.
- **Not tuning:** exposing the raw properties with a uniform update. **Tuning:** hard-coded property rules, non-zero
  starting weights, extra rewards.
- **Audits first:** puzzle efficiency, and "cold-start drag".
- **Study:** the pass condition is to reduce "the −0.56 initial under-valuation gap found in VC1" to ≤ 0.15.
- **Chances:** audit 95%; study 85%.

## Council checks
| claim | who | check | result |
|---|---|---|---|
| Pass if VC1's −0.56 gap falls to ≤ 0.15 | Gemini | VC1's −0.56 is the **habit value of the action "make"** (q − G), not the worth of a kind of thing (itemval) | **mismatched quantity**; not adopted |
| Learning rate 0.05 for property weights | Gemini | An invented number. `judge_item` already uses 0.15, or 0.3 when proved wrong | if built, reuse the existing rates |
| Exposing raw properties is not tuning | Gemini | GPT disagrees in part: exact hidden properties would be privileged knowledge | **GPT's caution adopted:** properties must be observable, perhaps imperfectly |
| The audits are "deterministic replays" | Gemini | They are read-only observers on new worlds | corrected (again) |

## Where they agree
- **Audit first** (read-only).
- **Then one capacity:** learning the worth of properties, with nothing preloaded, judged on prediction for unseen kinds,
  not on inventions.
- **Causal testing and explaining** come later, separately.
