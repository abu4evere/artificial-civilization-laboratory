# E0 — Baseline Human Predictions (FROZEN)

**Experiment:** E0 — Mind Before Civilization
**Configuration:** 10 founders, 500 simulated days (~71 weeks / ~1.37 years), seed 42, headless, stage E0-D.
**World Bible:** 7.1 · **World:** 0.1 · **Agent:** 0.1

These predictions were written **before** the first E0 run and are now frozen.
They must not be edited after observing results. Each one is a claim about what
the *current* architecture should produce, stated so it can be scored as
**confirmed**, **violated**, or **unresolved**.

The governing question: *does the current agent architecture produce non-trivial
behavior that cannot be explained as simple scripted reactions?*

---

## Predictions for roughly the first 50 simulated days

1. **Survival dominates early action.** The most frequent actions will be
   `forage`, `rest`, `hunt`, `explore`, and `gather` — direct responses to
   hunger, fatigue, and empty local tiles. Rationale: instincts (hunger→forage,
   fatigue→rest) are the strongest unlearned signals, and habits start at zero.

2. **Prediction error will be smallest for survival actions.** Foraging, resting,
   and hunting are driven by a physical model the agent can learn quickly, so
   `|predicted − actual|` should stay low there. This is the "trivial,
   predictable" baseline.

3. **Prediction error will be larger for social actions.** `court`, `give`,
   `attack`, `steal` depend on *another* agent's response, which the current
   agent has no model of. Expect higher error on those when they occur.

4. **Resource-rich areas will attract agents.** Fertile biomes (plains, river)
   will be visited more often than poor ones, because forage yield enters the
   decision score directly and `home` is the place where life has been best.

5. **Repeated successful actions will become more common.** Temporal-difference
   learning on `reward` + mood change should raise the Q-value of actions that
   keep the agent fed and safe, so foraging should rise relative to week 1.

6. **Agents with positive interactions will interact again.** `give`/`care`/`talk`
   raise affection, and affection raises the future utility of those same
   actions toward the same person (friendship as a positive feedback loop).

7. **The two founding bands will not meet.** With 5 people per island and no
   boat in the first 50 days, there will be **zero cross-island contact** and
   no shared knowledge across bands.

8. **Invention will be rare or absent in the first 50 days.** Making a blade,
   carrier, or raft requires gathering materials *and* then playing/making;
   expect **0–1 classified inventions** in this window.

9. **Emotions will track events but stay muted.** Grief on a death, loneliness
   in isolation, a mood dip when hungry — visible, but small, because deaths are
   rare in a 5-person group over ~7 weeks.

10. **Most behavior will be causally traceable.** The majority of actions should
    reduce to a visible cause (hunger, cold, a relationship, a memory, a grudge).
    We do **not** expect many actions with no identifiable trigger; if a large
    share of actions are unexplained, that is itself a finding.

---

## Kill-criterion expectation (written in advance)

**Expected honest outcome:** the *majority* of decisions in E0 will be
need-triggered and predictable (category A high), but a **non-trivial minority**
should already show adaptation (habit change), behavioral reuse (repeated
inventions), and transmission (teaching/copying) — because those systems exist
in the code. If even those do **not** appear, we declare the cognitive
architecture too thin, as instructed, rather than hiding it by adding agents.
