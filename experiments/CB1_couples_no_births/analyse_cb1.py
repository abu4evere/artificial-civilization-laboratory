"""CB1 analysis (questions.md, frozen as `CB1-frozen`). Read-only: CT1's saved C and K1 worlds. Exploratory.

  python experiments/CB1_couples_no_births/analyse_cb1.py   -> results.md
"""
import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "CT1_courting_nature" / "output"
SEEDS = range(8201, 8457)
PARTNERED = ("partner_dead", "apart", "low_health", "starving", "partner_child", "nursing", "eligible")
WPY = 52


def boot(d):
    rng = random.Random(2026)
    m = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(10000))
    return statistics.fmean(d), m[249], m[9749]


def blocks(r):
    c = {}
    for y in r["years"].values():
        for k, v in y.items():
            if k.startswith("r_"):
                c[k[2:]] = c.get(k[2:], 0) + v
    return c


def main():
    rows = {a: {} for a in ("c", "k1")}
    missing = []
    for a in rows:
        for s in SEEDS:
            f = OUT / f"{a}_seed_{s}.json"
            if f.exists():
                r = json.loads(f.read_text(encoding="utf-8"))
                rows[a][s] = (blocks(r), len(r["births"]))
            else:
                missing.append(f"{a} {s}")
    L = ["# CB1 — why did the extra couples not bring more children? Results (exploratory)", "",
         "Frozen as `CB1-frozen`. analyse_cb1.py. Read-only: CT1's saved C and K1 worlds (seeds 8201–8456). CT1 was not "
         "valid as committed, so this only describes.", ""]
    if missing:
        L.append(f"**Not valid: worlds missing ({', '.join(missing[:6])}); no outcome is shown.**")
    else:
        L.append("All 512 worlds present.")
        pw = {a: {s: sum(rows[a][s][0].get(b, 0) for b in PARTNERED) for s in SEEDS} for a in rows}
        ok = [s for s in SEEDS if pw["c"][s] >= WPY and pw["k1"][s] >= WPY]
        L += ["", f"## Q1–Q2: where partnered woman-weeks go (worlds with ≥ 52 partnered weeks in both arms: "
                  f"{len(ok)} of 256)", "",
              "| block | C pooled share (weeks) | K1 pooled share (weeks) | paired K1 − C, mean | 95% interval |",
              "|---|---|---|---|---|"]
        apart = None
        for b in PARTNERED:
            tot = {a: sum(pw[a][s] for s in ok) for a in rows}
            n = {a: sum(rows[a][s][0].get(b, 0) for s in ok) for a in rows}
            d = [rows["k1"][s][0].get(b, 0) / pw["k1"][s] - rows["c"][s][0].get(b, 0) / pw["c"][s] for s in ok]
            e, lo, hi = boot(d)
            if b == "apart":
                apart = (e, lo, hi)
            L.append(f"| {b} | {n['c'] / tot['c']:.1%} ({n['c']:,}) | {n['k1'] / tot['k1']:.1%} ({n['k1']:,}) | "
                     f"{e:+.4f} | [{lo:+.4f}, {hi:+.4f}] |")
        for a in rows:
            preg = sum(rows[a][s][0].get("pregnant", 0) for s in SEEDS)
            nop = sum(rows[a][s][0].get("no_partner", 0) for s in SEEDS)
            L.append(f"\n{a.upper()}: pregnant woman-weeks {preg:,}; woman-weeks with no partner {nop:,}; "
                     f"partnered woman-weeks {sum(pw[a].values()):,}.")
        ok3 = [s for s in SEEDS if rows["c"][s][0].get("eligible", 0) >= WPY and rows["k1"][s][0].get("eligible", 0) >= WPY]
        d = [rows["k1"][s][1] / rows["k1"][s][0]["eligible"] - rows["c"][s][1] / rows["c"][s][0]["eligible"] for s in ok3]
        e, lo, hi = boot(d)
        L += ["", f"## Q3: births per eligible woman-week (worlds with ≥ 52 eligible weeks in both arms: {len(ok3)})", ""]
        for a in rows:
            bth = sum(rows[a][s][1] for s in SEEDS)
            el = sum(rows[a][s][0].get("eligible", 0) for s in SEEDS)
            L.append(f"- {a.upper()} pooled: {bth:,} births / {el:,} eligible woman-weeks = {bth / el:.4f} a week "
                     f"(the code's conception chance is 0.04; births lag conception by pregnancy).")
        L.append(f"- Paired K1 − C: {e:+.5f} [{lo:+.5f}, {hi:+.5f}].")
        right = apart[0] > 0 and apart[1] > 0
        L += ["", "## The prior (frozen)", "",
              f"\"K1's extra couples spend more of their weeks apart\": the `apart` share K1 − C = {apart[0]:+.4f} "
              f"[{apart[1]:+.4f}, {apart[2]:+.4f}]: **{'right' if right else 'not shown'}**."]
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main()
