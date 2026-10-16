"""Put the creator's answers (drafts/creators_note.md) into a book source: Chapter 0 from answers 1-6, and answers 7-11
as Creator's Notes in place of the placeholders. Wording kept as given, with the creator's two changes of 16 October
2026: "bro" dropped; Reibik's pronouns made neutral (the record does not give Reibik's sex).
    python drafts/apply_creators_note.py BOOK_SOURCE.md
"""
import re, sys
from pathlib import Path

notes = Path(__file__).with_name("creators_note.md").read_text(encoding="utf-8")
parts = re.split(r"^## (\d+)\. .*$", notes, flags=re.M)
ans = {int(parts[i]): parts[i + 1].strip() for i in range(1, len(parts), 2)}

def unwrap(text):
    paras = [" ".join(l.strip() for l in p.splitlines()) for p in re.split(r"\n\s*\n", text.strip())]
    return "\n\n".join(paras)

a = {k: unwrap(v) for k, v in ans.items()}
a[5] = a[5].replace("I think because, bro, building", "I think because building")
r = a[11]
for x, y in [("Then he spent two years", "Then Reibik spent two years"),
             ("His behavior alone doesn't tell me exactly why he never filled it.",
              "Reibik's behavior alone doesn't tell me exactly why the vessel was never filled."),
             ("Perhaps he didn't understand", "Perhaps Reibik didn't understand"),
             ("Perhaps he never formed", "Perhaps Reibik never formed"),
             ("what makes his story", "what makes Reibik's story")]:
    assert x in r, x
    r = r.replace(x, y)
assert not re.search(r"\b(he|his|him)\b", r), "a pronoun is left in answer 11"
a[11] = r

ch0 = ("## Chapter 0 — Why This Project Exists\n\nThese are the creator's own words.\n\n"
       "**Where it started.** " + a[1] + "\n\n"
       "**Emergence.** " + a[2] + "\n\n"
       "**What was missing.** " + a[3] + "\n\n"
       "**Written by nobody.** " + a[4] + "\n\n"
       "**Why a world.** " + a[5] + "\n\n"
       "**What I hope you take from it.** " + a[6] + "\n\n")

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
i = s.index("// ===="); j = s.index("// ====", i + 10)
j = s.index("\n", j) + 1
s = s[:i] + ch0 + s[j:]
places = {7: "Who is Bob to you?", 8: "Why does this rule matter so much to you?", 9: "What did the E5 freeze feel like?",
          10: "Why did you prefer to leave the people unchanged?", 11: "What was it like to read Reibik's 102 weeks"}
for k, key in places.items():
    m = re.search(r"^// CREATOR'S NOTE \(to be written\): " + re.escape(key) + r".*$", s, flags=re.M)
    assert m, key
    s = s[:m.start()] + "**Creator's note.** " + a[k] + s[m.end():]
assert "CREATOR'S NOTE (to be written)" not in s
p.write_text(s, encoding="utf-8")
print("applied to", p)
