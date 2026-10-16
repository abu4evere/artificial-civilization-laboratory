"""Running, saving and resuming a world, and writing out what happened."""
from __future__ import annotations

import gzip
import json
import time
from pathlib import Path

from .config import VERSIONS, WEEKS_PER_YEAR, Config
from .historian import Historian
from .world import World


class EventLog:
    """Appends every event to a gzipped JSON-lines file."""

    def __init__(self, path: Path):
        self.f = gzip.open(path, "at", encoding="utf-8")

    def __call__(self, world, events):
        for e in events:
            self.f.write(json.dumps(e, separators=(",", ":")) + "\n")

    def close(self):
        self.f.close()


def save_snapshot(world: World, historian: Historian, path: Path) -> None:
    blob = {"world": world.to_dict(), "historian": historian.to_dict(), "versions": VERSIONS}
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(blob, f, separators=(",", ":"))   # key order matters: it is the order people think in


def load_snapshot(path: Path) -> tuple[World, Historian]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        blob = json.load(f)
    # A world saved under other laws of nature cannot be continued under these: its things and records are on another
    # scale. Saves without a version come from before nature v2 (world bible 7.1). Nothing is deleted; run such a world
    # from the `nature-v1` tag, or begin a new one (`python -m acl live --new` sets the old one aside).
    saved = blob.get("versions", {"world_bible": "7.1 or earlier"})
    if saved != VERSIONS:
        raise ValueError(f"{path} was saved under world bible {saved.get('world_bible')}, but this code is world bible "
                         f"{VERSIONS['world_bible']} (nature v2). Continue it from the `nature-v1` tag, or begin a new "
                         f"world; the saved one is left as it is.")
    return World.from_dict(blob["world"]), Historian.from_dict(blob["historian"])


def simulate(world: World, historian: Historian, years: int, out: Path | None = None,
             snapshot_every: int = 0, log_events: bool = True, progress=None) -> dict:
    """Run `years` more years. Writes events, snapshots and results into `out` if given."""
    if historian not in world.observers:
        world.observers.append(historian)
    log = None
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        if log_events:
            log = EventLog(out / "events.jsonl.gz")
            world.observers.append(log)
    started = time.time()
    end_tick = world.tick + years * WEEKS_PER_YEAR
    try:
        while world.tick < end_tick and world.living():
            world.step()
            if world.tick % WEEKS_PER_YEAR == 0:
                year = world.tick // WEEKS_PER_YEAR
                if progress:
                    progress(world, historian)
                if out is not None and snapshot_every and year % snapshot_every == 0:
                    save_snapshot(world, historian, out / f"snapshot_y{year:04d}.json.gz")
    finally:
        if log is not None:
            log.close()
            world.observers.remove(log)
    result = {
        "seed": world.cfg.seed,
        "metrics": historian.metrics(world),
        "state_hash": world.state_hash(),
        "event_chain": world.event_chain,
        "seconds": round(time.time() - started, 1),
    }
    if out is not None:
        save_snapshot(world, historian, out / "final.json.gz")
        write_outputs(world, historian, result, out)
    return result


def write_outputs(world: World, historian: Historian, result: dict, out: Path) -> None:
    from .report import write_report

    (out / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out / "history.json").write_text(json.dumps({
        "years": historian.years,
        "chronicle": historian.chronicle,
        "bands": historian.band_history,
        "settlements": historian.settlements,
        "feuds": historian.feuds,
        "oral_history": historian.oral_history(world),
    }, indent=1), encoding="utf-8")
    (out / "chronicle.md").write_text(chronicle_markdown(world, historian), encoding="utf-8")
    write_report(world, historian, result, out / "report.html")


def chronicle_markdown(world: World, historian: Historian) -> str:
    lines = [f"# Chronicle of seed {world.cfg.seed}", "",
             f"{world.tick // WEEKS_PER_YEAR} years. Started with {world.cfg.founders} founders in "
             f"{max(1, min(4, world.cfg.founders // 4))} bands.", ""]
    year = None
    for e in historian.chronicle:
        if e["kind"] == "era":
            lines += ["", f"> {e['text']}", ""]
            continue
        if e["year"] != year:
            year = e["year"]
            lines += ["", f"## Year {year}"]
        lines.append(f"- {e['text']}")
    oral = historian.oral_history(world)
    if oral:
        lines += ["", "## Still remembered at the end", ""]
        for o in oral:
            lines.append(f"- {o['event']}: remembered by {o['remembered_by']} living people")
    return "\n".join(lines) + "\n"


def new_world(seed: int, **overrides) -> tuple[World, Historian]:
    cfg = Config(seed=seed, **overrides)
    world = World(cfg)
    historian = Historian()
    world.observers.append(historian)
    return world, historian
