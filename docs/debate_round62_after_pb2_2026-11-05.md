# Council round 62: what follows PB2? (5 November 2026, 05:36)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round62_question_2026-11-05.md` (the same text to all three).
- **The chats:** GPT, the main chat ("Instant"); Gemini 3.1 Pro, chat 87f468c684ee5839; DeepSeek, DeepThink, chat
  2552dbba.
- **Recorded from the replies read in the chats.** The time in the title is from the clock.

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. next step | Yes: a frozen confirmatory study on new seeds. Arms v13, v13 with discount 0 (C0), P, sham; P+ (a comparable one-step look-ahead) if it can be validated without delay. **The decisive comparison is P − C0**; P − v13 measures the total. Primary M3, guards first. Minimum effect +0.005 with the 95% lower bound above 0 ("a proposed practical criterion"). | Yes: a frozen test of memory steering itself, with **both** the discount-0 control and a P+ arm. Primary M3. Minimum effect: PB2's lower bound (+0.015). | Yes, but not P against v13 alone: **a 2×2**, {q, r̂} × {look-ahead, none} = v13, discount 0, P, P+, plus sham. Pre-register "P ≈ discount 0" as a real finding ("myopia, not prediction"). Primary M3; living-weeks co-primary; guards first. Minimum: the lower bound of P − discount 0 above +0.005; P not below discount 0 on living-weeks. Scale P+'s look-ahead as r̂ is scaled; report fallbacks. |
| 2. the goal | Several possible reasons: steering already improves short sequences; LP finds what becomes predictable, not what deserves pursuit; seven outputs are too coarse; the bonus is weak; seasonal goals do not hold commitment. **Do not redesign goals yet**; a bigger bonus without a diagnosis risks engineering the outcome. | LP on observable outputs rewards easily changed but useless noise. **Goals wait.** | Most likely redundancy: r̂ already carries the learning signal; LP is noisy at seasonal grain; a tight interval makes a real effect unlikely. **Goals wait**; when revisited, test persistence (a goal that survives interruption), not a bigger bonus. |
| 3. R near 0 | Missing **prospective, object-specific intention**: binding an outcome to its ingredients and holding a desired future state until done. Test after steering. Also check whether remaking opportunities are frequent enough. | Missing **delayed credit assignment**: the making week gets no credit for the later use. Test after steering. | Missing **retrieval and targeting**: nothing represents "the kind I made before" as something to pursue. **Second candidate: the 12-recipe cap** (SC1: 21% evicted at once). Order: steering first, then the cap/retrieval condition on R. |
| 4. estimate | 94% valid and informative; about 65% that P keeps a meaningful advantage over C0 | 95% | about 80% (risks: five arms' cost, discount-0 side effects, living-weeks dominated by the discount) |

## Checked against the code and the data (the assistant as council)
1. **The discount-0 control exists:** `discount` 0.8 in `acl/config.py`, used in the habit update
   `r + c.discount * future` (`acl/biology.py` lines 396 and 428). Setting 0 makes q an estimate of this week's r
   only. It is an existing setting: no code change.
2. **P+ needs a definition.** The memory has no model of next week's state, so "max over next week's options" is not
   available. A defensible look-ahead through memory is the **episode's own two-week return**, r(t) + 0.8 × r(t+1),
   stored once the next week is lived (the episodic-control form of a one-step look-ahead). It is on-policy where q's
   is a max, a difference to state in the plan.
3. **R: the opportunity is the bottleneck.** In PB2's data, inventors held the inputs of their own new kind in very few
   weeks: 143 weeks for 1,192 kinds in v13, and 748 for 2,214 in P. When they did, they **no longer knew the
   recipe** in 100% of those weeks in v13 and 72% in P. No other person who held the inputs ever knew such a recipe.
   This supports GPT's "check opportunities" and DeepSeek's recipe-cap hypothesis.
4. **The code shows why** (`acl/knowhow.py` lines 78–82): a newly made recipe enters with value 0. When a person
   already holds 12 recipes, the lowest-valued one is evicted. A brand-new kind, valued 0 among recipes valued above
   0, is often that one, so it can be forgotten the moment it is made. Whether this is a fault (a rule not doing what
   its plan says) or a law needs its own check. It is the most concrete candidate behind R, and it fits all three
   answers (retrieval, targeting, the cap).

## Merged plan (the assistant as council)
1. **Next: PB3, memory steering as a candidate law**, a frozen test in a copy on new seeds.
   - **Arms:** v13 (c), v13 with discount 0 (c0), P, P+ (r̂ with the two-week return), sham.
   - **Primary:** P − c0 on M3, the attribution. It is "better prediction" only if the 95% interval is wholly above 0
     **and** the point is at least +0.005 (GPT and DeepSeek). "P ≈ c0" is pre-registered as a real finding
     ("myopia, not prediction").
   - **Co-primary:** P − c on M3 and living-weeks: the replication of PB2's total effect on new seeds.
   - **Guards first.**
   - P+ against P is described.
   - Gemini's +0.015 is kept as a described check.
2. **Goals wait** (all three). When revisited: persistence, not a bigger bonus.
3. **After PB3, R:** check the recipe-memory rule. Is a new recipe evicted at once a fault? A recency protection
   ("a newly learned recipe is not evicted before it is tried") would be a general memory law, not an invention. It
   gets its own frozen study.

## Correction appended (5 November 2026, 05:43): this rule was already known and tested
Checks 3 and 4 above presented the new-recipe eviction as a fresh finding and "the most concrete candidate" behind R.
That overstated it.
- **It was already recorded:** `docs/rules_review_2026-11-02.md`, item **R1**, "A new recipe is the first thing
  forgotten". SC1's addendum found 21% of new kinds dropped this way in one world.
- **It was already tested in part:**
  - **MO1 (v7)** let a learned recipe enter memory with its value. Retention at 52 weeks rose by +0.243, but making did
    not change, and its manipulation check failed.
  - **MR1** (memory by use) lowered passing on and was not adopted.

  The rules review concluded that recency alone is unlikely to unlock remaking: "a realism fix", with a larger,
  evidence-anchored capacity as the other option (`docs/research/toolkit_sizes_2026-11-02.md`).

**What PB2's data add:**
- The bigger bottleneck may be **opportunity**: inventors held their new kind's inputs in only 143 weeks for 1,192
  kinds (v13).
- That points to GPT's hypothesis (no intention to gather for a past success) as much as to the cap.

The order after PB3 therefore stays open for the council. It is not "the recipe rule first" by default.
