"""Read the minds of the grown people in one world on the live nature (v11), read-only, for the brain scan v2.

Per person and week: what the old brain scan showed (situation lit, the 32 x 19 habit table, options weighed and
their instinct/habit split, body, feelings, temperament) plus the parts of the mind it left out: memories, know-how,
beliefs, puzzles (surprises being tested), whom they trust, what they heard and have not tried, what is on their mind.
Uses the viewer's own read functions; nothing in acl/ is written.
  python design/brain_v11/brain_data_v11.py [seed] [start_year] [weeks] [out.json]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402
from acl import mindview  # noqa: E402
from acl.viewer import _brain, _memory_words  # noqa: E402
from acl.historian import CLASSES, classify  # noqa: E402

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 501
START = int(sys.argv[2]) if len(sys.argv) > 2 else 30
WEEKS = int(sys.argv[3]) if len(sys.argv) > 3 else 26
OUT = Path(sys.argv[4]) if len(sys.argv) > 4 else Path(__file__).with_name("brain_data_v11.json")
WPY = 52
MAX_MEM = 60  # memory store size, docs/ODD_v11.md

w = World(Config(seed=SEED))
for _ in range(START * WPY):
    w.step()
names, frames = {}, []
for week in range(WEEKS):
    w.step()
    tick = w.tick
    people = []
    for p in w.living():
        if p.stage(tick) not in ("child", "teen", "adult", "elder"):
            continue
        names[p.id] = p.name
        b = _brain(w, p)
        m = mindview.mind(w, p)
        mems = sorted(p.memories, key=lambda x: -(x.salience * x.strength))
        makes = []
        for sig in sorted(p.recipes, key=lambda s: -p.itemval.get(s, 0.0)):
            cls = classify(w.knowledge.get(sig, {}).get("props"))
            makes.append([CLASSES[cls[0]][1] if cls else "something of their own devising",
                          round(p.itemval.get(sig, 0.0), 2)])
        people.append({
            "id": p.id, "name": p.name, "sex": p.sex, "age": round(p.years(tick), 1), "stage": p.stage(tick),
            "ctx": b["ctx"], "chosen": b["chosen"], "decides": b["decides"], "q": b["q"], "valued": b["valued"],
            "weighed": b["weighed"], "body": b["body"], "genes": b["genes"],
            # memory: every memory as [strength, salience, valence, told(1)/lived-or-seen(0)], and the top six in words
            "mem": [[round(x.strength, 2), round(x.salience, 2), round(x.valence, 2), int(bool(x.source))] for x in mems],
            "mem_words": [_memory_words(w, x, p.id) for x in mems[:6]],
            "makes": makes,
            "beliefs": len(p.beliefs),
            "puzzles": [[x["text"], round(x["pull"], 2), x["tests"]] for x in m["puzzles"][:4]],
            "heard": m["heard"][:4], "trust": m["records"][:4],
            "thoughts": [x["text"] for x in m["thoughts"][:3]], "state": m["state"],
        })
    frames.append({"week": tick, "season": w.season, "people": people})

out = {"seed": SEED, "year": START, "nature": "v11 (live acl/)", "actions": list(_brain(w, w.living()[0])["actions"]),
       "n_contexts": _brain(w, w.living()[0])["n_contexts"], "max_mem": MAX_MEM, "names": names, "frames": frames}
OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
print(f"wrote {OUT.name}: {OUT.stat().st_size // 1024} KB, {len(frames)} weeks, "
      f"{len(frames[0]['people'])} people aged child or older in week one")
