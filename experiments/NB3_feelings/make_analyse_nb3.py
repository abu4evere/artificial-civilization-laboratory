"""One-time helper (kept for the record): builds analyse_nb3.py from NB2's frozen analysis, with NB3's arms and reading."""
from pathlib import Path

HERE = Path(__file__).parent
s = (HERE.parent / "NB2_connected_brain" / "analyse_nb2.py").read_text(encoding="utf-8")


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep('"""NB2 analysis (questions.md, NB2-frozen). Written before data. Paired world bootstrap, 10,000 draws, NumPy seed\n20261110.',
    '"""NB3 analysis (questions.md, NB3-frozen). Written before data, from NB2\'s. Paired world bootstrap, 10,000 draws,\nNumPy seed 20261113. Primary: f viable against c (extinct at most c + 3; population ratio upper bound >= 0.80; the\npoint and lower bound also reported). Secondary: the ablations, causes of death (years 100-600), survival to 16, genes.\n\nNB2\'s docstring:')
rep('import run_nb2 as R  # noqa: E402', 'import run_nb3 as R  # noqa: E402')
rep('RNG = np.random.default_rng(20261110)', 'RNG = np.random.default_rng(20261113)')
rep('ARMS = ("c", "s", "o", "l", "n")', 'ARMS = ("c", "n2", "f0", "fH", "f", "fmE", "fmH")')
rep('''NAME = {"c": "v17 (old minds)", "s": "sham: new options and sight, learning off", "o": "o: + NB1's REINFORCE",
        "l": "l: + actor-critic", "n": "n: + social learning (full NB2)"}''',
    '''NAME = {"c": "v17 (old minds)", "n2": "NB2's full brain", "f0": "f0: no joy in attacking", "fH": "fH: + inborn reluctance",
        "f": "f: all feelings", "fmE": "f without empathy", "fmH": "f without the inborn reluctance"}''')
rep('re.search(r"code_nb2 fingerprint: ([0-9a-f]{64})", zero)', 're.search(r"code_nb3 fingerprint: ([0-9a-f]{64})", zero)')
rep('''    L = ["# NB2: connect the world to the neural brain. Can the network decide? (results)", "",
         "Frozen as `NB2-frozen`. run_nb2.py, run_nb2_garden.py, analyse_nb2.py (written before data).", "",''',
    '''    L = ["# NB3: feelings. Can a neural people live in the open world if it is born with human feelings? (results)", "",
         "Frozen as `NB3-frozen`. run_nb3.py, analyse_nb3.py (written before data).", "",''')
rep('''f"- Zero checks (All: PASS, `code_nb2` fingerprint)''', '''f"- Zero checks (All: PASS, `code_nb3` fingerprint)''')
rep('''f"- One fingerprint, `code_nb2`'s''', '''f"- One fingerprint, `code_nb3`'s''')
# the primary: f against c
rep('''    viable = ext["n"] - ext["c"] <= 3 and pop["n"][1][1] >= 0.80''',
    '''    viable = ext["f"] - ext["c"] <= 3 and pop["f"][1][1] >= 0.80
    viable_by = {a: ext[a] - ext["c"] <= 3 and pop[a][1][1] >= 0.80 for a in ARMS[1:]}''')
rep('''    prim = diff("n", "s")
    learn_helps = prim[1][0] > 0''', '''    prim = diff("f", "n2")
    learn_helps = prim[1][0] > 0''')
rep('''    if not viable:
        reading = "not viable"
    elif learn_helps and inherited_yes:
        reading = "the network decides"
    elif learn_helps:
        reading = "learning helps, but the instincts still carry it"
    else:
        reading = "no improvement shown"''', '''    reading = "f viable" if viable else "f not viable"
    alive = {a: boot_mean([garden[(a, s)]["alive_1y"] / garden[(a, s)]["founders"] for s in seeds if (a, s) in garden])
             for a in ("g1Z", "g18Z")}''')
rep('''          f"- Viability: extinct worlds " + ", ".join(f"{a} {ext[a]}" for a in ARMS) + "; population (living-weeks, "
          f"years 100-600) against c: " + ", ".join(f"{a} {pop[a][0]:.4f} [{pop[a][1][0]:.4f}, {pop[a][1][1]:.4f}]"
                                                      for a in ARMS[1:]) + f"; n viable: **{'yes' if viable else 'no'}**.",
          f"- **Primary**, survival to 16 per birth (born years 100-600), n - s: {fd(prim)}; above 0: "
          f"**{'yes' if learn_helps else 'no'}**.",
          f"- Inherited competence (generation 18 - 1, g = 0, learning off): {fb(inherited)}; above 0: "
          f"**{'yes' if inherited_yes else 'no'}**.",
          f"- Learning's worth (generation 18, on - off): {fb(worth)}.", "",
          "Rule: 'not viable' if n has more than 3 extra extinct worlds than c or the population ratio's upper bound is "
          "below 0.80; 'the network decides' if n - s and the inherited garden both have lower bounds above 0; 'learning "
          "helps, but the instincts still carry it' if only n - s does; otherwise 'no improvement shown'.", "",''',
    '''          f"- Viability: extinct worlds " + ", ".join(f"{a} {ext[a]}" for a in ARMS) + "; population (living-weeks, "
          f"years 100-600) against c, point [2.5%, 97.5%]: " + ", ".join(
              f"{a} {pop[a][0]:.4f} [{pop[a][1][0]:.4f}, {pop[a][1][1]:.4f}]" for a in ARMS[1:]) + ".",
          f"- **Primary: f viable against c: {'yes' if viable else 'no'}.** (By the same rule: "
          + ", ".join(f"{a} {'yes' if viable_by[a] else 'no'}" for a in ARMS[1:]) + ")",
          f"- Survival to 16 per birth, f - n2: {fd(prim)}.",
          f"- Garden (if present; g = 0, learning off, feeling genes as inherited): founders alive after one year, "
          f"generation 1 {fb(alive['g1Z'])}, generation 18 {fb(alive['g18Z'])}; survival to 16, generation 18 - 1: "
          f"{fb(inherited)}.", "",
          "Rule (frozen): 'f viable' if f's extinct worlds are at most c's + 3 and the upper bound of f/c's population "
          "ratio is at least 0.80. Council 84 asked that the point and the lower bound be read too.", "",''')
rep('''    for a, b, lab in (("o", "s", "NB1's learning on the new options (o - s)"), ("l", "o", "actor-critic instead (l - o)"),
                      ("n", "l", "social learning (n - l)"), ("s", "c", "new options and sight, no learning, against the old minds (s - c)"),
                      ("n", "c", "full NB2 against the old minds (n - c)")):''',
    '''    for a, b, lab in (("f0", "n2", "no joy in attacking (f0 - n2)"), ("fH", "f0", "the inborn reluctance (fH - f0)"),
                      ("f", "fH", "the other feelings (f - fH)"), ("f", "fmE", "empathy (f - f without E)"),
                      ("f", "fmH", "the reluctance among all feelings (f - f without H)"), ("f", "c", "f against the old minds")):''')
rep('''    for a in ARMS[1:]:
        L.append(f"| {a} | " + " | ".join((f"{v:.3f} ({k})" if math.isfinite(v) else "-") for v, k in
                                         (g_at(a, y) for y in years)) + " |")''',
    '''    for a in ARMS[1:]:
        L.append(f"| {a} | " + " | ".join((f"{v:.3f} ({k})" if math.isfinite(v) else "-") for v, k in
                                         (g_at(a, y) for y in years)) + " |")

    def gene_at(a, year, gname):
        vals = [next((y.get(f"{gname}_mean") for y in runs[a][s]["years"] if y["year"] == year), None) for s in seeds]
        vals = [v for v in vals if v is not None]
        return (float(np.mean(vals)) if vals else float("nan")), len(vals)
    L += ["", "## The feeling genes in f (mean over worlds; start values E 0.5, G 0.5, L 1.0, A 0.5, C 0.5, H 1.0)", "",
          "| gene | " + " | ".join(str(y) for y in years) + " |", "|---|" + "---|" * len(years)]
    for gname in ("E", "G", "L", "A", "C", "H"):
        L.append(f"| {gname} | " + " | ".join((f"{v:.3f} ({k})" if math.isfinite(v) else "-") for v, k in
                                             (gene_at("f", y, gname) for y in years)) + " |")''')
rep('''    L += ["", "## CI1's eight guards, full NB2 (n) against v17 (descriptive; 16 seeds cannot gate harm)", "",''',
    '''    L += ["", "## CI1's guards, f (all feelings) against v17 (descriptive; years 100-600)", "",''')
rep('''        pa, pc, rr, ci = ratio("n", num, den, per)''', '''        pa, pc, rr, ci = ratio("f", num, den, per)''')
rep('''    # the network's part
    L += ["", "## The network's part of the decision (every 50th decision)", "",''',
    '''    # causes of death and the mix of acts (frozen secondaries; descriptive)
    causes = sorted({k[6:] for a in ARMS for s in seeds for k in runs[a][s]["sums"] if k.startswith("death_")})
    L += ["", "## Causes of death, share of all deaths by arm (years 100-600)", "",
          "| arm | deaths | " + " | ".join(causes) + " |", "|---|---|" + "---|" * len(causes)]
    for a in ARMS:
        tot = col(a, "deaths").sum()
        L.append(f"| {a} | {int(tot):,} | " + " | ".join(
            (f"{col(a, 'death_' + c).sum() / tot:.3f}" if tot else "-") for c in causes) + " |")
    ACTS = ("hunt", "attack", "steal", "give", "care", "take", "make")
    L += ["", "## Adults' acts, share of all adult acts by arm (centuries 1-5, years 100-600)", "",
          "| arm | acts | " + " | ".join(ACTS) + " |", "|---|---|" + "---|" * len(ACTS)]
    for a in ARMS:
        tot, cnt = 0, {x: 0 for x in ACTS}
        for s in seeds:
            for cen, d in runs[a][s].get("acts", {}).items():
                if 1 <= int(cen) <= 5:
                    tot += sum(d.values())
                    for x in ACTS:
                        cnt[x] += d.get(x, 0)
        L.append(f"| {a} | {tot:,} | " + " | ".join((f"{cnt[x] / tot:.4f}" if tot else "-") for x in ACTS) + " |")

    # the network's part
    L += ["", "## The network's part of the decision (every 50th decision; H counted with the instincts)", "",''')
(HERE / "analyse_nb3.py").write_text(s, encoding="utf-8")
print("built analyse_nb3.py")
