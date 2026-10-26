"""TF1 — where do made things go? (questions.md, frozen as `TF1-frozen`). Read-only: live nature v7 (`code_v7`)
unchanged, with one weekly observer and no wrappers. Each week it lists every made thing in the world (in living
people's hands and with bodies), follows each by identity, and reads its fate from the change between two weeks.

  python experiments/TF1_tool_fate/run_tf1.py zero    # hard stops (writes output/zero.txt)
  python experiments/TF1_tool_fate/run_tf1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODE = EXP / "NV7_nature_v7" / "code_v7"
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(18301, 18333))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9957, 9956)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
ARMS = {"lp": {"founders": 80, "width": 80, "height": 80}}
JOBS = [f"lp:{s}" for s in SEEDS]
BIN_EDGES = (0, 5, 10, 20, 50, 100, 200)
USES = ("forage", "hunt", "wood", "stone", "fiber", "fight", "carry", "cold")


def bin_of(tick):
    y = tick / WPY
    for i in range(len(BIN_EDGES) - 1):
        if y < BIN_EDGES[i + 1]:
            return i
    return len(BIN_EDGES) - 2


def setup():
    sys.path.insert(0, str(CODE))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V7, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODE / "acl")


def ffac(it):
    from acl.matter import factor
    return factor(it, "forage")


def best_use(it):
    from acl.matter import factor
    return max(factor(it, u) for u in USES)


class TF1Obs:
    """Read-only weekly census of made things and their fates."""

    def __init__(self, w):
        self.w = w
        self.things = {}                  # id(obj) -> record (the object is kept, so ids are never reused)
        self.bins = defaultdict(Counter)  # bin -> counters
        self.ended = []                   # finished forage-tool records
        self.first_tool = {}              # pid -> [age weeks, route, birth tick]
        self.tool_state = {}              # pid -> [holding a forage tool, tick lost or None]
        self.last_carer = {}
        self.mismatch = Counter()
        self.appeared = 0
        self.n_ended = 0
        self.prev_holder = {}             # id -> ("p"/"b", owner id)
        self._census(w, w.tick, [], first=True)

    def _holder_index(self, world):
        cur = {}
        for p in world.living():
            for it in p.items:
                cur[id(it)] = ("p", p.id, it)
        for b in world.bodies:
            for it in b.get("items", ()):
                cur[id(it)] = ("b", b["id"], it)
        return cur

    def _census(self, world, tick, events, first=False):
        cur = self._holder_index(world)
        made = defaultdict(set)          # pid -> sigs made / played / heated this week
        for e in events:
            if e.get("k") in ("make", "play", "heat") and e.get("thing"):
                made[e["a"]].add(e["thing"])
        bi = bin_of(tick)
        b = self.bins[bi]
        gained = set()
        # new things
        for k, (ht, hid, obj) in cur.items():
            r = self.things.get(k)
            if r is not None and r["obj"] is obj:
                continue
            self.appeared += 1
            if first:
                origin = "founding"
            elif ht == "p" and obj["sig"] in made.get(hid, ()):
                origin = "made"
            else:
                origin = "unseen"
            ff = ffac(obj)
            self.things[k] = {"obj": obj, "sig": obj["sig"], "ff": round(ff, 4), "best": round(best_use(obj), 4),
                              "origin": origin, "maker": hid if origin == "made" else None, "first": tick,
                              "holders": [(ht, hid)], "uses": obj.get("uses", 0), "moves": [], "drop": 1}
            if ht == "p":
                gained.add(hid)
            self.prev_holder[k] = (ht, hid)
        if first:
            return
        # moves and ends
        for k in list(self.things):
            r = self.things[k]
            ph = self.prev_holder.get(k)
            now = cur.get(k)
            if now is not None and now[2] is r["obj"]:
                if (now[0], now[1]) != ph:
                    route = self._move(world, ph, (now[0], now[1]))
                    r["moves"].append([tick, route])
                    r["holders"].append((now[0], now[1]))
                    self.prev_holder[k] = (now[0], now[1])
                    if now[0] == "p":
                        gained.add(now[1])
                u = r["obj"].get("uses", 0)
                r["drop"] = max(r["drop"], r["uses"] - u)       # the most uses it has lost in one week
                r["uses"] = u
                continue
            fate = self._fate(world, r, ph, made, gained)
            self._end(r, fate, tick, world)
            del self.things[k]
            self.prev_holder.pop(k, None)

    def _move(self, world, a, b):
        if a[0] == "p" and b[0] == "p":
            q = world.people.get(a[1])
            return "inherited" if q is not None and not q.alive else "moved_living"
        if a[0] == "p" and b[0] == "b":
            return "left_with_body"
        if a[0] == "b" and b[0] == "p":
            return "taken_from_body"
        return "moved_other"

    def _fate(self, world, r, ph, made, gained):
        if ph is None:
            return "unknown"
        if ph[0] == "b":
            alive_body = any(bd["id"] == ph[1] for bd in world.bodies)
            return "unknown" if alive_body else "lost_with_body"
        q = world.people.get(ph[1])
        if q is None or not q.alive:
            return "lost_at_death"
        for t in made.get(q.id, ()):
            rec = q.recipes.get(t) or (world.knowledge.get(t) or {}).get("recipe") or {}
            parts = list(rec.get("parts", ())) + ([rec.get("part")] if rec.get("verb") == "heat" else [])
            if r["sig"] in parts:
                return "used_in_making"
        if r["uses"] <= r["drop"]:                      # operational note 1: no more uses left than its largest weekly drop
            return "worn_out"
        if q.id in gained:
            return "deleted_at_limit"
        return "unknown"

    def _end(self, r, fate, tick, world):
        self.n_ended += 1
        b = self.bins[bin_of(tick)]
        b[f"end_all_{fate}"] += 1
        if fate == "unknown":
            self.mismatch["_unknown"] += 0      # counted in bins; checked against 1% in the analysis
        if r["ff"] <= 1.0:
            return
        b[f"end_tool_{fate}"] += 1
        extra = None
        if fate == "deleted_at_limit":
            q = world.people.get(r["holders"][-1][1])
            kept = [ffac(it) for it in q.items]
            worst = min(kept) if kept else 1.0
            deps = [d for d in world.dependents(q.id) if d.age(world.tick) < 16 * WPY]
            near = world.people_near(q.loc, world.cfg.reach, exclude=q.id)
            kids_near = any(n.age(world.tick) < 16 * WPY for n in near)
            extra = [round(worst, 4), int(r["ff"] > worst + 1e-9), int(bool(deps)), int(bool(near)), int(kids_near)]
        self.ended.append([r["first"], r["origin"], r["ff"], fate, tick, r["uses"], len(r["holders"]),
                           [m[1] for m in r["moves"]], extra])

    def __call__(self, world, events):
        tick = world.tick - 1
        self._census(world, tick, events)
        bi = bin_of(tick)
        b = self.bins[bi]
        living = world.living()
        b["pw"] += len(living)
        for e in events:                                # operational note 2: things gone within the week they were made
            if e.get("k") in ("make", "play") and e.get("thing"):
                q = world.people.get(e["a"])
                if q is None or not q.alive:
                    continue
                b[f"made_{e['k']}"] += 1
                if not any(it["sig"] == e["thing"] for it in q.items):
                    b[f"made_{e['k']}_gone_same_week"] += 1
                    b[f"made_{e['k']}_gone_worth0"] += q.itemval.get(e["thing"], 0.0) == 0.0
        tools = {}
        for p in living:
            tools[p.id] = sum(1 for it in p.items if ffac(it) > 1.0)
        for p in living:
            age = p.age(world.tick)
            if p.caregiver:
                self.last_carer[p.id] = p.caregiver
            has = tools[p.id] > 0
            if age >= 16 * WPY:
                b["adult_w"] += 1
                b["adult_tool_w"] += has
            elif age >= 6 * WPY:
                b["child_w"] += 1
                b["child_tool_w"] += has
                cid = p.caregiver or self.last_carer.get(p.id)
                c = world.people.get(cid) if cid else None
                ct = tools.get(c.id, 0) if c is not None and c.alive else 0
                if ct >= 1:
                    b["child_carer1_w"] += 1
                    b["child_carer1_none_w"] += not has
                if ct >= 2:
                    b["child_carer2_w"] += 1
                    b["child_carer2_none_w"] += not has
            # first forage tool, and how it came
            if has and p.id not in self.first_tool:
                route = self._route_of_tool(p)
                self.first_tool[p.id] = [age, route, p.birth]
            # replacement (LS1's rule), by route
            ts = self.tool_state.setdefault(p.id, [has, None])
            if ts[0] and not has:
                ts[1] = world.tick
            elif not ts[0] and has and ts[1] is not None:
                if world.tick - ts[1] <= WPY:
                    b[f"replaced_{self._route_of_tool(p)}"] += 1
                ts[1] = None
            if ts[1] is not None and world.tick - ts[1] > WPY:
                b["not_replaced"] += 1
                ts[1] = None
            ts[0] = has
        b["things_in_world"] += len(self.things)

    def _route_of_tool(self, p):
        best = None
        for it in p.items:
            if ffac(it) > 1.0:
                r = self.things.get(id(it))
                if r is None or r["obj"] is not it:
                    return "unseen"
                if r["moves"]:
                    best = r["moves"][-1][1]
                elif r["origin"] == "made" and r["maker"] == p.id:
                    return "made"
                else:
                    best = best or r["origin"]
        return best or "unseen"

    def results(self, world):
        still = 0
        for r in self.things.values():
            still += 1
            if r["ff"] > 1.0:
                self.ended.append([r["first"], r["origin"], r["ff"], "still_held", world.tick, r["uses"],
                                   len(r["holders"]), [m[1] for m in r["moves"]], None])
        if self.appeared != self.n_ended + still:
            self.mismatch["ledger"] += 1
        return {"bins": {str(k): dict(v) for k, v in sorted(self.bins.items())}, "tools": self.ended,
                "first_tool": list(self.first_tool.values()), "appeared": self.appeared, "ended": self.n_ended,
                "still": still, "mismatch": {k: v for k, v in self.mismatch.items() if not k.startswith("_")}}


def hashrun(arm, seed, years, observe):
    setup()
    w = make_world(seed, ARMS[arm])
    obs = None
    if observe:
        obs = TF1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        res = obs.results(w)
        unk = sum(v for b in res["bins"].values() for k, v in b.items() if k == "end_all_unknown")
        extra = ":" + json.dumps({**res["mismatch"], "_appeared": res["appeared"], "_ended": res["ended"],
                                  "_unknown": unk}, sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["lp"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((501, 20), (601, 60)):
        a = call("hashrun", "lp", seed, years, 1)
        b = call("hashrun", "lp", seed, years, 0)
        same = a.split(":")[:2] == b.split(":")[:2]
        info = json.loads(a.split(":", 2)[2]) if a.count(":") >= 2 else {"?": 1}
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and not any(mism.values()) and info.get("_appeared", 0) > 0
        ok &= t
        lines.append(f"arm lp, seed {seed}, {years} years: identical with and without the observer (state and random "
                     f"numbers): {'yes' if same else 'NO'}; ledger mismatches: {mism or 'none'}; things appeared "
                     f"{info.get('_appeared')}, ended {info.get('_ended')}, unknown fates {info.get('_unknown')}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm lp, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v7 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = TF1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v7", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), **obs.results(w)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
