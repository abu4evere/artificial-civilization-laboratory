# GPT's review of PF1's result (21 October 2026, verbatim; chat "AI World (1)")

Sent in sleep mode with PF1's result. A review, not the creator's sign-off. Its check 1 (variable ranges) is answered in
`findings.md`: founders' temperaments lie between 0.1 and 0.9 (`world.py`, `0.1 + 0.8 * rng.random()`), children's
drift a little, health is at most 100, so with no affection and no respect attraction stays at or below 0.55; couples
form only through `actions._court`. Attempts in `results.md` are the sum of paired, refused and "already taken" (one
log record per attempt).

---

Bro, this is a strong result. 🔥 PF1 answers the question MB1b left open: smaller bands increased contact, but contact wasn't the main thing preventing couples from forming. The biggest bottleneck is that women often don't choose to court.

And you found something deeper in the code: the rules make acceptance by a stranger extremely difficult. That's an important lead, but we need to distinguish a mechanism that explains the result from a mechanism we have proved causes it.

My recommendation: the first read-only audit should be what agents do instead of courting. I'd keep the 20-founder audit as a separate decision. Here's why.

1. What PF1 establishes
The frozen reading survived holdout

S5 — neither chose court — is the largest category in every band configuration, in both discovery and holdout.

First failed step P4 discovery P4 holdout
S1: No suitable man alive 3.4% 2.0%
S2: None within sight 30.3% 35.2%
S3: None within reach 18.8% 16.7%
S4: Disliked ~0% ~0%
S5: Neither chose court 47.1% 45.7%
S6: Tried and refused 0.4% 0.3%

B8 and B16 show the same broad pattern. That matters because it means the result isn't just a discovery-set accident.

The strongest conclusion is:

The largest measured bottleneck is failure to initiate courtship, not a lack of suitable men or outright rejection.

One precision point: this is a first-failed-step classification. It tells us where each woman-week first fails under the audit's ordered checks. It doesn't mean all other steps are irrelevant.

Smaller bands created more attempts, not more couples

Courting attempts rose as bands got smaller:

Discovery: 3,901 in P4 → 5,357 in B16.
Holdout: 3,574 in P4 → 5,530 in B16.

Yet couples formed stayed around 1,600.

That is an interesting separation between social contact, courtship attempts, and successful pair formation. Increasing opportunities for interaction can increase attempts without increasing successful outcomes.

It also explains why MB1b's increased cross-lineage contact didn't automatically resolve partner blocking. More encounters aren't necessarily more successful relationships.

However, we should be careful with the wording that the extra attempts were refused. Your summary says the extra attempts were refused, which supports that interpretation, but I'd verify whether the total attempts and refusals use identical definitions and counting units before quantifying the conversion rate.

2. The attraction formula is the most interesting lead

The acceptance rule is:

attraction = 0.25 + 0.2*sociability + affection + 0.2*respect + 0.1*health/100

Acceptance requires attraction greater than 0.55.

For a stranger with no affection or respect, this simplifies to:

attraction = 0.25 + 0.2*sociability + 0.1*health/100

Assuming sociability and health are each bounded from 0 to 1 and 0 to 100 respectively, the maximum is:

0.25 + 0.2 + 0.1 = 0.55

That means a stranger cannot exceed the strict > 0.55 threshold under those assumptions. Even at the maximum, the condition fails.

If those variable ranges and the implementation match this interpretation, a stranger with no affection and no respect can never accept courtship.

That's potentially important—but there's a distinction worth preserving:

PF1's demonstrated result: S5 is the dominant measured bottleneck.
Code-level observation: strangers without affection or respect appear unable to meet the acceptance threshold.
Still unproven: how much this acceptance rule contributes to the overall failure to form couples.

The acceptance threshold directly concerns what happens after an attempt. S5 concerns cases where neither person chooses courtship. The two may interact, but the formula alone doesn't explain why courtship isn't chosen in the first place.

I would not change the threshold yet. First, audit the behavior the agents already exhibit.

3. Review of the two candidate next steps
Candidate A: Read-only audit of what agents choose instead of courting

My recommendation: prioritize this one.

It addresses the biggest remaining uncertainty in the current results.

You know that S5 weeks end without either person choosing courtship. You don't yet know what they do instead.

The audit should distinguish, using existing logs wherever possible:

Seeking food or water.
Resting or recovering health.
Other social interactions.
Working toward another goal.
Staying idle or failing to select an action.
Having no valid courtship opportunity under the action-selection rules.

These are examples of categories to investigate, not claims about what ACL currently logs or what its agents actually do.

I'd also inspect whether the agent had a suitable candidate, whether the candidate was visible or reachable at the relevant decision time, and whether the agent had any affection or respect for that person.

Important caveat: the current S5 classification says neither chose court. It doesn't tell us whether an agent actively preferred another action, never considered courtship, or couldn't satisfy a prerequisite. The audit should keep those cases separate if the existing state permits it.

The purpose is to identify the actual decision path, not to decide in advance that agents are too busy, too selective, or too socially isolated.

Candidate B: Repeat the audit in 20-founder worlds

My recommendation: valuable, but second.

This would test whether the bottleneck generalizes beyond the 80-founder conditions used in PF1.

The distinction matters because smaller populations can change:

The number of suitable partners available.
How often potential partners meet.
The age and relationship composition of the population.
The frequency of opportunities to court.

Your existing evidence does not establish that the same bottleneck dominates in 20-founder worlds.

But I'd first finish the S5 diagnostic. It may reveal a specific mechanism worth measuring consistently across both population sizes. That would make the next audit more informative.

Also, keep the original PF1 result frozen. A new population-size audit should test generality, not retroactively change the original finding.

4. Two things I'd check before approving either audit
Check 1: Confirm the attraction variable ranges and the exact acceptance code

The mathematical conclusion above depends on the actual ranges of sociability and health, the treatment of missing affection or respect, and whether the implementation uses exactly the formula and strict threshold described.

Verify those details directly from the frozen code. Don't infer them from the formula's variable names.

Also check whether acceptance is evaluated only after courtship begins, and whether any other paths can form a couple.

Check 2: Preserve the denominator distinction you just resolved

Your clarification is important:

Partner blocking: a share of fertile woman-weeks spent without a partner.
Cross-lineage couples: pair events accumulated over the run.

Those are different measures. They can both be valid, but they should never be presented as though they measure the same thing.

A population can accumulate more cross-lineage couples over time while fertile women still spend a large share of their weeks without partners. One doesn't automatically imply the other.

I'd preserve that distinction in future reports and in the interpretation of any new audit.

5. What this means for ACL's bigger research question

There's a useful pattern emerging across these experiments:

Investigation What the results suggest
MB1b More cross-lineage contact did not meaningfully change extinction under the frozen criterion.
PF1 The largest measured partner-finding bottleneck is neither person choosing courtship.
Attraction rule A possible constraint on accepting strangers may exist, pending verification of ranges and implementation.
Next diagnostic Determine what agents do instead of courting, without changing their rules.

The broader lesson is not that contact doesn't matter. It's that contact alone may be insufficient when the rules governing decisions and acceptance also constrain relationship formation.

That's a hypothesis about the interaction between social opportunity and individual behavior—not a universal law about civilization.

And that's exactly the sort of question ACL should help you investigate.

My final recommendation
Keep PF1 frozen and archived. Its holdout results support the frozen reading.
Verify the attraction formula, variable ranges, and acceptance implementation.
Prioritize the proposed read-only S5 action audit. Keep it separate from any intervention or model change.
Consider the 20-founder audit afterward, using the same definitions where possible.
Don't adjust the courtship or attraction rules yet. Let the diagnostics tell you where the actual bottleneck lies.

Bro, the strongest part of this update is that you didn't stop at "smaller bands didn't solve partner finding." You traced the failure to a specific stage of the process and then found a rule that might constrain what happens next.

The next question isn't how to force more couples to form. It's why the agents aren't choosing courtship—and whether the rules make successful courtship possible when they do.
