"""Build the project's public website (GitHub Pages) from the page texts below.

    python site/make_site.py [repo-name]     -> site/*.html, site/findings/*.html, sitemap.xml, robots.txt

The site describes the project and its findings in plain words and points to the code and to the book on Amazon. It
holds no book text. Every number on it comes from a findings file in experiments/ (named on each page).
"""
import json
from html import escape as html_escape
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
REPO = sys.argv[1] if len(sys.argv) > 1 else "artificial-civilization-laboratory"
BASE = f"https://abu4evere.github.io/{REPO}/"
GITHUB = f"https://github.com/abu4evere/{REPO}"
AMAZON = "https://www.amazon.com/dp/B0HNVKRLFL"
AMAZON_LIVE = True                  # live on Amazon since 22 October 2026
NAME = "Artificial Civilization Laboratory (ACL)"
AUTHOR = "Abdurashid Khudoyberdiev"
TODAY = date.today().isoformat()

NAV = [("index.html", "ACL"), ("findings/why-inventions-disappear.html", "Why inventions disappear"),
       ("findings/why-small-worlds-die-out.html", "Why small worlds die out"), ("method.html", "How it is tested"), ("book.html", "The book"), ("faq.html", "FAQ"),
       ("about.html", "About")]


def page(path, title, description, body, extra_ld=None):
    depth = path.count("/")
    up = "../" * depth
    
    nav_items = []
    for i, (href, label) in enumerate(NAV):
        cls = []
        if i == 0:
            cls.append("home")
        if path == href:
            cls.append("active")
        class_attr = f' class="{" ".join(cls)}"' if cls else ""
        nav_items.append(f'<a href="{up}{href}"{class_attr}>{label}</a>')
    nav = "".join(nav_items)
    
    ld = [{"@context": "https://schema.org", "@type": "ResearchProject", "name": "Artificial Civilization Laboratory",
           "alternateName": ["ACL", "Artificial Civilization Lab"], "url": BASE,
           "description": "An agent-based simulation of hunter-gatherer people in which nature is programmed and "
                          "culture is not, used to test how civilization and cumulative culture can emerge.",
           "founder": {"@type": "Person", "name": AUTHOR}, "sameAs": [GITHUB]}]
    if extra_ld:
        ld.append(extra_ld)
        
    resolved_body = body.replace("{up}", up)
    
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="A2cUnqQfhJHbxhupCtxqF2Zxo8TpFhgormO1F3wDHWM">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{BASE}{'' if path == 'index.html' else path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{'' if path == 'index.html' else path}">
<meta property="og:image" content="{BASE}img/share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="{up}img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{up}img/favicon-180.png">
<meta name="theme-color" content="#030509">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css?v=9">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0])}</script>
</head>
<body>
<header class="top"><nav>{nav}</nav></header>
<main>
{resolved_body}
</main>
<footer><div>Artificial Civilization Laboratory (ACL), by {AUTHOR}. Code and every experiment record:
<a href="{GITHUB}">GitHub</a>. The book: <a href="{up}book.html"><em>The World That Nobody Wrote</em></a>.</div></footer>
<script src="{up}sky.js?v=7" defer></script>
</body>
</html>
"""
    out = HERE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return path


BOOK_LD = {"@context": "https://schema.org", "@type": "Book", "name": "The World That Nobody Wrote, Part One",
           "alternativeHeadline": "How I Tried to Build a Civilization Instead of Simulating One",
           "author": {"@type": "Person", "name": AUTHOR}, "isbn": "9798163874385", "url": BASE + "book.html", "numberOfPages": 87,
           "about": "Artificial Civilization Laboratory", "sameAs": [AMAZON],
           "offers": {"@type": "Offer", "url": AMAZON, "availability": "https://schema.org/InStock"}}

INDEX = f"""<section class="hero">
<div class="scene"><canvas aria-hidden="true"></canvas></div>
<div class="mark">ACL</div>
<p class="sub">Artificial Civilization Laboratory</p>
<h1>Can a civilization begin from nothing?</h1>
<p class="lead">Twenty people wake up on a set of islands knowing nothing. No tools, no fire, no language, no rules.
Nobody writes their history. What do they build?</p>
<div class="btns"><a class="btn primary" href="{GITHUB}">See the code and records</a>
<a class="btn" href="book.html">The book</a></div>
</section>

<figure class="film"><video controls preload="none" playsinline poster="{{up}}img/scene_fire.jpg" width="1280" height="720">
<source src="{{up}}img/acl_film.mp4" type="video/mp4">
Your browser cannot play this video.</video>
<figcaption>The ACL film (2 min 44 s): what ACL is, and the question behind it. Sound on.</figcaption></figure>


<h2>What ACL is</h2>
<p>The Artificial Civilization Laboratory is an artificial civilization simulation: an agent-based world of
hunter-gatherers in which <strong>nature is programmed and culture is not</strong>. People have bodies, hunger, cold,
fear, love, grief, curiosity and memory. Stone can be struck, wood floats, seeds grow. There is no list of inventions,
no reward for being clever and no script. Whatever they come to make, believe or pass on, they find for themselves, and
they learn their habits by trial and error in their own lifetimes.</p>
<p>ACL uses no large language models. A model trained on human writing already knows what a village, a trade and a law
are; if its agents built one, nobody could tell whether civilization emerged or was remembered.</p>

<figure class="loop"><video autoplay muted loop playsinline preload="metadata" poster="{{up}}img/scene_link.jpg" width="1280" height="720" aria-label="Illustration: three figures joined by a dotted line of light"><source src="{{up}}img/scene_link.mp4?v=2" type="video/mp4"></video>
<figcaption>What one person learns can pass to another, or be lost with them.</figcaption></figure>

<h2>The question</h2>
<p>Can civilization emerge from nature alone, without anyone writing its history? And if it cannot yet, what exactly
stops it? ACL answers that one step at a time, with controlled experiments on hundreds of simulated worlds.</p>

<h2>What it has found so far</h2>
<div class="cards">
<div class="card"><span class="num">9 in 10</span><h3>Inventions die with their inventor</h3>
<p>About nine in ten useful inventions are never learned by anyone else. Many are forgotten within a season.</p>
<p><a href="findings/why-inventions-disappear.html">Why inventions disappear</a></p></div>
<div class="card"><span class="num">1 in 3</span><h3>Small worlds die out quietly</h3>
<p>Not from hunger or war: births stop decades earlier, because too few people can find a partner.</p>
<p><a href="findings/why-small-worlds-die-out.html">Why small worlds die out</a></p></div>
<div class="card"><span class="num">70+</span><h3>Studies, predictions locked first</h3>
<p>Every experiment is planned and frozen before it runs, and wrong predictions are kept in the record.</p>
<p><a href="method.html">How it is tested</a></p></div>
</div>

<div class="card latest"><span class="tag">Latest experiment · October 2026</span>
<h3>A kinder way to forget made things worse</h3>
<p>People could remember how to make only 12 things, so new inventions were pushed out within a season. In MR1 they instead
forgot only what they had not used for two years. New inventions were kept at first, but people ended up remembering
far less, and fewer inventions were passed on: about 8 in 100 instead of 11 in 100. By the rule fixed before the
run, the idea was rejected, and the wrong prediction stays in the record.</p>
<p><strong>Then:</strong> GR1 protected only a new invention's first season. Slightly more inventions were passed on, though most offered lessons still were not taken up.</p>
<p><a href="{GITHUB}/blob/master/experiments/MR1_memory_by_use/findings.md">Read the MR1 findings</a></p></div>

<h2>The book</h2>
<p><em>The World That Nobody Wrote, Part One: How I Tried to Build a Civilization Instead of Simulating One</em> tells
the story of the project: how the worlds were built, what their people did, and what was predicted wrong.
As a Kindle ebook and a paperback on Amazon.</p>
<div class="btns"><a class="btn primary" href="book.html">About the book</a></div>

<h2>Run a world yourself</h2>
<p>ACL is open source, in Python with no dependencies. The code, every frozen plan, every result and every correction
are on <a href="{GITHUB}">GitHub</a>.</p>
"""

INVENT = f"""<h1>Why inventions disappear in an artificial civilization</h1>
<p class="lead">ACL's people invent things from their first weeks: carriers, rafts, fired clay, a vessel that can hold
water. Yet almost none of it accumulates. Three studies traced where the chain breaks.</p>

<figure class="loop"><video autoplay muted loop playsinline preload="metadata" poster="{{up}}img/scene_steps.jpg" width="1280" height="720" aria-label="Illustration: four glowing steps in a row: seeds, seasons, a village, stories"><source src="{{up}}img/scene_steps.mp4?v=2" type="video/mp4"></video>
<figcaption>Every step has to be found, kept and passed on.</figcaption></figure>

<h2>The chain</h2>
<p>For a discovery to become part of a people's life, it has to be invented, be useful, be passed to someone else, be
kept, be built on, and be passed on again. ACL's chain audit followed every useful invention in dozens of replayed worlds
through those links.</p>

<h2>Where it breaks: the first hand-over</h2>
<div class="cards">
<div class="card"><span class="num">11% / 10%</span><p>of useful inventions were ever learned by anyone but their
inventor (two independent sets of worlds). About nine in ten first hand-overs were teaching.</p></div>
<div class="card"><span class="num">99%</span><p>of the inventions lost before any lesson were pushed out of the
inventor's memory within a season: a person can remember how to make twelve things, and a new invention starts out
valued at nothing.</p></div>
<div class="card"><span class="num">1 in 12</span><p>When something made from other made things could have been taught,
the listener knew how to make its parts about one time in twelve.</p></div>
</div>
<p>Four in five of the inventions never passed on were made by children, who play and invent the most. The ones that
did spread were held about five times as long and shown to about twice as many people.</p>

<h2>What comes next</h2>
<p>The next experiment changes, as a test of nature and not of history, how memory chooses what to forget and whether a
lesson can start with the parts of a craft. Its plan was frozen before any data.</p>
<p class="note">Sources in the repository: <code>experiments/CA1_chain_audit/findings.md</code>,
<code>experiments/CA2_teaching_gates/findings.md</code>, <code>experiments/CA3_opportunity/findings.md</code>.
Findings describe ACL's simulated worlds, not human history.</p>
"""

DIE = f"""<h1>Why small simulated societies die out</h1>
<p class="lead">In ACL's standard world, twenty founders on a 40 × 40 map, about a third of worlds die out within 120
years. Not in famine or war: in quiet.</p>

<figure class="loop"><video autoplay muted loop playsinline preload="metadata" poster="{{up}}img/scene_alone.jpg" width="1280" height="720" aria-label="Illustration: a lone figure standing on a dark horizon"><source src="{{up}}img/scene_alone.mp4?v=2" type="video/mp4"></video>
<figcaption>A world ends when too few people can find each other.</figcaption></figure>

<h2>Births stop first</h2>
<p>In every one of the 22 worlds that died out among 64 studied, births stopped 40 to 65 years before the end and the
people aged out. In the last 30 years, women of childbearing age had no partner in every single week. Worlds that would
die were identifiable decades ahead from their population at year 20.</p>

<h2>Search or size?</h2>
<p>A diagnostic experiment gave the same worlds perfect partner finding. Weeks without a partner fell from 55% to 11% and
deaths of worlds from 22 to 7. In the 7 that still died, single women had no eligible man anywhere at all: the pool was
simply empty. Both search and size matter.</p>

<h2>Smaller bands, more mixing, same loneliness</h2>
<p>With 80 founders, very few worlds die. Splitting the same 80 into 4, 8 or 16 bands did not change survival (13, 8 and
7 of 256 worlds died out, within chance). Smaller bands met far more: couples across different families rose from
6% to 54%. Yet the share of time women spent without a partner stayed at about 0.46, and births did not change. Meeting
more people was not the same as finding someone. A follow-up audit is now tracing where partner finding stops.</p>

<div class="scroll"><table>
<tr><th>founding bands</th><th>worlds died out (of 256)</th><th>couples across families</th><th>time without a partner</th></tr>
<tr><td>4 × 20</td><td>13</td><td>6%</td><td>0.455</td></tr>
<tr><td>8 × 10</td><td>8</td><td>29%</td><td>0.461</td></tr>
<tr><td>16 × 5</td><td>7</td><td>54%</td><td>0.466</td></tr>
</table></div>
<p class="note">Sources in the repository: <code>experiments/F1_baseline_fragility/findings.md</code>,
<code>experiments/F2_perfect_search/findings.md</code>, <code>experiments/MB1_multi_band/findings_mb1b.md</code>.
Absolute shares depend on settings that are not anchored to real data (sight, reach, mortality); comparisons within a
study stand.</p>
"""

METHOD = f"""<h1>How ACL tests itself</h1>
<p class="lead">Most simulations can tell you what happened. ACL tries to say what caused it, and to keep its creator
from quietly writing the answer in.</p>
<h3>Predictions are written down and frozen before any data</h3>
<p>Every study has a plan, a prediction and a line that would mean the prediction was wrong. The plan is frozen and
tagged in the repository before code or data. Wrong predictions stay in the record.</p>
<h3>Many worlds, side by side</h3>
<p>One world can do almost anything. Every comparison runs the same starting worlds under both sets of rules, often 256
of each, and a difference has to hold across them. Results are checked on a second, unseen set where possible.</p>
<h3>Exact replay</h3>
<p>The simulation is deterministic: any world can be replayed exactly, down to its final state. Instruments that watch a
world are checked to change nothing in it.</p>
<h3>Nature only</h3>
<p>Only nature is programmed: bodies, needs, materials, seasons. Changes to nature need a written case and evidence about
the real world. Nothing is rewarded for being cultural, and no agent is told what to invent.</p>
<h3>Corrections in the open</h3>
<p>Mistakes are corrected beside the original, never over it, and every number traces to a committed script.</p>
<p class="note">The full list of studies, with predictions and results: <a href="{GITHUB}/blob/master/experiments/INDEX.md">experiments/INDEX.md</a>.</p>
"""

ABOUT = f"""<h1>About ACL</h1>
<p>The Artificial Civilization Laboratory is built by {AUTHOR}. It began as an idea for a personal AI companion and
turned into a bigger question: what would it take for a civilization to start by itself?</p>
<p>The project is open source. Its code, plans, results and corrections are public on
<a href="{GITHUB}">GitHub</a>. Its story is told in the book <a href="book.html"><em>The World That Nobody Wrote</em></a>.</p>
"""


CONTENTS = ["Prologue — The Vessel", "Before You Begin",
            ("Part I — The Dream", ["Why I Built a World", "Games That Already Know the Answer", "What Would Count as Success"]),
            ("Part II — The Rules I Gave Myself", ["Nature, Not History", "A World That Doesn't Care", "Where I Fell Short"]),
            ("Part III — What Happened", ["The First Worlds Come Alive", "A Thousand Years, and the Freeze", "Slowly Forgetting",
                                         "Why Nobody Bothers", "Winter, and the Planners", "Where the Food Goes"]),
            ("Part IV — Finding Each Other", ["The Worlds That Grew Old", "A Place to Come Home To", "One Band Alone",
                                              "What They Know, and Who They Are"]),
            ("Part V — What My Worlds Taught Me", ["A Chain, Not a Spark", "How I Keep Myself Honest",
                                                   "Questions Bigger Than My World"]),
            ("Part VI — The Road Ahead", ["The Minimum Conditions"]), "Epilogue — The End of the Beginning"]


def contents_html():
    out, n = ["<ul>"], 0
    for item in CONTENTS:
        if isinstance(item, str):
            out.append(f"<li>{item}</li>")
            continue
        part, chs = item
        items = []
        for ch in chs:
            n += 1
            items.append(f"<li>{n}. {ch}</li>")
        out.append(f"<li>{part}<ul>{''.join(items)}</ul></li>")
    return "".join(out) + "</ul>"


BUY = (f'<div class="btns"><a class="btn primary" href="{AMAZON}">Buy on Amazon</a></div>' if AMAZON_LIVE else
       '<p class="note">In review at Amazon (Kindle and paperback); the store link appears here as soon as it is live.</p>')

BOOK = f"""<h1>The World That Nobody Wrote</h1>
<p class="lead">Part One: How I Tried to Build a Civilization Instead of Simulating One</p>
<div class="bookrow">
<img class="cover" src="{{up}}img/book_cover.jpg" alt="Cover of The World That Nobody Wrote, Part One" width="600" height="900">
<div>
<p>Twenty people wake up in a world knowing nothing. No language, no tools, no idea how to survive. Nobody tells them
what to do. All they have is nature: hunger, cold, seasons, plants, water, and each other.</p>
<p><em>The World That Nobody Wrote</em> is the story of the Artificial Civilization Laboratory, a simulated world built
to ask one question: can a civilization start by itself, from nothing?</p>
<p>In its worlds, people tied a raft in their first weeks and almost never used it. Someone named Reibik made a vessel
that could hold water and never once filled it. Whole worlds ended, not in war but in quiet, because too few people could
find each other.</p>
<p>Part One tells what happened, what was predicted wrong, and the questions it raised: about memory, about who a
person is, and about what it means for a world to have a creator.</p>
{BUY}
</div></div>
<h2>Details</h2>
<div class="scroll"><table>
<tr><th>Author</th><td>{AUTHOR}</td></tr>
<tr><th>Formats</th><td>Kindle ebook, paperback (6 × 9 in, 87 pages)</td></tr>
<tr><th>Paperback ISBN</th><td>979-8-16-387438-5</td></tr>
<tr><th>Chapters</th><td>20, with a prologue, an epilogue and eight illustrations</td></tr>
</table></div>
<h2>Contents</h2>
{contents_html()}
<p class="note">Every number in the book comes from the project's experiment records, which are public on
<a href="{GITHUB}">GitHub</a>. Cover and illustrations are AI-generated images made for the book.</p>
"""

FAQ_ITEMS = [
    ("What is the Artificial Civilization Laboratory (ACL)?",
     "The Artificial Civilization Laboratory (ACL) is an agent-based simulation of hunter-gatherers in which nature is "
     "programmed and culture is not. Simulated people have bodies, needs, kinship, feelings and materials to work with, "
     "but no list of inventions, no reward for inventing and no language model. ACL tests whether culture and "
     "civilization can emerge from nature alone, and what stops them when they do not."),
    ("Who built ACL?",
     f"ACL is built by {AUTHOR}. The code and every experiment record are on GitHub; the story of the project is told "
     "in the book The World That Nobody Wrote."),
    ("Does ACL use large language models?",
     "No. A language model trained on human writing already knows what a village, a trade or a law is, so if its agents "
     "built one it would be impossible to tell emergence from recall. ACL's people learn by trial and error and from "
     "each other, inside the simulation."),
    ("What has ACL found so far?",
     "About nine in ten useful inventions are never learned by anyone except their inventor; many are "
     "lost from a limited memory before any chance to teach. About a third of small worlds (20 founders) die out, not "
     "from famine or war, but because too few people find a partner. Teaching a learner the missing part of a "
     "complex invention after a failed lesson raised how much was passed on; fixing an accident in how memory chose "
     "what to forget did not."),
    ("How does ACL keep its results honest?",
     "Every study's plan and prediction are written down and frozen in the repository before any code or data. Hundreds "
     "of worlds are compared side by side, the simulation replays exactly, instruments are checked to change nothing, "
     "and wrong predictions are kept in the record."),
    ("Is ACL a model of real human history?",
     "No. ACL is a model. It produces candidate explanations precise enough to test, compared with evidence about real "
     "foragers where possible, but it does not show how real societies worked."),
    ("Is ACL open source?",
     "The code is public on GitHub so anyone can read it and follow every experiment. It is not under an open-source "
     "licence: all rights are reserved by the author."),
    ("Where can I read more?",
     "The findings pages on this site, the experiment index in the GitHub repository, and the book The World That "
     "Nobody Wrote, Part One (Kindle and paperback, on Amazon: amazon.com/dp/B0HNVKRLFL)."),
]
FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_ITEMS]}
FAQ = "<h1>Questions about the Artificial Civilization Laboratory</h1>\n" + "\n".join(
    f"<h3>{html_escape(q)}</h3>\n<p>{html_escape(a)}</p>" for q, a in FAQ_ITEMS)

pages = [
    page("index.html", "Artificial Civilization Laboratory (ACL) — an artificial civilization simulation",
         "The Artificial Civilization Laboratory (ACL) is an artificial civilization simulation where nature is "
         "programmed and culture is not. Can civilization emerge without anyone writing its history?", INDEX, BOOK_LD),
    page("findings/why-inventions-disappear.html", "Why inventions disappear — Artificial Civilization Laboratory",
         "In ACL's artificial civilization, nine in ten useful inventions are never learned by anyone else. "
         "Three experiments traced why.", INVENT),
    page("findings/why-small-worlds-die-out.html", "Why small simulated societies die out — Artificial Civilization Laboratory",
         "A third of ACL's small worlds die out, not from hunger or war but because too few people find a partner. "
         "What the experiments show.", DIE),
    page("method.html", "How ACL tests itself — Artificial Civilization Laboratory",
         "Frozen predictions, many worlds side by side, exact replay and corrections in the open: the method of the "
         "Artificial Civilization Laboratory.", METHOD),
    page("book.html", "The World That Nobody Wrote — the book of the Artificial Civilization Laboratory",
         "The World That Nobody Wrote, Part One, by Abdurashid Khudoyberdiev: the story of the Artificial Civilization "
         "Laboratory (ACL), a simulated world where civilization has to emerge on its own.", BOOK, BOOK_LD),
    page("faq.html", "FAQ — Artificial Civilization Laboratory (ACL)",
         "What is the Artificial Civilization Laboratory (ACL)? Answers about the artificial civilization simulation, "
         "who built it, what it has found and how it is tested.", FAQ, FAQ_LD),
    page("about.html", "About — Artificial Civilization Laboratory (ACL)",
         f"The Artificial Civilization Laboratory (ACL), built by {AUTHOR}.", ABOUT),
]
(HERE / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE}{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod></url>\n"
              for p in pages) + "</urlset>\n", encoding="utf-8")
(HERE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
(HERE / ".nojekyll").write_text("", encoding="utf-8")
LLMS = [
    "# Artificial Civilization Laboratory (ACL)",
    "",
    f"> An agent-based simulation of hunter-gatherers in which nature is programmed and culture is not, built by "
    f"{AUTHOR}. No list of inventions, no reward for inventing, no language models. It tests whether culture and "
    "civilization can emerge from nature alone, and what stops them.",
    "",
    "Key findings: about nine in ten useful inventions are never learned by anyone but their inventor; about a third of "
    "small worlds die out because too few people find a partner; teaching the missing part after a failed lesson "
    "raises transmission. Every study is planned and frozen before it runs; wrong predictions are kept.",
    "",
    "## Pages",
    "",
    f"- [Home]({BASE}): what ACL is and the main findings",
    f"- [Why inventions disappear]({BASE}findings/why-inventions-disappear.html)",
    f"- [Why small worlds die out]({BASE}findings/why-small-worlds-die-out.html)",
    f"- [How ACL tests itself]({BASE}method.html)",
    f"- [FAQ]({BASE}faq.html)",
    f"- [The book: The World That Nobody Wrote]({BASE}book.html), on Amazon: {AMAZON}",
    "",
    "## Source",
    "",
    f"- [Code and every experiment record]({GITHUB}) (public; all rights reserved)",
]
(HERE / "llms.txt").write_text(chr(10).join(LLMS) + chr(10), encoding="utf-8")
print("built", len(pages), "pages for", BASE)
