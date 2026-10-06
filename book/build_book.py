"""Build the ACL book as a typeset .docx from its plain-text source.

    python book/build_book.py

Source: book/source/the_world_that_nobody_wrote.md — edit that, not the .docx.
Cover:  book/cover/cover.png (made by book/cover/make_cover.py).
Output: book/The_World_That_Nobody_Wrote_v1.docx

The book is laid out like a printed trade paperback: 6 x 9 inch pages with mirrored margins, a full-bleed
cover, a title page, an edition page, a table of contents, a page of its own for every part, every chapter
opening on a new page, Garamond text set justified with indented paragraphs, and page numbers in the footer.
Word fills in the contents' page numbers when the file is opened (it asks first).

Source format, one paragraph per line, blank lines between:
    % Title              %% Subtitle line (the last one is the edition line)
    # Part I — Name      a part page;  "# Appendix A — Name" and "# Some Title" open unnumbered sections
    ## Chapter N — Name  a chapter opening
    - bullet item        **bold** inline
    ![caption](path)     a figure, full text width, with its caption below; path relative to book/
    // note              not printed: notes for the editor, such as slots for the creator's own writing
    anything else        a body paragraph
"""
from __future__ import annotations

import re
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
SOURCE = HERE / "source" / "the_world_that_nobody_wrote.md"
COVER = HERE / "cover" / "cover.png"
BOOK = HERE / "The_World_That_Nobody_Wrote_v1.docx"

# --- page geometry (twentieths of a point; 1440 = 1 inch) -----------------------------------------------
PAGE_W, PAGE_H = 8640, 12960                      # 6 x 9 in
TOP, BOTTOM, INNER, OUTER = 1150, 1150, 1080, 900
TEXT_W = PAGE_W - INNER - OUTER
EMU = 914400                                      # per inch

FONT = "Garamond"
INK = "1E1B18"
ACCENT = "8A6A4A"

W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
DOC_NS = (W_NS + ' xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
          'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
          'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')


# --- text -------------------------------------------------------------------------------------------------
def runs(text: str, rpr: str = "") -> str:
    out = []
    for i, part in enumerate(re.split(r"\*\*", text)):
        if part:
            bold = "<w:b/>" if i % 2 else ""
            props = f"<w:rPr>{bold}{rpr}</w:rPr>" if (bold or rpr) else ""
            out.append(f'<w:r>{props}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def para(text: str, style: str, extra_ppr: str = "", rpr: str = "") -> str:
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{extra_ppr}</w:pPr>{runs(text, rpr)}</w:p>'


def first_para(text: str) -> str:
    """A chapter's opening paragraph: no indent, the first few words in small capitals."""
    if text.startswith("**"):
        return para(text, "BodyFirst")
    words = text.split(" ")
    n = min(3, len(words))
    lead, rest = " ".join(words[:n]), " ".join(words[n:])
    return ('<w:p><w:pPr><w:pStyle w:val="BodyFirst"/></w:pPr>'
            + runs(lead, "<w:smallCaps/>") + runs((" " + rest) if rest else "") + "</w:p>")


def toc_entry(text: str, level: int) -> str:
    """A hidden contents marker (a TC field). The table of contents is built from these, so each entry
    keeps its label ("Part VI: Lives", "38.  Reibik") instead of only the bare heading."""
    text = escape(text).replace('"', "'")
    return ('<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r><w:instrText xml:space="preserve"> TC "{text}" \\l {level} </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r>')


def heading(text: str, style: str, entry: str, level: int) -> str:
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs(text)}{toc_entry(entry, level)}</w:p>'


def page_break() -> str:
    return '<w:p><w:pPr><w:pStyle w:val="Spacer"/></w:pPr><w:r><w:br w:type="page"/></w:r></w:p>'


def spacer(twips: int) -> str:
    return f'<w:p><w:pPr><w:pStyle w:val="Spacer"/><w:spacing w:before="{twips}"/></w:pPr></w:p>'


def section_break(kind: str) -> str:
    """Ends a section: 'cover' (no margins), 'front' (no page numbers)."""
    if kind == "cover":
        sect = (f'<w:sectPr><w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>'
                '<w:pgMar w:top="0" w:right="0" w:bottom="0" w:left="0" w:header="0" w:footer="0" w:gutter="0"/>'
                '</w:sectPr>')
    else:
        sect = (f'<w:sectPr><w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>'
                f'<w:pgMar w:top="{TOP}" w:right="{OUTER}" w:bottom="{BOTTOM}" w:left="{INNER}" '
                'w:header="576" w:footer="576" w:gutter="0"/></w:sectPr>')
    return f'<w:p><w:pPr><w:pStyle w:val="Spacer"/>{sect}</w:pPr></w:p>'


def body_section() -> str:
    return (f'<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter"/>'
            f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>'
            f'<w:pgMar w:top="{TOP}" w:right="{OUTER}" w:bottom="{BOTTOM}" w:left="{INNER}" '
            'w:header="576" w:footer="576" w:gutter="0"/><w:pgNumType w:start="1"/></w:sectPr>')


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    return struct.unpack(">II", data[16:24])


def cover_image() -> str:
    """The cover fills the first page: an image anchored to the page corner, behind everything."""
    cx, cy = 6 * EMU, 9 * EMU
    return f'''<w:p><w:pPr><w:pStyle w:val="Spacer"/></w:pPr><w:r><w:drawing>
<wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="1" behindDoc="1" locked="1" layoutInCell="1" allowOverlap="1">
<wp:simplePos x="0" y="0"/>
<wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>
<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>
<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>
<wp:docPr id="1" name="Cover" descr="An archipelago at dusk, campfires on the islands, a raft between them, and a watcher on a cliff"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>
<pic:nvPicPr><pic:cNvPr id="1" name="cover.png"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="rIdCover"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:anchor></w:drawing></w:r></w:p>'''


# --- the book -------------------------------------------------------------------------------------------
IMAGE_RE = re.compile(r"^!\[(.*)\]\((.+)\)$")
IMAGES: list[Path] = []                           # figures in the body, in order; filled while building


def figure(caption: str, path: Path) -> str:
    """A picture set inline at full text width, centred, with its caption beneath."""
    IMAGES.append(path)
    n = len(IMAGES)
    w, h = png_size(path)
    cx = TEXT_W * EMU // 1440
    cy = cx * h // w
    pic = f'''<w:p><w:pPr><w:pStyle w:val="Figure"/></w:pPr><w:r><w:drawing>
<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>
<wp:docPr id="{100 + n}" name="Figure {n}" descr="{escape(caption)}"/>
<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>
<pic:nvPicPr><pic:cNvPr id="{100 + n}" name="figure{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="rIdFig{n}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    return pic + para(caption, "Caption")


PART_RE = re.compile(r"^(Part [IVXLC]+|Appendix [A-Z])\s+—\s+(.+)$")
CHAP_RE = re.compile(r"^Chapter (\d+)\s+—\s+(.+)$")


def parse(lines):
    title, subtitles, blocks = "", [], []
    for raw in lines:
        line = raw.rstrip()
        if not line or line.startswith("//"):
            continue
        if line.startswith("%% "):
            subtitles.append(line[3:])
        elif line.startswith("% "):
            title = line[2:]
        elif line.startswith("# "):
            blocks.append(("part", line[2:]))
        elif line.startswith("## "):
            blocks.append(("chapter", line[3:]))
        elif line.startswith("- "):
            blocks.append(("bullet", line[2:]))
        elif IMAGE_RE.match(line):
            blocks.append(("image", line))
        else:
            blocks.append(("text", line))
    return title, subtitles, blocks


def front_matter(title, subtitles) -> str:
    sub, edition = subtitles[0], (subtitles[1] if len(subtitles) > 1 else "")
    words = title.split()
    half = len(words) // 2 + len(words) % 2
    out = [cover_image(), section_break("cover")]
    # title page
    out.append(spacer(2600))
    out.append(para(" ".join(words[:half]), "BookTitle"))
    out.append(para(" ".join(words[half:]), "BookTitle"))
    out.append(para("—", "Ornament"))
    out.append(para(sub, "BookSubtitle"))
    out.append(spacer(3400))
    out.append(para("ARTIFICIAL CIVILIZATION LABORATORY", "Imprint"))
    out.append(page_break())
    # edition page
    out.append(spacer(5000))
    for line in (title, edition,
                 "Written from the experiment records of the Artificial Civilization Laboratory, E0 to E7.7. "
                 "Every number in this book comes from a record in the project's repository; every name is a "
                 "person who lived in a seeded world.",
                 "This is a living book. It is meant to be revised after every major experiment, and earlier "
                 "chapters are corrected in the open, never quietly rewritten.",
                 "Cover: an archipelago at dusk, drawn for this edition.",
                 "© 2026 Abdurashid Khudoyberdiev. All rights reserved. No part of this book may be copied, "
                 "reproduced, adapted or distributed, or presented as anyone else's work, without written permission "
                 "from the author.",
                 "github.com/abu4evere/simulated-world"):
        if line:
            out.append(para(line, "Colophon"))
    out.append(page_break())
    return "".join(out)


def contents(blocks) -> str:
    """A real table of contents field. Its saved result lists the entries; Word adds page numbers on open."""
    out = [para("Contents", "ContentsTitle")]
    out.append('<w:p><w:pPr><w:pStyle w:val="TOC1"/></w:pPr>'
               '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
               '<w:r><w:instrText xml:space="preserve"> TOC \\f \\l "1-2" \\z </w:instrText></w:r>'
               '<w:r><w:fldChar w:fldCharType="separate"/></w:r></w:p>')
    for kind, text in blocks:
        if kind == "part":
            m = PART_RE.match(text)
            out.append(para(f"{m.group(1)}: {m.group(2)}" if m else text, "TOC1"))
        elif kind == "chapter":
            m = CHAP_RE.match(text)
            out.append(para(f"{m.group(1)}.  {m.group(2)}" if m else text, "TOC2"))
    out.append('<w:p><w:pPr><w:pStyle w:val="TOC2"/></w:pPr><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')
    out.append(section_break("front"))
    return "".join(out)


def body(blocks) -> str:
    out = []
    after_heading = True
    in_part_intro = False          # text right after a part title is its introduction, on the part page
    # The body is a new section, so it already starts a page; its first heading must not break again.
    for n, (kind, text) in enumerate(blocks):
        first = n == 0
        if kind == "part":
            m = PART_RE.match(text)
            if m and m.group(1).startswith("Part"):
                # a part page: label, title, and any introduction; the next chapter starts a new page
                out.append(para(m.group(1).upper(), "PartLabelFirst" if first else "PartLabel"))
                out.append(heading(m.group(2), "Heading1", f"{m.group(1)}: {m.group(2)}", 1))
                out.append(para("—", "Ornament"))
                in_part_intro = True
            else:
                # an unnumbered section (the note, the appendices): opens like a chapter
                label, name = (m.group(1).upper(), m.group(2)) if m else ("", text)
                out.append(para(label or " ", "ChapterLabelFirst" if first else "ChapterLabel"))
                out.append(heading(name, "Heading1Plain", f"{m.group(1)}: {m.group(2)}" if m else text, 1))
                in_part_intro = False
            after_heading = True
            continue
        if kind == "chapter":
            m = CHAP_RE.match(text)
            out.append(para(f"CHAPTER {m.group(1)}" if m else " ", "ChapterLabelFirst" if first else "ChapterLabel"))
            out.append(heading(m.group(2) if m else text, "Heading2", f"{m.group(1)}.  {m.group(2)}" if m else text, 2))
            after_heading = True
            in_part_intro = False
            continue
        if kind == "image":
            m = IMAGE_RE.match(text)
            out.append(figure(m.group(1), (HERE / m.group(2)).resolve()))
            after_heading = True
            continue
        if kind == "bullet":
            out.append(para(text, "ListBullet"))
            after_heading = True          # the paragraph after a list starts flush, as after a heading
            continue
        # body text
        if in_part_intro:
            out.append(para(text, "PartIntro"))
        elif after_heading:
            out.append(first_para(text))
        else:
            out.append(para(text, "BodyText"))
        after_heading = False
    return "".join(out)


# --- package parts -------------------------------------------------------------------------------------
def rpr(size, bold=False, italic=False, caps=False, spacing=0, color=INK, font=FONT):
    return (f'<w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
            + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + ("<w:caps/>" if caps else "")
            + (f'<w:spacing w:val="{spacing}"/>' if spacing else "")
            + f'<w:color w:val="{color}"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>')


def style(sid, name, ppr, rp, kind="paragraph", based="Normal", nxt=None, outline=None, extra=""):
    ol = f'<w:outlineLvl w:val="{outline}"/>' if outline is not None else ""
    nx = f'<w:next w:val="{nxt}"/>' if nxt else ""
    bs = f'<w:basedOn w:val="{based}"/>' if based and sid != "Normal" else ""
    return (f'<w:style w:type="{kind}" w:styleId="{sid}"><w:name w:val="{name}"/>{bs}{nx}<w:qFormat/>'
            f'<w:pPr>{ppr}{ol}</w:pPr>{rp}{extra}</w:style>')


def styles_xml() -> str:
    tab = f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_W}"/></w:tabs>'
    s = [
        style("Normal", "Normal", '<w:widowControl/><w:spacing w:after="0" w:line="276" w:lineRule="auto"/>',
              rpr(24)),
        style("BodyText", "Body Text",
              '<w:spacing w:after="0" w:line="276" w:lineRule="auto"/><w:ind w:firstLine="360"/><w:jc w:val="both"/>',
              rpr(24)),
        style("BodyFirst", "Body Text First", '<w:spacing w:after="0" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/>',
              rpr(24), nxt="BodyText"),
        style("ListBullet", "List Bullet",
              '<w:numPr><w:numId w:val="1"/></w:numPr><w:spacing w:before="40" w:after="40" w:line="264" w:lineRule="auto"/>'
              '<w:ind w:left="540" w:hanging="260"/>', rpr(24)),
        style("PartLabel", "Part Label",
              '<w:pageBreakBefore/><w:spacing w:before="3400" w:after="200"/><w:jc w:val="center"/>',
              rpr(22, spacing=60, color=ACCENT)),
        style("Heading1", "heading 1", '<w:keepNext/><w:spacing w:after="160"/><w:jc w:val="center"/>',
              rpr(52), outline=0, nxt="Ornament"),
        style("Heading1Plain", "Section Title", '<w:keepNext/><w:spacing w:after="560"/><w:jc w:val="center"/>',
              rpr(44), outline=0, nxt="BodyFirst"),
        style("Ornament", "Ornament", '<w:keepNext/><w:spacing w:after="360"/><w:jc w:val="center"/>',
              rpr(28, color=ACCENT)),
        style("PartIntro", "Part Introduction",
              f'<w:spacing w:after="160" w:line="276" w:lineRule="auto"/><w:ind w:left="540" w:right="540"/><w:jc w:val="center"/>',
              rpr(23, italic=True, color="4A4440")),
        style("ChapterLabelFirst", "Chapter Label (section start)",
              '<w:keepNext/><w:spacing w:before="1600" w:after="120"/><w:jc w:val="center"/>',
              rpr(20, spacing=50, color=ACCENT)),
        style("PartLabelFirst", "Part Label (section start)",
              '<w:spacing w:before="3400" w:after="200"/><w:jc w:val="center"/>',
              rpr(22, spacing=60, color=ACCENT)),
        style("ChapterLabel", "Chapter Label",
              '<w:pageBreakBefore/><w:keepNext/><w:spacing w:before="1600" w:after="120"/><w:jc w:val="center"/>',
              rpr(20, spacing=50, color=ACCENT)),
        style("Heading2", "heading 2", '<w:keepNext/><w:spacing w:after="600"/><w:jc w:val="center"/>',
              rpr(40), outline=1, nxt="BodyFirst"),
        style("BookTitle", "Book Title", '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>',
              rpr(64)),
        style("BookSubtitle", "Book Subtitle", '<w:spacing w:after="0"/><w:ind w:left="540" w:right="540"/><w:jc w:val="center"/>',
              rpr(28, italic=True, color="4A4440")),
        style("Imprint", "Imprint", '<w:jc w:val="center"/>', rpr(18, spacing=60, color=ACCENT)),
        style("Colophon", "Colophon", '<w:spacing w:after="160" w:line="252" w:lineRule="auto"/>',
              rpr(18, color="4A4440")),
        style("ContentsTitle", "Contents Title", '<w:spacing w:before="600" w:after="480"/><w:jc w:val="center"/>',
              rpr(40)),
        style("TOC1", "toc 1", f'<w:keepNext/>{tab}<w:spacing w:before="200" w:after="40"/>',
              rpr(21, caps=True, spacing=20, color=ACCENT)),
        style("TOC2", "toc 2", f'{tab}<w:spacing w:after="20"/><w:ind w:left="240"/>', rpr(21)),
        style("Figure", "Figure", '<w:keepNext/><w:spacing w:before="240" w:after="80"/><w:jc w:val="center"/>', rpr(24)),
        style("Caption", "caption", '<w:spacing w:after="240"/><w:jc w:val="center"/>',
              rpr(19, italic=True, color="4A4440")),
        style("Spacer", "Spacer", '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>', rpr(2)),
        style("Footer", "footer", '<w:jc w:val="center"/>', rpr(19, color="4A4440")),
    ]
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {W_NS}>'
            f'<w:docDefaults><w:rPrDefault>{rpr(24)}</w:rPrDefault><w:pPrDefault><w:pPr>'
            '<w:spacing w:after="0" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
            + "".join(s) + "</w:styles>")


NUMBERING = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering {W_NS}>'
             '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/>'
             '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/>'
             '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="540" w:hanging="260"/></w:pPr>'
             f'<w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:color w:val="{ACCENT}"/></w:rPr></w:lvl>'
             '</w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')

FOOTER = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {W_NS}>'
          '<w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr>'
          '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
          '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')

SETTINGS = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {W_NS}>'
            '<w:updateFields w:val="true"/><w:mirrorMargins/><w:defaultTabStop w:val="360"/>'
            '<w:characterSpacingControl w:val="doNotCompress"/>'
            '<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
            '</w:settings>')

CONTENT_TYPES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                 '<Default Extension="xml" ContentType="application/xml"/>'
                 '<Default Extension="png" ContentType="image/png"/>'
                 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                 '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                 '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
                 '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
                 '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
                 '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
                 '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
                 '</Types>')

ROOT_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
             '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
             '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
             '</Relationships>')

DOC_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
            '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
            '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
            '<Relationship Id="rIdCover" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/cover.png"/>'
            '{figures}</Relationships>')


def core(title) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(title)}</dc:title><dc:creator>Artificial Civilization Laboratory</dc:creator>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>')


APP = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
       '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
       '<Application>ACL book builder</Application></Properties>')


def build():
    IMAGES.clear()
    title, subtitles, blocks = parse(SOURCE.read_text(encoding="utf-8").splitlines())
    w, h = png_size(COVER)
    assert abs(w / h - 2 / 3) < 0.01, f"cover should be 2:3, is {w}x{h}"
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {DOC_NS}><w:body>'
                + front_matter(title, subtitles) + contents(blocks) + body(blocks) + body_section()
                + "</w:body></w:document>")
    parts = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": ROOT_RELS,
        "docProps/core.xml": core(title),
        "docProps/app.xml": APP,
        "word/document.xml": document,
        "word/styles.xml": styles_xml(),
        "word/numbering.xml": NUMBERING,
        "word/settings.xml": SETTINGS,
        "word/footer1.xml": FOOTER,
        "word/_rels/document.xml.rels": DOC_RELS.format(figures="".join(
            f'<Relationship Id="rIdFig{n}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="media/figure{n}.png"/>' for n in range(1, len(IMAGES) + 1))),
    }
    tmp = BOOK.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, text in parts.items():
            z.writestr(name, text.encode("utf-8"))
        z.write(COVER, "word/media/cover.png")
        for n, path in enumerate(IMAGES, 1):
            z.write(path, f"word/media/figure{n}.png")
    tmp.replace(BOOK)
    words = sum(len(t.split()) for k, t in blocks if k != "image")
    chapters = sum(1 for k, _ in blocks if k == "chapter")
    print(f"built {BOOK.name}: {chapters} chapters, {words} words")


if __name__ == "__main__":
    build()
