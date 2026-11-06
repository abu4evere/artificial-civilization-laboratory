# Research note: what memory drops first (5 November 2026)

**Why now:** VA1 found that when a person's 12-recipe memory is full, a new invention is forgotten at once. In 129 of
130 tied cases (all at value 0) the tie was settled by the recipe's name in alphabetical order
(`knowhow.remember_recipe`: `min(value, name)`), and that order goes against the more nested, more complex kind.
Is there human evidence for a general rule to settle such ties?

## Source
**Anderson, J. R., & Schooler, L. J. (1991). Reflections of the environment in memory. *Psychological Science*, 2(6),
396–408.**
- **Read: full text** (14 pages, the PDF copy hosted at users.cs.northwestern.edu; text extracted with pypdf on
  5 November 2026).
- The record is also listed by the ACT-R publications page (act-r.psy.cmu.edu).

## What it says (paraphrased)
- The availability of a memory follows how often, how recently and in what pattern it was used before.
- The authors measured how often items are **needed** in three environments: New York Times headlines, speech to
  children, and electronic mail.
- The chance that an item is needed now ("need probability") follows the same patterns: it falls with time since last
  use as a **power function**, and rises with how often it was used.
- Their argument: memory is shaped like this because it is adapted to how often things are needed in the world. When a
  store cannot keep everything at hand, it should keep available what is most likely to be needed.
- They also discuss why forgetting is better described by power functions than by exponential ones.

## How it bears on ACL (a suggestion only; a frozen study decides)
- ACL's cap already drops "the least valued" recipe. Value is one sign of need.
- **On a tie, the evidence points to recency of use** (the longest-unused is the least likely to be needed), **not to
  the name.** A just-made invention has been used most recently, so a recency tie-break would keep it.
- This is a general law of memory, not a reward for novelty and not a named invention. It would apply to every
  recipe alike.
- **Caution:** recency could also protect useless new kinds that crowd out useful old ones. A test in a copy should
  watch the old recipes' loss and the value of what is kept, with a sham.
- A bigger version (need probability from both recency and frequency, replacing value) would change much more. It is
  not suggested now.

**Label:** a source suggests; only a frozen study decides.
