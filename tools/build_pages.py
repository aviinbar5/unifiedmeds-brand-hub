"""Build every hub page from src/<page>.html into the one shared shell (unifiedmeds Brand Hub, one site).

Run from the hub root:  python3 -I tools/build_pages.py
Order of the full build: build_tokens.py -> build_rulebook.py -> build_changelog.py -> build_pages.py -> check.py

- PAGES and NAV below are the single source of the menu, page titles, statuses and search keywords.
- The edition stamp is read from the first "## " entry of CHANGELOG.md.
- Writes search-index.js (pages, sections, rules, colours, files) for the search dialog in hub.js.
- REDIRECTS writes small pages for old addresses that now live elsewhere.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
EDITION = "Brand Edition 04"

# file: (menu label, <title>, description, status, Hebrew search words)
PAGES = {
    "index.html": ("Overview", "Overview", "Every unifiedmeds rule, value, asset and output in one place.", "current", "בית סקירה התחלה מבוא"),
    "rulebook.html": ("Rulebook and decisions", "Rulebook", "Every rule, decision, exception and open item, generated from brand-rules.md.", "current", "חוקים כללים החלטות חריגים פריטים פתוחים רולבוק"),
    "changelog.html": ("Changelog", "Changelog", "What changed and when: rules and values, pages and assets.", "current", "שינויים היסטוריה עדכונים יומן"),
    "how-we-work.html": ("How we work", "How we work", "Who decides, how a change travels, the pre-publish checklist, file naming and the archive.", "current", "תהליך אישורים מאשרים שמות קבצים ארכיון רשימת בדיקה סמכות"),
    "brand.html": ("Brand", "Brand", "Who unifiedmeds is: the idea, positioning, personality, principles, personas and the line bank.", "current", "מותג רעיון מיצוב אופי עקרונות פרסונות קהל משפטים סלוגן טאגליין"),
    "brand-architecture.html": ("Architecture and naming", "Brand architecture and naming", "Master brand, categories, products and plans, and how every name is written.", "current", "ארכיטקטורה שמות מוצרים קטגוריות תוכניות"),
    "logo-story.html": ("The logo story", "The logo story", "The brand behind the capsule seal: the brief, the directions and the choice.", "current", "סיפור הלוגו רעיון קפסולה חותם"),
    "logo.html": ("Logo in use", "Logo in use", "Lockups, colours, clear space, minimum sizes, do and don't, and the files.", "current", "לוגו סמל חותם שימוש גדלים קבצים הורדה מותר אסור"),
    "content.html": ("Voice and compliance", "Voice, content and compliance", "How unifiedmeds writes: wording rules, microcopy, required lines, compliance and privacy.", "current", "ניסוח קול טון מיקרוקופי טקסטים ציות פרטיות שורות חובה מילון"),
    "brand-in-use.html": ("Brand in use", "Brand in use", "The brand applied: right and wrong, side by side.", "current", "נכון לא נכון דוגמאות שימוש"),
    "foundations.html": ("Foundations", "Foundations", "Colour, contrast, type, layout, radius and elevation, from the token file.", "current", "צבעים צבע ניגודיות טיפוגרפיה פונט גופן גריד ריווח רדיוס צל טוקנים"),
    "icons.html": ("Icons", "Icons", "Feature icons, UI glyphs and the capsule icon family, with sizes, colours and downloads.", "current", "אייקונים סמלים"),
    "components.html": ("Components", "Components", "Buttons, fields, cards, header, footer, states and interactions.", "current", "רכיבים כפתורים שדות טפסים כרטיסים כותרת תפריט פוטר מצבים"),
    "motion.html": ("Motion", "Motion", "Motion principles, tokens, the motion set, logo motion and interactive patterns.", "current", "תנועה אנימציה אנימציות מעברים"),
    "images.html": ("Imagery", "Imagery", "Photography: casting, light, ratios, shapes on photos, copy on photos and placeholders.", "current", "תמונות צילום צילומים ליהוק"),
    "illustration.html": ("Illustration and patterns", "Illustration and patterns", "Spot illustrations and background patterns built from the capsule.", "proposed", "איורים איור דפוסים רקעים"),
    "sound.html": ("Sound", "Sonic branding", "The sting sound, product sounds and sound in videos.", "proposed", "סאונד צליל קול מוזיקה"),
    "website-pages.html": ("Website pages", "Website pages", "Every website page designed in Figma, launch and Phase 2.", "current", "עמודי אתר אתר"),
    "section-library.html": ("Home section library", "Home section library", "The sections of the homepage, top to bottom.", "current", "סקשנים עמוד בית ספריה"),
    "templates.html": ("Templates", "Templates", "Category page, product page, page spec and image slots.", "current", "תבניות מפרט עמוד צבעי מוצר צבעי קטגוריה"),
    "landing-pages.html": ("Landing pages", "Landing pages", "The Sexual health landing page and the LP 01 concepts.", "current", "דף נחיתה דפי נחיתה"),
    "assessment.html": ("Assessment", "Assessment", "The online assessment: patterns, flow, screens, states, validation and build rules.", "current", "שאלון שאלות הערכה ולידציה"),
    "product-screens.html": ("Product screens", "Product screens", "Funnel, member portal, clinical admin and support.", "current", "מסכי מוצר פורטל משפך תשלום אדמין תמיכה"),
    "data-viz.html": ("Data in the portal", "Data visualisation", "Charts and numbers in the member portal.", "current", "גרפים נתונים דאטה"),
    "emails.html": ("System emails", "System emails", "Order, provider reply, shipping and refill emails.", "current", "מיילים אימייל דוא\"ל"),
    "packaging.html": ("Packaging", "Packaging", "Labels, bottles and the capsule kit.", "current", "אריזה תווית תוויות בקבוק"),
    "unboxing.html": ("Box and unboxing", "Box and unboxing", "What is inside the box, the printed pieces and the unboxing.", "current", "קופסה מעטפה פתיחה"),
    "social.html": ("Social", "Social", "Shared social rules, every size and the channel kits.", "current", "רשתות חברתיות סושיאל פוסטים"),
    "social-facebook.html": ("Facebook", "Facebook kit", "Profile, cover, posts, stories and ads.", "current", "פייסבוק"),
    "social-instagram.html": ("Instagram and Threads", "Instagram and Threads kit", "Profile, grid, posts, carousels, stories and reels.", "current", "אינסטגרם"),
    "social-tiktok.html": ("TikTok", "TikTok kit", "Profile, video covers, safe zones and captions.", "current", "טיקטוק"),
    "social-youtube.html": ("YouTube", "YouTube kit", "Channel art, thumbnails, Shorts and end screens.", "current", "יוטיוב"),
    "social-linkedin.html": ("LinkedIn", "LinkedIn kit", "Company page, posts, documents and careers.", "current", "לינקדאין"),
    "social-x.html": ("X", "X kit", "Profile, header, posts and cards.", "current", "טוויטר"),
    "ads.html": ("Ads", "Ads", "Paid rules and ad templates by channel.", "current", "מודעות פרסום ממומן"),
    "newsletter.html": ("Newsletter", "Newsletter", "Consent, discretion and the newsletter templates.", "current", "ניוזלטר דיוור"),
    "videos.html": ("Videos", "Videos", "The logo stings and the brand film.", "current", "וידאו סרטונים סרטון סטינג סרט"),
    "media-kit.html": ("Media kit", "Media kit", "For the press: who we are, fact sheet, logo pack and contact.", "current", "ערכת עיתונות עיתונאים יחסי ציבור"),
    "handoff.html": ("Developer handoff", "Developer handoff", "What developers build from, page scope, tokens and the release checklist.", "current", "מפתח מסירה פיתוח קוד"),
    "downloads.html": ("Downloads and Figma", "Downloads and Figma files", "Every file to download, and the Figma files.", "current", "הורדות קבצים פיגמה הורדה"),
}
NAV = [
    ("Start", "The hub, its rules and how we work", ["index.html", "rulebook.html", "changelog.html", "how-we-work.html"]),
    ("Brand", "Who we are, the name, the logo and the voice", ["brand.html", "brand-architecture.html", "logo-story.html", "logo.html", "content.html", "brand-in-use.html"]),
    ("System", "The visual building blocks", ["foundations.html", "icons.html", "components.html", "motion.html", "images.html", "illustration.html", "sound.html"]),
    ("Website", "Pages, sections and templates", ["website-pages.html", "section-library.html", "templates.html", "landing-pages.html"]),
    ("Care journey", "From the assessment to the box", ["assessment.html", "product-screens.html", "data-viz.html", "emails.html", "packaging.html", "unboxing.html"]),
    ("Marketing", "Social, ads, video and press", ["social.html", "ads.html", "newsletter.html", "videos.html", "media-kit.html"]),
    ("Build", "For developers", ["handoff.html", "downloads.html"]),
]
CHILDREN = {"social.html": ["social-facebook.html", "social-instagram.html", "social-tiktok.html", "social-youtube.html", "social-linkedin.html", "social-x.html"]}
REDIRECTS = {"brand-book.html": "brand.html", "animations.html": "motion.html", "questionnaire.html": "assessment.html", "governance.html": "how-we-work.html"}

ORDER = [p for _, _, items in NAV for it in items for p in [it] + CHILDREN.get(it, [])]
GROUP_OF = {p: g for g, _, items in NAV for it in items for p in [it] + CHILDREN.get(it, [])}
missing = [p for p in PAGES if p not in ORDER] + [p for p in ORDER if p not in PAGES]
assert not missing, missing

top = (ROOT / "CHANGELOG.md").read_text().split("\n## ", 2)[1].splitlines()[0]
m = re.search(r"(\d{1,2}\.\d{1,2}\.\d{4})", top)
UPDATED = m.group(1) if m else ""
STAMP = f"{EDITION} · updated {UPDATED}" if UPDATED else EDITION
e = html.escape

SEARCH_SVG = '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><circle cx="8.75" cy="8.75" r="5.25"/><path d="M12.75 12.75L16.5 16.5"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8l4 4 4-4"/></svg>'


def link(p, page, cls=""):
    label = PAGES[p][0]
    cur = ' aria-current="page"' if p == page else ""
    dot = '<i class="nav-dot" title="Proposed"></i>' if PAGES[p][3] == "proposed" else ""
    return f'<a class="{cls}" href="{p}"{cur}>{e(label)}{dot}</a>' if cls else f'<a href="{p}"{cur}>{e(label)}{dot}</a>'


def nav(page):
    groups = []
    for name, desc, items in NAV:
        here = GROUP_OF.get(page) == name
        links = ""
        for it in items:
            links += link(it, page)
            kids = CHILDREN.get(it)
            if kids:
                links += '<div class="hub-sub">' + "".join(link(k, page) for k in kids) + "</div>"
        gid = re.sub(r"[^a-z]+", "-", name.lower())
        groups.append(f'<details class="hub-group" data-group="{gid}"{" open" if here else ""}><summary><span>{e(name)}</span><small>{e(desc)}</small>{CHEV}</summary><div class="hub-links">{links}</div></details>')
    return "".join(groups)


def pager(page):
    i = ORDER.index(page)
    prev = ORDER[i - 1] if i > 0 else None
    nxt = ORDER[i + 1] if i + 1 < len(ORDER) else None
    out = '<nav class="pager" aria-label="Previous and next page">'
    out += f'<a class="pager-prev" href="{prev}"><small>Previous</small><b>{e(PAGES[prev][0])}</b></a>' if prev else "<span></span>"
    out += f'<a class="pager-next" href="{nxt}"><small>Next</small><b>{e(PAGES[nxt][0])}</b></a>' if nxt else "<span></span>"
    return out + "</nav>"


def overview_cards():
    out = []
    for name, desc, items in NAV:
        cards = "".join(
            f'<a class="ov-card" href="{p}"><b>{e(PAGES[p][0])}</b><span>{e(PAGES[p][2])}</span>'
            + ('<em class="status status--proposed">Proposed</em>' if PAGES[p][3] == "proposed" else "") + "</a>"
            for it in items for p in [it] + CHILDREN.get(it, []) if p != "index.html")
        out.append(f'<section class="sec ov-group" aria-labelledby="ov-{name.lower().replace(" ", "-")}"><div class="sec-head"><h2 id="ov-{name.lower().replace(" ", "-")}">{e(name)}.</h2><p>{e(desc)}.</p></div><div class="ov-grid">{cards}</div></section>')
    return "\n".join(out)


def latest():
    md = (ROOT / "CHANGELOG.md").read_text()
    out = []
    for block in md.split("\n## ")[1:4]:
        lines = block.splitlines()
        items = "".join(f"<li>{e(re.sub(r'`([^`]+)`', r'\\1', l[2:]))}</li>" for l in lines[1:] if l.startswith("- "))
        out.append(f"<article><b>{e(lines[0])}</b><ul>{items}</ul></article>")
    return "".join(out)


def shell(page, style, body):
    label, title, desc, status, _ = PAGES[page]
    group = GROUP_OF[page]
    crumbs = "" if page == "index.html" else f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Hub</a><span aria-hidden="true">/</span><span>{e(group)}</span><span aria-hidden="true">/</span><span aria-current="page">{e(label)}</span></nav>'
    logo = '<a class="hub-brand" href="index.html"><img src="assets/brand/logo-horizontal.svg" width="185" height="30" alt="unifiedmeds Brand Hub, home"></a>'
    search_btn = f'<button class="hub-search-btn" type="button" data-search-open aria-haspopup="dialog">{SEARCH_SVG}<span>Search the hub</span><kbd>⌘K</kbd></button>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · unifiedmeds Brand Hub</title>
<meta name="description" content="{e(desc)}">
<!-- Generated by tools/build_pages.py from src/{page}. Edit the source, then run the build. -->
<link rel="icon" href="assets/brand/app-icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="brand.css">
<link rel="stylesheet" href="components.css">
<link rel="stylesheet" href="hub.css">
<link rel="stylesheet" href="extended.css">
<style>
{style}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="hub">
  <header class="hub-top">
    {logo}
    <button class="hub-icon-btn" type="button" data-search-open aria-haspopup="dialog" aria-label="Search the hub">{SEARCH_SVG}</button>
    <button class="hub-toggle" type="button" aria-expanded="false" aria-controls="hub-nav" aria-label="Open the hub menu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
  </header>
  <nav class="hub-nav" id="hub-nav" aria-label="Brand hub">
    {logo}
    <span class="hub-edition">{e(STAMP)}</span>
    {search_btn}
    {nav(page)}
    <p class="hub-nav-foot">Decided rules and tokens win. Figma follows them.</p>
  </nav>
  <main class="hub-main" id="main">
    <div class="page">
      {crumbs}
{body}
      {pager(page)}
      <footer class="page-foot cap"><span>unifiedmeds Brand Hub · {e(STAMP)}</span><span>Source: src/{page}</span></footer>
    </div>
  </main>
</div>
<dialog class="hub-search" aria-label="Search the hub">
  <div class="hub-search-box">{SEARCH_SVG}<input type="search" dir="auto" placeholder="Search pages, rules, colours, files…" aria-label="Search" autocomplete="off" spellcheck="false"><button type="button" class="hub-search-close" aria-label="Close search">Esc</button></div>
  <p class="hub-search-hint">Type a page, a rule (R-42), a colour (Deep Teal or #264653), a file or a word in Hebrew.</p>
  <ul class="hub-search-list" role="listbox" aria-label="Results"></ul>
</dialog>
<script src="search-index.js" defer></script>
<script src="hub.js" defer></script>
</body>
</html>
"""


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


index = []
built = 0
for page in ORDER:
    src = ROOT / "src" / page
    if not src.exists():
        print("MISSING src", page)
        continue
    text = src.read_text()
    m = re.match(r"\s*<style>(.*?)</style>\s*(.*)", text, flags=re.S)
    style, body = (m.group(1), m.group(2)) if m else ("", text)
    body = body.replace("<!--PAGE-CARDS-->", overview_cards()).replace("<!--LATEST-->", latest())
    (ROOT / page).write_text(shell(page, style, body))
    built += 1
    label, title, desc, status, he = PAGES[page]
    index.append({"t": label, "d": desc, "u": page, "k": "page", "g": GROUP_OF[page], "h": he})
    seen = set()
    for tag, hid, inner in re.findall(r'<(h2|h3)[^>]*\bid="([^"]+)"[^>]*>(.*?)</\1>', body, flags=re.S):
        t = strip_tags(inner).rstrip(".")
        if t and hid not in seen:
            seen.add(hid)
            index.append({"t": t, "d": label, "u": f"{page}#{hid}", "k": "section", "g": GROUP_OF[page]})
    for sid, inner in re.findall(r'<section[^>]*\bid="([^"]+)"[^>]*>\s*(?:<div class="sec-head">)?\s*<h2(?![^>]*\bid=)[^>]*>(.*?)</h2>', body, flags=re.S):
        t = strip_tags(inner).rstrip(".")
        if t and sid not in seen:
            seen.add(sid)
            index.append({"t": t, "d": label, "u": f"{page}#{sid}", "k": "section", "g": GROUP_OF[page]})

# rules, decisions, exceptions, open items
md = (ROOT / "brand-rules.md").read_text()
for line in md.splitlines():
    r = re.match(r"- \*\*([RE]-\d+)\*\*\s*(?:\[\w+\])?\s*(.*)", line)
    if r:
        index.append({"t": r.group(1), "d": strip_tags(r.group(2))[:150], "u": f"rulebook.html#{r.group(1).lower()}", "k": "rule"})
        continue
    r = re.match(r"\|\s*(?:~~)?([UOE]-\d+)(?:~~)?\s*\|\s*([^|]*)\|", line)
    if r:
        index.append({"t": r.group(1), "d": strip_tags(r.group(2).replace("~~", ""))[:150], "u": f"rulebook.html#{r.group(1).lower()}", "k": "decision" if r.group(1)[0] == "U" else "rule"})
# colours
tokens = json.loads((ROOT / "tokens" / "tokens.json").read_text())
for grp, vals in tokens.get("color", {}).items():
    if not isinstance(vals, dict):
        continue
    for name, v in vals.items():
        if isinstance(v, dict) and "$value" in v:
            index.append({"t": f"{name.replace('-', ' ').title()} {v['$value']}", "d": f"Colour · {grp} · " + str(v.get("$description", ""))[:110], "u": "foundations.html#color", "k": "colour"})
# downloadable files
for folder in ("brand", "icons", "icons-capsule", "shapes", "patterns", "sound", "video", "media-kit", "packaging"):
    base = ROOT / "assets" / folder
    if not base.exists():
        continue
    for f in sorted(base.rglob("*")):
        if f.is_file() and f.suffix.lower() in (".svg", ".png", ".mp4", ".wav", ".zip", ".pdf", ".jpg"):
            rel = f.relative_to(ROOT).as_posix()
            if "/preview/" in rel or "/build/" in rel:
                continue
            index.append({"t": f.name, "d": f"File · assets/{folder}", "u": rel, "k": "file"})
(ROOT / "search-index.js").write_text("window.HUB_INDEX = " + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";\n")

for old, new in REDIRECTS.items():
    (ROOT / old).write_text(f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>Moved · unifiedmeds Brand Hub</title><meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{new}"></head><body><p>This page moved to <a href="{new}">{e(PAGES[new][0])}</a>.</p></body></html>\n')
print(f"built {built} pages, {len(index)} search entries, {len(REDIRECTS)} redirects · {STAMP}")
