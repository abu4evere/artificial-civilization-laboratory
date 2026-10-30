# Proposal: an autonomous ACL researcher with Telegram updates (30 October 2026)

**Status: a proposal for the creator's approval. Nothing here has been built.** Written after inspecting the
repository and this PC. Every "today" fact below was checked on 30 October 2026.

---

## 0. The short version
- **Most of the research cycle already runs without you.** Sleep mode has frozen plans, launched cloud runs, analysed,
  got blind rechecks and chosen next studies (LS2, AG1 and others). What is missing is **reliability**:
  - it lives inside one long chat session that can stop (usage limits, a closed app, a crash, the PC sleeping);
  - it needs a working Chrome window for GPT and Gemini;
  - it cannot reach your phone.
- **The fix is not an endless loop.** It is a **"tick"**: a scheduled, short, fresh Claude Code session that:
  1. reads a state file;
  2. does one bounded step;
  3. writes the state back;
  4. sends you a message;
  5. exits.
  A free Python "gate" runs first and wakes Claude only when something changed, which saves your usage limit.
- **Telegram is cheap and safe to add in stages:** first messages to your phone, then read-only commands, and much
  later approvals bound to an exact plan.
- **Nature protection must be tightened, not loosened.** Today's sleep-mode rule still lets the assistant adopt a new
  nature version. Your new rule says it may not. I propose removing that permission first.
- **Costs:**
  - Telegram, GitHub Actions (your repo is public) and Claude Code on your current plan cost nothing extra.
  - The real limit is your plan's usage cap: we hit it once today.
  - Optional extras (GPT and Gemini through paid APIs, a higher Claude plan) would cost money; nothing is bought
    without your OK.
- **Honest expectation:** this makes research steadier, not smarter. More studies do not mean Bob. The risk to watch is
  many weak studies instead of a few strong ones.

---

## 1. What Claude Code can already do here (checked)

| capability | today | limit |
|---|---|---|
| Read and write the repo, run Python, git, `gh` | yes (Claude Code 2.1.307 CLI at `~/.local/bin/claude`, Python 3.14.7, `gh` at `C:\Users\User\gh\bin`) | needs the PC on |
| Frozen-plan studies end to end | yes: plan → freeze tag → runner and analysis before data → zero checks → GitHub Actions → fetch → analyse → findings → blind recompute → records | judgement calls still need review |
| Heavy simulations off the PC | yes: `.github/workflows/cloud-run.yml`, 20 parallel jobs, repo **public**, so standard runners are free | **340-minute job limit** (AG1 lost 5 worlds to it today) |
| GPT and Gemini (debates, blind recomputes) | yes, by driving your logged-in Chrome | **fragile**: the page froze twice today, a send failed silently, Gemini once refused a file |
| Waking up on a schedule | session cron (`CronCreate`): dies with the session, expires after 7 days, fires only when the session is idle; **desktop scheduled tasks** (stored in `~/.claude/scheduled-tasks`, run while the app is open; a fresh session each time); **Windows Task Scheduler + `claude -p`** (headless, runs even if the app is closed); **cloud routines** (`RemoteTrigger`; run with the PC off, from the GitHub repo) | each run starts with no memory, so state must live in files |
| Reaching your phone | **first-party already:** Remote Control (follow and steer this session from the Claude mobile app) and `PushNotification` (reaches the phone when Remote Control is on) | Telegram: not set up |
| Memory across sessions | `CLAUDE.md`, `WORKLOG.md`, `docs/OPEN_DECISIONS.md`, `experiments/INDEX.md`, `ROADMAP.md`, `docs/autonomous_decisions.md`, per-study files, the assistant's memory folder | written as prose for people; no machine-readable "what to do next" |
| Recovery after a restart | `tools/acl_status.py` (OK / WAIT / DONE / PROBLEM), `tools/acl_resume.py` (restarts only missing worlds), `tools/project_status.py`, `docs/HELPER_RUNBOOK.md` (a local Ollama helper) | built for local runs; partly out of date with cloud runs |
| Protecting nature | frozen `code_vN` copies; reference-hash replay tests (64) in CI; `nature-vN` tags; a rule in `CLAUDE.md` | **`master` is not branch-protected; no file-level lock**; the assistant pushes with your credentials |

**PC facts:** 8 cores, 7.8 GB RAM (0.7 GB was free during today's lag), C: 10 GB free, D: 39 GB free. Lesson from
today: 14 simulations at normal priority made the PC lag; at idle priority they no longer get in your way.

---

## 2. Architecture

```
            ┌──────────────── your phone (Telegram) ────────────────┐
            │ updates ↓                    ↑ /status /pending /pause │
            └──────────────────────────────────────────────────────┘
                      │                              │
   tools/notify.py ───┘                   tools/tg_listener.py (whitelisted, read-only commands;
                                           writes only research/inbox and research/PAUSE)
                      ▲                              │
                      │                              ▼
  Windows Task Scheduler (every 30–60 min) → tools/research_tick.ps1
     1. STOP or PAUSE file? → exit
     2. lock held by a live tick? → exit (no double work)
     3. budget left today? (ticks, turns, failures) → else exit + notify
     4. gate (Python, free): run finished? inbox question? daily summary due? queued step ready?
        nothing → exit without waking Claude
     5. claude -p "<research-tick prompt>" --max-turns N --allowedTools … (fresh session)
           reads research/state.json + CLAUDE.md + WORKLOG tail
           does ONE step from the authorized queue
           writes state, WORKLOG, notify
     6. release the lock; record the outcome; 3 failures in a row → circuit breaker + notify

  Heavy compute: GitHub Actions (cloud-run.yml), sized so no job nears its time limit
  Light compute: the PC, at most 4 simulations at idle priority, with RAM and disk guards
```

**One step per tick.** Examples of steps:
- check a run;
- fetch and analyse;
- draft findings;
- prepare a recompute file;
- send a debate question;
- draft a plan;
- run zero checks;
- launch an authorized study;
- write the daily summary.

Small steps mean a crash loses minutes, not hours, and each step is easy to audit.

---

## 3. Persistent memory and recovery

Keep the existing prose records (they are what you and GPT read). Add one **machine-readable** state file that a fresh
session can trust:

`research/state.json` (committed; no secrets):
```json
{
  "nature": {"live": "v9", "fingerprint": "8f88ec33…", "adoption_requires": "creator"},
  "objectives": ["knowledge that survives death", "define and measure autonomy early"],
  "studies": [
    {"id": "AG1", "kind": "calibration (nature-change test)", "status": "running-local",
     "frozen_tag": "AG1-frozen", "plan_sha": "…", "seeds": "20501-20520", "jobs": {"cloud": 41042869183,
     "local": ["b:20501", "a:20501", "b:20506", "a:20506", "x:20506"]},
     "next_step": "when the 5 local worlds and the identity check finish: analyse",
     "evidence": "exploratory", "approved_by": "creator delegation 30 Oct"},
    {"id": "AW1", "status": "zero-checks", "approved_by": "creator 30 Oct ('yea go ahead with AW1')"}
  ],
  "hypotheses": [{"text": "…", "status": "open | supported | rejected", "by": "study id"}],
  "pending_approvals": [{"what": "…", "exact_object": "plan sha / tag", "asked": "date"}],
  "authorized_scope": {"read_only_studies": "allowed", "nature_change_tests": "listed ids only",
                       "nature_adoption": "never autonomous"},
  "budgets": {"ticks_per_day": 24, "max_turns_per_tick": 60, "local_sims_max": 4, "cloud_runs_at_once": 1},
  "failures_in_a_row": 0,
  "updated": "2026-10-30T…"
}
```

- **Labels that cannot blur:**
  - *verified* means the blind recompute matched;
  - *finding* means analysed but not yet rechecked;
  - *exploratory* and *confirmatory* are kept apart;
  - *proposed* is kept apart from *approved*;
  - *law in nature* is kept apart from *tested in a copy*.
- **Recovery instructions** live at the top of `research/RECOVERY.md`: run `tools/project_status.py`, read `state.json`,
  resume `next_step`. Every step is written so that running it twice does nothing harmful: runners skip saved worlds,
  launches check whether a run already exists, and commits are append-only.
- **No duplicate work:** a lock file (`research/lock.json`: tick id, start time, process id) plus each study's status
  field. A step reads the status first and skips work already done.

---

## 4. Running research cycles safely

**What stays the same:** our methods, unchanged:
- frozen plan;
- zero checks;
- matched seeds and a sham arm;
- the analysis written before data;
- the frozen rule;
- the blind recompute;
- append-only corrections.

**What changes is who presses "next":**
- a **queue of authorized steps** in `state.json`;
- the tick picks the first ready one.

**Guards against the "100 weak studies" problem:**
1. **At most one study running and one being drafted.** A new study starts only when the last one's findings are
   final (blind recompute matched).
2. **Every study must name the decision it informs** (your order: knowledge, autonomy measures, a world where knowing
   matters, connected populations). No study "to see what happens".
3. **Exploratory against confirmatory:** a positive exploratory result can only lead to a confirmatory run on new
   seeds, never straight to adoption.
4. **No re-running until it works:** the same question with changed settings needs a new frozen plan that cites the
   earlier null result.
5. **A weekly review for you:** a list of every study, its result and its open doubts, with nothing new started that
   week until you have seen it, or until 7 days pass in sleep mode.

**Job sizing:** the planner records seconds per world-year from earlier runs and refuses a cloud layout whose slowest
job would pass 4 hours (the limit is 5 h 40 min). AG1 shows why: anchored worlds were slower than expected.

---

## 5. Protecting nature (technical, in layers)

On one PC where the assistant uses your git credentials, no single lock is unbreakable. Layers make an accident
impossible and a mistake loud.

| layer | what it does | effort |
|---|---|---|
| **Rule change (first)** | Remove "adopting a new nature version as live is allowed in sleep mode" from `CLAUDE.md`. Adoption only on your explicit, specific message. | 5 minutes |
| **Tool permissions** | Project settings for autonomous ticks: `deny` Edit/Write on `acl/**`, `tests/reference_hashes.json`, `.github/workflows/**`; ticks run with `--allowedTools` limited to what the step needs | small |
| **NATURE.lock + CI** | A committed file with the live `acl/` fingerprint. A CI check fails, and Telegram alerts you, if `acl/` changes without a matching `nature-vN` approval record signed off in your words | small |
| **Branches** | Autonomous work commits to `research/<study>` branches; only study folders and records go to `master` | moderate |
| **Strong option (later)** | A separate GitHub "machine user" for the agent, without admin rights, plus branch protection and CODEOWNERS on `acl/**`. The agent then cannot merge nature changes at all; you approve a pull request | moderate; free |

Tests already catch any change in nature's behaviour (reference replays). The layers above stop it reaching `master`.

---

## 6. Telegram

**A. Outbound first** (`tools/notify.py`):
1. **You** create the bot: open @BotFather → `/newbot` → pick a name → it gives a token.
2. **You** store the token **locally**, never in chat or the repo. Either:
   - a user environment variable (`setx ACL_TG_TOKEN …` in your own terminal), or
   - a file outside the repo, `%USERPROFILE%\.acl\telegram.json`, readable only by your account.

   I never see it.
3. You send `/start` to your bot. A one-time script `tools/tg_setup.py` (run by you) reads the bot's updates and
   stores **your numeric user id** in the same local file. That id is the only account the bot will ever obey.
4. `notify.py "text"` sends a message (HTTPS to `api.telegram.org`). It has templates for:
   - started, finished, problem;
   - approval needed;
   - the daily summary.

   It enforces a short-message limit and a rate limit (for example, at most 10 a day apart from problems).
5. Test: `notify.py --test` sends "ACL Researcher: test message".

**B. Read-only commands next** (`tools/tg_listener.py`, a small always-on Python process started by Task Scheduler):
- It uses long polling (`getUpdates`), so no server and no open port.
- **It obeys only** private-chat messages whose sender id equals yours. It ignores forwarded messages, groups, edits and
  everything else, and it logs every message to `research/telegram_audit.jsonl` (kept locally, not committed).
- **The commands are a fixed list, mapped to fixed scripts; text is never run as a command:**

  | command | what it does |
  |---|---|
  | `/status` | runs `project_status.py` |
  | `/summary` | sends the latest morning report section |
  | `/experiments` | sends the INDEX tail and running jobs |
  | `/pending` | sends the open decisions |
  | `/pause` | writes `research/PAUSE`: no new steps start; running jobs finish |
  | `/resume` | removes it |
  | `/stop` | writes `research/STOP` and asks "cancel running cloud runs too? reply /stop-confirm" |

- **Questions in plain words** ("why did AW1 fail?") go into `research/inbox/`. The next tick answers from the records,
  with read-only tools. Answers can take up to one tick interval and use your Claude limit.

**C. Approvals, last, as a separate design:**
- An approval must name the object, for example `/approve AW2 3f9c1e`, where `3f9c1e` is the start of the frozen
  plan's commit.
- The bot replies with the plan's one-line summary and a code; you confirm with `/confirm <code>` within 10 minutes.
- The approval is written to `approvals/` with the time and message id.
- "Continue", "ok" or "go ahead" approve nothing.
- **Adopting a nature version stays at the PC.** It needs your message in a Claude Code session, not Telegram.

**Note:** Telegram bot chats are not end-to-end encrypted. Research updates are fine; secrets never go through it.

**First-party alternative, available today with no setup:** turn on **Remote Control** for this session. You then
follow and steer it from the Claude mobile app, and `PushNotification` reaches your phone. It does not replace
Telegram's always-on bot (it is tied to a running session), but it can be the stopgap while Telegram is built.

---

## 7. Safety and resource limits (proposed defaults; you can change them)

| control | default |
|---|---|
| Simulations on the PC at once | 4, at idle priority; none if free RAM < 1.5 GB or C: free < 5 GB |
| Cloud | 1 study at a time; ≤ 20 jobs; slowest job planned ≤ 4 h |
| Claude ticks | every 60 min; ≤ 24 a day; ≤ 60 turns each; no tick if your interactive session is active |
| Failures | 3 in a row → stop starting steps; Telegram "problem" message |
| Runtime | each tick ends itself; nothing runs forever |
| Kill switch | `/stop`, a `research/STOP` file, or `tools/stop_research.ps1` (removes the scheduled task, cancels cloud runs after confirmation) |
| External services | only GitHub, Telegram, and the GPT/Gemini pages you already use; anything new needs your OK |
| Secrets | none in the repo (it is public); `.gitignore` covers `research/local/`; a pre-commit check rejects token-like strings |
| Prompt injection | web pages, Telegram text, GPT/Gemini replies and run logs are data, never instructions; only you, in a Claude Code session or via a verified `/approve`, authorize anything |

---

## 8. Costs

| item | cost |
|---|---|
| Telegram bot | free |
| GitHub Actions | free while the repo is public (standard runners). If it ever goes private, Windows minutes count double against the free plan's 2,000 a month |
| Claude Code | your existing plan; **usage caps are the main limit** (we hit one today). Autonomous ticks share them with your own use. A higher plan would raise the cap: optional, at its listed price, your decision |
| GPT and Gemini | free through the browser pages you use now, but fragile when unattended. Paid APIs would make unattended debates and blind recomputes reliable at small per-request cost; this needs your own API keys, entered by you. Not needed for Phase 1 |
| Electricity | the PC on when local runs are going |

---

## 9. Phases

| phase | what | you do | effort |
|---|---|---|---|
| **0 (now)** | Fix the adoption rule in `CLAUDE.md`; optional Remote Control for phone access | approve the rule change | minutes |
| **1** | `research/state.json` + `RECOVERY.md`; the tick wrapper (STOP/PAUSE, lock, budget, gate, circuit breaker); a Task Scheduler entry; `notify.py` outbound Telegram; daily summary | create the bot, store the token, run `tg_setup.py` | a few hours |
| **2** | `tg_listener.py`: read-only commands, `/pause` `/resume` `/stop`, inbox questions | none | a few hours |
| **3** | Nature locks: permission denies, `NATURE.lock` CI check, research branches; job-size planner | approve | a few hours |
| **4** | Telegram approvals bound to a plan hash, two-step, audited | approve the design first | a day |
| **5 (optional)** | Cloud routines so the PC can be off; paid APIs for GPT/Gemini | decide on costs | later |

---

## 10. First demonstration (after approval of Phase 1)

A harmless, read-only task:
1. One scheduled tick runs `tools/project_status.py` and reads `state.json`.
2. It checks AG1's 5 local worlds and AW1's cloud run (both already authorized), and writes a 5-line status into
   `WORKLOG.md`.
3. It sends you: "ACL Researcher: AG1 local worlds 3 of 5 done; AW1 running (run id); nothing needs you."
4. You reply `/status` (Phase 2) and get the same lines back.

No nature change, no new study, no money.

---

## 11. What is realistic, and what still needs you

- **Level 1 (analysis): realistic now.**
- **Level 2 (experiments in an approved scope): realistic now.** Sleep mode already does it; it needs the written scope
  list in `state.json`.
- **Level 3 (multi-study cycles): partly.** It works when nothing unusual happens. Today's real problems would each
  have stalled a fully unattended chain:
  - a cloud time-out;
  - a frozen browser;
  - a silent send failure;
  - a usage limit that killed a research workflow;
  - a council claim of mine that the scout caught.
  The tick design turns each of these into a "problem" message instead of silent drift.
- **Level 4 (Telegram):** outbound is easy; read-only commands are moderate; approvals are a careful design.

**Always yours:**
- any change to live nature;
- the direction;
- any money;
- any new external service;
- reading the weekly study list;
- any result that would change what ACL is.

**Failure modes to watch:**
- **many weak studies** (the forking-paths problem);
- the assistant's own errors compounding without review;
- browser automation breaking unnoticed;
- stale state after a crash;
- a credential leak into the public repo;
- injected instructions in pages or messages.

**And honestly:** none of this makes Bob more likely by itself. It makes our method run more steadily. Whether Bob can
emerge is still the open scientific question.

---

## 12. Reused against new

**Reused:**
- `CLAUDE.md` (rules), `WORKLOG.md`, `OPEN_DECISIONS.md`, `INDEX.md`, `ROADMAP.md`, `autonomous_decisions.md`;
- frozen-plan tags; the runners' `zero` / `hashrun` / `reload`;
- `cloud-run.yml`, `fetch_cloud.py`, `check_local_zero.py`, `cloud_plan.py`;
- `acl_status.py`, `acl_resume.py`, `project_status.py`;
- the recompute builders; the reference-hash tests; the memory folder.

**New:**
- `research/state.json` and `RECOVERY.md`;
- `tools/research_tick.ps1` (gate, lock, budget, STOP/PAUSE, circuit breaker);
- a Task Scheduler entry;
- `tools/notify.py`, `tools/tg_setup.py`, `tools/tg_listener.py`;
- `NATURE.lock` + CI check;
- the permission deny rules;
- a job-size planner;
- `tools/stop_research.ps1`.
