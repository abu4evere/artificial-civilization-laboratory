"""PLAY1 — the assistant plays one person inside a throwaway copy of nature v15. NOT a study and NOT nature: the creator's
one-off exception (7 November 2026: "i would prefer play mode its just for testing once or twice we will keep our old
rules still") to CLAUDE.md's "No LLMs inside ACL's people". Nothing here touches acl/, code_v15, studies or data.

The player sees only what the person can perceive, and chooses only among the options the world itself offers them
that week (the same list `mind.decide` builds and weighs). Everyone else lives by their own minds. One choice = one week.

  python experiments/PLAY1_inside_acl/play.py new <seed> <years>    # grow a world, then take over a young adult
  python experiments/PLAY1_inside_acl/play.py look                  # what I perceive, and this week's options
  python experiments/PLAY1_inside_acl/play.py do <n>                # choose option n; live the week
  python experiments/PLAY1_inside_acl/play.py wait <weeks>          # let my own mind choose for some weeks
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
CODE = HERE.parent / "NV15_nature_v15" / "code_v15"
sys.path.insert(0, str(CODE))
from acl import decision, fauna, mind, thought, weather  # noqa: E402
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

STATE = HERE / "state"
V11 = {"loved_location": "last_seen", "corner_block": 1, "ashore_if_float_breaks": 1, "knowledge_copy": 1,
       "parts_first": 1, "bodies_stay": 1, "digging": 1, "body_rot": 1, "twins": 1, "sex_ratio_birth": 1,
       "ground_items": 1, "curiosity_pull": 1}
WPY = 52


class Stop(Exception):
    pass


def save(w, me, log):
    STATE.mkdir(exist_ok=True)
    (STATE / "world.json").write_text(json.dumps(w.to_dict(), separators=(",", ":")), encoding="utf-8")
    (STATE / "me.json").write_text(json.dumps({"me": me, "log": log}, indent=1), encoding="utf-8")


def load():
    w = World.from_dict(json.loads((STATE / "world.json").read_text(encoding="utf-8")))
    m = json.loads((STATE / "me.json").read_text(encoding="utf-8"))
    return w, m["me"], m["log"]


def name(w, pid):
    p = w.people.get(pid)
    return f"{p.name} ({pid})" if p else str(pid)


def say_target(w, me, tgt):
    p = w.people[me]
    if tgt is None:
        return ""
    if isinstance(tgt, str):
        return name(w, tgt) if tgt in w.people else tgt
    if isinstance(tgt, (tuple, list)) and len(tgt) == 2 and all(isinstance(v, int) for v in tgt):
        dx, dy = tgt[0] - p.loc[0], tgt[1] - p.loc[1]
        return f"tile {tuple(tgt)} ({'here' if (dx, dy) == (0, 0) else f'{dx:+d},{dy:+d} from me'})"
    if isinstance(tgt, (tuple, list)):
        return " / ".join(say_target(w, me, t) for t in tgt)
    return str(tgt)


def options_at_my_turn(w, me):
    """Step a copy of the world until my turn; return the full list of options the world offers me, already weighed
    by my own mind (score, action, target), in the copy's state at that moment."""
    seen = {}
    steer0, decide0 = thought.steer, decision.decide

    def steer(p, options):
        out = steer0(p, options)
        if p.id == me:
            seen["options"] = [(o[0], o[1], o[2]) for o in out]
        return out

    def decide(world, p):
        d = decide0(world, p)
        if p.id == me:
            seen["world"] = world
            raise Stop
        return d
    thought.steer, decision.decide = steer, decide
    try:
        w.step()
    except Stop:
        pass
    finally:
        thought.steer, decision.decide = steer0, decide0
    return seen.get("options", []), seen.get("world", w)


def perceive(w, me):
    p = w.people[me]
    c = w.cfg
    t = w.tile(p.loc)
    yrs = (w.tick - p.birth) / WPY
    lines = [f"Week {w.tick} (year {w.tick // WPY}, season {['spring', 'summer', 'autumn', 'winter'][(w.tick % WPY) // 13]}). "
             f"I am {p.name}, {p.sex}, {yrs:.1f} years old. Health {p.health:.0f}/100. "
             f"Food {p.food:.1f} + seeds {p.seeds:.1f} (I need {p.need(c, w.tick):.1f} a week). "
             f"Hunger {mind.hunger_of(w, p):.2f}; thirst {p.thirst:.2f}; cold here {weather.coldness(w, p.loc):.2f}.",
             f"Where: tile {p.loc}, {t.biome}; plants {t.plants:.1f}, crop {t.crop:.1f}, wood {t.wood:.1f}, stone "
             f"{t.stone:.1f}, flint {t.flint:.1f}, fiber {t.fiber:.1f}; water nearby {bool(t.water)}; fire {t.fire:.1f}. "
             f"Prey here: {fauna.prey_here(w, p.loc)}."]
    if p.partner:
        lines.append(f"My partner: {name(w, p.partner)}" + ("" if w.people[p.partner].alive else " (dead)"))
    kids = [k for k in p.children if w.people[k].alive]
    if kids:
        lines.append("My children: " + ", ".join(f"{name(w, k)} {(w.tick - w.people[k].birth) / WPY:.0f}y" for k in kids))
    near = [q for q in w.living() if q.id != me and abs(q.loc[0] - p.loc[0]) <= 2 and abs(q.loc[1] - p.loc[1]) <= 2]
    if near:
        out = []
        for q in near[:12]:
            r = p.rel.get(q.id)
            rel = f"trust {r.trust:+.2f}, affection {r.affection:+.2f}" if r else "a stranger"
            out.append(f"{name(w, q.id)} {q.sex} {(w.tick - q.birth) / WPY:.0f}y at {q.loc} ({rel})")
        lines.append(f"People within 2 tiles ({len(near)}): " + "; ".join(out))
    else:
        lines.append("No one within 2 tiles.")
    lines.append("I carry: " + (", ".join(f"{it['sig']} ({it.get('uses', '?')} uses)" for it in p.items) or "no made things")
                 + "; materials: " + (", ".join(f"{k} {v:.1f}" for k, v in p.mats.items() if v > 0.05) or "none"))
    lines.append(f"I know how to make ({len(p.recipes)}): " + ", ".join(sorted(p.recipes)[:12]))
    return "\n".join(lines)


def cmd_new(seed, years):
    w = World(Config(seed=seed, anticipation_weight=1.0, **V11))
    for _ in range(years * WPY):
        w.step()
        if not w.living():
            sys.exit("the world died out; try another seed")
    young = sorted((q for q in w.living() if 16 * WPY <= w.tick - q.birth <= 30 * WPY), key=lambda q: q.id)
    if not young:
        sys.exit("no young adult alive; try another seed or year")
    me = young[0].id
    save(w, me, [])
    print(f"World seed {seed}, grown {years} years: {len(w.living())} people alive. I am now {name(w, me)}.")
    print(perceive(w, me))


def cmd_look():
    w, me, log = load()
    if not w.people[me].alive:
        sys.exit("I am dead.")
    opts, at = options_at_my_turn(World.from_dict(w.to_dict()), me)
    print(perceive(at, me))
    print("\nThis week the world offers me (my own mind's weight in brackets):")
    for i, (s, a, tg) in enumerate(sorted(opts, key=lambda o: -o[0])):
        print(f"  {i:2d}. {a:8s} {say_target(at, me, tg)}  [{s:.2f}]")


def cmd_do(n):
    w, me, log = load()
    pick = {}
    steer0, decide0 = thought.steer, decision.decide

    def steer(p, options):
        out = steer0(p, options)
        if p.id == me:
            ranked = sorted([(o[0], o[1], o[2]) for o in out], key=lambda o: -o[0])
            pick["choice"] = (ranked[n][1], ranked[n][2])
        return out

    def decide(world, p):
        d = decide0(world, p)
        if p.id == me and "choice" in pick:
            d.chosen = pick["choice"]
        return d
    thought.steer, decision.decide = steer, decide
    try:
        events = w.step()
    finally:
        thought.steer, decision.decide = steer0, decide0
    mine = [e for e in events if me in (e.get("a"), e.get("b")) or me in (e.get("party") or [])]
    log.append({"tick": w.tick - 1, "choice": [pick["choice"][0], str(pick["choice"][1])] if pick else None,
                "events": mine})
    save(w, me, log)
    print(f"I chose: {pick['choice'][0]} {say_target(w, me, pick['choice'][1])}" if pick else "No choice was asked of me.")
    for e in mine:
        print("  ", {k: v for k, v in e.items() if k not in ("id",)})
    if not w.people[me].alive:
        print("I died this week.")


def cmd_wait(weeks):
    w, me, log = load()
    for _ in range(weeks):
        events = w.step()
        mine = [e for e in events if me in (e.get("a"), e.get("b")) or me in (e.get("party") or [])]
        log.append({"tick": w.tick - 1, "choice": "own mind", "events": mine})
        for e in mine:
            print(w.tick - 1, {k: v for k, v in e.items() if k not in ("id",)})
        if not w.people[me].alive:
            print("I died.")
            break
    save(w, me, log)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "new":
        cmd_new(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "look":
        cmd_look()
    elif cmd == "do":
        cmd_do(int(sys.argv[2]))
    elif cmd == "wait":
        cmd_wait(int(sys.argv[2]))
