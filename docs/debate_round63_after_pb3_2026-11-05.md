# Council round 63: after PB3, the look-ahead (5 November 2026, 09:43)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round63_question_2026-11-05.md` (the same text to all three).
- **The chats:** GPT, the main chat; Gemini 3.1 Pro, chat 87f468c684ee5839; DeepSeek, DeepThink, chat 2552dbba.
- **Recorded from the replies read in the chats.** The time in the title is from the clock.

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. diagnose first? | **Yes, strongly.** A frozen read-only diagnosis on v13 and c0 worlds: **saturation** (q at ±1.5 by action and situation, and the q values used in decisions); **scale** (0.6 × q against the written pulls); **direction** (0.8 × max next q by action and resulting food band); **decision reversals** (re-rank exact decision states with the habit term rescaled or the next-state term removed, without changing the world). Scale and direction may interact. | **Yes.** Isolate scale (the clamp; swamping bodily pulls) from direction (max penalising preparation) in actual decision traces. | **Yes, before any PB4.** (a) the share of q at the clamp; (b) on decisions where make, play or gather compete, the margin split into written pull against 0.6 × q, and how often q alone decides; (c) the look-ahead's signed contribution per action; (d) a counterfactual rescaling of q, with choices recomputed. |
| 2. law or tuning | Discount 0 is a useful control, **not** a law to adopt for making more ("outcome-driven tuning"). Prefer a calibrated, uncertainty-aware estimate. An expected next value is worth investigating but is not automatically a fix. A smaller discount anchored to independent evidence is preferable. Consider normalising q against the written pulls. No change until diagnosed. | Discount 0 for chains alone is tuning. An **expected value** instead of max, or a discount anchored to hunter-gatherer time-preference evidence, is a general law. | Discount 0 is an ablation, "tuning by extreme". The general-law candidate is **expected rather than max**, since max is optimistic. **But expectation and max share the same fixed point r/(1−γ), so expectation fixes direction, not scale.** The clamp and the estimator are law questions; the discount value is calibration, later. |
| 3. R | Yes, as the next major question, but **a read-only invention-to-remaking audit first**: for each invention, whether the inventor survives, holds or can get the materials, remembers the recipe, meets an opportunity, and chooses to make. Separate no opportunity / opportunity without memory / memory but no attempt / attempt without success. Then a general mechanism (retrieving past successes and an intention to reproduce their observable results). Never reward remaking. | After the diagnosis: a read-only **causal credit audit**. When an inventor's r spikes from using a made thing, does memory keep a back-link to the making? | Lead with R once the diagnosis is in. First, read-only: **R conditional on the recipe still held and the inputs reachable**, separating opportunity (eviction, parts, retrieval) from choice. |
| 4. estimate | 97% (the diagnosis); about 85% (the R audit) | 95% | about 93% (diagnosis); about 88% (R decomposition); about 70% (a later max → expected law test) |

## Checked (the assistant as council)
1. **All three put a read-only diagnosis first and the R audit second.** No nature change until diagnosed.
2. **DeepSeek's fixed-point remark is right, and important.**
   - With max or with an expectation, q tends toward r + 0.8·V(next), which inflates toward r / (1 − 0.8) = 5r.
   - So "expected instead of max" alone cannot remove a scale effect.
   - The diagnosis must separate the two.
3. **Two small slips in DeepSeek's reply:**
   - "all 5 P remakes were by inventors" is PB2's figure (P: 5 of 2,214), not PB3's (P: 1);
   - "PB1b showed averaging beats maxing" overstates PB1b, which compared episodic memory with the habit table, not
     an average with a max.

   Neither changes its advice.
4. **Feasibility.** The choice score in `mind.decide` is `u + 0.6 × qv` per option (u = the written pulls). A read-only
   copy can log u and qv for each considered option, and the next-state term inside `_learn`, without changing any
   choice. A zero check proves it: the world hash must equal v13's.

## Merged plan
**LA1, a read-only diagnosis in two parts.** v13 and c0 worlds on new seeds; a logging-only copy; v13's world
unchanged.
1. **The look-ahead:**
   - saturation (q at the clamp);
   - the habit term against the written pulls in real choices;
   - the next-state term's signed contribution by action and food band;
   - counterfactual re-ranking of logged decisions with q rescaled to the c0 scale, or with the next-state term
     removed (scale against direction).
2. **R decomposition:** for each world-new kind, the inventor's path:
   - alive;
   - recipe still held;
   - inputs held or reachable;
   - a make option offered;
   - chosen.

   In v13 and c0 (GPT, DeepSeek). Gemini's credit back-link goes in as a described measure: the r the inventor got in
   weeks when they used the made thing.
