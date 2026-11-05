# Council round 61: PB2, the episodic brain helps choose (4 November 2026)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/pb2_design_draft_2026-11-05.md`.
- **The chats:** GPT, the main chat; Gemini `87f468c684ee5839`; DeepSeek `2552dbba-…`.
- **Recorded from the replies read in the chats.** The time comes from the commit (see git log).

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| estimate | (none given) | 90% | about 72% (risks: look-ahead and scale confounds, a smuggled output, the window) |
| steering | replace q (adding both double-counts, with an arbitrary mix). But PB1b validated observable changes, not r: **first a read-only check that r̂ predicts r better than q does**. **Others' internal rewards are not observable**, so r̂ comes from personal experience only. If r̂ fails, PB2's P is not a test of predictive steering | replace q; fall back to q only where the memory is empty | replace q, like for like, but two confounds: **(i) look-ahead**: q has a max look-ahead and r̂ has none, so add a described P+ with one-step look-ahead; **(ii) scale**: normalise r̂ to q's scale by a fixed running-spread rule (the temperature was set for q); report the share of fallbacks |
| the goal | learning progress is general, but (1) the 9 outputs are the researcher's choice; (2) "always reward positive change" confuses progress with wanting more: **let progress select a change with its direction, grounded in experienced outcomes**; a separate commitment rule; a bonus-off control | a general autotelic law; the curiosity-sized bonus is defensible | **leave "a new kind made" out of the goal outputs** (it would value invention explicitly) and distance (not a state); an LP floor (adopt only above noise) and a patience rule; the curiosity-sized bonus is defensible |
| primary | **M3** (ends-directed chains), M5 secondary; R and M2 secondary. Intent checks: preparation against matched controls, persistence, a targeted goal-memory deletion against a sham deletion. Contrasts P − c (steering), G − P and G − G0 (goals) | **R** (remaking on purpose), with above-chance and preparation tests | **M3/M5 primary**, R co-primary with intent tests 1–3 (the memory-removal test belongs to a later study); M2 described; "M3 up, R null" is a real finding |
| window | brains active from year 100, observed to year 150; say whether memories start empty; prefer agents born with the brain, measured after enough learning | from year 100 to 150 | on at year 100, measured in years 130–200; those alive at 100 start empty (report apart); cap memory; time a smoke run first |

## Checked and merged (the assistant as council)
1. **Steering: replace q by r̂** (all three).
   - **r̂ from personal experience only** (GPT): observed weeks carry no r, which is hidden, as in PB1b's masks.
   - **Scale:** r̂ is normalised to q's running spread by a fixed rule (DeepSeek).
   - **Look-ahead:** a described arm P+ adds a one-step look-ahead (DeepSeek's confound check).
   - **A validity check in arm c (GPT):** a shadow r̂ is scored prequentially against q as predictors of r. If r̂ is
     not better, P is reported as "not a test of predictive steering".
2. **The goal:**
   - **"a new kind made" and distance are removed** from the goal outputs (DeepSeek); invention is never a goal
     dimension. That leaves 7: food gained, net food, health, energy, materials, things held, affection;
   - **direction:** the goal is (output, sign). The sign is the one the person's own experience links with higher r
     (GPT);
   - **adoption:** only if LP is above a noise floor; at most one change per season (patience);
   - **the bonus:** the curiosity pull's size (all three accept it);
   - **controls:** a bonus-off control is P itself; G0 keeps random goals.
3. **The primary: M3 (ends-directed chains)**, with M5 secondary (GPT and DeepSeek; Gemini wanted R).
   - **R (remaking on purpose) is co-primary,** with intent tests 1–3 frozen now: above chance against matched
     non-inventors, preparation, and persistence (DeepSeek). The memory-removal test goes to a later study (PB3).
   - "M3 up, R null" counts as a real finding.
4. **The window:**
   - brains are switched on at **year 100** in every arm except c and the sham;
   - memories start empty; the run goes to **year 170**;
   - the primary is measured in **years 130–170**, so most adults have had at least 30 years with the brain;
   - people born after year 100 are reported apart (GPT: born with the brain).
5. **Before the cloud:** a timed smoke run (DeepSeek) and a capped memory (PB1b's 1,000 observed entries per action).
