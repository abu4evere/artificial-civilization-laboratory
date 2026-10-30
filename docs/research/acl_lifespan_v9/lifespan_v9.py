"""How long do ACL people live under nature v9? A descriptive look (not a frozen study; throwaway seeds).
LS2's own world (LP: 80 founders, 80 x 80, code_v9 with v9 settings), read-only: every death event is recorded.

  python lifespan_v9.py run <seed> <years> <out.json>
  python lifespan_v9.py sum <dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"D:\acl\experiments\LS2_knowledge_v9")


def run(seed, years, out):
    import run_ls2
    base = run_ls2.base
    base.setup()
    w = base.make_world(seed, run_ls2.ARMS["lp"])
    deaths = []
    orig = w.emit

    def emit(etype, actor, target, place, **data):
        if etype == "death":
            p = w.people[actor]
            deaths.append([w.tick, p.birth, data.get("cause"), data.get("age"), data.get("generation"), p.sex])
        return orig(etype, actor, target, place, **data)
    w.emit = emit
    births_alive_end = []
    for _ in range(years * 52):
        w.step()
        if not w.living():
            break
    for p in w.living():
        births_alive_end.append([p.birth, round(p.years(w.tick), 1), p.generation])
    Path(out).write_text(json.dumps({"seed": seed, "final_tick": w.tick, "deaths": deaths,
                                     "alive_end": births_alive_end}))
    print(seed, w.tick, len(deaths))


def summarise(d):
    import statistics as st
    from collections import Counter
    rows = [json.loads(f.read_text()) for f in sorted(Path(d).glob("*.json"))]
    W = 52
    print(f"worlds: {len(rows)}; final years: {[r['final_tick'] // W for r in rows]}")
    # cohort: world-born, born years 0-50, followed to the run's end (years >= 150)
    full = [r for r in rows if r["final_tick"] >= 150 * W]
    dead = [x for r in full for x in r["deaths"] if x[4] and x[4] > 0 and x[1] < 50 * W]
    alive = [x for r in full for x in r["alive_end"] if x[2] > 0 and x[0] < 50 * W]
    n = len(dead) + len(alive)
    ages = sorted(x[3] for x in dead)
    print(f"\ncohort born years 0-50 in worlds alive at year 150: {n} people ({len(alive)} still alive, censored)")
    if n:
        print(f"  died before 1: {sum(a < 1 for a in ages) / n:.3f}; before 5: {sum(a < 5 for a in ages) / n:.3f}; "
              f"before 16: {sum(a < 16 for a in ages) / n:.3f}")
        print(f"  mean age at death (dead only; censored few): {st.mean(ages):.1f}; median {st.median(ages):.1f}")
        ad = [a for a in ages if a >= 16]
        print(f"  reached 16 and died: {len(ad)}; their mean age at death {st.mean(ad):.1f}, median {st.median(ad):.1f}; "
              f"oldest {max(ages):.1f}")
        for lo in (16, 30, 45, 60, 70, 80):
            print(f"    share of 16+ deaths at {lo}+: {sum(a >= lo for a in ad) / len(ad):.3f}")
        c = Counter(x[2] for x in dead if x[3] >= 16)
        tot = sum(c.values())
        print("  causes of death, 16+: " + ", ".join(f"{k} {v / tot:.2f}" for k, v in c.most_common()))
        c = Counter(x[2] for x in dead if x[3] < 16)
        tot = sum(c.values()) or 1
        print("  causes of death, under 16: " + ", ".join(f"{k} {v / tot:.2f}" for k, v in c.most_common()))
        # age-specific death rate per person-year (all causes), the cohort above (dead: to death; alive: censored)
        lives = [(x[3], True) for x in dead] + [(x[1], False) for x in alive]
        print("  deaths per person-year by age (all causes) [forager total, SA1 note: 0.018 at 40, 0.039 at 60]:")
        for lo, hi in ((0, 1), (1, 5), (5, 15), (15, 30), (30, 45), (45, 60), (60, 70), (70, 200)):
            py = sum(max(0.0, min(a, hi) - lo) for a, _ in lives)
            dd = sum(1 for a, d in lives if d and lo <= a < hi)
            print(f"    {lo}-{hi}: {dd} deaths / {py:.0f} person-years = {dd / py if py else float('nan'):.4f}")
    # period: all world-born deaths in years 100-150
    per = [x[3] for r in rows for x in r["deaths"] if x[4] and x[4] > 0 and 100 * W <= x[0] < 150 * W]
    if per:
        print(f"\nall world-born deaths in years 100-150: {len(per)}; mean age {st.mean(per):.1f}; median {st.median(per):.1f}; "
              f"oldest {max(per):.1f}")


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    else:
        summarise(sys.argv[2])
