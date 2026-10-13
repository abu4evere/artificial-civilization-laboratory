"""The whole project's status in about 30 lines, so a status check is cheap. Reads only; changes nothing.

  python tools/project_status.py

Order: what is running, what the helper did, what was committed lately, what is unsaved, what waits for the creator.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def tail(path: Path, n: int) -> list[str]:
    if not path.exists():
        return []
    rows = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and l[:2] == "20"]
    return rows[-n:]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("== Runs")
    import acl_status
    acl_status.main()
    print("\n== Helper's work log (last 5 lines)")
    for l in tail(ROOT / "WORKLOG.md", 5) or ["(nothing written)"]:
        print("  " + l)
    print("\n== Recent commits")
    print("\n".join("  " + l[:110] for l in git("log", "-6", "--format=%h %ad %s", "--date=format:%m-%d %H:%M").splitlines()))
    tags = git("tag", "--sort=-creatordate").splitlines()[:6]
    print("  latest tags: " + ", ".join(tags))
    changed = [l for l in git("status", "--porcelain").splitlines()
               if not l.endswith((".txt",)) and "/output" not in l and "/output_" not in l]
    print(f"\n== Uncommitted changes outside run outputs: {len(changed)}")
    for l in changed[:8]:
        print("  " + l)
    drafts = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "drafts").rglob("*.md") if p.name != "README.md")
    print(f"\n== Drafts waiting for review: {len(drafts)}")
    for d in drafts[-8:]:
        print("  " + d)
    print("\n== Open decisions for the creator")
    od = ROOT / "docs" / "OPEN_DECISIONS.md"
    for l in od.read_text(encoding="utf-8").splitlines() if od.exists() else []:
        if l.startswith("- [ ]"):
            print("  " + l[6:].rsplit(" (`", 1)[0])


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    main()
