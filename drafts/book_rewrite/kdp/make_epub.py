"""The Kindle (EPUB 3) edition of Part One, from the same source as the Word and PDF editions.

    python drafts/book_rewrite/kdp/make_epub.py   -> drafts/book_rewrite/kdp/The_World_That_Nobody_Wrote_Part_One.epub

Needs kindle_cover.png (render_kdp_covers.ps1). Pictures are shrunk to 1200 px JPEGs to keep the file small (Amazon
charges delivery by size). Front matter mirrors the print edition: title page, edition page, contents.
"""
import io
import re
import uuid
import zipfile
from html import escape
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
BOOK = HERE.parents[2] / "book"
SRC = HERE.parent / "part1_v2_build.md"
OUT = HERE / "The_World_That_Nobody_Wrote_Part_One.epub"
AUTHOR = "Abdurashid Khudoyberdiev"
TITLE = "The World That Nobody Wrote"
SUBTITLE = "Part One: how I tried to build a civilization instead of simulating one"
IMG_RE = re.compile(r"^!\[(.*)\]\((.+)\)$")


def inline(t):
    t = escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def jpeg(path, width=1200):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "JPEG", quality=82)
    return b.getvalue()


def page(title, body):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">'
            f'<head><meta charset="utf-8"/><title>{escape(title)}</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>'
            f'<body>{body}</body></html>')


CSS = """body{font-family:serif;line-height:1.45;margin:0 1em}
p{margin:0;text-indent:1.4em;text-align:justify}
p.first,h1+p,h2+p,div.fig+p,ul+p{text-indent:0}
p.intro{font-style:italic;text-indent:0;margin:1em 2em;text-align:center}
h1{font-weight:normal;text-align:center;margin:3em 0 1.5em;font-size:1.6em}
h2{font-weight:normal;text-align:center;margin:1em 0 1.5em;font-size:1.4em}
.label{text-align:center;text-indent:0;letter-spacing:.2em;font-size:.8em;margin-top:3em;color:#7a6a50}
div.fig{margin:1.2em 0;text-align:center;page-break-inside:avoid;break-inside:avoid}
div.fig img{max-width:100%;max-height:60vh;width:auto;height:auto}
p.cap{font-style:italic;font-size:.85em;margin-top:.4em;text-indent:0;text-align:center;page-break-before:avoid;break-before:avoid}
ul{margin:.8em 0 .8em 1.2em;padding:0}
li{margin:.3em 0}
.title{text-align:center;text-indent:0;font-size:2em;margin-top:30%}
.sub{text-align:center;text-indent:0;font-style:italic;margin:1em 0}
.imprint{text-align:center;text-indent:0;font-size:.8em;letter-spacing:.15em;margin-top:3em}
.colophon p{text-indent:0;margin:0 0 .9em;font-size:.85em;text-align:left}
nav ol{list-style:none;padding-left:1em}"""


def build():
    lines = SRC.read_text(encoding="utf-8").splitlines()
    edition = [l[3:] for l in lines if l.startswith("%% ")][-1]
    records = next(l[4:] for l in lines if l.startswith("%%% "))
    sections, cur = [], None          # each: dict(kind, title, label, html list)
    images = []
    after_part = False
    for raw in lines:
        line = raw.rstrip()
        if not line or line.startswith("%"):
            continue
        if line.startswith("## "):
            m = re.match(r"^Chapter (\d+)\s+—\s+(.+)$", line[3:])
            cur = {"kind": "chapter", "title": m.group(2) if m else line[3:],
                   "toc": f"{m.group(1)}. {m.group(2)}" if m else line[3:],
                   "label": f"CHAPTER {m.group(1)}" if m else "", "html": []}
            sections.append(cur)
            after_part = False
            continue
        if line.startswith("# "):
            t = line[2:]
            m = re.match(r"^(Part [IVX]+)\s+—\s+(.+)$", t)
            cur = {"kind": "part" if m else "top", "title": m.group(2) if m else t, "toc": t,
                   "label": m.group(1).upper() if m else "", "html": []}
            sections.append(cur)
            after_part = bool(m)
            continue
        m = IMG_RE.match(line)
        if m:
            images.append(jpeg((BOOK / m.group(2)).resolve()))
            n = len(images)
            cur["html"].append(f'<div class="fig"><img src="images/fig{n}.jpg" alt="{escape(m.group(1))}"/>'
                               f'<p class="cap">{inline(m.group(1))}</p></div>')
            continue
        if line.startswith("- "):
            if cur["html"] and cur["html"][-1].endswith("</ul>"):
                cur["html"][-1] = cur["html"][-1][:-5] + f"<li>{inline(line[2:])}</li></ul>"
            else:
                cur["html"].append(f"<ul><li>{inline(line[2:])}</li></ul>")
            continue
        cls = ' class="intro"' if after_part else ""
        cur["html"].append(f"<p{cls}>{inline(line)}</p>")

    files = {}
    files["title.xhtml"] = page(TITLE, f'<p class="title">{TITLE}</p><p class="sub">{escape(SUBTITLE)}</p>'
                                       f'<p class="imprint">{AUTHOR.upper()}</p>'
                                       '<p class="imprint">ARTIFICIAL CIVILIZATION LABORATORY</p>')
    colophon = [TITLE, edition, records,
                "This is a living book. It is meant to be revised after every major experiment, and earlier chapters "
                "are corrected in the open, never quietly rewritten.",
                "Cover and illustrations: AI-generated images, made for this edition.",
                f"© 2026 {AUTHOR}. All rights reserved. No part of this book may be copied, reproduced, adapted or "
                "distributed, or presented as anyone else's work, without written permission from the author.",
                "github.com/abu4evere/simulated-world"]
    files["colophon.xhtml"] = page("Edition", '<div class="colophon">' +
                                   "".join(f"<p>{escape(c)}</p>" for c in colophon) + "</div>")
    spine, toc = ["cover.xhtml", "title.xhtml", "colophon.xhtml", "nav.xhtml"], []
    for i, s in enumerate(sections, 1):
        name = f"s{i:02d}.xhtml"
        head = (f'<p class="label">{s["label"]}</p>' if s["label"] else "") + \
               (f'<h1>{escape(s["title"])}</h1>' if s["kind"] != "chapter" else f'<h2>{escape(s["title"])}</h2>')
        files[name] = page(s["title"], head + "".join(s["html"]))
        spine.append(name)
        toc.append((s["kind"], s["toc"], name))
    # nav: parts hold their chapters
    nav, open_part = ["<ol>"], False
    for kind, t, name in toc:
        if kind == "chapter":
            nav.append(f'<li><a href="{name}">{escape(t)}</a></li>')
            continue
        if open_part:
            nav.append("</ol></li>")
        if kind == "part":
            nav.append(f'<li><a href="{name}">{escape(t)}</a><ol>')
            open_part = True
        else:
            nav.append(f'<li><a href="{name}">{escape(t)}</a></li>')
            open_part = False
    if open_part:
        nav.append("</ol></li>")
    nav.append("</ol>")
    files["nav.xhtml"] = page("Contents", '<nav epub:type="toc" id="toc"><h1>Contents</h1>' + "".join(nav) + "</nav>")
    files["cover.xhtml"] = page("Cover", '<div style="text-align:center"><img src="images/cover.jpg" alt="Cover" '
                                         'style="max-width:100%;max-height:100%"/></div>')

    uid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "abu4evere/simulated-world/book-part-one/kindle"))
    manifest = ['<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="coverimg" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>']
    for n in range(1, len(images) + 1):
        manifest.append(f'<item id="fig{n}" href="images/fig{n}.jpg" media-type="image/jpeg"/>')
    for f in spine:
        props = ' properties="nav"' if f == "nav.xhtml" else ""
        manifest.append(f'<item id="{f[:-6]}" href="{f}" media-type="application/xhtml+xml"{props}/>')
    opf = ('<?xml version="1.0" encoding="utf-8"?>'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
           f'<dc:identifier id="bookid">{uid}</dc:identifier><dc:title>{TITLE}: Part One</dc:title>'
           f'<dc:creator>{AUTHOR}</dc:creator><dc:language>en</dc:language>'
           '<dc:publisher>Artificial Civilization Laboratory</dc:publisher>'
           f'<dc:rights>© 2026 {AUTHOR}. All rights reserved.</dc:rights>'
           '<meta property="dcterms:modified">2026-10-19T00:00:00Z</meta><meta name="cover" content="coverimg"/>'
           '</metadata><manifest>' + "".join(manifest) + '</manifest><spine>' +
           "".join(f'<itemref idref="{f[:-6]}"/>' for f in spine) + '</spine></package>')

    with zipfile.ZipFile(OUT, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                   '</rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/images/cover.jpg", jpeg(HERE / "kindle_cover.png", 1600))
        for n, data in enumerate(images, 1):
            z.writestr(f"OEBPS/images/fig{n}.jpg", data)
        for name, html in files.items():
            z.writestr(f"OEBPS/{name}", html, compress_type=zipfile.ZIP_DEFLATED)
    print(f"wrote {OUT.name}: {len(sections)} sections, {len(images)} pictures, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    build()
