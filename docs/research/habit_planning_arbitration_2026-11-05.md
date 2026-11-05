# How does the brain choose between habit and deliberate prediction? (research note, 5 November 2026)

Written while PB2 runs on the cloud. In PB2's arm P, the memory's estimate r-hat **replaces** the habit table q
wherever the person has lived the action. Council round 61 rejected simply adding the two, because that counts twice
with an arbitrary mix. If PB2 shows that full replacement hurts (a guard raised, or worse chains), is there a
**principled** way to mix the two that is not tuned? A source suggests; only a frozen study decides.

## Lee, Shimojo & O'Doherty (2014)
"Neural computations underlying arbitration between model-based and model-free learning". *Neuron* 81(3), 687–699.
DOI [10.1016/j.neuron.2013.11.028](https://doi.org/10.1016/j.neuron.2013.11.028); PMC3968946; PMID 24507199.
**Read:** abstract, introduction, model description, behavioural results and discussion, from PubMed Central's full
text through the PubMed tool. Not read: the supplementary model equations. Volume, issue and pages checked in PubMed's
record.

**What they did:**
- 22 adults in fMRI, on a two-step choice task for coloured tokens.
- "Specific goal" trials: only one colour pays, and the colour switches from trial to trial. These favour deliberate,
  model-based control.
- "Flexible goal" trials: any colour pays. These let habit (model-free control) take over.
- The task's transition uncertainty changed over blocks.
- They compared six arbitration models.

**What they found** (as reported by the authors):
- The best model gives each system control **in proportion to how reliable its recent predictions have been**:
  - the deliberate system's reliability comes from its state-prediction errors;
  - the habit system's reliability comes, more simply, from the size of its reward-prediction errors.
- Versions where behaviour drifts toward habit over time (since deliberation costs effort) fit better.
- Reliability signals were found in inferior lateral prefrontal and frontopolar cortex. Where the arbitrator favoured
  deliberation, it appeared to **damp** the habit system's value signal, rather than add the two together.
- The integrated value in vmPFC looked like a weighted sum of the two values, weighted by the arbitrator.

## What it means for ACL (suggestions, not decisions)
1. **A general law, not a tuned number:** "trust each predictor in proportion to its recent reliability" needs no
   chosen weight. The weight comes from each person's own prediction errors. If PB2's P fails, a reliability
   arbitration between q and r-hat is a natural next candidate for its own frozen study.
   - ACL already has both error signals: q's error (the reward prediction error it learns from) and the memory's
     error (PB2 already tracks the memory's standardised errors for learning progress).
2. **It fits the parked creator's list**, item 2, "brains that evolve": how fast trust shifts could be a heritable
   trait rather than a written constant.
3. **It does not change PB2.** PB2 is frozen and running. This note only prepares the next candidate, and records
   that the human brain seems to arbitrate rather than replace.
4. **A caution:** this is a lab task with two steps and money. ACL's world is far richer. The evidence supports the
   general principle (reliability-weighted control), not any specific formula.
