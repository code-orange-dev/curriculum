#!/usr/bin/env python3
"""Fail if any relative markdown link in the repo points at a missing file."""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
bad = []
for md in root.rglob("*.md"):
    if ".git" in md.parts:
        continue
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = target.split("#")[0]
        if path and not (md.parent / path).exists():
            bad.append(f"{md.relative_to(root)}: {target}")
print("\n".join(bad) or "all relative links resolve")
sys.exit(1 if bad else 0)
