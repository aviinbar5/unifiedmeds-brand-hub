"""Writes assets/governance/pre-publish-checklist.md from the one coded checklist on src/how-we-work.html.

The page is the source (between the <!-- checklist:start --> and <!-- checklist:end --> markers).
Run from the hub root after an edit to the checklist, then build the pages:
    python3 -I assets/governance/build_checklist.py
    python3 -I tools/build_pages.py
Python 3 standard library only.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "src" / "how-we-work.html"
OUT = ROOT / "assets" / "governance" / "pre-publish-checklist.md"


def plain(fragment):
    text = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def main():
    page = SRC.read_text()
    block = page.split("<!-- checklist:start", 1)[1].split("<!-- checklist:end -->", 1)[0]
    blocks = re.findall(r'<article class="card[^"]*" data-block="([^"]+)"><h3>(.*?)</h3><ol>(.*?)</ol></article>', block, flags=re.S)
    if not blocks:
        raise SystemExit("no checklist blocks found in src/how-we-work.html")
    lines = [
        "# unifiedmeds · Pre-publish checklist",
        "",
        "Brand Edition 04 · generated from How we work (how-we-work.html#checklist) by assets/governance/build_checklist.py; edit the page, never this file.",
        "",
        "Run it on the exact file that ships. Write the codes you checked in the approval log. Every page and screen is checked at 1440 and 390 wide at least; website builds also at 768 and 1024 (R-27, R-107). The Dev block applies to website and product builds only.",
        "",
        "File: ______________________________  Version: v__  Date: __________  Checked by: __________",
        "",
    ]
    ranges = []
    for key, title, items in blocks:
        rows = re.findall(r"<li><code>([^<]+)</code><span>(.*?)</span></li>", items, flags=re.S)
        lines.append(f"## {plain(title)}")
        lines += [f"- [ ] {code} {plain(text)}" for code, text in rows]
        lines.append("")
        ranges.append(f"{rows[0][0]} to {rows[-1][0]}")
    lines += [
        "## Sign-off",
        "| Step | Name | Date | Result |",
        "|---|---|---|---|",
        "| Brand check | | | |",
        "| Clinical (if medical content) | | | |",
        "| Legal | | | |",
        "| Final sign-off (Brand) | | | |",
        "",
        "Codes in this checklist: " + ", ".join(ranges) + ".",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.relative_to(ROOT)} · {len(blocks)} blocks · " + ", ".join(ranges))


if __name__ == "__main__":
    main()
