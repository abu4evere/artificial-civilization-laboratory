# How free are ACL's people to act? An audit of nature v11 (2 November 2026)

**Why:** the creator, 2 November 2026: "in whole project we must make sure we are not restricting actions. Because in
real life i can literally can do whatever i want to do. And all people act different and think different".

**What it is:** a read-only reading of the code (`acl/mind.py`, `acl/actions.py`, `acl/world.py`, `acl/config.py`). It
changes nothing. It goes with the audit of what made things can do (`docs/affordance_audit_2026-11-02.md`).

## A. How a person acts today
- **One action a week.**
  - Each week, everyone aged 1 or more picks **one** of 19 kinds: rest, forage, hunt, gather, put, take, make, play,
    explore, give, care, talk, court, steal, attack, flee, join, heat, fill.
  - The world then moves on (`World.step`). Nobody can do two things in a week, such as walk somewhere, gather and talk.
- **Few targets, and most are picked for them.** For most kinds, the code first chooses the **single best target** by a
  written formula (`mind.decide`):
  - the best of a handful of tiles to forage or hunt: the current tile, home, **6 random tiles** within 3 steps, and
    places they were told about;
  - the best material to gather;
  - the best recipe to make;
  - the best thing to set down.

  The person then chooses among these few candidates, with some chance (softmax). **They never see, or choose among,
  all the places, things or recipes they could pick.**
- **Purposes are written into the actions.** "Forage" and "hunt" are for food, "court" for a partner, "care" for the
  sick or young, "steal" and "attack" for taking and harming. The action names a goal, not a movement.
- **Some actions happen inside others, and are not chosen.**
  - Teaching happens automatically inside talk: the speaker offers one of their three most valued things, picked at
    random (`information.show_how`).
  - What to gossip about, and which place to tell, are also automatic.
- **Distance:** at most 3 tiles a week (`config.reach`).
- **Age gates:**
  - talk from 1;
  - gather and play from 3;
  - forage and take from 6;
  - hunt, make, put, heat, fill, explore, care, steal and attack from 12;
  - court from 16 to 49.

## B. Where people already differ
- **Temperament:** eight inherited traits scale every instinct.
- **Habits:** 608 learned values, one per situation × action.
- **Memories and know-how:** 60 memories, up to 12 recipes, and beliefs.
- **Ties:** affection, trust and respect for others.
- **SC1 found a real personal style:** a person's own past actions predict their future ones beyond all of the above.
- **But everyone uses the same formulas.** Differences are in the numbers, not in **how** a person thinks or what they
  can think of doing.

## C. What nobody can do at all
1. **Invent a new kind of action**, or combine actions into a new routine (no macro-actions).
2. **Do more than one thing in a week**, or spend several weeks on one task as a single act.
3. **Pick a target the formula did not offer:** another tile, another material, a recipe other than the best one, or a
   particular lesson to teach.
4. **Hold a plan or a goal across weeks** (UP1, WP1).
5. **Act together on one task.** The only exception is hunting on the same tile.
6. **Signal on purpose.**
   - Marks are made while fiddling, not to say something.
   - Talk carries fixed kinds of content: gossip, reputation, places, lessons and habits.
7. **Build with made things, store them, or carry more than 3** (`docs/affordance_audit_2026-11-02.md`).

## D. What this means (the assistant's reading; for the creator and the council)
- **The creator's principle is right for ACL's goal.** Bob needs to choose his own goals and invent new ways to act.
  Today's people choose among a short menu of purposes, with targets mostly picked for them. That is the "options are
  given" gap SC1 marked as not measurable (capacities 6, 7, 8).
- **An honest limit:** no simulation can let people "do anything". Real people are also bound by their bodies and by
  physics. The realistic aim is that **what people can do comes from general abilities and physics**, not from a list
  of purposes. In practice:
  - actions as general verbs: move, pick up, put down, strike, join, give, show, hold, eat, rest;
  - targets chosen by the person from what they perceive;
  - purposes such as hunting, building or teaching **arising** from learned values, not written as actions.
- **That is a deep redesign of nature.** It should be done step by step, each step a frozen test in a copy with a sham,
  adopted only with the creator. Possible order, from smallest to largest:
  1. **the inventions audit's rules:** make by what it does; containers that contain; build and store with made things;
  2. **free targets:** a person may consider any reachable tile, material or known recipe, not only the formula's best
     one;
  3. **teaching as a choice:** what to show, and to whom;
  4. **actions as general verbs, purposes learned;**
  5. **a goal or plan kept across weeks; routines built from actions.**
- **Every step must open possibilities through general laws and physics, never name an outcome.** That is the line
  between "give them all possibilities" and scripting.
