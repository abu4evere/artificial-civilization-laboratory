# research/ — the state that scheduled research ticks read and write

Phase 1 of `docs/proposal_autonomous_researcher_2026-10-30.md`, approved by the creator on 30 October 2026 ("yes
remove it and build phase 1").

| file | what | committed |
|---|---|---|
| `state.json` | what is running, what comes next, what waits for the creator, budgets | yes |
| `RECOVERY.md` | what to do after a crash, restart or long pause | yes |
| `tick_prompt.md` | the instructions every scheduled tick starts from | yes |
| `STOP` / `PAUSE` | if present, no tick starts any work (create the file to stop; delete it to resume) | no |
| `local/` | logs, lock, budget counters, Telegram outbox, tick transcripts | **no** (`.gitignore`) |

## Labels that must not blur
- **verified**: findings final, and the blind recompute by GPT and Gemini matched.
- **finding**: analysed by the frozen script, not yet recomputed.
- **exploratory** against **confirmatory**: a positive exploratory result can only lead to a confirmatory run, never
  straight to adoption.
- **proposed** against **approved**: only the creator approves, by a message naming the exact plan or version.
- **tested in a copy** (`code_X`) against **law in nature** (`acl/`): nature changes only by the creator's decision.

## Study status values
`drafted` → `frozen` → `zero-checks` → `running-cloud` / `running-local` → `analysed` → `findings` →
`recompute-pending` → `final` (or `not-valid`, with the reason). A step reads the status first and does nothing if its
work is already done.

## Telegram setup (the creator, once; about 5 minutes)
1. In Telegram, open **@BotFather**, send `/newbot`, choose a name and a username ending in `bot`. BotFather replies
   with a token. **Do not paste it into any chat** (including this one).
2. On this PC, open PowerShell in `D:\acl` and run: `python tools\tg_setup.py`. Type or paste the token when asked (it
   stays hidden), then send `/start` to your new bot from your phone. The script saves the token and your account
   in `%USERPROFILE%\.acl\telegram.json` (outside the repository; only your Windows account can read it) and sends a
   test message.
3. Check any time: `python tools\notify.py --test`.

## Switching the scheduled ticks on and off
- On: `powershell -ExecutionPolicy Bypass -File tools\install_research_task.ps1 -Enable` (every hour at :07; a tick
  does nothing while an interactive session has been active in the last 90 minutes).
- Off, at once: `powershell -ExecutionPolicy Bypass -File tools\stop_research.ps1` (writes `research\STOP`, disables
  the task, lists cloud runs). Or create an empty file `research\STOP`.
- Pause new work but keep daily summaries: create `research\PAUSE`.
- One manual tick: `powershell -ExecutionPolicy Bypass -File tools\research_tick.ps1 -Reason "demonstration: read-only status"`.

## Talking to the PC from Telegram (Phase 2, the creator's choice, 30 October 2026)
- Write to the bot in plain words, as in the desktop chat. `tools/tg_listener.py` (task "ACL Telegram listener",
  started at logon, checked every 10 minutes) answers each message with a fresh Claude Code session
  (`research/telegram_prompt.md`). It obeys **only** the account saved by `tg_setup.py`; everyone else, groups and
  forwarded messages are ignored without a reply.
- Hard-to-undo actions come back with a 4-digit code; nothing happens until you reply with it (checked by the listener).
- Never through Telegram: nature changes or adoption, passwords or tokens, payments, deleting, Windows or security
  settings, untrusted software, publishing.
- Logs on this PC only: `research/local/telegram_audit.jsonl`, `research/local/tg/`.
- Stop: `tools\stop_research.ps1` (also stops the listener), or create `research\local\TG_OFF`.
