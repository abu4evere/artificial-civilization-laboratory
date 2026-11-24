# BX1 Phase A findings (exploratory, labelled; 23 Nov 2026)

One ACL person's "where" from Mind Lab's best brain (MBb, fixed weights, the quick adapter), among old-mind people.
Each world runs twice from the same seed: OLD (that person on the old mind) and NEW (on the brain). Not a frozen study.

## Founder version (the brain given to an adult founder from year 0; `run_watch.py`, 5 worlds x 60 years)
| world | OLD: years lived | NEW: years lived |
|---|---|---|
| 101 | 2 (thirst) | 1 (starvation) |
| 2026 | 8 (starvation) | 7 (starvation) |
| 42 | 16 (starvation) | 2 (starvation) |
| 555 | 9 (thirst) | 3 (starvation) |
| 7 | 29 (starvation) | 16 (starvation) |
| mean | 12.8 | 5.8 |
The brain founder lived shorter in all 5 worlds, almost always starving.

## Newborn version (the creator: "from born to grown up"; the world's first baby gets the brain from birth;
`run_newborn.py`, 5 worlds x 80 years)
| world, baby | OLD: age reached | NEW: age reached |
|---|---|---|
| 101, Soubom | 23.4 (starvation; 2 children) | 12.4 (starvation) |
| 2026, Theithethour | 35.9 (starvation) | 4.2 (illness) |
| 42, Sira | 66.0 (old age) | 3.2 (starvation) |
| 555, Sailai | 26.5 (starvation) | 26.1 (starvation) |
| 7, Baneiras | 4.8 (illness) | 21.2 (thirst; 1 child) |
| mean | 31.3 | 13.4 |
- The brain child's most common thought, in every world: "hungry; where is food?".

## What it means
1. **The fixed Mind Lab brain does not fit ACL.** Raised where food is rare (small patches), dropped where food is
   everywhere, its "worth" does not point to good foraging (the bridge test: empty ground worth more than food tiles).
   Adults on it starve sooner (5 of 5 worlds).
2. **One life at a time is too noisy to judge a brain.** Once one person chooses differently, the whole world takes a
   different path (other births, illnesses, weather draws): two brain babies died as toddlers (3.2 and 4.2), before
   the brain steers much at all (toddlers mostly rest and babble; Sira made 1 tile choice). The old twin in world 7
   died of illness at 4.8. These deaths are the world's chaos, not the brain's choices. Phase A shows *how* the agent
   lives; *whether* a brain is better needs many worlds and statistics (Phase B).
3. **Next:** a brain that LEARNS inside ACL as it grows (its own life plus its parent, the Mind Lab recipe), so it
   learns ACL's food instead of carrying Mind Lab's; then Phase B with that brain.

Speed: 0.013-0.016 s per week with one brain agent; Phase B (everyone) is affordable.

# BX1 Phase A2: the learning brain's school (exploratory, labelled; 23-24 Nov 2026)
The creator: "yes build the learning brain". The brain (from MBb, like genes) lived 300 lives, each as the first baby
of a new world (seeds 10001-10300), learning each week from its own feeling at the place it chose and from its
caregiver's while a child (value steps, Mind Lab's LR 0.01, clip 1.0). The old mind ran the same worlds (lives 1-112
on the PC; 201-300 on Oracle, pending). All numbers: `analyse_school.py` -> `output/analyse_school_300.txt`.

| lives | mean age at death | reached 16 | prediction error |
|---|---|---|---|
| 1-50 | 18.9 | 28/50 | 0.0217 |
| 51-100 | 15.9 | 21/50 | 0.0129 |
| 101-150 | 19.2 | 23/50 | 0.0110 |
| 151-200 | 27.8 | 30/50 | 0.0095 |
| 201-250 | 22.1 | 25/50 | 0.0097 |
| 251-300 | 35.0 | 37/50 | 0.0071 |

- Trend: +6.5 years per 100 lives (95% bootstrap +4.0 to +9.1; n = 300 lives). But every life is a different world.
- Paired with the old mind on the same worlds (lives 1-112): brain 18.2 y vs old mind 29.8 y; difference -11.6
  (-16.0 to -7.2); the gap's trend +10.3 y per 100 lives (-4.3 to +25.3: unclear).
- Deaths (lives 1-112): brain starvation 53, thirst 28, illness 14, neglect 11, killed 3; old mind starvation 39,
  old age 23, thirst 20, neglect 14, illness 12.
- **Reading (provisional):** the brain gets better at predicting its weeks and its lives grow longer over the school,
  but the rise may be partly the worlds. The fair test is running (questions.md addendum, written before its data):
  the school brain FIXED vs the old mind vs the untrained MBb on 150 new worlds, paired; plus the old mind on school
  lives 201-300. Its findings will be appended here.
