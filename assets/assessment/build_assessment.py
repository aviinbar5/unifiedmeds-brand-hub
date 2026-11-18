"""Assessment page: generated parts (unifiedmeds Brand Hub).

Run from the hub root:
    python3 -I assets/assessment/build_assessment.py
then build the pages as usual:
    python3 -I tools/build_pages.py

What it does
  1. Draws the progress capsule (R-42 progress mark, R-105, R-109) with tools/capsule_svg.py:
     the outline of both halves with the divider, plus the inner fill inset like the seal's
     filled half. The fill is clipped by CSS (--p) so the capsule fills as the member moves on.
     The fill never shows less than MIN_FILL, so the capsule reads on the first question (Q104).
     Lengths: 120 on desktop, 96 on mobile, 72 in the rail. Stroke = stroke_for(length).
  2. Draws the flow map (desktop and mobile versions) as inline SVG with CSS classes only,
     so every colour comes from brand.css tokens on the page.
  3. Writes the generated markup into src/assessment.html between markers
         <!--gen:NAME--> ... <!--/gen:NAME-->
     (every occurrence is refreshed, so the markers can repeat).
  4. Writes standalone copies to assets/assessment/ for the developer handoff:
     progress-capsule-*.svg and flow-map-*.svg. Standalone files may use the hex values
     from tokens.json; they are resolved from the hub's brand.css.
"""
import html
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXT = HERE.parent.parent
sys.path.insert(0, str(EXT / "tools"))
import capsule_svg as cs  # noqa: E402

SRC = EXT / "src" / "assessment.html"
CORE_CSS = EXT / "brand.css"
MIN_FILL = 0.1  # Q104: a visible start of the fill on the first question (the curve of the left cap)


def f(n):
    return cs.f(n)


# ---------------------------------------------------------------- progress capsule
def progress_parts(length):
    """Return (viewBox w, h, outline paths, fill paths) for a progress capsule whose
    rendered length is `length` px (stroke included)."""
    sw = cs.stroke_for(length)
    pad = sw / 2
    inner = length - sw
    ld, rd, (bw, bh) = cs.capsule_paths(pad, pad, inner)
    gap = sw * 1.5  # like the seal's filled half: one stroke of air inside the outline
    fl, fr, _ = cs.capsule_paths(pad, pad, inner, inset=gap)
    return bw + sw, bh + sw, sw, (ld, rd), (fl, fr)


def progress_inline(length):
    w, h, sw, (ld, rd), (fl, fr) = progress_parts(length)
    vb = f"0 0 {f(w)} {f(h)}"
    return (f'<svg class="as-prog__line" viewBox="{vb}" width="{f(w)}" height="{f(h)}" aria-hidden="true" focusable="false">'
            f'<path d="{ld}" stroke-width="{f(sw)}"/><path d="{rd}" stroke-width="{f(sw)}"/></svg>'
            f'<svg class="as-prog__fill" viewBox="{vb}" width="{f(w)}" height="{f(h)}" aria-hidden="true" focusable="false">'
            f'<path d="{fl}"/><path d="{fr}"/></svg>')


def progress_file(length, share, colours):
    """Standalone SVG at a given share (0..1) of progress, for the handoff."""
    w, h, sw, (ld, rd), (fl, fr) = progress_parts(length)
    teal = colours["--color-brand-deep-teal"]
    cut = f(w * share)
    return (f'<svg width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            f'<defs><clipPath id="p"><rect x="0" y="0" width="{cut}" height="{f(h)}"/></clipPath></defs>\n'
            f'<g clip-path="url(#p)" fill="{teal}"><path d="{fl}"/><path d="{fr}"/></g>\n'
            f'<path d="{ld}" stroke="{teal}" stroke-width="{f(sw)}"/>\n<path d="{rd}" stroke="{teal}" stroke-width="{f(sw)}"/>\n</svg>\n')


# ---------------------------------------------------------------- flow map data
# One step model for the whole funnel (U-32): Q97 order for the questions, Q98 email first, Q99 end of flow
# (consent, account, recommendation, checkout, ID, send).
STEPS = [
    # key, number shown, title, meta
    ("pre", "", "Welcome and email", "2 screens · not counted"),
    ("s1", "1", "About you", "4 screens"),
    ("s2", "2", "Health history", "7 screens"),
    ("s3", "3", "Medications", "5 screens"),
    ("s4", "4", "Your main concern", "7 screens"),
    ("s5", "5", "Preferences", "4 screens"),
    ("s6", "6", "Consent and account", "2 screens"),
    ("s7", "7", "Plan and send", "plan, checkout, ID, send"),
    ("send", "", "Send to your provider", "the one Yellow button"),
    ("prov", "", "Provider review", "[time · operations, R-68]"),
    ("pharm", "", "Pharmacy", "[partner · operations]"),
    ("ship", "", "Delivery", "packed with care · [time]"),
]
AFTER = {"prov", "pharm", "ship"}

EXITS = [
    # key, title, sources (step keys), lines
    ("sos", "Emergency: call 911", ["pre", "s2", "s4"], "Urgent signs, from any screen"),
    ("state", "Not available in your state", ["s1", "s7"], "Inline on the state screen (E-05), then Notify me"),
    ("person", "See a provider in person", ["s2"], "Heart and blood pressure answers"),
    ("stop", "Not eligible online", ["s1", "s3"], "Age, sex at birth, nitrates"),
]


def esc(s):
    return html.escape(s, quote=True)


def node(x, y, w, h, step, mobile=False):
    key, num, title, meta = step
    cls = "fm-n"
    if key == "pre":
        cls += " fm-n--pre"
    if key == "send":
        cls += " fm-n--send"
    if key in AFTER:
        cls += " fm-n--after"
    out = [f'<g class="{cls}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="12"/>']
    tx = x + 16
    if num:
        cx, cy = x + 28, y + h / 2
        out.append(f'<circle class="fm-num" cx="{f(cx)}" cy="{f(cy)}" r="14"/>'
                   f'<text class="fm-numt" x="{f(cx)}" y="{f(cy + 5)}" text-anchor="middle">{num}</text>')
        tx = x + 52
    if mobile:
        out.append(f'<text class="fm-t" x="{f(tx)}" y="{f(y + h / 2 - 3)}">{esc(title)}</text>'
                   f'<text class="fm-m" x="{f(tx)}" y="{f(y + h / 2 + 14)}">{esc(meta)}</text>')
    else:
        out.append(f'<text class="fm-t" x="{f(tx)}" y="{f(y + h / 2 + 5)}">{esc(title)}</text>'
                   f'<text class="fm-m" x="{f(x + w - 16)}" y="{f(y + h / 2 + 4)}" text-anchor="end">{esc(meta)}</text>')
    out.append("</g>")
    return "".join(out)


def exit_box(x, y, w, h, ex, mobile=False):
    key, title, _, line = ex
    cls = "fm-x fm-x--sos" if key == "sos" else "fm-x"
    cx, cy = x + 20, y + (h / 2 if not mobile else h / 2)
    mark = (f'<circle class="fm-xdot" cx="{f(cx)}" cy="{f(cy)}" r="8"/>'
            f'<rect class="fm-xbar" x="{f(cx - 1)}" y="{f(cy - 4.5)}" width="2" height="5.5" rx="1"/>'
            f'<circle class="fm-xbar" cx="{f(cx)}" cy="{f(cy + 3.5)}" r="1.1"/>')
    return (f'<g class="{cls}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="12"/>{mark}'
            f'<text class="fm-t" x="{f(x + 38)}" y="{f(y + h / 2 - 3)}">{esc(title)}</text>'
            f'<text class="fm-m" x="{f(x + 38)}" y="{f(y + h / 2 + 14)}">{esc(line)}</text></g>')


DEFS = ('<defs><marker id="{id}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path class="fm-arrow" d="M0 0L8 4L0 8Z"/></marker></defs>')


def flow_desktop():
    W = 928
    sx, sw_, nh, gap = 216, 336, 48, 20
    top = 56
    ys = {}
    parts = []
    y = top
    for i, st in enumerate(STEPS):
        if st[0] == "prov":
            y += 40  # room for the "after Send" label
        ys[st[0]] = y
        y += nh + gap
    H = y + 8
    parts.append(f'<svg class="fm fm--desk" viewBox="0 0 {W} {f(H)}" role="img" aria-labelledby="fm-d-t fm-d-d">'
                 '<title id="fm-d-t">Assessment flow map, desktop</title>'
                 '<desc id="fm-d-d">Welcome and email, then seven steps from About you to Plan and send (recommendation, checkout, ID), then Send to your provider. '
                 'Exits on the right: Emergency, Not available in your state, See a provider in person, Not eligible online. '
                 'Save and finish later works from any step. After Send: provider review, pharmacy, delivery.</desc>'
                 + DEFS.format(id="fm-a-d"))
    # column heads
    parts.append(f'<text class="fm-h" x="0" y="20">Any step</text>'
                 f'<text class="fm-h" x="{sx}" y="20">The assessment, in order</text>'
                 f'<text class="fm-h" x="616" y="20">Exits (suggested, the clinical team decides)</text>')
    # spine connectors
    keys = [s[0] for s in STEPS]
    for a, b in zip(keys, keys[1:]):
        x = sx + sw_ / 2
        cls = "fm-l fm-l--after" if b in AFTER else "fm-l"
        parts.append(f'<path class="{cls}" d="M{f(x)} {f(ys[a] + nh)}V{f(ys[b] - 2)}" marker-end="url(#fm-a-d)"/>')
    # after label
    parts.append(f'<text class="fm-h" x="{sx}" y="{f(ys["prov"] - 14)}">After Send (Product screens)</text>')
    # exits
    ex_y = {"sos": ys["pre"] - 4, "state": ys["s1"] + 34, "person": ys["s2"] + 72, "stop": ys["s3"] + 110}
    exh, exx, exw = 56, 616, 312
    lanes = {"sos": 562, "state": 576, "person": 590, "stop": 604}
    for ex in EXITS:
        key = ex[0]
        ey = ex_y[key] + exh / 2
        lx = lanes[key]
        for src in ex[2]:
            ny = ys[src] + nh / 2 + (6 if key in ("stop", "person") else -6 if key == "sos" else 0)
            parts.append(f'<path class="fm-l fm-l--x" d="M{sx + sw_} {f(ny)}H{lx}V{f(ey)}H{exx - 2}" marker-end="url(#fm-a-d)"/>')
    for ex in EXITS:
        parts.append(exit_box(exx, ex_y[ex[0]], exw, exh, ex))
    # nodes on top of lines
    for st in STEPS:
        parts.append(node(sx, ys[st[0]], sw_, nh, st))
    # save and resume bracket
    t, b = ys["s1"], ys["s7"] + nh
    parts.append(f'<path class="fm-l fm-l--save" d="M{sx - 4} {f(t)}H{sx - 20}V{f(b)}H{sx - 4}"/>')
    mid = (t + b) / 2
    parts.append(f'<g class="fm-save"><rect x="0" y="{f(mid - 74)}" width="176" height="148" rx="12"/>'
                 f'<text class="fm-t" x="16" y="{f(mid - 44)}">Save and finish later</text>'
                 f'<text class="fm-m" x="16" y="{f(mid - 22)}">From any step. Answers</text>'
                 f'<text class="fm-m" x="16" y="{f(mid - 4)}">are saved on Continue.</text>'
                 f'<text class="fm-m" x="16" y="{f(mid + 22)}">A link by email brings</text>'
                 f'<text class="fm-m" x="16" y="{f(mid + 40)}">him back to the next</text>'
                 f'<text class="fm-m" x="16" y="{f(mid + 58)}">open question.</text></g>')
    parts.append(f'<path class="fm-l fm-l--save" d="M176 {f(mid)}H{sx - 22}" marker-end="url(#fm-a-d)"/>')
    parts.append("</svg>")
    return "".join(parts), (W, H)


def flow_mobile():
    W = 350
    nh, gap, xh = 56, 16, 50
    parts = []
    y = 0
    body = []
    # top notes
    body.append(f'<g class="fm-save"><rect x="0" y="{y}" width="{W}" height="64" rx="12"/>'
                f'<text class="fm-t" x="16" y="{y + 26}">Any step: Save and finish later</text>'
                f'<text class="fm-m" x="16" y="{y + 46}">A link by email opens the next open question.</text></g>')
    y += 64 + 24
    attach = {"pre": ["sos"], "s1": ["state", "stop"], "s2": ["person", "sos"], "s3": ["stop"], "s4": ["sos"], "s7": ["state"]}
    exmap = {e[0]: e for e in EXITS}
    lines = []
    after_drawn = False
    prev_bottom = None
    for st in STEPS:
        key = st[0]
        if key in AFTER and not after_drawn:
            body.append(f'<text class="fm-h" x="0" y="{y + 14}">After Send</text>')
            y += 28
            after_drawn = True
        if prev_bottom is not None:
            cls = "fm-l fm-l--after" if key in AFTER else "fm-l"
            lines.append(f'<path class="{cls}" d="M24 {f(prev_bottom)}V{f(y - 2)}" marker-end="url(#fm-a-m)"/>')
        body.append(node(0, y, W, nh, st, mobile=True))
        y += nh
        bottom = y
        for xk in attach.get(key, []):
            y += 10
            ex = exmap[xk]
            lines.append(f'<path class="fm-l fm-l--x" d="M{W - 24} {f(bottom)}V{f(y + xh / 2)}H{W - 2}" />')
            body.append(exit_box(40, y, W - 80, xh, ex, mobile=True))
            # a short connector from the node edge into the exit box
            lines.append(f'<path class="fm-l fm-l--x" d="M24 {f(bottom)}V{f(y + xh / 2)}H38" marker-end="url(#fm-a-m)"/>')
            y += xh
        prev_bottom = y
        y += gap
    H = y
    # remove the right-hand helper lines (kept the left ones only, simpler on a phone)
    lines = [l for l in lines if f"M{W - 24} " not in l]
    parts.append(f'<svg class="fm fm--mob" viewBox="0 0 {W} {f(H)}" role="img" aria-labelledby="fm-m-t">'
                 '<title id="fm-m-t">Assessment flow map, mobile: the steps in order with their exits under each step</title>'
                 + DEFS.format(id="fm-a-m"))
    parts.extend(lines)
    parts.extend(body)
    parts.append("</svg>")
    return "".join(parts), (W, H)


# ---------------------------------------------------------------- screen gallery
CORE = ""
RAIL = ["About you", "Health history", "Medications", "Your main concern", "Preferences", "Consent and account", "Plan and send"]
ICONS = {
    "check": '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5 10.5l3 3 7-7"/></svg>',
    "chev": '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12.5 4.5L7 10l5.5 5.5"/></svg>',
    "close": '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M5 5l10 10M15 5L5 15"/></svg>',
    "alert": '<svg class="as-alert" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9"/><path d="M10 5.5v5.5"/><circle class="as-alert-dot" cx="10" cy="14.3" r="1.1"/></svg>',
    "core": CORE,
}


def loader_svg(cls="cap-loader"):
    """The capsule loader (core components.css .cap-loader), drawn with capsule_paths, length 60 in a 64 x 25.5 box."""
    ld, rd, (bw, bh) = cs.capsule_paths(2, 2, 60)
    return (f'<svg class="{cls}" viewBox="0 0 {f(bw + 4)} {f(bh + 4)}" aria-hidden="true">'
            f'<path class="cap-loader-fill" d="{ld}{rd}"/><path class="cap-loader-line" d="{ld}"/><path class="cap-loader-line" d="{rd}"/></svg>')


ICONS["loader"] = loader_svg()


def fill_icons(text):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: ICONS[m.group(1)], text)


def parse_screens():
    raw = (HERE / "screens.src.html").read_text()
    out = []
    for m in re.finditer(r"<!-- screen (.*?) -->(.*?)(?=<!-- screen |\Z)", raw, re.S):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        body = m.group(2)

        def part(tag):
            mm = re.search(r"<%s>(.*?)</%s>" % (tag, tag), body, re.S)
            return mm.group(1).strip() if mm else ""
        attrs["desc"], attrs["notes"], attrs["main"], attrs["main_m"] = part("desc"), part("notes"), part("main"), part("main-m")
        out.append(attrs)
    return out


def share(s):
    st = s["step"]
    if st == "done":
        return 1.0
    if st.isdigit():
        return max(MIN_FILL, (int(st) - 1 + float(s.get("within", 0))) / 7)
    return None


def pct(x):
    return f"{x * 100:.1f}".rstrip("0").rstrip(".") + "%"


def prog_block(s, size):
    sh = share(s)
    if sh is None:
        return ""
    st = s["step"]
    label = "Sent to your provider" if st == "done" else f"Step {st} of 7 · {RAIL[int(st) - 1]}"
    inner = progress_inline(120 if size == "d" else 96)
    if size == "m" and st != "done":
        # Q102: on mobile the capsule and its label are one button that opens the step list
        return (f'<div class="as-top"><button class="as-topbtn" type="button" aria-haspopup="dialog">'
                f'<span class="as-prog as-prog--{size}" style="--p: {pct(sh)}">{inner}</span>'
                f'<span class="as-steplabel">{label}</span><span class="as-topchev">{ICONS["chev"]}</span></button></div>')
    return (f'<div class="as-top"><span class="as-prog as-prog--{size}" style="--p: {pct(sh)}">{inner}</span>'
            f'<span class="as-steplabel">{label}</span></div>')


def rail(s):
    st = s["step"]
    if not st.isdigit():
        return ""
    cur = int(st)
    items = []
    for i, name in enumerate(RAIL, 1):
        cls = "is-passed" if i < cur else "is-active" if i == cur else ""
        num = ICONS["check"] if i < cur else str(i)
        items.append(f'<li class="{cls}"><span class="as-rail-n">{num}</span><span>{name}</span></li>')
    return f'<ol class="as-rail">{"".join(items)}</ol>'


def overlay(s, size):
    kind = s.get("overlay")
    if kind == "steps":
        if size == "d":
            return ""  # desktop shows the rail at all times
        st = int(s["step"])
        items = []
        for i, name in enumerate(RAIL, 1):
            cls = "is-passed" if i < st else "is-active" if i == st else ""
            num = ICONS["check"] if i < st else str(i)
            items.append(f'<li class="{cls}"><span class="as-rail-n">{num}</span><span>{name}</span></li>')
        return (f'<div class="as-scrim"></div><div class="as-dlg as-dlg--sheet"><button class="as-dlg-x" type="button" aria-label="Close">{ICONS["close"]}</button>'
                f'<p class="as-dlg-t">Your steps.</p><ol class="as-rail">{"".join(items)}</ol>'
                '<p class="as-small">Steps you have finished can be opened to change an answer.</p></div>')
    if kind != "save":
        return ""
    cls = "as-dlg" if size == "d" else "as-dlg as-dlg--sheet"
    return (f'<div class="as-scrim"></div><div class="{cls}"><button class="as-dlg-x" type="button" aria-label="Close">{ICONS["close"]}</button>'
            '<p class="as-dlg-t">Save and finish later.</p>'
            '<p class="as-help">Your answers are saved. We\'ll email a link to j•••@example.com, the address you gave at the start. The link signs you in; there is no password. The email won\'t say what it\'s about.</p>'
            '<div class="as-dlg-a"><button class="btn" type="button">Email me the link</button><button class="btn btn--outline" type="button">Keep going</button></div></div>')


def actions_desk(s):
    if not s.get("cta"):
        return ""
    kind = " btn--yellow" if s.get("kind") == "yellow" else ""
    dis = ' aria-disabled="true"' if s.get("dis") == "yes" else ""
    parts = [f'<button class="btn{kind}" type="button"{dis}>{s["cta"]}</button>']
    if s.get("cta2"):
        parts.append(f'<a class="as-tlink" href="#">{s["cta2"]}</a>')
    if s.get("back") == "yes":
        parts.append(f'<button class="as-tbtn as-tbtn--back" type="button">{ICONS["chev"]}Back</button>')
    return f'<div class="as-actions">{"".join(parts)}</div>'


SAVE_D = '<button class="as-tbtn" type="button">Save and finish later</button>'


def desk_screen(s):
    st = s["step"]
    save = st.isdigit() or st == "pre"
    hd = (f'<header class="as-hd"><img class="as-logo" src="{CORE}assets/brand/logo-horizontal.svg" width="321" height="52" alt="unifiedmeds">'
          f'<div class="as-hd-r">{SAVE_D if save else ""}<a class="as-tlink" href="#">Need help?</a></div></header>')
    r = rail(s)
    col = (f'<div class="as-col">{prog_block(s, "d")}<div class="as-main">{s["main"]}</div>{actions_desk(s)}'
           '<p class="as-legal">Assessment only. Not a diagnosis.</p></div>')
    body = f'<div class="as-body{"" if r else " as-body--solo"}">{r}{col}</div>'
    ft = ('<footer class="as-ft"><span>Is this an emergency? <a class="link" href="#">Call 911</a>.</span>'
          '<span><a class="link" href="#">Privacy</a> · <a class="link" href="#">Terms</a> · © 2026 unifiedmeds</span></footer>')
    out = f'<div class="as-scr as-scr--d" inert>{hd}{body}{ft}{overlay(s, "d")}</div>'
    return re.sub(r'name="(m-[a-z]+)"', r'name="\1-d"', out)


def mob_screen(s):
    st = s["step"]
    save = st.isdigit() or st == "pre"
    left = (f'<button class="as-ibtn" type="button" aria-label="Back">{ICONS["chev"]}</button>' if s.get("back") == "yes"
            else '<span class="as-ibtn"></span>')
    right = '<button class="as-tbtn" type="button">Save</button>' if save else '<a class="as-tlink" href="#">Help</a>'
    hd = (f'<header class="as-hd as-hd--m">{left}<img class="as-seal" src="{CORE}assets/brand/logo-seal.svg" width="137" height="50" alt="unifiedmeds">{right}</header>')
    main = s["main_m"] or s["main"]
    sos = "" if s["id"] == "sos" else '<p class="as-sos">Is this an emergency? <a class="link" href="#">Call 911</a>.</p>'
    bar = ""
    if s.get("cta"):
        kind = " btn--yellow" if s.get("kind") == "yellow" else ""
        dis = ' aria-disabled="true"' if s.get("dis") == "yes" else ""
        two = f'<a class="as-tlink" href="#">{s["cta2"]}</a>' if s.get("cta2") else ""
        bar = (f'<div class="as-bar"><button class="btn btn--bar{kind}" type="button"{dis}>{s["cta"]}</button>{two}'
               '<p class="as-legal">Assessment only. Not a diagnosis.</p></div>')
    out = (f'<div class="as-scr as-scr--m" inert>{hd}{prog_block(s, "m")}<div class="as-mbody"><div class="as-main">{main}</div>{sos}</div>'
           f'{bar}{overlay(s, "m")}</div>')
    return re.sub(r'name="(m-[a-z]+)"', r'name="\1-m"', out)


def gallery():
    screens = parse_screens()
    nav = "".join(f'<a href="#scr-{s["id"]}">{s["n"]} {html.escape(s["title"])}</a>' for s in screens)
    arts = [f'<nav class="as-shotnav" aria-label="Screens">{nav}</nav>']
    for s in screens:
        arts.append(
            f'<article class="as-shot" id="scr-{s["id"]}" aria-labelledby="scr-{s["id"]}-h">'
            f'<div class="as-shot-head"><span class="ext-pill">{s["n"]}</span><h3 id="scr-{s["id"]}-h">{html.escape(s["title"])}.</h3><p>{s["desc"]}</p></div>'
            f'<div class="as-shot-d"><span class="as-dim">Desktop · 1440 × 900</span><div class="as-frame as-frame--d" data-w="1440" data-h="900">{fill_icons(desk_screen(s))}</div></div>'
            f'<div class="as-shot-row"><div class="as-shot-m"><span class="as-dim">Mobile · 390 × 844</span><div class="as-frame as-frame--m" data-w="390" data-h="844">{fill_icons(mob_screen(s))}</div></div>'
            f'<div class="as-shot-notes"><b>Notes for the build</b><ul>{s["notes"]}</ul></div></div></article>')
    return "".join(arts)


# ---------------------------------------------------------------- standalone files
FM_CSS = """
.fm text { font-family: Inter, Arial, sans-serif; }
.fm-h { font-size: 12px; font-weight: 600; fill: var(--color-text-secondary); }
.fm-t { font-size: 14px; font-weight: 600; fill: var(--color-text-strong); }
.fm-m { font-size: 12px; fill: var(--color-text-secondary); }
.fm-n rect { fill: var(--color-surface-card); stroke: var(--color-line-field); stroke-width: 1; }
.fm-n--pre rect { fill: var(--color-surface-mist); stroke: var(--color-surface-mist); }
.fm-n--send rect { fill: var(--color-brand-teal-deep); stroke: var(--color-brand-teal-deep); }
.fm-n--send .fm-t { fill: var(--color-surface-paper); }
.fm-n--send .fm-m { fill: var(--color-surface-wash-blue); }
.fm-n--after rect { fill: var(--color-surface-paper); stroke: var(--color-line-deep); stroke-dasharray: 4 4; }
.fm-num { fill: var(--color-surface-paper); stroke: var(--color-brand-deep-teal); stroke-width: 1; }
.fm-numt { font-size: 13px; font-weight: 600; fill: var(--color-brand-deep-teal); }
.fm-x rect { fill: var(--color-surface-paper); stroke: var(--color-line-field); stroke-width: 1; }
.fm-x--sos > rect { stroke: var(--color-brand-teal-deep); stroke-width: 2; }
.fm-xdot { fill: var(--color-brand-coral); }
.fm-x .fm-xbar { fill: var(--color-surface-paper); stroke: none; }
.fm-save rect { fill: var(--color-surface-wash-blue); }
.fm-l { fill: none; stroke: var(--color-line-field); stroke-width: 1.5; }
.fm-l--x { stroke-dasharray: 4 3; }
.fm-l--after { stroke: var(--color-line-deep); stroke-dasharray: 4 4; }
.fm-l--save { stroke: var(--color-brand-blue); }
.fm-arrow { fill: var(--color-line-field); }
"""


def token_values():
    text = CORE_CSS.read_text()
    vals = dict(re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", text))

    def resolve(v, depth=0):
        m = re.fullmatch(r"var\((--[a-z0-9-]+)\)", v.strip())
        if m and depth < 5:
            return resolve(vals[m.group(1)], depth + 1)
        return v.strip()
    return {k: resolve(v) for k, v in vals.items()}


def standalone(svg_inline, size, colours):
    css = re.sub(r"var\((--[a-z0-9-]+)\)", lambda m: colours[m.group(1)], FM_CSS)
    w, h = size
    svg = svg_inline.replace("<svg ", f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" ', 1)
    svg = svg.replace("<defs>", f"<style>{css}</style><defs>", 1)
    return svg + "\n"


def inject(text, name, content):
    pat = re.compile(r"(<!--gen:%s-->)(.*?)(<!--/gen:%s-->)" % (re.escape(name), re.escape(name)), re.S)
    new, n = pat.subn(lambda m: m.group(1) + content + m.group(3), text)
    return new, n


def main():
    colours = token_values()
    desk, dsize = flow_desktop()
    mob, msize = flow_mobile()
    gen = {
        "flow-desktop": desk,
        "flow-mobile": mob,
        "prog-d": progress_inline(120),
        "prog-m": progress_inline(96),
        "prog-s": progress_inline(72),
        "screens": gallery(),
        "loader": loader_svg(),
    }
    text = SRC.read_text()
    for name, content in gen.items():
        text, n = inject(text, name, content)
        print(f"{name}: {n} place(s)")
    SRC.write_text(text)
    (HERE / "flow-map-desktop.svg").write_text(standalone(desk, dsize, colours))
    (HERE / "flow-map-mobile.svg").write_text(standalone(mob, msize, colours))
    for length, tag in ((120, "desktop-120"), (96, "mobile-96")):
        for share, stag in ((0, "0"), (3 / 7, "3of7"), (1, "7of7")):
            (HERE / f"progress-capsule-{tag}-{stag}.svg").write_text(progress_file(length, share, colours))
    print("wrote standalone SVGs to", HERE.relative_to(EXT))


if __name__ == "__main__":
    main()
