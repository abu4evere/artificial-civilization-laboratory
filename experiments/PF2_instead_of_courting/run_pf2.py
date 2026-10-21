"""PF2 — what people do instead of courting (questions.md, frozen as `PF2-frozen`). Read-only.

`code_pf2` = `code_mb1b` + logging in `mind.decide` only: for every decision by a single adult, courting's share of the
choice toward each person it was offered for, the chosen action, and who was within reach (nearest 12) at that moment,
appended to `world.pf2log` (not saved, read by nothing in the world; no random draws). A read-only weekly observer finds
PF1's S5 weeks (a suitable, not-disliked man within reach at the end of the week, and no courting between them) and
classifies each:

  O1 offered to her      her options included court toward one of those men
  O2 offered to him only not to her, but one of those men had court toward her among his options
  N  not offered         neither; first failed reason: no decision recorded / crowded out of the nearest 12 /
                         not within reach at the moment of deciding / within reach but another condition failed

MB1b's own worlds are replayed exactly: each replay's final state hash must equal the saved one.

  python experiments/PF2_instead_of_courting/run_pf2.py zero
  python experiments/PF2_instead_of_courting/run_pf2.py run      # discovery 5301-5316, then holdout 5317-5332; p4, b16
  python experiments/PF2_instead_of_courting/run_pf2.py smoke    # throwaway: seed 9701, 6 years
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"pf2": HERE / "code_pf2", "mb1b": EXP / "MB1_multi_band" / "code_mb1b"}
SAVED = EXP / "MB1_multi_band" / "output_mb1b"
OUT = HERE / "output"
WPY, YEARS = 52, 120
DISCOVERY = tuple(range(5301, 5317))
HOLDOUT = tuple(range(5317, 5333))
V2 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1}
ARMS = {"p4": {}, "b16": {"founding_bands": 16}}
GROUPS = {"forage": "subsistence", "hunt": "subsistence", "gather": "subsistence", "put": "subsistence",
          "take": "subsistence", "fill": "subsistence", "rest": "rest", "talk": "other social", "give": "other social",
          "care": "other social", "play": "other social", "explore": "movement", "join": "movement",
          "flee": "movement", "make": "other", "heat": "other", "steal": "other", "attack": "other",
          "court": "court (someone else)"}
CLASSES = ("O1_offered_to_her", "O2_offered_to_him_only", "N_not_offered")
REASONS = ("no_decision", "crowded_out_of_nearest_12", "not_in_reach_when_deciding", "in_reach_other_condition")


def setup(code="pf2"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw, founders=80):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, founders=founders, **V2, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["pf2"] / "acl")


class Audit:
    """Read-only: reads the world after each week and the week's decision log; changes nothing in the world."""

    def __init__(self):
        self.s5 = 0
        self.classes = Counter()
        self.won = Counter()          # "class|group"
        self.shares = {"O1": [], "O2": []}
        self.reasons = Counter()
        self.woman_weeks = 0

    def __call__(self, world, events):
        from acl.config import WEEKS_PER_YEAR
        c, tick = world.cfg, world.tick
        log = getattr(world, "pf2log", None) or []
        dec = {}
        for _t, pid, act, aim, court, near_ids, n in log:
            dec[pid] = (act, aim, court, near_ids, n)       # one decision per person per week
        if getattr(world, "pf2log", None) is not None:
            world.pf2log.clear()
        living = world.living()
        men = [q for q in living if q.sex == "M" and q.stage(tick) == "adult" and q.partner is None]
        for p in living:
            if p.sex != "F" or p.partner is not None:
                continue
            yrs = (tick - p.birth) / WEEKS_PER_YEAR
            if not (c.fertile_from <= yrs < c.fertile_until):
                continue
            self.woman_weeks += 1
            open_ = self.s5_men(world, p, men, dec)
            if not open_:
                continue
            self.s5 += 1
            ids = {q.id for q in open_}
            her = dec.get(p.id)
            her_share = sum(v for k, v in (her[2] if her else {}).items() if k in ids)
            if her and her_share > 0:
                self.classes[CLASSES[0]] += 1
                self.won[f"O1|{GROUPS.get(her[0], 'other')}"] += 1
                self.shares["O1"].append(round(her_share, 4))
                continue
            his = [(dec[q.id], dec[q.id][2].get(p.id, 0.0)) for q in open_ if q.id in dec and dec[q.id][2].get(p.id)]
            if his:
                d, sh = max(his, key=lambda x: x[1])
                self.classes[CLASSES[1]] += 1
                self.won[f"O2|{GROUPS.get(d[0], 'other')}"] += 1
                self.shares["O2"].append(round(sh, 4))
                continue
            self.classes[CLASSES[2]] += 1
            self.reasons[self.reason(her, ids)] += 1

    @staticmethod
    def s5_men(world, p, men, dec):
        """PF1's S1-S5 at the end of the week: suitable, in reach, not disliked, and no courting between them."""
        c = world.cfg
        match = [q for q in men if world.kinship(p, q) == 0 and abs(p.birth - q.birth) <= 15 * WPY
                 and q.id not in p.wards and p.id not in q.wards]
        if not match:
            return []
        ids = {q.id for q in match}
        reach = [q for q in world.people_near(p.loc, c.reach, exclude=p.id) if q.id in ids]

        def aff(a, b):
            r = a.rel.get(b.id)
            return r.affection if r else 0.0
        open_ = [q for q in reach if aff(p, q) > -0.2 and aff(q, p) > -0.2]
        her = dec.get(p.id)
        for q in open_:                       # any courting between them this week means S6, not S5
            hq = dec.get(q.id)
            if (her and her[0] == "court" and her[1] == q.id) or (hq and hq[0] == "court" and hq[1] == p.id):
                return []
        return open_

    @staticmethod
    def reason(her, ids):
        if her is None:
            return REASONS[0]
        near_ids, n = her[3], her[4]
        if not (set(near_ids) & ids):
            return REASONS[1] if n > 12 else REASONS[2]
        return REASONS[3]

    def results(self):
        return {"woman_weeks": self.woman_weeks, "s5_weeks": self.s5, "classes": dict(self.classes),
                "won": dict(self.won), "shares": self.shares, "reasons": dict(self.reasons)}


def hashrun(code, seed, years, kw, observe, founders):
    setup(code)
    w = make_world(seed, kw, founders)
    if observe:
        w.pf2log = []
        w.observers.append(Audit())
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for founders in (20, 80):
        for seed in (501, 601):
            for kw in ({}, {"founding_bands": 16}):
                ref = call("mb1b", seed, 20, json.dumps(kw), 0, founders)
                for obs in (0, 1):
                    t = call("pf2", seed, 20, json.dumps(kw), obs, founders) == ref
                    ok &= t
                    lines.append(f"{founders} founders, seed {seed}, 20 years, {kw or 'p4'}, logging+observer "
                                 f"{'on' if obs else 'off'}: = code_mb1b: {'yes' if t else 'NO'}")
    setup("pf2")
    lines.append(f"code_pf2 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("pf2")
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    w.pf2log = []
    audit = Audit()
    w.observers.append(audit)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "alive_end": len(w.living()), **audit.results()}
    saved = SAVED / f"{arm}_seed_{seed}.json"
    if saved.exists() and years == YEARS:
        res["reproduces"] = json.loads(saved.read_text(encoding="utf-8"))["world_hash"] == res["world_hash"]
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: reproduces {res.get('reproduces')}, S5 weeks {audit.s5}", flush=True)


def batch(seeds, years=YEARS, out=OUT, workers=2):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the zero checks have not passed (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), todo))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1",
                      int(sys.argv[7])))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "run":
        batch(DISCOVERY)
        print("DISCOVERY DONE", flush=True)
        batch(HOLDOUT)
        print("ALL DONE", flush=True)
    elif cmd == "smoke":
        batch((9701,), years=6, out=HERE / "output_smoke")
        print("SMOKE DONE", flush=True)
