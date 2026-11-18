"""Build src/product-screens.html (unifiedmeds Brand Hub, product screens).

Run from the hub root:
    python3 -B -I assets/product-screens/page.py      # -B: no __pycache__ in the hub
    python3 -I tools/build_pages.py

Every capsule comes from tools/capsule_svg.py (R-105, R-109: the logo's proportions, with the divider).
UI glyphs are inlined from assets/icons/ui/ (the UI set on the Icons page).
The page CSS lives in assets/product-screens/ps_style.css (tokens only, ps- prefix).
Screen content is in screens_*.py next to this file. All data is DEMO.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))
import capsule_svg as cs  # noqa: E402

CORE = ""
LOGO_H = CORE + "assets/brand/logo-horizontal.svg"
LOGO_H_REV = CORE + "assets/brand/logo-horizontal-reversed.svg"
LOGO_SEAL = CORE + "assets/brand/logo-seal.svg"
APP_ICON = CORE + "assets/brand/app-icon.svg"
BOTTLE = {"tad": "assets/packaging/bottle-tadalafil.png", "sil": "assets/packaging/bottle-sildenafil.png", "com": "assets/packaging/bottle-combo.png"}
PNAME = {"tad": "Tadalafil", "sil": "Sildenafil", "com": "Combo"}
TOKENS_HEX = {"deep": "#264653", "tad": "#9CC9E3", "sil": "#F4A38C", "com": "#82CFCB"}  # tokens.json, for standalone SVG files only

# ---------------------------------------------------------------- glyphs
_ICONS = {}


def ic(name, cls="ps-ic"):
    if name not in _ICONS:
        raw = (ROOT / "assets" / "icons" / "ui" / f"{name}.svg").read_text()
        inner = re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S).group(1).strip()
        _ICONS[name] = inner
    return (f'<svg class="{cls}" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_ICONS[name]}</svg>')


CHECK = ('<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M4 10.5L8 14.5L16 5.5"/></svg>')


# ---------------------------------------------------------------- capsules (tools/capsule_svg.py)
def _mark_geometry(length=28.0):
    sw = cs.stroke_for(length)          # 1.5 at this size (R-109 minimum)
    pad = sw / 2
    inner = length - sw
    ld, rd, (bw, bh) = cs.capsule_paths(pad, pad, inner)
    fill, _, _ = cs.capsule_paths(pad, pad, inner, inset=sw * 1.5)
    return ld, rd, fill, bw + sw, bh + sw, sw


def mark(p, cls=""):
    """Product mark: the brand capsule outlined in Deep Teal, its long half filled with the product colour."""
    ld, rd, fill, W, H, sw = _mark_geometry()
    return (f'<svg class="ps-mk ps-mk--{p} {cls}" viewBox="0 0 {cs.f(W)} {cs.f(H)}" aria-hidden="true">'
            f'<path class="f" d="{fill}"/><path class="o" d="{ld}" stroke-width="{cs.f(sw)}" vector-effect="non-scaling-stroke"/>'
            f'<path class="o" d="{rd}" stroke-width="{cs.f(sw)}" vector-effect="non-scaling-stroke"/></svg>')


def loader(label="Loading"):
    """The core capsule loader (components.css .cap-loader), geometry from capsule_paths: length 60 in a 64 x 25.5 box."""
    ld, rd, _ = cs.capsule_paths(2, 2, 60)
    lf, _, _ = cs.capsule_paths(2, 2, 60, inset=0.72)
    return (f'<svg class="cap-loader" viewBox="0 0 64 24.47" role="img" aria-label="{label}">'
            '<path class="cap-loader-fill" d="M33.11 3.94L11.49 3.94A8.29 8.29 0 0 0 11.49 20.53L33.11 20.53ZM37.11 3.2L51.76 3.2A9.04 9.04 0 0 1 51.76 21.27L37.11 21.27Z"/><path class="cap-loader-line" d="M35.11 1.94L11.49 1.94A10.29 10.29 0 0 0 11.49 22.53L35.11 22.53"/><path class="cap-loader-line" d="M35.11 1.2L51.76 1.2A11.04 11.04 0 0 1 51.76 23.27L35.11 23.27Z"/></svg>')  # the one loader drawing (components.html): fill inset, gap at the divider (R-109)


def write_assets():
    """Standalone SVG files for the developer (hex values from tokens.json only)."""
    ld, rd, fill, W, H, sw = _mark_geometry()
    for p in ("tad", "sil", "com"):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{cs.f(W)}" height="{cs.f(H)}" viewBox="0 0 {cs.f(W)} {cs.f(H)}" fill="none">\n'
               f'<path d="{fill}" fill="{TOKENS_HEX[p]}"/>\n<path d="{ld}" stroke="{TOKENS_HEX["deep"]}" stroke-width="{cs.f(sw)}"/>\n'
               f'<path d="{rd}" stroke="{TOKENS_HEX["deep"]}" stroke-width="{cs.f(sw)}"/>\n</svg>\n')
        (HERE / f"mark-{PNAME[p].lower()}.svg").write_text(svg)
    ld, rd, _ = cs.capsule_paths(2, 2, 60)
    lf, _, _ = cs.capsule_paths(2, 2, 60, inset=0.72)
    d = TOKENS_HEX["deep"]
    (HERE / "cap-loader.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="72" height="28.69" viewBox="0 0 64 25.5" fill="none">\n'
        '<style>.f{transform-box:fill-box;transform-origin:left center;animation:f 1.4s cubic-bezier(0,0,.58,1) infinite}'
        '@keyframes f{0%{transform:scaleX(0)}60%,100%{transform:scaleX(1);opacity:.15}}'
        '@media (prefers-reduced-motion:reduce){.f{animation:none;transform:scaleX(.5)}}</style>\n'
        f'<path class="f" d="{lf}{rd}" fill="{d}"/>\n<path d="{ld}" stroke="{d}" stroke-width="{cs.f(cs.stroke_for(72))}"/>\n<path d="{rd}" stroke="{d}" stroke-width="{cs.f(cs.stroke_for(72))}"/>\n</svg>\n')  # R-109


# ---------------------------------------------------------------- frames
_N = [0]


def uniq(html):
    """Every frame gets its own id suffix, so desktop and mobile copies never share an id."""
    _N[0] += 1
    n = _N[0]
    html = re.sub(r'\b(id|for)="([^"]+)"', lambda m: f'{m.group(1)}="{m.group(2)}-{n}"', html)
    html = re.sub(r'\b(aria-labelledby|aria-describedby|aria-controls)="([^"]+)"',
                  lambda m: f'{m.group(1)}="' + " ".join(f"{x}-{n}" for x in m.group(2).split()) + '"', html)
    html = re.sub(r'href="#([a-z][^"]*)"', lambda m: f'href="#{m.group(1)}-{n}"', html)
    return html


def browser(url, inner, cap, extra_cls=""):
    inner = uniq(inner)
    return (f'<figure class="ps-shot"><div class="ps-browser"><div class="ps-bar"><span class="ps-dots" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="ps-url">{url}</span><span class="ps-demo">DEMO data</span></div>'
            f'<div class="ps-vp" data-w="1440"><div class="ps-cv {extra_cls}">{inner}</div></div></div>'
            f'<figcaption><b>Desktop · 1440.</b> {cap}</figcaption></figure>')


def phone(inner, cap, statusbar=True, dark_status=False):
    inner = uniq(inner)
    sb = ('<div class="ps-row ps-between" style="padding: var(--space-2) var(--layout-margin-mobile) 0;'
          + (' background: var(--color-brand-teal-deep); color: var(--color-text-on-dark);' if dark_status else '')
          + '"><span class="ps-lb" style="color: inherit">9:41</span><span class="ps-lb" style="color: inherit">DEMO</span></div>') if statusbar else ""
    return (f'<figure class="ps-shot"><div class="ps-phone"><div class="ps-vp" data-w="390"><div class="ps-cv ps-cv--m">{sb}{inner}</div></div></div>'
            f'<figcaption><b>Mobile · 390.</b> {cap}</figcaption></figure>')


def notes(title, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="ps-notes"><h4>{title}</h4><ul>{lis}</ul></div>'


def screen(sid, title, desc, desktop="", phones=(), side=""):
    parts = [f'<article class="ps-screen" id="{sid}" aria-labelledby="{sid}-h"><header><h3 id="{sid}-h">{title}</h3><p>{desc}</p></header>']
    if desktop:
        parts.append(desktop)
    if phones:
        ph = "".join(phones)
        if side and len(phones) == 1:
            parts.append(f'<div class="ps-pair"><div class="ps-phones">{ph}</div>{side}</div>')
        elif side:
            parts.append(f'<div class="ps-phones">{ph}</div>{side}')
        else:
            parts.append(f'<div class="ps-phones">{ph}</div>')
    elif side:
        parts.append(side)
    parts.append("</article>")
    return "".join(parts)


# ---------------------------------------------------------------- shared pieces
def tl(steps, vertical=False, n=None):
    """steps: list of (state, title, detail) with state in done / next / ''."""
    out = []
    for st, t, d in steps:
        cls = {"done": "is-done", "next": "is-next"}.get(st, "")
        mk = CHECK if st == "done" else ""
        sr = {"done": ", done", "next": ", next step", "": ", upcoming"}[st]
        cur = ' aria-current="step"' if st == "next" else ""
        out.append(f'<li class="{cls}"{cur}><span class="ps-tlm" aria-hidden="true">{mk}</span><b>{t}</b><span class="d">{d}<span class="ps-sr">{sr}</span></span></li>')
    style = f' style="--n: {n or len(steps)}"'
    return f'<ol class="ps-tl{" ps-tl--v" if vertical else ""}"{style}>{"".join(out)}</ol>'


def meter(pct, left, right, label):
    return (f'<div class="ps-meter" role="img" aria-label="{label}"><span style="--w: {pct}%"></span></div>'
            f'<div class="ps-meter-l" aria-hidden="true"><span>{left}</span><span>{right}</span></div>')


def seg(a, b=None, i=0, full=False, label="Plan"):
    """Segmented control: `a` is a label or a list of labels (two or three options); `i` is the chosen one."""
    opts = list(a) if isinstance(a, (list, tuple)) else [a, b]
    btns = "".join(f'<button type="button" role="radio" aria-checked="{"true" if k == i else "false"}">{o}</button>' for k, o in enumerate(opts))
    return (f'<div class="segmented has-thumb{" segmented--full" if full else ""}" role="radiogroup" aria-label="{label}" style="--seg-n: {len(opts)}; --seg-i: {i}">'
            f'{btns}</div>')


def field(label, value="", help_="", typ="text", ph="", err=False, cls=""):
    v = f' value="{value}"' if value else ""
    p = f' placeholder="{ph}"' if ph else ""
    inv = ' aria-invalid="true"' if err else ""
    h = f'<span class="field__help">{help_}</span>' if help_ else ""
    return f'<label class="field{" field--error" if err else ""} {cls}"><span class="field__label">{label}</span><input class="field__input" type="{typ}"{v}{p}{inv}>{h}</label>'


def select(label, value, help_=""):
    h = f'<span class="field__help">{help_}</span>' if help_ else ""
    return (f'<label class="field"><span class="field__label">{label}</span><span class="ps-sel"><select class="field__input"><option>{value}</option></select>'
            f'{ic("chevron-down")}</span>{h}</label>')


def option(text, on=False):
    return f'<button type="button" class="option" role="radio" aria-checked="{"true" if on else "false"}"><span class="ps-o" aria-hidden="true"></span>{text}</button>'


def prod(p, sub="", size="name"):
    name = f'<span class="ps-prodname">{PNAME[p]}</span>' if size == "name" else f'<span class="ps-h2">{PNAME[p]}</span>'
    s = f'<span class="ps-cp">{sub}</span>' if sub else ""
    return f'<div class="ps-stack ps-stack--s"><div class="ps-prod">{mark(p)}{name}</div>{s}</div>'


def sw(on=False, label=""):
    return f'<button type="button" class="ps-sw" role="switch" aria-checked="{"true" if on else "false"}" aria-label="{label}"></button>'


def setrow(title, desc, on=False):
    return f'<label class="ps-set"><span><b>{title}</b><span class="ps-cp">{desc}</span></span>{sw(on, title)}</label>'


# One step model for the whole funnel (U-32, decision Q99): consent, account, recommendation, checkout, ID, send.
# The assessment counts seven steps; step 7 "Plan and send" holds the recommendation, checkout, the ID and the send.
# After Send: provider review, pharmacy, delivery. The progress mark sits in the content, not in the header (Q93).
STEP7 = "Plan and send"
SUBSTEPS = ["Your plan", "Checkout", "ID", "Send"]
CHARGE = "[charge line · operations]"
APPROVAL = "Prescription treatment is subject to provider approval. Results vary."


def _prog_svg(length):
    sw_ = cs.stroke_for(length)
    pad = sw_ / 2
    inner = length - sw_
    ld, rd, (bw, bh) = cs.capsule_paths(pad, pad, inner)
    fl, fr, _ = cs.capsule_paths(pad, pad, inner, inset=sw_ * 1.5)
    vb = f"0 0 {cs.f(bw + sw_)} {cs.f(bh + sw_)}"
    return (f'<svg class="ps-prog__line" viewBox="{vb}" aria-hidden="true"><path d="{ld}" stroke-width="{cs.f(sw_)}"/><path d="{rd}" stroke-width="{cs.f(sw_)}"/></svg>'
            f'<svg class="ps-prog__fill" viewBox="{vb}" aria-hidden="true"><path d="{fl}"/><path d="{fr}"/></svg>')


def funnel_prog(sub, mobile=False):
    """Progress row at the top of the content: the capsule, the step label beside it (Q104), and on desktop the parts of step 7."""
    share = (6 + (sub + 1) / (len(SUBSTEPS) + 1)) / 7
    size = "m" if mobile else "d"
    cap = f'<span class="ps-prog ps-prog--{size}" style="--p: {share * 100:.1f}%">{_prog_svg(96 if mobile else 120)}</span>'
    lis = "".join(f'<li class="{"is-done" if k < sub else ""}"{" aria-current=" + chr(34) + "step" + chr(34) if k == sub else ""}>{n}</li>'
                  for k, n in enumerate(SUBSTEPS))
    parts = "" if mobile else f'<ol class="ps-steps" aria-label="Parts of step 7">{lis}</ol>'
    return (f'<div class="ps-fprog" role="progressbar" aria-valuemin="0" aria-valuemax="7" aria-valuenow="7" aria-valuetext="Step 7 of 7, {STEP7}, {SUBSTEPS[sub]}">'
            f'{cap}<span class="ps-lb">Step 7 of 7 · {STEP7}</span>{parts}</div>')


def funnel_hdr(step, mobile=False):
    """The assessment header (R-29): 80 desktop with the Horizontal logo 52, 64 mobile with the Primary seal 50 (R-103).
    step 0 to 2 = inside step 7 (plan, checkout, ID); 3 = sent."""
    if mobile:
        left = (f'<a class="ps-ib" href="#" aria-label="Back">{ic("chevron-left")}</a>' if step < 3 else '<span class="ps-ib"></span>')
        right = '<a class="link ps-comp" href="#">Save</a>' if step < 3 else '<a class="link ps-comp" href="#">Account</a>'
        return f'<header class="ps-hdr">{left}<img class="ps-logo-seal" src="{LOGO_SEAL}" alt="unifiedmeds" width="137" height="50">{right}</header>'
    if step >= 3:
        right = '<a class="btn btn--outline btn--header" href="#">Go to your account</a>'
    else:
        right = '<span class="ps-row"><a class="link ps-comp" href="#">Save and finish later</a><a class="link ps-comp" href="#">Need help?</a></span>'
    return f'<header class="ps-hdr"><img class="ps-logo-h" src="{LOGO_H}" alt="unifiedmeds" width="320" height="52">{right}</header>'


def funnel_foot():
    return ('<footer class="ps-foot"><span class="ps-cp">© 2026 unifiedmeds</span><a class="ps-cp" href="#">Privacy</a><a class="ps-cp" href="#">Terms</a>'
            '<a class="ps-cp" href="#">Telehealth notice [legal]</a><span class="ps-cp">Assessment only. Not a diagnosis.</span></footer>')


PORTAL_NAV = [("home", "Home", "home"), ("treatment", "My treatment", "capsule"), ("messages", "Messages", "mail"),
              ("orders", "Orders", "package"), ("help", "Help", "help")]
PORTAL_TABS = [("home", "Home", "home"), ("treatment", "Treatment", "capsule"), ("messages", "Messages", "mail"),
               ("orders", "Orders", "package"), ("account", "Account", "user")]


def portal_d(active, inner, badge=1):
    items = []
    for key, label, icon in PORTAL_NAV:
        cur = ' aria-current="page"' if key == active else ""
        b = f'<span class="ps-badge" aria-label="{badge} new">{badge}</span>' if key == "messages" and badge else ""
        items.append(f'<a href="#"{cur}>{ic(icon)}{label}{b}</a>')
    acc_cur = ' aria-current="page"' if active == "account" else ""
    return (f'<div class="ps-app"><aside class="ps-side"><img class="ps-logo" src="{LOGO_H}" alt="unifiedmeds" width="185" height="30">'
            f'<nav class="ps-nav" aria-label="Your account">{"".join(items)}</nav>'
            f'<div class="ps-side-foot ps-nav"><a href="#"{acc_cur}>{ic("user")}Account</a><a href="#">{ic("log-out")}Sign out</a></div></aside>'
            f'<main class="ps-main">{inner}</main></div>')


def portal_m(active, inner, top=None, tabbar=True, badge=1):
    if top is None:
        top = (f'<header class="ps-top"><img class="ps-seal" src="{LOGO_SEAL}" alt="unifiedmeds" width="110" height="40">'
               f'<a class="ps-ib" href="#" aria-label="Help">{ic("help")}</a></header>')
    tabs = ""
    if tabbar:
        items = []
        for key, label, icon in PORTAL_TABS:
            cur = ' aria-current="page"' if key == active else ""
            b = f'<span class="ps-badge" aria-label="{badge} new">{badge}</span>' if key == "messages" and badge else ""
            items.append(f'<a href="#"{cur}>{ic(icon)}<span>{label}</span>{b}</a>')
        tabs = f'<nav class="ps-tabbar" aria-label="Your account">{"".join(items)}</nav>'
    return f'{top}<main class="ps-mmain">{inner}</main>{tabs}'


def back_top(title, sub=""):
    s = f'<span class="ps-cp" style="display:block">{sub}</span>' if sub else ""
    return (f'<header class="ps-top ps-top--back"><a class="ps-ib" href="#" aria-label="Back">{ic("chevron-left")}</a>'
            f'<span class="ps-h2">{title}{s}</span></header>')


ADMIN_NAV = [("queue", "Review queue", "clock", 12), ("members", "Members", "user", 0), ("messages", "Messages", "mail", 3),
             ("rx", "Prescriptions", "document", 0), ("audit", "Audit trail", "shield", 0), ("settings", "Settings", "settings", 0)]
SUPPORT_NAV = [("inbox", "Inbox", "mail", 9), ("mine", "Assigned to me", "user", 4), ("escalated", "Escalated", "alert-triangle", 2),
               ("macros", "Macros", "document", 0), ("orders", "Orders", "package", 0), ("audit", "Audit trail", "shield", 0)]


def internal_d(kind, active, inner):
    nav = ADMIN_NAV if kind == "clinical" else SUPPORT_NAV
    items = []
    for key, label, icon, n in nav:
        cur = ' aria-current="page"' if key == active else ""
        b = f'<span class="ps-badge">{n}</span>' if n else ""
        items.append(f'<a href="#"{cur}>{ic(icon)}{label}{b}</a>')
    env = "Clinical · internal" if kind == "clinical" else "Support · internal"
    who = ("<b>Jordan Lee, NP</b><span>Licensed in [states] · DEMO</span>" if kind == "clinical"
           else "<b>Sam Ortiz · Support</b><span>No access to health records</span>")
    return (f'<div class="ps-adm"><aside class="ps-aside"><img class="ps-logo" src="{LOGO_H_REV}" alt="unifiedmeds" width="148" height="24">'
            f'<span class="ps-env">{env}</span><nav aria-label="{env}">{"".join(items)}</nav>'
            f'<div class="ps-aside-foot">{who}<a href="#">{ic("log-out")}Sign out</a></div></aside>'
            f'<main class="ps-amain">{inner}</main></div>')


def pill(text, kind="", icon=None):
    k = f" ps-pill--{kind}" if kind else ""
    i = ic(icon) if icon else ""
    return f'<span class="ps-pill{k}">{i}{text}</span>'


def flag(text):
    return pill(text, "att", "alert-triangle")
