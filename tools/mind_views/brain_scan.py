"""Brain scan: a page showing how the people of one control world decide, week by week, read-only.

For every teen and adult, each week: the situation neuron lit (food held x company x season, 32 in all), the 32 x 19
table of learned habits (p.q, Q-learning), body and feelings, temperament, and the options weighed with their scores and
their learned share. Runs the control code (experiments/E13R_replication/code_e13r) and writes one self-contained HTML
page; nothing is written to the world or the code.

  python tools/mind_views/brain_scan.py                 # seed 501, year 11
  python tools/mind_views/brain_scan.py 1112 104        # any seed and year
Output: tools/mind_views/out/brain_scan_seed<SEED>_year<YEAR>.html (not committed; rebuild it any time)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
CODE = HERE.parents[1] / "experiments" / "E13R_replication" / "code_e13r"
sys.path.insert(0, str(CODE))
import acl  # noqa: E402
assert Path(acl.__file__).resolve().parent == (CODE / "acl").resolve()
from acl.config import Config  # noqa: E402
from acl.mind import hunger_of  # noqa: E402
from acl.person import A, ACTIONS, N_ACTIONS, N_CONTEXTS  # noqa: E402
from acl.world import World  # noqa: E402

WPY = 52


def extract(seed: int, start_year: int) -> dict:
    w = World(Config(seed=seed, anticipation_weight=1.0))
    for _ in range(start_year * WPY):
        w.step()
    c = w.cfg
    names, frames = {}, []
    for _ in range(WPY):
        if not w.living():
            break
        w.step()
        tick = w.tick
        people = []
        for p in w.living():
            if p.stage(tick) not in ("teen", "adult", "elder"):
                continue
            names[p.id] = p.name
            hunger = hunger_of(w, p, sum(d.need(c, tick) for d in w.dependents(p.id)))
            people.append({
                "id": p.id, "sex": p.sex, "age": round(p.years(tick), 1), "partner": p.partner,
                "ctx": p.last_ctx, "action": p.last_action,
                "q": [round(v * 100) for v in p.q],
                "body": {"hunger": round(hunger, 2), "thirst": round(p.thirst, 2),
                         "fatigue": round(1 - p.energy / 100, 2), "health": round(p.health / 100, 2),
                         "mood": round(p.mood, 2), "fear": round(p.fear, 2), "anger": round(p.anger, 2),
                         "grief": round(p.grief, 2), "loneliness": round(p.loneliness, 2)},
                "genes": {g: round(v, 2) for g, v in p.genes.items()},
                # options weighed: action, score, chosen, learned share (learned_weight x q[context, action])
                "weighed": [[a, round(sc, 2), int(ch), round(c.learned_weight * p.q[p.last_ctx * N_ACTIONS + A[a]], 2)]
                            for a, _aim, sc, ch in p.considered],
            })
        frames.append({"week": tick, "season": w.season, "people": people})
    return {"seed": seed, "year": start_year, "actions": list(ACTIONS), "n_contexts": N_CONTEXTS,
            "learned_weight": c.learned_weight, "learning_rate": c.learning_rate, "discount": c.discount,
            "names": names, "frames": frames}


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 501
    year = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    data = extract(seed, year)
    if not data["frames"] or not data["frames"][0]["people"]:
        sys.exit(f"No grown people alive in seed {seed} at year {year}.")
    page = (HERE / "brain_template.html").read_text(encoding="utf-8")
    blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    out = HERE / "out" / f"brain_scan_seed{seed}_year{year + 1}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page.replace("__DATA__", blob), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(data['frames'])} weeks)")


if __name__ == "__main__":
    main()
