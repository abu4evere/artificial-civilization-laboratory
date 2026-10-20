# Work log (helper and creator, while the assistant is unavailable)

One line per action, newest at the bottom: date and time, what `tools/acl_status.py` said, what was done.
Rules: `docs/HELPER_RUNBOOK.md`. The assistant reads this first when it is back.

- 2026-10-18 02:59 The assistant, sleep mode: RT1 at 258/768; started MB1b setup draft (creator's decision: P = 40x40, 80 founders, documented as a different setting).
- 2026-10-18 03:01 The assistant: MB1b draft written (questions_mb1b.md), committed; waits for the creator's sign-off.
- 2026-10-18 03:03 The assistant: CI green incl. live v2 (435dcf0). FX1 evidence review started (force-to-open food): Kaplan et al. 2000 via Kaplan, Gurven & Winking 2009 — forager calories hunted ~60%, extracted ~32%, collected ~8%; ACL diet measurement running (16 worlds, read-only). RT1 at 266/768.
- 2026-10-18 03:38 The assistant: FX1 done — ACL diet 98.9% collected / 1.1% crop / 0.02% meat vs foragers 8/32/60 (evidence.md, INDEX, decisions).
- 2026-10-18 03:40 The assistant: FX1 extended — Aché return rates (Hill et al. 1987, full text): hunting ≈ gathering per hour (1,339 vs 1,221 cal/hr); ACL hunting ≈ 4% of foraging.
- 2026-10-18 03:40 The assistant: FX1 — located the four code causes of low hunting returns (chance 0.10 base; zero chance without prey on tile; small game; meat beyond carrying lost). Note only, nothing changed.
- 2026-10-18 03:41 The assistant: living-book Chapter 84 'What They Ate' (FX1).
- 2026-10-18 20:11 The assistant (creator away, GPT delegation): MB1b Amendment 1 approved via GPT; torus-distance correction found and fixed before data; zero PASS, smoke placement ok; committed 1913393, tag MB1b-amend1; MB1b run started (1,024 worlds, ~40 h). Drafted RT1b and FX2 for sign-off.
- 2026-10-18 20:28 The assistant: GPT chose all RT1b/FX2 recommendations but kept both as drafts until the creator reads them; code + zero checks (PASS both) + mechanism-only pilots done (RT1b fix works: 46% -> 1.8%). Nothing frozen.
- 2026-10-18 20:31 The assistant: HB1 lead checked from saved tables only (contradicted; note appended to RT1 findings). GPT: stop new science, upkeep only; noted GPT says its answers are not creator authorization (flagged in MB1b plan). Handoff: drafts/handoff_2026-10-18.md. MB1b: 7/1024.
- 2026-10-18 21:03 Creator confirmed MB1b Amendment 1; run continues (23/1024).
- 2026-10-18 21:32 RT1b signed off and frozen by the creator (RT1b-frozen); runner + analysis smoke-tested (4fee841); watcher after_mb1b.sh will start RT1b when MB1b says ALL DONE (if the session restarts, start it by hand: python experiments/RT1_residence_time/run_rt1b.py run).
- 2026-10-18 22:16 FX2 signed off and frozen by the creator (FX2-frozen, with notes; seeds 6001-6256). Observer extended (hard thing actually used); zero re-run PASS; runner + analysis smoke-tested. Watcher after_rt1b.sh starts FX2 when RT1b says ALL DONE (if the session restarts: python experiments/FX2_embedded_food/run_fx2.py run).
- 2026-10-18 23:46 CA1 chain audit signed off and frozen (CA1-frozen); zero PASS; run started on 2 extra workers (36 worlds).
- 2026-10-19 00:18 The assistant, sleep mode: CA1 at 12/36, MB1b at 127/1024. Plan: when CA1 ends, analyse, findings, upkeep, book chapter.
- 2026-10-19 01:19 CA1 done: bottleneck = transmission (11%/10% of useful inventions ever learned by another), prior wrong; findings, INDEX, ROADMAP, decisions, book Ch 86 'The First Hand-Over', book rebuilt.
- 2026-10-19 01:19 Drafted CA2 (teaching gates + CA1's 'who built on' caveat) for sign-off; not frozen. MB1b at 148/1024.
- 2026-10-19 01:21 GPT reviewed CA2 (six refinements, all adopted into the draft; decision 5 added). Still a draft.
- 2026-10-19 01:36 CA2 signed off and frozen (CA2-frozen); logging copy zero PASS; run started on 2 workers (32 replays of CA1's worlds). Sleep mode.
- 2026-10-19 03:05 CA2 done: most losses before any lesson (G1 46%, G2 36-39%); narrowest gate G7 followable (1.2%/0.5%); building on others' taught parts 4%. Priors wrong. Findings, INDEX, ROADMAP, decisions, book Ch 87.
- 2026-10-19 03:07 GPT reviewed CA2's result: (a) read-only audit first, then (b) evidence review; drafted CA3 (opportunity vs availability) for sign-off. Not frozen.
- 2026-10-19 13:29 Creator away 4-5 h (work with GPT). CA3 signed off/frozen, zero PASS, run started (32 replays, 2 workers). Creator added becominghuman.org (ASU IHO) as a source; to use in CA3 step (b) evidence review. MB1b at 517/1024.
- 2026-10-19 14:54 CA3 done: availability 99% (12-recipe limit), composites followable 7.6/8.4%; prior right. Findings, INDEX, ROADMAP, decisions, book Ch 88 'Twelve Places'.
- 2026-10-19 14:57 GPT approved as drafts: memory evidence review (written) and Law 126 proposal LM1 (written: M1 tie-break by age, L1 parts-first lessons, 2x2). Nothing frozen. MB1b at 546/1024.
- 2026-10-19 15:00 LM1 reviewed twice by GPT: revision 1 (L1 now acts only on a visible failed lesson) and final checks added; GPT: send to the creator for sign-off. Not frozen.
- 2026-10-20 17:23 Restart had stopped all runs (MB1b at 607/1024, files intact). MB1b resumed (skips saved worlds; first log kept as run_mb1b_part1.log); RT1b and FX2 auto-start watchers restarted.
- 2026-10-20 17:42 LM1 signed off and frozen (LM1-frozen); code built; zero PASS (incl. M1 leaves the random state unchanged at 354 drops); smoke + analysis tested. Smoke showed the frozen M manipulation check is wrong (oldest-drop is not random); Amendment 1 proposed, awaiting the creator. LM1 queued after FX2, gated on Amendment 1 approval.
- 2026-10-20 00:11 Book: free PDF + release cover now match Amazon (How I tried, Part One); Kindle submitted, paperback set up (ISBN 9798163874385) and left for the creator to publish. Sleep mode on. MB1b at 827/1024 (~7 h left); RT1b, FX2 watchers alive; LM1 waits on its Amendment 1.
- 2026-10-20 00:18 Creator: book is Amazon-only. Release assets (PDF, Word, first edition) removed (local copies kept); release notes and README point to Amazon; book text and builds untracked + gitignored (cddc6e5). Still public, needs the creator: LinkedIn document post (creator deletes), old git history/tag v1.0 source zips and add_*.py chapter scripts (history rewrite = creator's call). Zenodo package must drop the book.
- 2026-10-20 09:31 MB1b done (finished 06:10; RT1b auto-started 06:14): no meaningful effect on survival (13/8/7 of 256), smaller bands mix far more (cross-lineage couples 6%->54%), partner blocking unchanged. Findings, INDEX, ROADMAP, decisions, living-book Ch 89 (local only), tag MB1b-done.
- 2026-10-20 09:42 Sent MB1b result, RT1b status and book move to GPT (creator's request); reply recorded verbatim (gpt_review_mb1b.md): recommends a read-only partner-finding pipeline audit first. Added to OPEN_DECISIONS.
- 2026-10-20 12:17 LM1 Amendment 1 approved by the creator (tag LM1-amend1-approved); analyse_lm1.py M check updated, smoke PASS. LM1 now starts automatically after FX2. PF1 frozen (PF1-frozen); zero check running. Project website live (abu4evere.github.io/simulated-world).
