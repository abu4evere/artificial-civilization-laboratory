"""Send a short message to the creator's phone through Telegram (outbound only). Phase 1 of
docs/proposal_autonomous_researcher_2026-10-30.md.

  python tools/notify.py "ACL Researcher: AW1 finished. Results saved."
  python tools/notify.py --kind problem "ACL Researcher: a run stopped with an error."
  python tools/notify.py --test

The bot token and the creator's chat id are read only from this machine, never from the repository:
  1. environment variables ACL_TG_TOKEN and ACL_TG_CHAT, or
  2. the file %USERPROFILE%\\.acl\\telegram.json  {"token": "...", "chat_id": 123, "user_id": 123}
They are never printed. If Telegram is not set up, the message is written to research/local/outbox.log instead,
so nothing is lost and nothing fails.

Limits: messages are cut to 1,000 characters; at most 12 non-problem messages a day (problems always go).
Every attempt is logged in research/local/notify.log (time, kind, sent or not; never the token or the chat id).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "research" / "local"
CONFIG = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".acl" / "telegram.json"
MAX_CHARS = 1000
DAILY_LIMIT = 12
KINDS = ("info", "started", "finished", "problem", "approval", "summary", "test", "reply")
REPLY_MAX = 3800        # answers to the creator's own Telegram messages: longer, and not counted in the daily limit


def credentials():
    token, chat = os.environ.get("ACL_TG_TOKEN"), os.environ.get("ACL_TG_CHAT")
    if (not token or not chat) and CONFIG.exists():
        try:
            c = json.loads(CONFIG.read_text(encoding="utf-8"))
            token, chat = token or c.get("token"), chat or c.get("chat_id")
        except (OSError, ValueError):
            pass
    return token, chat


def _log(line: str) -> None:
    LOCAL.mkdir(parents=True, exist_ok=True)
    with (LOCAL / "notify.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def sent_today() -> int:
    log = LOCAL / "notify.log"
    if not log.exists():
        return 0
    day = datetime.now().strftime("%Y-%m-%d")
    return sum(1 for ln in log.read_text(encoding="utf-8").splitlines()
               if ln.startswith(day) and ln.endswith(" sent") and " problem " not in ln and " reply " not in ln)


def send(text: str, kind: str = "info") -> bool:
    """Returns True if Telegram accepted the message."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = text.strip().replace("\r", "")[:REPLY_MAX if kind == "reply" else MAX_CHARS]
    if kind not in ("problem", "reply") and sent_today() >= DAILY_LIMIT:
        _log(f"{now} {kind} held (daily limit {DAILY_LIMIT})")
        _outbox(now, kind, text)
        return False
    token, chat = credentials()
    if not token or not chat:
        _log(f"{now} {kind} not-configured")
        _outbox(now, kind, text)
        return False
    data = urllib.parse.urlencode({"chat_id": chat, "text": text, "disable_web_page_preview": "true"}).encode()
    try:
        with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=20) as r:
            ok = json.loads(r.read().decode()).get("ok") is True
    except Exception as e:                       # never let the token reach a log through an error message
        _log(f"{now} {kind} failed ({type(e).__name__})")
        _outbox(now, kind, text)
        return False
    _log(f"{now} {kind} {'sent' if ok else 'refused'}")
    if not ok:
        _outbox(now, kind, text)
    return ok


def _outbox(now: str, kind: str, text: str) -> None:
    LOCAL.mkdir(parents=True, exist_ok=True)
    with (LOCAL / "outbox.log").open("a", encoding="utf-8") as f:
        f.write(f"{now} [{kind}] {text}\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.exit(__doc__)
    kind = "info"
    if "--kind" in args:
        i = args.index("--kind")
        kind = args[i + 1]
        del args[i:i + 2]
    if kind not in KINDS:
        sys.exit(f"kind must be one of {KINDS}")
    if args == ["--test"]:
        ok = send("ACL Researcher: test message. If you can read this on your phone, notifications work.", "test")
    elif args:
        ok = send(" ".join(args), kind)
    else:
        sys.exit(__doc__)
    print("sent" if ok else "not sent (see research/local/notify.log; the text is in research/local/outbox.log)")
