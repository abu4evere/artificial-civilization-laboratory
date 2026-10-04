"""Build the World Bible v8 DRAFT from the creator's v7.1 file.

Chapters 1-7 are copied unchanged (v7.1 §6: frozen, do not edit). Only the v7.1 amendment
layer and the closing status are replaced, using the book's own paragraph formatting.

Usage: python bible/build_v8.py  (writes bible/THE_ARTIFICIAL_CIVILIZATION_World_Bible_v8_DRAFT.docx)
"""
from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
SRC = Path(r"C:\Users\User\Downloads\THE_ARTIFICIAL_CIVILIZATION_World_Bible_v7.1.docx")
OUT = HERE / "THE_ARTIFICIAL_CIVILIZATION_World_Bible_v8_DRAFT.docx"


def run(text, b=False, i=False, size=22, color=None):
    props = ("<w:b/><w:bCs/>" if b else "") + ("<w:i/><w:iCs/>" if i else "")
    props += f'<w:color w:val="{color}"/>' if color else ""
    props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def h1(text):
    return ('<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:spacing w:after="180" w:before="360"/></w:pPr>'
            + run(text, b=True, size=30) + "</w:p>")


def h2(text):
    return ('<w:p><w:pPr><w:pStyle w:val="Heading2"/><w:spacing w:after="140" w:before="280"/></w:pPr>'
            + run(text, b=True, size=24) + "</w:p>")


def body(*runs_, align="left", after=140):
    return f'<w:p><w:pPr><w:spacing w:after="{after}"/><w:jc w:val="{align}"/></w:pPr>{"".join(runs_)}</w:p>'


def p(text, **kw):
    return body(run(text, **kw))


def lead(bold, rest):
    """A paragraph that starts with a bold phrase."""
    return body(run(bold, b=True), run(rest))


def bullet(text, bold=None):
    inner = (run(bold, b=True) if bold else "") + run(text)
    return (f'<w:p><w:pPr><w:spacing w:after="60"/><w:ind w:left="360"/></w:pPr>'
            f'{run("• ")}{inner}</w:p>')


def center(text, b=True, i=False, size=22):
    return body(run(text, b=b, i=i, size=size), align="center")


def law(title, statement, why, not_scripted):
    return [
        body(run(title, b=True, size=23), after=80),
        p(statement),
        body(run("Why: ", b=True), run(why), after=60),
        body(run("Does not script: ", b=True), run(not_scripted), after=200),
    ]


V8 = []
add = V8.extend

add([
    h1("VERSION 8 — LAWS FROM THE FIRST RUNS"),
    p("Chapters 1–7 stay frozen and are not edited. As v7.1 §6 requires, this layer replaces v7.1: it keeps "
      "v7.1’s working rules, records what the first experiments taught, and adds the laws those experiments "
      "showed the world needs.", i=True),
    p("DRAFT for the creator’s approval. It becomes v8.0 when approved. Until then v7.1 stands, and every place "
      "the code goes beyond v7.1 is listed in IMPLEMENTATION_STATUS.md.", b=True, color="8A1C1C"),

    h2("1. The runs"),
    p("Experiment 0 (E0) built the decision interface and the Surprise Log. Experiment 1 (E1) ran 8 worlds for up "
      "to 200 years each with every feature frozen. A second pass with read-only recorders reproduced all 8 "
      "histories exactly. Experiment 2 (E2) runs the same 8 worlds again under the laws this layer adds. "
      "Predictions and kill criteria were written down before each run."),

    h2("2. What the runs taught (findings, not laws)"),
    bullet("Building (heaping materials against the cold) held as a shared practice for about 190 years in 7 of 8 "
           "worlds and produced real dwellings. A killing in year 20 was still remembered 180 years later by 62 "
           "people across 5 generations, though by then most of them blamed the wrong person.",
           "Culture appears without being scripted. "),
    bullet("Gifts of food caused 78% of all movement in trust; tested claims caused 3%. Only about 5 claims were "
           "tested per world-year, and being right was luck (split-half r = 0.03). The chain of Law 92 never started.",
           "Trust followed food, not truth. "),
    bullet("Sowing beliefs persisted while sowing died out, because the crop mostly fed others: a sower got back "
           "0.17–0.41 food per seed sown, against 1 for eating it.",
           "A belief can outlive its practice. "),
    bullet("Rafts were invented within weeks in every world, but almost nobody carried one. Floating was never "
           "felt to be useful.", "Knowing is not using. "),
    bullet("People could cross water up to 3 tiles wide on foot, and 92% of all crossings between islands were "
           "such jumps. Islands isolated their bands only where the water was wider.",
           "A gap in physics decided history. "),
    bullet("14 of the 54 possible first steps already make a named kind of thing. Where invention was hard, the "
           "limit was materials (hide for a wrap) or depth (a blade before a spear), not thresholds.",
           "First inventions are one random step away. "),
    bullet("Marks became shared symbols in every world (763 in all). Most stood for places (water, shelter, "
           "graves), and many drifted in meaning.", "Meaning formed, and drifted. "),

    h2("3. How frozen laws are read (the frozen text is unchanged)"),
    bullet("A year is 52 weeks of 7 days (364 days). Agents decide once a week; the observer’s clock shows hours "
           "and days.", "Rule 1, the calendar. "),
    bullet("A journey passes through every place on the way. Water anywhere on the way stops anyone without "
           "something that floats.", "Rule 3, space is crossed, not skipped. "),
    bullet("Words shown to the observer (speech, thoughts) translate real states for the observer. They are never "
           "the agents’ knowledge or language.", "Rule 13 and Law 22, rendering is not language. "),
    bullet("Bodies need fresh water. It is found in places (rivers, lakes) and, for a while, after rain. Sea water "
           "does not quench thirst, and no agent knows that until experience shows it.",
           "Rule 14, thirst is physical. "),
    bullet("“Demonstrated success” is each receiver’s own record of how a source’s word has held. It is never a "
           "number the world assigns.", "Law 92, judged by the receiver. "),

    h2("4. New laws"),
    p("Each was found necessary by a run. Each creates a condition; none names an outcome."),
])
add(law("LAW 121 — Reality Must Be Checkable",
        "The world must give agents frequent and consistent chances to compare what they were told, or believe, "
        "with what happens. Claims that can never be checked cannot earn authority. Where little can be checked, "
        "trust follows goodwill instead of truth.",
        "E1 tested about 5 claims per world-year, and accuracy had no relation to trust (r = −0.07).",
        "which claims are true, or who comes to be trusted."))
add(law("LAW 122 — Credibility Is Earned by Record",
        "Every agent keeps its own record of whose word has held. As that record grows, it counts for more than "
        "goodwill in deciding what to believe. Agents may tell each other whose word holds; the listener weighs "
        "that like any other claim (Law 91).",
        "In E1 nobody could recognise an expert.",
        "experts, authority or institutions."))
add(law("LAW 123 — Doing Leaves Traces",
        "Acting on the world changes the place where it is done: turned earth, flakes of struck stone, ash, "
        "bones. Traces are physical. Anyone who comes by can perceive them, and they fade. They are not messages.",
        "Without traces, nobody could learn from what others did unless they saw it happen.",
        "what anyone makes of a trace."))
add(law("LAW 124 — Uses Must Be Experienced",
        "What a thing is good for is learned only from outcomes an agent experiences or sees: reaching land a "
        "raft made reachable, carrying more, keeping warm. The creator never tells agents what a thing is for, "
        "but the world must let every real use be felt.",
        "In E1 rafts were known everywhere and valued nowhere, because floating was never felt.",
        "which uses are found."))
add(law("LAW 125 — Records Can Be Sources",
        "A durable mark can be a source, like a person. An agent who has come to link a mark with a thing or a "
        "practice may read it as a claim, and keeps a record of how marks have held, as with people (Laws 52, "
        "56, 81, 115).",
        "It lets knowledge outlive the people who held it, without assigning any meaning (Law 22).",
        "which marks mean what, or that writing appears."))
add([
    h2("5. Mechanisms now enforced (the v7.1 §3 audit, updated)"),
    p("Every emergent law must name at least one enforced mechanism. The full audit is IMPLEMENTATION_STATUS.md. "
      "The first runs added these:"),
    bullet("wet and dry years, weekly rain, storms, floods, hard winters, cold that depends on place and season, "
           "thirst, salt water.", "Rules 8 and 14: "),
    bullet("animal species that each share one mind; a food chain; fear of animals learned from harm, from "
           "seeing it and from stories.", "Rule 9: "),
    bullet("marks start meaningless; a link counts only if the mark goes with a thing more often than that thing "
           "is around anyway.", "Laws 22–23: "),
    bullet("retelling changes stories; the observer records false versions against the truth.",
           "Laws 25–26, 51, 80: "),
    bullet("the listener decides; hearsay is kept apart from what was tested; being proved wrong counts more "
           "than being proved right.", "Laws 56, 61, 66, 84, 91–92: "),
    bullet("a surprise opens a puzzle; puzzles and claims taken on draw agents to test again.", "Laws 63–65: "),
    bullet("attention, focus and overthinking.", "Law 95: "),
    bullet("track records; reports of water and animals checked on sight; traces; crossings that give a raft its "
           "worth; marks read as claims.", "Laws 121–125: "),

    h2("6. The creator’s method (replaces v7.1 §§4–7)"),
    bullet("Before any experiment, predictions are written and frozen. Afterwards each is scored as confirmed, "
           "wrong or unclear.", "M1, predictions first. "),
    bullet("Every experiment states, before it runs, what would show it failed.", "M2, kill criterion. "),
    bullet("While an experiment runs, no feature changes. Only read-only measurement is added.",
           "M3, freeze during experiments. "),
    bullet("A recorder must leave the history identical. This is proven by comparing the full world state with "
           "a run without the recorder.", "M4, measurement never touches the world. "),
    bullet("Compare across seeds. One history proves nothing.", "M5, many worlds. "),
    bullet("Every feature lists the laws it implements and the laws it violates or only partly honours.",
           "M6, law accounting. "),
    bullet("Before building a major system, ask whether it creates conditions or scripts outcomes. If it "
           "scripts outcomes, it is not built.", "M7, conditions, not outcomes. "),
    bullet("When the code needs a rule the Bible lacks, the Bible is amended first, in the next version. "
           "Departures are recorded, never hidden.", "M8, the Bible comes first. "),
    bullet("The Surprise Log, the historian and the experiment measurements form one read-only observer layer "
           "(Observer Layer v1). No parallel systems (v7.1 §5).", "M9, one observer layer. "),

    h2("7. Departures to resolve"),
    bullet("Laws 121–125 were built into the code on 2026-10-03, before this draft existed, so M8 was not "
           "followed. If the creator approves this draft, they are regularised; if not, they are removed."),
    bullet("The experiment measurements (acl/measure.py) still run beside the Surprise Log, not inside it "
           "(M9, v7.1 §5)."),
    bullet("Chapter 1, Part IV names requests, warnings, plans, lies and promises as things communication "
           "carries. Requests, plans, lies and promises have no mechanism yet."),
    bullet("Speech bubbles are an English rendering (section 3); the agents have no language yet."),

    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
    h1("Status of the World Bible"),
    p("Foundational chain (frozen):", b=True),
    center("Reality → Culture → Knowledge → Discovery → Information → Influence → Power → Creation"),
    p("v8 adds the conditions that let truth be checked, credibility be earned, uses be felt, and knowledge be "
      "left behind in the world."),
    p("Still intentionally unscripted: government, religion, economy, formal law, modern science, warfare, "
      "education, markets, nations, trade, and language. All remain possible under the laws."),
    p("Versioning: v1–7 frozen. v8 replaces v7.1 once approved. v9 will come from what E2 and later runs teach."),
    body(run("“The creator writes the laws of the universe, not the history.”", b=True, i=True, size=24),
         align="center"),
    center("Build the world. Start the clock. Let them live."),
])


def main():
    work = HERE / "_v8_build"
    if work.exists():
        shutil.rmtree(work)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(work)
    doc = work / "word" / "document.xml"
    x = doc.read_text(encoding="utf-8")
    paras = list(re.finditer(r"<w:p[ >].*?</w:p>", x, re.S))

    def text(m):
        return "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", m.group(0), re.S))
    start = next(m for m in paras if text(m).startswith("VERSION 7.1"))
    end = paras[-1]
    x = x[:start.start()] + "".join(V8) + x[end.end():]
    x = x.replace(">Version 7.1<", ">Version 8.0 — DRAFT<")
    x = re.sub(r">Chapters 1.7 Frozen  \+  Thin Runnable Amendment Layer<",
               ">Chapters 1–7 Frozen  +  Laws From the First Runs (replaces v7.1)<", x)
    doc.write_text(x, encoding="utf-8")
    head = work / "word" / "header1.xml"
    head.write_text(head.read_text(encoding="utf-8").replace("World Bible v7.1", "World Bible v8 (draft)"),
                    encoding="utf-8")
    from xml.dom import minidom
    for f in ("word/document.xml", "word/header1.xml"):
        minidom.parse(str(work / f))          # well-formed, or this raises
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(SRC) as src, zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as out:
        for item in src.infolist():          # same files, same order as the creator's book
            out.write(work / item.filename, item.filename)
    shutil.rmtree(work)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
