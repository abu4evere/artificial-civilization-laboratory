"""Export the book to PDF through Microsoft Word (for the Zenodo deposit), after `python book/build_book.py`.

    python book/make_pdf.py

Writes release/The_World_That_Nobody_Wrote_v1.pdf. Word's own table of contents and fields are updated first.
"""
from __future__ import annotations

from pathlib import Path

import win32com.client

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "book" / "The_World_That_Nobody_Wrote_v1.docx"
DST = ROOT / "release" / "The_World_That_Nobody_Wrote_v1.pdf"
import sys                                 # an edition: python book/make_pdf.py --src X.docx --dst Y.pdf
if "--src" in sys.argv:
    SRC = Path(sys.argv[sys.argv.index("--src") + 1]).resolve()
    DST = Path(sys.argv[sys.argv.index("--dst") + 1]).resolve()
PDF = 17                                   # wdExportFormatPDF


def main():
    DST.parent.mkdir(exist_ok=True)
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(str(SRC), ReadOnly=True, AddToRecentFiles=False)
        try:
            for toc in doc.TablesOfContents:
                toc.Update()
            doc.Fields.Update()
            doc.ExportAsFixedFormat(str(DST), PDF, OpenAfterExport=False, OptimizeFor=0, CreateBookmarks=1,
                                    DocStructureTags=True,
                                    UseISO19005_1="--print" in sys.argv)   # print: PDF/A, so every font is embedded
            pages = doc.ComputeStatistics(2)           # wdStatisticPages
        finally:
            doc.Close(SaveChanges=0)
    finally:
        word.Quit()
    import pymupdf                          # PDF properties (Word leaves the title empty)
    pdf = pymupdf.open(DST)
    pdf.set_metadata({**pdf.metadata, "title": "The World That Nobody Wrote",
                      "subject": "How we tried to build a civilization instead of simulating one",
                      "author": "Abdurashid Khudoyberdiev", "keywords": "Artificial Civilization Laboratory; ACL"})
    pdf.saveIncr()
    pdf.close()
    print(f"wrote {DST.relative_to(ROOT)} ({pages} pages, {DST.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
