"""Brand check for the unifiedmeds Brand Hub (Edition 03). Run from the hub root:  python3 -I tools/check.py

Checks, on every page outside archive/:
  1. No colour literal (#hex, rgb(), hsl()) in <style> blocks, style="" attributes or .css files, except brand.css (generated).
  2. Every local link, image, stylesheet and script exists.
  3. No old brand name outside the archive and the history notes.
  4. Fonts: only DM Serif Display and Inter are loaded.
Prints each problem and exits 1 if there is any.
"""
import pathlib
import re
import sys
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")
OLD_NAME_OK = ("SoviCare editions", "SoviCare Edition", "SoviCare Brand Edition", "from SoviCare", "written for SoviCare",
               "SoviCare and SoviCare LLC", "Earlier SoviCare", "SoviCare Trio\" becomes", "\"SoviCare Trio\" or", "Never “Trio”, “SoviCare Trio”",
               "Unifiedmeds · UnifiedMeds · Unified Meds · UNIFIEDMEDS · SoviCare", "(October, SoviCare)", "replaces the SoviCare", "SoviCare quadrant symbol",
               "the old SoviCare", "SoviCare - Website", "SoviCare LLC", "SoviCare to unifiedmeds", "SoviCare Edition 02",
               "unifiedmeds and SoviCare brand edition", "sovicare-edition-02", "Pastel palette; wordmark", "\"SoviCare Trio\" is retired", "project \"SoviCare Homepage")
problems = []
pages = [p for p in ROOT.glob("*.html")]
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
    plain = re.sub(r"https?://[^\"\s<]+", "", text)
    for m in re.finditer(r"[Ss]ovi[Cc]are|SOVICARE", plain):
        ctx = plain[max(0, m.start() - 70): m.end() + 70]
        if not any(ok in ctx for ok in OLD_NAME_OK):
            problems.append(f"{page.name} old brand name: …{ctx.strip()[:120]}…")
    for fam in re.findall(r"fonts\.googleapis\.com/css2\?([^\"]+)", text):
        names = re.findall(r"family=([^:&]+)", fam)
        if any(n not in ("DM+Serif+Display", "Inter") for n in names):
            problems.append(f"{page.name} unexpected font: {names}")
for p in problems:
    print(p)
print(f"{len(problems)} problems in {len(pages)} pages")
sys.exit(1 if problems else 0)
