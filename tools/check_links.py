#!/usr/bin/env python3
"""Fail if any relative markdown link points at a missing file or a missing #heading.

    python3 tools/check_links.py

Checks links like [x](../week-02/), [x](notes/README.md) and [x](../README.md#week-2-...).
Heading anchors follow GitHub's rules: lowercase, punctuation dropped, spaces become dashes,
and repeated headings get -1, -2, ... Links inside code blocks are ignored.
External (http) links are not fetched.
"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def strip_code(text):
    text = FENCE.sub("", text)
    return re.sub(r"`[^`\n]*`", "", text)


def anchors(md):
    seen, out = {}, set()
    for line in strip_code(md.read_text(encoding="utf-8")).splitlines():
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1))  # [text](url) -> text
        text = re.sub(r"<[^>]+>", "", text).replace("`", "")
        slug = re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        out.add(slug if n == 0 else f"{slug}-{n}")
    for m in re.finditer(r'<a\s+(?:name|id)="([^"]+)"', md.read_text(encoding="utf-8")):
        out.add(m.group(1))
    return out


cache, bad, checked = {}, [], 0
for md in sorted(root.rglob("*.md")):
    if ".git" in md.parts:
        continue
    for target in LINK.findall(strip_code(md.read_text(encoding="utf-8"))):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        checked += 1
        path, _, anchor = target.partition("#")
        dest = (md.parent / path) if path else md
        if not dest.exists():
            bad.append(f"{md.relative_to(root)}: {target}  (missing file)")
            continue
        if anchor:
            if dest.is_dir():
                dest = dest / "README.md"
            if dest.suffix != ".md" or not dest.exists():
                continue
            if dest not in cache:
                cache[dest] = anchors(dest)
            if anchor not in cache[dest]:
                bad.append(f"{md.relative_to(root)}: {target}  (no heading #{anchor})")
print("\n".join(bad) or f"all {checked} relative links resolve")
sys.exit(1 if bad else 0)
