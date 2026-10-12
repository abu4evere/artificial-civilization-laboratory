"""LK1 — location knowledge (questions.md, frozen as `LK1-frozen`). Arms C (loved_location "current"), M ("last_seen"),
S (sham), in `code_lk1` (code_p2 with every P2/MC1 setting off, plus AA1's logging hooks and the one new setting).

  python experiments/LK1_location_knowledge/run_lk1.py zero    # hard stops: copy == control; logging leaves it unchanged
  python experiments/LK1_location_knowledge/run_lk1.py pilot   # manipulation check: seeds 9201-9204, 10 years, C and M
  python experiments/LK1_location_knowledge/run_lk1.py run     # C, M, S on seeds 4001-4256, 120 years

Observers (read-only): F1's probe (population at decade marks, births, rates; as every study), AA1's audit (go-to moves by
the branch that offered them: "loved" = toward a loved one's current tile, "loved_mem" = toward where they were last seen,
"seek" = partner search), and Bonds below (pairings, weeks to pairing, separation).
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
CODES = {"lk1": HERE / "code_lk1", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(4001, 4257))
PILOT = tuple(range(9201, 9205))
ARMS = {"c": {"loved_location": "current"}, "m": {"loved_location": "last_seen"},
        "s": {"loved_location": "current", "sham_draw": 1}}


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    for d in ("E7_passive", "F1_baseline_fragility", "AA1_artifact_audit"):
        sys.path.insert(1, str(EXP / d))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed, **kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint():
    from run_e7 import code_hash
    return code_hash(CODES["lk1"] / "acl")


class Bonds:
    """Pairings, weeks to pairing, and separation, read from the world after each week. Writes nothing to it."""

    def __init__(self):
        self.n = Counter()
        self.since = {}        # person -> week they became an eligible single (this spell)
        self.wait = []         # weeks from becoming an eligible single to pairing
        self.apart = {}        # bond key -> current spell length (weeks apart)
        self.spells = {"partner": [], "mother_child": []}

    def __call__(self, world, events):
        c, t, n = world.cfg, world.tick, self.n
        living = world.living()
        for e in events:
            if e["k"] == "pair":
                n["pairings"] += 1
                for pid in (e["a"], e.get("b")):
                    if pid in self.since:
                        self.wait.append(t - self.since.pop(pid))
        for p in living:
            if p.age(t) >= 16 * WPY and p.partner is None:
                n["single_weeks"] += 1
                self.since.setdefault(p.id, t)
            else:
                self.since.pop(p.id, None)
        bonds = []
        for p in living:
            if p.partner and p.id < p.partner and world.people[p.partner].alive:
                bonds.append(("partner", p.id, p.partner))
            if p.sex == "F":
                for cid in p.children:
                    ch = world.people[cid]
                    if ch.alive and ch.age(t) < 16 * WPY:
                        bonds.append(("mother_child", p.id, cid))
        live_keys = set()
        for kind, a, b in bonds:
            key = (kind, a, b)
            live_keys.add(key)
            pa, pb = world.people[a], world.people[b]
            from acl.util import distance
            out = distance(pa.loc, pb.loc, c.width, c.height) > c.perception
            n[f"{kind}_weeks"] += 1
            n[f"{kind}_weeks_apart"] += out
            if out:
                self.apart[key] = self.apart.get(key, 0) + 1
            elif key in self.apart:
                self.spells[kind].append(self.apart.pop(key))
        for key in [k for k in self.apart if k not in live_keys]:   # the bond ended while apart
            self.spells[key[0]].append(self.apart.pop(key))

    def results(self):
        for key in list(self.apart):
            self.spells[key[0]].append(self.apart.pop(key))
        return {"n": dict(self.n), "wait": self.wait, "spells": self.spells}


def attach(w):
    from run_f1 import Probe as F1Probe
    from run_aa1 import Audit
    f1p, audit, bonds = F1Probe(), Audit(), Bonds()
    w.aa1log = audit.buf
    w.observers += [f1p, audit, bonds]
    return f1p, audit, bonds


def hash_run(code, seed, years, kw, log):
    setup(code)
    w = make_world(seed, **kw)
    if log:
        attach(w)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(code, seed, kw, log):
        out = subprocess.run(me + ["hashrun", code, str(seed), json.dumps(kw), "1" if log else "0"],
                             capture_output=True, text=True).stdout
        return out.strip().splitlines()[-1]
    lines, ok, base = [], True, {}
    for seed in (11, 501):
        base[seed] = call("e13r", seed, {}, False)
        for log in (False, True):
            t = base[seed] == call("lk1", seed, ARMS["c"], log)
            ok &= t
            lines.append(f"loved_location current, observers {'on' if log else 'off'}, seed {seed}, 20 years: "
                         f"reproduces the control world: {'yes' if t else 'NO'}")
    for arm in ("m", "s"):
        t = call("lk1", 11, ARMS[arm], True) != base[11]
        ok &= t
        lines.append(f"arm {arm}, seed 11, 20 years: the world differs from the control: {'yes' if t else 'NO'}")
    setup("lk1")
    lines.append(f"code_lk1 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    setup("lk1")
    f0 = fingerprint()
    w = make_world(seed, **ARMS[arm])
    f1p, audit, bonds = attach(w)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "years": years, "code_hash": f0, "code_hash_after": fingerprint(),
           "final_tick": w.tick, "world_hash": world_hash(w), "audit": audit.results(), "bonds": bonds.results(),
           **f1p.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: alive {len(w.living())}, pops {f1p.pops}", flush=True)


def require_zero():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: zero checks have not passed")


def pilot():
    require_zero()
    me = [sys.executable, str(Path(__file__).resolve())]
    jobs = [(a, s) for a in ("c", "m") for s in PILOT]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["pilotone", j[0], str(j[1])]), jobs))
    po = HERE / "output_pilot"
    rows = {a: Counter() for a in ("c", "m")}
    for a, s in jobs:
        r = json.loads((po / f"{a}_seed_{s}.json").read_text(encoding="utf-8"))["audit"]
        rows[a].update({k: v for k, v in r.items() if isinstance(v, (int, float))})
    c, m = rows["c"], rows["m"]
    share_c = c["joins_loved_beyond_sight"] / c["joins"] if c["joins"] else 0.0
    ok1 = m["joins_loved_beyond_sight"] == 0
    ok2 = m["joins_loved_mem"] > 0
    ok3 = 0.272 <= share_c <= 0.314
    lines = [f"M: go-to moves toward an out-of-sight loved one's current tile: {m['joins_loved_beyond_sight']} "
             f"(must be 0): {'yes' if ok1 else 'NO'}",
             f"M: go-to moves toward a remembered tile: {m['joins_loved_mem']} (must be > 0): {'yes' if ok2 else 'NO'}",
             f"C: A5 share {share_c:.3f} ({c['joins_loved_beyond_sight']} of {c['joins']}); AA1 holdout interval "
             f"0.272-0.314: {'within' if ok3 else 'OUTSIDE'}"]
    (po / "manipulation.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok1 and ok2 and ok3 else 'FAIL'}\n",
                                         encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok1 and ok2 and ok3 else 'FAIL'}", flush=True)


def run():
    require_zero()
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for a in ("m", "c", "s") for s in SEEDS if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hash_run(sys.argv[2], int(sys.argv[3]), 20, json.loads(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "pilot":
        pilot()
    elif cmd == "pilotone":
        run_one(sys.argv[2], int(sys.argv[3]), years=10, out=HERE / "output_pilot")
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run()
