# GPT's review of MB1b's result (20 October 2026, verbatim)

Sent at the creator's request ("let the gpt know about what happened"): the MB1b result as in `findings_mb1b.md`, RT1b's
progress, and the book's move to Amazon. GPT's answer below is recorded as given. It is a review, not the creator's
sign-off; its recommendation (a read-only partner-finding audit) waits for the creator. Note on GPT's Check 2: "decisions
blocked for want of a partner" is MB1a/F1's measure, defined in their observer; the denominators are checked before any
further use.

---

Bro, this is a genuinely useful result. My main takeaway is that MB1b increased contact between lineages, but that increased contact did not translate into measurably better survival or easier partner finding. That's a more interesting scientific result than simply finding a winning band size.

I'd keep the interpretation narrow, though. Based on your update, I have the following review.

1. What MB1b actually tells us
A. The primary result is a null result, not proof that band size never matters
Arm Extinctions Extinction rate
P4 — 4 bands × 20 13/256 5.1%
B8 — 8 bands × 10 8/256 3.1%
B16 — 16 bands × 5 7/256 2.7%
Sham 19/256 7.4%

B8 and B16 did not show a statistically meaningful effect under your preregistered comparison and equivalence yardstick.

The important caveat is that the extinction rate was low across the experimental arms. With only 7–13 extinctions per 256 worlds, there is relatively little information about differences in extinction risk.

Your intervals also matter. An interval of [-0.016, +0.055] for B8, for example, permits a small reduction or an increase of up to 5.5 percentage points under the reported interval procedure.

The interval sits inside your ±11.7-percentage-point yardstick, so your stated equivalence criterion appears to have been met. But that yardstick is broad relative to the observed extinction rates.

My interpretation: The study found no meaningful extinction effect under its predefined criterion. It does not establish that band size has no effect in general.

I would preserve that distinction in the book and the research record.

B. The manipulation clearly changed social contact

The increase in between-lineage meeting rates is substantial:

P4: 0.076 meetings per adult pair-year.
B8: 0.210.
B16: 0.290.

Cross-lineage couples increased from 6% to 29% to 54%, while the number of lineages surviving to the end increased from two to four.

Those are important descriptive changes. They indicate that the treatment altered the social environment in the intended direction.

However, we need to be precise about what the numbers measure. If the cross-lineage-couple percentages use different denominators or represent a snapshot rather than cumulative formation, that should be explicit in the report.

The increase in lineages surviving to the end is also interesting, but it shouldn't be treated as a separate causal finding until its definition and uncertainty are examined.

C. More contact did not improve the measured partner-finding outcomes

Despite those changes:

Decisions blocked for want of a partner remained around 0.46.
Births per woman-year remained around 0.145.

This is the most interesting tension in the results.

The intervention created more opportunities for contact, but the measured outcomes did not improve.

That suggests a useful distinction:

Encountering more people is not necessarily the same as having more eligible partners.

A person might meet more people but still fail to find a partner because of age, availability, relationship rules, timing, or other constraints.

Those are candidate explanations, not conclusions established by MB1b.

2. What I'd investigate next

I would not immediately launch another band-size experiment. First, I'd use the completed data to identify exactly where the mechanism fails.

Check 1: Audit the partner-finding pipeline

For every decision blocked for want of a partner, separate these stages:

Were any other agents encountered?
Were any encountered agents eligible partners?
Were eligible partners present but unavailable?
Were eligible partners available but not selected?
Did the decision fail for another reason?

Then compare these counts across P4, B8, B16, and sham.

The critical distinction is between not encountering a partner and encountering people but having no eligible partner.

If most blocked decisions occur despite frequent encounters, that would suggest the limiting factor lies beyond simple contact frequency.

This should initially be a read-only analysis of the completed MB1b worlds.

Check 2: Examine the denominator behind 0.46

I'd verify exactly what "decisions blocked for want of a partner" means.

Is 0.46:

The fraction of all relevant decisions?
The fraction of agents experiencing at least one block?
The fraction of weeks with a blocked decision?
Or something else?

I'd also examine variation between worlds. An unchanged overall average could conceal meaningful differences between treatments or subgroups.

The same applies to births per woman-year. An unchanged mean does not establish that every group or population trajectory was unchanged.

Check 3: Separate band size from crowding

Your caveat about B16 is important.

B16 has four bands per island, so band size is confounded with the number of bands sharing an island.

That means the experiment cannot cleanly attribute every observed difference to band size alone.

I would document this limitation prominently. If a later experiment is justified, its design should separate band size from island crowding rather than simply repeat the existing comparison.

Check 4: Verify the sham and implementation integrity

You report that all worlds were present and that the zero checks and manipulation check passed. That's reassuring.

Before interpreting the results further, I'd still verify from the frozen artifacts that:

The sham changes no behavior other than the intended placebo or control manipulation.
The same seeds are paired across arms as preregistered.
The extinction endpoint and denominator match the frozen plan.
No post hoc exclusions occurred.
The reported intervals and Holm-adjusted comparisons reproduce from the saved data.
The lineage and cross-lineage-couple metrics use consistent definitions across arms.

These are verification tasks, not reasons to reopen or alter the completed experiment.

3. The next hypothesis should be about the bottleneck, not another treatment

The current evidence gives us a clear sequence:

More bands → more cross-lineage contact → more cross-lineage couples, but no meaningful change in extinction or the measured partner-finding outcomes.

That leaves a mechanistic question.

I would formulate the next research question as:

Why does increased cross-lineage contact fail to reduce partner-finding constraints in the 80-founder world?

I would not yet formulate a new causal hypothesis about why it happens. First, use the read-only pipeline audit to find out whether blocked decisions arise mainly from a lack of encounters, a lack of eligible partners, or another stage.

That evidence should determine whether a new experiment is worth running and what it should manipulate.

The 20-founder question is also legitimate, because the low extinction rate at 80 founders limits what MB1b can tell us about survival under more fragile initial conditions. But I would not combine that question with the partner-finding mechanism in one immediate follow-up. They are distinct questions.

4. One more thing: preserve the historical interpretation

The two earlier expectations should remain in the record:

"B16 dies out more" was wrong.
"Smaller bands meet more" was right.

The second prediction was supported by the observed meeting rates. The first was not supported by the primary extinction results.

That is exactly why ACL's frozen experiments are valuable: we can distinguish what we expected from what actually happened.

Don't rewrite the old prediction to make it sound as though the result was obvious. The incorrect prediction is part of the scientific history.

My recommendation, bro

I'd authorize the read-only partner-finding audit first, using the frozen MB1b artifacts. No new simulation runs, no changes to the baseline, and no reopening MB1b.

Then I'd review the audit before deciding whether to design a follow-up.

One important limitation: I'm evaluating the results as you've reported them here, not independently reproducing the analysis from the raw artifacts.

The central finding worth preserving is this: increasing opportunities for social contact changed who met and formed couples, but it did not meaningfully change the measured partner-finding constraints or extinction outcomes. Why those outcomes remained unchanged is the next question—not something MB1b has already answered.
