"""E3, second pass analysis: why infants starve more in E2. Read-only. Appends to report.md."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"


def load(code):
    c, ok, n = Counter(), [], 0
    for f in sorted(OUT.glob(f"feed_{code}_seed_*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        c.update(r["counts"])
        ok.append(r["identical"])
        n += 1
    return c, ok, n


def per(c, tag, key):
    return c.get(f"{tag}:{key}", 0) / max(1, c.get(f"{tag}:weeks", 0))


def main():
    a, ok1, n1 = load("e1")
    b, ok2, n2 = load("e2")
    L = ["", "## Second pass: how infants were fed, week by week", ""]
    w = L.append
    w(f"Every infant-week of the first 100 years, recorded just before and after the week's feeding. Re-runs identical "
      f"to the saved experiments: E1 {sum(1 for x in ok1 if x)}/{n1}, E2 {sum(1 for x in ok2 if x)}/{n2}.")
    w("")
    for name, c in (("E1", a), ("E2", b)):
        weeks = c["hungry:weeks"] + c["fed:weeks"]
        w(f"- **{name}:** {weeks} infant-weeks; the infant went hungry in {c['hungry:weeks']} "
          f"({100 * c['hungry:weeks'] / max(1, weeks):.1f}%).")
    w("")
    rows = [
        ("carer's food before feeding (units)", "carer_food", False),
        ("carer's own need + dependents' need", "carer_need_total", False),
        ("carer had less than that need", "short", True),
        ("dependents the carer feeds", "deps", False),
        ("carer foraged that week", "did_forage", True),
        ("food the carer foraged that week", "foraged", False),
        ("carer was given food that week", "got_gift", True),
        ("food given to the carer that week", "gift", False),
        ("carer is the mother", "carer_is_mother", True),
        ("carer has a partner alive", "has_mate", True),
        ("partner within 2 tiles", "mate_near", True),
    ]
    w("| per infant-week | E1 fed | E1 hungry | E2 fed | E2 hungry |")
    w("|---|---|---|---|---|")
    for label, key, pct in rows:
        vals = [per(a, "fed", key), per(a, "hungry", key), per(b, "fed", key), per(b, "hungry", key)]
        fmt = (lambda v: f"{100 * v:.0f}%") if pct else (lambda v: f"{v:.1f}")
        w(f"| {label} | " + " | ".join(fmt(v) for v in vals) + " |")
    w("")
    acts = sorted({k.split(":act:")[1] for k in list(a) + list(b) if ":act:" in k})
    w("What the carer did that week (share of infant-weeks):")
    w("")
    w("| carer's action | E1 fed | E1 hungry | E2 fed | E2 hungry |")
    w("|---|---|---|---|---|")
    for act in sorted(acts, key=lambda x: -(per(b, "hungry", "act:" + x) + per(a, "hungry", "act:" + x))):
        vals = [per(a, "fed", "act:" + act), per(a, "hungry", "act:" + act),
                per(b, "fed", "act:" + act), per(b, "hungry", "act:" + act)]
        if max(vals) >= 0.01:
            w(f"| {act} | " + " | ".join(f"{100 * v:.0f}%" for v in vals) + " |")
    w("")
    (HERE / "report.md").write_text((HERE / "report.md").read_text(encoding="utf-8").split("\n## Second pass")[0].rstrip()
                                    + "\n" + "\n".join(L) + "\n", encoding="utf-8")
    print("appended to report.md")


if __name__ == "__main__":
    main()
