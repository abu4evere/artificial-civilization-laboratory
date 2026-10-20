"""Find real people in replayed worlds whose lives show what the later chapters describe (read-only; nature v2).

  python drafts/book_rewrite/find_people.py 501 502 ...    # writes drafts/book_rewrite/people_<seed>.json

Nothing in a world is changed: one observer reads each week's events and people. Every name and fact the book uses
comes from these files, so the book's promise ("every name is a person who lived in a seeded world") holds.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "NV2_nature_v2" / "code_v2"))
from acl.config import Config, WEEKS_PER_YEAR  # noqa: E402
from acl.world import World  # noqa: E402

V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
YEARS = 120


class Watch:
    def __init__(self):
        self.ev = []
        self.recipes_max = {}
        self.single_weeks = {}      # woman id -> weeks aged 16-40 alive without a partner
        self.food_at_winter = {}    # (id, year) -> food held in the first week of winter

    def __call__(self, w, events):
        for e in events:
            if e["k"] in ("birth", "death", "give", "make", "learn", "pair", "harvest", "put"):
                self.ev.append({k: e.get(k) for k in ("t", "k", "a", "b", "cause", "age", "amount", "thing", "how")})
        season = (w.tick // 13) % 4
        for p in w.living():
            self.recipes_max[p.id] = max(self.recipes_max.get(p.id, 0), len(p.recipes))
            y = p.age(w.tick) / WEEKS_PER_YEAR
            if p.sex == "F" and 16 <= y <= 40 and not p.partner:
                self.single_weeks[p.id] = self.single_weeks.get(p.id, 0) + 1
            if season == 3 and w.tick % 13 == 0:
                self.food_at_winter[f"{p.id}|{w.tick // WEEKS_PER_YEAR}"] = round(p.food + p.seeds, 1)


def run(seed):
    w = World(Config(seed=seed, anticipation_weight=1.0, **V2))
    obs = Watch()
    w.observers.append(obs)
    for _ in range(YEARS * WEEKS_PER_YEAR):
        w.step()
        if not w.living():
            break
    people = {p.id: {"name": p.name, "sex": p.sex, "birth_year": round(p.birth / WEEKS_PER_YEAR, 1),
                     "mother": p.mother, "father": p.father, "alive": p.alive}
              for p in w.people.values()}
    out = {"seed": seed, "end_year": round(w.tick / WEEKS_PER_YEAR, 1), "alive_at_end": len(w.living()),
           "people": people, "events": obs.ev, "recipes_max": obs.recipes_max, "single_weeks": obs.single_weeks,
           "food_at_winter": obs.food_at_winter}
    (Path(__file__).parent / f"people_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    print(seed, "done, year", out["end_year"], "alive", out["alive_at_end"], flush=True)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(int(s))
