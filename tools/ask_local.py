"""Ask the local model a question about one file, and check its answer automatically.

  python tools/ask_local.py FILE "question"
  python tools/ask_local.py --selftest          # checks the verifier itself, no model needed

The model must answer only with exact lines from the file and their line numbers. A plain script (no model) then
checks every quoted line against the file: VERIFIED if the line really is there (at that number, or, marked MOVED,
elsewhere), UNVERIFIED if it is not. Only VERIFIED lines are to be trusted; a made-up answer cannot pass.
For finding things in long files. Never for judging results or making decisions.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

MODEL = "qwen2.5:3b"
MAX_CHARS = 24000   # a small local model reads only so much; longer files are cut, and the reply says so


def ask(numbered: str, question: str) -> str:
    prompt = ("Below is a file, one line per row, each starting with its line number and a tab. Answer the question "
              "ONLY by quoting lines of the file. Reply with JSON only, in this form: "
              "{\"quotes\": [{\"line\": 12, \"text\": \"the exact text of line 12\"}], \"answer\": \"one short sentence\"}. "
              "Quote each line exactly, without its number. If the file does not answer the question, reply "
              "{\"quotes\": [], \"answer\": \"not in this file\"}.\n\nQUESTION: " + question + "\n\nFILE:\n" + numbered)
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "format": "json",
                       "options": {"temperature": 0}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["response"]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def verify(lines: list[str], reply: str) -> list[tuple[str, int, str]]:
    """(status, line number, text) for each quote: VERIFIED, MOVED (exists at another line) or UNVERIFIED."""
    try:
        quotes = json.loads(reply).get("quotes", [])
    except (json.JSONDecodeError, AttributeError):
        return [("UNVERIFIED", 0, "(the reply was not valid JSON)")]
    out = []
    for q in quotes:
        n, text = q.get("line", 0), norm(str(q.get("text", "")))
        if not text:
            continue
        if isinstance(n, int) and 1 <= n <= len(lines) and norm(lines[n - 1]) == text:
            out.append(("VERIFIED", n, text))
        else:
            hits = [i + 1 for i, l in enumerate(lines) if norm(l) == text]
            out.append(("MOVED", hits[0], text) if hits else ("UNVERIFIED", n if isinstance(n, int) else 0, text))
    return out


def selftest() -> None:
    lines = ["alpha = 1", "beta = 2", "gamma = 3"]
    reply = json.dumps({"quotes": [{"line": 2, "text": "beta = 2"}, {"line": 1, "text": "gamma = 3"},
                                   {"line": 3, "text": "delta = 4"}], "answer": "x"})
    got = [s for s, _, _ in verify(lines, reply)]
    assert got == ["VERIFIED", "MOVED", "UNVERIFIED"], got
    assert verify(lines, "not json")[0][0] == "UNVERIFIED"
    print("selftest PASS: real quotes verified, misplaced quotes found, invented quotes rejected")


def main() -> None:
    if "--selftest" in sys.argv:
        selftest()
        return
    path, question = Path(sys.argv[1]), " ".join(sys.argv[2:])
    lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
    numbered, cut = "", False
    for i, l in enumerate(lines, 1):
        row = f"{i}\t{l}\n"
        if len(numbered) + len(row) > MAX_CHARS:
            cut = True
            break
        numbered += row
    reply = ask(numbered, question)
    try:
        answer = json.loads(reply).get("answer", "")
    except (json.JSONDecodeError, AttributeError):
        answer = ""
    print(f"Q: {question}\nModel's answer (trust only the VERIFIED lines below): {answer}")
    for status, n, text in verify(lines, reply):
        print(f"{status:10s} line {n}: {text[:160]}")
    if cut:
        print(f"NOTE: the file was cut at {MAX_CHARS} characters; lines beyond that were not read.")


if __name__ == "__main__":
    main()
