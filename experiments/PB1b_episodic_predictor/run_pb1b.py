"""PB1b — a shadow brain with episodic memory (questions.md, frozen as `PB1b-frozen`). Read-only on live nature v13.
It reuses PB1's runner (`../PB1_shadow_predictor/run_pb1.py`) for the decision-time inputs, the 9-output vector, the
standardisation (floor 0.05, clip +-10), the cases, the observation rules and the table B; only the predictors differ.

  E-own      episodic memory of own weeks: the exact lived (situation, action) cell's mean, else the k = 8 most similar
             same-action weeks weighted by 1 / (distance + 0.05); k = 5 and 15 described
  E-obs      the same over own + observed weeks; an observed week weighs 1 / (visible observed weeks that week)
  E-obs-0.5  observed weeks weigh 0.5
  L-obs-0.5  PB1's best variant, rerun as the reference
Observed memory holds at most 1,000 entries per action per person (the most recent).

  python experiments/PB1b_episodic_predictor/run_pb1b.py zero
  python experiments/PB1b_episodic_predictor/run_pb1b.py one c <seed> <years> <out>
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "PB1_shadow_predictor"))
import run_pb1 as P  # noqa: E402

base = P.base
CODE = P.CODE
WPY, YEARS = P.WPY, 120
SEEDS = tuple(range(23101, 23133))        # 32 new seeds, used by no study
SMOKE_SEEDS = (9895, 9894)
ARMS = {"c": {**base.LP}}
JOBS = [f"c:{s}" for s in SEEDS]
OUT = HERE / "output"
ADULT, BORN, COMMON, NOUT = P.ADULT, P.BORN, P.COMMON, P.NOUT
VARIANTS = ("B", "E", "Eo", "E5", "L5", "Ek5", "Ek15")
CASES = ("all", "fam", "u_pair", "u_prop", "rare", "u_place", "w0", "w1", "w2", "w3")
K, KS, EPS, OBS_CAP = 8, (5, 15), 0.05, 1000
# distance groups (indices into PB1's 116-dimensional input), each group's mean squared difference counting equally
GROUPS = [list(range(0, 4)), [8, 9, 10, 11, 12, 13, 14, 15], list(range(16, 27)), list(range(27, 32)),
          list(range(89, 114))]
DIDX = np.array([i for g in GROUPS for i in g])
GW = np.concatenate([np.full(len(g), 1.0 / len(g)) for g in GROUPS])


class Store:
    """Entries of one kind (own or observed) for one action: distance inputs, outputs, masks, cells, base weights."""

    def __init__(self, cap=None):
        self.cap = cap
        self.X = np.zeros((16, len(DIDX)))
        self.Y = np.zeros((16, NOUT))
        self.M = np.zeros((16, NOUT))
        self.C = np.zeros(16, dtype=int)
        self.Wb = np.zeros(16)
        self.n = 0                       # filled rows
        self.head = 0                    # next slot (ring buffer when capped)

    def add(self, xd, y, m, ctx, wb):
        """Adds an entry; returns the evicted (ctx, y, m, wb) when a capped store overwrites one, else None."""
        if self.cap is not None and self.n == self.cap:
            i = self.head
            old = (int(self.C[i]), self.Y[i].copy(), self.M[i].copy(), float(self.Wb[i]))
            self.head = (self.head + 1) % self.cap
        else:
            if self.n == len(self.X):
                grow = len(self.X) * 2 if self.cap is None else min(self.cap, len(self.X) * 2)
                for name in ("X", "Y", "M"):
                    a = getattr(self, name)
                    b = np.zeros((grow, a.shape[1]))
                    b[:self.n] = a[:self.n]
                    setattr(self, name, b)
                for name in ("C", "Wb"):
                    a = getattr(self, name)
                    b = np.zeros(grow, dtype=a.dtype)
                    b[:self.n] = a[:self.n]
                    setattr(self, name, b)
            i = self.n
            self.n += 1
            old = None
        self.X[i], self.Y[i], self.M[i], self.C[i], self.Wb[i] = xd, y, m, ctx, wb
        return old


class Memory:
    """One person's episodic memory: own and observed stores per action, with running cell sums for exact cells."""

    def __init__(self):
        self.own = {}
        self.obs = {}
        self.cells = defaultdict(lambda: {"o": [np.zeros(NOUT), np.zeros(NOUT)], "b": [np.zeros(NOUT), np.zeros(NOUT)],
                                          "h": [np.zeros(NOUT), np.zeros(NOUT)]})
        # cell sums: "o" own (weight 1), "b" observed with base weight 1/n, "h" observed with weight 0.5

    def add_own(self, act, ctx, xd, y):
        self.own.setdefault(act, Store()).add(xd, y, np.ones(NOUT), ctx, 1.0)
        c = self.cells[(ctx, act)]["o"]
        c[0] += y
        c[1] += 1.0

    def add_obs(self, act, ctx, xd, y, m, wb):
        old = self.obs.setdefault(act, Store(OBS_CAP)).add(xd, y, m, ctx, wb)
        cl = self.cells[(ctx, act)]
        cl["b"][0] += wb * m * y
        cl["b"][1] += wb * m
        cl["h"][0] += 0.5 * m * y
        cl["h"][1] += 0.5 * m
        if old is not None:
            octx, oy, om, owb = old
            co = self.cells[(octx, act)]
            co["b"][0] -= owb * om * oy
            co["b"][1] -= owb * om
            co["h"][0] -= 0.5 * om * oy
            co["h"][1] -= 0.5 * om

    def cell_mean(self, ctx, act, mode, fallback):
        c = self.cells.get((ctx, act))
        if c is None:
            return fallback
        s, w = c["o"][0].copy(), c["o"][1].copy()
        if mode in ("b", "h"):
            s += c[mode][0]
            w += c[mode][1]
        out = fallback.copy()
        ok = w > 1e-12
        out[ok] = s[ok] / w[ok]
        return out


def knn(Xs, Ys, Ms, Ws, xd, k, fallback):
    """Weighted mean of the k nearest entries (by the grouped distance), per output over entries that have it."""
    d = np.sqrt(((Xs - xd) ** 2 * GW).sum(1))
    kk = min(k, len(d))
    idx = np.argpartition(d, kk - 1)[:kk] if kk < len(d) else np.arange(len(d))
    w = Ws[idx] / (d[idx] + EPS)
    wm = w[:, None] * Ms[idx]
    den = wm.sum(0)
    out = fallback.copy()
    ok = den > 1e-12
    out[ok] = (wm * Ys[idx]).sum(0)[ok] / den[ok]
    return out, float(d.min()) if len(d) else float("nan")


class PB1bObs(P.PB1Obs):
    def __init__(self, w, born, variants=VARIANTS, verify=False):
        super().__init__(w, born, variants=("B",), verify=verify)
        self.variants = variants
        self.mem = {}
        self.lin = {}
        self.sse = {v: {k: np.zeros(NOUT) for k in CASES} for v in VARIANTS}
        self.unit_bad = 0
        self.nearest = []

    def __call__(self, world, events):
        tick = world.tick - 1
        gained, newkind = Counter(), set()
        for ev in events:
            k, a = ev["k"], ev.get("a")
            if k == "forage" and a:
                gained[a] += float(ev.get("got", 0.0))
            elif k == "take" and a:
                gained[a] += float(ev.get("food", 0.0))
            elif k == "hunt":
                party = ev.get("party", ())
                for i in party:
                    gained[i] += float(ev.get("meat", 0.0)) / len(party)
            elif k == "make" and a:
                sig = ev.get("thing")
                if sig and sig not in self.made[a]:
                    newkind.add(a)
                self.made[a].add(sig)
        for p in world.living():
            if self.born[0] <= p.birth < self.born[1]:
                self.visited[p.id].add(tuple(p.loc))
        caps, self.cap = self.cap, {}
        outs = {}
        for pid, cap in caps.items():
            p = world.people[pid]
            if not p.alive:
                continue
            y = self.outcome(world, p, cap, gained[pid])
            y[7] = 1.0 if pid in newkind else 0.0
            outs[pid] = y
            self.last[pid] = [cap["act"]] + self.last[pid][:1]
        if not outs:
            return
        std = np.sqrt(self.m2 / self.n) if self.n > 1 else np.ones(NOUT)
        std = np.maximum(std, P.STD_FLOOR)
        wmean = self.mean.copy()
        scoring = self.n >= P.BURN
        zc = lambda v: np.clip((v - wmean) / std, -P.ZCLIP, P.ZCLIP)  # noqa: E731
        own = [pid for pid in outs if self.followed(world.people[pid], tick)]
        for pid in own:
            cap, y = caps[pid], outs[pid]
            per = self.people.get(pid)
            if per is None:
                per = self.people[pid] = P.Person(self.feat.D, self.rng, ("B",))
                self.mem[pid] = Memory()
                if "L5" in self.variants:
                    self.lin[pid] = P.Lin(self.feat.D)
            mem, table = self.mem[pid], per.m["B"]
            x = cap["x"]
            xd = x[DIDX]
            act, ctx = cap["act"], cap["ctx"]
            lived = (ctx, act) in table.sa
            ek = self._edge_hard(x)
            pkey = (act, ek[0], ek[1], self._target_key(cap))
            unfam_prop = pkey not in per.props_seen
            z = zc(y)
            if scoring:
                bpred = table.predict(ctx, act, wmean)
                preds = {"B": bpred}
                if lived:
                    preds["E"] = mem.cell_mean(ctx, act, "o", bpred)
                    preds["Eo"] = mem.cell_mean(ctx, act, "b", bpred)
                    preds["E5"] = mem.cell_mean(ctx, act, "h", bpred)
                    preds["Ek5"] = preds["Ek15"] = preds["E"]
                    if self.verify and not np.allclose(preds["E"], bpred):
                        self.unit_bad += 1
                else:
                    so, sb = mem.own.get(act), mem.obs.get(act)
                    if so is not None and so.n:
                        Xo, Yo, Mo = so.X[:so.n], so.Y[:so.n], so.M[:so.n]
                        preds["E"], dmin = knn(Xo, Yo, Mo, np.ones(so.n), xd, K, bpred)
                        preds["Ek5"], _ = knn(Xo, Yo, Mo, np.ones(so.n), xd, KS[0], bpred)
                        preds["Ek15"], _ = knn(Xo, Yo, Mo, np.ones(so.n), xd, KS[1], bpred)
                        if len(self.nearest) < 200000:
                            self.nearest.append(dmin)
                    else:
                        preds["E"] = preds["Ek5"] = preds["Ek15"] = bpred
                    parts = [s for s in (so, sb) if s is not None and s.n]
                    if parts:
                        Xa = np.vstack([s.X[:s.n] for s in parts])
                        Ya = np.vstack([s.Y[:s.n] for s in parts])
                        Ma = np.vstack([s.M[:s.n] for s in parts])
                        wb = np.concatenate([s.Wb[:s.n] for s in parts])
                        isobs = np.concatenate([np.zeros(s.n) if s is so else np.ones(s.n) for s in parts])
                        preds["Eo"], _ = knn(Xa, Ya, Ma, wb, xd, K, bpred)
                        w5 = np.where(isobs > 0, 0.5, 1.0)
                        preds["E5"], _ = knn(Xa, Ya, Ma, w5, xd, K, bpred)
                    else:
                        preds["Eo"] = preds["E5"] = bpred
                if pid in self.lin:
                    preds["L5"] = None
                cases = ["all", "fam" if lived else None, "u_pair" if (act in COMMON and not lived) else None,
                         "u_prop" if unfam_prop else None, "rare" if act not in COMMON else None,
                         "u_place" if cap.get("new_place") else None,
                         f"w{sum(per.weeks >= b for b in P.WBANDS)}"]
                cases = [c for c in cases if c]
                for cs in cases:
                    self.cnt[cs] += 1
                for v in self.variants:
                    if v == "L5":
                        e = (z - np.clip(self.lin[pid].predict(x), -P.ZCLIP, P.ZCLIP)) ** 2
                    else:
                        e = (z - zc(preds[v])) ** 2
                    for cs in cases:
                        self.sse[v][cs] += e
            # learn
            table.learn(ctx, act, y)
            mem.add_own(act, ctx, xd, y)
            if pid in self.lin:
                self.lin[pid].learn(x[None, :], z[None, :], np.ones((1, NOUT)))
            per.weeks += 1
            per.props_seen.add(pkey)
            per.hid_mean = (per.hid_mean * per.hid_n + x[:P.HIDDEN_IN]) / (per.hid_n + 1)
            per.hid_n += 1
            self.s["own_weeks"] += 1
        for pid in own:
            yv = outs[pid]
            self.n += 1
            d = yv - self.mean
            self.mean += d / self.n
            self.m2 += d * (yv - self.mean)
        # observed weeks
        from acl.util import distance
        c = world.cfg
        for pid in own:
            per, mem = self.people[pid], self.mem[pid]
            O = world.people[pid]
            seen = []
            for aid, yv in outs.items():
                if aid == pid or distance(tuple(O.loc), caps[aid]["loc"], c.width, c.height) > c.perception:
                    continue
                seen.append(aid)
            if not seen:
                continue
            wb = 1.0 / len(seen)
            xs, zs = [], []
            for aid in seen:
                xo = caps[aid]["x"].copy()
                xo[:P.HIDDEN_IN] = per.hid_mean
                xo[-2] = 1.0
                mem.add_obs(caps[aid]["act"], caps[aid]["ctx"], xo[DIDX], outs[aid], P.VISIBLE, wb)
                xs.append(xo)
                zs.append(zc(outs[aid]))
            self.s["observed"] += len(seen)
            if pid in self.lin:
                X, Z = np.array(xs), np.array(zs)
                self.lin[pid].learn(X, Z, np.tile(P.VISIBLE, (len(xs), 1)), 0.5)
        self.s["living_weeks"] += len(world.living())
        self.s["followed_weeks"] += len(own)
        self.s["followed_people"] = len(self.people)

    def results(self):
        near = np.array(self.nearest) if self.nearest else np.array([np.nan])
        return {"variants": list(self.variants), "cases": list(CASES),
                "sse": {v: {k: [round(float(e), 6) for e in self.sse[v][k]] for k in CASES} for v in self.variants},
                "counts": dict(self.cnt), "sums": dict(self.s), "unit_bad": self.unit_bad,
                "nearest_quartiles": [round(float(q), 4) for q in np.nanpercentile(near, [25, 50, 75])]}


def install(w, obs):
    P.install(w, obs)


def hashrun(seed, years, observe, variants="all"):
    base.setup(CODE)
    w = base.make_world(seed, ARMS["c"])
    obs = None
    if observe:
        vs = VARIANTS if variants == "all" else ("B",) + tuple(variants.split(","))
        obs = PB1bObs(w, [5 * WPY, years * WPY], vs, verify=True)
        install(w, obs)
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    extra = ""
    if observe:
        r = obs.results()
        extra = ":" + json.dumps({"own": obs.s["own_weeks"], "obs": obs.s["observed"], "unit_bad": obs.unit_bad,
                                  "E_all": [round(e, 6) for e in r["sse"]["E"]["all"]]},
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
    specs = [(seed, years, obs, v) for seed, years in ((501, 20), (601, 60))
             for obs, v in ((0, "all"), (1, "all"), (1, "E"))]
    with ThreadPoolExecutor(4) as ex:
        got = dict(zip(specs, ex.map(lambda sp: call("hashrun", *sp), specs)))
        rl = ex.submit(lambda: subprocess.run(me + ["reload", "501"], capture_output=True, text=True).stdout.split())
        rl = rl.result()
    for seed, years in ((501, 20), (601, 60)):
        ro = hs(got[(seed, years, 0, "all")]) == hs(got[(seed, years, 1, "all")]) == hs(got[(seed, years, 1, "E")])
        a = json.loads(got[(seed, years, 1, "all")].split(":", 2)[2])
        b = json.loads(got[(seed, years, 1, "E")].split(":", 2)[2])
        alone = a["E_all"] == b["E_all"]
        applies = years > 21
        unit = a["unit_bad"] == 0 and (a["own"] > 0 or not applies)
        t = ro and alone and unit
        ok &= t
        lines.append(f"seed {seed}, {years} years: observer and predictors read-only (following people born after year "
                     f"5): {'yes' if ro else 'NO'}; E-own's errors are the same alone as beside the others: "
                     f"{'yes' if alone else 'NO'}; on lived cells E-own's prediction equals the table's: "
                     f"{('yes' if unit else 'NO') if applies else 'not applicable (nobody followed yet)'}; {a}")
    t = rl[-1:] == ["True"]
    ok &= t
    lines.append(f"seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    lines.append(f"code_v13 fingerprint: {call('fp')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    base.setup(CODE)
    f0 = base.fingerprint(CODE)
    w = base.make_world(seed, ARMS[arm])
    born = list(BORN) if years >= 110 else [max(0, years - 60) * WPY, max(1, years - 20) * WPY]
    obs = PB1bObs(w, born)
    install(w, obs)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "code_v13", "code_hash": f0, "code_hash_after": base.fingerprint(CODE),
           "final_tick": w.tick, "extinct": not w.living(), "born": born, "world_hash": base.world_hash(w),
           **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, followed {obs.s['followed_people']}, own weeks "
          f"{obs.s['own_weeks']}, observed {obs.s['observed']}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1", sys.argv[5]))
    elif cmd == "reload":
        print(P.reload_check(int(sys.argv[2])))
    elif cmd == "fp":
        base.setup(CODE)
        print(base.fingerprint(CODE))
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
