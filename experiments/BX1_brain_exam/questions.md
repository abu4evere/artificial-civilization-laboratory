# BX1: the one ACL comparison — the new brain's "where" against the old minds (DRAFT, not frozen)

- **The creator's decision (20 Nov 2026):** "we will test this brain inside acl once to compare current brain data with
  last acl brain data and then we will go back to brain itself again." Started together with the creator (23 Nov).
- **The brain:** Mind Lab's **MBb** (W3p-done, 23 Nov): MoveVIN that learns walls from its bumps; the best Mind Lab
  brain (detours 1.00, survives bare 0.99, Bob Profile 10/100).
- **Approach (scoping `../../../mindlab/acl_exam_scoping_2026-11-20.md`): the navigator transplant.** Each ACL person
  keeps the old mind (`acl/mind.py`) for **what** to do; the new brain scores **where** (which target tile). Smallest
  change, clearest answer; the whole-mind brains (NB2, NB3) died out, so we do not start there.

## Two phases (the creator, 23 Nov 2026)
**Phase A — one new-brain agent, watched (exploratory, labelled; first).** Give MBb to a single ACL person; everyone
else keeps the old mind. Watch that one agent closely: where it goes, what it chooses, its thoughts, how long it lives,
whether it thrives. Cheap (one heavy brain), safe (one agent can't collapse a world), and it is the bridge prototype +
the timing test Phase B needs. The agent can be highlighted in the atlas viewer. Quick adapter (a window around the
agent), not trained-in-ACL. Not a frozen statistical claim — a case study and a feasibility check.

**Phase B — everyone gets the new brain, compared to the last ACL brain (the frozen study; after A).** The formal
viable/better comparison (OLD vs NEW on 16 paired seeds), trained in ACL from birth, with council, the creator's
sign-off, checks and the blind recompute. Phase A's timing decides the years/seeds that fit our machines.

## The watched agent's "where" (Phase A default, the creator directing live, 23 Nov)
The new brain gives the **where** (a worth map over the tiles near the agent) and **replaces** the old hand-written
distance/pull term for that one agent; the old mind still picks the **what** (the action) and keeps the non-spatial
instincts. "Replace the where, keep the what" — the navigator transplant, purest to watch.

## The bridge (new code, written only after this plan is frozen and signed)
Each week, for the person deciding:
1. **Build an egocentric map** (the same channels MoveVIN was trained on) from the ACL person's own memory around them:
   food on tiles, water, home/shelter, never-seen, staleness. Read-only from the world; a brain change only.
2. **MoveVIN produces a worth map** from its feelings (hunger, tiredness, curiosity → the drives it already has) and
   its learned "can I enter here?" planning.
3. **Score the candidate tiles:** in `acl/mind.py` `decide`, each option has a target tile; add the brain's worth at
   that tile to the option's "where" term, in place of (or beside) the hand-written distance and pulls. The old mind
   still chooses the action and the randomness.
4. **Trained inside ACL from birth** with a parent (as W3d), the same recipe and kept copy, on ACL's senses — not the
   Mind Lab weights dropped in (ACL's eyes and body differ; named in the scoping note).

## Arms (16 paired seeds, nature v17 frozen)
| arm | the "where" | 
|---|---|
| OLD | the old minds' hand-written tile pulls (the baseline = the last ACL brain) |
| NEW | MBb's worth map scores the tiles |
Everything else identical: same worlds, same nature v17, same "what" and randomness.

## Readings (NB3's rules, so the numbers compare; frozen before data)
- **Viable (the bar):** extinct worlds at most the old minds' + 3; population ratio upper bound ≥ 0.80.
- Beside it: starvation share of deaths, child survival to 16, adult lifespan; and against NB1, NB2, NB3's published
  numbers ("current brain data compared with the last ACL brain data").
- A manipulation check: the new brain's worth actually moves where people go (its target tiles differ from the old
  minds' on the same situations).

## Before freezing (the scoping note's condition)
- **Measure the run time first, on one seed**, with the bridge in place: a 16-seed × ~600-year study is heavy, and it
  must fit the PC + Oracle + Google in reasonable time. This is an exploratory, labelled prototype, not the study.
- Council (GPT, Gemini, DeepSeek) on the plan.
- Then the creator's sign-off, the checks, and the run.

## Open questions for the creator and the council
1. Does the new brain replace the old "where" pulls entirely, or add to them? (Replace = the cleanest test of the
   brain; add = safer, less likely to collapse.)
2. One worth map per person per week is one MoveVIN run (30 planning rounds) — the timing test decides if 16×600 years
   is affordable, or if we need fewer years / seeds for the first comparison.
3. Train inside ACL from birth (true to the recipe) vs a frozen Mind Lab brain scoring tiles (cheaper, but its eyes
   never saw ACL). The scoping note prefers trained-in-ACL.
