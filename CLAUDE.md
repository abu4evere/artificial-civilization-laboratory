# Read this first (any assistant, any account)

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
- Book drafts in `drafts/book_rewrite/part2/` stay local: never commit or upload.
- No "Claude" or Co-Authored-By lines in commits. No API keys, passwords or payments.
- Don't publish or post (website, social) without the creator's explicit OK. Pushing commits to GitHub is fine.

## How work is done
- **GPT:** the creator's main ChatGPT chat is https://chatgpt.com/c/6adb8da9-5984-83ea-bff3-f4d9da68e4b3 (open it with
  the Claude in Chrome extension). You may ask GPT freely about ACL. Save its answers as `gpt_review_*.md`, labelled
  "GPT's opinion, not sign-off". Give the creator both views; only the creator decides.
  The Chrome extension follows one Claude account: after switching accounts, ask the creator to sign the extension
  into the current one. When typing into ChatGPT, send one paragraph (a newline sends the message early).
- **Cloud runs:** studies run on GitHub Actions (`.github/workflows/cloud-run.yml`), so the creator's PC can be off.
  `gh` is at `C:\Users\User\gh\bin\gh.exe`; fetch with `python tools/ci/fetch_cloud.py <run-id> <out_dir>`.
  The `tests` workflow runs only when code changes (`acl/`, `tests/`, `code_*`).
- **Tests:** `python -m pytest -q tests` (61 pass on nature v6).

## Where things are
- Current state and next step: the end of `WORKLOG.md`; `ROADMAP.md`; `docs/OPEN_DECISIONS.md`.
- All studies: `experiments/INDEX.md`. GPT's latest handoff: `docs/gpt_handoff_2026-10-24.md`.
