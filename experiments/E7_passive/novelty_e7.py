"""E7's recorder: E6's novelty recorder unchanged, plus what E7's pre-registration (E7_passive.md §6) adds.
Read-only, like E6's: it reads events and what people carry, and keeps references to nothing it changes.

Added on top of E6:
- First Encounter Counts: the world's own `consequence` events water_passive, ceramic_passive and food_by_fire
  (E6's recorder already tallies every consequence; they are pulled out under `fec` in the results);
- New Consequence 1, water carried: for every drink from a carried vessel (`water_carried`), the distance to the
  nearest fresh water (river or lake tile, toroidal, in tiles);
- New Consequence 2, fired clay outliving its maker: every fired-clay object (a thing whose name holds both `clay`
  and the heated mark `^`) is followed from the first week anyone is seen carrying it; its first carrier counts as
  its maker. It outlives its maker if it is still carried after the maker has died.
- New Consequence 3, food eaten past its natural rot threshold, cannot be measured: food is one pooled amount per
  person with no age, so no unit of food has a threshold to pass. It is reported as not measurable.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "E6_novelty"))
from novelty import WPY, Novelty  # noqa: E402

FRESH = ("lake", "river")
FEC = ("water_passive", "ceramic_passive", "food_by_fire")


class NoveltyE7(Novelty):
    def __init__(self, scale: int, materials: tuple):
        super().__init__(scale, materials)
        self.fresh = None             # fresh-water tiles, found on the first week
        self.carried = []             # [year, distance to fresh water] per drink from a carried vessel
        self.fired = {}               # id(object) -> [object, maker, first tick, last tick, maker died tick]
        self.first_fec = {}           # FEC kind -> first year it happened

    def _distance_to_fresh(self, world, at) -> int:
        from acl.util import distance
        c = world.cfg
        if self.fresh is None:
            self.fresh = [(t.x, t.y) for row in world.tiles for t in row if t.biome in FRESH]
        return min((distance(tuple(at), f, c.width, c.height) for f in self.fresh), default=-1)

    def __call__(self, world, events):
        tick = world.tick - 1
        for e in events:
            if e["k"] != "consequence":
                continue
            what = e.get("what")
            if what in FEC:
                self.first_fec.setdefault(what, tick // WPY)
            if what == "water_carried" and "at" in e:
                self.carried.append([tick // WPY, self._distance_to_fresh(world, e["at"])])
        for p in world.living():
            for it in p.items:
                sig = it["sig"]
                if "clay" in sig and "^" in sig:
                    rec = self.fired.get(id(it))
                    if rec is None or rec[0] is not it:
                        self.fired[id(it)] = [it, p.id, tick, tick, None]
                    else:
                        rec[3] = tick
        for rec in self.fired.values():
            if rec[4] is None and rec[3] == tick:
                maker = world.people.get(rec[1])
                if maker is not None and not maker.alive:
                    rec[4] = maker.death_tick
        super().__call__(world, events)

    def results(self, world):
        res = super().results(world)
        res["fec"] = {k: self.consequences.get(k, 0) for k in FEC}
        res["fec_first_year"] = self.first_fec
        d = [x[1] for x in self.carried]
        res["water_carried"] = {
            "drinks": len(d),
            "max_tiles": max(d, default=None),
            "drinks_3plus": sum(1 for x in d if x >= 3),
            "drinks_5plus": sum(1 for x in d if x >= 5),
            "first_year": min((x[0] for x in self.carried), default=None),
            "last_year": max((x[0] for x in self.carried), default=None),
            "first_year_3plus": min((x[0] for x in self.carried if x[1] >= 3), default=None),
            "last_year_3plus": max((x[0] for x in self.carried if x[1] >= 3), default=None),
        }
        objs = []
        for it, maker, first, last, maker_died in self.fired.values():
            objs.append({"sig": it["sig"], "maker": maker, "first_year": first // WPY,
                         "years_carried": round((last - first) / WPY, 1),
                         "outlived_maker": maker_died is not None and last > maker_died,
                         "years_after_maker": round((last - maker_died) / WPY, 1)
                         if maker_died is not None and last > maker_died else 0.0})
        res["fired_objects"] = sorted(objs, key=lambda o: -o["years_carried"])[:200]
        res["fired_summary"] = {
            "objects": len(objs),
            "outlived_maker": sum(1 for o in objs if o["outlived_maker"]),
            "longest_years": max((o["years_carried"] for o in objs), default=0.0),
            "over_50y_and_outlived": sum(1 for o in objs if o["outlived_maker"] and o["years_carried"] > 50),
        }
        res["food_past_rot_threshold"] = "not measurable: food is pooled per person and has no age"
        return res
