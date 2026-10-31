# Read this first (any assistant, any account)

**Latest handoff (30 October 2026): `docs/HANDOFF_2026-10-30.md`. Read it right after this file** (the 28 October one, `docs/HANDOFF_2026-10-28.md`, is older).

The creator works with more than one assistant account. This file is the shared mind: read it, then the tail of
`WORKLOG.md`, before doing anything. **After every real step, append one dated line to `WORKLOG.md`**, so whoever comes
next can pick up exactly where you stopped.

## What ACL is
An agent-based world of hunter-gatherers where **nature is programmed and culture is written by nobody**. The creator
writes the laws, never the history. The full why is in Book Part One, Chapter 0 and Chapters 1–12
(`book/editions/part1/the_world_that_nobody_wrote_part1.md`).

## The mission (the creator, 24 October 2026)
"Our mission is not to recreate Earth with the same human history but to create a world with **minimum laws** and a
period that produce an **autonomous and cognitive mind**." Earth and human evidence are the reference that keeps nature
honest (no tuning), not the blueprint. Later, "other natures" (one deep law changed at a time, frozen, never tuned) may
test which laws are truly needed (`docs/gpt_view_other_natures_2026-10-24.md`).

## Bob: the goal
Bob is the "final boss": the agent that will exist **when ACL succeeds**, one with **autonomy and a cumulative mind**.
Bob does not exist yet, and is not a person to pick or breed now. Every study is judged by whether it moves the world
toward minds that build on what they and others learned (cumulative) and choose their own goals (autonomy).
Bob matters more to the creator than civilization for its own sake. No LLMs inside ACL's people.

## Hard rules
- Freeze a plan (`questions.md`, git tag `X-frozen`) and get the **creator's sign-off** before any code or data.
- Never change nature (`acl/`, `code_vN`) without the creator's explicit decision. Zero checks before runs.
- No named inventions, recipe chains or rewards in nature (the test fails on invention names). Add conditions, not outcomes.
- Every number from a script; population beside every measure; append corrections, never rewrite findings.
- Judge work by diffs and executed tests, never by an assistant's own report.
- **Independent recompute** before a study's findings are final: a fresh session (another account or a new chat) or
  GPT recomputes the key numbers (the primary outcome and its interval, and any manipulation check) from the raw output
  files, **without seeing the study's analysis script**. Record it as `recompute_*.md` beside the findings. If the
  numbers disagree, the findings stay unfinished until the cause is found and appended. Record a model's recompute only from
  numbers actually read from its reply, never filled in ahead of it (an HL1 slip, 27 October, corrected in the open).
- Book drafts in `drafts/book_rewrite/part2/` stay local: never commit or upload.
- No "Claude" or Co-Authored-By lines in commits. No API keys, passwords or payments.
- Don't publish or post (website, social) without the creator's explicit OK. Pushing commits to GitHub is fine.

## How work is done
- **Talk to the creator simply** (the creator, 27 October 2026: "always send me messages more clearly simply"): plain
  words, short sentences, the big picture first, then what they need to decide. Keep technical detail in the files.
- **GPT:** the creator's main ChatGPT chat is https://chatgpt.com/c/6adb8da9-5984-83ea-bff3-f4d9da68e4b3 (open it with
  the Claude in Chrome extension). You may ask GPT freely about ACL. Save its answers as `gpt_review_*.md`, labelled
  "GPT's opinion, not sign-off". Give the creator both views; only the creator decides.
  **Ask Gemini too (the creator, 27 October 2026):** every question put to GPT also goes, the same text, to Gemini
  (https://gemini.google.com, in the same Chrome). Compare the two answers (where they agree, where they differ) and
  save both in the same `gpt_review_*.md` / `gpt_view_*.md` file, each labelled as an opinion, not sign-off. It is a **debate**: Claude is the council. Check each claim against the code and
  the records; where either model is wrong, tell that model with the facts and let it defend or revise; pass each one's
  main argument to the other for a reply. Report to the creator who argued what, and what survived checking.
  The Chrome extension follows one Claude account: after switching accounts, ask the creator to sign the extension
  into the current one. When typing into ChatGPT, send one paragraph (a newline sends the message early). The main chat is very long and the
  page can freeze when typing: insert the text with JavaScript (`document.execCommand('insertText', ...)` on
  `div.ProseMirror[contenteditable="true"]`; `#prompt-textarea` is gone since 28 October) and click the send button
  (`[data-testid="send-button"]`, or the round button right of the input if that is not found).
- **Cloud runs:** studies run on GitHub Actions (`.github/workflows/cloud-run.yml`), so the creator's PC can be off.
  `gh` is at `C:\Users\User\gh\bin\gh.exe`; fetch with `python tools/ci/fetch_cloud.py <run-id> <out_dir>`.
  Run the zero checks locally first and commit `zero_local.log`, then launch with `-f skip_zero=local`. The cloud then
  only checks that record (All: PASS, same code fingerprint) instead of re-running the zero checks, which saves about
  15–20 minutes.
  The `tests` workflow runs only when code changes (`acl/`, `tests/`, `code_*`).
- **Tests:** `python -m pytest -q tests` (65 pass on nature v10, live since 31 October 2026: ageing anchored to the
  !Kung, `mortality_base` × 0.0072/0.0249; `experiments/NV10_nature_v10/findings.md`; v9 = curiosity pull, 29 October).
  New studies use `code_v10`; v9 findings stay v9's (IW1 was frozen on v9 and runs on v9).

## Sleep mode (autonomous since 27 October 2026)
When the creator says "sleep", they are going to sleep. **The project must not stop.** The creator (27 October): "you
gotta work autonomy decide without me do not wait for me. Main priority not to stop project any time. Just measure
success rate if its more than 40% just go ahead without me. Overally you do everything i am giving you permission for
that."

**Sleep mode starts by itself** when the creator has not written for more than an hour (the creator, 27 October: "if i
do not be here for more than 1 hour it means you can start sleep mode automaticly … do not wait for me all the time").
An hourly heartbeat (a session cron job) checks this and keeps work going. Recurring jobs expire after 7 days; renew the
job when the creator is around.

So in sleep mode the assistant decides in the creator's place, including the steps that otherwise need their sign-off:
- drafting, freezing and signing off studies;
- running them on GitHub;
- analysing them and getting the independent recomputes;
- choosing the next study;
- with care, proposing and testing a nature change as a frozen study.

**How each decision is made:**
1. Ask GPT and Gemini the same question, and act as council.
2. Estimate the chance that the step succeeds: it is valid, it answers its question, and it keeps to ACL's rules.
3. **Go ahead if that estimate is 40% or more.** Otherwise pick a safer step (usually a read-only study) rather than
   stopping.
4. Record every autonomous decision in `docs/autonomous_decisions.md`, with the estimate, the models' votes and the
   reason. Sign-offs read "the assistant, under the creator's sleep-mode autonomy".

**Keep researching (the creator, 30 October 2026):** "do not forget to do research all the time because we may find
good sources we can use we can find our solutions somewhere maybe". Whenever runs are going, look for published work
(anchors, mechanisms, methods) bearing on the open question, read it, label what was read (full text / abstract /
record only), never invent a source, and save notes under `docs/research/`. A source suggests; only a frozen study
decides.

**Still never, even in sleep mode:**
- tune nature towards an outcome, or break the hard rules above (frozen plans, zero checks, recompute, no named
  inventions);
- publish or post publicly (website, social);
- upload the book;
- spend money or touch credentials;
- delete data or history.

**Adopting a new nature version as live** (`acl/`) **is allowed autonomously by the safe path** (the creator, 31 October
2026, at the PC in this Claude Code session, choosing "Adopt with safe path"; this replaces the 30 October rule "never
autonomous"). The assistant may adopt a version itself only when **all** of these hold, in this order:
1. a frozen study whose result supports the change (findings final);
2. an independent blind recompute by GPT and Gemini that matches;
3. **a confirmatory run on new seeds** that also supports it (not needed when the creator decides the version
   themselves, by a message naming it);
4. both GPT and Gemini consulted on adoption, with the assistant's estimate of success at 40% or more;
5. a new `code_vN` with zero checks (off = the previous nature; on = the study's arm);
6. reference hashes regenerated and the tests passing;
7. a git tag `nature-vN`, a line in `docs/autonomous_decisions.md`, and a Telegram message to the creator
   (`tools/notify.py`).

Adoption needs the browser (GPT and Gemini), so it happens in interactive or heartbeat sessions, **never in a scheduled
tick or a Telegram session**. Tuning nature towards an outcome stays forbidden. The creator can always decide a
version directly, by a message naming it.

The previous nature stays in `code_v(N−1)`, so the change can always be undone.

Log every step in `WORKLOG.md` and leave a short morning report listing every autonomous decision.

## Where things are
- Current state and next step: the end of `WORKLOG.md`; `ROADMAP.md`; `docs/OPEN_DECISIONS.md`.
- All studies: `experiments/INDEX.md`. GPT's latest handoff: `docs/gpt_handoff_2026-10-24.md`.
