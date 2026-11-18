"""unifiedmeds social kits (S1): writes src/social-facebook.html, src/social-instagram.html and src/social-x.html
from manifest.json (written by make_social.py) plus the page copy below.

Run from the extended hub root, after make_social.py:
    python3 -I assets/social/shared/build_kit_pages.py
    python3 -I tools/build_pages.py
Every channel page has the same six sections (ids profile, assets, mobile, copy, rules, files) and the
shared .sk-* classes, so the six channel pages match.
"""
import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
EXT = HERE.parents[2]
MAN = json.loads((HERE / "manifest.json").read_text())
DATE = "17.11.2026"
E = html.escape

CSS = """<style>
  .rule > .status { justify-self: start; }
  /* Social kit pages: shared classes (.sk-*), same block on every channel page. Tokens only. */
  .sk-pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-8) var(--space-6); align-items: start; }
  .sk-opt { margin: 0; display: grid; gap: var(--space-3); align-content: start; min-width: 0; }
  .sk-opt figcaption { display: grid; gap: var(--space-1); color: var(--color-text-secondary); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  .sk-opt figcaption b { color: var(--color-text-strong); font-weight: 600; }
  .sk-opt figcaption a { justify-self: start; }
  .sk-art { position: relative; margin: 0; border-radius: var(--radius-xs); overflow: hidden; border: 1px solid var(--color-line-base); background: var(--color-surface-mist); }
  .sk-art > img { display: block; width: 100%; height: auto; }
  .sk-art--tall { max-width: calc(var(--space-24) * 3.5); }
  .sk-art--sq { max-width: calc(var(--space-24) * 2.5); }
  .sk-art--grid { max-width: calc(var(--space-24) * 4.5); }
  .sk-art--post { max-width: calc(var(--space-24) * 4.5); }
  .sk-safe { position: absolute; box-sizing: border-box; border: 2px dashed var(--color-surface-paper); box-shadow: 0 0 0 1px var(--color-brand-teal-deep), inset 0 0 0 1px var(--color-brand-teal-deep); pointer-events: none; }
  .sk-safe i { position: absolute; left: var(--space-1); top: var(--space-1); max-width: calc(100% - var(--space-2)); padding: 0 var(--space-1); border-radius: var(--radius-xs); background: var(--color-brand-teal-deep); color: var(--color-text-on-dark); font: var(--type-desktop-label-weight) var(--type-desktop-label-size) / var(--type-desktop-label-line) var(--font-family-sans); font-style: normal; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .sk-safe--ui { background: color-mix(in srgb, var(--color-brand-teal-deep) 45%, transparent); }
  .sk-safe--round { border-radius: 50%; }
  .sk-safe--round i { left: 50%; top: 50%; transform: translate(-50%, -50%); }
  .sk-safe--sticker { border-style: dotted; }
  .sk-safe--keep2 { border-color: var(--color-surface-wash-blue); }
  .sk-safe--keep2 i { top: auto; bottom: var(--space-1); }
  .sk-kit:not(:has(.sk-toggle input:checked)) .sk-safe { display: none; }
  .sk-toggle { display: inline-flex; align-items: center; gap: var(--space-2); min-height: var(--size-tap-min); padding: 0 var(--space-4); border: 1px solid var(--color-line-mid); border-radius: var(--radius-button); background: var(--color-surface-card); color: var(--color-text-strong); font: var(--type-desktop-nav-weight) var(--type-desktop-nav-size) / var(--type-desktop-nav-line) var(--font-family-sans); cursor: pointer; }
  .sk-toggle input { width: var(--space-4); height: var(--space-4); accent-color: var(--color-brand-deep-teal); }
  .sk-block { display: grid; gap: var(--space-5); padding-top: var(--space-10); margin-top: var(--space-10); border-top: 1px solid var(--color-line-soft); }
  .sk-block:first-of-type { border-top: 0; margin-top: var(--space-4); padding-top: 0; }
  .sk-block > header { display: grid; gap: var(--space-2); max-width: var(--layout-measure); }
  .sk-block > header h3 { margin: 0; }
  .sk-block > header p { margin: 0; color: var(--color-text-secondary); }
  .sk-spec { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: var(--space-2) var(--space-4); margin: 0; padding: var(--space-4); border-radius: var(--radius-small); background: var(--color-surface-mist); }
  .sk-spec div { display: grid; gap: var(--space-1); min-width: 0; }
  .sk-spec dt { color: var(--color-text-secondary-on-mist); font: var(--type-desktop-label-weight) var(--type-desktop-label-size) / var(--type-desktop-label-line) var(--font-family-sans); letter-spacing: var(--type-desktop-label-tracking); }
  .sk-spec dd { margin: 0; color: var(--color-text-strong); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); overflow-wrap: anywhere; }
  .sk-strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-2); }
  .sk-strip img { display: block; width: 100%; height: auto; }
  .sk-rings { display: flex; flex-wrap: wrap; gap: var(--space-3); }
  .sk-rings span { display: grid; justify-items: center; gap: var(--space-1); width: var(--space-18); color: var(--color-text-secondary); font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); text-align: center; }
  .sk-rings img { width: var(--space-14); height: var(--space-14); border-radius: 50%; object-fit: cover; box-shadow: 0 0 0 2px var(--color-surface-paper), 0 0 0 3px var(--color-line-mid); }
  .sk-avs { display: flex; align-items: flex-end; gap: var(--space-4); }
  .sk-avs img { display: block; border-radius: 50%; border: 1px solid var(--color-line-base); }
  .sk-av-l { width: calc(var(--space-24) + var(--space-12)); height: calc(var(--space-24) + var(--space-12)); }
  .sk-av-m { width: var(--space-12); height: var(--space-12); }
  .sk-av-s { width: var(--space-8); height: var(--space-8); }
  .sk-ctx { display: flex; flex-wrap: wrap; gap: var(--space-6); align-items: flex-start; }
  .sk-ctx > figure { margin: 0; display: grid; gap: var(--space-2); min-width: 0; flex: 0 1 calc(var(--layout-frame-mobile) * 0.82); }
  .sk-ctx > figure.sk-ctx-desk { flex: 1 1 calc(var(--space-24) * 4); }
  .sk-ctx > figure.sk-ctx-wide { flex-basis: var(--layout-frame-mobile); }
  .rule > .status { justify-self: start; }
  .sk-ctx figcaption { color: var(--color-text-secondary); font: var(--type-desktop-caption-weight) var(--type-desktop-caption-size) / var(--type-desktop-caption-line) var(--font-family-sans); }
  .sk-phone { box-sizing: border-box; width: min(100%, calc(var(--layout-frame-mobile) * 0.82)); padding: var(--space-2); border: 1px solid var(--color-line-mid); border-radius: calc(var(--radius-card) * 2); background: var(--color-surface-card); }
  .sk-phone--wide { width: min(100%, var(--layout-frame-mobile)); }
  .sk-screen { position: relative; overflow: hidden; border-radius: calc(var(--radius-card) + var(--space-1)); background: var(--color-surface-paper); }
  .sk-screen > img, .sk-desk > img, .sk-fbcover > img, .sk-xhead > img { display: block; width: 100%; height: auto; }
  .sk-desk { box-sizing: border-box; width: 100%; border: 1px solid var(--color-line-mid); border-radius: var(--radius-small); overflow: hidden; background: var(--color-surface-paper); }
  .sk-desk-bar { display: flex; gap: var(--space-1); align-items: center; height: var(--space-6); padding: 0 var(--space-3); background: var(--color-surface-mist); border-bottom: 1px solid var(--color-line-base); }
  .sk-desk-bar span { width: var(--space-2); height: var(--space-2); border-radius: 50%; background: var(--color-line-mid); }
  .sk-desk-bar em { margin-left: var(--space-3); padding: 0 var(--space-3); border-radius: var(--radius-xs); background: var(--color-surface-paper); color: var(--color-text-tertiary); font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); font-style: normal; }
  .sk-app { display: flex; align-items: center; gap: var(--space-2); padding: var(--space-2) var(--space-3); color: var(--color-text-strong); font: 600 var(--type-mobile-compact-size) / var(--type-mobile-compact-line) var(--font-family-sans); }
  .sk-app img { width: var(--space-8); height: var(--space-8); border-radius: 50%; }
  .sk-app small { display: block; color: var(--color-text-secondary); font-weight: 400; }
  .sk-acts { display: flex; gap: var(--space-3); padding: var(--space-2) var(--space-3); }
  .sk-acts span { width: var(--space-6); height: var(--space-2); border-radius: var(--radius-xs); background: var(--color-line-base); }
  .sk-cap { margin: 0; padding: 0 var(--space-3) var(--space-3); color: var(--color-text-primary); font: var(--type-mobile-compact-weight) var(--type-mobile-compact-size) / var(--type-mobile-compact-line) var(--font-family-sans); }
  .sk-cropbox { position: relative; overflow: hidden; }
  .sk-cropbox img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .sk-c169 { aspect-ratio: 16 / 9; } .sk-c31 { aspect-ratio: 3 / 1; } .sk-c34 { aspect-ratio: 3 / 4; }
  .sk-ui-top, .sk-ui-bot { position: absolute; left: 0; right: 0; display: flex; align-items: center; gap: var(--space-2); padding: var(--space-2) var(--space-3); color: var(--color-text-on-dark); font: 600 var(--type-mobile-label-size) / var(--type-mobile-label-line) var(--font-family-sans); }
  .sk-ui-top { top: 0; background: linear-gradient(color-mix(in srgb, var(--color-brand-teal-deep) 55%, transparent), transparent); }
  .sk-ui-top img { width: var(--space-6); height: var(--space-6); border-radius: 50%; }
  .sk-ui-bot { bottom: 0; }
  .sk-ui-bot span { flex: 1; height: var(--space-8); border: 1px solid var(--color-surface-paper); border-radius: var(--radius-pill); opacity: 0.8; }
  .sk-link { padding: var(--space-2) var(--space-3) var(--space-3); background: var(--color-surface-mist); color: var(--color-text-strong); font: 600 var(--type-mobile-compact-size) / var(--type-mobile-compact-line) var(--font-family-sans); }
  .sk-link small { display: block; color: var(--color-text-secondary); font-weight: 400; }
  /* profile mocks */
  .sk-prof { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); gap: var(--space-6); align-items: start; }
  .sk-prof + .sk-prof { margin-top: var(--space-10); }
  .sk-prof > figure { margin: 0; display: grid; gap: var(--space-2); min-width: 0; }
  .sk-prof figcaption { color: var(--color-text-secondary); font: var(--type-desktop-caption-weight) var(--type-desktop-caption-size) / var(--type-desktop-caption-line) var(--font-family-sans); }
  .sk-fbcover, .sk-xhead { position: relative; }
  .sk-pbody { position: relative; display: grid; gap: var(--space-1); padding: var(--space-3) var(--space-4) var(--space-4); }
  .sk-pav { width: calc(var(--space-24) + var(--space-6)); height: calc(var(--space-24) + var(--space-6)); margin-top: calc(var(--space-14) * -1); border-radius: 50%; border: var(--space-1) solid var(--color-surface-paper); position: relative; }
  .sk-pav--s { width: calc(var(--space-18) + var(--space-2)); height: calc(var(--space-18) + var(--space-2)); margin-top: calc(var(--space-10) * -1); }
  .sk-pname { color: var(--color-text-strong); font: 600 var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); }
  .sk-pmeta { color: var(--color-text-secondary); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  .sk-pbtns { display: flex; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-2); }
  .sk-pbtns span { display: inline-flex; align-items: center; min-height: var(--space-8); padding: 0 var(--space-3); border-radius: var(--radius-xs); background: var(--color-surface-mist); color: var(--color-text-strong); font: 600 var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); }
  .sk-ptabs { display: flex; gap: var(--space-4); padding: var(--space-2) var(--space-4); border-top: 1px solid var(--color-line-base); color: var(--color-text-secondary); font: 600 var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); overflow: hidden; white-space: nowrap; }
  .sk-ptabs b { color: var(--color-text-strong); }
  .sk-ig { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: var(--space-4) var(--space-6); align-items: center; padding: var(--space-5); }
  .sk-ig .sk-pav { margin: 0; border-width: 0; }
  .sk-ig .sk-rings, .sk-ig .sk-iggrid { grid-column: 1 / -1; }
  .sk-iggrid img { display: block; width: 100%; height: auto; }
  .sk-ig--phone { grid-template-columns: auto minmax(0, 1fr); padding: var(--space-3); gap: var(--space-3); }
  .sk-ig--phone .sk-pav { width: calc(var(--space-18) + var(--space-2)); height: calc(var(--space-18) + var(--space-2)); }
  .sk-ig--phone .sk-pbio { grid-column: 1 / -1; }
  .sk-ig--phone .sk-rings span { width: var(--space-14); }
  .sk-ig--phone .sk-rings img { width: var(--space-12); height: var(--space-12); }
  .sk-pbio { margin: 0; color: var(--color-text-primary); font: var(--type-mobile-compact-weight) var(--type-mobile-compact-size) / var(--type-mobile-compact-line) var(--font-family-sans); }
  .sk-stats { display: flex; flex-wrap: wrap; gap: var(--space-4); color: var(--color-text-strong); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  /* copy */
  .sk-copy { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-4); }
  .sk-copy .rule p { white-space: pre-line; }
  .sk-count { color: var(--color-text-secondary); font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); }
  .sk-rules { margin: 0; padding-left: var(--space-6); display: grid; gap: var(--space-3); max-width: var(--layout-measure); }
  .sk-rules b { color: var(--color-text-strong); }
  @media (max-width: 1023px) {
    .sk-spec { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .sk-prof { grid-template-columns: minmax(0, 1fr); }
  }
  @media (max-width: 767px) {
    .sk-pair, .sk-copy { grid-template-columns: minmax(0, 1fr); }
    .sk-spec { grid-template-columns: minmax(0, 1fr); }
    .sk-art--tall, .sk-art--post { max-width: 100%; }
    .sk-ig { grid-template-columns: minmax(0, 1fr); }
  }
</style>
"""

CHANNELS = {
    "facebook": dict(
        page="social-facebook.html", eyebrow="Marketing · Social", h1="Facebook kit.",
        lead="Everything the unifiedmeds Facebook Page needs, in two options each: Option A is calm and editorial (photo-led, a serif headline), Option B is graphic (the capsule kit and colour). Each asset shows its desktop and its phone treatment.",
        status="The kit is approved for use. The profile picture is Option B, the white u|m on Navy (R-93, U-27). Lines come from the line bank and are candidates; legal approves every post before it runs (U-30).",
        assets=["avatar", "cover", "post-square", "post-portrait", "link", "story", "event", "ad"],
    ),
    "instagram": dict(
        page="social-instagram.html", eyebrow="Marketing · Social", h1="Instagram and Threads kit.",
        lead="Everything the unifiedmeds Instagram profile needs, plus the Threads card. Two options each: Option A is calm and editorial, Option B is graphic. Instagram is a phone channel first, so every asset is shown at phone size.",
        status="The kit is approved for use. The profile picture is Option B, the white u|m on Navy (R-93, U-27); the grid is designed for 3:4 (U-27). Lines are candidates from the line bank; legal approves every post before it runs (U-30).",
        assets=["avatar", "grid", "post-portrait", "post-square", "carousel", "story", "reel-cover", "highlights", "threads"],
    ),
    "x": dict(
        page="social-x.html", eyebrow="Marketing · Social", h1="X kit.",
        lead="Everything the unifiedmeds X profile needs, in two options each: Option A is calm and editorial, Option B is graphic. Each asset shows how it reads on a desktop timeline and on a phone.",
        status="The kit is approved for use. The profile picture is Option B, the white u|m on Navy (R-93, U-27). Handles, bios and lines are placeholders or candidates; legal approves every post before it runs (U-30).",
        assets=["avatar", "header", "post-wide", "post-square", "card"],
    ),
}


def assets_of(ch):
    return {m["key"]: m for m in MAN if m["channel"] == ch}


def kb(path):
    p = EXT / path
    return f"{p.stat().st_size / 1024:,.0f} KB" if p.exists() else "missing"


def safe_spans(m):
    w, h = m["size"]
    out = []
    for z in m["safe"]:
        style = f'left:{z["x"] / w * 100:.2f}%;top:{z["y"] / h * 100:.2f}%;width:{z["w"] / w * 100:.2f}%;height:{z["h"] / h * 100:.2f}%'
        out.append(f'<span class="sk-safe sk-safe--{z["kind"]}" style="{style}" aria-hidden="true"><i>{E(z["label"])}</i></span>')
    return "".join(out)


def art(m, src, alt, extra=""):
    w, h = m["size"]
    cls = "sk-art"
    if h / w > 1.5:
        cls += " sk-art--tall"
    elif m["key"] == "avatar":
        cls += " sk-art--sq"
    elif m["key"] == "grid":
        cls += " sk-art--grid"
    elif h / w > 0.9:
        cls += " sk-art--post"
    return f'<div class="{cls}{extra}"><img src="{src}" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy">{safe_spans(m)}</div>'


def spec(m):
    w, h = m["size"]
    zones = "; ".join(z["label"] for z in m["safe"]) or "None (planning view)"
    rows = [("Size", f"{w} × {h} px"), ("Ratio", m["ratio"]), ("File", m["ftype"]), ("Max file size", m["maxsize"]), ("Safe zones", zones)]
    return '<dl class="sk-spec">' + "".join(f"<div><dt>{a}</dt><dd>{E(b)}</dd></div>" for a, b in rows) + "</dl>"


def option(m, o, ch):
    d = m[o]
    letter = o.upper()
    files = d["files"]
    title = m["title"]
    if m["key"] == "carousel":
        visual = '<div class="sk-strip">' + "".join(
            art(m, f, f"{title}, Option {letter}, card {i + 1}") if i == 0 else
            f'<div class="sk-art"><img src="{f}" width="{m["size"][0]}" height="{m["size"][1]}" alt="{E(title)}, Option {letter}, card {i + 1}" loading="lazy"></div>'
            for i, f in enumerate(files)) + "</div>"
    elif m["key"] == "highlights":
        visual = art(m, files[0], f"Highlight cover, Option {letter}, {m['labels'][0]}") + '<div class="sk-rings">' + "".join(
            f'<span><img src="{f}" alt="" loading="lazy">{E(lab)}</span>' for f, lab in zip(files, m["labels"])) + "</div>"
    elif m["key"] == "avatar":
        visual = art(m, files[0], f"Profile picture, Option {letter}") + (
            f'<div class="sk-avs"><img class="sk-av-l" src="{files[0]}" alt="" loading="lazy"><img class="sk-av-m" src="{files[0]}" alt="" loading="lazy">'
            f'<img class="sk-av-s" src="{files[0]}" alt="" loading="lazy"></div>')
    else:
        visual = art(m, files[0], f"{title}, Option {letter}")
    j0 = (d.get("jpgs") or [None])[0]
    dl = " · ".join(f'<a class="link" href="{f}" download>PNG</a>' + (f' <a class="link" href="{j0}" download>JPG</a>' if j0 else "") +
                    f' <a class="link" href="{s}" download>SVG</a>' for f, s in zip(files[:1], d["svgs"][:1]))
    more = f" · {len(files)} files, see Files" if len(files) > 1 else ""
    return (f'<figure class="sk-opt">{visual}<figcaption><b>Option {letter}</b><span>{E(d["line"])}</span>'
            f'<span>{dl}{more}</span></figcaption></figure>')


# ------------------------------------------------------------------ context frames
def av(ch, o="a"):
    return f"assets/social/{ch}/{ch}-avatar-{o}.png"


def phone(inner, cap, wide=False):
    return f'<figure{" class=\"sk-ctx-wide\"" if wide else ""}><div class="sk-phone{" sk-phone--wide" if wide else ""}"><div class="sk-screen">{inner}</div></div><figcaption>{E(cap)}</figcaption></figure>'


def desk(inner, cap, url="facebook.com/[page]"):
    return (f'<figure class="sk-ctx-desk"><div class="sk-desk"><div class="sk-desk-bar"><span></span><span></span><span></span><em>{E(url)}</em></div>'
            f'{inner}</div><figcaption>{E(cap)}</figcaption></figure>')


def app_head(ch, sub="[time]"):
    name = "unifiedmeds"
    return f'<div class="sk-app"><img src="{av(ch)}" alt=""><span>{name}<small>{E(sub)}</small></span></div>'


ACTS = '<div class="sk-acts"><span></span><span></span><span></span></div>'


def context(m, ch):
    a = m["a"]["files"][0]
    b = m["b"]["files"][0]
    k, c = m["key"], m["ctx"]
    w, h = m["size"]
    img = lambda f, alt="": f'<img src="{f}" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy">'
    if c == "feed":
        sub = "Sponsored" if k == "ad" else "[time]"
        cap = CAPTIONS[ch][0][1].split("\n")[0]
        return phone(app_head(ch, sub) + img(a, "Option A in the feed") + ACTS + f'<p class="sk-cap"><b>unifiedmeds</b> {E(cap)}</p>', "Option A in the feed, phone 390") + \
            phone(app_head(ch, sub) + img(b, "Option B in the feed") + ACTS, "Option B in the feed, phone 390")
    if c == "cover":
        return desk(f'<div class="sk-fbcover">{img(a, "Cover on desktop")}{safe_spans(m)}</div>', "Desktop: the full cover. Dashed: what the phone keeps.") + \
            phone(f'<div class="sk-cropbox sk-c169"><img src="{a}" alt="Cover on a phone, 16:9 crop" loading="lazy"></div>', "Phone: 16:9 centre crop")
    if c in ("story", "reel"):
        top = f'<div class="sk-ui-top"><img src="{av(ch)}" alt="">unifiedmeds</div>'
        bot = '<div class="sk-ui-bot"><span></span></div>' if c == "story" else ""
        return phone(top + img(a, "Option A on a phone") + bot, "Option A with the app's own overlays") + \
            phone(top + img(b, "Option B on a phone") + bot, "Option B with the app's own overlays")
    if c in ("link", "xcard"):
        dom = "[domain]"
        return phone(app_head(ch) + f'<p class="sk-cap">{E(CAPTIONS[ch][2][1].split(chr(10))[0])}</p>' + img(a, "Link preview, Option A") +
                     f'<div class="sk-link"><small>{dom}</small>[Page title, set by the website]</div>' + ACTS, "Option A as a shared link, phone") + \
            phone(app_head(ch) + img(b, "Link preview, Option B") + f'<div class="sk-link"><small>{dom}</small>[Page title]</div>' + ACTS, "Option B as a shared link, phone")
    if c == "event":
        return desk(img(a, "Event cover on desktop") + '<div class="sk-pbody"><span class="sk-pmeta">[Date · time]</span><span class="sk-pname">[Event title]</span><span class="sk-pmeta">Online · hosted by unifiedmeds</span></div>', "Desktop event page", "facebook.com/events/[id]") + \
            phone(img(a, "Event cover on a phone") + '<div class="sk-pbody"><span class="sk-pname">[Event title]</span></div>', "Phone event page")
    if c == "carousel":
        return phone(app_head(ch) + f'<div class="sk-strip">' + "".join(f'<img src="{f}" alt="" loading="lazy">' for f in m["b"]["files"]) + "</div>" + ACTS,
                     "Option B: the capsule runs on when he swipes (three cards side by side here)", wide=True) + \
            phone(app_head(ch) + img(a, "Carousel cover in the feed") + ACTS, "Option A cover in the feed")
    if c == "threads":
        return phone(app_head(ch) + '<p class="sk-cap">[One line of text. The card repeats it, larger.]</p>' + img(a, "Threads card, Option A") + ACTS, "Option A in a Threads post") + \
            phone(app_head(ch) + '<p class="sk-cap">[One line of text.]</p>' + img(b, "Threads card, Option B") + ACTS, "Option B in a Threads post")
    if c == "xheader":
        return desk(f'<div class="sk-xhead">{img(a, "Header on desktop")}{safe_spans(m)}</div>', "Desktop: the full header. The avatar sits over the lower left.", "x.com/[handle]") + \
            phone(f'<div class="sk-cropbox sk-c31"><img src="{a}" alt="Header on a phone" loading="lazy"></div>', "Phone: the same 3:1, smaller; keep type large")
    if c == "xpost":
        return phone(app_head(ch, "@[handle] · [time]") + f'<p class="sk-cap">{E(CAPTIONS[ch][0][1].split(chr(10))[0])}</p>' + img(a, "Option A in the timeline") + ACTS, "Option A in the timeline, phone") + \
            phone(app_head(ch, "@[handle] · [time]") + img(b, "Option B in the timeline") + ACTS, "Option B in the timeline, phone")
    return ""


# ------------------------------------------------------------------ profile mocks
def profile(ch):
    out = []
    for o in ("a", "b"):
        L = o.upper()
        if ch == "facebook":
            cov = f"assets/social/facebook/facebook-cover-{o}.png"
            m = assets_of(ch)["cover"]
            d = (f'<div class="sk-fbcover"><img src="{cov}" width="1640" height="624" alt="Facebook cover, Option {L}" loading="lazy">{safe_spans(m)}</div>'
                 f'<div class="sk-pbody"><img class="sk-pav" src="{av(ch, o)}" alt="Profile picture, Option {L}"><span class="sk-pname">unifiedmeds</span>'
                 f'<span class="sk-pmeta">[Page category] · [n] followers</span><div class="sk-pbtns"><span>Follow</span><span>Message</span></div></div>'
                 f'<div class="sk-ptabs"><b>Posts</b><span>About</span><span>Photos</span><span>Events</span></div>')
            p = (f'<div class="sk-cropbox sk-c169"><img src="{cov}" alt="Facebook cover on a phone, Option {L}" loading="lazy"></div>'
                 f'<div class="sk-pbody"><img class="sk-pav sk-pav--s" src="{av(ch, o)}" alt=""><span class="sk-pname">unifiedmeds</span>'
                 f'<span class="sk-pmeta">[n] followers</span><div class="sk-pbtns"><span>Follow</span><span>Message</span></div></div>'
                 f'<img src="assets/social/facebook/facebook-post-square-{o}.png" alt="" loading="lazy">')
            dcap, pcap, url = "Desktop Page. Dashed: the 16:9 part the phone keeps, and where the profile picture overlaps.", "Phone 390: the cover is cropped to 16:9 at the centre.", "facebook.com/[page]"
        elif ch == "instagram":
            hl = assets_of(ch)["highlights"]
            rings = '<div class="sk-rings">' + "".join(f'<span><img src="{f}" alt="" loading="lazy">{E(lab)}</span>' for f, lab in zip(hl[o]["files"], hl["labels"])) + "</div>"
            bio = BIOS["instagram"][0][1]
            grid = f'<div class="sk-iggrid"><img src="assets/social/instagram/instagram-grid-{o}.png" width="1080" height="1437" alt="Profile grid, Option {L}" loading="lazy"></div>'
            d = (f'<div class="sk-ig"><img class="sk-pav" src="{av(ch, o)}" alt="Profile picture, Option {L}"><div class="sk-pbody">'
                 f'<span class="sk-pname">unifiedmeds</span><div class="sk-stats"><span>[n] posts</span><span>[n] followers</span><span>[n] following</span></div>'
                 f'<p class="sk-pbio">{E(bio)}</p><div class="sk-pbtns"><span>Follow</span><span>Message</span></div></div>{rings}{grid}</div>')
            p = (f'<div class="sk-ig sk-ig--phone"><img class="sk-pav" src="{av(ch, o)}" alt=""><div class="sk-stats"><span>[n] posts</span><span>[n] followers</span></div>'
                 f'<p class="sk-pbio"><b>unifiedmeds</b><br>{E(bio)}</p>{rings}{grid}</div>')
            dcap, pcap, url = "Desktop profile: avatar, bio, five highlights, the grid at 3:4.", "Phone 390: the same order, stacked; the grid is a third of the width per tile.", "instagram.com/[handle]"
        else:
            hd = f"assets/social/x/x-header-{o}.png"
            m = assets_of(ch)["header"]
            bio = BIOS["x"][0][1]
            d = (f'<div class="sk-xhead"><img src="{hd}" width="1500" height="500" alt="X header, Option {L}" loading="lazy">{safe_spans(m)}</div>'
                 f'<div class="sk-pbody"><img class="sk-pav" src="{av(ch, o)}" alt="Profile picture, Option {L}"><span class="sk-pname">unifiedmeds</span>'
                 f'<span class="sk-pmeta">@[handle]</span><p class="sk-pbio">{E(bio)}</p><span class="sk-pmeta">[domain] · Joined [month year]</span></div>'
                 f'<div class="sk-ptabs"><b>Posts</b><span>Replies</span><span>Media</span></div>')
            p = (f'<div class="sk-cropbox sk-c31"><img src="{hd}" alt="X header on a phone, Option {L}" loading="lazy"></div>'
                 f'<div class="sk-pbody"><img class="sk-pav sk-pav--s" src="{av(ch, o)}" alt=""><span class="sk-pname">unifiedmeds</span>'
                 f'<span class="sk-pmeta">@[handle]</span><p class="sk-pbio">{E(bio)}</p></div>')
            dcap, pcap, url = "Desktop profile. Dashed: the band phones keep and the avatar overlap.", "Phone 390: header at 3:1, avatar smaller over its lower left.", "x.com/[handle]"
        out.append(f'<h3>Option {L}.</h3><div class="sk-prof">{desk(d, dcap, url)}'
                   f'<figure><div class="sk-phone"><div class="sk-screen">{p}</div></div><figcaption>{E(pcap)}</figcaption></figure></div>')
    return "".join(out)


# ------------------------------------------------------------------ copy, mobile table, rules
BIOS = {
    "facebook": [("Option A", "Men's health, online. An assessment read by a licensed provider. Assessment only. Not a diagnosis.", 101),
                 ("Option B", "Discretion is part of the treatment. Online assessments, read by licensed providers.", 101)],
    "instagram": [("Option A", "Men's health care, online.\nAn assessment, reviewed by a licensed provider.\nAssessment only. Not a diagnosis.\n[link]", 150),
                  ("Option B", "Discretion is part of the treatment.\nOnline assessment · licensed providers · US only [to confirm]\nAssessment only. Not a diagnosis.", 150)],
    "x": [("Option A", "Men's health care, online. An assessment, reviewed by a licensed provider. Assessment only. Not a diagnosis. [link]", 160),
          ("Option B", "Discretion is part of the treatment. Online assessments, read by licensed providers. Assessment only. Not a diagnosis. [link]", 160)],
}
THREADS_BIO = [("Option A", "Men's health care, online. Same people as @[handle] on Instagram.", 150),
               ("Option B", "Notes from unifiedmeds on care, privacy and the people behind it.", 150)]

CAPTIONS = {
    "facebook": [
        ("Post · Nothing is looked at alone", "Every answer is read by a licensed provider, and they decide the next step with you. Start when it suits you: [link]\n\nAssessment only. Not a diagnosis."),
        ("Event · Questions, answered by a provider", "Bring your general questions about men's health to a live session with a licensed provider, [date · time]. Join here: [event link]\n\nGeneral information only, not advice for any one person."),
        ("Link · Evidence, translated", "What a provider looks at, in plain words. A short read: [link]"),
    ],
    "instagram": [
        ("Feed · Precision is a form of respect", "A licensed provider reads every answer, one person at a time. Link in bio.\n\nAssessment only. Not a diagnosis.\n#unifiedmeds #menshealth"),
        ("Carousel · How the assessment works", "Two steps. Swipe through, then start whenever it suits you: link in bio.\n\nAssessment only. Not a diagnosis.\n#unifiedmeds #menshealth #telehealth"),
        ("Reel · How a provider reads your answers", "What happens after you press send. Captions on.\n\nAssessment only. Not a diagnosis.\n#unifiedmeds"),
    ],
    "x": [
        ("Post · Nothing is looked at alone", "Every answer is read by a licensed provider. They decide the next step with you. Assessment only. Not a diagnosis. [link]"),
        ("Post · Evidence, translated", "What a provider looks at, in plain words: [link]"),
        ("Card · Care that keeps showing up", "Care that keeps showing up, without a waiting room. [link]"),
    ],
}

HASHTAGS = {
    "facebook": "Zero to two hashtags, branded or neutral only (#unifiedmeds, #menshealth). Never a condition, symptom or medicine as a hashtag. Links may sit in the post; use the website URL with UTM tags, never a link that opens the assessment with answers filled in.",
    "instagram": "Three to five hashtags at the end of the caption, branded or neutral (#unifiedmeds, #menshealth, #telehealth). Never a condition, symptom or medicine. Links do not work in captions: the bio link and the story link sticker carry them. Threads: one topic tag per post at most.",
    "x": "Zero or one hashtag (#unifiedmeds or none). Never a condition, symptom or medicine. A website link makes the card appear; keep the copy short so the card does the talking. UTM tags on every link.",
}

MOBILE = {
    "facebook": [
        ("Profile picture", "176 px circle on the Page, 40 px next to posts", "196 px circle, 40 px in the feed", "The mark inside the centre circle", "No type: the mark only"),
        ("Cover", "Full 1640 × 624 (2.63:1)", "16:9 centre crop: the middle 1110 px", "Headline and logo inside x 265 to 1375", "Headline 54 px on the file (about 18 px on a phone)"),
        ("Feed post 1:1 and 4:5", "Shown whole, about 500 px wide", "Shown whole, full phone width", "60 px margin", "Serif 76 px and Inter 30 px on a 1080 file"),
        ("Link share", "Full 1.91:1 under the text", "Full width; some placements crop to 1:1", "The centre square", "Serif 72 px on the file"),
        ("Story", "Opens in a phone-shaped frame", "Full screen 9:16", "Clear of the top and bottom 14%", "Serif 88 px, Inter 30 px"),
        ("Event cover", "Full 1.91:1", "Full width, a little smaller", "5% margin all round", "Serif 84 px on a 1920 file"),
        ("Ad-ready post", "Feed, right column at 1.91:1 (from the Ads page)", "Feed 4:5, Stories 9:16", "Ads page safe areas", "Serif 72 px, legal line 30 px"),
    ],
    "instagram": [
        ("Profile picture", "150 px circle", "86 px circle, 32 px in the feed", "The mark inside the circle", "No type"),
        ("Grid", "3 × 309 px tiles at 3:4", "3 × 129 px tiles at 3:4", "Type inside the 3:4 centre of every post", "Serif lines read only from 104 px on the file"),
        ("Feed post 4:5 and 1:1", "Up to 470 px wide in the feed", "Full phone width", "The 3:4 grid crop", "Serif 76 px, Inter 32 px on a 1080 file"),
        ("Carousel", "Arrows to move", "Swipe; dots under the card", "Grid crop on the cover", "Serif 92 px inside cards"),
        ("Story", "Phone frame in the middle of the screen", "Full screen", "Clear of the top and bottom 14%; link sticker above the reply bar", "Serif 92 px"),
        ("Reel cover", "Reels tab at 9:16; grid at 3:4", "Same", "Title inside the 3:4 crop (y 240 to 1680)", "Serif 84 px"),
        ("Highlight covers", "77 px circles", "64 px circles", "The icon inside the centre circle", "No type on the cover: the label is typed in the app"),
        ("Threads card", "Up to about 560 px wide", "Full width", "60 px margin", "Serif 104 px"),
    ],
    "x": [
        ("Profile picture", "133 px circle on the profile, 40 px on posts", "80 px circle, 40 px on posts", "The mark inside the circle", "No type"),
        ("Header", "Full 3:1, about 600 px wide", "3:1 at phone width; top and bottom trimmed under the status bar", "Type in the band y 60 to 440, clear of the avatar (lower left)", "Serif 56 px on the file (about 15 px on a phone): keep it one short line"),
        ("Post image 16:9", "Full, about 516 px wide", "Full, phone width", "80 px margin", "Serif 100 px on a 1600 file"),
        ("Post image 1:1", "Full, about 516 px wide", "Full, phone width", "60 px margin", "Serif 76 px"),
        ("Card image", "Full 1.91:1 with the domain on top", "Same, phone width", "Lower left clear for the domain label", "Serif 72 px"),
    ],
}

RULES = {
    "facebook": [
        ("Same profile picture as every channel.", "Option A or B from the shared pair; never the full seal or the wordmark at avatar size."),
        ("The cover speaks inside the phone crop.", "Headline and logo sit in the middle 1110 px; the profile picture overlaps the lower left on desktop."),
        ("Ad-ready posts follow the Ads page.", "Nine words or fewer, one Yellow \"Get started\", the legal line inside the art, no medicine, claim, price or review."),
        ("Events are general information.", "A provider at a live event answers general questions only, never one person's case, and says so at the start."),
        ("Comments stay public-safe.", "Never ask about symptoms in comments; move a personal question to a private message and from there to the assessment."),
    ],
    "instagram": [
        ("Plan the grid three posts at a time.", "Pick one rhythm (A checkerboard or B rows) and keep it; every post keeps its type inside the 3:4 grid crop."),
        ("Captions carry the legal line.", "Wherever a post points to the assessment, \"Assessment only. Not a diagnosis.\" appears in the caption, and on the last carousel card."),
        ("Stories keep the edges clear.", "Top and bottom 14% stay free of type; the link sticker sits above the reply bar."),
        ("Highlight covers carry icons, not words.", "The label is typed in the app. Five highlights, in this order: Start, How it works, Privacy, Questions, Delivery."),
        ("Threads is text first.", "An image card only when one line deserves it; same avatar as Instagram."),
    ],
    "x": [
        ("The header clears the avatar.", "Nothing important in the lower left (the profile picture sits there) or in the top and bottom 60 px."),
        ("One idea per post.", "A post image carries one line; the post text never repeats a claim the image does not show."),
        ("Cards carry the link.", "Use the card image on website pages (twitter:image); the lower left stays clear for X's domain label."),
        ("Replies stay general.", "Never discuss a person's health in public replies; point to the assessment or to support."),
    ],
}


def mobile_table(ch):
    rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td></tr>" for a, b, c, d, e in MOBILE[ch])
    return ('<div class="table-wrap"><table><thead><tr><th>Asset</th><th>Desktop shows</th><th>Phone shows</th><th>Keep inside the safe zone</th>'
            f'<th>Smallest type that stays readable on a phone</th></tr></thead><tbody>{rows}</tbody></table></div>')


def copy_section(ch):
    bios = BIOS[ch]
    lab = {"facebook": "Page intro", "instagram": "Instagram bio", "x": "Bio"}[ch]
    out = ['<h3>' + lab + '.</h3><div class="sk-copy">']
    for name, text, limit in bios:
        n = len(text)
        out.append(f'<div class="rule"><b>{name}</b><p>{E(text)}</p><span class="sk-count">{n} of {limit} characters</span></div>')
    out.append("</div>")
    if ch == "instagram":
        out.append('<h3>Threads bio.</h3><div class="sk-copy">')
        for name, text, limit in THREADS_BIO:
            out.append(f'<div class="rule"><b>{name}</b><p>{E(text)}</p><span class="sk-count">{len(text)} of {limit} characters</span></div>')
        out.append("</div>")
    out.append('<h3>Example captions.</h3><div class="sk-copy">')
    for title, text in CAPTIONS[ch]:
        out.append(f'<div class="rule"><b>{E(title)}</b><p>{E(text)}</p></div>')
    out.append(f'<div class="rule rule--do"><b>Hashtags and links.</b><p>{E(HASHTAGS[ch])}</p></div></div>')
    return "".join(out)


def rules_section(ch):
    return '<ol class="sk-rules">' + "".join(f"<li><b>{E(a)}</b> {E(b)}</li>" for a, b in RULES[ch]) + "</ol>"


def files_table(ch):
    rows = []
    for key in CHANNELS[ch]["assets"]:
        m = assets_of(ch)[key]
        w, h = m["size"]
        for o in ("a", "b"):
            for f, s, j in zip(m[o]["files"], m[o]["svgs"], m[o].get("jpgs") or [None] * len(m[o]["files"])):
                name = f.rsplit("/", 1)[1]
                size = kb(f) + (f" · JPG {kb(j)}" if j else "")
                jl = f' · <a class="link" href="{j}" download>JPG</a>' if j else ""
                rows.append(f'<tr><td>{E(m["title"])}</td><td>{o.upper()}</td><td><code>{name}</code></td><td>{w} × {h}</td><td>PNG {size}</td>'
                            f'<td><a class="link" href="{f}" download>PNG</a>{jl} · <a class="link" href="{s}" download>SVG</a></td></tr>')
    return ('<div class="table-wrap"><table><thead><tr><th>Asset</th><th>Option</th><th>File</th><th>Pixels</th><th>File size</th><th>Download</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="cap">Photo-led files over 1 MB also come as JPG (quality 80): upload the JPG where the platform recompresses anyway. SVG files keep live type (DM Serif Display, Inter, loaded from Google Fonts) and link the photos in <code>assets/photos/</code>; open them in a browser or Figma with the fonts installed. '
            'Rebuild every file: <code>python3 -I assets/social/shared/make_social.py</code>, then <code>python3 -I assets/social/shared/build_kit_pages.py</code> and <code>python3 -I tools/build_pages.py</code>.</p>')


def page(ch):
    c = CHANNELS[ch]
    A = assets_of(ch)
    blocks = []
    for key in c["assets"]:
        m = A[key]
        ctx = context(m, ch)
        blocks.append(
            f'<article class="sk-block" id="{ch}-{key}"><header><h3>{E(m["title"])}.</h3><p>{E(m["use"])}</p></header>{spec(m)}'
            f'<div class="sk-pair">{option(m, "a", ch)}{option(m, "b", ch)}</div>'
            + (f'<div class="sk-ctx">{ctx}</div>' if ctx else "") + "</article>")
    toc = '<a href="#profile">Profile</a><a href="#assets">Assets</a><a href="#mobile">Desktop and mobile</a><a href="#copy">Copy</a><a href="#rules">Rules</a><a href="#files">Files</a>'
    asset_toc = " · ".join(f'<a class="link" href="#{ch}-{k}">{E(A[k]["title"])}</a>' for k in c["assets"])
    body = f"""
      <header class="page-head">
        <span class="eyebrow">{E(c["eyebrow"])}</span>
        <h1>{E(c["h1"])}</h1>
        <p class="lead">{E(c["lead"])}</p>
        <nav class="toc" aria-label="On this page">{toc}</nav>
      </header>
      <div class="grid-2"><div class="rule"><span class="status status--current">Current</span><p>{E(c["status"])} Shared rules for every channel: <a class="link" href="social.html">Social overview</a>.</p></div>
      <div class="rule"><span class="status status--proposed">To confirm</span><p>Option A or B per asset (Avi). Photos are Pexels stand-ins, not approved, to replace before anything is posted (R-39, O-13).</p></div></div>

      <section class="sec" id="profile" aria-labelledby="profile-h">
        <div class="sec-head"><h2 id="profile-h">The profile, desktop and mobile.</h2><p>The kit's profile picture and banner in place, on a desktop browser and on a 390 phone. Dashed lines mark what each screen crops or covers.</p></div>
        {profile(ch)}
      </section>

      <section class="sec sk-kit" id="assets" aria-labelledby="assets-h">
        <div class="sec-head"><h2 id="assets-h">The asset set.</h2><p>One block per asset: the use, the exact size, the safe zones, then Option A (calm, photo-led) and Option B (graphic, the capsule kit) side by side, and the asset in its real context.</p></div>
        <label class="sk-toggle"><input type="checkbox" checked> Show safe zones</label>
        <p class="cap">{asset_toc}</p>
        {"".join(blocks)}
      </section>

      <section class="sec" id="mobile" aria-labelledby="mobile-h">
        <div class="sec-head"><h2 id="mobile-h">Mobile and desktop differences.</h2><p>Most people meet this channel on a phone. Sizes in px are on the exported file unless marked; display sizes are approximate and platforms change them, so check before a campaign.</p></div>
        {mobile_table(ch)}
      </section>

      <section class="sec" id="copy" aria-labelledby="copy-h">
        <div class="sec-head"><h2 id="copy-h">Captions and copy.</h2><p>Discreet, plain and short. No prescription names in any social asset or caption, no promise of results, no before and after. Square brackets mark what Avi or legal fills in.</p></div>
        {copy_section(ch)}
      </section>

      <section class="sec" id="rules" aria-labelledby="rules-h">
        <div class="sec-head"><h2 id="rules-h">Rules for this channel.</h2><p>On top of the shared social rules and the rules on <a class="link" href="content.html">Voice and compliance</a>.</p></div>
        {rules_section(ch)}
      </section>

      <section class="sec" id="files" aria-labelledby="files-h">
        <div class="sec-head"><h2 id="files-h">Files.</h2><p>Every file at its exact size. PNG to upload; SVG to edit.</p></div>
        {files_table(ch)}
      </section>
"""
    (EXT / "src" / c["page"]).write_text(CSS + body)
    print("wrote", c["page"])


if __name__ == "__main__":
    for ch in CHANNELS:
        page(ch)
