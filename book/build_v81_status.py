"""Make the v8.1 Bible with an implementation status under every law, from the creator's own v8.1 file.

The creator's file is read, never changed. Two edits, both agreed with the creator on 2026-10-03:
  1. Law 16: the trait the engine calls "diligence" was written "persistence". Use "diligence".
  2. The status notation (Implemented / Partial / Future mechanism / Example only) is explained after
     "How to read this version", and every law ends with its status (from law_status_v81.py).

Usage: python book/build_v81_status.py
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from law_status_v81 import ENGINE, STATUS  # noqa: E402

SRC = Path.home() / "Downloads" / "THE_ARTIFICIAL_CIVILIZATION_World_Bible_v8_1_EXPANDED_DRAFT.docx"
OUT = HERE / "THE_ARTIFICIAL_CIVILIZATION_World_Bible_v8_1_EXPANDED_DRAFT_with_status.docx"

PARA = re.compile(r"<w:p[ >].*?</w:p>", re.S)
TITLE = re.compile(r"^LAW (\d+):")


def text(p: str) -> str:
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))


def label(s: str) -> str:
    return (f'<w:p><w:pPr><w:pStyle w:val="RuleLabel"/><w:keepNext/></w:pPr>'
            f"<w:r><w:t>{escape(s)}</w:t></w:r></w:p>")


def body(bold: str, rest: str) -> str:
    return (f"<w:p><w:pPr/><w:r><w:rPr><w:b/></w:rPr><w:t>{escape(bold)}</w:t></w:r>"
            f'<w:r><w:t xml:space="preserve"> {escape(rest)}</w:t></w:r></w:p>')


def plain(s: str) -> str:
    return f'<w:p><w:pPr/><w:r><w:t xml:space="preserve">{escape(s)}</w:t></w:r></w:p>'


LEGEND = "".join([
    label("Implementation status notation"),
    plain("Each law ends with an implementation status. It describes the engine, not the law: a law is never "
          "weakened because the engine does not yet do what it permits, and a rule that mentions a capability does "
          f"not mean the capability already exists. Status as of 3 October 2026 ({ENGINE.split(';')[0]})."),
    body("Implemented —", "currently exists in the simulation."),
    body("Partial —", "exists in simplified form."),
    body("Future mechanism —", "permitted by the rule but not yet implemented."),
    body("Example only —", "an explanatory example, not a required current capability."),
])


def status_block(n: int) -> str:
    kind, note, example = STATUS[n]
    out = label("Implementation status") + body(kind + ".", note)
    if example:
        head, _, rest = example.partition(":")
        out += body(head.strip() + ":", rest.strip())
    return out


def main():
    with zipfile.ZipFile(SRC) as z:
        files = {i: z.read(i) for i in z.namelist()}
        infos = {i.filename: i for i in z.infolist()}
    xml = files["word/document.xml"].decode("utf-8")

    paras = list(PARA.finditer(xml))
    out, pos = [], 0
    current = None          # law whose status is still to be written
    done, fixed, legend = set(), 0, False

    def close_law():
        nonlocal current
        if current is not None:
            out.append(status_block(current))
            done.add(current)
            current = None

    for m in paras:
        p, t = m.group(0), text(m.group(0))
        out.append(xml[pos:m.start()])
        pos = m.end()
        title = TITLE.match(t)
        is_heading = 'w:val="Heading' in p
        is_blank = not t.strip()
        if current is not None and (title or is_heading or is_blank):
            close_law()
        if title:
            current = int(title.group(1))
        if current == 16 and "sociability, persistence, anxiety" in p:
            p = p.replace("sociability, persistence, anxiety", "sociability, diligence, anxiety")
            fixed += 1
        out.append(p)
        if t.startswith("A detailed rule contains four parts"):
            out.append(LEGEND)
            legend = True
    close_law()
    out.append(xml[pos:])
    new = "".join(out)

    assert fixed == 1, "Law 16 wording not found"
    assert legend, "reading guide paragraph not found"
    assert done == set(STATUS), f"laws without a status: {sorted(set(STATUS) - done)}"

    files["word/document.xml"] = new.encode("utf-8")
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(infos[name], data)
    print("wrote", OUT, f"({len(done)} laws given a status; Law 16 fixed)")


if __name__ == "__main__":
    main()
