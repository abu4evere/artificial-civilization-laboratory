"""EG1 analysis (questions.md, frozen as `EG1-frozen`). Written before data.

  python experiments/EG1_energy_gate/analyse_eg1.py [output_dir]
"""
from __future__ import annotations

import glob
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "output"
N_BOOT = 10_000
BANDS = ("6-11", "12-15", "16-29", "30-49", "50+")


def load():
    rows = [json.load(open(f)) for f in sorted(glob.glob(str(OUT / "c_seed_*.json")))]
    return rows


def totals(r, starving=None, band=None, sex=None):
    t = Counter()
    for k, v in r["sums"].items():
        b, s, st = k.split("|")
        if starving is not None and int(st) != starving:
            continue
        if band is not None and b != band:
            continue
        if sex is not None and s != sex:
            continue
        t.update(v)
    return t


def boot(rows, f, seed=1):
    rng = random.Random(seed)
    vals = []
    for _ in range(N_BOOT):
        draw = [rows[rng.randrange(len(rows))] for _ in rows]
        v = f(draw)
        if v is not None:
            vals.append(v)
    vals.sort()
    if not vals:
        return None, None
    return vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))]


def share(rows, num, den, **kw):
    n = sum(totals(r, **kw)[num] for r in rows)
    d = sum(totals(r, **kw)[den] for r in rows)
    return n / d if d else None


def fmt(v):
    return "n/a" if v is None else f"{v:.4f}"


def main():
    rows = load()
    print(f"# EG1 results (from {OUT.name})\n")
    fps = {r["code_hash"] for r in rows} | {r["code_hash_after"] for r in rows}
    seeds = sorted(r["seed"] for r in rows)
    print(f"Worlds: {len(rows)} (seeds {seeds[0] if seeds else '-'}-{seeds[-1] if seeds else '-'}); "
          f"fingerprints: {sorted(fps)}; extinct: {sum(1 for r in rows if r['extinct'])}")
    chk = Counter()
    for r in rows:
        chk.update(r["check"])
    bad = chk["forage_mismatch"] + chk["hunt_mismatch"] + chk["energy_mismatch"] + chk["missing_forage_entry"]
    print(f"Hook check over all logged person-weeks ({chk['weeks']}): mismatches {bad} "
          f"({dict(chk)}) -> {'OK' if bad == 0 else 'STOP: the log does not match the options offered'}")
    if len(rows) != 32 or len(fps) != 1 or bad:
        print("\n**Zero check 5 or the hook check fails: the study stops here.**")

    # Primary
    def P(rs):
        return share(rs, "c", "weeks", starving=1)
    p = P(rows)
    lo, hi = boot(rows, P)
    sw = sum(totals(r, starving=1)["weeks"] for r in rows)
    sc = sum(totals(r, starving=1)["c"] for r in rows)
    print(f"\n## Primary\nP = blocked-by-energy-alone starving person-weeks / all starving person-weeks = {sc} / {sw} = "
          f"{fmt(p)}  [95% {fmt(lo)}, {fmt(hi)}]")
    if p is not None and p >= 0.20 and lo >= 0.10:
        reading = "energy binds when starving"
    elif hi is not None and hi < 0.05:
        reading = "energy rarely binds"
    else:
        reading = "a minor contributor"
    print(f"**Reading: {reading}**")

    # S1: four-part split of starving weeks
    print("\n## Secondaries\n1. Starving person-weeks split (a offered and chosen, b offered not chosen, c blocked by "
          "energy alone, d no food feasible):")
    for part in "abcd":
        v = share(rows, part, "weeks", starving=1)
        l, h = boot(rows, lambda rs, part=part: share(rs, part, "weeks", starving=1))
        print(f"   {part}: {fmt(v)} [{fmt(l)}, {fmt(h)}]")

    # S2: by band and sex
    print("2. By age band and sex, starving weeks: weeks; a, b, c, d shares")
    for b in BANDS:
        for sx in ("F", "M"):
            t = Counter()
            for r in rows:
                t.update(totals(r, starving=1, band=b, sex=sx))
            if t["weeks"]:
                print(f"   {b} {sx}: {t['weeks']} weeks; " + ", ".join(f"{k} {t[k] / t['weeks']:.3f}" for k in "abcd"))
            else:
                print(f"   {b} {sx}: 0 weeks")

    # S3: non-starving weeks
    v = share(rows, "c", "weeks", starving=0)
    l, h = boot(rows, lambda rs: share(rs, "c", "weeks", starving=0))
    nw = sum(totals(r, starving=0)["weeks"] for r in rows)
    print(f"3. Non-starving person-weeks blocked by energy alone: {fmt(v)} [{fmt(l)}, {fmt(h)}] of {nw} weeks")

    # S4: the best-tile quirk
    for st, name in ((1, "starving"), (0, "non-starving")):
        q = share(rows, "c_affordable_tile_with_food", "c", starving=st)
        l, h = boot(rows, lambda rs, st=st: share(rs, "c_affordable_tile_with_food", "c", starving=st))
        o = share(rows, "c_own_tile_unaffordable", "c", starving=st)
        print(f"4. Blocked {name} weeks where a tile looked at had food and was affordable (the best-tile quirk): "
              f"{fmt(q)} [{fmt(l)}, {fmt(h)}]; where even one's own tile (25) was unaffordable: {fmt(o)}")

    # S5: what was done instead
    inst = Counter()
    for r in rows:
        inst.update(r["instead"])
    n = sum(inst.values())
    print(f"5. Chosen in blocked starving weeks ({n}): " + ", ".join(f"{k} {v / n:.3f}" for k, v in inst.most_common()))

    # S6: runs
    runs = Counter()
    for r in rows:
        runs.update({int(k): v for k, v in r["runs"].items()})
    nr = sum(runs.values())
    if nr:
        mean = sum(k * v for k, v in runs.items()) / nr
        two = sum(v for k, v in runs.items() if k >= 2) / nr
        print(f"6. Runs of consecutive blocked starving weeks: {nr} runs; mean length {mean:.3f}; share of 2+ weeks "
              f"{two:.4f}; longest {max(runs)}")

    # S7: deaths
    d = Counter()
    for r in rows:
        d.update(r["deaths"])
    ns = d["starvation"]
    if ns:
        f7 = lambda rs: (sum(r["deaths"].get("starvation_blocked_last4", 0) for r in rs)
                         / max(1, sum(r["deaths"].get("starvation", 0) for r in rs)))
        l, h = boot(rows, f7)
        print(f"7. Starvation deaths at 6+: {ns}; with a blocked starving week in their last 4 decisions: "
              f"{d['starvation_blocked_last4']} = {d['starvation_blocked_last4'] / ns:.4f} [{fmt(l)}, {fmt(h)}] "
              f"(with any logged decision in that span: {d['starvation_decided_last4']}); all deaths at 6+ by cause: "
              f"{ {k: v for k, v in d.items() if '_' not in k} }")

    # S8: rest weeks of the grown
    t = Counter()
    for r in rows:
        t.update(totals(r))
    if t["rest"]:
        print(f"8. Rest weeks of the grown (16+, all weeks): {t['rest']}; food blocked by energy alone "
              f"{t['rest_c'] / t['rest']:.4f}; food offered and rest chosen {t['rest_b'] / t['rest']:.4f}; "
              f"no food feasible {t['rest_d'] / t['rest']:.4f}")

    # S9: energy
    for st, name in ((1, "starving"), (0, "non-starving")):
        e = sum(totals(r, starving=st)["energy"] for r in rows)
        w = sum(totals(r, starving=st)["weeks"] for r in rows)
        print(f"9. Mean energy at decision, {name} weeks: {e / w:.2f} ({w} weeks)" if w else f"9. {name}: 0 weeks")


if __name__ == "__main__":
    main()
