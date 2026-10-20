"""PF1 analysis (questions.md, frozen as `PF1-frozen`): where partner finding stops, by arm, in discovery and holdout.

  python experiments/PF1_partner_pipeline/analyse_pf1.py     -> results.md (outcomes shown only if every check passes)
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_pf1 import ARMS, AGES, DISCOVERY, HOLDOUT, OUT, STEPS  # noqa: E402

NAMES = {"S1_no_match_alive": "S1 no match alive", "S2_none_in_sight": "S2 none in sight",
         "S3_none_in_reach": "S3 none in reach", "S4_disliked": "S4 disliked", "S5_not_tried": "S5 not tried",
         "S6_refused": "S6 refused"}


def load(seeds):
    R, missing = {}, []
    for a in ARMS:
        for s in seeds:
            f = OUT / f"{a}_seed_{s}.json"
            if f.exists():
                R[(a, s)] = json.loads(f.read_text(encoding="utf-8"))
            else:
                missing.append(f.name)
    return R, missing


def pooled(R, arm):
    c, ww = Counter(), 0
    for (a, _s), r in R.items():
        if a == arm:
            c.update(r["steps"])
            ww += r["woman_weeks"]
    return {k: c[k] / ww if ww else None for k in STEPS}, ww


def main():
    out = ["# PF1 — where partner finding stops: results", "", "Frozen as `PF1-frozen`. run_pf1.py, analyse_pf1.py.",
           "", "## Validity", ""]
    zero = (OUT / "zero.txt")
    z_ok = zero.exists() and "All: PASS" in zero.read_text(encoding="utf-8")
    sets = {"discovery": load(DISCOVERY), "holdout": load(HOLDOUT)}
    all_present = all(not m for _R, m in sets.values())
    rs = [r for R, _m in sets.values() for r in R.values()]
    repro = all(r.get("reproduces") is True for r in rs) and bool(rs)
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    one_fp = len(fps) == 1
    out += [f"- Zero check (logging and observer change nothing against `code_mb1b`): **{'yes' if z_ok else 'NO'}**",
            f"- All 96 worlds present: **{'yes' if all_present else 'NO'}**",
            f"- Every replay equals MB1b's saved world (final state hash): **{'yes' if repro else 'NO'}** "
            f"({sum(r.get('reproduces') is True for r in rs)} of {len(rs)})",
            f"- One code fingerprint (`code_pf1`): **{'yes' if one_fp else 'NO'}**", ""]
    valid = z_ok and all_present and repro and one_fp
    if not valid:
        out += ["**Not valid: no outcome is shown.**"]
        for name, (_R, m) in sets.items():
            if m:
                out.append(f"- {name}: missing {len(m)} files")
        (HERE / "results.md").write_text("\n".join(out) + "\n", encoding="utf-8")
        print("\n".join(out))
        return
    out += ["**Valid.**", ""]
    bottleneck = {}
    for name, (R, _m) in sets.items():
        out += [f"## {name.capitalize()} (seeds {min(s for _a, s in R)}–{max(s for _a, s in R)})", "",
                "Share of fertile single woman-weeks ending at each step (pooled), with population beside it.", "",
                "| arm | median alive at the end | single woman-weeks | " + " | ".join(NAMES[k] for k in STEPS)
                + " | bottleneck |", "|" + "---|" * (len(STEPS) + 4)]
        shares = {}
        for arm in ARMS:
            sh, ww = pooled(R, arm)
            shares[arm] = sh
            alive = statistics.median(r["alive_end"] for (a, _s), r in R.items() if a == arm)
            top = max(STEPS, key=lambda k: sh[k] or 0)
            bottleneck[(name, arm)] = top
            out.append(f"| {arm} | {alive:.0f} | {ww} | " + " | ".join(f"{sh[k]:.1%}" for k in STEPS)
                       + f" | {NAMES[top]} |")
        out += ["", "Shift, B16 minus P4 (percentage points; described, no test): "
                + ", ".join(f"{NAMES[k]} {100 * (shares['b16'][k] - shares['p4'][k]):+.1f}" for k in STEPS), ""]
        # described: by age and courting attempts
        out += ["By her age (share of that age group's single woman-weeks at each step):", "",
                "| arm | age | " + " | ".join(NAMES[k] for k in STEPS) + " |", "|" + "---|" * (len(STEPS) + 2)]
        for arm in ARMS:
            for lo, hi in AGES:
                c = Counter()
                for (a, _s), r in R.items():
                    if a == arm:
                        for k, v in r["by_age"].items():
                            band, step = k.split("|")
                            if band == f"{lo}-{hi}":
                                c[step] += v
                n = sum(c.values())
                out.append(f"| {arm} | {lo}–{hi} | " + " | ".join(f"{c[k] / n:.1%}" if n else "–" for k in STEPS)
                           + " |")
        out += ["", "Courting attempts between people not already partners (all, both sexes): "]
        for arm in ARMS:
            at = Counter()
            pw = sm = 0
            for (a, _s), r in R.items():
                if a == arm:
                    at.update(r["attempts"])
                    pw += r["person_weeks"]
                    sm += r["single_men_weeks"]
            tot = sum(at.values())
            out.append(f"- {arm}: {tot} attempts; paired {at['paired']}, refused {at['refused']}, one already taken "
                       f"{at['taken']}; single adult man-weeks per person-week {sm / pw:.3f}")
        out.append("")
    out += ["## The frozen reading", "", "| arm | bottleneck, discovery | bottleneck, holdout | reading |",
            "|---|---|---|---|"]
    for arm in ARMS:
        d, h = bottleneck[("discovery", arm)], bottleneck[("holdout", arm)]
        out.append(f"| {arm} | {NAMES[d]} | {NAMES[h]} | {'**' + NAMES[d] + '** (stands)' if d == h else 'no reading (sets disagree)'} |")
    (HERE / "results.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
