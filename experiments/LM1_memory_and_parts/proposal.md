# LM1 — Memory or parts? A Law 126 study (SIGNED OFF 20 October 2026; frozen as `LM1-frozen` before any code or data)

**Why.** Three read-only audits traced where ACL's chain of cumulative culture breaks. CA1: about nine in ten useful
inventions are never learned by anyone but their inventor. CA2: most are lost before any lesson (G1–G2), and the few
composites that are shown can almost never be followed (G7). CA3: the loss before any lesson is **memory** (99% pushed
out of the inventor's 12-recipe limit within a season), and a composite's parts were known by the listener in about **1
teaching talk in 12**. Two evidence reviews (notes only) sit beside them: `../CA3_opportunity/evidence_teaching.md`
and `../CA3_opportunity/evidence_memory.md`.

Drafted on GPT's review under the creator's delegation ("Law 126 proposal — APPROVED AS A DRAFT ... Treat this as a
design sketch, not authorization to run it"). **Changing either rule is a change to nature (Law 126): the creator
decides.** GPT's warning stands: "our goal isn't to make ACL agents preserve more inventions by any means necessary."

## Three hypotheses, all kept alive

- **A, memory:** useful inventions vanish because inventors lose them before passing them on. In ACL that loss comes
  from a rule no source supports in its form: a hard limit of 12, new recipes valued at zero, and ties broken by name so
  that composites are dropped first.
- **B, prerequisites:** inventions fail to spread because learners cannot follow them: a composite can be taught only to
  someone who already makes every part. Living learners meet parts and simpler versions first (Lew-Levy et al. 2017;
  Tehrani and Riede 2008; Stout 2002).
- **C, both:** memory removes the chances to teach, and prerequisites waste the chances that remain; fixing one alone
  may not be enough.

## The candidate changes (one of each; alternatives listed for the creator)

**Memory (Decision 1).**
- **M1, the tie-break only (recommended first, as GPT asked):** when recipes tie for least valued, drop the one held
  longest instead of the one whose name sorts first. Nothing else changes: still 12, new recipes still start at 0. It
  removes a bookkeeping accident, not a claim about human memory.
- M2: a new recipe cannot be dropped for its first N weeks (needs a number no source gave; not recommended now).
- M3: replace the hard limit with gradual forgetting that depends on use (closest to the skill-decay literature, but
  needs several numbers; a larger change; not recommended now).

**Learning (Decision 2).**
- **L1, parts first (recommended):** when a teacher chooses to show a composite and the learner cannot make one of its
  made parts, the teacher shows that part instead (if the teacher knows it), as a lesson of its own, passing the same
  checks as any lesson (new to the learner, believed, followable). One recipe per lesson, as now. The learner can learn
  the whole later, in another lesson. Nothing becomes understandable without its parts.
- L2: let a learner take a composite without its parts (rejected: it would make every invention understandable to every
  agent, which GPT ruled out).

## Design sketch (GPT's four arms)

| arm | memory rule | learning rule |
|---|---|---|
| C | today (12, ties by name) | today (all parts needed) |
| M | M1 (ties by age) | today |
| L | today | L1 (parts first) |
| ML | M1 | L1 |

- **Seeds:** 256 new worlds per arm (1,024 in all), 20 founders, 40 × 40, 120 years, nature v2; CA1's observer and
  CA2's logging copy loaded unchanged. A sham arm optional (Decision 3).
- **Primary (Decision 4):** the share of useful inventions passed on to anyone (CA1's link 3), per world, each arm
  against C, paired by seed; and the 2 × 2 interaction (does ML exceed what M and L each add?).
- **Also measured** (GPT's list): survival time of useful knowledge; reaching a teaching talk; successful transmission;
  whether learners make the thing; whether a learner builds a better thing on it and that is passed on (CA1's links 5
  and 6, with CA2's "who built on what"); extinction and population, as possible costs.
- **Checks:** zero checks (each rule off = today exactly); manipulation checks (M: composites no longer dropped first
  among ties; L: parts-first lessons happen); fresh seeds; predictions frozen before code.

## Limitations, stated before any design is frozen

- Neither rule is anchored to a measured human number; M1 removes an accident, L1 follows a qualitative pattern in the
  ethnography.
- A rise in transmission would show what becomes possible under these rules, not that real culture began this way.
- Worlds with more knowledge kept may differ in population, which must be shown beside every measure.

## Decisions for the creator

1. Memory change: **M1, ties by age** (recommended), or M2 / M3, or none.
2. Learning change: **L1, parts first** (recommended), or none.
3. Sham arm: yes or no.
4. Primary: **share of useful inventions passed on, with the interaction** (recommended), or another.
5. Whether to proceed at all: freeze as a study after MB1b, RT1b and FX2, or hold.

## Revision 1 after GPT's review (19 October 2026; still a draft)

GPT: "I approve the direction, not the freeze yet", with these points, all taken in:

- **M1, defined precisely.** It acts only when two or more recipes tie under today's least-value rule. Among the tied,
  the one held longest is dropped; if held equally long, the one learned earlier in the person's life order; only then
  by name. The 12-recipe limit, the zero starting value and every other memory rule stay as they are. A check logs
  every tie and shows that M1 changes **only** which tied recipe goes. M1 is described as **a controlled correction to
  an implementation choice, not a model of human memory**: "It cannot establish how human memory works."
- **L1, without telepathy.** As first drafted, the teacher would have known which parts the learner lacked: knowledge
  of another person's mind that ACL does not give. Revised: L1 acts only on a **visible failure**. When a lesson on a
  composite fails because the learner cannot follow it (CA2's G7), in that same lesson the teacher shows instead **one
  made part of that composite that the teacher knows**, the first in the recipe's own order, without knowing whether the
  learner lacks it. That part lesson passes the usual checks (new to the learner, believed, followable) and may fail.
  It uses **the same talk, the same single lesson and the same cost** as any lesson: no extra lesson, no extra time. If
  the teacher knows no made part of it, nothing happens, as today.
- **Primary, with its denominator.** The share of useful inventions passed on, exactly CA1's link 3: useful kinds
  (largest factor ≥ 1.05) first appearing in a world, passed on if anyone other than the first knower learned them;
  denominator = all useful kinds in that world, including those lost before any teaching chance. Per world, each arm
  against C, paired by seed. The number of useful kinds created is reported beside it, so a change in creation cannot
  pass for a change in transmission.
- **The interaction, preregistered:** (ML − L) − (M − C), per world, paired, with its own test and interval, fixed
  before the run.
- **Five different achievements, kept apart** (GPT's point 4): a learner **holding** the object; **knowing** the
  recipe; **making** it (a `make` event by the learner); **improving** it (a better kind first made by someone who had
  learned the part from someone else, CA2's "a learner"); and **passing on** the improvement. L1 counts as helping only
  if more than parts are passed around.
- **Manipulation checks:** M1: among ties, composites are no longer dropped first (share of composite drops among ties
  falls to their share of tied recipes); L1: part lessons happen, and some succeed.
- Fresh, paired seeds for all four arms; today's baseline preserved exactly by the zero checks.

GPT's principle, kept as the proposal's own: "We should change the rules that prevent knowledge from accumulating—not
give agents the ability to accumulate knowledge by assumption."

## GPT's final review (19 October 2026): "Send LM1 to Abdurashid for sign-off"

"The remaining checks are implementation and preregistration checks, not reasons to redesign the study." Added:

- **M1 log checks:** only tied candidates considered; the longest-held dropped; equal holding times by earlier
  learning, then name; **no other recipe, value or random-number draw changes** (M1 draws no random numbers; a check
  compares the random state with and without M1 at every tie).
- **L1 is one lesson:** the failed composite lesson and the part shown instead are the same lesson in the same talk,
  at the same cost, enforced in the code and in a test. Choosing the first known part in recipe order is a stated
  implementation choice, not a claim about how real teachers choose; the share of part lessons by recipe shape is
  reported.
- **Reported together, identically defined in all four arms:** useful kinds created; useful kinds passed on; the link-3
  proportion; knowledge survival and each transmission stage.
- **The interaction test, fixed now:** per world, (ML − L) − (M − C) on the link-3 proportion; Wilcoxon signed-rank
  test; 95% bootstrap interval (10,000 resamples, `random.Random(2026)`). Support for an interaction: p < 0.05 and an
  interval excluding zero. **A non-significant result is reported as "not shown", never as "no interaction".**

GPT: "I especially like one thing about this design: L1 can fail ... That's exactly what makes it a scientific test
rather than a scripted success. No run until the required sign-off and frozen protocol are recorded."

## Sign-off (20 October 2026)

Asked about LM1, the creator answered: "**go ahead**". Read as approving every recommendation: (1) memory change **M1,
ties by age**; (2) learning change **L1, parts first**; (4) primary: **share of useful inventions passed on, with the
interaction**; (5) **freeze, to run after MB1b, RT1b and FX2**. Decision 3 (sham) had no recommendation; the assistant
set **no sham** (the four arms are paired by seed, and chance is measured by the paired tests), recorded here so the
creator can add one before any data. This is a study of rule changes, not their adoption into nature: adopting either
would be a separate Law 126 decision. The prior below is frozen.

## Operational details (fixed at freezing, before any code)

- **Code `code_lm1`:** a copy of `code_v2` plus two settings, both default 0 (= `code_v2` exactly): `memory_ties_by_age`
  (M1) and `parts_first` (L1).
  - **M1:** in `knowhow.remember_recipe`, when the 13th recipe arrives, the least-valued recipe is dropped as today;
    among recipes tied at that least value, the one **held longest** (earliest in the person's own recipe order, which is
    the order they were learned or made) is dropped, instead of the one whose name sorts first. No random number is
    drawn.
  - **L1:** in `information.hear_how`, when a lesson fails only because the learner cannot follow it (a made part they
    cannot make), the teacher shows instead, in the same lesson, the **first made part of that recipe, in the recipe's
    own order, that the teacher knows how to make**, through the same `hear_how` with the same claim, so it passes the same
    checks (new to the learner, not refused, believed, followable) and may fail. At most one substitution per lesson; a
    part lesson that fails at its own followability check is not substituted again. If the teacher knows no made part of
    it, nothing more happens.
- **World and seeds:** nature v2, 20 founders, 40 × 40, 120 years; arms `c`, `m`, `l`, `ml`; **seeds 7001–7256**
  (unused by any study); 1,024 worlds, after FX2.
- **Observers (read-only):** CA1's chain observer (unchanged), extended as CA3 to save each kind's first knower and its
  learners; plus a count of `make` events by people other than the first knower, per kind.
- **Primary:** per world, link-3 proportion = useful kinds (largest factor ≥ 1.05) passed on to anyone other than the
  first knower ÷ all useful kinds first appearing in that world. M, L and ML each against C, paired by seed: Wilcoxon
  signed-rank; effect = mean paired difference with a 95% bootstrap interval (10,000 resamples, `random.Random(2026)`);
  Holm over the three. **Interaction** as fixed above: (ML − L) − (M − C), its own test, not in the Holm family.
  Reading: an arm "changes transmission" if Holm p < 0.05; "not shown" otherwise (never "no effect" without an interval
  inside ±0.02 of the control's proportion, which is then called "no meaningful effect").
- **Reported beside (identical definitions in all arms):** useful kinds created; passed on; knowledge survival time;
  the five achievements (holds, knows, makes, improves as a learner, passes the improvement on); extinction and median
  population by decade.
- **Hard stops:** zero checks (both settings 0 = `code_v2`; each setting acts; observers read-only; save and reload
  exact); M1 log check (ties only; longest-held dropped; random state unchanged by M1); manipulation checks (M: the
  share of composites among recipes dropped from ties falls to their share of tied recipes, ± 0.05; L: part lessons
  occur in every L and ML world that lives 10 years, and some succeed); all 1,024 worlds; one fingerprint.

## The assistant's prior (frozen; held loosely)

M alone: small rise in link 3 (the accident it removes falls on composites, a minority of kinds). L alone: small rise.
ML: larger than either, but the interaction "not shown". Improvement by a learner stays rare (under 10% of link-5
pairs) in every arm.

## Amendment 1 (proposed 20 October 2026, before any data; NEEDS THE CREATOR'S APPROVAL)

**What the smoke test showed** (throwaway seeds 9951–9952, 10 years; code check only): M1 does exactly what it says:
in M and ML worlds the longest-held recipe was dropped in **100%** of ties (C: about 6%), and composites fell from
96–100% of tie drops (C) to about 64%. But the frozen manipulation check, "composites' share of tie drops within 5
points of their share of tied recipes", came out **64% against 73%: NO**. The check was wrong, not the rule: dropping
the oldest recipe is not dropping at random, and recipes learned earliest are less often composites, so their share
among drops need not match their share among ties. Under the frozen check, LM1 would be declared invalid though M1
worked.

**Proposed change (the M manipulation check only):** M1 passes if, pooled over M and ML worlds, **the longest-held
recipe is dropped in at least 99% of ties**, and composites' share of tie drops is **lower than in C** (it was the
naming accident that made them go first). Their share of tie drops against their share of ties is reported, not a hard
stop. Nothing else changes: arms, seeds, primary, interaction and readings stand as frozen.

The run will not start until the creator approves this amendment (the queue checks for the word "APPROVED" in the
line below).

Amendment 1 status: awaiting the creator.
