r"""The Part One cover: the book's cover (book/cover/cover.svg, unchanged) with "PART ONE" set under the subtitle, in the
cover's gold, small and widely spaced like its other capitals.

    python book/editions/part1/make_cover_part1.py      -> book/editions/part1/cover_part1.svg
    powershell -File book\cover\render_cover.ps1 -Svg book\editions\part1\cover_part1.svg -Png book\editions\part1\cover_part1.png
"""
from pathlib import Path

HERE = Path(__file__).parent
svg = (HERE.parents[1] / "cover" / "cover.svg").read_text(encoding="utf-8")
mark = ('<text x="800.0" y="700" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-size="46" '
        'fill="#e2a85c" letter-spacing="16">PART ONE</text>\n')
assert svg.rstrip().endswith("</svg>")
(HERE / "cover_part1.svg").write_text(svg.rstrip()[:-len("</svg>")] + mark + "</svg>\n", encoding="utf-8")
print("wrote cover_part1.svg")
