"""The ACL Telegram listener (Phase 2 of docs/proposal_autonomous_researcher_2026-10-30.md; the creator chose it on
30 October 2026 and lifted the safety check for it by approving it in Ask mode).

The creator writes to the bot in plain words, as in the desktop chat; each message is answered by a fresh Claude Code
session on this PC (research/telegram_prompt.md), and the answer is sent back to Telegram.

  python tools/tg_listener.py        # runs until stopped; Task Scheduler ("ACL Telegram listener") keeps it alive

Who is obeyed: only private messages from the one account saved by tools/tg_setup.py (the user id in
%USERPROFILE%\\.acl\\telegram.json). Everyone else, groups, channels, forwarded and edited messages are ignored without
a reply and noted in research/local/telegram_audit.jsonl (local, never committed).

Text is never run as a command. The session decides what to do under CLAUDE.md and its prompt; actions that are hard
to undo come back as "CONFIRM: ..." and run only after the creator replies with the 4-digit code sent to them
(checked here, by the listener, not by the model). One session at a time; a running research tick finishes first.
Stop: tools/stop_research.ps1 (also stops this listener), or create research/local/TG_OFF.
"""
from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "research" / "local"
sys.path.insert(0, str(ROOT / "tools"))
import notify  # noqa: E402

CLAUDE = r"C:\Users\User\.local\bin\claude.exe"
SESSION_TIMEOUT = 25 * 60          # seconds for one answer
CONFIRM_MINUTES = 30
HISTORY_KEEP = 12
BELOW_NORMAL = 0x00004000
ALLOWED = ["Read", "Glob", "Grep", "Edit", "Write", "Bash", "PowerShell", "WebSearch", "WebFetch",
           "mcp__claude-in-chrome", "mcp__plugin_desktop-commander_desktop-commander"]
DENIED = ["Edit(acl/**)", "Edit(tests/reference_hashes.json)", "Read(~/.acl/**)", "Edit(~/.acl/**)",
          "Bash(git push --force*)", "Bash(git reset --hard*)", "Bash(rm -rf*)", "Bash(rm -r *)",
          "PowerShell(Remove-Item*)", "PowerShell(Format-*)", "PowerShell(Set-ExecutionPolicy*)"]


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def api(token: str, method: str, http_timeout: int = 60, **params) -> dict:
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/{method}", data=data,
                                timeout=http_timeout) as r:
        return json.loads(r.read().decode())


def audit(**entry) -> None:
    LOCAL.mkdir(parents=True, exist_ok=True)
    with (LOCAL / "telegram_audit.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now(), **entry}, ensure_ascii=False) + "\n")


def history() -> list:
    p = LOCAL / "tg_history.jsonl"
    if not p.exists():
        return []
    rows = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    return rows[-HISTORY_KEEP:]


def remember(you: str, me: str) -> None:
    with (LOCAL / "tg_history.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now(), "you": you, "me": me[:1500]}, ensure_ascii=False) + "\n")


def pid_alive(pid: int) -> bool:
    r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
    return str(pid) in r.stdout


def single_instance() -> bool:
    lock = LOCAL / "tg_listener.lock"
    if lock.exists():
        try:
            if pid_alive(int(lock.read_text().strip())):
                return False
        except (ValueError, OSError):
            pass
    lock.write_text(str(os.getpid()))
    return True


def wait_for_tick(max_wait: int = 15 * 60) -> None:
    """A scheduled research tick holds research/local/lock.json; let it finish first (at most 15 minutes)."""
    lock, start = LOCAL / "lock.json", time.time()
    while lock.exists() and time.time() - start < max_wait:
        try:
            if not pid_alive(int(json.loads(lock.read_text(encoding="utf-8-sig"))["pid"])):
                return
        except (ValueError, KeyError, OSError):
            return
        time.sleep(20)


def run_session(message: str, confirmed: str | None) -> str:
    hist = "\n".join(f"[{h['t']}] Creator: {h['you']}\n[{h['t']}] You: {h['me']}" for h in history()) or "(none)"
    prompt = (ROOT / "research" / "telegram_prompt.md").read_text(encoding="utf-8")
    prompt += (f"\n\n--- Recent Telegram conversation ---\n{hist}\n\n"
               f"--- The creator's new message ({now()}) ---\n{message}\n")
    if confirmed:
        prompt += f"\nCONFIRMED by code (verified by the listener): {confirmed}\n"
    args = [CLAUDE, "-p", "--permission-mode", "dontAsk", "--output-format", "text", "--chrome",
            "--allowedTools", *ALLOWED, "--disallowedTools", *DENIED]
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    (LOCAL / "tg").mkdir(parents=True, exist_ok=True)
    (LOCAL / "tg" / f"{stamp}.prompt.md").write_text(prompt, encoding="utf-8")
    try:
        r = subprocess.run(args, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=SESSION_TIMEOUT, cwd=str(ROOT), creationflags=BELOW_NORMAL)
        out, err = r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        out, err = "", "timeout"
    (LOCAL / "tg" / f"{stamp}.out.txt").write_text(out + "\n\n--- stderr ---\n" + err, encoding="utf-8")
    if not out:
        return ("Sorry, that one did not finish (it took too long or failed). Nothing was deleted; the log is "
                f"research\\local\\tg\\{stamp}.out.txt on the PC.")
    return out


def handle(msg: dict) -> None:
    text = (msg.get("text") or "").strip()
    if not text:
        notify.send("I can read text messages only, for now.", "reply")
        audit(kind="non-text", action="replied")
        return
    pend_file = LOCAL / "tg_pending.json"
    confirmed, request = None, text
    if pend_file.exists():
        pend = json.loads(pend_file.read_text(encoding="utf-8"))
        fresh = datetime.now() < datetime.fromisoformat(pend["expires"])
        if fresh and re.search(rf"\b{pend['code']}\b", text):
            confirmed, request = pend["action"], pend["request"]
            audit(kind="confirmation", action=pend["action"])
        if confirmed or not fresh:
            pend_file.unlink()
    notify.send("Got it, working on it.", "reply")
    wait_for_tick()
    lock = LOCAL / "lock.json"
    lock.write_text(json.dumps({"pid": os.getpid(), "started": now(), "by": "telegram"}), encoding="utf-8")
    try:
        answer = run_session(request, confirmed)
    finally:
        lock.unlink(missing_ok=True)
    m = re.search(r"^CONFIRM:\s*(.+)$", answer, re.MULTILINE)
    if m and not confirmed:
        code = f"{secrets.randbelow(9000) + 1000}"
        expires = (datetime.now() + timedelta(minutes=CONFIRM_MINUTES)).isoformat(timespec="seconds")
        pend_file.write_text(json.dumps({"code": code, "action": m.group(1).strip(), "request": text,
                                         "expires": expires}), encoding="utf-8")
        answer = answer[:m.start()].rstrip() + (f"\n\nTo go ahead, reply with code {code} (valid {CONFIRM_MINUTES} "
                                                f"minutes): {m.group(1).strip()}")
        audit(kind="confirm-asked", action=m.group(1).strip())
    notify.send(answer, "reply")
    remember(text, answer)
    audit(kind="answered", chars=len(answer), confirmed=bool(confirmed))


def main() -> None:
    LOCAL.mkdir(parents=True, exist_ok=True)
    if not single_instance():
        return
    cfg = json.loads(notify.CONFIG.read_text(encoding="utf-8"))
    token, user = cfg["token"], int(cfg["user_id"])
    off_file = LOCAL / "tg_offset.txt"
    offset = int(off_file.read_text()) if off_file.exists() else 0
    audit(kind="listener-start")
    while not (LOCAL / "TG_OFF").exists():
        try:
            upd = api(token, "getUpdates", http_timeout=70, offset=offset, timeout=50)
        except Exception as e:                     # network hiccups, or a replaced token: wait, re-read, poll again
            audit(kind="poll-error", error=type(e).__name__)
            time.sleep(15)
            try:                                   # tg_setup.py may have saved a new token or account
                cfg = json.loads(notify.CONFIG.read_text(encoding="utf-8"))
                token, user = cfg["token"], int(cfg["user_id"])
            except (OSError, ValueError, KeyError):
                pass
            continue
        for u in upd.get("result", []):
            offset = u["update_id"] + 1
            off_file.write_text(str(offset))
            msg = u.get("message")
            if not msg:
                audit(kind="ignored", why="not a new message")
                continue
            frm, chat = msg.get("from") or {}, msg.get("chat") or {}
            forwarded = any(k in msg for k in ("forward_origin", "forward_from", "forward_date",
                                               "forward_sender_name"))
            if frm.get("id") != user or chat.get("type") != "private" or frm.get("is_bot") or forwarded:
                audit(kind="ignored", why="not the creator, not private, a bot, or forwarded")
                continue
            try:
                handle(msg)
            except Exception as e:
                audit(kind="handle-error", error=type(e).__name__)
                notify.send("Something went wrong on the PC while answering; the error is logged. Try again.",
                            "reply")
    audit(kind="listener-stop", why="TG_OFF present")


if __name__ == "__main__":
    main()
