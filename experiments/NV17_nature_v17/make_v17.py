"""Nature v17 = v16 + OD1's doors (experiments/OD1_open_doors/findings.md), the arm that the frozen rule lets go live:
'o' (D1-D5) or 'p' (D2-D5, D1 closed). The doors come from OD1's own patch (patch_od1.py, unchanged); this script only
turns the adopted doors' defaults to 1. Prepared before OD1's data; run only after OD1's findings are final.

  python experiments/NV17_nature_v17/make_v17.py <o|p> <acl folder>      # patches that folder in place (line endings kept)
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ARM = sys.argv[1]
assert ARM in ("o", "p")
root = Path(sys.argv[2])
subprocess.run([sys.executable, str(HERE.parent / "OD1_open_doors" / "patch_od1.py"), str(root)], check=True)
ON = ["containers_carry", "made_binders", "made_hammers", "layers_add"] + (["similar_parts"] if ARM == "o" else [])
p = root / "config.py"
s = p.read_bytes().decode("utf-8")
crlf = "\r\n" in s
s = s.replace("\r\n", "\n")
for d in ON:
    old = f"    {d}: int = 0 "
    assert s.count(old) == 1, d
    s = s.replace(old, f"    {d}: int = 1 ")
s = s.replace("# OD1 (D", "# NV17 (OD1, D")
p.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))
print("v17 doors on:", ", ".join(ON), "in", root)
