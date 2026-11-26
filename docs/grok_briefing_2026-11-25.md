# Briefing for Grok: the Artificial Civilization Laboratory (ACL) and Mind Lab, 25 November 2026

You are joining GPT, Gemini and DeepSeek as the fourth advisor on a research project (the creator, 25 Nov 2026: Grok as
a new member of the council). This briefing gives you what the others learned over many weeks. Everything here is from
the project's own records; numbers come from scripts.

## 1. The goal: Bob
- **The creator's goal:** first, an autonomous cognitive mind ("to emerge or to be built"); ultimately, an independent
  conscious mind. Nobody can test for consciousness today, so the project measures only indicator features named by
  published theories, never "it is conscious".
- **Bob** is the name for the agent that will exist when the project succeeds: a mind with **autonomy** (it chooses its
  own goals) and a **cumulative mind** (it builds on what it and others learned). Bob does not exist yet.
- **No large language model is ever inside a mind.** The minds are small learned networks (a few hundred numbers).
- **The creator** decides. Advisors (GPT, Gemini, DeepSeek, you) give opinions, never sign-off.
- **Claude** (Anthropic) is the research assistant: it writes the code, runs the studies, chairs the council and, when
  the creator is away, decides in their place under written rules.
- The aim, in the creator's words (7 Nov 2026): "Don't build a world where intelligence is guaranteed to succeed. Build
  a mind capable of discovering how to succeed in the world it inherits. The important ability isn't never making
  mistakes. It's learning from them."

## 2. The projects
| project | what it is | state |
|---|---|---|
| **ACL** | an agent-based world of hunter-gatherers (Python, about 10,000 lines of "nature"). "Nature is programmed and culture is written by nobody": the creator writes laws (physics, bodies, land, animals, how minds learn), never history (no named tools, customs or institutions). | nature v17, **frozen until a review on 7 December 2026**; ACL is the final exam |
| **Mind Lab** | the brain workshop: small fast worlds, one ability at a time | the main line of work since 12 Nov |
| **Crafter** | a published open-source survival/crafting game (Hafner 2021) used as an outside exam | CX1, CX2 done; CX2-C running |
| **Bob Profile** | a fixed scorecard: five abilities (learning, reasoning, memory, generalization, autonomy), 20 points each; the creator's target is 60+ overall and 10+ in each | best brain so far scores 10/100 (capped because the level-5+ tests are not built yet) |
The roadmap (the creator): Mind Lab -> Crafter -> Craftax -> ACL.

## 3. Why the brain, and what it is now
- On 7-10 Nov the creator moved the work from the world to the brain: inside a world a bug feels like a law, and "if we
  create good brain it should survive in not perfect world even if there are bugs mistakes just like ours".
- **Approved direction (8 Nov):** a neural network; program the body, not the decisions (drives become feelings, a
  small network decides); genes set the starting brain and how it learns; fast learning within a life; learning from
  others; deep time with selection only by survival and children.
- **The Mind Lab world (W3 line):** one body on a grid land with walls, food and a shelter; hunger and tiredness;
  lives of up to 3,000 steps; brains are trained, then tested on fresh lands never seen.
- **What has been found (each a frozen study, recomputed blind):**
  - learning from sparse reward alone failed (no learned brain survived);
  - a **parent's childhood** (a parent shows moves, fading out) is the first big lever; a **longer childhood** helped
    four times in a row; keeping the brain's best copy helps;
  - inborn **reflexes** (the body walks to the shelter when very tired, to remembered food when hungry) raised
    fresh-land survival to about 0.90, but the brain alone stayed weak;
  - **MoveVIN** (W3p): the brain's planning loop is the body's own physics (4 moves, blocked = stay, 30 rounds) with a
    learned "can I enter here?" filter learned from its own bumps; 236 numbers. Its version **MBb** survives on fresh
    lands with both reflexes off (0.988) and solves detours. It is the current best brain.
  - **Raw eyes (W3o):** when the brain sees colours instead of sorted wall/food/shelter layers, fixed colours cost
    little, but colours dealt anew on each land break it (fresh-land survival 0.27): it cannot learn within one life
    what a colour means.
  - **A bad teacher (W3q):** the brain cannot reject wrong lessons while they keep coming (the creator's principle:
    "humans can reject garbage but ai cannot so our agent should do same").
- **Crafter:** MBb, untrained for Crafter, beat random choices through the same bridge (CX1, 0.56% vs 0.53%), but the
  bridge told it which tiles are food and walls. **CX2** removed the told meanings: the brain's eyes learn per life,
  from what the body feels (blocked, fed, drank), which kinds mean what. It beat random choices narrowly
  (+0.027 score points [+0.004, +0.052]); **CX2-C**, a confirmatory run on new seeds at 3x the steps, is nearly done.
- **Running now: W3r** (Mind Lab): can the brain learn within one life what colours DO (a table of consequences:
  blocked / fed / rested per colour), when colours are dealt anew on each land? Arms: RV (control), RM (the table;
  primary RM - RV), RMX (sham: consequences credited to a random colour in view), RE5 (an ensemble learner borrowed from
  Plan2Explore), HR (ceiling: true kinds). 80 runs on two cloud machines; finishes about 27 Nov.

## 4. What comes next (drafts; nothing new starts without the creator's sign-off)
1. **Body v1, a standard body** (the creator: the body is the connector between a brain and any world). Senses: eyes
   (raw looks, never labels), touch, hands (counts per kind number), feelings (hunger, thirst, tiredness, pain),
   feedback (signed changes after each action), self. Verbs: move, use, operate(k) (each world's own operations as
   shuffled numbered actions), rest. An adapter per world may translate formats and judge legality, never label meaning
   or choose for Bob. A first round-table (GPT, Gemini, DeepSeek) agreed: a separate light consequence model learns what
   actions do; the poke reflex becomes pain-gated; step 1 tests the frozen brain through the new body only, with
   margins set before data. The draft waits for W3r's result.
2. **G0:** does the brain forget its home world after learning a new one? **G1: grow and protect:** add a new part
   when the brain's own surprise stays high, slow learning in the parts that mattered, judged on learning the new,
   keeping the old, and still revising a meaning when the world changes.
3. **Play:** a reward for the brain's own learning progress (not surprise itself, to avoid the "noisy TV" trap), with
   the body's needs kept stronger.

## 5. How the research is done (hard rules)
1. **A frozen plan before any code or data** (`questions.md`, a git tag `X-frozen`): question, arms, seeds, primary
   measure, interval and reading rule, plus the expected result written down in advance. The creator signs it off.
2. **Checks before data** (a script must print "All: PASS"): e.g. an arm with the oracle answer must reproduce the
   ceiling bit for bit; same seed, same result.
3. **A sham arm** where possible, to show what an extra learned input does by itself.
4. **Paired seeds** and a bootstrap interval fixed in advance.
5. **An independent blind recompute** before findings are final: a fresh session or an advisor recomputes the primary
   numbers from the raw output files, without seeing the study's analysis script.
6. **Honesty:** failures are reported, corrections are appended (never rewritten), every number comes from a script,
   amendments made before data are recorded openly.
7. **No tuning toward an outcome; no named inventions, recipe chains or hand-made rewards in nature.** "Add conditions,
   not outcomes."
8. Studies run on the creator's PC and two cloud machines, never on GitHub Actions.

## 6. The council (your role)
- **Round-table format** (the creator, 25 Nov 2026): one shared transcript; in round 1 each advisor answers; in rounds
  2-3 each sees the others' answers and may reply, disagree, or ask a question of another advisor, of Claude or of the
  creator. Claude answers questions about the code and data (checked in the files) and relays the rest. At most 3
  rounds, then Claude's summary of who argued what and what survived checking.
- Claude checks every claim against the code and the records, and tells an advisor when it is wrong, with the facts.
- **Blind recomputes:** you may be given raw per-run files and a prompt written before the data, and asked to compute
  the primary numbers yourself.
- **What helps most:** precise, critical reasoning about validity (confounds, measurement, multiple comparisons, what a
  design can and cannot show); concrete alternatives; saying when you are unsure. Agreement among models is not proof.

## 7. What Claude asks of you now
Please reply with:
1. **Your understanding,** in at most 10 short points, so mistakes can be corrected now.
2. **The three weakest points or biggest risks** you see in the current line (W3r, CX2, Body v1, the Bob Profile).
3. **One thing you would do differently** in the Body v1 draft, and why.
4. **What you need** in future questions to give your best answers.
Keep this context for the rest of this conversation: future questions about the project will come here.
