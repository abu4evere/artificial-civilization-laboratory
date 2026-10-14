"""Ask several AI models the same question, for ideas, and save their answers side by side in drafts/council/.

  python tools/council.py "Your question in plain words"          # every enabled model in tools/council_models.json
  python tools/council.py --file drafts/question.md               # the question from a file
  python tools/council.py --list                                   # show the models and whether each can be reached
  python tools/council.py --cloud-only "question"                  # skip models on this PC (saves memory while runs go)

Rules (docs/HELPER_RUNBOOK.md and Law 126 apply to everything that comes back):
- Ideas only. Nothing a model says is a decision; Claude sorts the answers against ACL's rules, and the creator decides.
- No private code or data leaves this PC: the question must describe ACL in words. The tool refuses text that looks
  like code or file paths.
- Keys are never written in any file: NVIDIA's key is read from the environment variable NVIDIA_API_KEY, which the
  creator sets themselves.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = Path(__file__).with_name("council_models.json")
OUT = ROOT / "drafts" / "council"
FRAME = ("You are one of several independent advisers to a research project. The project is ACL, an agent-based "
         "simulation of hunter-gatherer people in which nature (bodies, drives, temperament, learning) is programmed and "
         "culture must emerge without being scripted. The project never adds a rule that names the outcome it studies, "
         "and changes to nature must rest on evidence about real humans. Give your own ideas, briefly and concretely; "
         "say what evidence or test would show each idea right or wrong; say when you are unsure.\n\nQuestion:\n")
CODE_LIKE = re.compile(r"(^\s*(def|class|import|from)\s|[A-Za-z]:\\\\|[A-Za-z]:\\|\.py\b|\{\s*\"|=\s*\[)", re.M)


def ask(model: dict, question: str, timeout: int = 600) -> str:
    if model["provider"] == "ollama":
        url, headers = "http://localhost:11434/v1/chat/completions", {}
    elif model["provider"] == "nvidia":
        key = os.environ.get("NVIDIA_API_KEY", "")
        if not key:
            raise RuntimeError("NVIDIA_API_KEY is not set")
        url, headers = "https://integrate.api.nvidia.com/v1/chat/completions", {"Authorization": f"Bearer {key}"}
    else:
        raise RuntimeError(f"unknown provider {model['provider']}")
    # thinking models (GLM, Kimi) spend tokens on hidden reasoning first, so the limit must leave room for the answer
    body = json.dumps({"model": model["model"], "temperature": 0.7, "max_tokens": 4000,
                       "messages": [{"role": "user", "content": FRAME + question}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", **headers})
    for attempt in (1, 2):   # one retry: NVIDIA's free endpoints sometimes answer 502/503/504 when busy
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                choice = json.loads(r.read())["choices"][0]
            break
        except urllib.error.HTTPError as e:
            if attempt == 2 or e.code not in (502, 503, 504):
                raise
            time.sleep(20)
    content = choice["message"].get("content")
    if not content:
        raise RuntimeError(f"empty answer (finish_reason: {choice.get('finish_reason')})")
    return content.strip()


def main() -> None:
    models = [m for m in json.loads(MODELS.read_text(encoding="utf-8"))["models"]]
    if "--list" in sys.argv:
        for m in models:
            state = "enabled" if m.get("enabled") else "off"
            note = " (needs NVIDIA_API_KEY)" if m["provider"] == "nvidia" and not os.environ.get("NVIDIA_API_KEY") else ""
            print(f"{state:8s} {m['provider']:7s} {m['model']}{note}")
        return
    if "--file" in sys.argv:
        question = Path(sys.argv[sys.argv.index("--file") + 1]).read_text(encoding="utf-8").strip()
    else:
        question = " ".join(a for a in sys.argv[1:] if not a.startswith("--")).strip()
    if not question:
        sys.exit("Give a question in words, or --file with one.")
    if CODE_LIKE.search(question):
        sys.exit("REFUSED: the question looks like it contains code or file paths. Describe it in words instead.")
    OUT.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", question.lower())[:50].strip("_")
    path = OUT / f"{datetime.now():%Y-%m-%d_%H%M}_{slug}.md"
    lines = [f"# Council: {question[:120]}", "", f"Asked {datetime.now():%Y-%m-%d %H:%M}. **Ideas only; not decisions.** "
             "Claude sorts these against ACL's rules before anything is used.", "", "## The question", "", question, ""]
    for m in models:
        if not m.get("enabled") or ("--cloud-only" in sys.argv and m["provider"] == "ollama"):
            continue
        print(f"asking {m['provider']} {m['model']} ...", flush=True)
        try:
            answer = ask(m, question)
        except Exception as e:  # noqa: BLE001
            answer = f"(no answer: {type(e).__name__}: {e})"
        lines += [f"## {m['provider']}: {m['model']}", "", answer, ""]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"saved {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
