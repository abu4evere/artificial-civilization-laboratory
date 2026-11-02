"""HA1 — why does handing stay rare? (questions.md, frozen as `HA1-frozen`). Read-only on live nature v11
(`experiments/NV11_nature_v11/code_v11`, unchanged). ES2's runner supplies the world set-up (`setup`, `make_world`,
hashes); the observer here is HA1's own:
  thought.steer   every decision that reaches the choice, by a person holding a made thing: the funnel (someone near
                  with room; someone with net > 0; a handing option; the softmax mass on handing options), by relation,
                  and the best handing score against the top score
  events          every hand (giver, receiver, kind, relation, whether the receiver knew the kind) and every make
                  (maker, kind); a yearly count of made things held, by holder age
A handing is checked against the decisions seen: it must come from a decision with a handing option to that receiver.

  python experiments/HA1_handing_audit/run_ha1.py zero
  python experiments/HA1_handing_audit/run_ha1.py one h <seed> <years> <out>
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

CODE = "v11"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(21601, 21633))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9979, 9978)
ARMS = {"h": dict(base.LP)}               # live v11 as it is (hand_items 1 is v11's default)
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
LATE = (100 * WPY, 200 * WPY)
CHILD, ADULT = 12 * WPY, 16 * WPY


def age_group(weeks):
    return "child" if weeks < CHILD else ("12-15" if weeks < ADULT else "16+")


def holder_group(weeks):
    return "child" if weeks < CHILD else ("12-15" if weeks < ADULT else ("16-59" if weeks < 60 * WPY else "60+"))


class HA1Obs:
    def __init__(self, w, late=LATE):
        self.w = w
        self.late = late
        self.mismatch = Counter()
        self.s = defaultdict(float)
        self.by = defaultdict(lambda: [0, 0, 0, 0, 0.0, 0.0, 0.0])   # giver age group -> [decisions, room, net,
        #   option, mass, best-hand score gap sum (top - best hand, over decisions with an option), options seen]
        self.rel = defaultdict(lambda: [0, 0.0])            # relation -> [handing options, mass]
        self.seen = set()                                   # (tick, giver, receiver) with a handing option
        self.hands = []                                     # [tick, receiver, kind, relation, knew]
        self.makes = []                                     # [tick, maker, kind]
        self.holders = defaultdict(int)                     # holder age group -> made things held (yearly census)

    def relation(self, world, p, q):
        if p.partner == q.id:
            return "partner"
        return "kin" if world.kinship(p, q) > 0 else "other"

    def decision(self, world, p, options):
        if not p.items or not options:
            return
        tick = world.tick
        if not (self.late[0] <= tick < self.late[1]):
            # outside the counted years: still note handing options, for the handing check
            for o in options:
                if o[1] == "give" and world.hand_intent.get((p.id, o[2])):
                    self.seen.add((tick, p.id, o[2]))
            return
        from acl.mind import hand_pick
        from acl.util import distance
        c = world.cfg
        near = world.people_near(p.loc, c.reach, exclude=p.id)
        near.sort(key=lambda q: (distance(p.loc, q.loc, c.width, c.height), q.id))
        near = near[:12]
        room = [q for q in near if len(q.items) < c.item_limit]
        has_net = any(hand_pick(p, q)[0] > 0.0 for q in room)
        top = max(o[0] for o in options)
        wts = [math.exp((o[0] - top) / c.choice_temperature) for o in options]
        tot = sum(wts)
        mass, best, n_opt = 0.0, None, 0
        for wt, o in zip(wts, options):
            if o[1] == "give" and world.hand_intent.get((p.id, o[2])):
                n_opt += 1
                mass += wt / tot
                best = o[0] if best is None else max(best, o[0])
                self.seen.add((tick, p.id, o[2]))
                q = world.people.get(o[2])
                r = self.rel[self.relation(world, p, q) if q is not None else "other"]
                r[0] += 1
                r[1] += wt / tot
        b = self.by[age_group(p.age(tick))]
        b[0] += 1
        b[1] += bool(room)
        b[2] += has_net
        b[3] += n_opt > 0
        b[4] += mass
        if best is not None:
            b[5] += top - best
        b[6] += n_opt

    def __call__(self, world, events):
        tick = world.tick - 1
        late = self.late[0] <= tick < self.late[1]
        for ev in events:
            k = ev["k"]
            if k == "hand":
                if (ev["t"], ev.get("a"), ev.get("b")) not in self.seen:
                    self.mismatch["hand_unseen"] += 1
                if late:
                    p, q = world.people.get(ev.get("a")), world.people.get(ev.get("b"))
                    kind = ev.get("thing")
                    knew = int(q is not None and kind in q.recipes)
                    rel = self.relation(world, p, q) if p is not None and q is not None else "other"
                    self.hands.append([ev["t"], ev.get("b"), kind, rel, knew])
                    self.s["hands"] += 1
            elif k == "make" and late:
                self.makes.append([ev["t"], ev.get("a"), ev.get("thing")])
        self.seen = {x for x in self.seen if x[0] >= tick}
        if late and tick % WPY == WPY - 1:
            for p in world.living():
                if p.items:
                    self.holders[holder_group(p.age(world.tick))] += len(p.items)
            self.s["adult_years"] += sum(1 for p in world.living() if p.age(world.tick) >= ADULT)

    def results(self):
        return {"by_fields": ["decisions", "room", "net", "option", "mass", "gap_sum", "options"],
                "by": {k: v for k, v in self.by.items()}, "rel_fields": ["options", "mass"], "rel": dict(self.rel),
                "hands_fields": ["tick", "receiver", "kind", "relation", "knew"], "hands": self.hands,
                "makes_fields": ["tick", "maker", "kind"], "makes": self.makes, "holders": dict(self.holders),
                "sums": dict(self.s), "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import thought
    o_steer = thought.steer

    def steer(p, options):
        out = o_steer(p, options)
        if w.people.get(p.id) is p:
            obs.decision(w, p, out)
        return out
    thought.steer = steer


def hashrun(seed, years, observe):
    base.setup(CODE)
    w = base.make_world(seed, ARMS["h"])
    obs = None
    if observe:
        obs = HA1Obs(w, late=(0, years * WPY))       # zero checks: every year counted
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        dec = sum(v[0] for v in obs.by.values())
        extra = ":" + json.dumps({**obs.mismatch, "_decisions": dec, "_hands": obs.s["hands"]},
                                 sort_keys=True, separators=(",", ":"))
    return base.world_hash(w) + ":" + base.rng_state(w) + extra


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
    specs = [(seed, years, obs) for seed, years in ((501, 20), (601, 60)) for obs in (0, 1)]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
    for seed, years in ((501, 20), (601, 60)):
        off, on = got[(seed, years, 0)], got[(seed, years, 1)]
        ro = hs(off) == hs(on)
        info = json.loads(on.split(":", 2)[2])
        mism = {k: v for k, v in info.items() if not k.startswith("_")}
        t = ro and not any(mism.values()) and info["_decisions"] > 0 and (info["_hands"] > 0 or years < 60)
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only: {'yes' if ro else 'NO'}; mismatches (a handing "
                     f"not seen as an option): {mism or 'none'}; item-holding decisions seen {info['_decisions']}; "
                     f"handings {info['_hands']:.0f}")
    lines.append(f"code_v11 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    obs = HA1Obs(w)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v11", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "world_hash": base.world_hash(w), **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, mismatches {res['mismatch']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1"))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
