# N1 — What should a satisfied person feel? Candidates (design document, not frozen)

**Written:** October 2026, after U1. **No code, no experiments.** Asked by the creator: list every plausible
interpretation of what a satisfied person should feel, and judge each against ACL's founding rule (nature is
programmed; culture is written by nobody) before anyone touches code.

## Why this question

U1 traced the chain from E8 to one line of nature. In ACL, hunger is `1 − weeks of food ÷ 2` (counting dependents'
need and one's own stashes nearby): it reaches **zero at two weeks of food**. The pull to forage is `0.25 + 1.6 ×
hunger`, so at two weeks it falls to its floor and talking, joining and giving outscore it. People forage in 86% of
autumn weeks with under half a week of food and in 6% with two to four weeks. Stashing becomes possible above exactly
the same line. **People stop gathering where storing could begin.**

That two-week line is itself a design choice, written when ACL's needs were first built. It is nature in ACL, and like
all nature in ACL it can be wrong. The question is what should replace it, if anything, without writing in the answer.

## How each candidate is judged

- **Nature?** Is it a property of bodies, needs, feelings or capacities that a person would have before any culture?
- **Culture?** Is it something people learn from each other, which ACL must leave to emerge?
- **Scripting risk:** does it encode knowledge of winter, of storage, or of what to do? (none / low / medium / high)
- **Human capacity?** Is it something humans plausibly have? Evidence strength: strong / plausible / weak. *Every
  statement about humans below is general knowledge, not a checked citation; each must be checked before any design is
  frozen.*
- **Leak:** would it change the behaviour of someone who has never gone short? (A capacity should change behaviour
  through experience or need, not by itself pointing at winter.)

---

## C0 — Keep it as it is

Hunger is zero at two weeks of food.

- **Nature:** yes (it is the current nature). **Culture:** no. **Scripting:** none.
- **Human capacity:** weak as a description. Human hunger is felt in the body over hours and days, not as a count of
  weeks of food in hand. ACL's "hunger" already mixes two different things: the body's hunger and worry about food.
- **Note:** keeping it is a choice too. The two-week line was not set from human evidence; it was set to make early
  worlds work. Keeping it means accepting that ACL's people, by construction, cannot feel any reason to gather beyond
  two weeks unless something else (like E9's anticipation) pushes them.

## C1 — A longer, fixed satiety horizon

Hunger reaches zero at N weeks of food instead of two (for example four or eight).

- **Nature:** yes, it is a parameter of the same feeling. **Culture:** no. **Scripting:** low in form (no winter, no
  storage in it), **high in practice**: any N is a dial, and choosing N by what produces storage would be writing the
  answer in through a number.
- **Human capacity:** weak. Nobody's body hungers with three weeks of food in the store.
- **Leak:** yes. It changes everyone at once, whatever they have lived.
- **Verdict:** possible only if N is fixed by an argument made before any result, never tuned. The weakest of the
  nature candidates because it has no human basis of its own.

## C2 — Two drives: the body's hunger and food security

Split the current hunger into (a) **body hunger**, short-term, felt when one has not eaten enough this week, and (b)
**food security**, a weaker, separate wish to hold food, which falls slowly as stock rises and never reaches exactly
zero.

- **Nature:** yes. Both are dispositions, not knowledge. **Culture:** no, though *what* people do about insecurity
  would be learned. **Scripting:** medium. A built-in wish to hold food is close to a wish to store; it is not tied to
  any season, but it leans toward the behaviour being studied.
- **Human capacity:** plausible. Worry about having enough food is a widely described human experience, separate from
  the hunger of the moment.
- **Leak:** yes, mildly. It applies to everyone, all year.
- **Verdict:** a serious candidate, but the strength of the security drive would again be a number that could be tuned
  toward the answer; it must be set by argument, not results.

## C3 — Smooth satiety: never quite zero

Keep one hunger, but let the pull of more food fade smoothly with stock instead of stopping dead at two weeks: each
extra week of food is worth less than the last, never nothing.

- **Nature:** yes. **Culture:** no. **Scripting:** low. It encodes nothing about winter or storage; it only removes a
  hard edge.
- **Human capacity:** plausible. Diminishing value of more of the same good is a general feature of human wanting.
- **Leak:** small, and the same for everyone.
- **Verdict:** the least scripted change to the feeling itself. Its effect may be small; that would itself be a
  finding (the edge was not the cause).

## C4 — Insecurity learned from one's own swings

People who have lived through swings in their food feel less satisfied by the same stock; people who never have, feel
as now. A generalisation of E9's anticipation (A2), which already learns from going short, but without the season.

- **Nature:** the capacity is nature; its content is learned from experience. **Culture:** no, but it is the kind of
  thing culture could later carry. **Scripting:** low.
- **Human capacity:** plausible. People who have lived through hunger often hold food differently afterwards.
- **Leak:** none by design. Someone who has never gone short behaves exactly as now. This is the only candidate with a
  built-in leak test, as E9 had.
- **Verdict:** strong on the founding rule. But E9 showed the weakness of experience-based lessons in ACL: they are
  strong but rare, and they erase themselves when they succeed (E9.4). Without the season it may also be faint.

## C5 — Carers feel further ahead

Satiety for a person with dependents fades over a longer horizon than for a person alone, because they feed others.

- **Nature:** yes. Parental care is already built into ACL. **Culture:** no. **Scripting:** low to medium.
- **Human capacity:** plausible. Provisioning for dependents is a widespread human pattern.
- **Leak:** changes carers whatever they have lived.
- **Note:** ACL's hunger already counts dependents' need, so a carer's two weeks is two weeks for the household. This
  candidate would add a further, unexplained lengthening; it needs a reason beyond "carers worry more".

## C6 — A seasonal instinct

Some built-in sense that the season is turning (shorter days, cooling) makes people want to gather more, as caching
animals do.

- **Nature:** in some animals, yes. **Culture:** for humans, knowledge of seasons and of what to do about them is
  largely learned. **Scripting:** **high.** It points directly at winter and at gathering for it.
- **Human capacity:** weak as an inborn drive. Human preparation for winter is generally understood as learned.
- **Leak:** total. Everyone prepares, whatever they have lived.
- **Verdict:** **rejected.** It writes in exactly the behaviour ACL exists to see emerge.

## C7 — Holding food feels good

Having food in hand gives a small, steady sense of wellbeing each week, apart from hunger.

- **Nature:** plausible as a feeling. **Culture:** no. **Scripting:** medium. It rewards holding food at all times,
  which is close to rewarding storage directly.
- **Human capacity:** plausible but hard to separate from C2.
- **Leak:** everyone.
- **Verdict:** a variant of C2 that acts through reward instead of pull. Weaker on the rule than C2 because it is a
  direct reward for the behaviour being studied.

## C8 — The feeling is fine; the mind's horizon is short

Do not change satiety. Instead let people link what they do now to what happens months later (a longer memory for
causes, or learning that reaches further back than the current habit learner's few weeks; E6.6 measured about five).

- **Nature:** yes, a cognitive capacity. **Culture:** no, though such links are what culture can later carry.
  **Scripting:** low. It encodes no particular link.
- **Human capacity:** strong. Humans can connect causes and effects separated by seasons.
- **Leak:** none by design. Someone only learns a long link if they live through one.
- **Verdict:** not an answer to "what should a satisfied person feel", but a real alternative interpretation of U1: the
  stop at two weeks may be the right feeling with too short a mind. Worth keeping beside the satiety candidates.

## C9 — Holding food brings standing

People respect those who hold food.

- **Nature:** no. **Culture:** yes. What a people respects is culture. **Scripting:** high.
- **Verdict:** **rejected** as nature. If it appears, it should emerge.

## C10 — Make gathering cheaper or the alternatives dearer

Change the cost of foraging, or weaken talking, joining and giving.

- **Nature:** yes (costs are physics and body). **Scripting:** medium. It reshapes the competition to produce the
  answer, without any human reason for the new numbers.
- **Verdict:** **not a satiety candidate.** Listed so it is not mistaken for one.

## C11 — The body as a store

Food eaten beyond need is kept in the body as reserve (fat), and burned when food runs short.

- **Nature:** strongly yes. It is physiology. **Culture:** no. **Scripting:** low. It encodes nothing about winter or
  storage; a body stores whatever it is given.
- **Human capacity:** strong. Human bodies store energy in good times and draw on it in lean ones.
- **Leak:** everyone, but only through eating more when food is plentiful, which they already decide by hunger.
- **Risk:** it gives people a **non-cultural store**. It may soften winter without anyone learning anything, which could
  *reduce* the pressure that makes cultural storage worth inventing. It would also need hunger to be redefined around
  the body's reserve instead of food in hand.
- **Verdict:** the most clearly natural candidate. It does not answer the creator's question directly (it is about the
  body, not the feeling), but it changes what "satisfied" means.

## C12 — Separate the stash line from the satiety line

Let a stash be possible below two weeks of food, so the two thresholds no longer coincide.

- **Nature:** no. It is a decision rule in the code. **Scripting:** low to medium.
- **Verdict:** **not a satiety candidate.** It belongs with S1's gates (eligibility, the shared put slot). Listed
  because U1 found the two lines coincide.

---

## Summary

| | candidate | nature | culture | scripting risk | human capacity | leak |
|---|---|---|---|---|---|---|
| C0 | keep as is | yes | no | none | weak | none (status quo) |
| C1 | longer fixed horizon | yes | no | low in form, high in practice | weak | everyone |
| C2 | body hunger + food security | yes | no | medium | plausible | everyone, mild |
| C3 | smooth satiety, never zero | yes | no | low | plausible | small |
| C4 | insecurity learned from own swings | capacity yes, content learned | no | low | plausible | **none** |
| C5 | carers feel further ahead | yes | no | low–medium | plausible | carers |
| C6 | seasonal instinct | animals only | for humans, learned | **high** | weak | total — **rejected** |
| C7 | holding food feels good | plausible | no | medium | plausible | everyone |
| C8 | longer mind horizon (not satiety) | yes | no | low | strong | **none** |
| C9 | food brings standing | no | **yes** | high | — | **rejected** |
| C10 | cheaper gathering (not satiety) | yes | no | medium | — | not satiety |
| C11 | the body as a store | **strongly yes** | no | low | **strong** | everyone, via eating |
| C12 | separate stash line (not satiety) | no (code rule) | no | low–medium | — | not satiety |

## Assistant's view (the creator decides)

On the founding rule alone, four stand out:
- **C3 (smooth satiety)** is the smallest change to the feeling itself, with the lowest scripting risk.
- **C4 (insecurity learned from experience)** is the only satiety candidate with no leak by design, but it inherits
  E9's weakness: lessons from suffering are rare and erase themselves.
- **C11 (the body as a store)** is the most clearly natural, but it may relieve the very pressure that makes cultural
  storage worth inventing.
- **C8 (a longer mind)** is not about satiety at all, but it is the strongest alternative reading of U1.

**C6 and C9 are rejected:** they write in the behaviour or the culture.

**Rules for any next step, whichever is chosen:**
1. Any number in a chosen candidate is fixed by an argument written before any result, never tuned to produce storage.
2. A pre-registration with frozen predictions, a pilot, a leak test that cannot come out empty, a zero check, and the
   usual reading order, as for every experiment since E9.
3. A candidate that leaks (changes people who have never gone short) must say so in its pre-registration, and its
   conclusion must be capped accordingly.
4. The human-capacity claims above must be checked against sources before the design is frozen.
