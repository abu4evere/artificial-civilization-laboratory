"""BD3 analysis in the frozen order (questions.md, `BD3-frozen`). Written before any data.

  python experiments/BD3_bodies_breakdown/analyse_bd3.py            # writes results.md
  python experiments/BD3_bodies_breakdown/analyse_bd3.py --smoke    # throwaway smoke outputs; writes nothing

Validity: zero checks pass; all 9,216 worlds present; one fingerprint (`code_bd3`).
Manipulation (hard stop): in each arm with a part off, that part's events are 0 and its opportunity is above 0; in F
every part's events are above 0.
Primary, time-averaged population (the mean of the 12 ten-yearly counts, 0 after dying out). All arms are bootstrapped
together by seed (10,000 resamples). (1) Gate: F / N - 1, 95% interval; if its lower bound is not above 0, the rest is
described only. (2) Each part x: F / (F-x) - 1 with a Holm-adjusted interval across the five parts (parts ordered by
their two-sided bootstrap p; the k-th uses level 1 - 0.05 / (5 - k + 1) while every earlier part was wholly away from 0,
and 1 - 0.05 / 5 from the first that was not). Readings: wholly above +0.02 "carries a meaningful part of the gain";
above 0 but reaching below +0.02 "carries part of the gain; size uncertain"; wholly below 0 "works against the gain";
wholly inside -0.02 to +0.02 "small, if any"; else "inconclusive". (3) Described: shares (F - F-x) / (F - N); the
eat x carried interaction; F-all against N.
Survival (secondary): each F-x against F, paired risk difference, discordant pairs, exact McNemar.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_bd3 import ARMS, BINS, DELAYS, OUT, PARTS, SEEDS, SMOKE_SEEDS  # noqa: E402
from scipy.stats import binomtest  # noqa: E402

B = 10000
MARGIN = 0.02
EVENT = {"eat": "meat_meals", "carried": "left_with_body", "foul": "foul_weeks", "seen": "seen", "tools": "tools"}
OPP = {"eat": "opp_meat", "carried": "opp_carried", "foul": "foul_opp", "seen": "seen_opp", "tools": "opp_tools"}
OFF = {"f_eat": ("eat",), "f_carried": ("carried",), "f_foul": ("foul",), "f_seen": ("seen",), "f_tools": ("tools",),
       "f_eat_carried": ("eat", "carried"), "f_all": PARTS}


def died(r):
    return int(r["final_tick"] < 120 * 52)


def tavg(r):
    return sum(r["pops"][i] if len(r["pops"]) > i else 0 for i in range(12)) / 12


def q(xs, level):
    xs = sorted(xs)
    a = (1 - level) / 2
    return xs[int(a * (len(xs) - 1))], xs[int((1 - a) * (len(xs) - 1))]


def read_part(lo, hi):
    if lo > MARGIN:
        return "carries a meaningful part of the gain"
    if lo > 0:
        return "carries part of the gain; size uncertain"
    if hi < 0:
        return "works against the gain"
    if -MARGIN < lo and hi < MARGIN:
        return "small, if any"
    return "inconclusive"


def main(smoke=False):
    seeds = list(SMOKE_SEEDS if smoke else SEEDS)
    out = HERE / "output_smoke" if smoke else OUT
    rows, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = out / f"{a}_seed_{s}.json"
            if f.exists():
                rows.setdefault(a, {})[s] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f"{a} {s}")
    L = [f"# BD3 — what in a body keeps more people alive: results{' (SMOKE TEST, throwaway seeds)' if smoke else ''}",
         "", "Frozen as `BD3-frozen`. run_bd3.py, analyse_bd3.py (written before data).", "", "## Validity", ""]
    z = OUT / "zero.txt"
    zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
    L.append(f"- Zero checks: **{'yes' if zt else 'NO'}**")
    ok = zt
    L.append(f"- All worlds present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing[:8])}**")
    ok &= not missing
    if not missing:
        allr = [r for a in rows.values() for r in a.values()]
        fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
        L.append(f"- One fingerprint (`code_bd3`): **{'yes' if len(fps) == 1 else 'NO'}**")
        ok &= len(fps) == 1
        L += ["", "Manipulation check (events of the part / opportunities for it, summed over seeds):", "",
              "| arm | " + " | ".join(PARTS) + " | passes |", "|---|" + "---|" * (len(PARTS) + 1)]
        man = True
        for a in ["f"] + list(OFF):
            cells, good = [], True
            for x in PARTS:
                ev = sum(rows[a][s][EVENT[x]] for s in seeds)
                op = sum(rows[a][s][OPP[x]] for s in seeds)
                cells.append(f"{ev:,.0f} / {op:,.0f}")
                if a == "f":
                    good &= ev > 0
                elif x in OFF[a]:
                    good &= ev == 0 and op > 0
            man &= good
            L.append(f"| {a} | " + " | ".join(cells) + f" | {'yes' if good else 'NO'} |")
        L.append(f"\n- Manipulation check: **{'passes' if man else 'FAILS'}**")
        ok &= man
    L += ["", f"**{'Valid.' if ok else 'NOT VALID: no outcome is shown.'}**"]
    if ok:
        T = {a: [tavg(rows[a][s]) for s in seeds] for a in ARMS}
        n = len(seeds)
        mean = {a: statistics.fmean(T[a]) for a in ARMS}
        rng = random.Random(2026)
        boots = []
        for _ in range(B):
            idx = [rng.randrange(n) for _ in range(n)]
            boots.append({a: sum(T[a][i] for i in idx) / n for a in ARMS})

        def rat(a, b, m):
            return m[a] / m[b] - 1 if m[b] else 0.0
        g0 = rat("f", "n", mean)
        glo, ghi = q([rat("f", "n", m) for m in boots], 0.95)
        gate = glo > 0
        L += ["", "## Primary: time-averaged population", "",
              "Means: " + ", ".join(f"{a} **{mean[a]:.2f}**" for a in ARMS) + ".", "",
              f"**(1) Gate, the gain on fresh seeds:** F / N - 1 = {g0:+.3f} [{glo:+.3f}, {ghi:+.3f}]: "
              f"**{'the gain replicates' if gate else 'NOT replicated: everything below is described only'}**", ""]
        parts = []
        for x in PARTS:
            a = f"f_{x}"
            bs = [rat("f", a, m) for m in boots]
            p = min(1.0, 2 * min(sum(v <= 0 for v in bs), sum(v >= 0 for v in bs)) / B)
            parts.append([x, rat("f", a, mean), bs, p])
        parts.sort(key=lambda t: t[3])
        still = True
        L += ["**(2) Each part (F / (F-x) - 1, Holm-adjusted intervals):**", "",
              "| part | F / (F-x) - 1 | interval | level | bootstrap p | reading |", "|---|---|---|---|---|---|"]
        res = {}
        for k, (x, r0, bs, p) in enumerate(parts):
            level = 1 - 0.05 / (len(PARTS) - k) if still else 1 - 0.05 / len(PARTS)
            lo, hi = q(bs, level)
            still &= lo > 0 or hi < 0
            rd = read_part(lo, hi) if gate else "described only (gate not passed)"
            res[x] = (r0, lo, hi, rd)
            L.append(f"| {x} | {r0:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {level:.3f} | {p:.4f} | **{rd}** |")
        L += ["", "**(3) Described:**", "", "| quantity | estimate | 95% interval |", "|---|---|---|"]
        for x in PARTS:
            a = f"f_{x}"

            def share(m, a=a):
                d = m["f"] - m["n"]
                return (m["f"] - m[a]) / d if d else float("nan")
            lo, hi = q([share(m) for m in boots], 0.95)
            L.append(f"| share of the gain: {x} | {share(mean):+.2f} | [{lo:+.2f}, {hi:+.2f}] |")

        def inter(m):
            return (m["f"] - m["f_eat"] - m["f_carried"] + m["f_eat_carried"]) / m["f"] if m["f"] else 0.0
        lo, hi = q([inter(m) for m in boots], 0.95)
        L.append(f"| eat x carried interaction, as a share of F | {inter(mean):+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
        lo, hi = q([rat("f_all", "n", m) for m in boots], 0.95)
        L.append(f"| F-all against N (what remains) | {rat('f_all', 'n', mean):+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
        L += ["", "## Survival (secondary)", "",
              "| arm | died out | against F: saved / lost (discordant) | risk difference (arm - F) | McNemar p |",
              "|---|---|---|---|---|"]
        df = {s: died(rows["f"][s]) for s in seeds}
        L.append(f"| f | {sum(df.values())} | | | |")
        for a in ARMS:
            if a == "f":
                continue
            da = {s: died(rows[a][s]) for s in seeds}
            worse = sum(1 for s in seeds if da[s] and not df[s])
            better = sum(1 for s in seeds if df[s] and not da[s])
            p = binomtest(worse, worse + better).pvalue if worse + better else 1.0
            L.append(f"| {a} | {sum(da.values())} | {better} / {worse} | {(sum(da.values()) - sum(df.values())) / n:+.3f} "
                     f"| {p:.3g} |")
        L += ["", "## Described (population first)", "",
              "| arm | median pop. yr 60 / 120 | bodies | meat meals | carried meals | rotten meals | foul person-weeks "
              "| seen | tools to kin | kin visits | food to plants |", "|---|" + "---|" * 10]
        for a in ARMS:
            rs = [rows[a][s] for s in seeds]
            p60 = statistics.median(r["pops"][5] if len(r["pops"]) > 5 else 0 for r in rs)
            p120 = statistics.median(r["pops"][11] if len(r["pops"]) > 11 else 0 for r in rs)
            L.append(f"| {a} | {p60:.0f} / {p120:.0f} | {sum(r['bodies'] for r in rs):,} | "
                     f"{sum(r['meat_meals'] for r in rs):,} | {sum(r['carried_meals'] for r in rs):,} | "
                     f"{sum(r['ate_rotten'] for r in rs):,} | {sum(r['foul_weeks'] for r in rs):,} | "
                     f"{sum(r['seen'] for r in rs):,} | {sum(r['tools'] for r in rs):,} | "
                     f"{sum(r['kinvisit'] for r in rs):,} | {sum(r['toplants'] for r in rs):,.0f} |")
        L += ["", "**Avoidance (GPT's hypothesis): F (with the penalty) against F-foul (same moments, no penalty).**", "",
              "| arm | exposures | by weeks since death " + " / ".join(f"{a}-{b}" for a, b in BINS)
              + " | back within one tile at " + " / ".join(f"{d}" for d in DELAYS)
              + " weeks (of those alive) | went there when within reach, by weeks since exposure 1-4 / 5-14 / 15-52 / 53-104 |",
              "|---|---|---|---|---|"]
        for a in ("f", "f_foul"):
            av = [rows[a][s]["avoid"] for s in seeds]
            ex = sum(v["exposures"] for v in av)
            eb = [sum(v["exp_bins"][k] for v in av) for k in range(4)]
            back = [sum(v["back"][k] for v in av) / max(1, sum(v["alive_at"][k] for v in av)) for k in range(4)]
            went = [sum(v["went"][k] for v in av) / max(1, sum(v["opp"][k] for v in av)) for k in range(4)]
            L.append(f"| {a} | {ex:,} | {' / '.join(f'{x:,}' for x in eb)} | {' / '.join(f'{x:.3f}' for x in back)} | "
                     f"{' / '.join(f'{x:.3f}' for x in went)} |")
        L += ["", "| arm | deaths | starvation | illness | old age | thirst | killed |", "|---|---|---|---|---|---|---|"]
        for a in ARMS:
            ds = [d for s in seeds for d in rows[a][s]["deaths"]]
            cnt = lambda k: sum(1 for d in ds if d[1] == k)  # noqa: E731
            L.append(f"| {a} | {len(ds):,} | {cnt('starvation'):,} | {cnt('illness'):,} | {cnt('old age'):,} | "
                     f"{cnt('thirst'):,} | {cnt('killed'):,} |")
    text = "\n".join(L) + "\n"
    if not smoke:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)


if __name__ == "__main__":
    main(smoke="--smoke" in sys.argv)
