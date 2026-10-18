"""FX1 (evidence review, read-only): where ACL's people get their food, by source, to set beside forager diets
(Kaplan et al. 2000: hunted ~60%, extracted ~32%, collected ~8% of calories, 10 societies). Live package = nature v2.
Counts food units from the world's own events: forage (wild plants and crop), harvest (the crop part), hunt (meat, by
animal). An observer that only reads events; checked: the world's state hash is identical with and without it.

  python experiments/FX1_extracted_foods/acl_diet.py      # 16 seeds (501-516), 60 years -> acl_diet.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from acl import Config, World  # noqa: E402

SEEDS, YEARS = tuple(range(501, 517)), 60


class Diet:
    def __init__(self):
        self.c = Counter()

    def __call__(self, world, events):
        for e in events:
            k = e["k"]
            if k == "forage":
                self.c["forage_total"] += e.get("got", 0)
            elif k == "harvest":
                self.c["crop"] += e.get("crop", 0)
            elif k == "hunt" and e.get("success"):
                self.c["meat"] += e.get("meat", 0)
                self.c["meat_" + str(e.get("animal"))] += e.get("meat", 0)
                self.c["hunts_won"] += 1
            elif k == "hunt":
                self.c["hunts_lost"] += 1


def run(seed, observe):
    w = World(Config(seed=seed))
    d = Diet()
    if observe:
        w.observers.append(d)
    for _ in range(YEARS * 52):
        w.step()
        if not w.living():
            break
    return w, d


def main():
    w0, _ = run(SEEDS[0], False)
    w1, d1 = run(SEEDS[0], True)
    assert w0.state_hash() == w1.state_hash(), "observer changed the world"
    tot = Counter(d1.c)
    for s in SEEDS[1:]:
        tot += run(s, True)[1].c
        print("seed", s, flush=True)
    wild = tot["forage_total"] - tot["crop"]
    food = wild + tot["crop"] + tot["meat"]
    res = {"seeds": list(SEEDS), "years": YEARS, "code": "acl (nature v2)", "observer_read_only": True,
           "units": dict(tot), "share": {"wild_plants": round(wild / food, 4), "crop": round(tot["crop"] / food, 4),
                                          "meat": round(tot["meat"] / food, 4)}}
    (Path(__file__).with_name("acl_diet.json")).write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res["share"]), tot["hunts_won"], tot["hunts_lost"])


if __name__ == "__main__":
    main()
