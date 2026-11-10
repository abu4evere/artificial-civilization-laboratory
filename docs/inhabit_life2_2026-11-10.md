# A second hand-played life: p00028, seed 7211, weeks 1040–1053

*Written 10 November 2026, 15:39 (clock from `date`). The creator, 15:35 (Telegram): "Ok do it one more time later i
mean keep living inside acl". This is the second life, after `docs/inhabit_2026-11-10.md` (p00027, seed 7103).*

A probe, not a study: one person, one throwaway world, chosen by hand. Nature is untouched (`acl/` not edited), no
study output was read or written, and nothing here changes the world. The freeze holds: everything below is **noted for
the 7 December review**, not acted on.

Tool: `tools/mind_views/inhabit.py` (built in the previous session). World kept in `research/local/inhabit2/`
(local, gitignored), journal in `research/local/inhabit2/journal.md`.

## Who I was

Seed 7211, run 20 years on its own, then I took the controls of **p00028**, 16 years old, the youngest adult,
population 24, week 1040. Twelve recipes, three things in hand, a thought that said *misses Tholun*.

I set myself one aim and kept it across weeks, which is what the previous life could not test: **build something in
steps, then try to pass it on.**

## The fourteen weeks

| week | what I chose | what it cost me |
|---|---|---|
| 1040 | go to home (join 1,24) | food 14.4 → 6.9 |
| 1041 | gather plants (hungry) | food → 19.4 |
| 1042 | **make a carrier** `(fiber+fiber)#fiber` (contain 70) | food −7.7; fell ill the same week |
| 1043 | **make `((fiber+fiber)#fiber+flint)#fiber`** out of that carrier (contain 93, edge 25, hard 70) | food → 4.3, health −3.5 |
| 1044 | gather plants (food 4.3, ill) | the make options vanished: fiber down to 0.66 |
| 1045 | talk with Tholun | gossip + a vouch + two things learned *from* me |
| 1046–1048 | talk, talk (Dote, Houthair) | food 17.1 → 2.2 |
| 1049 | (index drifted: gathered fiber instead of talking) | food 0.0, health 57.2 |
| 1050–1052 | eat, eat, eat | health back to 61.7 |
| 1052 | **make a club** `(((fiber+fiber)#fiber+flint)#fiber+wood)#fiber` (reach 90, contain 100, hard 70) | food → 4.5 |

Three steps of one project, four weeks apart, each built on the last. **On every one of those three weeks the draw
would have picked `rest`.** Cumulative work inside a life is permitted by nature; it is simply never what the week is
about.

## What living it showed

**1. The teaching channel is mostly not about know-how.** `information.show_how` (line 256) pools *recipes* and
*beliefs* that the teacher values above 0.15, sorts them together, keeps the **top three**, and draws one.

My own pool at week 1046, read out of the saved world:

```
1.000 belief wood@3
0.772 belief flint/stone@1
0.512 recipe flint/stone
0.290 recipe ((fiber+fiber)#fiber+flint)#fiber     <- what I had just built
0.287 recipe (((fiber+fiber)#fiber+wood...)        <- the club
0.209 recipe (flint+flint/stone/stone)#fiber
...  13 things above 0.15, 9 of them recipes
```

So of my nine teachable recipes, **only one can ever reach my mouth**, and two of the three draws are beliefs about
where I once left wood or flint. The thing I built over three weeks sat 5th: unteachable while those two beliefs are in
my head.

**2. This is not just me.** Same world, same week, all 24 living people (read-only):

- 21 have something to teach;
- of their 56 top-three slots, **19 are recipes and 37 are beliefs**;
- **8 of the 21 can never teach a recipe at all** — their whole top three is beliefs.

**3. Why the two scales do not meet.** Belief strength is added up and clamped to ±1 (`knowhow._credit`, line 176:
`clamp(p.beliefs.get(key,0) + change, -1, 1)`), so a belief that keeps being confirmed **saturates at 1.0**. A recipe's
worth moves towards what the week actually felt like (`knowhow.py:56`: `v + rate*(felt - v)`), and a week of making
feels like 0.1 (the rewards I got: make 0.1, forage 0.196–0.3, talk 0.169–0.269). Recipes therefore live near 0.1–0.5
for ever while beliefs climb to 1.0 — and then the two are ranked in one list. That ordering, not language and not
willingness, is what keeps know-how out of talk.

**4. Talk really did carry only news.** The four talks I chose produced: 6 `told` (who was born, who died), 3
`vouched` (what someone is like), and 2 `learn` — a water spot (`g:5,26`) and the belief `flint/stone@1`. No recipe
passed in any of them.

**5. Passing it on costs food.** Three weeks of talking in a row took me from 17.1 food to 0.0 and health 57. A week
of making cost about 7.7 food, the same as a week of talk, while a week of foraging brought 12–24 back. So a person can
build *or* teach *or* eat, one per week, and only the eating is ever urgent. Hunger pushed "talk with Tholun" down to
0.28 while "gather plants" stood at 1.84.

**6. Missing someone does not make you seek them.** Week 1040's loudest thought was *misses Tholun* (pull 1.1). In the
same week's menu, "talk with Tholun" was weighted **below** talking to two people I had no feeling about, and at week
1041, with Tholun standing right there, it was the lowest talk option (0.29 against 0.37). The thought names a person;
the weighing does not use the name.

**7. One honest correction.** I first read the club as *not* in my hands after making it — I had compared a signature
string against item dicts. The club is in my items (`decision.state_snapshot` lists it). Corrected here before it was
written anywhere else.

## Where this leaves things

Points 1, 2, 3 and 6 are mechanisms in the code, not impressions, and each one bears on the creator's open problem:
RF1 found 0 of about 11,500 new kinds was ever made by anyone but its inventor. The last life found that deliberate
making never records what it produced (`actions.py:633`); this life found that even when the recipe *is* recorded and
valued, the one channel for passing it on is two-thirds full of beliefs on a different scale.

Nothing was changed. The world stays v17 and frozen. These go to the **7 December review**, where "the teaching pool
mixes two scales" is the one-line proposal worth testing — and point 6 is brain-shaped, which is where the work already
is.
