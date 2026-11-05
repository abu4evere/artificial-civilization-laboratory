# Council round 59: PB1, the shadow brain (4 November 2026, about 18:00; corrected from an estimated "18:30")

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/pb1_design_draft_2026-11-04.md`.
- **The chats:** GPT, the main chat; Gemini `87f468c684ee5839`; DeepSeek `2552dbba-…`.
- **Recorded from the replies read in the chats.**

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| estimate | 94% (methodological, if its safeguards are added) | 95% | about 82% (risks: rare-action bias, a state mismatch in observation, a small adult window) |
| inputs | fair; check each is observable at decision time; **add the target's properties** (striking hard stone against soft material); normalise only with prespecified or past information | fair but incomplete: **add the target's physical properties**, since tool × target is where generalisation lives | fair; add weather, prey on the tile, dependents and partner present, and 1–2 recent actions; **split food into acquisition and consumption** |
| generalisation test | keep unfamiliar (situation, action) primary, but call it **compositional**; mandatory secondary tests: unfamiliar property combinations and unfamiliar places; use a **stronger baseline conditioned on the action** | primary should be **unfamiliar property combinations**: a new (situation, action) may just be a familiar act in another season | keep (situation, action) primary but **stratify**: unfamiliar pairs of common actions primary; rare actions (fill, heat, steal) described; materials and places secondary |
| observed examples | not one-for-one: own only, against own + observed at a **fixed weight of 0.5** (a convention, never tuned); report where observations come from | full weight (1.0): the same physical evidence | full weight as an upper bound, plus a 0.3 sensitivity arm; **observations must use the actor's state, action and outcome**, never the observer's state |
| failures | yes when visible; **output-specific visibility masks**: never infer hidden health, energy, rewards or inventory; never fill the unseen with zero | yes: what does not work is essential negative data | yes when visible (a missed hunt seen); no when hidden; a visibility flag from the observer's own perception |
| other | predict before updating; no leakage between shadow models in one world (normalisation, initialisation); **one primary contrast**, with architectures and observation secondary and multiplicity-aware; report skill per output | — | report skill per output (affection could dominate a summed error); report the followed-adult count and prequential weeks; a headroom check on the baseline's own error |

## Checked and merged (the assistant as council)
1. **Target properties: added** (GPT and Gemini agree).
   - **Gather:** the raw material's own property values.
   - **Forage and hunt:** the target tile's plants and prey.
   - **Social acts:** the relation to the target person (affection, trust, familiarity).
   - **Make:** the known properties of the recipe's result.
   - **Other acts:** none.
2. **The primary test:**
   - **Primary:** unfamiliar (situation, action) pairs among the **common** actions (forage, gather, give, talk, put,
     join, rest, take, care, make). This keeps a large sample (DeepSeek) and is what PB2 needs (GPT).
   - **Mandatory secondary:** unfamiliar property combinations (Gemini, GPT), described with its own interval.
   - **Described:** unfamiliar places, and rare actions.
3. **The baseline:** the habit-table baseline **with an action-conditioned fallback** (GPT). For a pair never lived,
   it uses the person's own mean for that action, or the overall mean if the action was never taken.
4. **The primary contrast** (GPT: one, pre-specified): **L-own** (linear, own experience only) against that baseline.
   It is the minimal brain from one life. N-own, L-obs (weight 1.0), L-obs-0.5 and N-obs are secondary.
5. **Observation:** the actor's state, action and outcome, with output-specific visibility.
   - **Visible:** distance moved, things held, a new kind made, raw materials held, food gained by the action.
   - **Hidden:** health, energy, affection, food eaten.
   - Hidden outputs are left out of the update, never set to zero.
   - Visible failures are kept.
6. **Food is split:** food gained by the week's own action, and the net change in edible food.
7. **Inputs added:** rain this week, prey on the tile, dependents and partner within reach, the last 2 actions.
8. **Prequential integrity:**
   - outputs are standardised by a running, past-only spread per world;
   - weights start at 0 (linear) or from a fixed seeded draw (network);
   - nothing is shared between people.
9. **Reported per output,** with the followed-adult count, prequential weeks, and the baseline's own error (headroom).
