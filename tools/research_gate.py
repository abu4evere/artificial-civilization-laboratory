"""The free gate before a scheduled research tick (Phase 1). Decides whether Claude needs waking; costs no usage.

  python tools/research_gate.py            # prints JSON: {"wake": true/false, "reasons": [...]}

Reads research/state.json and checks, in order:
  STOP file → never wake; PAUSE file → wake only for the daily summary;
  an interactive session active in the last 90 minutes (research/local/interactive.txt) → don't wake;
  today's tick budget used up → don't wake;
  the live nature fingerprint differs from state.json → send a problem message, write PAUSE, don't wake;
  a cloud run listed as running has completed → wake;
  all local worlds listed for a study exist → wake;
  the daily summary is due and not yet sent today → wake.
Changes nothing except the PAUSE file and a problem message in the nature check.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "research"
LOCAL = RES / "local"
GH = r"C:\Users\User\gh\bin\gh.exe"
REPO = "abu4evere/artificial-civilization-laboratory"
sys.path.insert(0, str(ROOT / "tools"))


def out(wake: bool, reasons: list) -> None:
    print(json.dumps({"wake": wake, "reasons": reasons}))
    sys.exit(0)


def live_fingerprint() -> str:
    sys.path.insert(0, str(ROOT / "experiments" / "E7_passive"))
    from run_e7 import code_hash
    return code_hash(ROOT / "acl")


def cloud_status(run: int) -> str:
    try:
        r = subprocess.run([GH, "run", "view", str(run), "-R", REPO, "--json", "status", "--jq", ".status"],
                           capture_output=True, text=True, timeout=60)
        return r.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def main() -> None:
    state = json.loads((RES / "state.json").read_text(encoding="utf-8"))
    budgets = state.get("budgets", {})
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    if (RES / "STOP").exists():
        out(False, ["STOP file present"])

    summary_due = False
    at = budgets.get("daily_summary_at", "07:30")
    hh, mm = map(int, at.split(":"))
    sent = LOCAL / "summary_sent.txt"
    if now >= now.replace(hour=hh, minute=mm, second=0, microsecond=0) and \
            (not sent.exists() or sent.read_text(encoding="utf-8").strip() != today):
        summary_due = True

    if (RES / "PAUSE").exists():
        out(summary_due, ["PAUSE file present"] + (["daily summary due"] if summary_due else []))

    beat = LOCAL / "interactive.txt"
    if beat.exists():
        try:
            last = datetime.fromisoformat(beat.read_text(encoding="utf-8").strip())
            if now - last < timedelta(minutes=90):
                out(False, [f"an interactive session was active at {last:%H:%M}"])
        except ValueError:
            pass

    bud = LOCAL / "budget.json"
    used = 0
    if bud.exists():
        b = json.loads(bud.read_text(encoding="utf-8"))
        used = b.get("ticks", 0) if b.get("date") == today else 0
    if used >= budgets.get("ticks_per_day", 24):
        out(False, [f"tick budget used today ({used})"])

    fp = live_fingerprint()
    if fp != state["nature"]["acl_fingerprint"]:
        LOCAL.mkdir(parents=True, exist_ok=True)
        (RES / "PAUSE").write_text(f"{now:%Y-%m-%d %H:%M} the live nature (acl/) changed without a record\n",
                                   encoding="utf-8")
        import notify
        notify.send("ACL Researcher: PROBLEM. The live nature code (acl/) differs from the approved fingerprint. "
                    "Research is paused until you look.", "problem")
        out(False, ["live nature fingerprint changed: paused and notified"])

    reasons = []
    for s in state.get("studies", []):
        jobs = s.get("jobs", {})
        if s.get("status") == "running-cloud" and jobs.get("cloud_run"):
            st = cloud_status(jobs["cloud_run"])
            if st == "completed":
                reasons.append(f"{s['id']}: cloud run {jobs['cloud_run']} completed")
        if s.get("status") == "running-local" and jobs.get("local"):
            d = ROOT / jobs["local_dir"]
            have = sum(1 for j in jobs["local"] if (d / f"{j.split(':')[0]}_seed_{j.split(':')[1]}.json").exists())
            if have == len(jobs["local"]):
                reasons.append(f"{s['id']}: all {have} local worlds done")
    if summary_due:
        reasons.append("daily summary due")
    out(bool(reasons), reasons or ["nothing changed"])


if __name__ == "__main__":
    main()
