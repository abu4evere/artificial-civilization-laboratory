"""G1 analysis in the frozen order (questions.md, `G1-questions`).

  python experiments/G1_group_fluidity/analyse_g1.py discovery
  python experiments/G1_group_fluidity/analyse_g1.py holdout
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_g1 import DISCOVERY, HOLDOUT, LAGS  # noqa: E402

WEEKS = {1: 4, 3: 12, 6: 24, 13: 52, 26: 104}


def share(n, key):
    d = n.get("den_" + key, 0)
    return n.get("num_" + key, 0) / d if d else None


def f(x):
    return "–" if x is None else f"{x:.3f}"


def reading(p12, p104):
    if p104 is not None and p104 >= 0.5:
        return "ACL's groups are more fixed than forager bands (co-residence lasts years)"
    if p12 is not None and p12 < 0.5:
        return "ACL's groups are more fluid than forager bands (co-residence does not last months)"
    return "consistent with the forager benchmark ('stable over months but not years')"


def main(name):
    seeds = DISCOVERY if name == "discovery" else HOLDOUT
    R = [json.loads((HERE / "output" / f"seed_{s}.json").read_text(encoding="utf-8")) for s in seeds]
    L = []
    w = L.append
    w(f"# G1 — Group fluidity: {name} ({len(R)} control worlds, seeds {seeds[0]}–{seeds[-1]})\n")
    checks = (HERE / "output" / "checks.txt").read_text(encoding="utf-8")
    rep = [r.get("reproduces") for r in R]
    w(f"- Observer read-only: **{'yes' if 'All: PASS' in checks else 'NO'}**; code unchanged: "
      f"**{'yes' if all(r['code_hash'] == r['code_hash_after'] for r in R) else 'NO'}**"
      + (f"; reproduce F1's populations: **{sum(x is True for x in rep)} of {len(R)}**" if name == "discovery" else ""))
    died = sum(not (len(r["pops"]) == 12 and r["pops"][-1] > 0) for r in R)
    w(f"- Baseline (rule 14): {died} of {len(R)} died out.\n")
    pooled = Counter()
    for r in R:
        pooled.update(r["groups"])
    b = pooled["blocks_with_pairs"]
    w("## Population and single-group blocks\n")
    w(f"- 4-week blocks with at least two adults: {b}; mean adults per such block "
      f"{pooled['adult_blocks'] / b:.1f}; per-world median of mean adults "
      f"{statistics.median(r['groups']['adult_blocks'] / r['groups']['blocks_with_pairs'] for r in R if r['groups'].get('blocks_with_pairs')):.1f}")
    s2, s4 = pooled["single_group_blocks_r2"] / b, pooled["single_group_blocks_r4"] / b
    w(f"- Blocks in which all adults form one group: camp radius {s2:.1%}; perception {s4:.1%}"
      + (" — **more than half: persistence there is 1 by construction** (reading also given for blocks with two or more "
         "groups)" if s2 > 0.5 else "") + "\n")
    w("## Co-residence persistence P(Δ): share of co-resident adult pairs still co-resident Δ later\n")
    w("| groups | Δ weeks | pooled | per-world median [IQR] | pairs (pooled) | seeker pairs | other pairs | multi-group blocks |")
    w("|---|---|---|---|---|---|---|---|")
    for tag, lab in (("r2", "camp radius (primary)"), ("r4", "perception (sensitivity)")):
        for lag in LAGS:
            k = f"{tag}_{lag}"
            per = sorted(x for x in (share(r["groups"], k) for r in R) if x is not None)
            q = statistics.quantiles(per, n=4) if len(per) >= 4 else [None, None, None]
            w(f"| {lab} | {WEEKS[lag]} | **{f(share(pooled, k))}** | {f(statistics.median(per) if per else None)} "
              f"[{f(q[0])}, {f(q[2])}] | {pooled.get('den_' + k, 0)} | {f(share(pooled, k + '_seeker'))} | "
              f"{f(share(pooled, k + '_other'))} | {f(share(pooled, k + '_multi'))} |")
    p12, p104 = share(pooled, "r2_3"), share(pooled, "r2_26")
    w(f"\n**Frozen reading** (pooled, camp radius; P(12 weeks) = {f(p12)}, P(104 weeks) = {f(p104)}): "
      f"**{reading(p12, p104)}**.")
    if s2 > 0.5:
        m12, m104 = share(pooled, "r2_3_multi"), share(pooled, "r2_26_multi")
        w(f"\nBlocks with two or more groups only (descriptive): P(12) = {f(m12)}, P(104) = {f(m104)}: {reading(m12, m104)}.")
    p12b, p104b = share(pooled, "r4_3"), share(pooled, "r4_26")
    w(f"\nSensitivity (perception): P(12) = {f(p12b)}, P(104) = {f(p104b)}: {reading(p12b, p104b)}.")
    text = "\n".join(L) + "\n"
    (HERE / f"results_{name}.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
