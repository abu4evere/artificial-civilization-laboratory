"""Rebuild E1's simulation code by undoing, in reverse order, the four changes made after E1
(P1 reputation, P2 testing, P3 records, P4 floating/water). The copy goes to code_e1/acl.

Only modules that decide what happens are reverted. Read-only modules (historian, measure, mindview,
stage, viewer) stay current. The rebuilt code is trusted only if it reproduces E1's saved year-100
states exactly (see verify in forensics.py).
"""
from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "acl"
DST = HERE / "code_e1" / "acl"
SCRATCH = Path(r"C:\Users\User\AppData\Local\Temp\claude\C--Users-User-council\ba63843e-e840-4d40-b6c8-d492a2d2504a\scratchpad")
SIM = {"world.py", "actions.py", "mind.py", "information.py", "knowhow.py", "marks.py", "weather.py",
       "fauna.py", "thought.py"}


def pairs_of(script: Path) -> list:
    """The (file, old, new) replacements a patch script made, without running its writes."""
    found = []
    src = script.read_text(encoding="utf-8").replace(r'Path(r"D:\acl\acl")', "Path(_TMP)")
    ns = {"_TMP": tempfile.mkdtemp()}

    def patch(name, prs):
        for old, new in prs:
            found.append((name, old, new))
    # run with our own patch() in place of the script's
    src = re.sub(r"\ndef patch\(name, pairs\):.*?\n\n\n", "\n", src, flags=re.S)
    exec(compile(src, str(script), "exec"), {**ns, "patch": patch, "Path": Path})
    return found


def main():
    if DST.parent.exists():
        shutil.rmtree(DST.parent)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
    files = {p.name: p.read_text(encoding="utf-8") for p in DST.glob("*.py")}

    def undo(name, old, new):
        if name not in SIM:
            return
        s = files[name]
        assert new in s, f"{name}: cannot find\n{new[:200]}"
        files[name] = s.replace(new, old, 1)

    def undo_all(script):
        removed = {}
        for name, old, new in reversed(pairs_of(SCRATCH / script)):
            if new == "":
                removed.setdefault(name, []).append(old)     # a later step deleted this; it goes back with its block
                continue
            for gone in removed.get(name, []):
                if gone in new and new not in files[name]:
                    new = new.replace(gone, "")
            undo(name, old, new)

    # P4, then P3, then P2 (with its two hand fixes first), then P1.
    for script in ("patch_p4.py", "patch_p3.py"):
        undo_all(script)
    # P2's hand fixes, undone so P2's own text is back in place
    undo("mind.py", '''    for key, h in p.heard.items():
        if key[:2] == "g:":
            spot = tuple(int(v) for v in key[2:].split(","))
            if distance(p.loc, spot, w, h_) <= c.reach and spot not in tiles:''', '''    for key in p.heard:
        if key[:2] == "g:":
            spot = tuple(int(v) for v in key[2:].split(","))
            if distance(p.loc, spot, w, h) <= c.reach and spot not in tiles:''')
    undo("mind.py", "d = distance(p.loc, spot, w, h_)", "d = distance(p.loc, spot, w, h)")
    undo("information.py", 'listener.loc, place=key, how="told")', 'listener.loc, spot=key, how="told")')
    undo_all("patch_p2.py")
    # P1
    s = files["information.py"]
    a, b = s.index("MAX_RECORDS = 40"), s.index("# --- stories ---")
    files["information.py"] = s[:a] + P1_OLD + s[b:]
    undo("actions.py", '''    if q.age(world.tick) >= 52 * 3 and world.rng.random() < 0.3 + 0.4 * h["sociability"]:
        social.gossip(world, q, p)''', '''    if q.age(world.tick) >= 52 * 3 and world.rng.random() < 0.3 + 0.4 * h["sociability"]:
        social.gossip(world, q, p)
    # Who has turned out right, and who wrong.
    if q.age(world.tick) >= 52 * 6:
        information.share_reputation(world, p, q)''')
    for name, text in files.items():
        (DST / name).write_text(text, encoding="utf-8")
    print("rebuilt", DST)


P1_OLD = '''def credence(world, listener, speaker, about: str = "", evidence: float = 0.0) -> float:
    """How far `listener` believes what `speaker` says, 0 .. 1. Reads only what the listener
    feels, knows and can see: never the speaker's mind."""
    r = listener.rel.get(speaker.id)
    trust = r.trust if r else 0.0
    respect = r.respect if r else 0.0
    c = 0.35 + 0.45 * max(trust, 0.0) - 0.6 * max(-trust, 0.0) + 0.2 * respect
    # The young believe the grown-ups around them.
    tick = world.tick
    if listener.age(tick) < CHILD_END and speaker.age(tick) >= CHILD_END:
        c += 0.2
    # Someone who visibly does well is easier to believe (demonstrated success).
    c += 0.25 * (speaker.health / 100.0 - 0.7) - (0.1 if speaker.starving else 0.0)
    c += evidence
    # Fear makes stories of harm and danger easier to believe.
    if about in HARM or about == "mauled":
        c += 0.25 * listener.fear
    # A mind full of something else takes in less.
    if thought.state(listener) == "overthinking":
        c *= 0.6
    return clamp(c)


def tested(world, p, hkey: str, outcome: float) -> None:
    """p's own experience has now tested something they were told (key "b:..." or "m:...").
    Whoever told them is believed more if it held, and less if it did not."""
    h = p.heard.pop(hkey, None)
    if h is None:
        return
    claim = h[0]
    held = (outcome > 0.05 and claim > 0) or (outcome <= 0.05 and claim <= 0)
    for src in h[1]:
        if src != p.id:
            bump(p, src, world.tick, trust=0.06 if held else -0.1)
    world.emit("verified" if held else "refuted", p.id, None, p.loc, claim=hkey, by=list(h[1]))


'''

if __name__ == "__main__":
    main()
