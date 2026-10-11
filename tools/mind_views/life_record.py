"""Life record: what chosen people of one control world did, thought and weighed, week by week, read-only, for the book.

Replays a control world (experiments/E13R_replication/code_e13r) and, for the named people, records each week: age,
health, food held, partner, where they were, what they chose, the options they weighed, and what held their attention
(acl/mindview.py). Also their life facts: parents, siblings, children, partners, how they died. Writes one JSON file
under book/records/ so every quotation in the book can be traced to it.

  python tools/mind_views/life_record.py 1112 104 117 Kibok Riyei     # seed, from year, to year, names
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
CODE = ROOT / "experiments" / "E13R_replication" / "code_e13r"
sys.path.insert(0, str(CODE))
import acl  # noqa: E402
assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()
from acl import mindview  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.util import distance  # noqa: E402
from acl.world import World  # noqa: E402

WPY = 52


def main():
    seed, y0, y1, names = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
    w = World(Config(seed=seed, anticipation_weight=1.0))
    while w.tick < y0 * WPY and w.living():
        w.step()
    ids, partners_seen, weeks = {}, {}, []

    def find():   # the named people, as soon as they are born
        for q in w.people.values():
            if q.name in names and q.id not in ids:
                ids[q.id] = q.name
                partners_seen[q.id] = []
    find()
    while w.tick < y1 * WPY and (not ids or len(ids) < len(names) or any(w.people[pid].alive for pid in ids)) and w.living():
        w.step()
        find()
        t = w.tick
        row = {"tick": t, "year": t // WPY, "week": t % WPY + 1, "alive_in_world": len(w.living()), "people": {}}
        for pid in ids:
            p = w.people[pid]
            if not p.alive:
                continue
            if p.partner and p.partner not in partners_seen[pid]:
                partners_seen[pid].append(p.partner)
            m = mindview.mind(w, p)
            row["people"][p.name] = {
                "age": round(p.years(t), 1), "health": round(p.health), "food_weeks": round(p.edible() / p.need(w.cfg, t), 2),
                "starving": bool(p.starving), "partner": w.people[p.partner].name if p.partner else None, "loc": list(p.loc),
                "chose": p.last_action, "weighed": [[o["text"], round(o["score"], 2), o["chosen"]] for o in m["weighed"]],
                "thoughts": [[o["text"], round(o["pull"], 2)] for o in m["thoughts"]], "feelings": m["feelings"]}
        locs = [w.people[pid].loc for pid in ids if w.people[pid].alive]
        if len(locs) == 2:
            row["distance_between"] = distance(locs[0], locs[1], w.cfg.width, w.cfg.height)
        weeks.append(row)
    nm = lambda x: w.people[x].name if x and x in w.people else None  # noqa: E731
    lives = {}
    for pid, name in ids.items():
        p = w.people[pid]
        sibs = [q.name for q in w.people.values() if q.id != pid and q.mother and q.mother == p.mother and q.father == p.father]
        lives[name] = {"id": pid, "sex": p.sex, "born_year": p.birth // WPY if p.birth >= 0 else "founder",
                       "generation": p.generation, "mother": nm(p.mother), "father": nm(p.father), "full_siblings": sibs,
                       "children": [nm(c) for c in p.children], "partners_in_window": [nm(x) for x in partners_seen[pid]],
                       "died": {"year": p.death_tick // WPY, "week": p.death_tick % WPY + 1, "cause": p.death_cause,
                                "age": round(p.years(p.death_tick), 1)} if not p.alive else None,
                       "temperament": {g: round(v, 2) for g, v in p.genes.items()}}
    if len(ids) == 2:
        a, b = (w.people[x] for x in ids)
        lives["kinship_between"] = w.kinship(a, b)
    summary = {}
    for name in names:
        th, ch = Counter(), Counter()
        for r in weeks:
            if name in r["people"]:
                th.update(t for t, _ in r["people"][name]["thoughts"])
                ch[r["people"][name]["chose"]] += 1
        summary[name] = {"weeks_recorded": sum(1 for r in weeks if name in r["people"]),
                         "most_frequent_thoughts": th.most_common(10), "choices": ch.most_common()}
    d = [r["distance_between"] for r in weeks if "distance_between" in r]
    if d:
        summary["distance_between"] = {"weeks": len(d), "median": sorted(d)[len(d) // 2], "within_sight_share": round(sum(x <= 4 for x in d) / len(d), 3)}
    out = ROOT / "book" / "records" / f"life_seed{seed}_{'_'.join(names)}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"seed": seed, "from_year": y0, "to_year": y1, "code": "code_e13r (control)",
                               "lives": lives, "summary": summary, "weeks": weeks}, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"lives": lives, "summary": summary}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
