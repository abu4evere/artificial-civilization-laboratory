"""E1 investigations: re-run E1 seeds with read-only recorders attached.

    A. Why doesn't accuracy affect trust?   -> every trust change, by what caused it
    B. Why does sowing fail?                -> every seed put in the ground, and what came of it
    C. Why do rafts appear immediately?     -> every island crossing (plus a static check, see analyse_inv.py)
    D. Which cultural patterns last longest? -> yearly holders of every technique, belief, symbol, story, dwelling

The world is deterministic, so a re-run is the same history. The recorders only
read. The trust recorder wraps `bump` to note who called it and by how much trust
moved, then calls the real thing unchanged. To prove nothing changed, each re-run's
state at year 100 is checked against the snapshot E1 saved at year 100.

Usage: python experiments/E1/investigate.py 102 104 ...
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent))

from acl import actions, information, marks, social  # noqa: E402
from acl.config import WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import Historian  # noqa: E402
from acl.matter import best_float, pile_warmth  # noqa: E402
from acl.measure import Lab  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402
from acl.world import World  # noqa: E402

OUT = HERE / "output"


class TrustRecorder:
    """Wraps `bump` wherever it is used. Records the actual change in trust and the calling function."""

    def __init__(self):
        self.year = Counter()        # caller -> sum of |change| this year
        self.year_n = Counter()      # caller -> number of changes this year
        self.year_signed = Counter() # caller -> signed sum
        self.touched_by_test: set = set()   # (listener, source) relations ever moved by a test
        self.original = social.bump

    def install(self):
        orig = self.original

        def bump(p, other, tick, **kw):
            r = p.rel.get(other)
            before = r.trust if r is not None else 0.0
            orig(p, other, tick, **kw)
            change = p.rel[other].trust - before
            if change:
                caller = sys._getframe(1).f_code.co_name
                self.year[caller] += abs(change)
                self.year_n[caller] += 1
                self.year_signed[caller] += change
                if caller == "tested":
                    self.touched_by_test.add((p.id, other))
        social.bump = bump
        actions.bump = bump
        information.bump = bump

    def uninstall(self):
        social.bump = self.original
        actions.bump = self.original
        information.bump = self.original


class Probe:
    """Weekly and yearly read-only records for the four investigations."""

    def __init__(self, trust: TrustRecorder):
        self.trust = trust
        self.island: dict = {}
        self.trust_years = []
        self.trust_total_prev = None
        self.tests: dict = defaultdict(list)          # source -> [1 held / 0 failed, in time order]
        self.test_kinds = Counter()
        # B: sowing
        self.sowings = []                            # [tick, who, x, y, amount, season, belief]
        self.harvests = []                           # [tick, who, x, y, crop, sowers of that tile in the last year]
        self.sowers_of: dict = defaultdict(list)     # (x, y) -> [[tick, who]]
        self.summer_fields = []                      # [year, tiles with crop >= 5, total crop]
        self.believer_weeks = Counter()              # outcomes for people who believe in sowing this season
        # C: crossings
        self.where: dict = {}                        # pid -> island they were last on
        self.crossings = []                          # [tick, who, from, to, float of best item, generation]
        self.at_sea = 0
        # D: patterns
        self.patterns = []                           # one dict per year: key -> [holders, min gen, max gen]

    def _islands(self, world):
        if not self.island:
            for i, comp in enumerate(world.landmasses()):
                for loc in comp:
                    self.island[loc] = i
        return self.island

    def __call__(self, world, events):
        tick = world.tick - 1
        week = tick % WEEKS_PER_YEAR
        season = week // 13
        isl = self._islands(world)
        for e in events:
            k = e["k"]
            if k in ("verified", "refuted"):
                self.test_kinds[(k, str(e.get("claim", ""))[:2])] += 1
                for src in e.get("by") or []:
                    self.tests[src].append(1 if k == "verified" else 0)
            elif k == "put" and e.get("thing") == "seeds" and e.get("into") == "ground":
                x, y = e["at"]
                self.sowings.append([tick, e["a"], x, y, e.get("amount", 0), season, e.get("belief", 0)])
                self.sowers_of[(x, y)].append([tick, e["a"]])
            elif k == "harvest":
                x, y = e["at"]
                sowers = sorted({w for t, w in self.sowers_of.get((x, y), []) if tick - t <= WEEKS_PER_YEAR})
                self.harvests.append([tick, e["a"], x, y, e.get("crop", 0), sowers])
        # B: did people who believe in sowing this season sow, and if not, why not?
        for d in world.week_decisions:
            key = f"seeds@{season}"
            b = d.state["beliefs"].get(key)
            p = world.people.get(d.agent_id)
            if b is None or b < 0.2 or p is None:
                continue
            self.believer_weeks["believer-weeks"] += 1
            put_seen = any(c[0] == "put" and c[1] == "seeds" for c in d.candidates)
            chose = d.chosen[0] == "put" and d.chosen[1] == "seeds"
            self.believer_weeks["put seeds was among their top choices" if put_seen else "put seeds not among top choices"] += 1
            if chose:
                self.believer_weeks["sowed"] += 1
            need = p.need(world.cfg, d.tick)
            if d.state["food"] < 2.0 * need:
                self.believer_weeks["had under 2 weeks of food"] += 1
            if d.chosen[0] in ("forage", "hunt", "take"):
                self.believer_weeks["chose food instead"] += 1
        # C: crossings between islands
        for p in world.living():
            here = isl.get(p.loc)
            if here is None:
                self.at_sea += 1
                continue
            before = self.where.get(p.id)
            if before is not None and before != here:
                self.crossings.append([tick, p.id, before, here, round(best_float(p)[1], 2), p.generation])
            self.where[p.id] = here
        if week == 30:
            crops = [t.crop for r in world.tiles for t in r if t.crop > 0]
            self.summer_fields.append([tick // WEEKS_PER_YEAR, sum(1 for c in crops if c >= 5), round(sum(crops), 1)])
        if week == WEEKS_PER_YEAR - 1:
            self._year(world, tick)

    def _year(self, world, tick):
        living = world.living()
        ids = {q.id for q in living}
        total = sum(abs(r.trust) for q in living for pid, r in q.rel.items() if pid in ids)
        row = {"year": tick // WEEKS_PER_YEAR, "by_cause": dict(self.trust.year), "n": dict(self.trust.year_n),
               "signed": dict(self.trust.year_signed), "abs_trust_total": round(total, 2),
               "relations": sum(1 for q in living for pid in q.rel if pid in ids)}
        self.trust_years.append(row)
        self.trust.year, self.trust.year_n, self.trust.year_signed = Counter(), Counter(), Counter()
        # D: who holds what this year
        pat: dict = {}

        def hold(key, q):
            v = pat.get(key)
            if v is None:
                pat[key] = [1, q.generation, q.generation]
            else:
                v[0] += 1
                v[1] = min(v[1], q.generation)
                v[2] = max(v[2], q.generation)
        for q in living:
            for sig in q.recipes:
                hold("tech:" + sig, q)
            for key, v in q.beliefs.items():
                if v >= 0.15:
                    hold("belief:" + key, q)
            for hkey, h in q.heard.items():
                if h[0] >= 0.15:
                    hold("hearsay:" + hkey[2:], q)
            for shape in q.marks:
                for thing, v in marks.meaning(q, shape).items():
                    if v >= 0.3:
                        hold(f"symbol:{shape}|{thing}", q)
            for m in q.memories:
                if m.kind in ("killed", "attacked", "stole", "mauled", "died", "storm", "flood"):
                    hold(f"story:{m.eid}", q)
        for r in world.tiles:
            for t in r:
                if t.pile and pile_warmth(t.pile) >= 0.2:
                    pat[f"dwelling:{t.x},{t.y}"] = [1, 0, 0]
        self.patterns.append({k: v for k, v in pat.items() if v[0] >= 2 or k.startswith("dwelling:")})


def run(seed: int, years: int = 200) -> dict:
    trust = TrustRecorder()
    trust.install()
    try:
        w = World(Config(seed=seed))
        h = Historian()
        probe = Probe(trust)
        w.observers += [h, Lab(h), probe]       # the same observers E1 had, plus the probe
        check = None
        t0 = time.time()
        for y in range(years):
            for _ in range(WEEKS_PER_YEAR):
                w.step()
            if y + 1 == 100:
                saved = OUT / f"seed_{seed}_year100.json.gz"
                if saved.exists():
                    sw, _ = load_snapshot(saved)
                    check = sw.state_hash() == w.state_hash()
                    print(f"  seed {seed}: year 100 identical to E1: {check}", flush=True)
            if not w.living():
                break
        out = {"seed": seed, "years": w.year, "identical_at_100": check, "seconds": round(time.time() - t0),
               "trust_years": probe.trust_years, "touched_by_test": len(trust.touched_by_test),
               "tests": dict(probe.tests), "test_kinds": {f"{a}|{b}": v for (a, b), v in probe.test_kinds.items()},
               "sowings": probe.sowings, "harvests": probe.harvests, "summer_fields": probe.summer_fields,
               "believer_weeks": dict(probe.believer_weeks), "crossings": probe.crossings, "at_sea_weeks": probe.at_sea,
               "patterns": probe.patterns,
               "names": {pid: [p.name, p.generation, p.birth] for pid, p in w.people.items()}}
    finally:
        trust.uninstall()
    (OUT / f"inv_seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    return out


if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[1:]] or list(range(101, 109)):
        if (OUT / f"inv_seed_{s}.json").exists():
            print(f"seed {s}: already done")
            continue
        r = run(s)
        print(f"seed {s}: done, {r['years']} years, {r['seconds']}s, identical at 100: {r['identical_at_100']}", flush=True)
