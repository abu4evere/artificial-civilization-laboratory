"""Reproducibility guard: a few reference worlds must replay to exactly the recorded state.

`tests/reference_hashes.json` holds state hashes of short runs of (1) ACL's own code (the live world) and (2) the frozen
control copy used by the experiments (`experiments/E13R_replication/code_e13r`). If ACL's nature is changed on purpose,
regenerate the first set (python tests/test_reference_replays.py --update acl) and say so in the commit; the control copy
is frozen and its hashes should never change.

The hashes were made on Windows 10 (build 19045) with Python 3.14.7. Exact replay also depends on Windows' own C maths
library: on Windows Server 2025 one pow() result differs in its last digit, and the frozen control world, seed 11, parts
from this PC's at week 121 (traced with tools/ci/replay_trace.py, 12 October 2026). Windows Server 2022 matches this PC,
so CI runs there. Worlds replayed on another system can therefore differ in detail while being the same model.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = Path(__file__).with_name("reference_hashes.json")
CODES = {"acl": ROOT, "control": ROOT / "experiments" / "E13R_replication" / "code_e13r",
         "v2": ROOT / "experiments" / "NV2_nature_v2" / "code_v2",
         "v3": ROOT / "experiments" / "NV3_nature_v3" / "code_v3",
         "v4": ROOT / "experiments" / "NV4_nature_v4" / "code_v4",
         "v5": ROOT / "experiments" / "NV5_nature_v5" / "code_v5",
         "v6": ROOT / "experiments" / "NV6_nature_v6" / "code_v6"}
# Each code's settings: ACL's own code has none (since 16 October 2026 its defaults were nature v2; since 21 October 2026 nature v3; since 23 October 2026
# nature v4; since 24 October 2026 nature v5, then v6, so
# its hashes equal v6's); the control copy runs as the experiments do; v2 is the control code with
# NV2's four changes on (experiments/NV2_nature_v2/questions.md). Like the control hashes, v2's should never change.
EXTRA = {"acl": "", "control": ", anticipation_weight=1.0",
         "v2": ", anticipation_weight=1.0, loved_location='last_seen', corner_block=1, ashore_if_float_breaks=1, knowledge_copy=1",
         "v3": ", anticipation_weight=1.0, loved_location='last_seen', corner_block=1, ashore_if_float_breaks=1, knowledge_copy=1, parts_first=1",
         "v4": ", anticipation_weight=1.0, loved_location='last_seen', corner_block=1, ashore_if_float_breaks=1, knowledge_copy=1, parts_first=1, bodies_stay=1",
         "v5": ", anticipation_weight=1.0, loved_location='last_seen', corner_block=1, ashore_if_float_breaks=1, knowledge_copy=1, parts_first=1, bodies_stay=1, digging=1",
         "v6": ", anticipation_weight=1.0, loved_location='last_seen', corner_block=1, ashore_if_float_breaks=1, knowledge_copy=1, parts_first=1, bodies_stay=1, digging=1, body_rot=1"}
CASES = [(11, 5), (501, 5)]          # (seed, years)


def _hash(code: str, seed: int, years: int) -> str:
    """Run in a fresh process, so the two packages named `acl` never meet."""
    extra = EXTRA[code]
    prog = ("import sys; sys.path.insert(0, sys.argv[1]); from acl import Config, World;"
            f"w = World(Config(seed=int(sys.argv[2]){extra}));"
            "[w.step() for _ in range(int(sys.argv[3]) * 52)]; print(w.state_hash())")
    out = subprocess.run([sys.executable, "-c", prog, str(CODES[code]), str(seed), str(years)],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip().splitlines()[-1]


def _check(code: str) -> None:
    ref = json.loads(REF.read_text(encoding="utf-8"))[code]
    for seed, years in CASES:
        assert _hash(code, seed, years) == ref[f"{seed}:{years}"], f"{code} world, seed {seed}, {years} years no longer replays"


def test_acl_reference_worlds_replay():
    _check("acl")


def test_frozen_control_code_replays():
    _check("control")


def test_nature_v2_replays():
    _check("v2")


def test_nature_v3_replays():
    _check("v3")


def test_nature_v4_replays():
    _check("v4")


def test_nature_v5_replays():
    _check("v5")


def test_nature_v6_replays():
    _check("v6")


if __name__ == "__main__" and sys.argv[1:2] == ["--update"]:
    which = sys.argv[2:] or list(CODES)
    data = json.loads(REF.read_text(encoding="utf-8")) if REF.exists() else {}
    for code in which:
        data[code] = {f"{s}:{y}": _hash(code, s, y) for s, y in CASES}
    REF.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=1))
