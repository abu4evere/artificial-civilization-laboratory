"""Build the ACL Mind page: the template with the brain-scan data (design/brain_v11/brain_data_v11.json) inlined.
  python design/mind_v11/build_mind_page.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = (HERE.parent / "brain_v11" / "brain_data_v11.json").read_text(encoding="utf-8")
page = (HERE / "mind_template.html").read_text(encoding="utf-8").replace("/*DATA*/null", data)
(HERE / "acl_mind_v11.html").write_text(page, encoding="utf-8")
print(f"wrote acl_mind_v11.html: {len(page) // 1024} KB")
