#!/usr/bin/env python3
"""Write index.html for the slides site (see .github/workflows/slides.yml).

    python3 tools/build_slides_site.py site

Expects site/week-NN.html and site/week-NN.pdf, made by Marp. Titles come from each
week's README, so the page stays in sync with the syllabus.
"""
import html
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
out = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
repo = "https://github.com/code-orange-dev/curriculum/tree/main/decoding-bitcoin"

rows = []
for readme in sorted((root / "decoding-bitcoin").glob("week-*/README.md")):
    week = readme.parent.name
    first = readme.read_text(encoding="utf-8").splitlines()[0]
    title = re.sub(r"^#\s*Week \d+:\s*", "", first).strip()
    n = int(week.split("-")[1])
    rows.append(f"""<li><span class="n">{n:02d}</span><span class="t">{html.escape(title)}</span>
<span class="l"><a href="{week}.html">Slides</a> <a href="{week}.pdf">PDF</a> <a href="{repo}/{week}">Study guide</a></span></li>""")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Decoding Bitcoin slides</title>
<style>
:root{{--bg:#0b0b0b;--fg:#ececec;--dim:#9a9a9a;--o:#f7931a;--line:#262626}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:760px;margin:0 auto;padding:40px 16px 64px}}h1{{margin:0 0 6px;font-size:28px}}h1 b{{color:var(--o)}}
p{{color:var(--dim);margin:0 0 28px}}a{{color:var(--o)}}ul{{list-style:none;padding:0;margin:0}}
li{{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline;padding:14px 0;border-top:1px solid var(--line)}}
.n{{color:var(--o);font-weight:700;font-variant-numeric:tabular-nums}}.t{{flex:1 1 260px}}.l a{{margin-right:12px;text-decoration:none}}.l a:hover{{text-decoration:underline}}
footer{{margin-top:32px;color:var(--dim);font-size:14px}}
</style></head><body><main>
<h1><b>Decoding Bitcoin</b> facilitator slides</h1>
<p>One deck per week of the 10-week cohort by <a href="https://codeorange.dev/decoding-bitcoin">Code Orange Dev School</a>.
Lessons are on <a href="https://bitcoindevs.xyz/decoding">Decoding Bitcoin</a> by The Bitcoin Dev Project. Press P in a deck for speaker notes.</p>
<ul>
{chr(10).join(rows)}
</ul>
<footer>CC0, public domain. Source and improvements: <a href="https://github.com/code-orange-dev/curriculum">github.com/code-orange-dev/curriculum</a></footer>
</main></body></html>
"""
out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(page, encoding="utf-8")
missing = [w for w in (f"week-{i:02d}" for i in range(1, len(rows) + 1)) if not (out / f"{w}.html").exists()]
print(f"index.html: {len(rows)} weeks" + (f" (missing decks: {', '.join(missing)})" if missing else ""))
