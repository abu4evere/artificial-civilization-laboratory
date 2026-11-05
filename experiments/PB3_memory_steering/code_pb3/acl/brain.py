"""PB2 (a test in a copy of nature): an episodic brain that helps choose.

Each adult keeps a memory of the weeks they lived (what they perceived when deciding, what they did, the nine
observable changes that followed, and the learning signal r that habits learn from) and of the visible weeks of people
they saw (no r: others' feelings are not observable). From it:
  r-hat   their own expected r for an option: the exact (situation, action) cell's mean if they have lived it, else the
          8 most similar own weeks with that action (distance over five equal-weight groups of inputs)
  y-hat   the expected observable changes for an option, from own and observed weeks the same way
With `brain` 1-3, r-hat (put on q's scale) takes the habit's place in a choice; with 2 (or 3, random), a goal chosen by
learning progress on one of seven observable outputs (never "a new kind made", never distance) adds the curiosity
pull's size to options expected to move it the chosen way. With `brain_shadow` 1 (and `brain` 0) the memory is kept
outside the world's saved state and only scored: nothing it holds changes any choice.
A memory ends with its owner: the memories of the dead are not kept. PB3: with `brain_lookahead` 1, r-hat uses each
own week's two-week return r(t) + discount x r(t+1), once the next own week is lived. Nothing here uses the world's random generator.
"""
from __future__ import annotations

import hashlib
import random

import numpy as np

from . import fauna, matter, weather
from .config import WEEKS_PER_YEAR
from .person import ACTIONS
from .util import distance

NOUT = 9
GOAL_OUT = (0, 1, 2, 3, 4, 5, 8)        # food gained, net food, health, energy, materials, things held, affection
VISIBLE = np.array([1, 0, 0, 0, 1, 1, 1, 1, 0], dtype=float)
K, EPS, OBS_CAP = 8, 0.05, 1000
LP_WIN, LP_FLOOR, STD_FLOOR = 26, 0.05, 0.05
SEASON = WEEKS_PER_YEAR // 4
ADULT = 16 * WEEKS_PER_YEAR
SOCIAL = ("give", "care", "talk", "court", "steal", "attack")
ACT = {a: i for i, a in enumerate(ACTIONS)}
NA = len(ACTIONS)
MAT = matter.MATERIALS
GROUPS = [list(range(0, 4)), [8, 9, 10, 11, 12, 13, 14, 15], list(range(16, 27)), list(range(27, 32)),
          list(range(89, 114))]
DIDX = np.array([i for g in GROUPS for i in g])
GW = np.concatenate([np.full(len(g), 1.0 / len(g)) for g in GROUPS])
D_IN = 116


def on(world) -> bool:
    c = world.cfg
    return bool((c.brain or c.brain_shadow) and world.tick >= c.brain_on_year * WEEKS_PER_YEAR)


# --- perception (the inputs at a decision) --------------------------------------------------------------------------

def base_inputs(world, p) -> list:
    c, t = world.cfg, world.tick
    w, h = c.width, c.height
    x = [min(1.0, p.edible() / max(1e-9, p.need(c, t)) / 6.0), p.health / 100.0, p.energy / 100.0, float(p.thirst)]
    st = p.stage(t)
    x += [1.0 if st == s else 0.0 for s in ("teen", "adult", "elder")]
    x.append(1.0 if p.sex == "F" else 0.0)
    mate = world.people.get(p.partner) if p.partner else None
    x.append(1.0 if mate is not None and mate.alive and distance(p.loc, mate.loc, w, h) <= c.reach else 0.0)
    x.append(1.0 if any(d.alive and distance(p.loc, d.loc, w, h) <= c.reach for d in world.dependents(p.id)) else 0.0)
    x += [1.0 if world.season == s else 0.0 for s in range(4)]
    x.append(1.0 if weather.raining(world, p.loc) else 0.0)
    x.append(min(1.0, len(world.people_near(p.loc, c.reach, exclude=p.id)) / 12.0))
    tile = world.tile(p.loc)
    x += [min(1.0, tile.plants / 10.0), 1.0 if weather.fresh_near(world, p.loc, c.perception) else 0.0,
          1.0 if tile.fire > 0 else 0.0]
    x += [min(1.0, tile.material(m) / 20.0) for m in MAT]
    if p.items:
        x += [max(it[k] for it in p.items) / 100.0 for k in ("edge", "reach", "hard", "contain")]
    else:
        x += [0.0, 0.0, 0.0, 0.0]
    x.append(min(1.0, len(p.items) / 3.0))
    return x


def option_inputs(world, p, base: list, last2: list, action: str, target) -> np.ndarray:
    x = list(base)
    for k in range(2):
        v = [0.0] * NA
        if len(last2) > k and last2[k] in ACT:
            v[ACT[last2[k]]] = 1.0
        x += v
    v = [0.0] * NA
    v[ACT[action]] = 1.0
    x += v
    tp, mp, rp, kp = [0.0] * 2, [0.0] * 10, [0.0] * 3, [0.0] * 10
    if action in ("forage", "hunt") and isinstance(target, (tuple, list)) and len(target) == 2:
        tt = world.tile(tuple(target))
        tp = [min(1.0, tt.plants / 10.0), min(1.0, fauna.prey_here(world, tuple(target)) / 20.0)]
    elif action == "gather" and isinstance(target, (tuple, list)) and len(target) == 2 and target[1] in MAT:
        mp = [v / 100.0 for v in matter.RAW[target[1]]]
    elif action in SOCIAL and isinstance(target, str):
        r = p.rel.get(target)
        if r is not None:
            rp = [float(r.affection), float(r.trust), float(r.familiarity)]
    elif action == "make" and isinstance(target, str):
        k = world.knowledge.get(target)
        props = k.get("props") if k else None
        if props:
            kp = [float(props.get(q, 0)) / 100.0 for q in matter.PROPS]
    x += tp + mp + rp + kp
    x.append(0.0)
    x.append(1.0)
    return np.array(x, dtype=float)


# --- the memory -----------------------------------------------------------------------------------------------------

class _Store:
    def __init__(self, cap=None, with_r=False):
        self.cap, self.with_r = cap, with_r
        self.X = np.zeros((8, len(DIDX)))
        self.Y = np.zeros((8, NOUT))
        self.M = np.zeros((8, NOUT))
        self.R = np.zeros(8)
        self.C = np.zeros(8, dtype=int)
        self.Wb = np.zeros(8)
        self.n = 0
        self.head = 0

    def add(self, xd, y, m, r, ctx, wb):
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
                for name in ("R", "C", "Wb"):
                    a = getattr(self, name)
                    b = np.zeros(grow, dtype=a.dtype)
                    b[:self.n] = a[:self.n]
                    setattr(self, name, b)
            i = self.n
            self.n += 1
            old = None
        self.X[i], self.Y[i], self.M[i], self.R[i], self.C[i], self.Wb[i] = xd, y, m, r, ctx, wb
        return old

    def to_dict(self):
        n = self.n
        return {"cap": self.cap, "n": n, "head": self.head, "X": self.X[:n].tolist(), "Y": self.Y[:n].tolist(),
                "M": self.M[:n].tolist(), "R": self.R[:n].tolist(), "C": self.C[:n].tolist(), "Wb": self.Wb[:n].tolist()}

    @classmethod
    def from_dict(cls, d):
        s = cls(d["cap"])
        n = d["n"]
        size = max(8, n)
        s.X, s.Y, s.M = np.zeros((size, len(DIDX))), np.zeros((size, NOUT)), np.zeros((size, NOUT))
        s.R, s.C, s.Wb = np.zeros(size), np.zeros(size, dtype=int), np.zeros(size)
        if n:
            s.X[:n], s.Y[:n], s.M[:n] = np.array(d["X"]), np.array(d["Y"]), np.array(d["M"])
            s.R[:n], s.C[:n], s.Wb[:n] = np.array(d["R"]), np.array(d["C"], dtype=int), np.array(d["Wb"])
        s.n, s.head = n, d["head"]
        return s


class Brain:
    def __init__(self):
        self.own = {}                 # action -> _Store (own weeks, with r)
        self.obs = {}                 # action -> _Store (observed weeks, capped)
        self.cells = {}               # "ctx,action" -> [own sum y (9), own sum r, own count, obs sum wmy (9), obs sum wm (9)]
        self.errs = []                # last 2 x LP_WIN weeks of |standardised error| on the goal outputs (lists of 7)
        self.corr = [[0.0] * 5 for _ in GOAL_OUT]   # per goal output: sum y, sum r, sum yr, sum y2, sum r2
        self.ncorr = 0
        self.goal = None              # [output index, direction, seasons kept]
        self.wait = False             # a goal was dropped this season: adopt at the next season start
        self.hid = [0.0, 0.0, 0.0, 0.0]
        self.hid_n = 0
        self.last2 = []
        self.made = []
        self.r2 = {}                  # PB3 (brain_lookahead): action -> own weeks' two-week returns (aligned with own)
        self.r2ok = {}                # PB3: action -> 1 where the next own week has been lived
        self.c2 = {}                  # PB3: "ctx,action" -> [sum of two-week returns, count]
        self.pend = None              # PB3: [action, ctx, index, r] of the last own week, waiting for its next week

    # -- cells
    def _cell(self, ctx, act):
        k = f"{ctx},{act}"
        c = self.cells.get(k)
        if c is None:
            c = self.cells[k] = [[0.0] * NOUT, 0.0, 0, [0.0] * NOUT, [0.0] * NOUT]
        return c

    def add_own(self, act, ctx, xd, y, r):
        self.own.setdefault(act, _Store(with_r=True)).add(xd, y, np.ones(NOUT), r, ctx, 1.0)
        c = self._cell(ctx, act)
        c[0] = [a + b for a, b in zip(c[0], y.tolist())]
        c[1] += r
        c[2] += 1
        for j, o in enumerate(GOAL_OUT):
            v = float(y[o])
            s = self.corr[j]
            s[0] += v
            s[1] += r
            s[2] += v * r
            s[3] += v * v
            s[4] += r * r
        self.ncorr += 1

    def chain2(self, act, ctx, r, disc):
        """PB3: complete the last own week's two-week return with this week's r, then hold this week open."""
        if self.pend is not None:
            pa, pc, pi, pr = self.pend
            v = pr + disc * r
            self.r2[pa][pi], self.r2ok[pa][pi] = v, 1
            c = self.c2.setdefault(f"{pc},{pa}", [0.0, 0])
            c[0] += v
            c[1] += 1
        n = self.own[act].n
        for d, dt in ((self.r2, float), (self.r2ok, int)):
            a = d.get(act)
            if a is None or len(a) < n:
                b = np.zeros(max(8, 2 * n), dtype=dt)
                if a is not None:
                    b[:len(a)] = a
                d[act] = b
        self.pend = [act, ctx, n - 1, r]

    def add_obs(self, act, ctx, xd, y, m, wb):
        old = self.obs.setdefault(act, _Store(cap=OBS_CAP)).add(xd, y, m, 0.0, ctx, wb)
        c = self._cell(ctx, act)
        c[3] = [a + wb * mm * yy for a, mm, yy in zip(c[3], m.tolist(), y.tolist())]
        c[4] = [a + wb * mm for a, mm in zip(c[4], m.tolist())]
        if old is not None:
            octx, oy, om, owb = old
            co = self._cell(octx, act)
            co[3] = [a - owb * mm * yy for a, mm, yy in zip(co[3], om.tolist(), oy.tolist())]
            co[4] = [a - owb * mm for a, mm in zip(co[4], om.tolist())]

    # -- prediction
    def rhat(self, ctx, act, xd):
        c = self.cells.get(f"{ctx},{act}")
        if c is not None and c[2] > 0:
            return c[1] / c[2]
        s = self.own.get(act)
        if s is None or s.n == 0:
            return None
        d = np.sqrt(((s.X[:s.n] - xd) ** 2 * GW).sum(1))
        kk = min(K, s.n)
        idx = np.argpartition(d, kk - 1)[:kk] if kk < s.n else np.arange(s.n)
        w = 1.0 / (d[idx] + EPS)
        return float((w * s.R[idx]).sum() / w.sum())

    def rhat2(self, ctx, act, xd):
        """PB3: r-hat from two-week returns (only own weeks whose next own week has been lived)."""
        c = self.c2.get(f"{ctx},{act}")
        if c is not None and c[1] > 0:
            return c[0] / c[1]
        s = self.own.get(act)
        ok = self.r2ok.get(act)
        if s is None or ok is None:
            return None
        sel = np.flatnonzero(ok[:s.n])
        if not len(sel):
            return None
        d = np.sqrt(((s.X[sel] - xd) ** 2 * GW).sum(1))
        kk = min(K, len(sel))
        idx = np.argpartition(d, kk - 1)[:kk] if kk < len(sel) else np.arange(len(sel))
        w = 1.0 / (d[idx] + EPS)
        return float((w * self.r2[act][sel][idx]).sum() / w.sum())

    def yhat(self, ctx, act, xd):
        c = self.cells.get(f"{ctx},{act}")
        if c is not None and c[2] > 0:
            s = np.array(c[0]) + np.array(c[3])
            w = c[2] + np.array(c[4])
            return s / np.maximum(w, 1e-12)
        parts = [st for st in (self.own.get(act), self.obs.get(act)) if st is not None and st.n]
        if not parts:
            return None
        X = np.vstack([st.X[:st.n] for st in parts])
        Y = np.vstack([st.Y[:st.n] for st in parts])
        M = np.vstack([st.M[:st.n] for st in parts])
        Wb = np.concatenate([st.Wb[:st.n] for st in parts])
        d = np.sqrt(((X - xd) ** 2 * GW).sum(1))
        kk = min(K, len(d))
        idx = np.argpartition(d, kk - 1)[:kk] if kk < len(d) else np.arange(len(d))
        wm = (Wb[idx] / (d[idx] + EPS))[:, None] * M[idx]
        den = wm.sum(0)
        out = np.zeros(NOUT)
        ok = den > 1e-12
        out[ok] = (wm * Y[idx]).sum(0)[ok] / den[ok]
        return out

    def direction(self, j):
        n = self.ncorr
        if n < 2:
            return 1
        sy, sr, syr, syy, srr = self.corr[j]
        cov = syr / n - (sy / n) * (sr / n)
        vy, vr = syy / n - (sy / n) ** 2, srr / n - (sr / n) ** 2
        if vy <= 1e-12 or vr <= 1e-12 or abs(cov) <= 1e-15:
            return 1
        return 1 if cov > 0 else -1

    def lp(self):
        if len(self.errs) < 2 * LP_WIN:
            return None
        e = np.array(self.errs[-2 * LP_WIN:])
        return e[:LP_WIN].mean(0) - e[LP_WIN:].mean(0)

    # -- saving
    def to_dict(self):
        return {"own": {a: s.to_dict() for a, s in sorted(self.own.items())},
                "obs": {a: s.to_dict() for a, s in sorted(self.obs.items())},
                "cells": {k: [list(v[0]), v[1], v[2], list(v[3]), list(v[4])] for k, v in sorted(self.cells.items())},
                "errs": [list(e) for e in self.errs], "corr": [list(s) for s in self.corr], "ncorr": self.ncorr,
                "goal": self.goal, "wait": self.wait, "hid": list(self.hid), "hid_n": self.hid_n,
                "last2": list(self.last2), "made": sorted(self.made)} | self._la_dict()

    def _la_dict(self):
        if self.pend is None and not self.c2:
            return {}                 # saved only when used (PB3's P+), so PB2's saved worlds are unchanged
        return {"r2": {a: v[:self.own[a].n].tolist() for a, v in sorted(self.r2.items())},
                "r2ok": {a: v[:self.own[a].n].tolist() for a, v in sorted(self.r2ok.items())},
                "c2": {k: list(v) for k, v in sorted(self.c2.items())}, "pend": self.pend}

    @classmethod
    def from_dict(cls, d):
        b = cls()
        b.own = {a: _Store.from_dict(s) for a, s in d["own"].items()}
        b.obs = {a: _Store.from_dict(s) for a, s in d["obs"].items()}
        b.cells = {k: [list(v[0]), v[1], v[2], list(v[3]), list(v[4])] for k, v in d["cells"].items()}
        b.errs = [list(e) for e in d["errs"]]
        b.corr = [list(s) for s in d["corr"]]
        b.ncorr, b.goal, b.wait = d["ncorr"], d["goal"], d["wait"]
        b.hid, b.hid_n, b.last2, b.made = list(d["hid"]), d["hid_n"], list(d["last2"]), list(d["made"])
        if "r2" in d:
            for a, v in d["r2"].items():
                b.r2[a] = np.zeros(max(8, 2 * len(v)))
                b.r2[a][:len(v)] = v
            for a, v in d["r2ok"].items():
                b.r2ok[a] = np.zeros(max(8, 2 * len(v)), dtype=int)
                b.r2ok[a][:len(v)] = v
            b.c2 = {k: list(v) for k, v in d["c2"].items()}
            b.pend = d["pend"]
        return b

    def digest(self) -> str:
        h = hashlib.sha256()
        for store in (self.own, self.obs):
            for a in sorted(store):
                s = store[a]
                for arr in (s.X[:s.n], s.Y[:s.n], s.M[:s.n], s.R[:s.n], s.C[:s.n], s.Wb[:s.n]):
                    h.update(np.ascontiguousarray(arr).tobytes())
                h.update(str((a, s.n, s.head)).encode())
        h.update(repr((sorted((k, v[1], v[2]) for k, v in self.cells.items()), self.goal, self.wait, self.ncorr,
                       len(self.errs), self.hid_n, self.last2)).encode())
        if self.pend is not None or self.c2:           # PB3: only when used, so PB2's digests are unchanged
            for a in sorted(self.r2):
                n = self.own[a].n
                h.update(np.ascontiguousarray(self.r2[a][:n]).tobytes())
                h.update(np.ascontiguousarray(self.r2ok[a][:n]).tobytes())
            h.update(repr((sorted((k, v[0], v[1]) for k, v in self.c2.items()), self.pend)).encode())
        return h.hexdigest()


# --- per world state ------------------------------------------------------------------------------------------------

def stats(world) -> dict:
    s = world.brain_stats
    if s is None:
        s = {"n": 0, "m": [0.0] * NOUT, "m2": [0.0] * NOUT, "rq": [0, 0.0, 0.0, 0.0, 0.0],
             "fallback": 0, "steered": 0}
        if world.cfg.brain:
            world.brain_stats = s
        else:
            world._shadow_stats = getattr(world, "_shadow_stats", None) or s
            s = world._shadow_stats
    return s


def brain_of(world, p, create=True):
    if world.cfg.brain:
        if p.brain is None and create:
            p.brain = Brain()
        return p.brain
    sh = world._shadow
    if p.id not in sh and create:
        sh[p.id] = Brain()
    return sh.get(p.id)


def _std(s):
    n = s["n"]
    if n < 2:
        return np.ones(NOUT)
    return np.maximum(np.sqrt(np.array(s["m2"]) / n), STD_FLOOR)


# --- in a decision --------------------------------------------------------------------------------------------------

def decision_start(world, p):
    """Called once at the start of p's decision when the brain is on: perceives the base inputs."""
    world._brain_base = (p.id, world.tick, base_inputs(world, p))


def _x(world, p, action, target):
    pid, t, base = world._brain_base
    b = brain_of(world, p)
    return option_inputs(world, p, base, b.last2, action, target)


def steer(world, p, action, target, qv, ctx, curiosity, hunger):
    """With `brain` 1-3: the value term for an option (r-hat on q's scale, or q when there is none) and the goal bonus."""
    c = world.cfg
    b = brain_of(world, p)
    x = _x(world, p, action, target)
    xd = x[DIDX]
    s = stats(world)
    rh = b.rhat2(ctx, action, xd) if c.brain_lookahead else b.rhat(ctx, action, xd)
    val = qv
    if rh is not None:
        n, mr, m2r, mq, m2q = s["rq"]
        if n >= 30:
            sr = max(np.sqrt(m2r / n), 1e-9)
            sq = np.sqrt(m2q / n)
            val = (rh - mr) / sr * sq + mq
    bonus = 0.0
    if c.brain in (2, 3) and b.goal is not None:
        yh = b.yhat(ctx, action, xd)
        if yh is not None:
            o, direction = GOAL_OUT[b.goal[0]], b.goal[1]
            if yh[o] * direction > 0:
                bonus = 0.3 * curiosity * (1.0 - hunger)
    return val, bonus


def capture(world, p, chosen, ctx, qv_chosen):
    """At the end of p's decision: what they perceived and chose, and their state then."""
    action, target = chosen
    b = brain_of(world, p)
    x = _x(world, p, action, target)
    rh = b.rhat2(ctx, action, x[DIDX]) if world.cfg.brain_lookahead else b.rhat(ctx, action, x[DIDX])
    s = stats(world)
    if rh is not None:
        # running r-hat and q statistics (for the scale), over decisions made with the brain
        n, mr, m2r, mq, m2q = s["rq"]
        n += 1
        dr = rh - mr
        mr += dr / n
        m2r += dr * (rh - mr)
        dq = qv_chosen - mq
        mq += dq / n
        m2q += dq * (qv_chosen - mq)
        s["rq"] = [n, mr, m2r, mq, m2q]
        s["steered"] += 1
    else:
        s["fallback"] += 1
    world._brain_caps[p.id] = {"x": x, "act": action, "ctx": ctx, "loc": tuple(p.loc), "edible": p.edible(),
                               "health": p.health, "energy": p.energy, "mats": p.mat_total(), "items": len(p.items),
                               "aff": sum(r.affection for r in p.rel.values()), "rhat": rh, "q": qv_chosen}


# --- at the end of a week -------------------------------------------------------------------------------------------

def week_end(world, events) -> None:
    caps, world._brain_caps = world._brain_caps, {}
    if not on(world):
        return
    c = world.cfg
    gained, newkind = {}, set()
    for ev in events:
        k, a = ev["k"], ev.get("a")
        if k == "forage" and a:
            gained[a] = gained.get(a, 0.0) + float(ev.get("got", 0.0))
        elif k == "take" and a:
            gained[a] = gained.get(a, 0.0) + float(ev.get("food", 0.0))
        elif k == "hunt":
            party = ev.get("party", ())
            for i in party:
                gained[i] = gained.get(i, 0.0) + float(ev.get("meat", 0.0)) / len(party)
        elif k == "make" and a and a in world.people:
            sig = ev.get("thing")
            b = brain_of(world, world.people[a], create=False)
            if b is not None and sig:
                if sig not in b.made:
                    newkind.add(a)
                    b.made.append(sig)
    s = stats(world)
    std = _std(s)
    mean = np.array(s["m"])
    outs = {}
    for pid in sorted(caps):
        p = world.people[pid]
        if not p.alive:
            continue
        cap = caps[pid]
        y = np.array([gained.get(pid, 0.0), p.edible() - cap["edible"], p.health - cap["health"],
                      p.energy - cap["energy"], p.mat_total() - cap["mats"], len(p.items) - cap["items"],
                      distance(cap["loc"], tuple(p.loc), c.width, c.height), 1.0 if pid in newkind else 0.0,
                      sum(r.affection for r in p.rel.values()) - cap["aff"]], dtype=float)
        outs[pid] = y
    valid = getattr(world, "_brain_valid", None)
    for pid in sorted(outs):
        p, cap, y = world.people[pid], caps[pid], outs[pid]
        b = brain_of(world, p)
        r = p.reward + 2.0 * (p.mood - p.mood_before)
        xd = cap["x"][DIDX]
        if valid is not None and cap["rhat"] is not None:     # arm c: squared errors and moments of r, r-hat, q
            rh, qq = cap["rhat"], cap["q"]
            for i, v in enumerate(((r - rh) ** 2, (r - qq) ** 2, 1, r, r * r, rh, rh * rh, qq, qq * qq, r * rh, r * qq)):
                valid[i] += v
        yh = b.yhat(cap["ctx"], cap["act"], xd)
        if yh is not None:
            err = np.abs((y - yh) / std)
            b.errs.append([float(err[o]) for o in GOAL_OUT])
            if len(b.errs) > 2 * LP_WIN:
                del b.errs[0]
        b.add_own(cap["act"], cap["ctx"], xd, y, float(r))
        if c.brain_lookahead:                 # PB3's P+: the two-week return of the previous own week is now known
            b.chain2(cap["act"], cap["ctx"], float(r), c.discount)
        b.hid = [(h * b.hid_n + v) / (b.hid_n + 1) for h, v in zip(b.hid, cap["x"][:4].tolist())]
        b.hid_n += 1
        b.last2 = [cap["act"]] + b.last2[:1]
    for pid in sorted(outs):
        yv = outs[pid]
        s["n"] += 1
        m = np.array(s["m"])
        d = yv - m
        m = m + d / s["n"]
        s["m2"] = (np.array(s["m2"]) + d * (yv - m)).tolist()
        s["m"] = m.tolist()
    # observed weeks
    for pid in sorted(outs):
        O = world.people[pid]
        b = brain_of(world, O)
        seen = [aid for aid in sorted(outs) if aid != pid
                and distance(tuple(O.loc), caps[aid]["loc"], c.width, c.height) <= c.perception]
        if not seen:
            continue
        wb = 1.0 / len(seen)
        for aid in seen:
            xo = caps[aid]["x"].copy()
            xo[:4] = b.hid
            xo[-2] = 1.0
            b.add_obs(caps[aid]["act"], caps[aid]["ctx"], xo[DIDX], outs[aid], VISIBLE, wb)
    # goals, at the start of each season
    if c.brain in (2, 3) and world.tick % SEASON == 0:
        for pid in sorted(outs):
            p = world.people[pid]
            b = brain_of(world, p)
            lp = b.lp()
            if b.goal is not None:
                b.goal[2] += 1
                if lp is None or lp[b.goal[0]] <= 0 or b.goal[2] >= 4:
                    b.goal = None
                    b.wait = True
                continue
            if b.wait:
                b.wait = False
                continue
            if lp is None:
                continue
            j = int(np.argmax(lp))
            if lp[j] <= LP_FLOOR:
                continue
            if c.brain == 2:
                b.goal = [j, b.direction(j), 0]
            else:                         # G0: the same moment, a random output and direction (a private generator)
                rng = random.Random(int(hashlib.sha256(f"g0:{c.seed}:{pid}:{world.tick}".encode()).hexdigest()[:16],
                                        16))
                b.goal = [rng.randrange(len(GOAL_OUT)), rng.choice((1, -1)), 0]
    # a memory ends with its owner: nothing reads a dead person's memory again, so it is not kept (or saved)
    if c.brain:
        for p in world.people.values():
            if p.brain is not None and not p.alive:
                p.brain = None
    else:
        sh = world._shadow
        for pid in [q for q in sh if not world.people[q].alive]:
            del sh[pid]
