# GPT's view of CT1, Draft 0 (22 October 2026; GPT, not a verified source)

Asked in the ACL ChatGPT project, in the chat that also holds TP1's review. GPT's answer is condensed here; its
substance is kept and labelled as GPT's.

**Verdict:** "a worthwhile study", but "I would not sign CT1 exactly as written". Keep the four-arm draft, improve
the justification and the decision rule, and change nothing in nature v3 until the creator signs.

**On the candidates**
- **K1** (familiarity in attraction): defensible as a hypothesis, but the implementation claims more than the
  evidence. Zajonc shows exposure can raise liking, not that it raises acceptance of a partner. Festinger et al. show
  propinquity creates opportunity. Bossard shows proximity is associated with marriage, but does not isolate
  familiarity. Add Finkel et al. (2015): familiarity can promote or undermine attraction, depending on awareness,
  surface contact or mutuality. K1 tests whether familiarity can *on its own* overcome the acceptance barrier, which
  is a stronger claim. Keep it, with the coefficient labelled exploratory.
- **K2** (loneliness in courting): plausible but weaker. Loneliness may lead to any social contact, not courtship in
  particular. Sayre et al. 2023 is about physical activity and is not support. The effect of a multiplier inside a
  softmax depends on the other options' scores.
- **A better later candidate: reciprocated interest.** Courting responds to an observable positive response, not to
  hidden feelings (named: "Proximate and ultimate perspectives on romantic love"; Back et al. 2011, where speed-dating
  choices were less reciprocal than people expect but flirting was more reciprocal). First check whether ACL's
  relationship changes already act like it.
- **"Nature or culture":** familiarity and attraction are individual-level mechanisms whose expression culture shapes.
  Say "individual-level", not "pure nature".

**On the sizes:** don't invent a conversion into ACL's units. Either test two strengths (more arms and comparisons),
calibrate to a behavioural target (none exists here), or run a sensitivity study (a separate experiment). For CT1,
label 0.3 and (1 + loneliness) as uncalibrated exploratory parameters. The creator accepts that CT1 tests these
implementations. Never pick values by which saves the most worlds.

**On the adoption rule**
- "Fewer worlds die out" needs a stated statistical criterion.
- State what the ±0.117 yardstick decides. F2 wrote in an outcome, so it is a rough scale, not a minimum effect.
- Births per woman-year should be a mechanism outcome, not a condition.
- A 50% relative harm threshold is unstable on small baselines. Report absolute and relative changes with intervals,
  and name which harms are unacceptable.
- K12 beating each alone is not evidence of synergy; test the interaction if that is the question.

**On the design:** keep the paired seeds (pairs share a start, not a path, once arms differ). Keep C exactly v3.
Make the manipulation checks diagnostic: acceptance by familiarity level, courting by loneliness level, who is
approached, and whom the change acts on. Report all arms. Keep the creator's decision separate from the statistics.

**Its key principle:** "Survival improvement is evidence about the consequences of a mechanism, not evidence that the
mechanism is biologically correct." Also: "CT1 is a test of candidate implementations of human behavior, not a
contest to discover which rule saves the most worlds."

**Sources it named** (record only; to check before citing):
- Finkel, E. J., Norton, M. I., Reis, H. T., Ariely, D., Caprariello, P. A., Eastwick, P. W., Frost, J. H. and
  Maniaci, M. R. (2015). When does familiarity promote versus undermine interpersonal attraction? A proposed
  integrative model from erstwhile adversaries. *Perspectives on Psychological Science* 10(1): 3–19.
- Back, M. D., Penke, L., Schmukle, S. C., Sachse, K., Borkenau, P. and Asendorpf, J. B. (2011). Why mate choices are
  not as reciprocal as we assume: the role of personality, flirting and physical attractiveness. *European Journal of
  Personality* 25(2): 120–132.
- Bossard, J. H. S. (1932). Residential propinquity as a factor in marriage selection. *American Journal of Sociology*
  38(2): 219–224 (GPT: about a third of 5,000 Philadelphia couples lived within five blocks).

**Adopted in Revision 1 of `questions.md`:** all of the above except new arms for size sensitivity and the
reciprocity candidate, which are left for later studies.
