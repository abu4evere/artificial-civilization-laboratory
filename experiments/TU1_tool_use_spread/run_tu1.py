"""TU1 — how tool use is learned, and whether it spreads (questions.md, frozen as `TU1-frozen`). Read-only.

FX3's tool arms (S25, B50) on seeds 7301-7556, replayed exactly with FX2's frozen code (`code_fx2`) and a read-only
weekly observer; no logging copy is needed. A "tool use" is an `open_food` event with a hard thing in hand (hard > 0)
that got food. For each person's FIRST tool use, the route (first that applies):

  told       before that week, they had heard an opinion of that item's kind ("m:<sig>" in their heard)
  received   the item came to them from another person: in ACL that is only inheritance (an `inherit` event in the
             week the item first appeared in their hands; items are never handed over otherwise)
  own        they came by the item themselves (made it, or it hardened in a fire) and had heard nothing of it

and whether, in the 13 weeks before, anyone within perception used a tool on embedded food (and whether that person
was kin). Each replay's final state hash must equal FX3's saved one.

  python experiments/TU1_tool_use_spread/run_tu1.py zero
  python experiments/TU1_tool_use_spread/run_tu1.py one <arm> <seed> <years> <out>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "FX3_gentler_embedded"))
import run_fx3 as F  # noqa: E402  (FX3's frozen runner: settings, world builder)

OUT = HERE / "output"
SAVED = EXP / "FX3_gentler_embedded" / "output"
WPY, YEARS = 52, 120
SEEDS = F.SEEDS
SMOKE_SEEDS = (9921, 9922)
ARMS = {"s25": F.ARMS["s25"], "b50": F.ARMS["b50"]}
ROUTES = ("told", "received", "own")


class Spread:
    """Read-only: reads the week's events and the world after each week; changes nothing in the world."""

    def __init__(self):
        self.heard_before = {}      # person -> set of heard item kinds as of the end of last week
        self.held = {}              # person -> item kinds in hand at the end of last week
        self.origin = {}            # (person, kind) -> "inherited" or "own", when the kind first appeared in their hands
        self.first = {}             # person -> week of first tool use
        self.uses = Counter()       # person -> weeks with a tool use
        self.last_use = {}          # person -> (tick, loc) of their latest tool use
        self.routes = Counter()
        self.seen_before = Counter()   # first uses with someone in sight using in the 13 weeks before (and kin)
        self.decade_users = {}      # decade -> share of adults who have ever used
        self.span = []              # weeks between first and last use, per user (filled at the end)
        self.last_tick = {}

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick - 1
        heirs = {e["a"] for e in events if e["k"] == "inherit" and e.get("a")}
        users = []
        for e in events:
            if e["k"] == "open_food" and e.get("hard", 0) > 0 and e.get("got", 0) > 0:
                users.append(e["a"])
        for pid in users:
            p = world.people[pid]
            self.uses[pid] += 1
            self.last_tick[pid] = tick
            if pid not in self.first:
                self.first[pid] = tick
                item = max(p.items, key=lambda it: it["hard"]) if p.items else None
                sig = item["sig"] if item else None
                if sig and sig in self.heard_before.get(pid, set()):
                    route = "told"
                elif sig and self.origin.get((pid, sig)) == "inherited":
                    route = "received"
                else:
                    route = "own"
                self.routes[route] += 1
                near = [q for q, (t, loc) in self.last_use.items() if q != pid and tick - t <= 13
                        and distance(p.loc, loc, c.width, c.height) <= c.perception]
                if near:
                    self.seen_before["someone"] += 1
                    if any(world.kinship(p, world.people[q]) > 0 for q in near):
                        self.seen_before["kin"] += 1
                else:
                    self.seen_before["nobody"] += 1
            self.last_use[pid] = (tick, p.loc)
        living = world.living()
        for p in living:
            now = {it["sig"] for it in p.items}
            for sig in now - self.held.get(p.id, set()):
                self.origin.setdefault((p.id, sig), "inherited" if p.id in heirs else "own")
            self.held[p.id] = now
        self.heard_before = {p.id: {k[2:] for k in p.heard if k.startswith("m:")} for p in living}
        if tick % 520 == 519:
            adults = [p for p in living if p.age(world.tick) >= 16 * WPY]
            if adults:
                self.decade_users[tick // 520] = round(sum(1 for p in adults if p.id in self.first) / len(adults), 4)

    def results(self):
        spans = [self.last_tick[p] - self.first[p] for p in self.first]
        return {"first_users": len(self.first), "routes": dict(self.routes), "seen_before": dict(self.seen_before),
                "uses_per_user": sorted(self.uses.values()), "spans": sorted(spans),
                "decade_users": self.decade_users}


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def hashrun(seed, years, arm, observe):
    F.setup("fx2")
    w = F.make_world(seed, ARMS[arm])
    if observe:
        w.observers.append(Spread())
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
    for arm in ARMS:
        for seed in (501, 601):
            t = call(seed, 20, arm, 1) == call(seed, 20, arm, 0)
            ok &= t
            lines.append(f"arm {arm}, seed {seed}, 20 years: identical with and without the observer: {'yes' if t else 'NO'}")
    F.setup("fx2")
    lines.append(f"code_fx2 fingerprint: {F.fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years, out):
    F.setup("fx2")
    f0 = F.fingerprint()
    w = F.make_world(seed, ARMS[arm])
    obs = Spread()
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code_hash": f0, "code_hash_after": F.fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), **obs.results()}
    saved = SAVED / f"{arm}_seed_{seed}.json"
    if saved.exists() and years == YEARS:
        res["reproduces"] = json.loads(saved.read_text(encoding="utf-8"))["world_hash"] == res["world_hash"]
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: reproduces {res.get('reproduces')}, first users {len(obs.first)}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5] == "1"))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
