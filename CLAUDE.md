# Read this first (any assistant, any account)

**Latest handoff (2 November 2026): `docs/HANDOFF_2026-11-02.md`. Read it right after this file** (the 30 October one, `docs/HANDOFF_2026-10-30.md`, is older).

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

## Direction: open the doors, then freeze the world, then the brain (the creator, 7 November 2026)
The creator: "bug=law" … "we should freeze the world for a while and focus almost entirely on building the Bob's
brain". Inside a world, a bug feels like a law (gravity could be one), and no one can tell in reasonable time which
quirk shapes the world and which blocks it. A perfect world is not needed; a world that permits survival and learning,
plus minds capable of cumulative adaptation, may be enough (the Minecraft lesson: simple rules that combine, and people
build what the makers never planned). The creator chose this order (the assistant's recommendation "B"):
1. **Open the closed doors, once:** one package of general laws through properties, never named things (made things
   as binders or hammers when their properties allow, containers that contain, made things in heaps, tools together,
   room to carry; `docs/affordance_audit_2026-11-02.md`). It goes as one frozen test with a sham.
2. **Then freeze the world** (nature after step 1) until a review on **7 December 2026**.
   - While frozen, there are no world-rule studies and no fault hunts.
   - The one exception: code that plainly does not do what its own comment says may be fixed quickly.
   - A brain test that shows the world lacks something is noted for the review, not acted on.
3. **Then almost all work goes to Bob's brain.** It starts **together with the creator**. The creator, 8 November
   2026: "we will start together when we move to brain itself till that you keep working yourself". No session
   starts brain design or brain studies alone before that. The focus: value, memory, curiosity, learning from others, building on what
   others learned, and choosing one's own goals.
   - Law tests of the mind (like VW1) are brain work, so they also wait for the creator.
   - World and biology laws (like law B, "both parents feed", council round 79) are paused.
4. **The aim of the brain work** (the creator, 7 November 2026): "Don't build a world where intelligence is guaranteed to succeed. Build a mind capable of discovering how to succeed in the world it inherits. The important ability isn't never making mistakes. It's learning from them." So the doors only open possibilities; they never make success easy.

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
- **The creator's ideas go into the book notes automatically** (the creator, 31 October 2026: "do not ask me to add my
  ideas to the book but add them automaticly"). Whenever they share an idea or reflection about the project, append it,
  in their exact words, to `drafts/book_rewrite/part2/notes_for_book_<date>.md` (local only, gitignored; never commit or
  upload). Never write feelings for them; leave [YOUR WORDS: …] where only they can speak.
- **GPT:** the creator's main ChatGPT chat is https://chatgpt.com/c/6adb8da9-5984-83ea-bff3-f4d9da68e4b3 (open it with
  the Claude in Chrome extension). You may ask GPT freely about ACL. Save its answers as `gpt_review_*.md`, labelled
  "GPT's opinion, not sign-off". Give the creator both views; only the creator decides.
  **Ask Gemini too (the creator, 27 October 2026):** every question put to GPT also goes, the same text, to Gemini
  (https://gemini.google.com, in the same Chrome). Compare the two answers (where they agree, where they differ) and
  save both in the same `gpt_review_*.md` / `gpt_view_*.md` file, each labelled as an opinion, not sign-off.
  **Ask DeepSeek too (the creator, 2 November 2026):** "i also opened deepseek tab use that as extra for gpt and
  gemini from now on you will use those 3". DeepSeek (https://chat.deepseek.com, in the same Chrome) gets the same
  question text as GPT and Gemini, and its answer is saved beside theirs, labelled as an opinion, not sign-off. Its
  briefing on ACL is `docs/deepseek_briefing_2026-11-02.md`. It is a **debate**: Claude is the council. Check each claim against the code and
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
- **Local runs must not slow the creator's PC** (1 November 2026: the PC lagged under four of the assistant's
  simulations). Run local simulations at Idle priority (PowerShell: `(Get-Process -Id <pid>).PriorityClass = 'Idle'`,
  or start them with `start /low`), at most 2 at once; prefer the cloud for anything long. **While the creator is away**
  (the creator, 1 November 2026: "Now u can use pc at max capacity cuz i am not working its all your own just lmk what is
  happening through telegram"), local runs may use full speed, up to 4 at once (`research/state.json` budgets); report
  through Telegram. The careful setting returns when they are back.
- **Tests:** `python -m pytest -q tests` (71 pass on nature v16, live since 7 November 2026 (evening): forage, hunt and
  gather are offered at the best target the person can afford when the best is too far (FF4, a fault fix;
  `experiments/NV16_nature_v16/findings.md`); v15 = children aged 3
  and over may make again what they know (CI1 and CI1-C; `experiments/NV15_nature_v15/findings.md`); v14 = memory ties
  drawn evenly instead of by name (FF3), 6 November; v13 = FF2's three hunt, carry and water fixes, 3 November;
  v12 = FF1's fixes; v11 = handing made things). New studies use `code_v16`; earlier findings stay their version's.
  findings stay their version's.

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

**Editing the world's rules (the creator, 2 November 2026, at the PC in this Claude Code session):** "I give you
permission to edit world rules. Take a look and check all rules. If you find something fix it or add any new rules.
From now on keep working without me". So the assistant may review every rule of nature, propose fixes and new rules,
and adopt them without asking first. How:
- each change is still **a general law or a fix of a fault**, never a named invention, recipe chain or reward, and never
  tuned towards an outcome;
- each goes through the same path: council (GPT and Gemini), a frozen test in a copy with a sham, the blind recompute,
  a confirmatory run on new seeds, then the safe-path adoption above (steps 4–7);
- a plain **fault in the code** (a rule that does not do what its own comment or plan says) may be fixed as a new
  `code_vN` after zero checks and tests, with the fault shown in a recorded check, without a full study;
- the guiding aim is the creator's: open what people can do through general abilities and physics
  (`docs/action_audit_2026-11-02.md`, `docs/affordance_audit_2026-11-02.md`); tell the creator on Telegram each time a
  rule goes live.

Log every step in `WORKLOG.md` and leave a short morning report listing every autonomous decision.

## Where things are
- Current state and next step: the end of `WORKLOG.md`; `ROADMAP.md`; `docs/OPEN_DECISIONS.md`.
- All studies: `experiments/INDEX.md`. GPT's latest handoff: `docs/gpt_handoff_2026-10-24.md`.
