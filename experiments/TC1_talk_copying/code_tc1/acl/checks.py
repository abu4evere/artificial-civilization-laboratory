"""Success criteria for the first version, scored across many seeds.

These check that the foundations work: people survive, raise children and
carry a culture across generations, and things nobody programmed show up. They
are health checks, not targets to tune toward. Passing them on one seed proves
little, which is why `check` runs many.
"""
from __future__ import annotations

from .runner import load_snapshot, new_world, save_snapshot, simulate

CRITERIA = [
    ("survives", "people are still alive at the end",
     lambda m, f: m["population_end"] > 0),
    ("grows", "the population grew past the founders",
     lambda m, f: m["population_peak"] > f),
    ("generations", "at least 3 generations were born",
     lambda m, f: m["max_generation"] >= 3),
    ("children", "at least half of children reached 16",
     lambda m, f: (m["child_survival_to_16"] or 0) >= 0.5),
    ("varied", "people lead varied lives (action entropy at least 0.5)",
     lambda m, f: m["action_entropy"] >= 0.5),
    ("emergent", "at least 5 of 8 unprogrammed patterns appeared",
     lambda m, f: len(emergent_patterns(m)) >= 5),
]


def emergent_patterns(m: dict) -> list[str]:
    found = []
    if m["exchange_partnerships"] > 0:
        found.append("exchange between unrelated people")
    if m["bands_ever"] > 0:
        found.append("bands")
    if m["revenge_acts"] > 0:
        found.append("revenge")
    if m["settlements"] > 0:
        found.append("settlements")
    if m["know_spread"] and max(m["know_spread"].values()) >= 0.3:
        found.append("a made thing many people know")
    if "fire" in m["firsts"]:
        found.append("fire made by hand")
    if "dwelling" in m["firsts"]:
        found.append("dwellings")
    if "farming" in m["firsts"] or "storing" in m["firsts"]:
        found.append("sowing or storing food on purpose")
    return found


def score(metrics: dict, founders: int) -> dict:
    return {key: bool(test(metrics, founders)) for key, _, test in CRITERIA}


def replay_check(seed: int, years: int, tmp_dir) -> dict:
    """The same seed must produce the same history, straight through or resumed from a snapshot."""
    from pathlib import Path

    tmp = Path(tmp_dir)
    tmp.mkdir(parents=True, exist_ok=True)
    w1, h1 = new_world(seed)
    a = simulate(w1, h1, years)
    w2, h2 = new_world(seed)
    b = simulate(w2, h2, years)
    half = years // 2
    w3, h3 = new_world(seed)
    simulate(w3, h3, half)
    snap = tmp / f"replay_seed{seed}.json.gz"
    save_snapshot(w3, h3, snap)
    w4, h4 = load_snapshot(snap)
    c = simulate(w4, h4, years - half)
    return {
        "seed": seed,
        "years": years,
        "run_1": a["state_hash"],
        "run_2": b["state_hash"],
        "resumed_at_year": half,
        "resumed": c["state_hash"],
        "identical": a["state_hash"] == b["state_hash"] == c["state_hash"]
        and a["event_chain"] == b["event_chain"] == c["event_chain"]
        and a["metrics"] == b["metrics"] == c["metrics"],
    }
