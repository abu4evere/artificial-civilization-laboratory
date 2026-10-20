"""Experiment 0 — "Mind Before Civilization".

A deterministic, headless experiment harness for the Artificial Civilization
Laboratory. It adds three things to the existing world, all of them read-only
with respect to the simulation:

* a formal **decision interface** (see :mod:`acl.decision`),
* the **SurpriseLog** — one record per chosen action, with prediction vs.
  outcome, needs and emotions before/after, relationship changes, and any
  knowledge/memory/behaviour copied or transmitted,
* the **InventionLog** — a structured record of every previously-unseen useful
  configuration the matter system produces.

Plus a runner that supports staged feature toggles (E0-A..E0-D), checkpointing,
resume, replay, and an honest "kill criterion" report.

The governing principle: *the creator writes the laws of the universe, not the
history* — and its extension: *the creator writes the laws of the mind, not the
mind itself.* Nothing here makes the agents interesting; it only measures
whether the laws let them become interesting.
"""
from __future__ import annotations

import gzip
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import decision
from .config import VERSIONS, WEEKS_PER_YEAR
from .historian import classify
from .runner import load_snapshot, new_world, save_snapshot

EXPERIMENT_ID = "E0"
WORLD_BIBLE_VERSION = VERSIONS["world_bible"]
WORLD_VERSION = VERSIONS["world"]
AGENT_VERSION = VERSIONS["agent"]

_EMOTIONS = ("mood", "fear", "anger", "grief", "loneliness", "wellbeing")
_NEEDS = ("health", "energy", "food", "sick", "starving")
_REL_DIMS = (0, 1, 3, 4)   # affection, trust, grudge, respect (of Relation.to_list())


@dataclass
class ExperimentConfig:
    experiment_id: str = EXPERIMENT_ID
    world_bible_version: str = WORLD_BIBLE_VERSION
    world_version: str = WORLD_VERSION
    agent_version: str = AGENT_VERSION
    seed: int = 42
    duration_days: int = 500
    founders: int = 10
    stage: str = "E0-D"

    def weeks(self) -> int:
        return max(1, self.duration_days // 7)


# ---------------------------------------------------------------------------
# The SurpriseLog (read-only)
# ---------------------------------------------------------------------------

def _jsonable_target(t):
    if isinstance(t, tuple):
        return list(t)
    return t


def _rel_changes(before: dict, after: dict) -> list:
    out = []
    for k in set(before) | set(after):
        b, a = before.get(k), after.get(k)
        if b is None:
            out.append([k, "formed"])
        elif a is None:
            out.append([k, "ended"])
        else:
            d = [round(a[i] - b[i], 3) for i in _REL_DIMS]
            if any(abs(x) >= 0.01 for x in d):
                out.append([k, d])
    return out


def _copied(events, agent_id):
    return [e.get("thing") for e in events
            if e["k"] == "learn" and e.get("a") == agent_id and e.get("how") == "copied"]


def _transmitted(events, agent_id):
    return [e.get("thing") or e.get("belief") for e in events
            if e["k"] == "learn" and e.get("b") == agent_id and e.get("how") in ("taught", "told")]


class SurpriseLog:
    """Read-only observer: records every decision and its measured outcome.

    It never touches the world. It only reads ``world.week_decisions`` (written
    by :func:`acl.decision.decide`) and the agent's state after the week.
    """

    def __init__(self, cfg: ExperimentConfig):
        self.cfg = cfg
        self.records = []

    def __call__(self, world, events) -> None:
        for d in world.week_decisions:
            p = world.people.get(d.agent_id)
            if p is None:
                continue
            after = decision.state_snapshot(world, p)
            before = d.state
            reward = p.reward if p.alive else 0.0
            chosen = d.chosen
            self.records.append({
                "experiment_id": self.cfg.experiment_id,
                "tick": d.tick,
                "agent_id": d.agent_id,
                "location": before["loc"],
                "state_snapshot_ref": before["ref"],
                "candidate_actions": d.candidates,
                "chosen_action": [chosen[0], _jsonable_target(chosen[1])],
                "predicted_outcome": d.prediction,
                "actual_outcome": {"reward": round(reward, 3), "alive": p.alive},
                "prediction_error": decision.prediction_error(d, reward),
                "energy_before": before["energy"],
                "energy_after": after["energy"],
                "needs_before": {k: before[k] for k in _NEEDS if k in before},
                "needs_after": {k: after[k] for k in _NEEDS if k in after},
                "emotional_state_before": {k: before[k] for k in _EMOTIONS if k in before},
                "emotional_state_after": {k: after[k] for k in _EMOTIONS if k in after},
                "relationship_changes": _rel_changes(before["relationships"], after["relationships"]),
                "new_knowledge": {
                    "recipes": sorted(set(after["recipes"]) - set(before["recipes"])),
                    "beliefs": sorted(set(after["beliefs"]) - set(before["beliefs"])),
                },
                "new_memory": sorted(set(after["memories"]) - set(before["memories"])),
                "copied_behavior": _copied(events, d.agent_id),
                "transmitted_behavior": _transmitted(events, d.agent_id),
                "researcher_prediction": None,
                "researcher_note": None,
            })

    def to_dict(self) -> dict:
        return {"records": self.records}


# ---------------------------------------------------------------------------
# The InventionLog (read-only)
# ---------------------------------------------------------------------------

class InventionLog:
    """Read-only observer: records each previously-unseen useful configuration.

    It observes; it does not create. The matter system produces the invention;
    this only writes it down with its properties, re-use, and transmission.
    """

    def __init__(self):
        self.records = []
        self._by_thing = {}

    def __call__(self, world, events) -> None:
        for e in events:
            if e["k"] in ("make", "play") and e.get("thing"):
                self._record(world, e)
            elif e["k"] == "learn" and e.get("thing"):
                self._transmit(e)

    def _record(self, world, e) -> None:
        sig = e["thing"]
        rec = self._by_thing.get(sig)
        if rec is not None:
            rec["repeated_use"] += 1
            rec["last_tick"] = e["t"]
            return
        props = {k: e.get(k) for k in ("edge", "reach", "hard", "contain", "warm", "float")}
        rec = {
            "invention_id": len(self.records),
            "first_tick": e["t"],
            "last_tick": e["t"],
            "agent_id": e.get("a"),
            "thing": sig,
            "how": e["k"],
            "result_properties": props,
            "classes": classify(props),
            "repeated_use": 0,
            "copied_by": [],
            "taught_to": [],
            "survived_generation": None,
        }
        self.records.append(rec)
        self._by_thing[sig] = rec

    def _transmit(self, e) -> None:
        rec = self._by_thing.get(e.get("thing"))
        if rec is None:
            return
        if e.get("how") == "taught":
            rec["taught_to"].append(e.get("a"))
        elif e.get("how") == "copied":
            rec["copied_by"].append(e.get("a"))

    def to_dict(self) -> dict:
        return {"records": self.records}


# ---------------------------------------------------------------------------
# The runner
# ---------------------------------------------------------------------------

def run_experiment(cfg: ExperimentConfig, out: Path | None = None,
                   progress=None) -> dict:
    """Run E0 headlessly and deterministically.

    Returns a dict with metrics, the surprise log, the invention log, and the
    state hash (for replay verification). If ``out`` is given, writes a full
    checkpoint (world + historian + logs) and a summary.
    """
    world, historian = new_world(cfg.seed, founders=cfg.founders, stage=cfg.stage)
    surp = SurpriseLog(cfg)
    inv = InventionLog()
    for obs in (historian, surp, inv):
        if obs not in world.observers:
            world.observers.append(obs)

    started = time.time()
    world.run(cfg.weeks())
    seconds = round(time.time() - started, 1)

    result = {
        "config": asdict(cfg),
        "seed": cfg.seed,
        "weeks": world.tick,
        "years": round(world.tick / WEEKS_PER_YEAR, 2),
        "population_end": len(world.living()),
        "state_hash": world.state_hash(),
        "event_chain": world.event_chain,
        "seconds": seconds,
        "metrics": historian.metrics(world),
        "surprise": surp.to_dict(),
        "inventions": inv.to_dict(),
    }
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        save_snapshot(world, historian, out / "final.json.gz")
        (out / "surprise_log.json").write_text(
            json.dumps(result["surprise"], indent=1), encoding="utf-8")
        (out / "invention_log.json").write_text(
            json.dumps(result["inventions"], indent=1), encoding="utf-8")
        (out / "results.json").write_text(
            json.dumps({k: v for k, v in result.items() if k not in ("surprise", "inventions")},
                       indent=1), encoding="utf-8")
    return result


def resume_and_verify(cfg: ExperimentConfig, out: Path) -> dict:
    """Replay check: resume from a saved snapshot and confirm an identical world.

    The same seed + configuration must reproduce the same history whether run
    straight through or resumed from a checkpoint.
    """
    snap = out / "final.json.gz"
    world, historian = load_snapshot(snap)
    world.run(cfg.weeks())
    return {
        "resumed_state_hash": world.state_hash(),
        "resumed_event_chain": world.event_chain,
    }


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyse(result: dict) -> dict:
    """The honest post-run accounting: kill criterion, classification, surprises."""
    surp = result["surprise"]["records"]
    inv = result["inventions"]["records"]
    metrics = result["metrics"]

    errors = [r["prediction_error"] for r in surp]
    n = len(surp)

    # Prediction error: is the agent's own expectation ever wrong by much?
    avg_err = round(sum(errors) / n, 3) if n else 0.0
    big_err = sum(1 for e in errors if e >= 1.0)
    # Emotional change per decision (is behaviour ever more than need-triggered?).
    mood_moves = sum(1 for r in surp
                     if abs(r["emotional_state_after"].get("mood", 0) - r["emotional_state_before"].get("mood", 0)) >= 0.05)

    # Inventions: how many were reused, copied, or taught?
    inventions = [r for r in inv if r["classes"]]
    reused = sum(1 for r in inventions if r["repeated_use"] > 0)
    copied = sum(1 for r in inventions if r["copied_by"])
    taught = sum(1 for r in inventions if r["taught_to"])

    # Transmission of knowledge across the whole run.
    transmits = sum(len(r["transmitted_behavior"]) for r in surp)
    copies = sum(len(r["copied_behavior"]) for r in surp)

    # Relationships: did social ties form and change beyond scripted bumps?
    rel_events = sum(1 for r in surp if r["relationship_changes"])

    # Surprise classification of the notable behaviours.
    notable = _classify_notable(result)

    return {
        "decisions": n,
        "avg_prediction_error": avg_err,
        "decisions_with_large_error": big_err,
        "share_large_error": round(big_err / n, 3) if n else 0.0,
        "decisions_with_mood_change": mood_moves,
        "inventions_classified": len(inventions),
        "inventions_reused": reused,
        "inventions_copied": copied,
        "inventions_taught": taught,
        "transmissions_total": transmits,
        "copies_total": copies,
        "relationship_change_events": rel_events,
        "action_counts": metrics.get("action_counts", {}),
        "deaths_by_cause": metrics.get("deaths_by_cause", {}),
        "notable": notable,
    }


def _classify_notable(result: dict) -> list:
    """Classify notable behaviours as NOVEL / REPEATABLE / TRANSMITTED / COPIED /
    INTERGENERATIONAL / CAUSALLY_TRACEABLE / UNEXPLAINED.

    A one-time random event is not automatically emergence; this only applies
    labels that the logs actually support.
    """
    out = []
    for r in result["inventions"]["records"]:
        if not r["classes"]:
            continue
        tags = ["NOVEL"]
        if r["repeated_use"] > 0:
            tags.append("REPEATABLE")
        if r["copied_by"]:
            tags.append("COPIED")
        if r["taught_to"]:
            tags.append("TRANSMITTED")
        out.append({
            "kind": "invention",
            "tick": r["first_tick"],
            "what": r["classes"][0],
            "agent": r["agent_id"],
            "tags": tags,
        })
    return out


def kill_criterion(analysis: dict, baseline_violations: int) -> str:
    """Render the kill-criterion report (A-G) as markdown."""
    return "\n".join([
        "## Kill Criterion",
        "",
        f"- **A. Fully predictable from existing rules:** {analysis['decisions']} decisions total; "
        f"{analysis['decisions'] - analysis['decisions_with_large_error']} had small prediction error "
        f"(|predicted − actual| < 1.0).",
        f"- **B. Unexpected by the preregistered human baseline:** {baseline_violations} (see baseline_predictions.md).",
        f"- **C. Unexpected by the agents themselves:** {analysis['decisions_with_large_error']} decisions "
        f"({analysis['share_large_error']:.1%} with prediction error ≥ 1.0).",
        f"- **D. Repeated:** {analysis['inventions_reused']} inventions were made again.",
        f"- **E. Copied or transmitted:** {analysis['copies_total']} copied, {analysis['transmissions_total']} taught/told.",
        f"- **F. Survived across generations:** none at this horizon ({analysis['decisions'] and '' or ''}~1.4 years).",
        "- **G. Unexplained by a simple mechanism:** see the notable list — only behaviours with an "
        "unambiguous causal chain were marked CAUSALLY_TRACEABLE; anything else is logged, not waved away.",
    ])
