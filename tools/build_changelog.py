"""Render CHANGELOG.md into src/changelog.html; tools/build_pages.py wraps it in the hub shell.

Run from the hub root:  python3 -I tools/build_changelog.py
src/changelog.html is generated. Edit CHANGELOG.md, then run this and build_pages.py.
Build order: build_tokens.py -> build_rulebook.py -> build_changelog.py -> build_pages.py -> check.py

CHANGELOG.md format: "## " starts an entry (the first entry is the current one), "- " is a list item,
"**Label**" alone on a line is a sub-heading, any other line is a paragraph, "---" ends the entries
and what follows it is a closing note.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MD = (ROOT / "CHANGELOG.md").read_text()


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = t.replace("brand-rules.md", '<a class="link" href="brand-rules.md">brand-rules.md</a>', 1) if "brand-rules.md" in t and "<code>" not in t else t
    return t


def entry_id(title):
    m = re.match(r"(?:unifiedmeds Brand )?Edition (\d+)", title)
    ed = f"ed{m.group(1)}" if m else "entry"
    d = re.search(r"update ([\d. to]+?\d{4})", title)
    tail = re.sub(r"[^a-z0-9]+", "-", d.group(1).lower()).strip("-") if d else ""
    word = re.search(r"\d{4} (night|evening)", title)
    return "-".join(p for p in (ed, tail, word.group(1) if word else "") if p)


def toc_label(title):
    t = re.sub(r"\s*\(.*\)$", "", title)
    t = t.replace("unifiedmeds Brand ", "").replace("Edition 03 · update ", "Update ")
    return t


head, _, rest = MD.partition("\n## ")
entries_md, _, closing = ("## " + rest).partition("\n---\n")
blocks = [b for b in re.split(r"^## ", entries_md, flags=re.M) if b.strip()]

sections, toc, ids = [], [], set()
for n, block in enumerate(blocks):
    lines = block.rstrip().splitlines()
    title = lines[0].strip().rstrip(".")
    sid = entry_id(title)
    while sid in ids:
        sid += "-b"
    ids.add(sid)
    toc.append((sid, toc_label(title)))
    status = '<span class="status status--current">Current</span>' if n == 0 else '<span class="status">Earlier</span>'
    out, in_list = [], False
    for ln in lines[1:]:
        if ln.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(ln[2:].strip())}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if not ln.strip():
            continue
        if re.fullmatch(r"\*\*[^*]+\*\*", ln.strip()):
            out.append(f'<h3 class="cl-kind">{inline(ln.strip()[2:-2])}.</h3>')
        else:
            out.append(f"<p>{inline(ln.strip())}</p>")
    if in_list:
        out.append("</ul>")
    sections.append(
        f'<section class="sec" id="{sid}" aria-labelledby="{sid}-h"><div class="sec-head">{status}'
        f'<h2 id="{sid}-h">{inline(title)}.</h2></div><div class="prose">\n' + "\n".join(out) + "\n</div></section>")

closing_html = "".join(f"<p>{inline(ln.strip())}</p>" for ln in closing.splitlines() if ln.strip())
style = """  .sec-head > .status { justify-self: start; }
  .cl-kind { margin-top: var(--space-6); font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); color: var(--color-text-strong); }
  .cl-kind:first-child { margin-top: 0; }
  .cl-end { color: var(--color-text-secondary); }
  @media (max-width: 767px) { .cl-kind { font: var(--type-mobile-card-weight, 600) var(--type-mobile-body-size) / var(--type-mobile-body-line) var(--font-family-sans); margin-top: var(--space-5); } }
"""
page = f"""<style>
{style}</style>

      <header class="page-head">
        <span class="eyebrow">Start</span>
        <h1>Changelog.</h1>
        <p class="lead">What changed and when, newest first: rules and values, pages and assets. Generated from CHANGELOG.md; earlier editions are archived.</p>
        <nav class="toc" aria-label="On this page">{"".join(f'<a href="#{s}">{html.escape(t)}</a>' for s, t in toc)}</nav>
      </header>
{chr(10).join(sections)}
<section class="sec" id="earlier" aria-label="Earlier editions"><div class="prose cl-end">{closing_html}</div></section>
"""
(ROOT / "src" / "changelog.html").write_text(page)
print("src/changelog.html:", len(sections), "entries")
