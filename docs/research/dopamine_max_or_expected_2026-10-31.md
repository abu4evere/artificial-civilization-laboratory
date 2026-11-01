# Research note: do real brains learn from the best next option or the expected one? (31 October 2026)

**For the open question:** ES1 (running) tests replacing ACL's max look-ahead with an expected look-ahead. The
learning-rule note of 30 October (`learning_rule_sources_2026-10-30.md`) left this unread: "the human or animal
evidence on whether people learn more like the max or like the expected value." A source suggests; only a frozen study
decides.

## What was read (labels per CLAUDE.md)
1. **Morris, G., Nevet, A., Arkadir, D., Vaadia, E., Bergman, H. (2006).** "Midbrain dopamine neurons encode decisions
   for future action." *Nature Neuroscience* (August 2006). PMID 16862149. **Read: the abstract (PubMed).**
   - Recordings from dopamine neurons in **monkeys** doing an instructed-choice task and a two-armed bandit.
   - "The activity of dopamine neurons in the decision setting is modulated according to the value of the **upcoming
     action**." That is the action the animal then takes, which is the signature of on-policy learning (SARSA-like),
     close to an expected look-ahead.
   - The abstract does not name SARSA. A commentary, Niv et al., "Choice values" (PMID 16871163), exists but has no
     abstract and was not read.
2. **Roesch, M. R., Calu, D. J., Schoenbaum, G. (2007).** "Dopamine neurons encode the better option in rats deciding
   between differently delayed or sized rewards." *Nature Neuroscience* (December 2007). PMID 18026098. **Read: the
   abstract (PubMed).**
   - Recordings in the ventral tegmental area of **rats** choosing between rewards of different delay and size.
   - "When rats were given a choice between two differently valued outcomes, the activity of the neurons initially
     reflected the **more valuable option, even when it was not subsequently selected**." That is the signature of
     the max (Q-learning-like), which is ACL's rule today.

## Bearing on ACL
- **The animal evidence is split** in what was read: monkeys look on-policy (expected-like), and rats look max-like.
  **Neither rule is clearly "nature's way."** So ES1 is a test of a choice between two biologically plausible rules,
  not a fix towards a known truth.
- **ES1's primary (calibration across all actions) fits this.** It asks which rule makes values match what happens,
  without assuming either is right.
- **ES1's operational note 1** recorded, before data, that the smoke world's expected rule undershot returns. If the
  real run agrees, a later form could take the expectation over the full choice (instinct terms included), which is
  closer to Morris et al.'s "value of the upcoming action". That would be a new frozen study, not a change to ES1.

## Not read
- The full texts of both papers; Niv et al.'s commentary; any human behavioural study comparing SARSA and Q-learning
  fits.
