"""AP1 — why are couples apart? (questions.md, frozen as `AP1-frozen`). Read-only: CT1's C and K1 worlds, seeds
8201-8328, replayed exactly with `code_ct1` and a read-only observer. Each replay's final state hash must equal CT1's.

  python experiments/AP1_why_apart/run_ap1.py zero    # observer changes nothing (C and K1, seed 501, 20 years)
  python experiments/AP1_why_apart/run_ap1.py smoke   # throwaway seeds 9981-9982, 6 years (code check only)
  python experiments/AP1_why_apart/run_ap1.py run     # c, k1 on seeds 8201-8328, 120 years (skips saved)
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "CT1_courting_nature"))
import run_ct1 as R  # noqa: E402

OUT = HERE / "output"
SAVED = EXP / "CT1_courting_nature" / "output"
WPY, YEARS = 52, 120
SEEDS = tuple(range(8201, 8329))
SMOKE_SEEDS = (9981, 9982)
ARMS = {"c": R.ARMS["c"], "k1": R.ARMS["k1"]}

# Operational note (before data): fill (fetching water) and heat (cooking) count as subsistence; put, make, steal,
# attack count as "other". See questions.md.
CLASS = {}
for a in ("forage", "gather", "hunt", "take", "fill", "heat"):
    CLASS[a] = "subsistence"
for a in ("care", "give"):
    CLASS[a] = "care"
for a in ("talk", "court", "play"):
    CLASS[a] = "social"
for a in ("explore", "join", "flee"):
    CLASS[a] = "moving"
CLASS["rest"] = "rest"
SPELL_EDGES = (1, 2, 4, 8, 13, 26, 52, 104, 10 ** 9)


def act_class(p):
    if getattr(p, "voyage", None):
        return "moving"
    return CLASS.get(p.last_action, "other")


def reason(a, b):
    if "moving" in (a, b):
        return "one_moving"
    if "care" in (a, b):
        return "one_caring"
    if a == "subsistence" and b == "subsistence":
        return "both_subsistence"
    if "rest" in (a, b):
        return "one_resting"
    return "other"


class Apart:
    """Read-only, after each week: for each fertile, non-pregnant woman with a living partner (F1's order of checks),
    whether the couple is apart, what each was doing, who moved, starving flags, and separation spells."""

    def __init__(self):
        self.c = Counter()
        self.prev = {}                     # woman id -> (partner id, her loc, his loc, apart?)
        self.spell = {}                    # woman id -> (partner id, length)

    def _close(self, wid, reunited):
        if wid in self.spell:
            pid, n = self.spell.pop(wid)
            b = next(i for i, e in enumerate(SPELL_EDGES) if n <= e)
            self.c[f"spell_len_b{b}"] += 1
            self.c["spells"] += 1
            self.c["spell_weeks"] += n
            self.c["spells_reunited" if reunited else "spells_open"] += 1

    def __call__(self, world, events):
        from acl.util import distance
        c, tick = world.cfg, world.tick
        seen = set()
        for p in world.living():
            if p.sex != "F" or not (c.fertile_from <= p.years(tick) < c.fertile_until) or p.pregnant is not None:
                continue
            if p.partner is None:
                continue
            m = world.people.get(p.partner)
            if m is None or not m.alive:
                continue
            seen.add(p.id)
            d = distance(p.loc, m.loc, c.width, c.height)
            apart = d > c.camp_radius
            ca, cb = act_class(p), act_class(m)
            self.c["partnered_weeks"] += 1
            if apart:
                self.c["apart_weeks"] += 1
                self.c[f"reason_{reason(ca, cb)}"] += 1
                self.c[f"her_{ca}"] += 1
                self.c[f"him_{cb}"] += 1
                self.c["apart_starving"] += bool(p.starving or m.starving)
                self.c["apart_dist_sum"] += d
            else:
                self.c["together_weeks"] += 1
                self.c["together_starving"] += bool(p.starving or m.starving)
            pv = self.prev.get(p.id)
            if pv and pv[0] == m.id and not pv[3] and apart:          # together last week, apart now: who moved?
                only_her = distance(p.loc, pv[2], c.width, c.height) > c.camp_radius
                only_him = distance(pv[1], m.loc, c.width, c.height) > c.camp_radius
                who = "both" if only_her == only_him else ("her" if only_her else "him")
                self.c[f"split_{who}"] += 1
            sp = self.spell.get(p.id)
            if apart:
                if sp and sp[0] == m.id:
                    self.spell[p.id] = (m.id, sp[1] + 1)
                else:
                    self._close(p.id, False)
                    self.spell[p.id] = (m.id, 1)
            elif sp:
                self._close(p.id, sp[0] == m.id)
            self.prev[p.id] = (m.id, p.loc, m.loc, apart)
        for wid in list(self.spell):                                   # no longer a fertile, partnered, unpregnant woman
            if wid not in seen:
                self._close(wid, False)
                self.prev.pop(wid, None)

    def results(self):
        for wid in list(self.spell):
            self._close(wid, False)
        return {"apart": dict(self.c)}


def hashrun(arm, seed, years, observe):
    R.setup("ct1")
    w = R.make_world(seed, ARMS[arm])
    if observe:
        w.observers.append(Apart())
    for _ in range(years * WPY):
        w.step()
    return R.world_hash(w)


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(*args):
        r = subprocess.run(me + ["hashrun", *map(str, args)], capture_output=True, text=True)
        if r.returncode or not r.stdout.split():
            sys.exit("hash run failed: " + " ".join(map(str, args)) + chr(10) + r.stderr[-2000:])
        return r.stdout.split()[-1]
    lines, ok = [], True
    for arm in ("c", "k1"):
        t = call(arm, 501, 20, 1) == call(arm, 501, 20, 0)
        ok &= t
        lines.append(f"arm {arm}, seed 501, 20 years: identical with and without the observer: {'yes' if t else 'NO'}")
    R.setup("ct1")
    lines.append(f"code_ct1 fingerprint: {R.fingerprint()}")
    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n"
    (OUT / "zero.txt").write_text(text, encoding="utf-8")
    print(text, flush=True)
    return ok


def run_one(arm, seed, years=YEARS, out=None):
    R.setup("ct1")
    f0 = R.fingerprint()
    w = R.make_world(seed, ARMS[arm])
    ob = Apart()
    w.observers.append(ob)
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    res = {"arm": arm, "seed": seed, "nature": "v3", "code_hash": f0, "final_tick": w.tick,
           "world_hash": R.world_hash(w), **ob.results()}
    saved = SAVED / f"{arm}_seed_{seed}.json"
    if saved.exists() and years == YEARS:
        res["reproduces"] = json.loads(saved.read_text(encoding="utf-8"))["world_hash"] == res["world_hash"]
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: done, tick {w.tick}, reproduces {res.get('reproduces')}", flush=True)


def batch(seeds=SEEDS, years=YEARS, out=OUT):
    q = (HERE / "questions.md").read_text(encoding="utf-8")
    if "SIGNED OFF" not in q.splitlines()[0]:
        sys.exit("ABORT: AP1 is not signed off")
    me = [sys.executable, str(Path(__file__).resolve())]
    todo = [(a, s) for s in seeds for a in ARMS if not (out / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1]), str(years), str(out)]), todo))
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "hashrun":
        print(hashrun(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5] == "1"))
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    elif cmd == "smoke":
        batch(SMOKE_SEEDS, 6, HERE / "output_smoke")
    elif cmd == "run":
        batch()
