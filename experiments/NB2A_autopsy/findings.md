# NB2-A findings: why did NB2's people die out? (a read-only autopsy; descriptive)

**Status:** final as a description. This autopsy has no blind recompute, because it tests nothing; it counts.

**Validity, with correction 1** (`questions.md`):
- 46 of the 48 exact replays end with NB2's own world fingerprint.
- The 2 that do not (n:25606 and n:25611) also fail to reproduce when NB2's plain runner is replayed with no recorders
  on another machine. So the cause is cross-machine floating-point drift, not the recorders.
- `results.md` reads the 46 exact worlds; `results_all48.md` reads all 48. They tell the same story.

**Code and runs:** NB2's code_nb2, unchanged; arms c (v17's old minds), s (new options, no learning) and n (full NB2);
seeds 25601–25616; cloud-run 42947973136.

## The answer in one line
**No single cause.** People in the neural worlds **kill each other**, children and kin included, without hunger or
grudge. They **starve more** while kin nearby have food to spare. And they **die before old age.** By the frozen rule
neither violence nor starvation alone "drives" the collapse (thresholds: a quarter of deaths, and 5 × v17's share).

## The numbers (46 exact worlds; deaths over whole lives)
**What adults (16 and over) die of:**

| cause | v17 | s | n |
|---|---|---|---|
| killed | 0.5% | 13.3% | **17.7%** |
| starvation | 21% | 33% | 33% |
| old age | **46%** | 22% | 18% |
| illness, thirst, childbirth | about 32% | about 32% | about 31% |

**Teens (12–15):** in n, killed is 33% of their deaths (v17 4%).

**Children under 12:** in n, killed is 6% (v17 0%). Starvation is about 57–62% everywhere.

**Violence:**

| | v17 | s | n |
|---|---|---|---|
| attacks, all worlds | 1,522 | 31,100 | 20,764 |
| … that the old brain would never have offered (grudge ≤ 0.15) | 0% | **64%** | **55%** |
| … against a child under 12 | 0.2% | **20%** | **19%** |
| … against kin | 6% | 19% | 20% |
| … by a hungry attacker | 7% | 3.6% | 3.4% |
| … chosen (not retaliation for a theft) | 68% | 95% | 95% |

**Starvation:**
- everyone who starved held no food, in every arm;
- about a quarter had kin within reach holding more than twice their own need (v17 22%, s 28%, n 23%);
- giving dropped: children 3–11 gave in 3% of weeks (v17 10%); teens 5% (v17 11%).

**What children chose:**
- children 3–11 now explore (22% of weeks) and set off to join others (14%), where v17 children did neither;
- they talk much less (7% against 30%).

(The world moves children under 12 back to their carer every week, so the exploring is mostly a wasted week.)

## What it means (the assistant's reading, for NB3)
- **Violence is the new killer, and it is unprovoked.** Most attacks come with no grudge, no hunger and no
  retaliation, and a fifth hit small children. **The world rewards the attacker every time** (+0.1 per attack). The old brain's
  grudge rule had been hiding that reward.
  - **NB3:** remove the joy of attacking; give an inborn reluctance to harm; give empathy (others' pain hurts) and
    guilt.
- **Hunger is not the motive:** only 3% of attackers were hungry. So "they fight over food" is wrong.
- **Sharing broke down.** People starve next to kin with plenty, and children no longer give or talk.
  - **NB3:** love of one's own child, empathy, and approval for helping.
- **People die before old age** (18% against 46%) because violence and hunger come first.
- **Not covered here:** why the sham s, with learning off, already fails. Its instinct scores are v17's formulas,
  applied to many more options. A rarely-chosen bad option, offered often enough, becomes a frequent act. This is a
  design point for NB3: the inborn reluctance must be strong at birth.
- **The assistant's prior:**
  - violence drives the collapse: 60% (no, by the strict rule, though it is the largest new cause);
  - most attacks would never have been offered by the old brain: 85% (yes: 55–64%);
  - starvation drives it: 35% (no).
