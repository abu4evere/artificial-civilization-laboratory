# E13 — Following a visible, respected example: candidates (design document, not frozen)

**Written:** 2026-10-06, after E12. No E13 code exists. For the creator to choose from after the pilot below.

## Why

E12 found every ingredient of social influence in place except transmission: planners were more visible than most,
fed more people, gained respect and trust faster, and protected their children, and nobody around them changed. ACL's
people can copy a recipe by watching (rafts and hunts only), and children absorb their carers' habits; a planner's
preparation lived in an expectation that no channel carries. The creator's rule for E13: copy **observable behaviour
only**, never the expectation behind it. The learner does not know why; only that people who do well tend to do this.

## Two facts from the code that shape every candidate

- **Habits know the season.** A habit (`p.q`) is a learned value for each action in each of 32 situations: food in hand
  (4 levels: under half a week, under 2 weeks, under 6, more), company or not, and season. "Forage in autumn with
  weeks of food in hand" is a single situation a habit can hold.
- **Habits learn from near-term reward.** Each week's habit update counts next week at 0.8; E6.6 measured that a reward
  more than about 5 weeks away barely registers. Preparation pays in winter, months after the autumn foraging. So the
  planners' own habits may not hold any lesson that preparing pays; they may even hold that foraging while stocked is
  barely worth it. **Any candidate that copies habits or learned values could spread the wrong lesson.** The pilot
  measures this before anything is chosen.

## Candidates

### B1 — Doing what respected people are doing (imitation in the moment)
- **Change:** when choosing, a person feels a pull toward an action that respected adults within sight are doing that
  week, in proportion to how much they respect them. Nothing is learned; it acts only while the example is visible.
- **Copies:** observable actions only.
- **Strength:** does not depend on habits at all, so the short-horizon problem does not apply.
- **Risk:** it spreads whatever respected people do, not only preparing; it lasts only while models are there, so it
  may not outlive the planners.

### B2 — Learning from the outcomes of those who do well (prestige-biased vicarious learning)
- **Change:** when a person sees someone who visibly does well (well fed, children alive, respected) take an action, they
  update their own habit for that action in that situation using the outcome they can see, as if they had done it
  themselves. Only from people who do well.
- **Copies:** observed actions and their visible results.
- **Strength:** chooses models by success, which E12 measured is visible; lasts, because it is learned.
- **Risk:** the visible outcome of autumn foraging is a little more food now, not survival months later; with the habit
  horizon as it is, the lesson that reaches the learner may be weak.

### B3 — Adults absorb respected adults' habits (upbringing extended)
- **Change:** as children already do with their carers, adults slowly move their habits toward those of respected adults
  they spend time with.
- **Copies:** habits, not expectations.
- **Strength:** reuses an existing mechanism with its existing rate.
- **Risk:** copies internal values rather than visible behaviour, which bends the creator's rule; and if planners' habits
  do not hold the lesson (see above), it copies nothing useful.

## Pilot (read-only), to run before choosing

On the E9 A2-full worlds, where the planners lived:
1. **What do planners' habits say?** Their habit value for foraging in autumn situations with 2+ weeks of food,
   against comparison adults'. If it is no higher, B2 and B3 would not carry preparation.
2. **How often is a planner seen foraging in autumn?** Adult-weeks in which a non-planner is within sight of a planner
   who is foraging that week. This is the raw material for B1 and B2.
3. **Who would be a model under B2?** How often planners are among the best fed and most respected of those around them.

## Pilot results (read-only, 2026-10-06)

`run_pilot.py` on the E9 A2-full worlds (probe read-only; all four replays matched E9):

1. **Planners' habits do hold the lesson, modestly.** Their habit value for foraging in autumn with 2+ weeks of food
   averaged 0.28 (n = 113) against 0.20 for comparison adults (n = 6,601). The concern above was too pessimistic:
   foraging still brings a small immediate reward, and planners did it often enough that their habits moved. B2 and B3
   are not ruled out.
2. **The raw material is thin.** 2.3% of adult autumn-weeks are spent within sight of a planner who is foraging that week.
3. **Who would be a model depends on what "doing well" means.** Planners were the best-fed adult within sight 72% of the
   time (n = 29 mid-autumn samples), but the most respected only 3%. Respect in ACL builds over years of relationships;
   a planner is an ordinary person after one hard winter. **A prestige bias based on respect would almost never pick the
   planners; one based on visible success (being well fed) would pick them most of the time.**

## Assistant's view (the creator decides)

B2 matches what E12 measured and the creator's preference, and the pilot leaves it standing, with one design
consequence: models should be chosen by **visible success** (food in hand, children alive), not by accumulated respect.
B1 remains the cleanest test of pure behaviour-copying. Both act on thin raw material (2.3% of autumn-weeks), so an
effect, if any, may be small at first.
