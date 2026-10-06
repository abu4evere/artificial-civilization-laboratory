"""U — uncertain years (preregistration.md). Arms: c (as now), w (wider, world-wide), p (wider, by quarter of the map).

  python experiments/N4_uncertain_winters/run_u.py zero        # zero checks and region tests
  python experiments/N4_uncertain_winters/run_u.py calibrate   # land variability only, W at four half-widths
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E13R = HERE.parent / "E13R_replication"
CODES = {"u": HERE / "code_u", "e13r": E13R / "code_e13r"}
MEAN = 0.95
HALF_WIDTHS = (0.30, 0.50, 0.70, 0.95)
CALIB = tuple(range(801, 805))
WPY, WPS = 52, 13
OUT = HERE / "output"


def setup(code):
    sys.path.insert(0, str(CODES[code]))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODES[code] / "acl").resolve()


def settings(arm, half):
    s = {"weather_low": round(MEAN - half, 4), "weather_high": round(MEAN + half, 4)} if arm in ("w", "p") else {}
    if arm == "p":
        s["weather_regions"] = 4
    return s


def make_world(seed, **kw):
    from acl.config import Config
    from acl.world import World
    return World(Config(seed=seed, anticipation_weight=1.0, **kw))


def hash_run(code, seed, years, kw):
    setup(code)
    w = make_world(seed, **kw)
    weathers = []
    for _ in range(years * WPY):
        w.step()
        if (w.tick - 1) % WPY == 0:
            weathers.append(w.weather)
    import hashlib
    d = w.to_dict()
    d.pop("cfg")                       # the arms' settings differ by design; compare the world itself
    h = hashlib.sha256(json.dumps(d, separators=(",", ":")).encode()).hexdigest()
    return {"hash": h, "weathers": weathers, "regions": getattr(w, "region_weather", None)}


def zero():
    me = [sys.executable, str(Path(__file__).resolve())]

    def call(code, kw):
        out = subprocess.run(me + ["hashrun", code, json.dumps(kw)], capture_output=True, text=True).stdout.strip()
        return json.loads(out.splitlines()[-1])
    lines, ok = [], True
    a, b = call("e13r", {}), call("u", {})
    t = a["hash"] == b["hash"]
    ok &= t
    lines.append(f"1. U code, defaults, equals E13R code (world state without settings, seed 501, 10 years): {'yes' if t else 'NO'}")
    wide = settings("w", 0.70)
    a, b = call("e13r", wide), call("u", wide)
    t = a["hash"] == b["hash"]
    ok &= t
    lines.append(f"2. U code with W's wider setting equals E13R code with the same setting: {'yes' if t else 'NO'}")
    p = call("u", settings("p", 0.70))
    t = p["weathers"][:1] == b["weathers"][:1]
    ok &= t
    lines.append(f"3. P makes no extra draws from the world's random stream (first year's world weather identical to W's; "
                 f"later years diverge in every arm as worlds differ): {'yes' if t else 'NO'}")
    rw = p["regions"]
    t = rw is not None and len(rw) == 4 and len(set(rw)) > 1 and all(MEAN - 0.70 <= x <= MEAN + 0.70 for x in rw)
    ok &= t
    lines.append(f"4. P draws four different regional weathers within the range: {'yes' if t else 'NO'} ({rw})")
    setup("u")
    from acl.config import Config
    c = Config()
    idx = lambda x, y: (1 if y >= c.height // 2 else 0) * 2 + (1 if x >= c.width // 2 else 0)
    t = [idx(0, 0), idx(c.width - 1, 0), idx(0, c.height - 1), idx(c.width - 1, c.height - 1)] == [0, 1, 2, 3]
    ok &= t
    lines.append(f"5. Region index maps the four corners to the four quarters: {'yes' if t else 'NO'}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "zero.txt").write_text("\n".join(lines) + f"\nAll: {'PASS' if ok else 'FAIL'}\n", encoding="utf-8")
    print("\n".join(lines), f"\nAll: {'PASS' if ok else 'FAIL'}", flush=True)
    return ok


def calibrate_one(half, seed):
    """Land only: year-to-year variability of mid-autumn plant food per land tile, and its mean."""
    setup("u")
    w = make_world(seed, **settings("w", half))
    land = [t for row in w.tiles for t in row if not t.water]
    autumn = []
    for _ in range(120 * WPY):
        w.step()
        if (w.tick - 1) % WPY == 2 * WPS + 6:
            autumn.append(sum(t.plants + t.crop for t in land) / len(land))
        if not w.living():
            break
    a = autumn[1:]
    cv = statistics.pstdev(a) / statistics.mean(a) if len(a) > 5 else None
    res = {"half": half, "seed": seed, "years": len(a), "cv": cv, "mean": statistics.mean(a) if a else None}
    (OUT / "calibration").mkdir(parents=True, exist_ok=True)
    (OUT / "calibration" / f"h{half}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"calibration half-width {half} seed {seed}: cv {cv}", flush=True)


def calibrate():
    me = [sys.executable, str(Path(__file__).resolve())]
    jobs = [(h, s) for h in HALF_WIDTHS for s in CALIB]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: subprocess.call(me + ["calone", str(j[0]), str(j[1])]), jobs))
    rows = []
    for h in HALF_WIDTHS:
        r = [json.loads((OUT / "calibration" / f"h{h}_seed_{s}.json").read_text(encoding="utf-8")) for s in CALIB]
        cvs = [x["cv"] for x in r if x["cv"] is not None]
        means = [x["mean"] for x in r if x["mean"] is not None]
        rows.append((h, statistics.median(cvs), statistics.mean(means)))
    base = rows[0][2]
    lines = [f"half-width {h}: median CV {cv:.3f}, mean food per land tile {m:.2f} ({m / base:.3f} of half-width 0.30's)"
             for h, cv, m in rows]
    target = 1 / 3
    reach = [r for r in rows if r[1] >= target]
    chosen = min(rows, key=lambda r: abs(r[1] - target))[0] if reach else rows[-1][0]
    note = "nearest to one third" if reach else "none reaches one third: the widest is used and the shortfall reported"
    lines.append(f"RULE: chosen half-width {chosen} ({note}).")
    (OUT / "calibration" / "verdict.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "hashrun":
        print(json.dumps(hash_run(sys.argv[2], 501, 10, json.loads(sys.argv[3]))))
    elif cmd == "zero":
        sys.exit(0 if zero() else 1)
    elif cmd == "calone":
        calibrate_one(float(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "calibrate":
        calibrate()
