# Research note: habits that start low, and a longer view (1 November 2026)

**For the open question:** under ES2's realized look-ahead, every well-sampled action's habit value sits below what
actually followed (q below G in 20 of 20 rows, `experiments/ES2_realized_lookahead/explore_q_vs_G.md`; exploratory, not
frozen). Rest is one case of this. **Why do habits stay too low, and would a longer look-ahead help?** A source suggests;
only a frozen study decides.

## What was read (labels per CLAUDE.md)
**Sutton, R. S. & Barto, A. G. (1998).** *Reinforcement Learning: An Introduction* (1st edition, MIT Press). The
authors' HTML edition, http://incompleteideas.net/book/ebook/. **Read: sections 2.7 ("Optimistic Initial Values") and
7.2 ("The Forward View of TD(λ)"), as page text.** The equations are images and did not come through in the text, so
the formulas themselves were not read. No other section was read.

### 2.7 Optimistic initial values
- **Learners are "biased by their initial estimates".** With a constant step size (like ACL's 0.05), "the bias is
  permanent, though decreasing over time".
- **High starting values make a learner try every action.** It is "disappointed" by what it gets and switches to
  others, so all actions are tried "several times before the value estimates converge".
- The authors call this "a simple trick" for problems that do not change, "far from being a generally useful
  approach". Its push to explore "is inherently temporary".

### 7.2 The forward view of TD(λ)
- **TD(λ) updates toward a weighted average of the 1-step, 2-step, 3-step… returns.** Each further step's weight
  fades by λ.
- **λ = 0 is the one-step method** (ACL's kind). **λ = 1 is the full realized return** (Monte Carlo, "constant-α MC").
- In their random-walk example, an intermediate λ did best.

## Bearing on ACL (the assistant's reading; hypotheses for the council)
1. **A low start can last a lifetime.**
   - In ACL, a newborn's habits start at half the parents' mean (`acl/biology.py` line 553), then move 5% per update.
   - By 2.7, that start biases values for a long time.
   - Under v11, the max's upward push may have hidden it. Under ES2's expectation, nothing hides it.
   - This fits q < G everywhere under r. **Not tested.**
2. **A low start may also keep rare actions rare.**
   - 2.7 is the mirror image: high starts make a learner try everything.
   - In ACL, making, courting, exploring and play have q far below G under both rules (exploratory table).
   - A low habit means rarely chosen, so rarely updated, so it stays low.
   - A caution: a rare action's G is measured only on the occasions it was chosen, perhaps the good ones, so its gap
     may be partly selection.
   - This may be part of the "choice gap" (making loses to food). **A hypothesis only.** Changing how habits start
     would be a nature change, debated and frozen first, with no target outcome.
3. **A caution for any longer-view study.**
   - At λ = 1 the update target *is* the realized return G, which is exactly VC1's calibration measure.
   - So a λ rule would partly score well on calibration by construction.
   - A study of it needs a primary measure that is not G itself, or must say so plainly.
4. **The first step stays read-only.** Calibration split by age, or by how often the person had already updated that
   habit, would show whether the under-valuation is a "young minds" effect. It is queued in `research/state.json`, for
   debate with GPT and Gemini.

## Addendum (11:57): how human value learning changes with age
**Palminteri, S., Kilford, E. J., Coricelli, G. & Blakemore, S.-J. (2016).** "The computational development of
reinforcement learning during adolescence." *PLoS Computational Biology* 12(6): e1004953 (open access,
doi 10.1371/journal.pcbi.1004953). **Read: the abstract and the author summary only.**
- **Adolescents' choices were better fit by a basic learning rule.** Adults added "a counterfactual learning module"
  and "a value contextualisation module".
- **Adolescents learned from reward but were "less likely to learn from punishment"**; adults learned from both alike.
- **Bearing on ACL** (a suggestion only):
  - In people, age changes *how* values are learned, not only where they start.
  - In ACL, every age uses the same rule, so UV1's age bins can show only starting values and experience, not a
    developing rule.
  - That is a difference from Earth to keep in mind when reading UV1. It is not a proposal to change nature.
