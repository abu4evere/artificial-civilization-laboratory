"""S1 — world size (preregistration.md, frozen as `S1-frozen`). Arms differ only in settings (width, height, founders;
the sham adds one random draw in week one), all in P2's code copy (`code_p2`) with every P2/MC1 setting off. Observers:
F1's, HF4's ledger, P2's Encounters (all read-only).

  python experiments/S1_world_size/run_s1.py zero     # code_p2 off == control code at 40x40 and 80x80
  python experiments/S1_world_size/run_s1.py pilot    # run time only: one 120-year world per arm on seeds 9101-9104
  python experiments/S1_world_size/run_s1.py run      # C, L, LP, P, S on the frozen seeds (after the pilot)

Operational detail written before any main-run data: the pilot times every arm (C, L, LP, P on 9101-9104; S costs as C),
not only LP and P, so that the projection in the pre-registration uses measured times for all arms. Only run times are
recorded from the pilot.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "P2_outward_search"))
import run_p2 as R  # noqa: E402

OUT = HERE / "output"
YEARS, WPY = 120, 52
ARMS = {"c": {"width": 40, "height": 40, "founders": 20},
        "l": {"width": 80, "height": 80, "founders": 20},
        "lp": {"width": 80, "height": 80, "founders": 80},
        "p": {"width": 40, "height": 40, "founders": 80},
        "s": {"width": 40, "height": 40, "founders": 20, "sham_draw": 1}}
ALL_SEEDS = tuple(range(3001, 3257))
PILOT = {"c": 9103, "l": 9104, "lp": 9101, "p": 9102}
LIMIT_HOURS = 48


def seeds():
    f = OUT / "pilot.json"
    if not f.exists():
        sys.exit("ABORT: the runtime pilot has not been run")
    return ALL_SEEDS if json.loads(f.read_text(encoding="utf-8"))["use_seeds"] == 256 else ALL_SEEDS[:128]


def zero():
    me = [sys.executable, str((EXP / "P2_outward_search" / "run_p2.py").resolve())]

    def call(code, seed, kw):
        out = subprocess.run(me + ["hashrun", code, str(seed), json.dumps(kw), "1" if code == "p2" else "0"],
                             capture_output=True, text=True).stdout
        return out.strip().splitlines()[-1]
    cases = [(3001, ARMS["c"]), (3002, ARMS["c"]), (3001, ARMS["l"]), (3002, ARMS["lp"])]
    lines, ok = [], True
    for seed, kw in cases:
        t = call("e13r", seed, kw) == call("p2", seed, kw)
        ok &= t
        lines.append(f"code_p2 settings off (observers on) vs control code, {kw['width']}x{kw['height']}, "
                     f"{kw['founders']} founders, seed {seed}, 20 years: identical world: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def manipulation(w) -> dict:
    """Manipulation checks at week one, defined as in the feasibility check (feasibility.py); no outcome."""
    from statistics import mean
    from acl.util import distance
    c = w.cfg
    land = sum(1 for row in w.tiles for t in row if not t.water)
    founders = list(w.people.values())
    band, bands = {}, []
    for p in founders:
        if p.id not in band:
            members = [p] + [w.people[q] for q in p.rel if q in w.people]
            for m in members:
                band[m.id] = len(bands)
            bands.append(members)

    def centre(ms):
        x0, y0 = ms[0].loc
        xs = [x0 + ((m.loc[0] - x0 + c.width // 2) % c.width - c.width // 2) for m in ms]
        ys = [y0 + ((m.loc[1] - y0 + c.height // 2) % c.height - c.height // 2) for m in ms]
        return (round(sum(xs) / len(xs)) % c.width, round(sum(ys) / len(ys)) % c.height)
    cs = [centre(b) for b in bands]
    gaps = [distance(a, b, c.width, c.height) for i, a in enumerate(cs) for b in cs[i + 1:]]
    elig = [[q for q in founders if q.sex != p.sex and w.kinship(p, q) == 0 and abs(p.birth - q.birth) <= 15 * WPY]
            for p in founders]
    return {"land_share": round(land / (c.width * c.height), 3), "land_per_founder": round(land / len(founders), 1),
            "bands": [len(b) for b in bands], "band_gap": round(mean(gaps), 1) if gaps else None,
            "eligible_in_sight_per_founder": round(mean(sum(1 for q in e if distance(p.loc, q.loc, c.width, c.height)
                                                            <= c.perception) for p, e in zip(founders, elig)), 2)}


def run_one(arm, seed, years=YEARS, out=None, record_outcomes=True):
    R.setup("p2")
    from run_f1 import Probe as F1Probe
    from run_hf4 import Ledger
    f0 = R.fingerprint()
    w = R.make_world(seed, **ARMS[arm])
    f1p, lg, enc = F1Probe(), Ledger(), R.Encounters()
    w.ledger, w.p2log = lg.buf, enc.buf
    w.observers += [lg, f1p, enc]
    week1 = manipulation(w)
    t0 = time.perf_counter()
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            break
    secs = time.perf_counter() - t0
    res = {"arm": arm, "seed": seed, "years": years, "seconds": round(secs, 1), "code_hash": f0,
           "code_hash_after": R.fingerprint(), "week1": week1}
    if record_outcomes:
        res.update({"final_tick": w.tick, "world_hash": R.world_hash(w), "ledger": lg.results(), "enc": enc.results(),
                    **f1p.results()})
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: {secs:.0f} s" + (f", pops {f1p.pops}" if record_outcomes else ""), flush=True)


def pilot():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: zero checks have not passed")
    po = HERE / "output_pilot"
    me = [sys.executable, str(Path(__file__).resolve())]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["pilotone", j[0], str(j[1])]), PILOT.items()))
    t = {a: json.loads((po / f"{a}_seed_{s}.json").read_text(encoding="utf-8"))["seconds"] for a, s in PILOT.items()}
    t["s"] = t["c"]
    hours = 256 * sum(t.values()) / 4 / 3600
    use = 256 if hours <= LIMIT_HOURS else 128
    res = {"seconds_per_world": t, "projected_hours_256": round(hours, 1), "limit_hours": LIMIT_HOURS, "use_seeds": use}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "pilot.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1), flush=True)


def run_all():
    v = OUT / "zero.txt"
    if not v.exists() or "All: PASS" not in v.read_text(encoding="utf-8"):
        sys.exit("ABORT: zero checks have not passed")
    S = seeds()
    R.setup("p2")
    fp = R.fingerprint()
    me = [sys.executable, str(Path(__file__).resolve())]
    # slowest arms first, so the four workers finish together
    todo = [(a, s) for a in ("lp", "p", "l", "c", "s") for s in S if not (OUT / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["one", j[0], str(j[1])]), todo))
    bad = [(a, s) for a in ARMS for s in S
           if json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8"))["code_hash"] != fp]
    print("ALL DONE; code fingerprint unchanged" if not bad else f"HARD STOP: fingerprint changed in {bad[:5]}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "pilot":
        pilot()
    elif cmd == "pilotone":
        run_one(sys.argv[2], int(sys.argv[3]), out=HERE / "output_pilot", record_outcomes=False)
    elif cmd == "one":
        run_one(sys.argv[2], int(sys.argv[3]))
    elif cmd == "run":
        run_all()
