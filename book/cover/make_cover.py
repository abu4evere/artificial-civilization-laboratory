"""Draw the book cover (2:3, 1600 x 2400): the creator's chosen picture (a valley at sunset seen from a rock, from an
AI-generated image the creator supplied, `source_scene.webp`; only its picture is used, not its lettering), set
full-width in the lower part and faded into a night-blue field, with the book's title, subtitle and author above and
below in light type.

    python book/cover/make_cover.py     -> book/cover/cover.svg (picture embedded)
Render to PNG with a headless browser (see render_cover.ps1).

(Earlier covers, a dusk scene, a map of world 515 and a daylight camp, are in the repository's history.)
"""
import base64
import io
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
W, H = 1600, 2400
CROP = (75, 545, 995, 1290)                      # the source's picture, without its frame, spine shading and lettering
TOP, BOTTOM = "#021428", "#0c1013"               # the source's own sky (top of the crop) and rock (bottom)
PIC_Y = 880

src = Image.open(HERE / "source_scene.webp").convert("RGB").crop(CROP)
pic = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
buf = io.BytesIO()
pic.save(buf, "JPEG", quality=92)
data = base64.b64encode(buf.getvalue()).decode()
PH = pic.height

INK, SOFT, GOLD = "#f3efe6", "#b7c2d0", "#e2a85c"
FONT = "Cormorant Garamond, Georgia, serif"
out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" '
  f'width="{W}" height="{H}">')
a(f"""<defs>
  <linearGradient id="field" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#010d1c"/><stop offset="0.35" stop-color="{TOP}"/>
    <stop offset="0.75" stop-color="{TOP}"/><stop offset="1" stop-color="{BOTTOM}"/>
  </linearGradient>
  <linearGradient id="fadeTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{TOP}" stop-opacity="1"/><stop offset="1" stop-color="{TOP}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="fadeBottom" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BOTTOM}" stop-opacity="0"/><stop offset="1" stop-color="{BOTTOM}" stop-opacity="1"/>
  </linearGradient>
</defs>""")
a(f'<rect width="{W}" height="{H}" fill="url(#field)"/>')
a(f'<image x="0" y="{PIC_Y}" width="{W}" height="{PH}" xlink:href="data:image/jpeg;base64,{data}"/>')
a(f'<rect x="0" y="{PIC_Y - 2}" width="{W}" height="240" fill="url(#fadeTop)"/>')
a(f'<rect x="0" y="{PIC_Y + PH - 260}" width="{W}" height="262" fill="url(#fadeBottom)"/>')
a(f'<rect x="0" y="{PIC_Y + PH}" width="{W}" height="{H - PIC_Y - PH}" fill="{BOTTOM}"/>')

a(f'<text x="{W / 2}" y="300" text-anchor="middle" font-family="{FONT}" font-weight="500" font-size="150" '
  f'fill="{INK}" letter-spacing="2">The World That</text>')
a(f'<text x="{W / 2}" y="455" text-anchor="middle" font-family="{FONT}" font-weight="500" font-size="150" '
  f'fill="{INK}" letter-spacing="2">Nobody Wrote</text>')
a(f'<line x1="{W / 2 - 60}" y1="525" x2="{W / 2 + 60}" y2="525" stroke="{GOLD}" stroke-width="3"/>')
a(f'<text x="{W / 2}" y="598" text-anchor="middle" font-family="{FONT}" font-style="italic" font-size="50" '
  f'fill="{SOFT}">How we tried to build a civilization instead of simulating one</text>')
a(f'<text x="{W / 2}" y="2205" text-anchor="middle" font-family="{FONT}" font-size="48" fill="{INK}" '
  f'letter-spacing="6">ABDURASHID KHUDOYBERDIEV</text>')
a(f'<line x1="{W / 2 - 40}" y1="2240" x2="{W / 2 + 40}" y2="2240" stroke="{GOLD}" stroke-width="2"/>')
a(f'<text x="{W / 2}" y="2300" text-anchor="middle" font-family="{FONT}" font-size="32" fill="{SOFT}" '
  f'letter-spacing="11">ARTIFICIAL CIVILIZATION LABORATORY</text>')
a("</svg>")
(HERE / "cover.svg").write_text("\n".join(out), encoding="utf-8")
print(f"wrote cover.svg (picture {W} x {PH} at y {PIC_Y})")
