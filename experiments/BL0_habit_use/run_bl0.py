"""BL0 — does ACL's brain meaningfully learn? (questions.md, frozen as `BL0-frozen`; Amendment 1, `BL0-amend1`: part T.)
A logging copy of the control code (`code_bl0`: code_e13r plus hooks that hand values to a log held outside the world's
state, as `code_aa1`) and a read-only observer that keeps the split of every habit value and the decision measures.

  python experiments/BL0_habit_use/run_bl0.py zero        # the logging copy reproduces the control world; parts add up
  python experiments/BL0_habit_use/run_bl0.py discovery   # 501-516, 601-616, 120 years
  python experiments/BL0_habit_use/run_bl0.py holdout     # 811-818, 1101-1124 (after the discovery reading)
  python experiments/BL0_habit_use/run_bl0.py smoke       # throwaway: seed 9501, 15 years (code check only)

The hooks (one per habit writer found by Amendment 1's search, plus the decision): `mind.decide` (each option's score
before and after the thought bonus, the chosen index); own experience (`biology._learn`); upbringing
(`biology._upbringing`); birth; clearing at death; the gift nudge (`actions._give`); imitation in talk
(`actions._imitate`). `_follow` (E13's watching) is off in the control world (`b2_mode` 0) and has no hook.

Operational notes written before any data (the frozen text leaves these open; each is the most literal reading):
- Split, per person, 544 values each: I, C, E, T, and the same habit split again by the generation whose own experience
  (E, clipping and gift nudges included) first put it there ("origin generation"). Blends act on both splits exactly as on
  the habit: upbringing and imitation take (1 - rate) of every part and add rate x the carer's or speaker's habit to C
  or T; in the origin split they mix in rate x the carer's or speaker's own origin split. Own experience: every part of
  that value x (1 - learning rate), then the rest of the change (target, clipping) to E and to the person's generation.
  Birth: I = the habit; origin split = 1/4 (mother's + other parent's), as the habit is. Founders start at zero.
- Checks every week, every living person: I + C + E + T = habit, and the origin split sums to the habit; the largest
  error is recorded (zero check: to 1e-9).
- Q1, per decision of every person aged 1+: learned part L_k = learned_weight x habit value for option k; final score S_k
  (after the thought bonus); without the learned term S_k - L_k. Choice effect = total variation distance between the
  two softmax distributions at the world's temperature. Top changed = the highest-scoring option (first, on ties)
  differs. Instinct part = score before the thought bonus - L_k. Medians of |L| and |instinct| per action from
  log-spaced histograms (400 bins, 1e-6 to 10; reported as approximate to a bin).
- Q2 attribution: in each decision, each part's share of the habit term = sum over options of |learned_weight x part|
  / the same summed over all four parts; averaged over adult decisions weighted by the choice effect (the frozen "share
  of the choice effect, attributed by part"), and unweighted beside it. Absolute values, because parts can cancel.
- Q3 later life: a habit (situation, action) is "stopped" if chosen before and not chosen for 52+ weeks. When its
  situation comes back, its value and the choice effect of removing the learned term of stopped options only.
- Q3 descendants: "parents' habits at birth" = the mean of the mother's and the other parent's habits (the father's, or
  the mother's twice if he is dead, as the birth rule does). Sham = an adult (16+) alive at the birth, not a parent and
  of kinship 0 with the child, drawn by the observer's own `random.Random(seed)` (never the world's). Pearson correlation
  over the 544 values at ages 12, 20 and 40.
- Lineage: an adult's share (absolute values) of the origin split from generations at least two above their own.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"bl0": HERE / "code_bl0", "e13r": EXP / "E13R_replication" / "code_e13r"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
DISCOVERY = tuple(range(501, 517)) + tuple(range(601, 617))
HOLDOUT = tuple(range(811, 819)) + tuple(range(1101, 1125))
SMOKE_SEED = 9501
G = 48                                      # origin generations kept (a hard stop if exceeded)
NB, LO, HI = 400, 1e-6, 10.0
AGES = ((1, 5), (5, 12), (12, 16), (16, 30), (30, 45), (45, 200))


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def make_world(seed):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0))


def world_hash(w):
    d = w.to_dict()
    d.pop("cfg")
    return hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()


def fingerprint(code="bl0"):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


def hbin(x):
    if x <= LO:
        return 0
    return min(NB - 1, int((math.log10(x) - math.log10(LO)) / (math.log10(HI) - math.log10(LO)) * (NB - 1)) + 1)


def band(years):
    for i, (a, b) in enumerate(AGES):
        if a <= years < b:
            return i
    return None


def softmax(xs, t):
    top = max(xs)
    w = [math.exp((x - top) / t) for x in xs]
    s = sum(w)
    return [v / s for v in w]


def tvd(a, b, t):
    return 0.5 * sum(abs(x - y) for x, y in zip(softmax(a, t), softmax(b, t)))


class BL0:
    """Receives values from the hooks and reads the world after each week; draws nothing from the world's generator and
    writes nothing to the world."""

    def __init__(self, seed):
        from acl.person import ACTIONS, N_ACTIONS, N_CONTEXTS
        self.ACTIONS, self.NA, self.N = ACTIONS, N_ACTIONS, N_ACTIONS * N_CONTEXTS
        self.A = {a: i for i, a in enumerate(ACTIONS)}
        self.M = {}                                  # pid -> array (4 + G, N): I, C, E, T, then origin generations
        self.changed = {}                            # pid -> array (N,) of the week each value last changed
        self.last_chosen = {}                        # pid -> {index: week}
        self.rng = random.Random(seed)
        self.max_err = 0.0
        self.n = Counter()
        self.sum = defaultdict(float)
        self.hist = {"L": [[0] * NB for _ in ACTIONS], "inst": [[0] * NB for _ in ACTIONS]}
        self.ctx_count = Counter()
        self.stale = Counter()
        self.kids = {}                               # child pid -> [birth week, parents' mean habit, sham habit or None]
        self.desc = []                               # [age, corr parents, corr sham, |I| share, |E| share]
        self.snap = []                               # yearly: [year, age band, person, values |E|>=.05, I, C, E, T shares, lineage share or None]
        self.pops, self.gens_max = [], 0

    def _m(self, p):
        m = self.M.get(p.id)
        if m is None:
            if any(p.q):
                self.n["first_seen_nonzero"] += 1
            m = np.zeros((4 + G, self.N))
            self.M[p.id] = m
            self.changed[p.id] = np.zeros(self.N)
        return m

    def _gen(self, p):
        if p.generation >= G:
            raise SystemExit(f"HARD STOP: generation {p.generation} beyond the {G} kept")
        self.gens_max = max(self.gens_max, p.generation)
        return 4 + p.generation

    # --- hooks -----------------------------------------------------------------------------------------------
    def own(self, world, p, i, old):
        m, lr = self._m(p), world.cfg.learning_rate
        m[:, i] *= 1.0 - lr
        delta = p.q[i] - (1.0 - lr) * old
        m[2, i] += delta
        m[self._gen(p), i] += delta
        self.changed[p.id][i] = world.tick
        self.n["own"] += 1

    def nudge(self, world, p, i, old):
        m = self._m(p)
        delta = p.q[i] - old
        m[2, i] += delta
        m[self._gen(p), i] += delta
        self.changed[p.id][i] = world.tick
        self.n["nudge"] += 1

    def blend(self, world, p, other, rate, row):
        m, o = self._m(p), self._m(other)
        m[:4] *= 1.0 - rate
        m[row] += rate * np.asarray(other.q)
        m[4:] = (1.0 - rate) * m[4:] + rate * o[4:]
        self.changed[p.id][:] = world.tick
        self.n["upbringing" if row == 1 else "imitation"] += 1

    def birth(self, world, child, mother, other):
        mm, om = self._m(mother), self._m(other)
        m = np.zeros((4 + G, self.N))
        m[0] = np.asarray(child.q)
        m[4:] = 0.25 * (mm[4:] + om[4:])
        self.M[child.id] = m
        self.changed[child.id] = np.full(self.N, float(world.tick))
        parents = 0.5 * (np.asarray(mother.q) + np.asarray(other.q))
        cands = sorted((q for q in world.living() if q.id not in (mother.id, other.id, child.id)
                        and q.years(world.tick) >= 16 and world.kinship(child, q) == 0 and world.kinship(q, child) == 0),
                       key=lambda q: q.id)
        sham = np.asarray(cands[self.rng.randrange(len(cands))].q) if cands else None
        self.kids[child.id] = [world.tick, parents, sham]
        self.n["births"] += 1

    def death(self, world, p):
        self.M.pop(p.id, None)
        self.changed.pop(p.id, None)
        self.last_chosen.pop(p.id, None)
        self.kids.pop(p.id, None)

    def decide(self, world, p, base, lw, pre, post, i):
        t, tick = world.cfg.choice_temperature, world.tick
        yrs = p.years(tick)
        b = band(yrs)
        adult = yrs >= 16
        idx = [base + self.A[o[1]] for o in post]
        L = [lw * p.q[k] for k in idx]
        S = [o[0] for o in post]
        S0 = [s - l for s, l in zip(S, L)]
        ce = tvd(S, S0, t)
        top = S.index(max(S)) != S0.index(max(S0))
        n, s = self.n, self.sum
        n[f"dec_{b}"] += 1
        s[f"ce_{b}"] += ce
        n[f"top_{b}"] += top
        for (pre_s, act, _), l in zip(pre, L):
            a = self.A[act]
            self.hist["L"][a][hbin(abs(l))] += 1
            self.hist["inst"][a][hbin(abs(pre_s - l))] += 1
        m = self._m(p)
        parts = [sum(abs(lw * m[r, k]) for k in idx) for r in range(4)]
        tot = sum(parts)
        if adult and tot > 0:
            for r, name in enumerate("ICET"):
                s[f"w_{name}"] += ce * parts[r] / tot
                s[f"u_{name}"] += parts[r] / tot
            s["w_total"] += ce
            n["dec_adult_parts"] += 1
        ctx = base // self.NA
        self.ctx_count[ctx] += 1
        lc = self.last_chosen.setdefault(p.id, {})
        stale = [j for j, k in enumerate(idx) if k in lc and tick - lc[k] >= WPY]
        if stale:
            Ls = [l if j in stale else 0.0 for j, l in enumerate(L)]
            s["stale_ce"] += tvd(S, [x - y for x, y in zip(S, Ls)], t)
            s["stale_abs_value"] += sum(abs(p.q[idx[j]]) for j in stale)
            n["stale_decisions"] += 1
            n["stale_options"] += len(stale)
        chosen = idx[i]
        self.stale[min(int(tick - self.changed[p.id][chosen]), 10 * WPY)] += 1
        lc[chosen] = tick

    # --- each week -------------------------------------------------------------------------------------------
    def __call__(self, world, events):
        tick = world.tick - 1
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        for p in living:
            if not p.q:
                continue
            m = self._m(p)
            q = np.asarray(p.q)
            err = max(float(np.max(np.abs(m[:4].sum(0) - q))), float(np.max(np.abs(m[4:].sum(0) - q))))
            self.max_err = max(self.max_err, err)
            age_w = world.tick - p.birth
            if p.id in self.kids and age_w in (12 * WPY, 20 * WPY, 40 * WPY):
                _, par, sham = self.kids[p.id]
                corr = lambda a, b: float(np.corrcoef(a, b)[0, 1]) if a is not None and np.std(a) > 0 and np.std(b) > 0 else None  # noqa: E731
                ab = np.abs(m[:4]).sum(1)
                tot = ab.sum()
                self.desc.append([age_w // WPY, corr(q, par), corr(q, sham) if sham is not None else None,
                                  float(ab[0] / tot) if tot else None, float(ab[2] / tot) if tot else None])
            if tick % WPY == WPY - 1:
                ab = np.abs(m[:4]).sum(1)
                tot = ab.sum()
                yrs = p.years(world.tick)
                lin = None
                if yrs >= 16:
                    og = np.abs(m[4:]).sum(1)
                    ot = og.sum()
                    lin = float(og[:max(0, p.generation - 1)].sum() / ot) if ot else None
                self.snap.append([tick // WPY, band(yrs), int(np.sum(np.abs(m[2]) >= 0.05)),
                                  *([float(x / tot) for x in ab] if tot else [None] * 4), lin])

    def results(self):
        return {"n": dict(self.n), "sum": dict(self.sum), "hist": self.hist, "ctx_count": dict(self.ctx_count),
                "staleness_weeks": dict(self.stale), "desc": self.desc, "snap": self.snap, "pops": self.pops,
                "max_split_error": self.max_err, "max_generation": self.gens_max}


def hash_run(code, seed, years, observe):
    setup(code)
    w = make_world(seed)
    obs = None
    if observe:
        obs = BL0(seed)
        w.bl0 = obs
        w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + " " + (f"{obs.max_err:.3g}" if obs else "-")


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]
    call = lambda code, seed, obs: subprocess.run(me + ["hashrun", code, str(seed), "1" if obs else "0"],  # noqa: E731
                                                  capture_output=True, text=True).stdout.strip().splitlines()[-1].split()
    lines, ok = [], True
    for seed in (501, 601):
        ctrl, plain, logged = call("e13r", seed, False), call("bl0", seed, False), call("bl0", seed, True)
        a, b = plain[0] == ctrl[0], logged[0] == ctrl[0]
        e = float(logged[1])
        ok &= a and b and e <= 1e-9
        lines.append(f"seed {seed}, 20 years: code_bl0 without the log = control: {'yes' if a else 'NO'}; with the log and "
                     f"observer = control: {'yes' if b else 'NO'}; largest split error {e:.3g} (must be <= 1e-9)")
    setup("bl0")
    lines.append(f"code_bl0 fingerprint: {fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(seed, years=YEARS, out=None):
    setup("bl0")
    f0 = fingerprint()
    w = make_world(seed)
    obs = BL0(seed)
    w.bl0 = obs
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"seed": seed, "code_hash": f0, "code_hash_after": fingerprint(), "final_tick": w.tick,
           "world_hash": world_hash(w), "temperature": w.cfg.choice_temperature, **obs.results()}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: ended week {w.tick}, pops {obs.pops}, split error {obs.max_err:.2g}", flush=True)


def batch(seeds):
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: the logging copy has not been shown to leave the world unchanged (run 'zero')")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [s for s in seeds if not (OUT / f"seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda s: subprocess.call(me + ["one", str(s)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hash_run(sys.argv[2], int(sys.argv[3]), 20, sys.argv[4] == "1"))
    elif cmd == "one":
        run_one(int(sys.argv[2]))
    elif cmd == "smoke":
        run_one(SMOKE_SEED, years=15, out=HERE / "output_smoke")
    elif cmd == "discovery":
        batch(DISCOVERY)
    elif cmd == "holdout":
        if not (HERE / "findings_discovery.md").exists():
            sys.exit("ABORT: the discovery reading has not been written down")
        batch(HOLDOUT)
