"""Build the ACL research book (.docx) from its plain-text source.

    python book/build_book.py

Source: book/source/the_world_that_nobody_wrote.md — edit that, not the .docx.
Output: book/The_World_That_Nobody_Wrote_v1.docx. Its styles (fonts, headings, lists) are kept; only the
text is replaced, so the book keeps its look from one edition to the next.

Source format, one paragraph per line, blank lines between:
    % Title              %% Subtitle line
    # Part heading       (starts a new page)
    ## Chapter heading
    - bullet item        **bold** inline
    // note              not printed: notes for the editor, such as slots for the creator's own writing
    anything else        a body paragraph
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
SOURCE = HERE / "source" / "the_world_that_nobody_wrote.md"
BOOK = HERE / "The_World_That_Nobody_Wrote_v1.docx"

PAGE_BREAK = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def runs(text: str) -> str:
    out = []
    for i, part in enumerate(re.split(r"\*\*", text)):
        if part:
            bold = "<w:rPr><w:b/></w:rPr>" if i % 2 else ""
            out.append(f'<w:r>{bold}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def para(text: str, style: str | None = None) -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{runs(text)}</w:p>"


def body_xml(lines: list[str]) -> str:
    out, contents, first_part = [], [], True
    for line in lines:
        if line.startswith("# "):
            contents.append(("part", line[2:]))
        elif line.startswith("## "):
            contents.append(("chapter", line[3:]))
    for raw in lines:
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("%% "):
            out.append(para(line[3:], "Subtitle"))
        elif line.startswith("% "):
            out.append(para(line[2:], "Title"))
        elif line.startswith("# "):
            if first_part:
                # Contents, before the first part.
                out.append(PAGE_BREAK)
                out.append(para("Contents", "Heading1"))
                for kind, title in contents:
                    out.append(para(title, None) if kind == "chapter" else para(f"**{title}**"))
                first_part = False
            out.append(PAGE_BREAK)
            out.append(para(line[2:], "Heading1"))
        elif line.startswith("## "):
            out.append(para(line[3:], "Heading2"))
        elif line.startswith("- "):
            out.append(para(line[2:], "ListBullet"))
        else:
            out.append(para(line))
    return "".join(out)


def build():
    lines = [l for l in SOURCE.read_text(encoding="utf-8").splitlines() if not l.startswith("//")]
    src = zipfile.ZipFile(BOOK)
    doc = src.read("word/document.xml").decode("utf-8")
    head = doc[: doc.index("<w:body>") + len("<w:body>")]
    sect = doc[doc.index("<w:sectPr"): doc.index("</w:body>")]
    new_doc = head + body_xml(lines) + sect + "</w:body></w:document>"
    files = {i.filename: (i, src.read(i.filename)) for i in src.infolist()}
    src.close()
    tmp = BOOK.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, (info, data) in files.items():
            z.writestr(info, new_doc.encode("utf-8") if name == "word/document.xml" else data)
    tmp.replace(BOOK)
    words = sum(len(re.sub(r"^[#%\-]+ ", "", l).split()) for l in lines)
    print(f"built {BOOK.name}: {words} words")


if __name__ == "__main__":
    build()
