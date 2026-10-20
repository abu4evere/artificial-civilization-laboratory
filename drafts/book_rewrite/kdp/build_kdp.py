"""Build every file the Amazon (KDP) upload needs, from the book's source, in one go.

    python drafts/book_rewrite/kdp/build_kdp.py

  1. paperback interior: 6 x 9 in PDF, no cover page, every font embedded, pictures at print resolution
  2. paperback cover: one PDF (back, spine, front, with bleed), spine width from the interior's page count
  3. Kindle cover (1600 x 2560) and the Kindle ebook (EPUB)
"""
import glob
import os
import re
import subprocess
import sys
from pathlib import Path

import pymupdf
from PIL import Image

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
SRC = HERE.parent / "part1_v2_build.md"
DOCX = HERE / "interior_6x9.docx"
INTERIOR = HERE / "The_World_That_Nobody_Wrote_Part_One_interior_6x9.pdf"
COVER_PDF = HERE / "The_World_That_Nobody_Wrote_Part_One_paperback_cover.pdf"
PY = sys.executable


def run(*args):
    subprocess.run(args, check=True, cwd=ROOT)


def interior():
    run(PY, "book/build_book.py", "--src", str(SRC), "--out", str(DOCX), "--print")
    run(PY, "book/make_pdf.py", "--src", str(DOCX), "--dst", str(INTERIOR), "--print")
    # Word's PDF export downsamples pictures to 200 dpi; put the full-size originals back
    md = SRC.read_text(encoding="utf-8")
    originals = [(ROOT / "book" / p).resolve() for p in re.findall(r"^!\[[^]]*\]\(([^)]+)\)", md, re.M)]
    (HERE / "print_images").mkdir(exist_ok=True)
    jpgs = []
    for p in originals:
        full = p.with_name(p.name.replace("_web.png", ".png"))
        im = Image.open(full if full.exists() else p).convert("RGB")
        if im.width > 1800:
            im = im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS)
        j = HERE / "print_images" / (full.stem + ".jpg")
        im.save(j, quality=92)
        jpgs.append(j)
    d = pymupdf.open(INTERIOR)
    placed = [(pg.number, im[0]) for pg in d for im in pg.get_images()]
    assert len(placed) == len(jpgs), (len(placed), len(jpgs))
    for (n, xref), j in zip(placed, jpgs):
        d[n].replace_image(xref, filename=str(j))
    tmp = INTERIOR.with_suffix(".tmp")
    d.save(tmp, garbage=4, deflate=True)
    d.close()
    os.replace(tmp, INTERIOR)
    pages = len(pymupdf.open(INTERIOR))
    print(f"interior: {pages} pages")
    return pages


def covers(pages):
    run(PY, str(HERE / "make_kdp_covers.py"), str(pages))
    spine = pages * 0.002252
    w_in, h_in = 2 * 0.125 + 12 + spine, 9.25
    w, h = round(w_in * 300), round(h_in * 300)
    run("powershell", "-ExecutionPolicy", "Bypass", "-File", str(HERE / "render_kdp_covers.ps1"),
        "-W", str(w), "-H", str(h))
    im = Image.open(HERE / "paperback_cover.png").convert("RGB")
    assert im.size == (w, h), im.size
    doc = pymupdf.open()                      # the picture, lossless, on a page of the exact cover size
    pg = doc.new_page(width=w_in * 72, height=h_in * 72)
    pg.insert_image(pg.rect, filename=str(HERE / "paperback_cover.png"))
    doc.save(COVER_PDF, deflate=True)
    print(f"paperback cover: {w_in:.4f} x {h_in} in ({w} x {h} px)")


if __name__ == "__main__":
    n = interior()
    covers(n)
    run(PY, str(HERE / "make_epub.py"))
