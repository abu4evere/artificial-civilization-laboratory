"""WM1 — why do women die younger than men? (questions.md, frozen as `WM1-frozen`).

Part A (read-only): live nature v7 (`code_v7`) with a logging observer, settings C20 and D80.
Part B (diagnostic arms, C20): `code_wm1` = v7 + three switches, each 0 = v7 exactly (`v7_to_wm1.diff`):
`wm1_p0` (pregnancy needs no extra food), `wm1_b0` (no childbirth deaths; the draw is kept), `wm1_k0` (a carer meets
her own need before feeding dependants). A full 2 x 2 x 2 design; its all-off cell is Part A's C20 (code_v7).

  python experiments/WM1_why_women_die_younger/run_wm1.py zero    # hard stops (writes output/zero.txt)
  python experiments/WM1_why_women_die_younger/run_wm1.py one <arm> <seed> <years> <out>    # one world (cloud-run)
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
CODES = {"v7": EXP / "NV7_nature_v7" / "code_v7", "wm1": HERE / "code_wm1"}
OUT = HERE / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(17001, 17129))       # 128 new seeds, used by no study
SMOKE_SEEDS = (9963, 9962)
V7 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
      "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1}
SW = {"p": "wm1_p0", "b": "wm1_b0", "k": "wm1_k0"}


def _arm(name):
    if name == "c20":
        return {"code": "v7", "kw": {}}
    if name == "d80":
        return {"code": "v7", "kw": {"founders": 80}}
    return {"code": "wm1", "kw": {SW[ch]: 1 for ch in name}}


ARMS = {a: _arm(a) for a in ("c20", "d80", "p", "b", "k", "pb", "pk", "bk", "pbk")}
BANDS = ((16, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, 55), (55, 200))


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    sys.path.insert(1, str(EXP / "E7_passive"))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


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


def fingerprint(code):
    from run_e7 import code_hash
    return code_hash(CODES[code] / "acl")


def band_of(years):
    for lo, hi in BANDS:
        if lo <= years < hi:
            return f"{lo}-{hi - 1}" if hi < 200 else "55+"
    return None


def cut(x, edges, labels):
    for e, lab in zip(edges, labels):
        if x <= e:
            return lab
    return labels[-1]


class WM1Obs:
    """Read-only. At the start of every week (the end of the last), each living person aged 16+ is put in cells by
    independent indicators; deaths during the week are counted in those cells. Reads the food ledger (`world.ledger`,
    HF4's logging copy, which nothing in nature reads), the week's events and each person's action."""

    def __init__(self, w):
        w.ledger = []
        self.cells = {}                    # "group|sex|band|indicator|value" -> [pw, health_sum, sick_weeks, fed, deaths{}]
        self.deaths = []
        self.hist = {}                     # pid -> {"def": deque(13), "sick": deque(52), "fed": deque(13), "recv": deque(13), "share": float}
        self.expo = {}                     # "sex|group|what" -> number
        self.prov = {}                     # "recipient sex|recipient state|giver relation" -> food
        self.carer_weeks = {"F": 0, "M": 0}
        self.pops = []
        self.assign = {}
        self.snapshot(w)

    def h(self, pid):
        if pid not in self.hist:
            self.hist[pid] = {"def": deque(maxlen=13), "sick": deque(maxlen=52), "fed": deque(maxlen=13),
                              "recv": deque(maxlen=13), "share": 0.0}
        return self.hist[pid]

    def add(self, key, field, x=1.0):
        c = self.cells.setdefault(key, [0, 0.0, 0, 0.0, {}])
        c[field] += x

    def state_of(self, w, p):
        """The indicators at the start of a week."""
        t = w.tick
        hp = self.h(p.id)
        deps = len(w.dependents(p.id))
        preg = p.pregnant is not None
        since = (t - p.last_birth) if p.sex == "F" and p.last_birth > -10_000 else None
        ind = {"all": "all"}
        ind["cohort"] = ("founder" if p.birth < 0 else
                         cut(p.birth / WPY, (40, 70), ("born <40", "born 40-69", "born 70+")))
        if p.sex == "F":
            ind["preg"] = (f"trim{min(3, (t - p.conceived) // 13 + 1)}" if preg else "no")
            ind["since"] = ("never" if since is None else cut(since, (12, 52, 104), ("0-12", "13-52", "53-104", ">104")))
            ind["preg_deps"] = ("preg+deps" if preg and deps else "preg only" if preg else
                                "deps only" if deps else "neither")
        ind["deps"] = cut(deps, (0, 1, 2), ("0", "1", "2", "3+"))
        sh = hp["share"]
        ind["fed_share"] = "0" if sh <= 0 else cut(sh, (0.25, 0.5), ("<25%", "25-50%", ">50%"))
        d13 = sum(hp["def"]) / len(hp["def"]) if hp["def"] else 0.0
        ind["deficit13"] = "0" if d13 <= 0.0 else cut(d13, (0.1, 0.3), ("0-0.1", "0.1-0.3", ">0.3"))
        ind["sick_now"] = "yes" if p.sick else "no"
        ind["sick_year"] = cut(sum(hp["sick"]), (0, 4), ("0", "1-4", "5+"))
        ind["health"] = cut(p.health, (40, 70, 90), ("<40", "40-70", "70-90", ">=90"))
        if preg:
            load = "pregnant"
        elif since is not None and since <= 52:
            load = "after delivery"
        elif deps:
            load = "carer"
        else:
            load = "unloaded"
        ind["load"] = load
        return ind, deps

    def snapshot(self, w):
        t = w.tick
        self.assign = {}
        for p in w.living():
            y = p.years(t)
            if y < 16:
                continue
            band = band_of(y)
            group = "world" if p.birth >= 0 else "founder"
            ind, deps = self.state_of(w, p)
            keys = [f"{group}|{p.sex}|{band}|{k}|{v}" for k, v in ind.items()]
            for k in keys:
                self.add(k, 0, 1)
                self.add(k, 1, p.health)
                self.add(k, 2, 1 if p.sick else 0)
            if deps:
                self.carer_weeks[p.sex] += 1
            self.assign[p.id] = (keys, ind, p.loc, group)

    def __call__(self, w, events):
        t_week = w.tick - 1                # the week that just ran
        led = w.ledger
        fed_now = {}
        for pid, _adult, need, _held, deficit, fed in led:
            hp = self.h(pid)
            hp["def"].append(max(0.0, deficit))
            hp["fed"].append(fed)
            hp["share"] = fed / need if need > 0 else 0.0
            fed_now[pid] = fed
        del led[:]
        recv_now = {}
        for ev in events:
            k = ev.get("k")
            a, b = ev.get("a"), ev.get("b")
            if k == "give" and b in w.people:
                q, g = w.people[b], w.people.get(a)
                amt = ev.get("amount", 0.0)
                recv_now[b] = recv_now.get(b, 0.0) + amt
                if b in self.assign and g is not None:
                    rel = "partner" if q.partner == a else "kin" if w.kinship(q, g) > 0 else "other"
                    key = f"{q.sex}|{self.assign[b][1]['load']}|{rel}"
                    self.prov[key] = self.prov.get(key, 0.0) + amt
            for pid, what in ((a, k), (b, k + "_on")):
                if pid in self.assign and k in ("attack", "kill", "injured"):
                    p = w.people[pid]
                    key = f"{p.sex}|{self.assign[pid][3]}|{what}"
                    self.expo[key] = self.expo.get(key, 0) + 1
        for pid, (keys, ind, loc0, group) in self.assign.items():
            p = w.people[pid]
            hp = self.h(pid)
            hp["recv"].append(recv_now.get(pid, 0.0))
            for k in keys:
                self.add(k, 3, fed_now.get(pid, 0.0))
            for what, x in (("weeks", 1), ("hunt_weeks", 1 if p.doing == "hunt" else 0),
                            ("travel", abs(p.loc[0] - loc0[0]) + abs(p.loc[1] - loc0[1]))):
                key = f"{p.sex}|{group}|{what}"
                self.expo[key] = self.expo.get(key, 0) + x
            if not p.alive and p.death_tick == t_week:
                cause = p.death_cause or "unknown"
                for k in keys:
                    dd = self.cells[k][4]
                    dd[cause] = dd.get(cause, 0) + 1
                mate = w.people.get(p.partner) if p.partner else None
                self.deaths.append({
                    "group": group, "sex": p.sex, "age": round(p.years(t_week), 2), "cause": cause,
                    "ind": ind, "partner_alive": bool(mate and mate.alive),
                    "partner_near": bool(mate and mate.alive and abs(mate.loc[0] - p.loc[0]) <= 2
                                         and abs(mate.loc[1] - p.loc[1]) <= 2),
                    "fed13": round(sum(hp["fed"]), 2), "recv13": round(sum(hp["recv"]), 2),
                    "def13": round(sum(hp["def"]) / max(1, len(hp["def"])), 3), "sick52": sum(hp["sick"])})
        for pid in self.assign:
            self.h(pid)["sick"].append(1 if w.people[pid].sick else 0)
        if w.tick % WPY == 0:
            self.pops.append(len(w.living()))
        self.snapshot(w)


def summarise(w):
    """Births per world-born woman reaching 45, and child survival to 5 (full follow-up), for the arms' side effects."""
    end = w.tick
    kids = [p for p in w.people.values() if p.birth >= 0 and p.birth + 5 * WPY <= end]
    surv5 = sum(1 for p in kids if p.alive or p.death_tick - p.birth >= 5 * WPY)
    women = [p for p in w.people.values() if p.sex == "F" and p.birth >= 0 and p.birth + 45 * WPY <= end
             and (p.alive or p.death_tick - p.birth >= 45 * WPY)]
    births = sum(len({w.people[c].birth for c in p.children if w.people[c].mother == p.id}) for p in women)
    return {"child5": [surv5, len(kids)], "women45": len(women), "deliveries_women45": births}


def hashrun(code, seed, years, kw, observe):
    setup(code)
    w = make_world(seed, kw)
    if observe:
        w.observers.append(WM1Obs(w))
    for _ in range(years * WPY):
        w.step()
    return world_hash(w) + ":" + rng_state(w)


def reload_check(code, seed, kw):
    setup(code)
    from acl.world import World
    a = make_world(seed, kw)
    for _ in range(10 * WPY):
        a.step()
    b = World.from_dict(json.loads(json.dumps(a.to_dict())))
    for w in (a, b):
        for _ in range(5 * WPY):
            w.step()
    return world_hash(a) == world_hash(b)


def unit_tests():
    """Each switch changes only its own rule (direct calls on a real world)."""
    setup("wm1")
    from acl import biology
    from acl.config import CHILD_END
    lines, ok = [], True

    def world(kw):
        w = make_world(11, kw)
        for _ in range(3):
            w.step()
        return w
    # P0: a pregnant woman's need
    needs = {}
    for name, kw in (("off", {}), ("p0", {"wm1_p0": 1})):
        w = world(kw)
        mum = [p for p in w.living() if p.sex == "F" and p.age(w.tick) >= CHILD_END][0]
        base = mum.need(w.cfg, w.tick)
        mum.pregnant = "x"
        needs[name] = (base, mum.need(w.cfg, w.tick))
    t = needs["off"][1] == needs["off"][0] + 1.5 and needs["p0"][1] == needs["p0"][0]
    lines.append(f"P0: pregnancy adds 1.5 to need when off, nothing when on; other needs unchanged: {'yes' if t else 'NO'}")
    ok &= t
    # B0: a forced childbirth-death draw kills when off, not when on; the draw is consumed either way
    res = {}
    for name, kw in (("off", {}), ("b0", {"wm1_b0": 1})):
        w = world(kw)
        mum = [p for p in w.living() if p.sex == "F" and p.age(w.tick) >= CHILD_END][0]
        dad = [p for p in w.living() if p.sex == "M" and p.age(w.tick) >= CHILD_END][0]
        mum.pregnant = dad.id
        w.cfg.birth_death_chance = 1.0                  # any draw is below it: she dies unless the switch blocks it
        n0 = len(w.people)
        biology.give_birth(w, mum)
        res[name] = (mum.alive, len(w.people) - n0, rng_state(w))
    t = (res["off"][0] is False and res["b0"][0] is True and res["off"][1] == res["b0"][1] >= 1
         and res["off"][2] == res["b0"][2])
    lines.append(f"B0: a forced childbirth draw kills when off, not when on; same birth and same draws: {'yes' if t else 'NO'}")
    ok &= t
    # K0: a carer with too little food
    got = {}
    for name, kw in (("off", {}), ("k0", {"wm1_k0": 1})):
        w = world(kw)
        carer = [p for p in w.living() if p.age(w.tick) >= CHILD_END][0]
        kid = [p for p in w.living() if p.id != carer.id][0]
        kid.birth = w.tick - 2 * WPY
        kid.caregiver = carer.id
        carer.wards.append(kid.id)
        carer.food, carer.seeds, kid.food, kid.seeds = 5.0, 0.0, 0.0, 0.0
        own = carer.need(w.cfg, w.tick)
        before = carer.food
        # the feeding block alone: run body_phase's first part by calling it and reading food moved to the child
        w.ledger = []
        biology.body_phase(w)
        fed = [e[5] for e in w.ledger if e[0] == carer.id]
        got[name] = (fed[0] if fed else None, own, before)
    off_fed, own, before = got["off"]
    k_fed = got["k0"][0]
    t = off_fed is not None and off_fed > 0 and k_fed == 0.0 and before < own
    lines.append(f"K0: a carer holding less than her own need feeds the child when off, nothing when on: {'yes' if t else 'NO'}")
    ok &= t
    return ok, lines


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + [*map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for seed, years in ((11, 5), (501, 5), (501, 20), (601, 20)):
        t = call("hashrun", "wm1", seed, years, "{}", 0) == call("hashrun", "v7", seed, years, "{}", 0)
        ok &= t
        lines.append(f"seed {seed}, {years} years: code_wm1 with all switches 0 = code_v7, state and random numbers: "
                     f"{'yes' if t else 'NO'}")
    off = {s: call("hashrun", "wm1", s, 20, "{}", 0) for s in (501, 601)}
    for ch, sw in SW.items():
        if ch == "b":
            continue
        t = any(call("hashrun", "wm1", s, 20, json.dumps({sw: 1}), 0) != off[s] for s in (501, 601))
        ok &= t
        lines.append(f"switch {ch.upper()}0 alone, seeds 501/601, 20 years: changes the world (it acts): {'yes' if t else 'NO'}")
    # Operational amendment 1: childbirth deaths are rare (none in 20 years on seeds 501-508), so B0 is checked on the
    # first of seeds 501-520 whose v7 world has a childbirth death, run to one year after that death.
    found = call("firstbirthdeath")
    if found == "none":
        t = False
        lines.append("switch B0 alone: no childbirth death found on seeds 501-520 in 120 years: NO")
    else:
        s, yrs = map(int, found.split(","))
        t = call("hashrun", "wm1", s, yrs, json.dumps({"wm1_b0": 1}), 0) != call("hashrun", "wm1", s, yrs, "{}", 0)
        lines.append(f"switch B0 alone, seed {s} (its first childbirth death), {yrs} years: changes the world (it acts): "
                     f"{'yes' if t else 'NO'}")
    ok &= t
    for arm, a in ARMS.items():
        kw = json.dumps(a["kw"])
        t = call("hashrun", a["code"], 501, 20, kw, 1) == call("hashrun", a["code"], 501, 20, kw, 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without the observer: {'yes' if t else 'NO'}")
    for arm in ("c20", "pbk"):
        a = ARMS[arm]
        t = call("reload", a["code"], 501, json.dumps(a["kw"])) == "True"
        ok &= t
        lines.append(f"arm {arm}, seed 501: saved at year 10 and reloaded, continues exactly to year 15: {'yes' if t else 'NO'}")
    r = subprocess.run(me + ["units"], capture_output=True, text=True)
    t = r.returncode == 0 and "All units: PASS" in r.stdout
    ok &= t
    lines += [ln for ln in r.stdout.splitlines() if ln.strip() and not ln.startswith("All units")] or [r.stderr[-1500:]]
    lines.append(f"unit tests: {'yes' if t else 'NO'}")
    lines.append(f"code_v7 fingerprint: {call('fp', 'v7')}")
    lines.append(f"code_wm1 fingerprint: {call('fp', 'wm1')}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    a = ARMS[arm]
    setup(a["code"])
    f0 = fingerprint(a["code"])
    w = make_world(seed, a["kw"])
    obs = WM1Obs(w)
    w.observers.append(obs)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "code": a["code"], "kw": a["kw"], "code_hash": f0,
           "code_hash_after": fingerprint(a["code"]), "final_tick": w.tick, "world_hash": world_hash(w),
           "pops": obs.pops, "cells": obs.cells, "deaths": obs.deaths, "expo": obs.expo, "prov": obs.prov,
           "carer_weeks": obs.carer_weeks, **summarise(w)}
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), json.loads(sys.argv[5]), sys.argv[6] == "1"))
    elif cmd == "reload":
        print(reload_check(sys.argv[2], int(sys.argv[3]), json.loads(sys.argv[4])))
    elif cmd == "firstbirthdeath":
        setup("v7")
        res = "none"
        for s in range(501, 521):
            w = make_world(s, {})
            for _ in range(YEARS * WPY):
                w.step()
                if any(not p.alive and p.death_cause == "childbirth" for p in w.people.values()):
                    res = f"{s},{w.tick // WPY + 1}"
                    break
            if res != "none":
                break
        print(res)
    elif cmd == "fp":
        setup(sys.argv[2])
        print(fingerprint(sys.argv[2]))
    elif cmd == "units":
        ok, lines = unit_tests()
        print("\n".join(lines))
        print(f"All units: {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    elif cmd == "one":
        assert sys.argv[2] in ARMS
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
