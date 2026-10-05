"""Traces: what doing things leaves on the land (turned earth, stone flakes, ash, bones).

Physics only. A trace is plain to see for a while and then fades. See world.TRACE_KEEP.
"""
from __future__ import annotations


def leave_trace(tile, kind: str, tick: int, amount: float = 1.0) -> None:
    rec = tile.traces.get(kind)
    if rec is None:
        tile.traces[kind] = [round(min(1.0, amount), 3), tick]
    else:
        rec[0] = round(min(1.0, rec[0] + amount), 3)
        rec[1] = tick
