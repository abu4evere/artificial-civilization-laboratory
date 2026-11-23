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
