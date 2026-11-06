"""Exploratory, read-only (not frozen; no reading is drawn from it): do inventors keep holding the thing they invented,
so that they never want its materials again (mind._material_wants skips recipes whose item is held)? Runs nature v13
worlds with VA1's observer plus a weekly check of whether the inventor still holds an item of the kind.

  python experiments/VA1_value_at_invention/explore_holding.py <seed> <years> <from_year>   -> explore_holding_<seed>.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_va1 as V  # noqa: E402


class Holding(V.VA1Obs):
    def __call__(self, world, events):
        super().__call__(world, events)
        from acl.mind import _holding
        tick = world.tick - 1
        for sig, kd in self.kinds.items():
            if not (kd["t"] <= tick < kd["t"] + V.REMAKE):
                continue
            p = world.people.get(kd["inv"])
            if p is None or not p.alive:
                kd.setdefault("died_week", tick - kd["t"])
                continue
            h = _holding(p, sig, True)
            kd.setdefault("holding_weeks", 0)
            kd["holding_weeks"] += int(h)
            if not h and kd.get("first_not_holding") is None:
                kd["first_not_holding"] = tick - kd["t"]
                kd["recipe_when_not_holding"] = int(sig in p.recipes)
                kd["value_when_not_holding"] = round(p.itemval.get(sig, 0.0), 4)


def main(seed, years, from_year):
    V.WIN[0], V.WIN[1] = from_year * V.WPY, years * V.WPY
    V.base.setup(V.CODE)
    w = V.base.make_world(seed, V.ARMS["c"])
    obs = Holding(w)
    V.install(w, obs)
    w.observers.append(obs)
    for _ in range(years * V.WPY):
        w.step()
    rows = []
    for sig, kd in obs.kinds.items():
        rows.append({"holding_weeks": kd.get("holding_weeks", 0), "first_not_holding": kd.get("first_not_holding"),
                     "recipe_when_not_holding": kd.get("recipe_when_not_holding"),
                     "value_when_not_holding": kd.get("value_when_not_holding"), "died_week": kd.get("died_week"),
                     "inputs": kd["inputs"], "free": kd["free"], "offered": kd["offered"], "remade": kd["remade"],
                     "full": kd["full"], "first": kd["first"], "lost_at": kd["lost_at"], "n_uses": len(kd["uses"]),
                     "t": kd["t"]})
    (HERE / f"explore_holding_{seed}.json").write_text(json.dumps(rows), encoding="utf-8")
    print(seed, "kinds", len(rows))


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
