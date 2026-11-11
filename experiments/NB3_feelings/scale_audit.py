"""NB3 scale audit (council round 84, GPT): how large would each feeling be, at its start gene, next to the signals the
brain already has? Read-only, on NB2's full brain (code_nb2, arm n), throwaway seeds 9001-9002, 40 years each. It reads
scale only, never survival, and decides nothing by itself: the frozen plan states the choices it informs.

  python experiments/NB3_feelings/scale_audit.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "NB2_connected_brain"))
import run_nb2 as P  # noqa: E402

WPY = P.WPY
STARTS = {"E": 0.5, "G": 0.5, "L": 1.0, "A": 0.5, "C": 0.5, "H": 1.0}


def main():
    out = {}
    for seed in (9001, 9002):
        w = P.make(seed, "n")
        from acl import brain_nb2, mind, actions
        c = w.cfg
        rec = defaultdict(list)
        prev_distress = {}
        prev_aff = {}
        counts = defaultdict(int)
        hits = defaultdict(int)
        learn0 = brain_nb2.learn

        def distress(q):
            need = q.need(c, w.tick) or 1.0
            hunger = min(1.0, max(0.0, 1.0 - (q.edible() / need) / 2.0))
            return (hunger + 1.0 - q.health / 100.0) / 2.0

        def learn(world, p, r, on):
            rec["r"].append(r)
            near = world.people_near(p.loc, c.reach, exclude=p.id)
            if near:
                ws, ds, rises = [], [], []
                for q in near:
                    kin = world.kinship(p, q) > 0 or p.partner == q.id
                    rr = p.rel.get(q.id)
                    wt = 1.0 if kin else (0.5 if rr is not None and rr.affection > 0.3 else 0.2)
                    d = distress(q)
                    ws.append(wt)
                    ds.append(d)
                    rises.append(max(0.0, d - prev_distress.get(q.id, d)))
                ws = np.array(ws)
                rec["empathy_level"].append(float((ws * np.array(ds)).sum() / ws.sum()))
                rec["empathy_rise"].append(float((ws * np.array(rises)).sum() / ws.sum()))
            kids = [world.people[k] for k in p.children if world.people[k].alive and world.people[k].age(world.tick) < 6 * WPY]
            if kids:
                well = [1.0 if (k.edible() >= k.need(c, world.tick) * 0.5 and k.health >= 50 and k.loc == world.people[k.caregiver].loc
                                if k.caregiver in world.people else False) else 0.0 for k in kids]
                rec["love_well"].append(float(np.mean(well)))
                rec["love_concern"].append(float(np.mean([distress(k) for k in kids])))
            aff = sum((q.rel[p.id].affection if p.id in q.rel else 0.0) for q in world.people.values() if q.alive and q.id != p.id
                      ) if (world.tick % 13 == 0) else None
            if aff is not None:
                if p.id in prev_aff:
                    rec["approval_change_per_quarter"].append(aff - prev_aff[p.id])
                prev_aff[p.id] = aff
            key = (p.last_ctx, p.last_action)
            counts[key] += 1
            rec["curiosity"].append(0.1 / counts[key])
            if p.last_action in ("attack", "steal"):
                hits[p.last_action] += 1
            hits["weeks"] += 1
            return learn0(world, p, r, on)
        brain_nb2.learn = learn
        for _ in range(40 * WPY):
            for q in w.living():
                prev_distress[q.id] = distress(q)
            w.step()
            if not w.living():
                break
        brain_nb2.learn = learn0
        rec["attack_week_share"] = [hits["attack"] / max(1, hits["weeks"])]
        rec["steal_week_share"] = [hits["steal"] / max(1, hits["weeks"])]
        for k, v in rec.items():
            out.setdefault(k, []).extend(v)
    S = {}
    for k, v in out.items():
        a = np.array(v, dtype=float)
        S[k] = {"n": int(len(a)), "mean": round(float(a.mean()), 4), "sd": round(float(a.std()), 4),
                "p5": round(float(np.percentile(a, 5)), 4), "p95": round(float(np.percentile(a, 95)), 4)}
    (HERE / "scale_audit.json").write_text(json.dumps(S, indent=1), encoding="utf-8")
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
