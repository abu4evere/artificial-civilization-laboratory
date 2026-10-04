"""A self-contained HTML report of one run: charts, the final map, and the chronicle."""
from __future__ import annotations

import html
import json
from collections import Counter

from .matter import pile_warmth

W, H = 640, 220
ML, MR, MT, MB = 44, 16, 14, 26

CSS = """
:root{color-scheme:light;
 --page:#f9f9f7;--surface:#fcfcfb;--ink:#0b0b0b;--ink-2:#52514e;--muted:#898781;
 --grid:#e1e0d9;--axis:#c3c2b7;--ring:rgba(11,11,11,.10);
 --s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--land:#008300;--water:#2a6fb0;--shelter:#0b0b0b}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;
 --page:#0d0d0d;--surface:#1a1a19;--ink:#fff;--ink-2:#c3c2b7;--muted:#898781;
 --grid:#2c2c2a;--axis:#383835;--ring:rgba(255,255,255,.10);
 --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--land:#0ca30c;--water:#2a6fb0;--shelter:#ffffff}}
:root[data-theme="dark"]{color-scheme:dark;
 --page:#0d0d0d;--surface:#1a1a19;--ink:#fff;--ink-2:#c3c2b7;--muted:#898781;
 --grid:#2c2c2a;--axis:#383835;--ring:rgba(255,255,255,.10);
 --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--land:#0ca30c;--water:#2a6fb0;--shelter:#ffffff}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:980px;margin:0 auto;padding:32px 16px 64px}
h1{font-size:28px;margin:0 0 4px;font-weight:650}
h2{font-size:18px;margin:40px 0 12px;font-weight:620}
.sub{color:var(--ink-2);margin:0 0 24px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}
.tile{background:var(--surface);border:1px solid var(--ring);border-radius:10px;padding:12px 14px}
.tile .label{color:var(--ink-2);font-size:13px}
.tile .value{font-size:26px;font-weight:600}
.tile .note{color:var(--muted);font-size:12px}
.card{background:var(--surface);border:1px solid var(--ring);border-radius:12px;padding:16px;margin-top:12px;position:relative}
.card h3{margin:0 0 2px;font-size:15px;font-weight:600}
.card .hint{margin:0 0 8px;color:var(--ink-2);font-size:13px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
svg{display:block;width:100%;height:auto;overflow:visible}
svg text{fill:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}
.legend{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:13px;color:var(--ink-2);margin:4px 0 8px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.key{display:inline-block;width:14px;height:2px;border-radius:2px}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%}
.tip{position:absolute;pointer-events:none;background:var(--surface);border:1px solid var(--ring);
 border-radius:8px;padding:6px 10px;font-size:13px;box-shadow:0 4px 16px rgba(0,0,0,.12);display:none;z-index:2;min-width:120px}
.tip .yr{color:var(--muted);font-size:12px}
.tip .row{display:flex;align-items:center;gap:6px;white-space:nowrap}
.tip strong{font-variant-numeric:tabular-nums}
.chron{max-height:560px;overflow:auto;padding-right:8px}
.chron .year{color:var(--muted);font-size:12px;margin-top:10px;font-variant-numeric:tabular-nums}
.chron p{margin:2px 0}
.chron .era{border-left:2px solid var(--axis);padding:4px 10px;margin:14px 0;color:var(--ink-2)}
.bars .row{display:grid;grid-template-columns:110px 1fr 44px;align-items:center;gap:8px;margin:6px 0;font-size:13px}
.bars .track{height:12px}
.bars .bar{height:12px;border-radius:0 4px 4px 0;background:var(--s1)}
.bars .n{text-align:right;font-variant-numeric:tabular-nums;color:var(--ink-2)}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th,td{text-align:right;padding:4px 8px;border-bottom:1px solid var(--grid)}
th:first-child,td:first-child{text-align:left}
details{margin-top:12px}
summary{cursor:pointer;color:var(--ink-2)}
.tablewrap{overflow-x:auto}
ul.plain{padding-left:18px;margin:6px 0}
"""

JS = """
const tip=document.createElement('div');tip.className='tip';
document.querySelectorAll('[data-chart]').forEach(svg=>{
  const card=svg.closest('.card');const t=tip.cloneNode();card.appendChild(t);
  const d=JSON.parse(svg.dataset.chart);const cross=svg.querySelector('.cross');
  const ov=svg.querySelector('.overlay');
  function show(ev){
    const r=svg.getBoundingClientRect();const sx=(ev.clientX-r.left)*(%W%/r.width);
    let i=Math.round((sx-%ML%)/d.dx);i=Math.max(0,Math.min(d.x.length-1,i));
    const x=%ML%+i*d.dx;cross.setAttribute('x1',x);cross.setAttribute('x2',x);cross.style.display='';
    t.replaceChildren();const yr=document.createElement('div');yr.className='yr';yr.textContent='Year '+d.x[i];t.appendChild(yr);
    d.s.forEach(s=>{const row=document.createElement('div');row.className='row';
      const k=document.createElement('span');k.className='key';k.style.background='var('+s.c+')';
      const v=document.createElement('strong');v.textContent=s.f(s.v[i]);
      const l=document.createElement('span');l.textContent=s.n;row.append(k,v,l);t.appendChild(row);});
    t.style.display='block';const cr=card.getBoundingClientRect();
    let left=ev.clientX-cr.left+14;if(left+t.offsetWidth>cr.width)left=ev.clientX-cr.left-t.offsetWidth-14;
    t.style.left=left+'px';t.style.top=(ev.clientY-cr.top-t.offsetHeight-10)+'px';}
  d.s.forEach(s=>{s.f=s.p?v=>(v*100).toFixed(0)+'%':v=>Number(v).toLocaleString(undefined,{maximumFractionDigits:s.dp})});
  ov.addEventListener('pointermove',show);ov.addEventListener('pointerleave',()=>{t.style.display='none';cross.style.display='none'});
});
document.querySelectorAll('[data-tile]').forEach(el=>{
  const card=el.closest('.card');const t=tip.cloneNode();card.appendChild(t);
  el.addEventListener('pointermove',ev=>{const g=ev.target.closest('[data-info]');if(!g){t.style.display='none';return}
    t.replaceChildren();g.dataset.info.split('|').forEach((line,j)=>{const div=document.createElement('div');
      if(j===0){div.className='yr'}div.textContent=line;t.appendChild(div)});
    t.style.display='block';const cr=card.getBoundingClientRect();
    let left=ev.clientX-cr.left+14;if(left+t.offsetWidth>cr.width)left=ev.clientX-cr.left-t.offsetWidth-14;
    t.style.left=left+'px';t.style.top=(ev.clientY-cr.top+14)+'px'});
  el.addEventListener('pointerleave',()=>{t.style.display='none'});
});
""".replace("%W%", str(W)).replace("%ML%", str(ML))


def _esc(s) -> str:
    return html.escape(str(s), quote=True)


def _nice_max(v: float) -> float:
    if v <= 0:
        return 1.0
    for step in (1, 2, 2.5, 5):
        for mag in (1, 10, 100, 1000, 10000):
            m = step * mag
            if m >= v:
                return float(m)
    return float(v)


def line_chart(title: str, hint: str, xs: list, series: list, y_max: float | None = None,
               percent: bool = False, area: bool = False, dp: int = 0) -> str:
    """series: [(name, values, css var)]"""
    n = len(xs)
    if n < 2:
        return ""
    top = y_max if y_max is not None else _nice_max(max(max(v) for _, v, _ in series) * 1.05)
    pw, ph = W - ML - MR, H - MT - MB
    dx = pw / (n - 1)

    def sy(v):
        return MT + ph - (v / top) * ph

    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{_esc(title)}" data-chart=\'{_esc(json.dumps({"x": xs, "dx": dx, "s": [{"n": nm, "v": [round(x, 3) for x in vals], "c": c, "p": percent, "dp": dp} for nm, vals, c in series]}))}\'>']
    for k in range(5):
        v = top * k / 4
        y = sy(v)
        parts.append(f'<line x1="{ML}" x2="{W - MR}" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--{"axis" if k == 0 else "grid"})" stroke-width="1"/>')
        label = f"{v * 100:.0f}%" if percent else (f"{v:,.0f}" if top >= 10 else f"{v:.1f}")
        parts.append(f'<text x="{ML - 6}" y="{y + 4:.1f}" text-anchor="end">{label}</text>')
    step = 10 if n <= 120 else 25 if n <= 300 else 100
    for i, x in enumerate(xs):
        if x % step == 0:
            parts.append(f'<text x="{ML + i * dx:.1f}" y="{H - 6}" text-anchor="middle">{x}</text>')
    for name, vals, c in series:
        pts = " ".join(f"{ML + i * dx:.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        if area:
            parts.append(f'<polygon points="{ML},{sy(0):.1f} {pts} {ML + (n - 1) * dx:.1f},{sy(0):.1f}" fill="var({c})" opacity="0.1"/>')
        parts.append(f'<polyline points="{pts}" fill="none" stroke="var({c})" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        lx, ly = ML + (n - 1) * dx, sy(vals[-1])
        parts.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4" fill="var({c})" stroke="var(--surface)" stroke-width="2"/>')
    parts.append(f'<line class="cross" x1="0" x2="0" y1="{MT}" y2="{MT + ph}" stroke="var(--axis)" stroke-width="1" style="display:none"/>')
    parts.append(f'<rect class="overlay" x="{ML}" y="{MT}" width="{pw}" height="{ph}" fill="transparent"/>')
    parts.append("</svg>")
    legend = ""
    if len(series) > 1:
        legend = '<div class="legend">' + "".join(
            f'<span><i class="key" style="background:var({c})"></i>{_esc(nm)}</span>' for nm, _, c in series) + "</div>"
    return (f'<div class="card"><h3>{_esc(title)}</h3><p class="hint">{_esc(hint)}</p>{legend}'
            + "".join(parts) + "</div>")


def map_svg(world) -> str:
    c = world.cfg
    cell = 18
    w, h = c.width * cell, c.height * cell
    people_at: dict = {}
    for p in world.living():
        people_at.setdefault(p.loc, []).append(p)
    out = [f'<svg viewBox="0 0 {w} {h}" data-tile="1" role="img" aria-label="Map of the world at the end of the run">',
           '<defs><pattern id="field" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<line x1="0" y1="0" x2="0" y2="5" stroke="var(--land)" stroke-width="1.6" opacity=".9"/></pattern></defs>']
    for row in world.tiles:
        for t in row:
            x, y = t.x * cell, t.y * cell
            here = people_at.get((t.x, t.y), [])
            names = ", ".join(q.name for q in here[:6]) + (f" +{len(here) - 6}" if len(here) > 6 else "")
            warmth = pile_warmth(t.pile) if t.pile else 0.0
            animals = sum(g["n"] for g in world.herds.get((t.x, t.y), ()))
            info = (f"Tile {t.x}, {t.y}|{t.biome}|fertility {t.fertility:.2f} · wild food {t.plants:.0f} · animals {animals:.0f}"
                    + (f"|growing from sown seed: {t.crop:.0f}" if t.crop >= 1 else "")
                    + (f"|a heap of {', '.join(f'{v:.0f} {k}' for k, v in t.pile.items())}, keeps out "
                       f"{warmth * 100:.0f}% of the cold" if t.pile else "")
                    + ("|a fire is burning" if t.fire > 0 else "")
                    + (f"|{sum(s[1] + s[2] for s in t.stash):.0f} food left here" if t.stash else "")
                    + (f"|{names}" if here else ""))
            out.append(f'<g data-info="{_esc(info)}">')
            if t.water:
                out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="var(--water)" opacity="0.9"/>')
            else:
                out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="var(--land)" '
                           f'opacity="{0.06 + 0.5 * t.fertility:.3f}"/>')
            if t.crop >= 5:
                out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="url(#field)"/>')
            if warmth >= 0.2:
                out.append(f'<rect x="{x + 2}" y="{y + 2}" width="6" height="6" rx="1" fill="var(--shelter)"/>')
            if t.fire > 0:
                out.append(f'<circle cx="{x + cell - 5}" cy="{y + 5}" r="3" fill="var(--s4)"/>')
            if here:
                r = 4 if len(here) < 4 else 5.5
                out.append(f'<circle cx="{x + cell / 2 + 2}" cy="{y + cell / 2 + 2}" r="{r}" fill="var(--s2)" '
                           f'stroke="var(--surface)" stroke-width="2"/>')
                if len(here) > 1:
                    out.append(f'<text x="{x + cell - 1}" y="{y + cell - 1}" text-anchor="end" '
                               f'style="font-size:8px;fill:var(--ink)">{len(here)}</text>')
            out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="transparent"/></g>')
    out.append("</svg>")
    legend = ('<div class="legend"><span><i class="dot" style="background:var(--land);opacity:.5"></i>land, darker is more fertile</span>'
              '<span><i class="dot" style="background:var(--water)"></i>sea and lakes</span>'
              '<span><i class="dot" style="background:var(--s2)"></i>people (number = how many)</span>'
              '<span><i class="dot" style="background:var(--shelter);border-radius:2px"></i>dwelling (a heap that keeps out cold)</span>'
              '<span><i class="dot" style="background:var(--s4)"></i>fire</span>'
              '<span><svg width="14" height="10"><rect width="14" height="10" fill="url(#field)"/></svg>sown ground</span></div>')
    return legend + "".join(out)


def write_report(world, historian, result: dict, path) -> None:
    m = result["metrics"]
    years = historian.years
    xs = [r["year"] + 1 for r in years]
    living = world.living()

    def tile(label, value, note=""):
        return (f'<div class="tile"><div class="label">{_esc(label)}</div><div class="value">{_esc(value)}</div>'
                + (f'<div class="note">{_esc(note)}</div>' if note else "") + "</div>")

    tiles = "".join([
        tile("Population", m["population_end"], f"peak {m['population_peak']}, from {world.cfg.founders} founders"),
        tile("Generations", m["max_generation"], "founders are generation 0"),
        tile("Births", m["births"], f"{(m['child_survival_to_16'] or 0) * 100:.0f}% of children reached 16"),
        tile("Killings", m["killings"], f"{m['revenge_acts']} acts of revenge, {m['feuds']} feuds"),
        tile("Inventions", len(m["firsts"]), "first blade, fire, dwelling, field…"),
        tile("Exchange partners", m["exchange_partnerships"], "unrelated pairs trading food"),
        tile("Settlements", m["settlements"], f"{m['bands_now']} bands at the end"),
    ])

    charts = []
    if len(xs) >= 2:
        charts.append(line_chart("Population", "People alive at the end of each year.", xs,
                                 [("population", [r["population"] for r in years], "--s1")], area=True))
        charts.append(line_chart("Births and deaths", "Per year.", xs,
                                 [("births", [r["births"] for r in years], "--s1"),
                                  ("deaths", [r["deaths"] for r in years], "--s2")]))
        charts.append(line_chart(
            "Who can make what",
            "Share of living people who know how to make each kind of thing. Nobody starts knowing any; "
            "the names are the historian's, given by what the thing can do.", xs,
            [(label, [r["know"][cls] / r["population"] if r["population"] else 0 for r in years], f"--s{i + 1}")
             for i, (cls, label) in enumerate((("blade", "sharp edge"), ("spear", "spear"),
                                               ("carrier", "carrier"), ("wrap", "warm wrap")))],
            y_max=1.0, percent=True))
        charts.append(line_chart(
            "What people have come to believe",
            "Share of living people who believe leaving seeds in the ground, heaping up materials, "
            "or leaving food somewhere is worth doing.", xs,
            [(label, [r["practice"][k] / r["population"] if r["population"] else 0 for r in years], f"--s{i + 1}")
             for i, (k, label) in enumerate((("sowing", "sow seeds"), ("building", "heap things up"),
                                            ("storing", "leave food")))],
            y_max=1.0, percent=True))
        charts.append(line_chart(
            "Things on the land", "Dwellings (heaps that keep out a fifth of the cold or more), sown ground, "
            "fires burning and food stores, counted at each year's end.", xs,
            [("dwellings", [r["dwellings"] for r in years], "--s1"),
             ("sown ground", [r["fields"] for r in years], "--s2"),
             ("fires", [r["fires"] for r in years], "--s3"),
             ("food stores", [r["stores"] for r in years], "--s4")]))
        charts.append(line_chart("Happiness", "Average mood of the living, 0 to 1.", xs,
                                 [("happiness", [r["mood"] for r in years], "--s3")], y_max=1.0, dp=2))
        charts.append(line_chart("Gifts and thefts", "Food given away vs. food stolen, per year.", xs,
                                 [("gifts", [r["gifts"] for r in years], "--s1"),
                                  ("thefts", [r["thefts"] for r in years], "--s2")]))

    deaths = Counter(m["deaths_by_cause"])
    top = max(deaths.values(), default=1)
    bars = "".join(
        f'<div class="row"><span>{_esc(k)}</span><div class="track"><div class="bar" style="width:{100 * v / top:.1f}%"></div></div>'
        f'<span class="n">{v}</span></div>' for k, v in deaths.most_common())

    chron = []
    year = None
    for e in historian.chronicle:
        if e["kind"] == "era":
            chron.append(f'<div class="era">{_esc(e["text"])}</div>')
            continue
        if e["year"] != year:
            year = e["year"]
            chron.append(f'<div class="year">Year {year}</div>')
        chron.append(f"<p>{_esc(e['text'])}</p>")

    bands = [b for b in historian.bands if b["missing"] == 0 and b["announced"]]
    band_html = "".join(
        f"<li>{_esc(b['name'][:1].upper() + b['name'][1:])}: {len(b['members'])} grown members, most respected: "
        f"{_esc(world.people[b['leader']].name)}</li>" for b in bands) or "<li>None right now.</li>"
    oral = historian.oral_history(world)
    oral_html = "".join(f"<li>{_esc(o['event'].capitalize())}: still told by {o['remembered_by']} living people</li>"
                        for o in oral) or "<li>No killings are remembered by anyone alive.</li>"

    elders = sorted(living, key=lambda p: p.birth)[:5]
    elder_html = "".join(
        f"<li>{_esc(p.name)}, {p.years(world.tick):.0f}, generation {p.generation}, "
        f"{sum(1 for c in p.children if world.people[c].alive)} living children, "
        f"knows how to make {len(p.recipes)} things, {len(p.memories)} memories</li>" for p in elders)

    rows = "".join(
        f"<tr><td>{r['year'] + 1}</td><td>{r['population']}</td><td>{r['births']}</td><td>{r['deaths']}</td>"
        f"<td>{r['generation']}</td><td>{r['pairs']}</td><td>{r['mood']:.2f}</td><td>{r['gifts']}</td>"
        f"<td>{r['thefts']}</td><td>{r['attacks']}</td><td>{r['killings']}</td><td>{r['dwellings']}</td>"
        f"<td>{r['fields']}</td><td>{r['fires']}</td><td>{r['stores']}</td><td>{r['weather']:.2f}</td></tr>" for r in years)
    table = ("<div class='tablewrap'><table><tr><th>Year</th><th>Pop.</th><th>Births</th><th>Deaths</th><th>Gen.</th>"
             "<th>Couples</th><th>Mood</th><th>Gifts</th><th>Thefts</th><th>Attacks</th><th>Killings</th>"
             "<th>Dwellings</th><th>Sown</th><th>Fires</th><th>Stores</th><th>Weather</th></tr>" + rows + "</table></div>")

    metric_rows = "".join(f"<tr><td>{_esc(k)}</td><td>{_esc(v)}</td></tr>" for k, v in m.items()
                          if not isinstance(v, dict))

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ACL seed {world.cfg.seed}</title><style>{CSS}</style></head><body><main>
<h1>Seed {world.cfg.seed}: {m['years']} years</h1>
<p class="sub">{world.cfg.founders} founders, one tick per week. Everything below was done by the people themselves; the historian only names it.</p>
<div class="tiles">{tiles}</div>
<h2>How the population lived</h2>
<div class="grid2">{"".join(charts[:2])}</div>
<div class="grid2">{"".join(charts[2:4])}</div>
<div class="grid2">{"".join(charts[4:6])}</div>
<div class="grid2">{"".join(charts[6:8])}</div>
<details><summary>Show the numbers as a table</summary>{table}</details>
<h2>The world at the end</h2>
<div class="grid2"><div class="card"><h3>Map</h3><p class="hint">Hover a tile for details.</p>{map_svg(world)}</div>
<div class="card"><h3>How people died</h3><p class="hint">All deaths over the whole run.</p><div class="bars">{bars}</div>
<h3 style="margin-top:20px">Bands</h3><ul class="plain">{band_html}</ul>
<h3 style="margin-top:20px">Oldest living</h3><ul class="plain">{elder_html}</ul>
<h3 style="margin-top:20px">Stories still told</h3><ul class="plain">{oral_html}</ul></div></div>
<h2>Chronicle</h2>
<div class="card chron">{"".join(chron) or "<p>Nothing notable happened.</p>"}</div>
<h2>Measurements</h2>
<div class="card"><table>{metric_rows}</table>
<p class="hint" style="margin-top:8px">State hash {result['state_hash'][:16]}… · event chain {result['event_chain'][:16]}…</p></div>
</main><script>{JS}</script></body></html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
