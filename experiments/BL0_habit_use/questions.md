# BL0 — Does ACL's brain meaningfully learn? (APPROVED to run after the existing queue; thresholds await sign-off; not frozen; nothing run)

**Creator's decision (12 October 2026):** BL0 is approved, to run **after the existing queue (WS1 → AA1 → MB1a → ID1)**,
without changing the frozen order. Before it runs, its analysis must (a) separate habit effects on **scores** from
effects on **actual choices**, and (b) separate **individual learning** from **inherited** and **caregiver-shaped**
habits. It must also ask whether habits persist into later life and reach descendants. The design below does all of
these. It is frozen only after the creator signs off the reading thresholds (marked **[sign-off]**).

**Why first.** The fly-brain review (`reports/ACL audit and next phase October 2026.md`, section 7) suggests mechanisms
ACL lacks: forgetting, need-gated use, generalisation. Each only matters if the habits ACL already has change what people
do. "Before making the brain bigger, find out whether the existing brain meaningfully learns." No study so far has
measured this (experiments/INDEX.md).

## What ACL does today (read from the code, 12 October 2026)

- **Score.** Each week every person at least 1 year old scores each option as:
  - *instinct*: hand-written formulas in `mind.decide`;
  - plus `learned_weight` (0.6) × the habit value for (situation, action), with 32 situations × 17 actions = 544
    habits, clipped to ±1.5;
  - plus a bonus from whatever is on their mind (`thought.steer`).
- **Choice.** A softmax at temperature 0.2 over the final scores (`util.softmax_pick`).
- **Three sources of habit change** (each a weighted blend, so each can be followed exactly):
  1. **Inherited:** at birth, habit = ¼ × (mother's + father's); the mother's twice if no father is alive.
  2. **Caregiver-shaped:** under 12, while with the carer, habit ← 0.92 × habit + 0.08 × carer's habit.
  3. **Own experience:** the week's chosen (situation, action) ← 0.95 × habit + 0.05 × (reward + 0.8 × best next value),
     then clipped. A repaid gift adds 0.025 to the giver's give-habit.
- Nothing else changes a habit; unused habits never fade.

## Questions (descriptive; read-only)

**Q1 — Effect on scores versus effect on choices** (the creator's distinction; measured separately, every decision of
every person 1 or more):

- **Score effect:**
  - the learned term's size beside the instinct part (median |learned| / median |instinct|, per action);
  - the share of decisions in which removing the learned term changes **which option scores highest**.
- **Choice effect:** the probability that the actual choice would differ without the learned term. That is the total
  variation distance between the two softmax distributions over the same options, the same thought bonus and the same
  temperature, with and without the learned term. Computed exactly from the scores; no random draw is used or needed.
  This is the primary measure: a habit can shift a score without changing the choice, and a choice can differ even
  when the top option does not.

**Q2 — Where each habit value comes from** (individual learning versus inherited versus caregiver-shaped). Each habit
value is split exactly into three parts that always add up to it: **inherited (I)**, **caregiver (C)**, **own experience
(E)**. Every blend scales all three parts and credits the new term to its source:

- at birth: I = the habit, C = E = 0;
- upbringing: all parts × 0.92, then C += 0.08 × the carer's habit;
- own experience: all parts × 0.95, then E += 0.05 × the target;
- clipping and gift nudges: credited to E.

Reported by age:

- how many of the 544 values have a non-trivial own-experience part (|E| ≥ 0.05);
- each source's share of the habit term in the decisions of Q1, i.e. of the choice effect, attributed by part.

**Q3 — Persistence.**

- **Later life:** for habits a person has stopped using (that action not chosen in that situation for 52 or more
  weeks), the value that remains and its choice effect whenever that situation comes back.
- **Descendants:** similarity (correlation over the 544 values) between a child's habits at 12, 20 and 40 and their
  parents' habits at the child's birth, against a **sham**: a random adult of the same world and year who is not kin.
  And the share of a child's own-experience part that is new, versus the inherited part carrying the parents' own
  experience forward. The **lineage-level** question (does experience accumulate across generations, or merely get
  passed on and diluted?) is the share of an adult's habit term that traces back to the experience of ancestors two or
  more generations up. This is computed by carrying each part's origin generation along with the split; it is the same
  linear bookkeeping, one more field.

**Q4 — Reach and staleness:** how often each of the 32 situations recurs per person-year; weeks since a habit value was
last changed when it is used.

**Q5 — Population and survival** beside each measure (rules 14 and 18).

## How (read-only, as AA1)

- **Code.** A logging copy of the control code, `code_e13r` → `code_bl0`, with hooks in:
  - `mind.decide`: each option's instinct part, learned part and thought bonus, and the chosen index;
  - birth, `_upbringing` and `_learn` (and the gift nudge): the split of Q2.
- **Read-only.** The split and the logs live **outside** the world state, as `code_aa1` keeps `aa1log`. No random draw
  is added, moved or removed.
- **Zero check before any run:** state hashes of two seeds identical with and without the hooks, and identical to the
  control code. Also, for every person each week, I + C + E = the habit value, to 1e-9.
- **Worlds:** F1's 64 seeds and 120 years. Discovery: 501–516 and 601–616. Holdout: 811–818 and 1101–1124.
- **Reported** per world, then the median across worlds with a bootstrap interval (`random.Random(2026)`, as before).

## Reading (operational thresholds, **[sign-off]**)

On Q1's choice effect, the mean over adult decisions, read only where discovery and holdout agree:

- **Habits steer:** ≥ 0.10 (one decision in ten would go differently without them).
- **Habits barely steer:** < 0.02.
- Otherwise **"habits steer a little."**

On Q2, among adults, by each source's share of the habit term:

- **"Mostly learned"** if own experience gives ≥ 50%;
- **"mostly inherited or absorbed"** if it gives < 25%;
- otherwise **"mixed."**

On Q3, for descendants, parents-versus-sham similarity at 20 is reported with its interval; it is described, not
thresholded.

## What it would decide

- **Habits steer, and are mostly learned:** a controlled test of one mechanism (forgetting, need-gating or
  generalisation; report section 7), designed and frozen separately.
- **Habits steer, but are mostly inherited or absorbed:** the habit system is mainly a channel of transmission. The next
  question is cultural (does it accumulate across generations?), and the Q3 lineage measure starts it.
- **Habits barely steer:** no learning mechanism is tested next; the question becomes why (the learned term's size
  against instinct; how rarely situations recur), read-only again.

## Cost and timing

Replays only, about F1's cost (64 worlds × 120 years) plus logging. Runs **after ID1**, in the agreed order.

## What it cannot show

Whether ACL's learning resembles a fly's or a person's. It measures whether, and from where, learned values change
behaviour in ACL.
