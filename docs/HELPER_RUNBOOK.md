# Helper runbook: what a local helper (Ollama) may do while Claude is unavailable

Written by Claude, 12 October 2026, for the creator. When Claude's usage limit is reached, a local model in Ollama can
help the creator keep ACL's background runs going. The helper **follows these steps exactly and changes nothing
else**. Claude checks everything in `WORKLOG.md` when it is back.

**Why the limits are strict.** ACL's science depends on frozen plans and on nobody adjusting anything after results
exist. A helper that "fixes" something could make months of results unusable. So the helper may only **run the commands
below, read their output, and write in `WORKLOG.md`**.

## Never

1. Never edit any file except `WORKLOG.md` and files in `drafts/`.
2. Never edit anything in `acl/`, `experiments/`, `tests/`, `book/`, `docs/`, `ROADMAP.md`, `DESIGN.md` or `bible_dump.txt`.
3. Never delete any file, especially outputs (`*.json`), even ones that look broken.
4. Never run `git` (no commit, no push, no reset, no checkout).
5. Never start an experiment other than with `python tools/acl_resume.py`.
6. Never interpret results or decide what they mean. Running a frozen analysis script is allowed (step 3); reading it is
   Claude's job.
7. If anything is unclear or unexpected: **stop**, write it in `WORKLOG.md`, and wait for Claude.

## Every session: three steps

Open a terminal in `D:\acl` (PowerShell: `cd D:\acl`).

**Step 1: check.**
```
python tools/acl_status.py
```
Every line starts with **OK**, **WAIT**, **DONE**, **INFO** or **PROBLEM**.

- Only OK, WAIT, DONE or INFO: nothing to do. Go to step 4.
- **PROBLEM ... NOT running**: go to "Runs stopped" below.
- **PROBLEM ... unreadable output** or **... error log has an error**: do **not** run anything. Copy the PROBLEM line
  (and, for an error log, its last 20 lines) into `WORKLOG.md`. Stop.

**Runs stopped** (usually after the PC slept, shut down or restarted):
```
python tools/acl_resume.py
```
It prints STARTED, OK, DONE or STOP. If it says STOP, write the line in `WORKLOG.md` and stop. Otherwise run step 1
again: the stopped run should now say OK.

**Step 3: when a run says DONE** (only then; never before):

| run | command (writes `results.md` in its folder) |
|---|---|
| LK1 | `python experiments/LK1_location_knowledge/analyse_lk1.py` |
| SA1 | `python experiments/SA1_sensitivity/analyse_sa1.py` |

First run `$env:PYTHONIOENCODING = "utf-8"` in the same PowerShell window: without it the script writes `results.md`
and then stops with a `UnicodeEncodeError` while printing (seen with LK1, 13 October 2026). That error is harmless,
but write it in `WORKLOG.md` if it appears.

Do not change the scripts. Do not open or summarise `results.md` for the creator as if it were a finding. Claude reads
it against the frozen plan first: a run can be **not valid**, and then nothing in it counts.

**Step 4: write in `WORKLOG.md`.** One line per action, at the bottom:
```
2026-10-13 09:10  status: LK1 512 of 768 OK, SA1 WAIT.  did: nothing.
2026-10-13 14:02  status: LK1 PROBLEM not running.  did: acl_resume.py -> STARTED LK1; status again -> OK.
```

## Keep the PC awake

Runs stop whenever the PC sleeps. Keep it plugged in with the lid open (or set "closing the lid" to *Do nothing* when
plugged in, in Control Panel → Power Options). Do not run a large Ollama model while experiments run: this PC has 7.6 GB
of memory, and the runs need most of it. Close Ollama when you are done asking it things.

## Other read-only tools (safe to run any time)

- `python tools/project_status.py`: the whole project in about 30 lines (runs, work log, commits, drafts, open decisions).
- `python tools/council.py "question in words"`: asks several models for **ideas**; answers go to `drafts/council/`.
  Ideas only. Describe ACL in words, never paste code (the tool refuses code or file paths).
- `python tools/ask_local.py FILE "question"`: the local model answers with quoted lines; only lines marked VERIFIED
  are real.

## Things the helper can usefully help with (drafts only, in `drafts/`)

These never touch the record. Claude reviews them before anything is used.

- **The Creator's Note** (the book's missing Chapter 0, in the creator's own voice). The helper can ask the creator
  questions and write the creator's answers into `drafts/creators_note.md`. The words must be the creator's.
- **Questions for Claude.** Anything the creator wants to ask or decide next, collected in `drafts/questions_for_claude.md`.

## What is running now (12 October 2026, 23:36)

- **LK1** (location knowledge): 768 worlds, about 11 hours left (around 10–11 a.m. on 13 October if the PC stays awake).
- **SA1** (sensitivity audit): starts by itself when LK1 is done; 896 worlds, about 12 hours.
- Both are frozen. Their analysis scripts were written before any data. Nothing about them may change.

## For Claude, on return

1. Read `WORKLOG.md`.
2. Run `python tools/acl_status.py`.
3. Check any `results.md` against its frozen plan (validity first).
4. Review `drafts/`.
