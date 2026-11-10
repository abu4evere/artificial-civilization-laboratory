"""Live one week at a time inside one person's head, in a throwaway world.

This is a probe, not a study and not nature. It never writes to `acl/` and it
never touches a study's output. It exists so that whoever is working on ACL can
sit where one of its people sits: see exactly the state that person's mind reads,
see the options their mind weighed with the weights it gave them, and then pick
one of those options by hand instead of letting the draw pick it.

Nature is unchanged. The mind still runs in full (attention, habits, thoughts,
the weights); the only difference is which of the options the body carries out.
Everything a person cannot know stays hidden: only what `decision.state_snapshot`
and `mindview.mind` already expose to a watcher is shown.

Three steps:

    python tools/mind_views/inhabit.py start --seed 7001 --years 20
    python tools/mind_views/inhabit.py look
    python tools/mind_views/inhabit.py act --option 0

`look` reads the week and never saves. `act` carries out one option and saves the
world, then appends what happened to `journal.md`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from acl import decision, mind, mindview, thought                     # noqa: E402
from acl.config import WEEKS_PER_YEAR                        # noqa: E402
from acl.runner import load_snapshot, new_world, save_snapshot  # noqa: E402

DEFAULT_DIR = ROOT / "research" / "local" / "inhabit"


class Pause(Exception):
    """Raised to stop the week at the moment this person decides (look mode)."""


def _dir(args) -> Path:
    return Path(args.dir) if args.dir else DEFAULT_DIR


def _who_path(d: Path) -> Path:
    return d / "who.json"


def _snap_path(d: Path) -> Path:
    return d / "world.json.gz"


def _menu(world, p, decide=None) -> list:
    """The options this person's mind weighed this week, with their real targets.

    `mind.decide` hands its whole weighed list to `thought.steer` just before it
    ranks and draws. Watching that one call recovers every option, with the real
    target and the weight attention gave it, without changing any rule. (The
    person's own record, `p.considered`, keeps only the best four plus the one
    drawn, so it is not the whole menu.)
    """
    seen = {}
    original = thought.steer

    def watch(person, options):
        out = original(person, options)
        if person.id == p.id:
            seen["options"] = list(out)
        return out

    thought.steer = watch
    try:
        d = (decide or decision.decide)(world, p)
    finally:
        thought.steer = original
    full = seen.get("options", [])
    order = sorted(range(len(full)), key=lambda k: -full[k][0])
    rows = []
    for i, k in enumerate(order):
        u, action, target = full[k][0], full[k][1], full[k][2]
        rows.append({
            "option": i,
            "action": action,
            "aim": mind._aim(target),
            "weight": round(u, 3),
            "the_draw_picked": bool(d.chosen == (action, target)),
            "target": target,
        })
    return d, rows


def _words(world, p, rows) -> dict:
    m = mindview.mind(world, p)
    return {
        "headline": mindview.headline(world, p),
        "thoughts": m.get("thoughts", []),
        "situation": m.get("situation", m.get("where")),
        "choices_in_words": [mindview.choice_words(world, p, r["action"], r["aim"]) for r in rows],
    }


def _body(world, p) -> dict:
    s = decision.state_snapshot(world, p)
    keep = ("tick", "loc", "season", "age_weeks", "stage", "health", "energy", "food", "mood",
            "fear", "anger", "grief", "loneliness", "wellbeing", "sick", "starving", "partner",
            "nearby_people", "recipes", "items", "materials", "memories", "focus")
    return {k: s[k] for k in keep if k in s}


def cmd_start(args) -> None:
    d = _dir(args)
    d.mkdir(parents=True, exist_ok=True)
    world, historian = new_world(args.seed)
    end = args.years * WEEKS_PER_YEAR
    while world.tick < end and world.living():
        world.step()
    living = [p for p in world.living() if p.alive]
    if not living:
        print("nobody is alive in this world; try another seed")
        return
    adults = [p for p in living if p.stage(world.tick) == "adult"]
    pool = adults or living
    pool.sort(key=lambda p: p.age(world.tick))
    me = pool[0]
    _who_path(d).write_text(json.dumps({"seed": args.seed, "pid": me.id,
                                        "started_tick": world.tick}, indent=1), encoding="utf-8")
    save_snapshot(world, historian, _snap_path(d))
    (d / "journal.md").write_text(
        f"# Inside {me.id}\n\nSeed {args.seed}. Taken over at week {world.tick} "
        f"(year {world.tick // WEEKS_PER_YEAR}), age {me.age(world.tick) // WEEKS_PER_YEAR} years, "
        f"stage {me.stage(world.tick)}. Population {len(living)}.\n\n"
        "A probe, not a study: nature is unchanged, only this person's choice is made by hand.\n\n",
        encoding="utf-8")
    print(json.dumps({"pid": me.id, "tick": world.tick, "population": len(living),
                      "age_years": me.age(world.tick) // WEEKS_PER_YEAR}, indent=1))


def _load(d: Path):
    who = json.loads(_who_path(d).read_text(encoding="utf-8"))
    world, historian = load_snapshot(_snap_path(d))
    p = world.people[who["pid"]]
    return who, world, historian, p


def cmd_look(args) -> None:
    d = _dir(args)
    who, world, historian, p = _load(d)
    if not p.alive:
        print(json.dumps({"dead": True, "pid": p.id, "tick": world.tick}, indent=1))
        return
    seen = {}
    real = decision.decide

    def hook(w, q):
        if q.id != who["pid"]:
            return real(w, q)
        dec, rows = _menu(w, q, real)
        seen["body"] = _body(w, q)
        seen["mind"] = _words(w, q, rows)
        seen["options"] = [{k: (repr(v) if k == "target" else v) for k, v in r.items()} for r in rows]
        raise Pause()

    decision.decide = hook
    try:
        world.step()
    except Pause:
        pass
    finally:
        decision.decide = real
    seen["tick"] = world.tick
    seen["pid"] = p.id
    (d / "look.json").write_text(json.dumps(seen, indent=1, default=str), encoding="utf-8")
    print(json.dumps(seen, indent=1, default=str))


def cmd_act(args) -> None:
    d = _dir(args)
    who, world, historian, p = _load(d)
    if not p.alive:
        print("this person is dead; the probe is over")
        return
    picked = {}
    real = decision.decide

    def hook(w, q):
        if q.id != who["pid"]:
            return real(w, q)
        dec, rows = _menu(w, q, real)
        if not rows:
            picked["note"] = "no options; nature's own choice stands"
            return dec
        k = min(args.option, len(rows) - 1)
        dec.chosen = (rows[k]["action"], rows[k]["target"])
        picked["mine"] = {"action": rows[k]["action"], "aim": rows[k]["aim"], "weight": rows[k]["weight"]}
        picked["draw_would"] = next((r["action"] + " " + str(r["aim"]) for r in rows if r["the_draw_picked"]), None)
        picked["words"] = mindview.choice_words(w, q, rows[k]["action"], rows[k]["aim"])
        return dec

    before = _body(world, p)
    decision.decide = hook
    try:
        events = world.step()
    finally:
        decision.decide = real
    after = _body(world, p)
    mine = [e for e in (events or []) if who["pid"] in json.dumps(e, default=str)]
    out = {
        "tick": world.tick,
        "i_chose": picked.get("mine"),
        "in_words": picked.get("words"),
        "the_draw_would_have": picked.get("draw_would"),
        "did": getattr(p, "doing", ""),
        "reward": round(getattr(p, "reward", 0.0), 3),
        "alive": p.alive,
        "change": {k: round(after[k] - before[k], 2) for k in ("health", "energy", "food", "mood")
                   if isinstance(before.get(k), (int, float)) and isinstance(after.get(k), (int, float))},
        "now": after,
        "events_about_me": mine[:12],
    }
    save_snapshot(world, historian, _snap_path(d))
    with (d / "journal.md").open("a", encoding="utf-8") as f:
        f.write(f"## week {world.tick}\n\n```json\n{json.dumps(out, indent=1, default=str)}\n```\n\n")
    print(json.dumps(out, indent=1, default=str))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", default=None, help="where the probe keeps its world (default research/local/inhabit)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start", help="make a throwaway world and take over one person")
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("--years", type=int, default=20)
    sub.add_parser("look", help="see this week through their eyes; saves nothing")
    a = sub.add_parser("act", help="carry out one of the options and let the week run")
    a.add_argument("--option", type=int, required=True)
    args = ap.parse_args(argv)
    {"start": cmd_start, "look": cmd_look, "act": cmd_act}[args.cmd](args)


if __name__ == "__main__":
    main()
