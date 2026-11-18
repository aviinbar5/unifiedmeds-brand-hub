"""Brand check for the unifiedmeds Brand Hub (Edition 04). Run from the hub root:  python3 -I tools/check.py

Checks, on every page (root pages and lp/) outside archive/:
  1. No colour literal (#hex, rgb(), hsl()) in <style> blocks, style="" attributes or .css files, except brand.css (generated).
  2. Every local link, image, stylesheet and script exists.
  3. No former brand name anywhere in the site (U-16, U-31): every text file outside archive/ is scanned,
     pages, landing pages, scripts, styles, tokens, Markdown, SVG and the tools, URLs included. There is no allow-list.
  4. Fonts: only DM Serif Display and Inter are loaded.
Prints each problem and exits 1 if there is any.
"""
import pathlib
import re
import sys
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")
OLD_NAME = re.compile("sov" + r"i[\s_.-]?care", re.I)  # built in two parts so this file never names it
TEXT = {".html", ".md", ".js", ".json", ".css", ".svg", ".txt", ".py", ".csv", ".xml"}
problems = []
pages = [p for p in ROOT.glob("*.html")] + list((ROOT / "lp").glob("*.html"))
for css in [p for p in ROOT.glob("*.css") if p.name != "brand.css"]:
    for n, line in enumerate(css.read_text().splitlines(), 1):
        if COLOUR.search(re.sub(r"/\*.*?\*/", "", line)):
            problems.append(f"{css.name}:{n} colour literal: {line.strip()[:80]}")
for page in pages:
    text = page.read_text()
    for block in re.findall(r"<style>(.*?)</style>", text, flags=re.S):
        for line in block.splitlines():
            if COLOUR.search(re.sub(r"/\*.*?\*/", "", line)):
                problems.append(f"{page.name} <style> colour literal: {line.strip()[:80]}")
    for attr in re.findall(r'style="([^"]*)"', text):
        if COLOUR.search(attr):
            problems.append(f"{page.name} style attribute colour literal: {attr[:80]}")
    for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
        u = urlsplit(ref)
        if u.scheme or ref.startswith(("#", "mailto:")):
            continue
        target = (page.parent / u.path).resolve()
        if u.path and not target.exists():
            problems.append(f"{page.name} broken link: {ref}")
    for fam in re.findall(r"fonts\.googleapis\.com/css2\?([^\"]+)", text):
        names = re.findall(r"family=([^:&]+)", fam)
        if any(n not in ("DM+Serif+Display", "Inter") for n in names):
            problems.append(f"{page.name} unexpected font: {names}")
for f in sorted(ROOT.rglob("*")):
    rel = f.relative_to(ROOT)
    if not f.is_file() or rel.parts[0] in ("archive", ".git") or f.suffix.lower() not in TEXT:
        continue
    if OLD_NAME.search(str(rel)):
        problems.append(f"{rel} former brand name in the file path")
    try:
        lines = f.read_text().splitlines()
    except UnicodeDecodeError:
        continue
    for n, line in enumerate(lines, 1):
        m = OLD_NAME.search(line)
        if m:
            problems.append(f"{rel}:{n} former brand name: …{line[max(0, m.start() - 60): m.end() + 60].strip()}…")
for p in problems:
    print(p)
print(f"{len(problems)} problems in {len(pages)} pages")
sys.exit(1 if problems else 0)
