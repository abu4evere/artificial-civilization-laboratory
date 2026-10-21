# Medium article draft (the creator posts; nothing posted)

**Title:** Why 9 in 10 Inventions Die in My Simulated Civilization

**Subtitle:** I built a world where nature is programmed and culture is not. Its people keep inventing things, and
almost none of it lasts. Here's what I found when I traced why.

**Tags (Medium allows 5):** Artificial Intelligence, Simulation, Agent Based Modeling, Cultural Evolution, Science

**Image ideas:** the website's viewer screenshot (site/img/viewer.png) at the top; the book cover near the end.

---

In one of my simulated worlds, in its twelfth year, a person named Reibik tied a few things together and made a vessel
that could hold water. Nobody had shown Reibik how. For two years Reibik carried it everywhere, often within reach of
fresh water, and never once filled it.

That small mystery is a good way into what I've been building: the **Artificial Civilization Laboratory (ACL)**.

## A world with nature, but no history

ACL is an agent-based simulation of hunter-gatherers. Twenty people wake up on a set of islands knowing nothing. What I
programmed is nature only: bodies that get hungry, thirsty and cold; seasons; plants and animals; family ties and
feelings; and materials with properties. Stone can be struck, wood floats, clay hardens in a fire.

What I didn't program is anything cultural. There's no list of inventions, no reward for being clever, and no language
model. Each person learns habits by trial and error in their own lifetime, and anything they figure out has to be shown
to someone else, or it dies with them.

The question behind it is simple: **can civilization start by itself?** And if it can't yet, what exactly stops it?

## They do invent

The first surprise was how quickly ACL's people invent. In their first weeks they tie floating wood into rafts. They
make carriers, warm wraps, blades. Clay left by a fire hardens. Reibik's vessel appeared without anyone teaching it.

The second surprise was how little of it lasts. The raft was invented almost at once and almost never used. Fired clay
appeared and stopped. Worlds that started with a burst of novelty settled into the same few things for centuries.

So I stopped asking *whether* they invent, and started asking *where inventions go*.

## Following every invention

For an invention to become part of a people's life, it has to pass through a chain:

1. someone invents it,
2. it turns out to be useful,
3. someone else learns it,
4. they keep it,
5. someone builds something better on it,
6. and that is passed on in turn.

I followed every useful invention through that chain in dozens of replayed worlds. The chain broke at link 3, the very
first hand-over. **Only about 1 in 10 useful inventions was ever learned by anyone except the person who invented it**
(11% in one set of worlds, 10% in a second set I hadn't looked at before). Almost all first hand-overs, about nine in
ten, were teaching: one person showing another during a conversation.

So the problem wasn't that people couldn't learn. It was that teaching almost never happened for the things that
mattered.

## Where teaching fails

Next I traced teaching itself, gate by gate: did the inventor talk to anyone while they still knew it? Did they value
it enough to show it? Was it among the few things they chose to show? Was the listener able to follow it?

Two obstacles stood out.

**Most inventions never even reached a lesson.** Nearly half were lost before any teaching conversation could happen.
When I looked at those, the answer was almost embarrassingly simple: **memory**. A person in ACL can remember how to
make twelve things. A brand-new invention starts out valued at nothing, so when memory is full, the newest thing is
usually the first to go. **99% of these lost inventions were pushed out of their inventor's memory within a season.**

Four in five of the inventions that were never passed on were made by children, who play the most and invent the most.
The ones that did spread were held about five times as long and shown to about twice as many people.

**Complex things could hardly be taught at all.** Something made from other made things can only be followed by
someone who already knows how to make its parts. In the conversations where such a thing could have been taught, the
listener knew the parts about one time in twelve.

There was also an accident. When two remembered things were valued exactly the same, the code broke the tie by name, and
the names of composite things happened to sort first. So the things a longer chain of invention would need were the
first to be forgotten. Nobody designed that as nature; it was bookkeeping, and I only found it because I went looking.

## What real people do differently

Anthropologists who study forager children describe something ACL's people don't have: children meet the parts of a
craft long before the whole. A toy bow before a real one; a share of the work before all of it. In my world there are no
toy bows, and no room in memory to keep the new thing while learning the old.

So I tested two changes to nature on 1,024 worlds: fix the memory accident (forget the oldest thing, not whatever
sorts first by name), and let a teacher whose lesson just failed show the missing part instead. Four versions: neither,
each alone, and both.

**Fixing the memory accident did nothing** for how much was passed on. **Showing the missing part worked**: the share of
useful inventions that reached someone else rose by about two points, from a typical 9%, in world after world, far
beyond chance. It's a small step (about one more invention in fifty passed on), but it's the first change that moved the
place where the chain breaks.

## How I try to keep myself honest

The easiest way to "succeed" with a project like this is to slip the answer in: reward the agents for inventing, or
use a model that already knows what a village is. So I run ACL like a lab:

- **Predictions are written down and frozen in git before any code or data.** My wrong predictions stay in the record,
  and there are plenty of them.
- **Many worlds, side by side.** One world can do almost anything. Comparisons run the same starting worlds under both
  sets of rules, often 256 of each.
- **Exact replay.** The simulation is deterministic, and every instrument that watches a world is checked to change
  nothing in it.
- **Nature only.** A change to nature needs a written case and evidence about the real world, never a wish for a better
  result.

None of this proves anything about human history. ACL is a model; what it gives me are candidate explanations, made
precise enough to test.

## What's next

A second puzzle has also given up part of its answer. When I split
the same 80 founders into smaller bands, families mixed far more (couples across families went from 6% to 54%), but the
time women spent without a partner didn't change at all. So I replayed those worlds and traced every single woman's
week. In about half of them, a suitable man was right there, within reach, and neither of them courted. Courting was
on their list of options about nine times in ten, but it had roughly one chance in a thousand against looking for food.
And when someone did court a near-stranger, the answer was almost always no: in ACL, accepting depends on already
liking the person. Meeting more people, it turns out, isn't the same as finding someone.

If you build simulations, study cultural evolution, or just like a good puzzle, I'd love your criticism, especially
anywhere it looks like I've scripted the answer without noticing.

- Website and findings: https://abu4evere.github.io/artificial-civilization-laboratory/
- Code and every experiment record: https://github.com/abu4evere/artificial-civilization-laboratory
- The story of the project, as a book: *The World That Nobody Wrote*,
  https://abu4evere.github.io/artificial-civilization-laboratory/book.html
