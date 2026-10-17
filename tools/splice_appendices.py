# -*- coding: utf-8 -*-
"""Splice generated appendix B/C into the draft (idempotent).
Replaces the body between a '## Appendix X' header and the next '## ' with the generated file.
"""
import re, sys
from pathlib import Path

PAPER = Path(__file__).resolve().parent.parent
DRAFT = PAPER / "DRAFT-v6-20261017.md"

def splice(text, header_prefix, gen_path):
    gen = Path(gen_path).read_text(encoding="utf-8")
    # drop the generated file's own title line and keep the rest
    body = "\n".join(gen.splitlines()[1:]).strip()
    pat = re.compile(r"(## " + re.escape(header_prefix) + r"[^\n]*\n)(.*?)(?=\n## |\Z)", re.S)
    m = pat.search(text)
    if not m:
        raise SystemExit(f"header not found: {header_prefix}")
    return text[:m.start(2)] + "\n" + body + "\n\n" + text[m.end(2):].lstrip("\n")

t = DRAFT.read_text(encoding="utf-8")
t = splice(t, "Appendix B.", PAPER / "data" / "appendix-b-per-game.md")
t = splice(t, "Appendix C.", PAPER / "data" / "appendix-c-registry.md")
DRAFT.write_text(t, encoding="utf-8")
print("已拼入。行数:", len(t.splitlines()))
