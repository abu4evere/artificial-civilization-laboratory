# The laws of ACL's nature, version 7 (as the code actually works, 27 October 2026)

Written in plain words from the live code (`acl/`, nature v7, live since 25 October 2026), for review by the creator, GPT
and Gemini. "Laws" means the rules the world and minds follow. Nobody scripts what people do. Numbers in brackets are
the code's settings.

## Part A — World laws (body and nature)

**Time and space**
1. **Time.** One step is one week; 52 weeks make a year. Time only goes forward.
2. **Space.**
   - The world is a grid of tiles (80 × 80 in our studies) with land, water, rock and climate bands.
   - People move tile by tile (they can act within 3 tiles in a week and see 4).
   - Water stops anyone without something that floats.
3. **Seasons and weather.**
   - Four seasons. Rain and cold change week by week and by place.
   - Water sources can dry up.

**Body**

4. **Food.** People need food every week; more when growing, pregnant or feeding children. Plants grow on tiles; animals
   live, move and breed (fauna).
5. **Water.** People drink from fresh water within 2 tiles. Without it they get thirsty and are hurt.
6. **Warmth.** Cold hurts. Shelter, fire, clothes and a heap of things kept warm all help.
7. **Health and death.**
   - Health falls from hunger, thirst, cold, injury, illness and old age, and rises with rest and food.
   - People die of these, in childbirth, or by violence. Lifespans are human-like.
8. **Birth.**
   - Couples have children: twins sometimes (v7), and boys slightly more often than girls.
   - A child is cared for by a carer (usually the mother) until 12.
9. **Inheritance of temperament.**
   - A child gets 8 traits: curiosity, diligence, sociability, kindness, temper, anxiety, care and boldness.
   - Each is the parents' average plus a small random change (sd 0.08).
   - **How people learn is NOT inherited:** it is the same for everyone.
10. **Bodies stay.**
    - The dead leave a body, with their food and tools, which rots by warmth.
    - The hungry can eat from it; kin can take the tools.

**Matter and making**

11. **Materials.** Stone, flint, bone, wood, fiber, hide, clay and char can be gathered.
12. **Making.**
    - Things are made by recipes: striking one thing with another, shaping, binding two parts with a binder, and
      heating in fire.
    - Made things have real properties (edge, weight, and so on) that decide how much they help a use: foraging,
      hunting, wood, stone, fiber, fighting, carrying and cold.
    - **No invention is named or scripted:** what works is found by trying.
13. **Wear and carrying.**
    - Tools wear out with use.
    - A person carries at most **3 made things in total**. When a 4th is made, the least valued **vanishes** (it is
      deleted, not dropped).
14. **Fire.** Fire can be made from sparks (struck flint), kept, and used to heat, cook and harden.
15. **Places.**
    - **Food and seeds** can be set down (a stash, or sown) and food found and taken later.
    - **Raw materials** can be put on a pile (it gives warmth, or feeds a fire), but **cannot be gathered back from the
      pile**.
    - **Made things cannot be set down at all**: there is no law for leaving a tool somewhere.
    - Pits can be dug to hide food and keep it longer.
    - Others can take what was left, which is stealing if it is someone else's.

## Part B — Mind laws (how people choose, learn and share)

**Choosing**

16. **Each week a person chooses one action** from 19 kinds:

    rest, forage, hunt, gather, put, take, make, play, explore, give, care, talk, court, steal, attack, flee, join,
    heat, fill.

    For each possible action and target, a score adds up:
    - **built-in pulls**, from needs (hunger, thirst, cold, tiredness, loneliness), temperament and what is in reach;
    - **learned habit** (law 18) × 0.6;
    - **what is on their mind** (law 23).

    The choice is random but leans strongly to high scores ("softmax", temperature 0.2). Only the 12 nearest people are
    considered as targets.
17. **Situations.** People sort their week into 32 situations:
    - how much food they have (4 levels);
    - whether anyone is near (2);
    - the season (4).

**Learning from experience**

18. **Habits.**
    - Each person has a habit value for every situation × action (32 × 19 = 608 values).
    - Each week the value of what they just did moves 5% towards: this week's reward + 0.8 × the best habit value in
      next week's situation.
    - The reward includes how mood changed.
    - This is standard "Q-learning" (TD).
19. **Worth of things.** People learn how much each kind of thing they hold or make is worth from using it. A tool
    that helps is valued up; one that does not is valued down.
20. **Places and placements.** People link what they left somewhere to what happened there (rate 0.25), and learn good
    and bad spots.
21. **Expectations.** People remember seasons when they went short and feel the next one coming.
22. **Surprise and puzzles (curiosity).**
    - A big gap between what was expected and what happened becomes a "puzzle".
    - Puzzles pull attention and lead to trying related things, until they fade.
23. **Attention.** A few thoughts hold a person's mind each week (needs, puzzles, loved ones, things told) and make
    related actions more attractive. Too long on one thing means "overthinking", which lowers how much they believe
    others.
24. **Trying new things.**
    - Untried recipes and things have a "pull of the new".
    - Play is trying combinations of materials; new things are found this way.
    - Exploring visits new places.

**Learning from others**

25. **Copying habits in talk** (`_imitate`).
    - When two people talk, the listener copies the speaker's habits if they respect the speaker (≥ 0.2) or the
      speaker seems happier.
    - **All 608 habit values** move towards the speaker's, at a rate of 0.05 × (0.5 + curiosity) × (0.5 + respect).
    - The copy is not checked against the listener's own experience.
    - **[CL1: this carries 93% of the over-valuation of common actions. HC1 is testing "copy only the speaker's
      current situation".]**
26. **Carers' ways.** A child under 12 absorbs 8% of their carer's habits every 4 weeks.
27. **Birth habits.** A newborn starts with habits at 0.25 × (mother's + father's).
28. **Teaching recipes** (`show_how` / `hear_how`).
    - In talk, a teacher shows one of their 3 most valued recipes. It can come across garbled.
    - **The learner takes it if:**
      - they don't know it;
      - they haven't found it bad;
      - a random draw passes p = credence × openness, where openness = 0.35 × (0.5 + curiosity), doubled from a
        parent;
      - and they can follow it, meaning they know how to make its parts.
    - **If they can't follow it:** the teacher shows the first made part they know instead ("parts-first"), one level
      deep, with its own belief draw.
    - **[LA1: 85–88% of lessons fail because a part is missing. PT1: parts-first reaches only 28%; most are too deep.]**
29. **Memory for recipes.**
    - A person holds at most 12 recipes; the lowest valued is forgotten.
    - **A just-taught recipe is valued at 0 at that moment**, so it is usually the one forgotten.
    - **[PT1: 71% of overflows delete the new lesson. MO1 tested setting the value first: helped, but missed its frozen
      threshold.]**
30. **Watching.** Only in two moments: on a **joint hunt**, and when someone **floats across water** nearby. There, seeing
    someone do well with a thing can, rarely, let the watcher work out how to make it. People do **not** learn by
    watching someone make something.
31. **Belief and trust (credence).**
    - How much someone is believed depends on goodwill (trust, respect), their record of being right, their visible
      health, whether they hold the thing, and a bonus for adults talking to children.
    - People keep score of who turned out right.
32. **Stories and gossip.**
    - People tell what they saw (who did what to whom), and listeners weigh it by credence.
    - Stories change trust and grudges, and can be disputed by those who were there.
33. **Places told.** People tell where water and animals were seen; fresh news is worth more.
34. **Marks.** People can leave marks that others read as claims (for example, a kind of stone here).

**Social life**

35. **Relations.** Each pair has affection, trust, respect, familiarity and grudges, which change with what happens and
    fade over time.
36. **Family and couples.** Courting needs attraction (affection, respect, health), so strangers are rarely accepted.
   
37. **Giving, care, theft and violence.** People can give food, care for others, steal, attack, flee and join others.
    Witnesses remember and tell.
38. **Mood and feelings.**
    - Mood rises and falls with food, warmth, company, loss and success, and is part of the reward (law 18).
    - Anger, fear, grief and loneliness exist.

## What is fixed for everyone (not inherited, not learned)
- the learning rate (0.05);
- the look-ahead (0.8 per week);
- the copying rate (0.05) and the copy-everything rule;
- the 12-recipe memory;
- the choice randomness (0.2);
- one-level parts-first teaching.

## What our studies say is wrong (final findings)
- **Copying habits in talk spreads over-valued habits** (CL1: 93% of the +0.42 over-valuation of common actions).
- **Making is under-valued because it is never practised** (VC1, CL1: own value 0.01 against a real return of 0.62).
- **Teaching fails because parts are missing, and parts-first is too shallow** (LA1, PT1).
- **The memory order deletes new lessons** (PT1; MO1's fix not supported as frozen).
- **Making loses the weekly choice** (MK1, CO1, HL1), though tools pay back 1.5–2.2 times their cost.

## Correction (27 October 2026, after GPT's review)
The first version of this document said "a person carries at most 3 of a kind" and "food and things can be set down".
Both were wrong against the code:
- `item_limit` is 3 made things in total, and `_keep` deletes the extra;
- `_put` handles food, seeds and raw materials only, not made things.

GPT spotted the second ("Made objects apparently cannot actually be put on the ground and recovered"); the assistant
checked both in `acl/actions.py` and corrected laws 13 and 15 above.

## Correction 2 (27 October 2026, after GPT's review)
GPT also flagged laws 15 and 30. Checked in the code:
- **Law 15:** `_gather` reads only a tile's own stock (`Tile.material`), not its pile, so raw materials put on a pile
  cannot be taken back.
- **Law 30:** `knowhow.watch` is called only from joint hunts (`resolve_hunts`) and floating across water
  (`_over_water`).

Both laws are corrected above.
