"""HD1 — can a person hand a made thing to another? (questions.md, frozen as `HD1-frozen`). A nature-change test in a
copy: `code_hd1` = `code_v10` + `hand_items` (0 = v10). Arms v10 (hand_items 0), h (hand_items 1), x (sham).
The observer is read-only: TR1's forage wrapper (food with, and without, the tool in hand), a wrapper on `_hand` that
checks conservation, and the law's events (`hand`, `give`, `death`) with a yearly census.

  python experiments/HD1_handing/run_hd1.py zero
  python experiments/HD1_handing/run_hd1.py one <arm> <seed> <years> <out>
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
CODES = {"hd1": HERE / "code_hd1", "v10": EXP / "NV10_nature_v10" / "code_v10"}
OUT = HERE / "output"
WPY, YEARS = 52, 200
SEEDS = tuple(range(21201, 21233))        # 32 new paired seeds, used by no study
SMOKE_SEEDS = (9997, 9996)
V10 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
LP = {"founders": 80, "width": 80, "height": 80}
ARMS = {"c": {**LP, "hand_items": 0}, "h": {**LP, "hand_items": 1}, "x": {**LP, "sham_draw": 1}}   # c = v10
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
LATE = (100 * WPY, 200 * WPY)
ADULT = 16 * WPY
CHILD_END = 12 * WPY


def setup(code="hd1"):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **{**V10, **kw}))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def rng_state(w):
    return hashlib.sha256(repr(w.rng.getstate()).encode()).hexdigest()


def fingerprint(code="hd1"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


def forage_got(rate, eff, room, crop, plants):
    """`actions._forage`'s own arithmetic (TR1)."""
    want = min(rate * eff, room)
    from_crop = min(crop, want * 1.3)
    from_wild = min(plants, max(0.0, want - from_crop / 1.3))
    return from_crop + from_wild


class HD1Obs:
    def __init__(self, w):
        self.w = w
        self.mismatch = Counter()
        self.s = defaultdict(float)             # late sums (adults unless named)
        self.recent = {}                        # receiver -> tick of the last item received
        self.handed = []                        # recent handings: (tick, giver, receiver, sig)
        self.census = []                        # [year, living, adults, children, recipes_adults]

    def before_forage(self, world, p, eff):
        from acl.matter import best_item, carry_capacity
        from acl.mind import forage_rate
        tile = world.tile(p.loc)
        idx, tf = best_item(p, "forage")
        rate = forage_rate(world, p)
        room = max(0.0, carry_capacity(world, p) - p.edible())
        return {"tf": tf, "with": forage_got(rate, eff, room, tile.crop, tile.plants),
                "without": forage_got(rate / tf, eff, room, tile.crop, tile.plants), "food0": p.food + p.seeds}

    def after_forage(self, world, p, info):
        actual = p.food + p.seeds - info["food0"]
        if not p.alive:
            self.s["died_in_forage"] += 1
        elif abs(actual - info["with"]) > 1e-9:
            self.mismatch["forage_replay"] += 1
        if not (LATE[0] <= world.tick < LATE[1]) or p.age(world.tick) < ADULT:
            return
        s = self.s
        s["forage_weeks"] += 1
        s["with"] += info["with"]
        s["without"] += info["without"]
        tool = info["tf"] > 1.0 + 1e-12
        s["tool_weeks"] += tool
        t0 = self.recent.get(p.id)
        if t0 is not None and world.tick - t0 <= WPY:
            s["recipient_forage_weeks"] += 1
            s["recipient_tool_weeks"] += tool

    def handed_check(self, p, q, n_p, n_q):
        if len(p.items) != n_p - 1 or len(q.items) != n_q + 1:
            self.mismatch["conservation"] += 1

    def __call__(self, world, events):
        tick = world.tick - 1
        late = LATE[0] <= tick < LATE[1]
        for ev in events:
            k = ev["k"]
            if k == "hand":
                self.s["hands_all"] += 1
                g, r, sig = ev.get("a"), ev.get("b"), ev.get("thing")
                if any(t >= tick - 4 and gg == r and rr == g and ss == sig for t, gg, rr, ss in self.handed):
                    self.s["reversals"] += late
                self.handed.append((tick, g, r, sig))
                self.recent[r] = tick
                if late:
                    self.s["hands"] += 1
            elif k == "give" and late:
                self.s["food_gifts"] += 1
            elif k == "death" and late:
                if ev.get("age", 99) < 12:
                    self.s["child_deaths"] += 1
        self.handed = [h for h in self.handed if h[0] >= tick - 4]
        if late:
            living = world.living()
            self.s["adult_weeks"] += sum(1 for p in living if p.age(world.tick) >= ADULT)
            self.s["child_weeks"] += sum(1 for p in living if p.age(world.tick) < CHILD_END)
            self.s["living_weeks"] += len(living)
        if tick % WPY == WPY - 1:
            living = world.living()
            adults = [p for p in living if p.age(world.tick) >= ADULT]
            self.census.append([tick // WPY, len(living), len(adults),
                                sum(1 for p in living if p.age(world.tick) < CHILD_END),
                                sum(len(p.recipes) for p in adults)])

    def results(self):
        return {"sums": dict(self.s), "mismatch": dict(self.mismatch),
                "census_fields": ["year", "living", "adults", "children", "recipes_adults"], "census": self.census}


def install(w, obs, code="hd1"):
    from acl import actions
    orig_forage = actions.HANDLERS["forage"]

    def forage(world, p, target, eff):
        if world is not w:
            return orig_forage(world, p, target, eff)
        info = obs.before_forage(world, p, eff)
        out = orig_forage(world, p, target, eff)
        obs.after_forage(world, p, info)
        return out

    actions.HANDLERS["forage"] = forage
    if hasattr(actions, "_hand"):
        orig_hand = actions._hand

        def _hand(world, p, q):
            n_p, n_q = len(p.items), len(q.items)
            before = len(world.events)
            out = orig_hand(world, p, q)
            if world is w and len(world.events) > before and world.events[-1]["k"] == "hand":
                obs.handed_check(p, q, n_p, n_q)
            return out

        actions._hand = _hand


def hashrun(code, arm, seed, years, observe):
    setup(code)
    kw = dict(ARMS[arm])
    if code == "v10":
        kw.pop("hand_items", None)
    w = make_world(seed, kw)
    obs = None
    if observe:
        obs = HD1Obs(w)
        install(w, obs, code)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        extra = ":" + json.dumps({**obs.mismatch, "_hands": obs.s["hands_all"], "_forages": obs.s["forage_weeks"]},
                                 sort_keys=True, separators=(",", ":"))
    return world_hash(w) + ":" + rng_state(w) + extra


def reload_check(seed):
    setup()
    from acl.world import World
    a = make_world(seed, ARMS["h"])
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for x in (a, b):
        for _ in range(5 * WPY):
            x.step()
    return world_hash(a) == world_hash(b) and b.cfg.hand_items == 1


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-3000:])
        return r.stdout.split()[-1]

    def hs(x):
        return x.split(":")[:2]
    lines, ok = [], True
    from concurrent.futures import ThreadPoolExecutor
    specs = [(code, arm, seed, years, obs) for seed, years in ((501, 20), (601, 60))
             for code, arm, obs in (("v10", "c", 0), ("hd1", "c", 0), ("hd1", "h", 1), ("hd1", "h", 0), ("hd1", "x", 0))]
    with ThreadPoolExecutor(5) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        v10 = got[("v10", "c", seed, years, 0)]
        c0 = got[("hd1", "c", seed, years, 0)]
        h1 = got[("hd1", "h", seed, years, 1)]
        h0 = got[("hd1", "h", seed, years, 0)]
        x0 = got[("hd1", "x", seed, years, 0)]
        same = hs(v10) == hs(c0)
        ro = hs(h1) == hs(h0)
        acts = hs(h0) != hs(c0)
        sham = hs(x0) != hs(c0)
        info = json.loads(h1.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = same and ro and acts and sham and not any(mism.values()) and info.get("_hands", 0) > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_hd1 with hand_items 0 = code_v10: {'yes' if same else 'NO'}; "
                     f"observer read-only (arm h): {'yes' if ro else 'NO'}; the law acts: {'yes' if acts else 'NO'}; "
                     f"the sham acts: {'yes' if sham else 'NO'}; conservation and replay mismatches: {mism or 'none'}; "
                     f"handings (arm h) {info.get('_hands'):.0f}")
    r = subprocess.run(me + ["reload", "501"], capture_output=True, text=True)
    t = r.stdout.split()[-1:] == ["True"]
    ok &= t
    lines.append(f"arm h, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_hd1 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup()
    f0 = fingerprint()
    w = make_world(seed, ARMS[arm])
    obs = HD1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_hd1", "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        setup()
        print(fingerprint())
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
