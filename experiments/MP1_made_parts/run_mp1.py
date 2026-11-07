"""MP1 — where do the made parts of new kinds go? (questions.md, frozen as `MP1-frozen`). Read-only: one arm on
`code_v15`, LP, seeds 24901-24932, 200 years; kinds born in years 100-190 are followed for 5 years each.

Followed kinds: world-new kinds whose recipe needs at least one made part. For each, the furthest stage reached within 5
years after its invention week by anyone who knows its recipe at a week's end:
  A  no knower holds any of its made parts        B  some, never all at once
  C  one knower holds all its made parts, but cannot make it
  D  one knower can make it at a week's end, but it is never made again
  E  it is made again (a make or play event of it after its invention week)

Tracked parts: every made thing created in a knower's hands (make, play, fire) whose kind is a made part of a followed
kind in its window. Its first fate is read by wrapping (never changing) actions._craft, actions._hold_in_fire,
matter.wear, actions._hand, actions.drop_on_ground, actions.ground_week, biology.body_phase and biology.die, and by a
weekly look at who holds it.

  python experiments/MP1_made_parts/run_mp1.py zero
  python experiments/MP1_made_parts/run_mp1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.CODES["v15"] = HERE.parent / "NV15_nature_v15" / "code_v15"
CODE = "v15"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(24901, 24933))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9907, 9908)
ARMS = {"c": dict(base.LP)}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
WIN = [100 * WPY, 190 * WPY]              # kinds born here are followed
FOLLOW = 5 * WPY
STAGES = "ABCDE"
CUR = []


def made_parts(recipe):
    from acl.matter import MATERIALS
    out = [x for x in recipe.get("parts", ()) if x not in MATERIALS]
    if recipe.get("verb") == "heat" and recipe.get("part") not in MATERIALS:
        out.append(recipe["part"])
    return out


def depth(sig, knowledge, memo, seen=()):
    if sig in memo:
        return memo[sig]
    rec = knowledge.get(sig)
    if rec is None or sig in seen:
        return 0
    parts = made_parts(rec["recipe"])
    d = 0 if not parts else 1 + max(depth(x, knowledge, memo, seen + (sig,)) for x in parts)
    memo[sig] = d
    return d


class MP1Obs:
    def __init__(self, w):
        self.w = w
        self.kinds = {}        # sig -> dict(t0, inv, parts, stage, istage, depth, other, e_events, all_seen)
        self.track = {}        # id(item) -> dict(item, sig, kinds, born, maker, close, fate, sub)
        self.fates = Counter()
        self.sub = Counter()
        self.chk = Counter()
        self.limit = Counter()
        self.memo = {}
        self.dying = set()     # ids of the tracked things a dying person held (their fate is read after die)
        self.open = set()      # ids still to watch: no fate yet, or left with a body before the window closes
        CUR[:] = [self]

    # --- helpers -------------------------------------------------------------------------------------------------
    def active_kinds_for_part(self, world, p, sig):
        t = world.tick
        return [k for k, kd in self.kinds.items()
                if t <= kd["t0"] + FOLLOW and sig in kd["parts"] and k in p.recipes]

    def start(self, world, p, item):
        if item is None or id(item) in self.track:
            return
        ks = self.active_kinds_for_part(world, p, item["sig"])
        if not ks:
            return
        self.track[id(item)] = {"item": item, "sig": item["sig"], "kinds": ks, "born": world.tick, "maker": p.id,
                                "close": max(self.kinds[k]["t0"] + FOLLOW for k in ks), "fate": None, "sub": None}
        self.open.add(id(item))
        self.chk["tracked"] += 1

    def fate(self, iid, what):
        tr = self.track.get(iid)
        if tr is None or tr["fate"] is not None:
            return
        tr["fate"] = what
        self.fates[what] += 1
        if what != "died: left with the body":
            self.open.discard(iid)

    def rekey(self, old, new_item):
        tr = self.track.pop(old)
        tr["item"] = new_item
        self.track[id(new_item)] = tr
        if old in self.open:
            self.open.discard(old)
            self.open.add(id(new_item))
        self.chk["rekeyed"] += 1

    # --- the week ------------------------------------------------------------------------------------------------
    def __call__(self, world, events):
        from acl.mind import can_make
        tick = world.tick - 1
        for ev in events:
            if ev["k"] not in ("make", "play") or ev.get("thing") is None:
                continue
            sig = ev["thing"]
            kd = self.kinds.get(sig)
            if kd is not None:
                if kd["t0"] < tick <= kd["t0"] + FOLLOW:
                    kd["e_events"] += 1
                    kd["stage"] = 4
                    if ev.get("a") == kd["inv"]:
                        kd["istage"] = 4
                    else:
                        kd["other"] = 1
                continue
            rec = world.knowledge.get(sig)
            if rec is not None and rec.get("first_tick") == tick and rec.get("first_by") == ev.get("a") \
                    and WIN[0] <= tick < WIN[1]:
                parts = made_parts(rec["recipe"])
                if parts:
                    self.kinds[sig] = {"t0": tick, "inv": ev.get("a"), "parts": Counter(parts), "stage": 0,
                                       "istage": 0, "depth": depth(sig, world.knowledge, self.memo), "other": 0,
                                       "e_events": 0, "all_seen": 0}
        living = world.living()
        held = {}
        for p in living:
            for it in p.items:
                held[id(it)] = p.id
        ground = {id(g["item"]) for g in world.ground}
        # stages
        active = {k: kd for k, kd in self.kinds.items() if kd["t0"] < tick <= kd["t0"] + FOLLOW}
        if active:
            lim = world.cfg.item_limit
            for p in living:
                ks = [k for k in p.recipes if k in active]
                if not ks:
                    continue
                have = Counter(it["sig"] for it in p.items)
                at_limit = len(p.items) >= lim
                for k in ks:
                    kd = active[k]
                    self.limit["knower_weeks"] += 1
                    self.limit["knower_weeks_at_limit"] += int(at_limit)
                    need = kd["parts"]
                    st = 0
                    if any(have[x] > 0 for x in need):
                        st = 1
                    if all(have[x] >= n for x, n in need.items()):
                        st = 2
                        kd["all_seen"] += 1
                    if st == 2 and can_make(p, p.recipes[k]):
                        st = 3
                    kd["stage"] = max(kd["stage"], st)
                    if p.id == kd["inv"]:
                        kd["istage"] = max(kd["istage"], st)
        # weekly look: unfated tracked items must be held or on the ground; sub-fates of dropped and bodies' items
        for iid in list(self.open):
            tr = self.track[iid]
            if tr["fate"] is None:
                if world.tick > tr["close"]:
                    self.fate(iid, "still held" if iid in held or iid in ground else "unexplained")
                    if self.track[iid]["fate"] == "unexplained":
                        self.chk["unexplained"] += 1
                elif iid not in held and iid not in ground:
                    self.fate(iid, "unexplained")
                    self.chk["unexplained"] += 1
                continue
            if tr["sub"] is None and tr["fate"] == "died: left with the body" and iid in held:
                tr["sub"] = "taken from the body"
                self.sub["taken from the body"] += 1
            if tr["sub"] is not None or world.tick > tr["close"]:
                self.open.discard(iid)

    def results(self):
        out = Counter()
        for kd in self.kinds.values():
            s, i = STAGES[kd["stage"]], STAGES[kd["istage"]]
            out[f"stage_{s}"] += 1
            out[f"inv_stage_{i}"] += 1
            d = min(kd["depth"], 3)
            out[f"depth{d}_stage_{s}"] += 1
            out["kinds"] += 1
            out["made_other"] += kd["other"]
            if s == "E" and kd["e_events"] == 0:
                self.chk["stage_E_without_event"] += 1
            if s in ("C", "D") and kd["all_seen"] == 0:
                self.chk["stage_CD_without_all"] += 1
        self.chk["open_at_end"] = sum(1 for tr in self.track.values() if tr["fate"] is None)
        drops = [tr for tr in self.track.values() if tr["fate"] == "dropped at the carry limit"]
        for tr in drops:
            if tr["sub"] is None:
                self.sub["dropped: still on the ground or gone"] += 1
        return {"stages": dict(out), "fates": dict(self.fates), "sub": dict(self.sub), "limit": dict(self.limit),
                "check": dict(self.chk), "n_tracked": len(self.track)}


def install():
    from acl import actions, biology, matter
    if getattr(actions, "_mp1", False):
        return
    actions._mp1 = True
    craft0, fire0, wear0 = actions._craft, actions._hold_in_fire, matter.wear
    hand0, drop0, ground0 = actions._hand, actions.drop_on_ground, actions.ground_week
    body0, die0 = biology.body_phase, biology.die

    def obs():
        return CUR[0] if CUR else None

    def craft(world, p, recipe):
        o = obs()
        if o is None:
            return craft0(world, p, recipe)
        before = [id(it) for it in p.items]
        item = craft0(world, p, recipe)
        after = {id(it) for it in p.items}
        into = item["sig"] if item is not None else None
        for iid in before:
            if iid not in after and iid in o.track and o.track[iid]["fate"] is None:
                ks = o.track[iid]["kinds"]
                o.fate(iid, "used: into its kind" if into in ks else "used: into another thing")
        if item is not None:
            o.start(world, p, item)
            if id(item) in o.track and id(item) not in after and o.track[id(item)]["fate"] is None                     and any(g["item"] is item for g in world.ground):
                v = p.itemval.get(item["sig"], 0.0)
                o.limit["drops_tracked"] += 1
                o.limit["drops_new_at_once"] += 1
                o.limit["drops_least_valued"] += int(v <= min((p.itemval.get(it["sig"], 0.0) for it in p.items),
                                                             default=v))
                o.limit["drops_valued_zero"] += int(v <= 0.0)
                o.fate(id(item), "dropped at the carry limit")
                o.track[id(item)]["dropper"] = p.id
        return item

    def fire(world, p, part):
        o = obs()
        if o is None:
            return fire0(world, p, part)
        before = [(id(it), it["sig"]) for it in p.items]
        out = fire0(world, p, part)
        now = {id(it): it for it in p.items}
        old_ids = {i for i, _ in before}
        for iid, sig in before:
            if iid in now or iid not in o.track:
                continue
            same = [it for i, it in now.items() if i not in old_ids and it["sig"] == sig]
            if same and out is None:
                o.rekey(iid, same[0])                  # only dried: the same thing, a new record
            elif out is not None:
                ks = o.track[iid]["kinds"]
                o.fate(iid, "used: into its kind" if out["sig"] in ks else "used: into another thing")
            else:
                o.fate(iid, "used: lost in a fire")
        if out is not None:
            o.start(world, p, out)
        return out

    def wear(p, index):
        o = obs()
        if o is None or index < 0:
            return wear0(p, index)
        it = p.items[index]
        wear0(p, index)
        if not any(x is it for x in p.items):
            o.fate(id(it), "worn out in use")

    def hand(world, p, q):
        o = obs()
        if o is None:
            return hand0(world, p, q)
        before = [id(it) for it in p.items]
        out = hand0(world, p, q)
        qs = {id(it) for it in q.items}
        for iid in before:
            if iid in qs:
                o.fate(iid, "handed to another")
        return out

    def drop(world, p, item):
        o = obs()
        if o is not None and id(item) in o.track and id(item) not in o.dying:
            if o.track[id(item)]["fate"] is None:
                v = p.itemval.get(item["sig"], 0.0)
                o.limit["drops_tracked"] += 1
                o.limit["drops_least_valued"] += int(v <= min((p.itemval.get(it["sig"], 0.0) for it in p.items),
                                                             default=v))
                o.limit["drops_valued_zero"] += int(v <= 0.0)
            o.fate(id(item), "dropped at the carry limit")
            o.track[id(item)]["dropper"] = p.id
        return drop0(world, p, item)

    def ground(world):
        o = obs()
        if o is None:
            return ground0(world)
        lying = {id(g["item"]) for g in world.ground}
        out = ground0(world)
        still = {id(g["item"]) for g in world.ground}
        picked = lying - still
        if picked:
            holder = {id(it): p.id for p in world.living() for it in p.items}
            for iid in picked:
                tr = o.track.get(iid)
                if tr is None or tr["fate"] != "dropped at the carry limit" or tr["sub"] is not None:
                    continue
                who = holder.get(iid)
                tr["sub"] = "picked up by the one who dropped it" if who == tr.get("dropper") else \
                    "picked up by someone else"
                o.sub[tr["sub"]] += 1
        return out

    def body(world, *a, **k):
        o = obs()
        if o is None:
            return body0(world, *a, **k)
        before = {p.id: [(i, id(it), it["sig"]) for i, it in enumerate(p.items)] for p in world.living()}
        out = body0(world, *a, **k)
        for pid, lst in before.items():
            p = world.people[pid]
            if not p.alive:
                continue
            now = {id(it) for it in p.items}
            for i, iid, sig in lst:
                if iid in now or iid not in o.track or o.track[iid]["fate"] is not None:
                    continue
                rep = p.items[i] if i < len(p.items) else None
                if rep is not None and id(rep) not in {x[1] for x in lst} and rep["sig"] != sig:
                    ks = o.track[iid]["kinds"]
                    o.fate(iid, "used: into its kind" if rep["sig"] in ks else "used: into another thing")
                else:
                    o.fate(iid, "worn out by the cold")
        return out

    def die(world, p, cause, killer):
        o = obs()
        if o is None:
            return die0(world, p, cause, killer)
        mine = [id(it) for it in p.items if id(it) in o.track]
        o.dying = set(mine)
        try:
            out = die0(world, p, cause, killer)
        finally:
            o.dying = set()
        if mine:
            held = {id(it) for q in world.living() for it in q.items}
            ground = {id(g["item"]) for g in world.ground}
            for iid in mine:
                o.fate(iid, "died: passed to an heir" if (iid in held or iid in ground) else "died: left with the body")
        return out

    actions._craft, actions._hold_in_fire, matter.wear = craft, fire, wear
    actions._hand, actions.drop_on_ground, actions.ground_week = hand, drop, ground
    biology.body_phase, biology.die = body, die


def make(seed, arm="c", code=CODE):
    base.setup(code)
    return base.make_world(seed, dict(ARMS[arm]))


def hashrun(code, seed, years, observe):
    WIN[0], WIN[1] = 0, (years - 5) * WPY   # zero checks: kinds from the start, each window closed by the end
    w = make(seed, "c", code)
    obs = None
    if observe:
        install()
        obs = MP1Obs(w)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"stages": {k: v for k, v in r["stages"].items() if k.startswith("stage_")},
                                  "fates": r["fates"], "sub": r["sub"], "check": r["check"]},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


def reload_check(seed):
    w = make(seed)
    from acl.world import World
    for _ in range(10 * WPY):
        w.step()
    b = World.from_dict(json.loads(json.dumps(w.to_dict())))
    for x in (w, b):
        for _ in range(5 * WPY):
            x.step()
    return base.world_hash(w) == base.world_hash(b)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.strip().splitlines()[-1]

    def hs(x):
        return x.split(":")[:2]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (0, 1)]
    with ThreadPoolExecutor(2) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", CODE, *sp), specs)))
        acc = ex.submit(call, "hashrun", CODE, 701, 30, 1)
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0)]) == hs(got[(seed, years, 1)])
        ok &= ro
        lines.append(f"seed {seed}, {years} years: observer read-only (world and random stream): {'yes' if ro else 'NO'}; "
                     f"{got[(seed, years, 1)].split(':', 2)[2]}")
    info = json.loads(acc.result().split(":", 2)[2])
    ch = info["check"]
    t = (ch.get("tracked", 0) > 0 and ch.get("unexplained", 0) == 0 and ch.get("stage_E_without_event", 0) == 0
         and ch.get("stage_CD_without_all", 0) == 0 and ch.get("open_at_end", 0) == 0
         and sum(info["fates"].values()) == ch.get("tracked", 0))
    ok &= t
    lines.append(f"seed 701, 30 years: fate accounting (every tracked part has exactly one first fate or 'still held'; "
                 f"none gone unexplained) and stage checks: {'yes' if t else 'NO'}; {info}")
    t = rl.result()[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v15 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = make(seed, arm)
    install()
    obs = MP1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v15", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, check {res['check']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "reload":
        base.setup(CODE)
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":                  # a code test of the analysis only: kinds from the start; never study data
        WIN[0], WIN[1] = 0, (int(sys.argv[4]) - 5) * WPY
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
