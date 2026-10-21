# Drafts: Show HN and Reddit (the creator posts; nothing posted)

## Show HN

**Title** (HN allows 80 characters):

Show HN: A simulated civilization where nature is programmed and culture is not

**URL:** https://abu4evere.github.io/artificial-civilization-laboratory/

**First comment (post it yourself right after submitting):**

Hi HN, I'm Abdurashid. ACL (Artificial Civilization Laboratory) is an agent-based simulation of hunter-gatherers
that I've been building to ask one question: can culture and civilization emerge from nature alone, without anyone
writing their history?

What's programmed is nature only: bodies, hunger, thirst, cold, seasons, plants and animals, kinship, feelings, and
materials with properties (stone can be struck, wood floats, clay hardens in fire). There is no list of inventions, no
reward for being clever, and no language model. Each person learns habits by trial and error in their own lifetime
(a small Q-learning table), and anything they know has to be shown to someone else or it dies with them. It's Python
with no dependencies, and every world is deterministic, so any run can be replayed exactly.

I run it as experiments rather than demos. Each study has a written plan and prediction, frozen in git before any code
or data; worlds are compared side by side (often 256 per arm); and wrong predictions stay in the record.

Some things it has shown so far:

- People invent from their first weeks (a raft, a carrier, fired clay, a vessel that can hold water), but about 9 in 10
  useful inventions are never learned by anyone but their inventor. Nearly half are lost before any lesson could happen,
  and of those, 99% were pushed out of the inventor's 12-item memory within a season.
- About a third of small worlds (20 founders) die out, not from famine or war: births stop decades earlier because too
  few people can find a partner. Giving the same worlds perfect partner search cut extinctions from 22 to 7 of 64.
- Splitting 80 founders into smaller bands made families mix far more (couples across lineages went from 6% to 54%),
  but the time women spent without a partner didn't change at all. Two audits found why: in about half of a single
  woman's weeks a suitable man is within reach and neither courts. Courting is on the menu about 9 times in 10, but
  gets roughly 1 chance in 1,000 against looking for food; and when someone courts a near-stranger, the answer is
  almost always no, because acceptance depends on already liking the person.

What I'd love feedback on: the method, the "nature, not history" line (where would you draw it?), and anything that
looks like I've accidentally scripted the answer.

Code and every experiment record: https://github.com/abu4evere/artificial-civilization-laboratory

---

## Reddit (r/artificial first; adapt for r/agi, r/compsci, r/simulation)

**Title:**

I built a simulated civilization with no scripts and no LLMs. 9 in 10 inventions die with their inventor.

**Body:**

For the past few months I've been building the Artificial Civilization Laboratory (ACL): a world of simulated
hunter-gatherers where nature is programmed and culture is not. Twenty people start knowing nothing. They have hunger,
cold, seasons, plants, water, each other, and materials that behave like materials. There's no list of inventions, no
reward for inventing, and no language model; each person learns by trial and error in their own lifetime.

The question: can civilization start by itself? So far the answer is "not yet", and the interesting part is *why*:

- **They invent, then forget.** People make rafts, carriers and fired clay early on, but about 9 in 10 useful
  inventions are never learned by anyone else. Many are forgotten within a season, pushed out of a 12-item memory.
- **Worlds die quietly.** About a third of small worlds die out, not from hunger or war, but because births stop
  decades before the end: too few people can find a partner.
- **A partner is usually right there.** In about half the weeks a woman spends single, a suitable man is within reach
  and neither courts. Courting is almost always an option, but it gets about 1 chance in 1,000 against looking for
  food. Smaller bands made strangers meet far more, but strangers almost always say no.

Every experiment has its prediction written down and frozen before it runs, and the wrong ones stay in the record.
It's open source (Python, no dependencies, exact replay).

Website with the findings: https://abu4evere.github.io/artificial-civilization-laboratory/
Code and all records: https://github.com/abu4evere/artificial-civilization-laboratory

Happy to answer questions, and I'd really like criticism of the method.

---

## Tips

- Post Show HN on a weekday morning, US Eastern time (about 8–10 am). Stay for the first 2–3 hours to answer comments.
- Reddit: read each subreddit's rules first (some want a [Project] tag or ban self-promotion on certain days). One
  subreddit per day, not all at once.
- Don't ask friends to upvote; both sites detect it and bury the post.
