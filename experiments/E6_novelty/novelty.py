"""E6's novelty recorder. Read-only: it looks at each week's events and, every 10 years, at what people hold.

Definitions are in predictions.md (frozen). In brief:
- a *kind* is a thing's lasting properties, each in one of 5 bands; kinds come from events that report the
  properties of a thing the actor made or changed;
- a *behaviour* is an event someone did, with the kinds of things involved and its object (material, substance,
  where it went, surface, form, how);
- a novelty is new to the world and done or made by 3+ different people within 10 years of its first appearance;
- a lasting novelty is done or made again 50+ years after it first appeared;
- LFA (latest first appearance) is the first year of the latest lasting novelty.

Years are counted like the world counts them: year 0 is the first year (tick // 52).
Works under the baseline code (properties 0-1) and the E6 code (whole numbers 0-100): pass scale=1 or 100.
"""
from __future__ import annotations

WPY = 52
WINDOW = 10 * WPY
LASTING = 50 * WPY

# Lasting properties a thing can have (transient states such as heat and wetness are left out).
LASTING_PROPS = ("edge", "reach", "hard", "contain", "warm", "float", "tight", "plastic", "fuel", "flex", "mass")
# Categorical objects of an event.
OBJECTS = ("kind", "into", "on", "how", "form", "substance", "with", "material")
# Things that happen to people, or that they learn: not behaviours.
NOT_DONE = {"birth", "death", "ill", "pregnant", "injured", "mauled", "learn", "told", "tested", "verified",
            "vouched", "puzzled", "drank_sea", "inherit", "knowledge_lost", "found_gone", "disputed", "pair",
            "taken_in", "year", "read", "kill", "fire_out", "storm", "flood", "drought", "hard_winter"}


def band(v, scale):
    """One of 5 equal bands, whatever the scale (baseline 0-1, E6 0-100)."""
    return min(4, int(v * 5 / scale))


def profile(props: dict, scale) -> tuple:
    return tuple((k, band(props[k], scale)) for k in LASTING_PROPS if k in props)


class Novelty:
    def __init__(self, scale: int, materials: tuple):
        self.scale = scale
        self.materials = set(materials)
        self.first = {}      # key -> first tick
        self.early = {}      # key -> people who did it within 10 years of its first appearance
        self.last = {}       # key -> last tick seen
        self.kind_of = {}    # key -> "kind" or "behaviour"
        self.samples = []    # every 10 years: what 3+ people hold or do
        self.held_first = {} # tradition item -> first sample year it was held by anyone
        self.decade_doers = {}
        self.consequences = {}

    # --- each week -----------------------------------------------------------------
    def _thing(self, world, value, ev):
        """A thing named in an event: a raw material or substance by name, a made thing by its kind."""
        if value is None:
            return None
        if value in self.materials or value in ("food", "seeds", "water", "embers"):
            return value
        rec = world.knowledge.get(value) if isinstance(value, str) else None
        if rec and rec.get("props"):
            return profile(rec["props"], self.scale)
        return "item"

    def _see(self, key, kind, tick, actors):
        if key not in self.first:
            self.first[key] = tick
            self.early[key] = set()
            self.kind_of[key] = kind
        if tick - self.first[key] <= WINDOW:
            self.early[key].update(a for a in actors if a)
        self.last[key] = tick
        if kind == "behaviour":
            d = self.decade_doers.setdefault(key, set())
            d.update(a for a in actors if a)

    def __call__(self, world, events):
        tick = world.tick - 1
        for e in events:
            k = e["k"]
            actor = e.get("a")
            if k == "consequence":
                self.consequences[e.get("what")] = self.consequences.get(e.get("what"), 0) + 1
                continue
            if not actor or k in NOT_DONE:
                continue
            actors = [actor] + list(e.get("party", []))
            props = e.get("props") or ({p: e[p] for p in LASTING_PROPS if p in e} or None)
            made = profile(props, self.scale) if props else None
            parts = [k]
            if made is not None:
                parts.append(("made", made))
                self._see(("kind", made), "kind", tick, actors)
            elif "thing" in e:
                parts.append(("thing", self._thing(world, e["thing"], e)))
            for o in OBJECTS:
                if o in e:
                    v = e[o]
                    parts.append((o, self._thing(world, v, e) if o in ("with", "material") else v))
            self._see(("behaviour", tuple(parts)), "behaviour", tick, actors)
        if tick % WINDOW == WINDOW - 1:
            self._sample(world, tick)

    # --- every 10 years ------------------------------------------------------------
    def _sample(self, world, tick):
        from acl import marks
        year = tick // WPY
        living = world.living()
        held = {}
        for p in living:
            for sig in p.recipes:
                held["tech:" + sig] = held.get("tech:" + sig, 0) + 1
            for key, val in p.beliefs.items():
                if val >= 0.15:
                    held["belief:" + key] = held.get("belief:" + key, 0) + 1
            for shape in p.marks:
                for thing, mv in marks.meaning(p, shape).items():
                    if mv >= 0.3:
                        held[f"symbol:{shape}|{thing}"] = held.get(f"symbol:{shape}|{thing}", 0) + 1
        firsts = {}
        for key, doers in self.decade_doers.items():
            name = f"behaviour:{key[1]!r}"
            held[name] = len(doers)
            firsts[name] = self.first[key] // WPY
        self.decade_doers = {}
        for item in held:
            if item in firsts:
                first = firsts[item]
            elif item.startswith("tech:"):
                rec = world.knowledge.get(item[5:])
                first = rec["first_tick"] // WPY if rec else year
            else:
                first = year
            self.held_first.setdefault(item, first)
        self.samples.append({"year": year, "population": len(living),
                             "traditions": sorted(i for i, n in held.items() if n >= 3)})

    # --- after the run -------------------------------------------------------------
    def results(self, world):
        novel = []
        for key, t0 in self.first.items():
            if len(self.early[key]) >= 3:
                novel.append({"key": repr(key[1]), "type": self.kind_of[key], "first_year": t0 // WPY,
                              "people_first_10y": len(self.early[key]), "last_year": self.last[key] // WPY,
                              "lasting": self.last[key] - t0 >= LASTING})
        lasting = [n for n in novel if n["lasting"]]
        lfa = max((n["first_year"] for n in lasting), default=None)
        after = sum(1 for n in lasting if n["first_year"] > 100)
        # traditions: held or done by 3+ in every sample for 100+ years, first appearing after year 100
        runs, current = {}, {}
        for s in self.samples:
            now = {}
            for t in s["traditions"]:
                start, n = current.get(t, (s["year"], 0))
                now[t] = (start, n + 1)
                if n + 1 > runs.get(t, (0, 0))[0]:
                    runs[t] = (n + 1, start)
            current = now
        new_trad = sorted(((t, 10 * n, st) for t, (n, st) in runs.items()
                           if n >= 10 and self.held_first.get(t, 0) > 100), key=lambda x: -x[1])
        return {"novelties": novel, "lasting": len(lasting), "LFA": lfa,
                "share_after_100": round(after / len(lasting), 4) if lasting else None,
                "new_traditions": [{"item": t, "years": y, "from": st} for t, y, st in new_trad],
                "consequences": self.consequences, "samples": self.samples}
