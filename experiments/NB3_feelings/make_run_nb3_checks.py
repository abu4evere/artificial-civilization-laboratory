"""One-time helper (kept for the record): replaces the NB2 checks copied into run_nb3.py with NB3's own checks."""
from pathlib import Path

HERE = Path(__file__).parent
p = HERE / "run_nb3.py"
s = p.read_text(encoding="utf-8")
a = s.index("def reload_check(seed):")
b = s.index("def save_ckpt(")
new = (HERE / "nb3_checks_block.py").read_text(encoding="utf-8")
s = s[:a] + new + "\n\n" + s[b:]
p.write_text(s, encoding="utf-8")
print("ok")
