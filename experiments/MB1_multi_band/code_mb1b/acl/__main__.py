"""Command line.

    python -m acl run --seed 42 --years 100
    python -m acl resume runs/seed42/final.json.gz --years 50
    python -m acl check --seeds 1-10 --years 100
    python -m acl replay --seed 42 --years 30
    python -m acl watch --seed 42
    python -m acl live            # their world, living on its own clock
    python -m acl stop            # stop it (it saves first)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .checks import CRITERIA, emergent_patterns, replay_check, score
from .runner import load_snapshot, new_world, simulate


def _progress(world, historian):
    if world.year % 10 == 0:
        r = historian.years[-1] if historian.years else {}
        print(f"  year {world.year:4d}  population {r.get('population', 0):4d}  "
              f"generation {r.get('generation', 0):2d}  happiness {r.get('mood', 0):.2f}", flush=True)


def _seeds(spec: str) -> list[int]:
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def _summary(result: dict, out: Path | None) -> None:
    m = result["metrics"]
    print(f"\nseed {result['seed']}: {m['years']} years in {result['seconds']}s")
    print(f"  population {m['population_end']} (peak {m['population_peak']}), "
          f"{m['max_generation']} generations, {m['births']} births")
    print(f"  deaths: {', '.join(f'{k} {v}' for k, v in m['deaths_by_cause'].items())}")
    print(f"  emerged: {', '.join(emergent_patterns(m)) or 'nothing yet'}")
    print(f"  state hash {result['state_hash'][:16]}")
    if out:
        print(f"  report: {out / 'report.html'}")
        print(f"  chronicle: {out / 'chronicle.md'}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="acl", description="Artificial Civilization Laboratory")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="start a new world")
    r.add_argument("--seed", type=int, default=42)
    r.add_argument("--years", type=int, default=100)
    r.add_argument("--out", type=Path, default=None, help="default: runs/seed<SEED>")
    r.add_argument("--snapshots", type=int, default=25, help="save a snapshot every N years (0 = off)")
    r.add_argument("--no-events", action="store_true", help="skip the full event log")

    s = sub.add_parser("resume", help="continue a world from a snapshot")
    s.add_argument("snapshot", type=Path)
    s.add_argument("--years", type=int, default=50)
    s.add_argument("--out", type=Path, default=None)
    s.add_argument("--snapshots", type=int, default=25)

    c = sub.add_parser("check", help="score the success criteria across many seeds")
    c.add_argument("--seeds", default="1-10")
    c.add_argument("--years", type=int, default=100)
    c.add_argument("--out", type=Path, default=Path("runs/check"))

    p = sub.add_parser("replay", help="prove the same seed gives the same history")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--years", type=int, default=30)

    lv = sub.add_parser("live", help="their world, living on its own clock and saved as it goes")
    lv.add_argument("--home", type=Path, default=Path(os.environ.get("ACL_HOME", "world")),
                    help="where the world is kept (default: ./world)")
    lv.add_argument("--new", action="store_true", help="begin a new world; the old one is set aside, not deleted")
    lv.add_argument("--seed", type=int, default=None, help="seed for a new world (default: random)")
    lv.add_argument("--hours-per-day", type=float, default=0.25, help="real hours per day of theirs (default 0.25 = 15 minutes)")
    lv.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    lv.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8765")))
    lv.add_argument("--open", action="store_true", help="open the page in your browser")
    lv.add_argument("--public", action="store_true", help="online mode: no stop button reachable from outside")

    st = sub.add_parser("stop", help="stop their world (it saves first)")
    st.add_argument("--port", type=int, default=8765)

    v = sub.add_parser("watch", help="a throwaway world at any speed, to try things out")
    v.add_argument("--seed", type=int, default=42)
    v.add_argument("--port", type=int, default=8765)
    v.add_argument("--speed", type=float, default=4.0, help="weeks per second")
    v.add_argument("--out", type=Path, default=None, help="save a report of what you watched here on exit")
    v.add_argument("--no-browser", action="store_true")

    args = ap.parse_args(argv)

    if args.cmd == "run":
        out = args.out or Path("runs") / f"seed{args.seed}"
        world, historian = new_world(args.seed)
        print(f"seed {args.seed}, {args.years} years -> {out}")
        result = simulate(world, historian, args.years, out, args.snapshots,
                          log_events=not args.no_events, progress=_progress)
        _summary(result, out)
        return 0

    if args.cmd == "resume":
        world, historian = load_snapshot(args.snapshot)
        out = args.out or args.snapshot.parent / f"resumed_from_y{world.year}"
        print(f"resuming seed {world.cfg.seed} at year {world.year} for {args.years} years -> {out}")
        result = simulate(world, historian, args.years, out, args.snapshots, progress=_progress)
        _summary(result, out)
        return 0

    if args.cmd == "check":
        seeds = _seeds(args.seeds)
        rows = []
        for seed in seeds:
            world, historian = new_world(seed)
            result = simulate(world, historian, args.years, args.out / f"seed{seed}", snapshot_every=0,
                              log_events=False)
            passed = score(result["metrics"], world.cfg.founders)
            rows.append({"seed": seed, "passed": passed, "metrics": result["metrics"]})
            marks = " ".join(("ok " if v else "NO ") + k for k, v in passed.items())
            print(f"seed {seed:3d}: {marks}  ({result['seconds']}s)", flush=True)
        print()
        for key, desc, _ in CRITERIA:
            n = sum(1 for row in rows if row["passed"][key])
            print(f"  {n:3d}/{len(rows)}  {desc}")
        all_pass = sum(1 for row in rows if all(row["passed"].values()))
        print(f"\n  {all_pass}/{len(rows)} seeds pass every criterion")
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "check.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
        return 0

    if args.cmd == "live":
        from .viewer import live
        if sys.stdout is None:
            # Started without a window (pythonw): keep a log next to the world instead.
            args.home.mkdir(parents=True, exist_ok=True)
            sys.stdout = sys.stderr = open(args.home / "live.log", "a", encoding="utf-8", buffering=1)
        live(args.home, args.seed, args.hours_per_day, args.new, args.host, args.port, args.open, args.public)
        return 0

    if args.cmd == "stop":
        import urllib.request
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{args.port}/shutdown", timeout=5).read()
            print("Their world is saving and stopping.")
        except OSError:
            print("Their world does not seem to be running.")
        return 0

    if args.cmd == "watch":
        from .viewer import watch
        watch(args.seed, args.port, args.speed, args.out, open_browser=not args.no_browser)
        return 0

    if args.cmd == "replay":
        res = replay_check(args.seed, args.years, Path("runs") / "replay")
        print(json.dumps(res, indent=2))
        return 0 if res["identical"] else 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
