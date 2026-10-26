# MK1 debate, round 1 (27 October 2026): why making loses

**Opinions, not sign-off.** The creator set up a debate: GPT and Gemini get the same questions, and Claude is the
council that checks claims against the code and the records. Asked while MK1 was frozen and about to run. Nothing here
changes MK1.

## The claims and what survived checking

| claim | who | council check | result |
|---|---|---|---|
| TD discounting (γ 0.8 a week) is why making loses | Gemini (first view) | Making's score comes mostly from `itemval`, learned per use with no time discount; the TD habit term for make is 0.0004–0.03 | **Wrong; Gemini withdrew it** |
| A novice's tool is worse than bare hands | Gemini (first view) | Quality = (55 + 45 × skill)%; smoke forage tools at skill 0.2–0.35 had factors 1.15–1.21 | **Wrong; withdrawn** |
| Making is scored as a single use's gain against foraging's whole week (a "unit mismatch"): the decision has no term for a tool's stream of future uses against the week given up | Gemini (revised), GPT agrees, Claude agrees | True of the code: worth = felt per use, scaled by 2.0, against forage's full utility | **Stands** (a feature of the code; whether it causes the collapse is MK1's question) |
| The other options' soft maximum rising carries the fall | Gemini and GPT (prediction) | Untested; in the 10-year smoke run U_other was 1.31 and 1.30 in years 0–5 and 5–10 | **Open: MK1 decides** |
| ...because the forage habit compounds through talk-copying | Gemini | The habit term is 0.6 × a value; whether forage's rises is not yet measured | **Open** |
| Learned worth v contributes substantially; the make habit offsets the decline rather than causing it | GPT | LS1: the make habit at 16 *rose* 0.005 → 0.030 | **Consistent with LS1; open for MK1** |
| A big gap explains why making is rare, not why it became rarer; read the change, not the level | GPT | Correct, and already in the frozen plan (Q3 is the early-to-late change) | **Stands** |
| v is a maximum of four sources (worth, part, belief, surprise), so its changes cannot be read as `itemval` alone | GPT | True; MK1 logs v but not which source won | **Stands, as a limitation of MK1** (not addable after freezing; for a follow-up) |

## The predictions on record, before MK1's data
- **Gemini:** the rise in the other options' soft maximum is the primary part of the fall (through foraging habits),
  learned worth v is secondary, and habit and hunger are minor.
- **GPT:** the same ranking (others' soft maximum, then v, hunger, thought, habit), with habit possibly offsetting the
  decline.
- **Claude (frozen prior in questions.md):** the gap is mostly the learned worth term.

## Where the debate agrees
A tool can be useful without making it look worth making. The learning answers "how good was this tool when I used
it", but the decision needs "what will owning it give me, against what I give up now". GPT: "For Bob, that's the
interesting question: can an inhabitant learn to invest effort in something whose value is realized over time, without
us programming what the investment should be?"
