# GPT's review of the MK1 draft (26 October 2026)

**GPT's opinion, not sign-off.** Asked in the main chat in sleep mode. Condensed by Claude, with GPT's wording kept where
quoted.

"MK1 is the right next study. I support it with revisions before freezing."

**The main criticism:** the low-skill trap and opportunity cost "are not mutually exclusive". Low skill may make tools
worth less, while high immediate food from foraging prevents the practice that would raise skill. Both could reinforce
each other.

## 1. What is wrong or missing
- **A. Log every making opportunity, not only weighed ones.** Making is offered only when v > 0.05, and holding the
  thing can suppress it. Separate the steps:
  - feasible but not offered;
  - offered (weighed);
  - offered but not chosen;
  - chosen and done;
  - a useful tool produced.

  Otherwise a second bottleneck at the worth threshold could be missed.
- **B. Skill and worth cause each other.** Making raises skill, better tools raise worth, and more worth means more
  making. Q2's associations cannot say which causes which. Track each person's history of making, tool quality, tool
  use and the worth updates that follow.
- **C. Log the whole choice set.** Making could lose because foraging's score rises or because other attractive options
  appear. Distinguish the top-scoring option from the action the softmax actually drew.

## 2. Q3: the softmax decomposition
The gap to the single winner is not the right quantity. With T = 0.2, let U_m be making's full utility (with its habit
term), and U_other = 0.2 · log Σ_{j≠m} exp(U_j / 0.2) over all other offered actions. Then
P(make | offered) = 1 / (1 + exp((U_other − U_m) / 0.2)). Define the effective advantage G = U_m − U_other. Exactly,
log-odds(make) = G / 0.2.

The early-to-late change in log-odds can then be split into:
- making's learned worth;
- hunger and diligence;
- the making habit;
- competing options (the change in U_other).

This is an exact accounting, not a causal one, because the terms interact (worth × hunger × diligence). Use a
pre-specified Shapley split for the interactions. Also report the actual probability of choosing to make, since the
average log-odds and the average probability can differ.

## 3. Q4's counterfactual is not sound
The same person's foraging returns in matched weeks do not tell what would have happened without the tool. The person
might go elsewhere, lose the tool or die, and conditions change. Replace it with descriptive measures:
- **realised benefit:** food owed to the tool over the weeks after it was made, with the tool's life, how often it was
  used, and food availability;
- **estimated immediate cost:** food plausibly forgone in the making week, from comparable observed foraging;
- their difference, reported as "an observational benefit-cost proxy, not a causal net return";
- **better still,** the tool's incremental yield at each actual forage act, holding that act fixed. This is its
  immediate physical contribution.

52 weeks may miss later returns. Report a cumulative benefit curve over several horizons, handling censoring
explicitly.

## 4. Size
32 worlds × 200 years is "enough for an initial descriptive mechanism audit, not guaranteed for precise inference". Only
32 independent units; rare making events may be scarce for Q4. Report the early-to-late changes both within surviving
worlds and across all worlds, recording extinctions.

## 5. Three hypotheses, pre-registered (all may hold)
| hypothesis | prediction |
|---|---|
| Low-skill trap | Low skill predicts poor tool quality, low learned worth and little later making, even with comparable immediate opportunities |
| Opportunity cost dominates | Making loses mainly because competing forage utility is higher; even skilled agents rarely choose it |
| Delayed-benefit failure | Making and tool use pay over the longer term, but that is not reflected in learned worth and choice |

The third "is particularly important for Bob". A positive association would justify a controlled experiment, not a new
cognitive architecture.

**Verdict:** "Keep MK1 read-only. Add offer-gate logging, use the full-softmax effective gap, and downgrade Q4 from a
causal counterfactual to a descriptive return estimate." Don't merge fly-brain work. "The question MK1 must answer is
not 'How do we make agents craft again?' It's 'What do the agents actually have reason to do, and what prevents
experience from changing those reasons?'"
