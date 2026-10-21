"""Turn a post draft (Markdown body after its header notes) into simple HTML for pasting into Medium.

    python drafts/posts/md_to_html.py drafts/posts/medium_article.md "In one of my simulated worlds"
"""
import html
import re
import sys
from pathlib import Path

src, start = Path(sys.argv[1]), sys.argv[2]
s = src.read_text(encoding="utf-8")
body = s[s.index(start):].strip()


def inl(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return re.sub(r"(https?://[^\s<,)]+)", r'<a href="\1">\1</a>', t)


blocks, para, items, kind = [], [], [], None


def flush_para():
    global para
    if para:
        blocks.append("<p>" + inl(" ".join(para)) + "</p>")
        para = []


def flush_list():
    global items, kind
    if items:
        blocks.append(f"<{kind}>" + "".join(f"<li>{inl(i)}</li>" for i in items) + f"</{kind}>")
        items, kind = [], None


for line in body.split("\n"):
    l = line.rstrip()
    m, b = re.match(r"^(\d+)\. (.*)", l), re.match(r"^- (.*)", l)
    if not l.strip():
        flush_para()
        continue
    if l.startswith("## "):
        flush_para(); flush_list()
        blocks.append("<h3>" + inl(l[3:]) + "</h3>")
    elif m or b:
        flush_para()
        k = "ol" if m else "ul"
        if kind and kind != k:
            flush_list()
        kind = k
        items.append(m.group(2) if m else b.group(1))
    elif l.startswith("  ") and items:
        items[-1] += " " + l.strip()
    else:
        flush_list()
        para.append(l.strip())
flush_para()
flush_list()
out = src.with_suffix(".html")
out.write_text("".join(blocks), encoding="utf-8")
print(out, len(blocks), "blocks")
