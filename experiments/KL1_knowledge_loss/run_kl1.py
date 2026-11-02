"""KL1 — does know-how outlive its holders? (questions.md, frozen as `KL1-frozen`). Read-only on live nature v11
(`experiments/NV11_nature_v11/code_v11`, unchanged). ES2's runner supplies the world set-up; the observer is KL1's own:
  knowhow.remember_recipe   every gain (person, kind, path) and every eviction by the 12-recipe cap
  knowhow.forget_useless    every recipe dropped as useless
  knowhow.check_lost        at each check: knowers found dead (lost by death), the observer's record checked against
                            everyone's recipes, every world-level loss classified (death / forgetting / mixed) and
                            every revival given its path, and the world's own register checked against the prediction
  events                    `read` events; a yearly census of knowers per kind

  python experiments/KL1_knowledge_loss/run_kl1.py zero
  python experiments/KL1_knowledge_loss/run_kl1.py one k <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

CODE = "v11"
WPY, YEARS = base.WPY, 200
SEEDS = tuple(range(21701, 21733))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9969, 9968)
ARMS = {"k": dict(base.LP)}               # live v11 as it is
JOBS = [f"{a}:{s}" for a in ARMS for s in SEEDS]
OUT = HERE / "output"
LATE = (100 * WPY, 200 * WPY)
PATHS = ("made", "heated", "taught", "copied", "read", "taught_variant", "copied_variant")
REVIVAL_PATHS = ("made", "heated", "read", "taught_variant", "copied_variant")   # no living knower needed


class KL1Obs:
    def __init__(self, w, late=LATE):
        self.w = w
        self.late = late
        self.mismatch = Counter()
        self.mirror = defaultdict(set)                  # person -> kinds the observer knows they know
        self.gains = defaultdict(list)                  # kind -> [(tick, person, path)] since the last check
        self.losses = defaultdict(list)                 # kind -> [(tick, person, cause)] since the last check
        self.alive_since = {}                           # kind -> tick it became known (first or revival)
        self.s = defaultdict(float)
        self.gain_paths = Counter()                     # path -> gains (counted years)
        self.mind_losses = Counter()                    # cause -> losses from minds (counted years)
        self.world_losses = defaultdict(lambda: [0, 0, 0])   # markable? ("1"/"0") -> [death, forgetting, mixed]
        self.revivals = defaultdict(Counter)            # markable? -> path -> revivals
        self.lifetimes = []                             # weeks a kind stayed known before a counted loss
        self.at_death = [0, 0]                          # a dead knower's kinds: [survived in someone, lost with them]
        self.census = defaultdict(lambda: [0, 0, 0])    # year -> [kinds alive, knowers summed, kinds with one knower]
        self.reads = 0

    def counted(self, tick):
        return self.late[0] <= tick < self.late[1]

    def markable(self, world, sig):
        rec = world.knowledge.get(sig)
        return "1" if rec is not None and rec.get("recipe", {}).get("verb") == "strike" else "0"

    def gained(self, world, p, before, how, sig_in, meant=None):
        after = set(p.recipes)
        t = world.tick
        if how in ("taught", "copied") and meant and meant != sig_in:
            how = how + "_variant"                         # shown or seen with an error: a kind other than the one meant
        if sig_in not in before and sig_in not in after:   # learned and pushed out by the cap in the same moment
            self.gains[sig_in].append((t, p.id, how))
            self.losses[sig_in].append((t, p.id, "evicted"))
            if self.counted(t):
                self.gain_paths[how] += 1
                self.mind_losses["evicted"] += 1
        for sig in after - before:
            self.gains[sig].append((t, p.id, how))
            if self.counted(t):
                self.gain_paths[how] += 1
        for sig in before - after:
            self.losses[sig].append((t, p.id, "evicted"))
            if self.counted(t):
                self.mind_losses["evicted"] += 1
        self.mirror[p.id] = after

    def forgot(self, world, p, before):
        after = set(p.recipes)
        t = world.tick
        for sig in before - after:
            self.losses[sig].append((t, p.id, "forgotten"))
            if self.counted(t):
                self.mind_losses["forgotten"] += 1
        self.mirror[p.id] = after

    def check(self, world):
        """Called just before the world's own check_lost; returns the kinds predicted alive."""
        t = world.tick
        known = set()
        dead = []
        for pid, sigs in list(self.mirror.items()):
            p = world.people.get(pid)
            if p is None or not p.alive:
                dead.append((pid, sigs))
                continue
            actual = set(p.recipes)
            if actual != sigs:
                self.mismatch["mirror"] += 1
                self.mirror[pid] = actual
            known |= actual
        for q in world.living():                        # anyone the mirror has not seen yet must know nothing
            if q.id not in self.mirror and q.recipes:
                self.mismatch["mirror"] += 1
                self.mirror[q.id] = set(q.recipes)
                known |= set(q.recipes)
        for pid, sigs in dead:
            for sig in sigs:
                self.losses[sig].append((t, pid, "death"))
                if self.counted(t):
                    self.mind_losses["death"] += 1
                    self.at_death[0 if sig in known else 1] += 1
            del self.mirror[pid]
        for sig, rec in world.knowledge.items():
            mk = self.markable(world, sig)
            if rec["alive"] and sig not in known:              # lost to the world now
                causes = {c for _, _, c in self.losses.get(sig, ())}
                if not causes:
                    self.mismatch["unexplained_loss"] += 1
                elif self.counted(t):
                    kind = 0 if causes == {"death"} else (1 if "death" not in causes else 2)
                    self.world_losses[mk][kind] += 1
                    self.lifetimes.append(t - self.alive_since.get(sig, rec.get("first_tick", t)))
            elif not rec["alive"] and sig in known:            # revived
                g = self.gains.get(sig, ())                     # in the order the gains happened
                if not g:
                    self.mismatch["unexplained_revival"] += 1
                else:
                    if g[0][2] not in REVIVAL_PATHS:               # the exact kind taught or copied needs a living knower
                        self.mismatch["revival_path"] += 1
                    self.alive_since[sig] = g[0][0]
                    if self.counted(t):
                        self.revivals[mk][g[0][2]] += 1
            if sig not in self.alive_since and rec["alive"]:
                self.alive_since[sig] = rec.get("first_tick", t)
        self.gains.clear()
        self.losses.clear()
        return known

    def after_check(self, world, known):
        for sig, rec in world.knowledge.items():
            if rec["alive"] != (sig in known):
                self.mismatch["register"] += 1

    def __call__(self, world, events):
        tick = world.tick - 1
        if not self.counted(tick):
            return
        for ev in events:
            if ev["k"] == "read":
                self.reads += 1
        if tick % WPY == WPY - 1:
            n_by = Counter()
            for q in world.living():
                for sig in q.recipes:
                    n_by[sig] += 1
            c = self.census[str(tick // WPY)]
            c[0] += len(n_by)
            c[1] += sum(n_by.values())
            c[2] += sum(1 for v in n_by.values() if v == 1)

    def results(self):
        return {"gain_paths": dict(self.gain_paths), "mind_losses": dict(self.mind_losses),
                "world_losses_fields": ["death", "forgetting", "mixed"], "world_losses": dict(self.world_losses),
                "revivals": {k: dict(v) for k, v in self.revivals.items()}, "lifetimes": self.lifetimes,
                "at_death_fields": ["survived", "lost"], "at_death": self.at_death,
                "census_fields": ["kinds_alive", "knowers", "single_knower_kinds"], "census": dict(self.census),
                "reads": self.reads, "mismatch": dict(self.mismatch)}


def install(w, obs):
    from acl import knowhow
    o_remember, o_forget, o_check = knowhow.remember_recipe, knowhow.forget_useless, knowhow.check_lost

    def remember_recipe(world, p, *args, **kw):
        if world is not w:
            return o_remember(world, p, *args, **kw)
        how = args[2] if len(args) > 2 else kw.get("how")
        sig_in = args[0] if args else kw.get("sig")
        before = set(p.recipes)
        out = o_remember(world, p, *args, **kw)
        obs.gained(world, p, before, how, sig_in, kw.get("meant"))
        return out

    def forget_useless(p):
        before = set(p.recipes)
        out = o_forget(p)
        if w.people.get(p.id) is p:
            obs.forgot(w, p, before)
        return out

    def check_lost(world):
        if world is not w:
            return o_check(world)
        known = obs.check(world)
        out = o_check(world)
        obs.after_check(world, known)
        return out
    knowhow.remember_recipe = remember_recipe
    knowhow.forget_useless = forget_useless
    knowhow.check_lost = check_lost


def hashrun(seed, years, observe):
    base.setup(CODE)
    w = base.make_world(seed, ARMS["k"])
    obs = None
    if observe:
        obs = KL1Obs(w, late=(0, years * WPY))       # zero checks: every year counted
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        losses = sum(sum(v) for v in obs.world_losses.values())
        extra = ":" + json.dumps({**obs.mismatch, "_gains": sum(obs.gain_paths.values()), "_world_losses": losses},
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
        t = ro and not any(mism.values()) and info["_gains"] > 0
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer read-only: {'yes' if ro else 'NO'}; mismatches (record, "
                     f"register, unexplained): {mism or 'none'}; gains {info['_gains']}; world-level losses "
                     f"{info['_world_losses']}")
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
    obs = KL1Obs(w)
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
