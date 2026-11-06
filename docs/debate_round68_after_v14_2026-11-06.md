# Council round 68: the CI1 design, before the freeze (6 November 2026, 04:57)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round68_question_2026-11-06.md` (the same paragraph to all three).
- **The chats:** GPT, the main chat; Gemini 3.1 Pro "High", chat 87f468c684ee5839; DeepSeek, chat 2552dbba.
- **Recorded from the replies read in the chats.** The time in the title is from the clock.

## Answers
| | GPT | Gemini 3.1 Pro | DeepSeek |
|---|---|---|---|
| 1. IN as keeping only | **Yes**, as the first minimal step; another pull would confound. Protect only the quantity the current recipe needs, **including intermediate made parts**. Higher-valued uses and survival override. A complete set is not remaking. Do not add the order of making to CI1 | **Retention only is right.** But **IN must protect the inputs of a missing made part too**, or "the multi-step assembly order will still break" | Right in spirit, **one gap**: the failure is in made parts (10,044 vs 4,071 piece-weeks), and as drafted IN protects one level only. Extend protection one level down, as **a sixth arm IN-nest**. Define "fresh" (held, not worn). Setting down materials the aim does not need must stay allowed, because that frees the carry cap (35% of wanting weeks). No time limit is right |
| 2. LG | **The make option only**; keep material, energy and age limits | **The make option only** | **The make option only**; heat recipes stay out of children's reach (described, for a possible LG2) |
| 3. co-primary | Mechanistic: the share of eligible wanting kinds reaching a complete set; behavioural: remaking within 5 years. Report child and adult inventors separately; define eligibility and deaths consistently | Switch to the funnel (complete set); remaking described | **Replace remaking:** the share of inventor-kinds reaching a complete input set within 5 years, **counted per kind, not per wanting week** (LG changes who invents, so wanting-week denominators are biased). Remaking and "make chosen once complete" described |
| 4. guards | Child deaths: the 1.25 rule, provisionally, plus the absolute excess. **Gifts to kin's children: a fall is the harm**, so below 0.80 with the upper bound below 1. Describe child health and hunger, inventory, care of dependent adults | Child deaths: 1.25 is sound. **Gifts: inverted**, below 0.80 with the upper bound below 1 | **Gifts: a direction error**, below 0.80 with the upper bound below 1. Child deaths: the ratio rule plus an absolute floor (3+ per 1,000 child-years above v14). Add child starvation; describe care given, food per adult and the cap share |
| 5. estimate | 95% valid and informative; about 65% that IN raises complete sets meaningfully; less that it yields deliberate remaking | 95% | about 75% (with IN-nest, the per-kind co-primary and the corrected gift guard) |

## Checked (the assistant as council)
1. **The gift guard's direction was wrong in the question.** All three caught it. Harm is a fall, so the guard is a
   ratio below 0.80 with its upper bound below 1. Corrected.
2. **Nested pieces:** all three, in their own words, want the inputs of a missing made part protected.
   - Gemini and GPT would put this inside IN. DeepSeek would add a sixth arm.
   - **Adopted: inside IN.** IN protects the pieces of the aim's recipe, and also the pieces of any part the recipe
     needs that is missing, one level down. The arm stays one law.
   - The order of making is still not added (GPT).
3. **The primary: DeepSeek's per-kind form is adopted.**
   - The share of world-new kinds whose inventor ever holds the complete input set while knowing the recipe, within 5
     years. The denominator is all kinds, so it is not biased by who reaches a wanting week.
   - Remaking, and "make chosen once complete", are reported beside it, for child and grown inventors apart (GPT).
4. **"Fresh"** means the make option's own test: held with more than 5 uses left (`_holding`). Setting down materials
   the aim does not need stays allowed (DeepSeek).
5. **Guards added:**
   - child deaths: the ratio rule and an absolute floor (3 or more per 1,000 child-years above v14, both needed);
   - child starvation, separately.
   - Described: care given, food per adult, the cap share, child health.

## Merged plan (CI1, to be frozen)
- **Arms:** v14, LG, IN, LG+IN, sham. 32 new seeds; 200 years.
- **LG:** the make option for children 3 and over.
- **IN:** retention only, with one level of nesting and survival uses open.
- **Primary:** the per-kind complete-set share. **Remaking** is reported beside it.
- **Guards:** as corrected above.
