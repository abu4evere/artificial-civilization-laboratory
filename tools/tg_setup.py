"""One-time Telegram setup, run by the creator in their own terminal (never by the assistant).

  python tools/tg_setup.py

1. Asks for the bot token from @BotFather (typed in, not shown on screen) and saves it to
   %USERPROFILE%\\.acl\\telegram.json, a file outside the repository, readable only by your Windows account.
2. Asks you to send /start to your bot from your phone, then finds that message and saves your chat id and user id
   in the same file. Only that account will ever be messaged (and, in Phase 2, obeyed).
3. Sends a test message.

Nothing is printed except "saved" and your Telegram first name, so you can see it picked the right account.
Run it again at any time to replace the token or the account.
"""
from __future__ import annotations

import getpass
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notify  # noqa: E402

CONFIG = notify.CONFIG


def api(token: str, method: str, **params) -> dict:
    q = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"https://api.telegram.org/bot{token}/{method}" + (f"?{q}" if q else "")
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())


def save(cfg: dict) -> None:
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(cfg), encoding="utf-8")
    user = os.environ.get("USERNAME", "")
    if user:      # only your Windows account may read the file
        subprocess.run(["icacls", str(CONFIG), "/inheritance:r", "/grant:r", f"{user}:F"],
                       capture_output=True, text=True)


def main() -> None:
    print("ACL Telegram setup. The token is typed in hidden and saved only on this PC.")
    raw = getpass.getpass("Bot token from @BotFather (hidden): ")
    # A pasted token can arrive wrapped in invisible terminal characters (bracketed paste); keep only the token itself.
    m = re.search(r"\d{5,}:[A-Za-z0-9_-]{30,}", raw)
    if not m:
        sys.exit("That did not look like a bot token (digits, a colon, then letters). Run again and paste it once, "
                 "with right-click or Ctrl+V, then press Enter.")
    token = m.group(0)
    try:
        me = api(token, "getMe")
    except Exception as e:
        sys.exit(f"Telegram did not accept the token ({type(e).__name__}). Check it and run again.")
    if not me.get("ok"):
        sys.exit("Telegram did not accept the token. Check it and run again.")
    print(f"Bot found: @{me['result'].get('username')}")
    print("Now open Telegram on your phone, find that bot, and send it:  /start")
    print("Waiting up to 3 minutes...")
    deadline, chosen = time.time() + 180, None
    while time.time() < deadline and chosen is None:
        upd = api(token, "getUpdates", timeout=20)
        for u in upd.get("result", []):
            m = u.get("message") or {}
            chat, frm = m.get("chat") or {}, m.get("from") or {}
            if chat.get("type") == "private" and (m.get("text") or "").strip().startswith("/start") \
                    and not m.get("forward_origin") and not frm.get("is_bot"):
                chosen = (chat["id"], frm["id"], frm.get("first_name", ""))
        if chosen is None:
            time.sleep(2)
    if chosen is None:
        sys.exit("No /start message arrived. Run the setup again and send /start to the bot.")
    save({"token": token, "chat_id": chosen[0], "user_id": chosen[1]})
    print(f"Saved. Authorized account: {chosen[2]}")
    ok = notify.send("ACL Researcher: setup complete. You will get research updates here.", "test")
    print("Test message sent." if ok else "The test message could not be sent; see research/local/notify.log.")


if __name__ == "__main__":
    main()
