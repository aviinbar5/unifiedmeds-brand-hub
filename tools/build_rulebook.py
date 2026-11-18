"""Render brand-rules.md into src/rulebook.html; tools/build_pages.py wraps it in the hub shell.

Run from the hub root:  python3 -I tools/build_rulebook.py
src/rulebook.html is generated. Edit brand-rules.md, then run this and build_pages.py.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MD = (ROOT / "brand-rules.md").read_text()


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"~~(.+?)~~", r"<s>\1</s>", t)
    t = re.sub(r"\*\*(To confirm\.?)\*\*", r'<span class="status status--proposed">To confirm</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = t.replace("[same]", '<span class="mark mark--same">same</span>')
    t = t.replace("[changed]", '<span class="mark mark--changed">changed</span>')
    t = t.replace("[new]", '<span class="mark mark--new">new</span>')
    return t


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


out, toc, lines, i = [], [], MD.splitlines(), 0
in_list = False
while i < len(lines):
    ln = lines[i]
    if in_list and not ln.startswith("- "):
        out.append("</ul>")
        in_list = False
    if ln.startswith("# "):
        i += 1
        continue  # page title comes from the shell
    if ln.startswith("## "):
        t = ln[3:].strip()
        m = re.match(r"(.*?)\s*\{#([a-z0-9-]+)\}$", t)  # optional explicit anchor: "## Title {#id}"
        t, sid = (m.group(1), m.group(2)) if m else (t, slug(t))
        toc.append((sid, t))
        out.append(f'</section><section class="sec" id="{sid}"><div class="sec-head"><h2>{inline(t)}.</h2></div>')
    elif ln.startswith("### "):
        out.append(f"<h3>{inline(ln[4:].strip())}</h3>")
    elif ln.startswith("- "):
        if not in_list:
            out.append('<ul class="rules">')
            in_list = True
        m = re.match(r"- \*\*([ROEUD]-\d+)\*\*", ln)
        rid = f' id="{m.group(1).lower()}"' if m else ""
        out.append(f"<li{rid}>{inline(ln[2:])}</li>")
    elif ln.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        head, body = rows[0], [r for r in rows[2:]]
        t = '<div class="table-wrap"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
        for r in body:
            rid = re.match(r"(?:~~)?([ROEUD]-\d+)", r[0])
            idattr = f' id="{rid.group(1).lower()}"' if rid else ""
            t += f"<tr{idattr}>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
        out.append(t + "</tbody></table></div>")
        continue
    elif ln.strip() == "---" or not ln.strip():
        pass
    else:
        out.append(f'<p class="prose-p">{inline(ln.strip())}</p>')
    i += 1
if in_list:
    out.append("</ul>")

body = "\n".join(out)
body = body.replace("</section>", "", 1)  # first heading opens the first section
intro = re.split(r"\n## ", MD, maxsplit=1)[0]
main = f'''      <header class="page-head">
        <span class="eyebrow">Start</span>
        <h1>Rulebook and decisions.</h1>
        <p class="lead">Every rule, decision, exception and open item of Edition 04. Generated from <a class="link" href="brand-rules.md">brand-rules.md</a>. Decided rules and tokens win; the designer's Figma is the source only for what is not decided yet (R-01).</p>
        <nav class="toc" aria-label="On this page">{"".join(f'<a href="#{s}">{html.escape(t)}</a>' for s, t in toc)}</nav>
      </header>
      <div class="rule"><p>Rule marks: <span class="mark mark--same">same</span> unchanged since Edition 02 · <span class="mark mark--changed">changed</span> rewritten for unifiedmeds · <span class="mark mark--new">new</span> added in Edition 03 or later.</p></div>
{body}
      </section>
'''
style = '''  .rules { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--space-3); }
  .rules li { padding: var(--space-4) var(--space-5); border: 1px solid var(--color-line-base); border-radius: var(--radius-small); background: var(--color-surface-card); scroll-margin-top: var(--space-6); }
  .rules li:target, tr:target { outline: var(--size-focus-width) solid var(--color-focus-ring); outline-offset: var(--size-focus-offset); }
  .prose-p { max-width: var(--layout-measure); color: var(--color-text-secondary); }
  .sec h3 { font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); color: var(--color-text-strong); margin-top: var(--space-4); }
  .mark { display: inline-flex; align-items: center; padding: 0 var(--space-2); border-radius: var(--radius-pill); font: var(--type-desktop-label-weight) var(--type-desktop-label-size) / var(--type-desktop-label-line) var(--font-family-sans); vertical-align: middle; }
  .mark--same { background: var(--color-surface-mist); color: var(--color-text-secondary-on-mist); }
  .mark--changed { background: var(--color-surface-wash-yellow); color: var(--color-brand-teal-deep); }
  .mark--new { background: var(--color-surface-wash-green); color: var(--color-brand-teal-deep); }
'''

(ROOT / "src" / "rulebook.html").write_text("<style>\n" + style + "</style>\n" + main)
print("src/rulebook.html:", len(toc), "sections")
