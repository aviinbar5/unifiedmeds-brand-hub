"""YouTube kit: art, PNG exports, previews and the hub page src/social-youtube.html.

Run:  python3 -I assets/social/youtube/make.py   (add --page to rebuild only the page)
Hub page status: Current (hub merge 18.11.2026).
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sk_kit as k  # noqa: E402
from sk_kit import C, esc  # noqa: E402

OUT = k.HERE
PREV = OUT / "preview"
REL = "assets/social/youtube/"
SHORTS = k.V(safe=(60, 200, 880, 1400))     # Shorts: rail 200 on the right, title and channel in the bottom 520
ASSETS = {}

# Banner areas (YouTube channel art, 2560 x 1440)
TV = (0, 0, 2560, 1440)
DESK = (0, 508, 2560, 423)
TAB = (352, 508, 1855, 423)
SAFE = (507, 508, 1546, 423)
THUMB_TIME = (1070, 630, 190, 70)          # the duration badge, bottom right of a thumbnail


def art_avatar(o, s=800):
    return k.shared_avatar(o, s)


def art_banner(o):
    b = []
    x0, y0, w, h = SAFE
    if o == "a":
        b.append(k.rect(0, 0, 2560, 1440, C["paper"]))
        b.append(k.capsule(-260, 1080, 1000, stroke=C["line_base"], sw=24))
        b.append(k.logo("logo-seal", x0 + 30, y0 + 36, h=124)[0])
        b.append(k.text(x0 + 30, y0 + 268, ["Care that keeps", "showing up."], 92, C["teal_deep"], lh=1.06))
        b.append(k.photo("man-reading-window-wide-2048-pexels-8217708.jpg", x0 + 780, y0 + 20, 736, 383, .56, .3, r=24))
    else:
        b.append(k.rect(0, 0, 2560, 1440, C["deep_teal"]))
        b.append(k.capsule(2110, 560, 900, stroke=C["sky"], sw=24, inner=C["logo_blue"], gap=32))
        b.append(k.capsule(-560, 600, 980, stroke=C["sky"], sw=24))
        b.append(k.logo("logo-seal-reversed", x0 + 60, y0 + 110, h=200)[0])
        b.append(k.text(x0 + 700, y0 + 190, ["Care that keeps", "showing up."], 92, C["paper"], lh=1.06))
    return k.doc(2560, 1440, "".join(b))


def art_thumb(o):
    b = []
    if o == "a":
        b.append(k.rect(0, 0, 1280, 720, C["paper"]))
        b.append(k.photo("man-kitchen-coffee-pexels-6269909.jpg", 540, 0, 740, 720, .58, .3))
        b.append(k.logo("logo-seal", 56, 56, h=56)[0])
        b.append(k.text(60, 300, "EXPLAINER", 30, C["slate"], "sans", 600, ls="0.06em"))
        b.append(k.text(56, 420, ["How it", "works."], 130, C["teal_deep"], lh=1.0))
    else:
        b.append(k.rect(0, 0, 1280, 720, C["deep_teal"]))
        b.append(k.capsule(860, 210, 700, stroke=C["sky"], sw=18, inner=C["logo_blue"], gap=24))
        b.append(k.capsule(1010, -130, 300, vertical=True, stroke=C["sky"], sw=18))
        b.append(k.logo("logo-seal-reversed", 56, 56, h=56)[0])
        b.append(k.text(60, 300, "EXPLAINER", 30, C["wash_blue"], "sans", 600, ls="0.06em"))
        b.append(k.text(56, 440, ["How it", "works."], 150, C["paper"], lh=0.98))
    return k.doc(1280, 720, "".join(b))


def art_endscreen(o):
    b = []
    dark = o == "b"
    ground, slot, tc, sc = ((C["deep_teal"], C["line_on_dark"], C["paper"], C["wash_blue"]) if dark
                            else (C["paper"], C["mist"], C["teal_deep"], C["slate"]))
    b.append(k.rect(0, 0, 1920, 1080, ground))
    if dark:
        b.append(k.capsule(-240, 960, 760, stroke=C["sky"], sw=20))
    else:
        b.append(k.capsule(-240, 960, 760, stroke=C["line_base"], sw=20))
    for (x, y, w, h) in ENDS["video"]:
        b.append(k.rect(x, y, w, h, slot, r=16))
    cx, cy, r = ENDS["subscribe"]
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{slot}"/>')
    b.append(k.logo("logo-seal-reversed" if dark else "logo-seal", 140, 150, h=80)[0])
    b.append(k.text(140, 420, ["Watch next."], 110, tc))
    b.append(k.text(140, 500, ["One plain explainer at a time."], 36, sc, "sans", 400))
    return k.doc(1920, 1080, "".join(b))


ENDS = {"video": [(1040, 150, 740, 416), (1040, 610, 740, 416)], "subscribe": (300, 780, 150)}


def art_lower(o):
    b = []
    x, y, h = 96, 836, 150
    name, role = "[Name], [credentials]", "[Role, for example licensed provider]"
    w = max(k.est(name, 44, "sans", 600), k.est(role, 30, "sans")) + 290
    if o == "a":
        b.append(k.rect(x, y, w, h, C["paper"], r=12))
        b.append(k.logo("logo-seal", x + 32, y + 46, h=58)[0])
        b.append(k.rect(x + 210, y + 32, 2, h - 64, C["line_base"]))
        b.append(k.text(x + 240, y + 70, name, 44, C["teal_deep"], "sans", 600))
        b.append(k.text(x + 240, y + 116, role, 30, C["slate"], "sans", 400))
    else:
        b.append(k.rect(x, y, w, h, C["deep_teal"], r=12))
        b.append(k.logo("logo-seal-reversed", x + 32, y + 46, h=58)[0])
        b.append(k.rect(x + 210, y + 32, 2, h - 64, C["line_on_dark"]))
        b.append(k.text(x + 240, y + 70, name, 44, C["paper"], "sans", 600))
        b.append(k.text(x + 240, y + 116, role, 30, C["wash_blue"], "sans", 400))
    return k.doc(1920, 1080, "".join(b))


def art_title(o):
    b = []
    if o == "a":
        b.append(k.rect(0, 0, 1920, 1080, C["paper"]))
        b.append(k.photo("man-reading-window-wide-2048-pexels-8217708.jpg", 0, 0, 900, 1080, .58, .3))
        b.append(k.text(1020, 400, "EPISODE [01]", 32, C["slate"], "sans", 600, ls="0.06em"))
        b.append(k.text(1020, 520, ["How the", "assessment", "works."], 112, C["teal_deep"], lh=1.06))
        b.append(k.logo("logo-seal", 1020, 900, h=70)[0])
    else:
        b.append(k.rect(0, 0, 1920, 1080, C["deep_teal"]))
        b.append(k.capsule(1240, 620, 1000, stroke=C["sky"], sw=22, inner=C["logo_blue"], gap=30))
        b.append(k.capsule(1560, -170, 420, vertical=True, stroke=C["sky"], sw=22))
        b.append(k.text(160, 330, "EPISODE [01]", 32, C["wash_blue"], "sans", 600, ls="0.06em"))
        b.append(k.text(160, 460, ["How the", "assessment", "works."], 124, C["paper"], lh=1.04))
        b.append(k.logo("logo-seal-reversed", 160, 880, h=70)[0])
    return k.doc(1920, 1080, "".join(b))


def art_watermark(o):
    if o == "a":
        return k.doc(150, 150, k.logo("app-icon", 0, 0, w=150)[0])
    w = 128
    return k.doc(150, 150, k.rect(0, 0, 150, 150, C["paper"], r=24) + k.logo("logo-seal", 11, 75 - w / k.logo_ratio("logo-seal") / 2, w=w)[0])


def build_art():
    jobs = []

    def add(name, svg, w, h, transparent=False):
        p = OUT / f"{name}.svg"
        k.write(p, svg)
        jobs.append((p, OUT / f"{name}.png", w, h, transparent))
        ASSETS[name] = (w, h, transparent)

    for o in "ab":
        add(f"youtube-avatar-{o}", art_avatar(o), 800, 800)
        add(f"youtube-banner-{o}", art_banner(o), 2560, 1440)
        add(f"youtube-thumb-{o}", art_thumb(o), 1280, 720)
        add(f"youtube-shorts-{o}", k.vframe("cover", o, dict(text="Things you don’t have to do.", kicker="SHORTS",
                                                              photo="man-kitchen-coffee-pexels-6269909.jpg", fx=.55, fy=.3), SHORTS), 1080, 1920)
        add(f"youtube-endscreen-{o}", art_endscreen(o), 1920, 1080)
        add(f"youtube-lowerthird-{o}", art_lower(o), 1920, 1080, True)
        add(f"youtube-titlecard-{o}", art_title(o), 1920, 1080)
        add(f"youtube-watermark-{o}", art_watermark(o), 150, 150, True)
    k.write(OUT / "youtube-safe-banner.svg", k.overlay(
        2560, 1440, s=2.4, keep=[], safe=SAFE, guides=[DESK, TAB],
        labels=[(1280, 485, "Desktop 2560 × 423 (dotted)", "middle"), (1280, 1000, "Every device 1546 × 423 (dashed) · tablet 1855 × 423 (dotted)", "middle"),
                (1280, 120, "TV shows all 2560 × 1440", "middle")]))
    k.write(OUT / "youtube-safe-avatar.svg", k.overlay(800, 800, circle=(400, 400, 400), s=1.0))
    k.write(OUT / "youtube-safe-thumb.svg", k.overlay(
        1280, 720, s=1.0, keep=[THUMB_TIME], safe=(48, 40, 1184, 640), labels=[(1165, 615, "Duration", "middle")]))
    sx0, sy0, sx1, sy1 = SHORTS.x0, SHORTS.y0, SHORTS.x1, SHORTS.y1
    k.write(OUT / "youtube-safe-shorts.svg", k.overlay(
        1080, 1920, s=1.6, keep=[(0, 0, 1080, sy0), (sx1, sy0, 1080 - sx1, sy1 - sy0), (0, sy1, 1080, 1920 - sy1)],
        safe=(sx0, sy0, sx1 - sx0, sy1 - sy0),
        labels=[(540, 120, "Search and menu · 200", "middle"), (980, 900, "Rail", "middle"),
                (540, 1680, "Title, channel, subscribe · 520", "middle"), (470, 1375, "Safe 820 × 1200", "middle")]))
    vids = [(x, y, w, h) for (x, y, w, h) in ENDS["video"]]
    cx, cy, r = ENDS["subscribe"]
    k.write(OUT / "youtube-safe-endscreen.svg", k.overlay(
        1920, 1080, s=1.4, keep=vids + [(cx - r, cy - r, 2 * r, 2 * r)], safe=(96, 54, 1728, 972),
        labels=[(1410, 370, "Video element", "middle"), (1410, 830, "Video element", "middle"), (cx, cy + 10, "Subscribe", "middle"),
                (960, 1040, "Title-safe 1728 × 972", "middle")]))
    k.write(OUT / "youtube-safe-video.svg", k.overlay(
        1920, 1080, s=1.4, keep=[(1920 - 96 - 150, 1080 - 54 - 150, 150, 150)], safe=(96, 54, 1728, 972),
        labels=[(960, 110, "Title-safe 1728 × 972", "middle"), (1599, 820, "Watermark", "middle")]))
    k.export(jobs)
    for name in ASSETS:
        k.jpg_copy(OUT / f"{name}.png")
    for name, (w, h, tr) in ASSETS.items():
        k.preview(OUT / f"{name}.png", PREV / f"{name}.{'png' if tr else 'jpg'}", 640 if h > w else 960)


# ---------------------------------------------------------------- page
def pv(name):
    w, h, tr = ASSETS[name]
    return f"{REL}preview/{name}.{'png' if tr else 'jpg'}"


def links(name):
    jpg = [("JPG", f"{REL}{name}.jpg")] if (OUT / f"{name}.jpg").exists() else []
    return [("PNG", f"{REL}{name}.png")] + jpg + [("SVG", f"{REL}{name}.svg")]


def asset(id_, title, use, spec, figs, ctx="", pair_cls="sk-pair"):
    return (f'<article class="sk-asset" id="{id_}"><h3>{esc(title)}</h3><p>{use}</p>{k.spec_dl(spec)}'
            f'{k.toggle()}<div class="{pair_cls}">{figs}</div>{ctx}</article>')


def banner_crop(o, area, alt):
    x, y, w, h = area
    return k.crop_img(pv(f"youtube-banner-{o}"), 2560, 1440, x, y, w, h, alt)


def profile_row(o):
    av = pv(f"youtube-avatar-{o}")
    thumbs = [f"youtube-thumb-{o}", f"youtube-titlecard-{o}", f"youtube-thumb-{'b' if o == 'a' else 'a'}", f"youtube-endscreen-{o}"]
    grid = "".join(f'<div class="yt-v"><img src="{pv(t)}" alt="" loading="lazy"><span class="sk-bar"></span><span class="sk-bar yt-short"></span></div>' for t in thumbs)
    desk = f"""<figure><div class="sk-desk"><div class="yt-d">
      {banner_crop(o, DESK, f'Banner option {o.upper()}, desktop crop')}
      <div class="yt-head sk-m"><div class="sk-dot yt-av"><img src="{av}" alt="Profile picture, option {o.upper()}"></div>
        <div class="yt-id"><b>unifiedmeds</b><span>[@unifiedmeds] · [0] subscribers · [0] videos</span><span>{esc(ABOUT[0][:70])}…</span><span class="yt-btn">Subscribe</span></div></div>
      <div class="yt-tabs sk-m"><b>Home</b><span>Videos</span><span>Shorts</span><span>Playlists</span></div>
      <div class="yt-grid4">{grid}</div></div></div>
      <figcaption><b>Desktop · youtube.com</b> · the banner shows as a 2560 × 423 strip; avatar 160 px.</figcaption></figure>"""
    shorts = "".join(f'<img src="{pv(t)}" alt="" loading="lazy">' for t in (f"youtube-shorts-{o}", f"youtube-shorts-{'b' if o == 'a' else 'a'}"))
    phone = f"""<figure><div class="sk-phone"><div class="yt-p sk-m">
      {banner_crop(o, SAFE, f'Banner option {o.upper()}, phone crop')}
      <div class="yt-p-id"><div class="sk-dot yt-p-av"><img src="{av}" alt="Profile picture, option {o.upper()}, on a phone"></div><div><b>unifiedmeds</b><span>[@unifiedmeds]</span></div></div>
      <span class="yt-btn yt-btn--full">Subscribe</span>
      <div class="yt-tabs sk-m"><b>Home</b><span>Videos</span><span>Shorts</span></div>
      <div class="yt-v"><img src="{pv(f'youtube-thumb-{o}')}" alt="" loading="lazy"><span class="sk-bar"></span></div>
      <div class="yt-shorts">{shorts}</div></div></div>
      <figcaption><b>Phone · 390 wide</b> · only the centre 1546 × 423 of the banner shows; avatar 72 pt.</figcaption></figure>"""
    return f'<h3 class="yt-row-h">Option {o.upper()} · {"editorial, photo-led" if o == "a" else "graphic, colour-led"}</h3><div class="sk-ctx">{desk}{phone}</div>'


ABOUT = [
    "Plain explainers on men’s health care online: how the assessment works, who reviews it and what happens next. Assessment only. Not a diagnosis.",
    "unifiedmeds is men’s health care, online and discreet. Short videos on how it works, from the people who run it. Assessment only. Not a diagnosis.",
]
TITLES = [
    ("How the assessment works", "Tell us what’s changed. A licensed provider reviews your information. Receive a personalized care plan. Stay supported. This video walks through each step.\nAssessment only. Not a diagnosis.\n[unifiedmeds.com]\n#unifiedmeds #menshealth"),
    ("Who reads your answers", "A licensed provider reviews every assessment. Here is what that means, and what it does not.\nAssessment only. Not a diagnosis.\n[unifiedmeds.com]\n#unifiedmeds #telehealth"),
    ("Things you don’t have to do  #Shorts", "No waiting room. No explaining it out loud.\nAssessment only. Not a diagnosis.\n#unifiedmeds #Shorts"),
]


def page():
    css = k.PAGE_CSS + """
  .yt-row-h { margin-top: var(--space-6); font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); color: var(--color-text-strong); }
  .yt-d { display: grid; gap: var(--space-3); padding: var(--space-3); }
  .yt-d > .sk-crop { border-radius: var(--radius-xs); }
  .yt-head { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 5fr); gap: var(--space-4); align-items: center; }
  .yt-av { width: 100%; aspect-ratio: 1; }
  .yt-id, .yt-p { display: grid; gap: var(--space-1); justify-items: start; font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); min-width: 0; }
  .yt-id b, .yt-p b { font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); }
  .yt-id span:not(.yt-btn) { color: var(--color-text-secondary); }
  .yt-btn { padding: var(--space-1) var(--space-4); border-radius: var(--radius-pill); background: var(--color-brand-teal-deep); color: var(--color-text-on-dark); }
  .yt-btn--full { justify-self: stretch; text-align: center; margin: 0 var(--space-3); }
  .yt-tabs { display: flex; gap: var(--space-5); padding: 0 var(--space-3) var(--space-2); border-bottom: 1px solid var(--color-line-base); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); justify-self: stretch; }
  .yt-grid4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--space-3); }
  .yt-v { display: grid; gap: var(--space-1); }
  .yt-v img { display: block; width: 100%; height: auto; border-radius: var(--radius-xs); }
  .yt-v .sk-bar { height: var(--space-2); }
  .yt-v .yt-short { width: 60%; }
  .yt-p { padding-bottom: var(--space-3); }
  .yt-p > .sk-crop { justify-self: stretch; }
  .yt-p > .yt-v, .yt-p > .yt-shorts { justify-self: stretch; padding: 0 var(--space-3); }
  .yt-p-id { display: flex; gap: var(--space-3); align-items: center; padding: var(--space-2) var(--space-3) 0; }
  .yt-p-id > div:last-child { display: grid; }
  .yt-p-id span { color: var(--color-text-secondary); }
  .yt-p-av { width: var(--space-14); aspect-ratio: 1; }
  .yt-shorts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-2); }
  .yt-shorts img { display: block; width: 100%; height: auto; border-radius: var(--radius-xs); }
  .yt-crops { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-4); width: 100%; }
  .yt-crops figure { margin: 0; display: grid; gap: var(--space-2); justify-items: stretch; }
  .yt-crops .sk-crop { border-radius: var(--radius-xs); box-shadow: 0 0 0 1px var(--color-line-mid); }
  .yt-at168 { display: flex; flex-wrap: wrap; gap: var(--space-6); align-items: start; justify-content: center; }
  .yt-at168 figure { margin: 0; display: grid; gap: var(--space-2); }
  .yt-at168 img { display: block; width: calc(var(--space-24) + var(--space-18)); height: auto; border-radius: var(--radius-xs); }
  .yt-list { display: grid; gap: var(--space-3); padding: var(--space-3); }
  .yt-list > div { display: grid; grid-template-columns: 43% minmax(0, 1fr); gap: var(--space-2); }
  .yt-list img { display: block; width: 100%; height: auto; border-radius: var(--radius-xs); }
  .yt-list span { display: grid; gap: var(--space-1); align-content: start; }
  .yt-list .sk-bar { height: var(--space-2); }
  .yt-player { position: relative; }
  .yt-player > img:first-child { display: block; width: 100%; height: auto; }
  .yt-wm { position: absolute; right: 5%; bottom: 5%; width: 7.8%; opacity: 0.85; }
  .yt-wm img { display: block; width: 100%; height: auto; }
"""
    A = []
    A.append(asset(
        "avatar", "Profile picture",
        "Shown as a circle: 160 px on the channel page, 72 pt on a phone, 24 to 36 px next to every video. The logo files as they are.",
        [("Size", "800 × 800 px"), ("Ratio", "1:1, cropped to a circle"), ("Type", "PNG or JPG"), ("Max file", "4 MB"), ("Safe zone", "The inscribed circle")],
        k.opt_fig("A", "The \u201cu|m\u201d mark in Navy on Cream, the same in all six kits. Light and calm, reads at every size.", pv("youtube-avatar-a"), 800, 800, links("youtube-avatar-a"), f"{REL}youtube-safe-avatar.svg", "sk-art--sq")
        + k.opt_fig("B", "The app icon, “u|m” on Navy (R-93). The only one that reads at 24 px.", pv("youtube-avatar-b"), 800, 800, links("youtube-avatar-b"), f"{REL}youtube-safe-avatar.svg", "sk-art--sq")))
    crops = lambda o: f"""<div class="yt-crops">{''.join(f'<figure>{banner_crop(o, a, n)}<figcaption class="cap"><b>{n}</b> · {d}</figcaption></figure>' for a, n, d in ((TV, 'TV', '2560 × 1440, all of it'), (DESK, 'Desktop', '2560 × 423'), (TAB, 'Tablet', '1855 × 423'), (SAFE, 'Phone', '1546 × 423, the safe area')))}</div>"""
    A.append(asset(
        "banner", "Channel banner",
        "One file, four crops. A TV shows all of it, a desktop a wide strip, a phone only the centre. The logo and the line live in the centre 1546 × 423; everything outside is mood.",
        [("Size", "2560 × 1440 px"), ("Ratio", "16:9"), ("Type", "PNG or JPG"), ("Max file", "6 MB"), ("Safe zone", "1546 × 423, centred (x 507, y 508)")],
        k.opt_fig("A", "Paper, the seal and the line on the left, a photo in a rounded window. Everything inside the safe area.", pv("youtube-banner-a"), 2560, 1440, links("youtube-banner-a"), f"{REL}youtube-safe-banner.svg")
        + k.opt_fig("B", "Deep Teal, the reversed seal large, two capsules that only desktop and TV show.", pv("youtube-banner-b"), 2560, 1440, links("youtube-banner-b"), f"{REL}youtube-safe-banner.svg"),
        ctx=f'<div class="sk-ctx sk-ctx--even"><figure>{crops("a")}<figcaption><b>Option A</b> in every crop.</figcaption></figure><figure>{crops("b")}<figcaption><b>Option B</b> in every crop.</figcaption></figure></div>'))
    at168 = "".join(f'<figure><img src="{pv(f"youtube-thumb-{o}")}" alt="Thumbnail option {o.upper()} at 168 px wide"><figcaption class="cap"><b>Option {o.upper()}</b> at 168 px</figcaption></figure>' for o in "ab")
    lst = "".join(f'<div><img src="{pv(f"youtube-thumb-{o}")}" alt=""><span><span class="sk-bar"></span><span class="sk-bar" style="width: 70%;"></span></span></div>' for o in "abab")
    A.append(asset(
        "thumb", "Thumbnail",
        "The poster for every long video. It must read at 168 px wide, the size in the phone’s list and in “Up next”. Three words or fewer, no face under type, nothing in the bottom right where the duration sits.",
        [("Size", "1280 × 720 px"), ("Ratio", "16:9"), ("Type", "JPG or PNG"), ("Max file", "2 MB"), ("Safe zone", "Bottom right 210 × 90 under the duration badge")],
        k.opt_fig("A", "Paper panel, “How it works.” in DM Serif 130, the photo on the right.", pv("youtube-thumb-a"), 1280, 720, links("youtube-thumb-a"), f"{REL}youtube-safe-thumb.svg")
        + k.opt_fig("B", "Deep Teal, the words at 150, a split capsule cropped by the right edge.", pv("youtube-thumb-b"), 1280, 720, links("youtube-thumb-b"), f"{REL}youtube-safe-thumb.svg"),
        ctx=f'<div class="sk-ctx"><figure><div class="yt-at168">{at168}</div><figcaption><b>At 168 px</b> · the headline is about 17 px tall: still readable. Anything under 90 px at full size disappears.</figcaption></figure><figure><div class="sk-phone"><div class="yt-list">{lst}</div></div><figcaption><b>Phone · list</b> · thumbnails at about 43% of the screen.</figcaption></figure></div>'))
    A.append(asset(
        "shorts", "Shorts cover",
        "The still for a Short in the Shorts shelf and on the channel. Same layout as the TikTok cover, with YouTube’s wider rail and taller bottom.",
        [("Size", "1080 × 1920 px"), ("Ratio", "9:16"), ("Type", "Frame from the video"), ("Max file", "Part of the video upload"), ("Safe zone", "x 60 to 880, y 200 to 1400")],
        k.opt_fig("A", "Paper panel and serif headline, the photo below.", pv("youtube-shorts-a"), 1080, 1920, links("youtube-shorts-a"), f"{REL}youtube-safe-shorts.svg", "sk-art--tall")
        + k.opt_fig("B", "Deep Teal, the headline large, two capsules at the edges.", pv("youtube-shorts-b"), 1080, 1920, links("youtube-shorts-b"), f"{REL}youtube-safe-shorts.svg", "sk-art--tall")))
    A.append(asset(
        "endscreen", "End screen",
        "The last 5 to 20 seconds of a long video. The art leaves room for YouTube’s own elements: two videos on the right, Subscribe on the left. Place them in YouTube Studio exactly on the panels.",
        [("Size", "1920 × 1080 px"), ("Ratio", "16:9"), ("Type", "Frames in the edit (5 to 20 s)"), ("Max file", "Part of the video"), ("Safe zone", "Elements inside the title-safe 1728 × 972")],
        k.opt_fig("A", "Paper, Mist panels where the elements land.", pv("youtube-endscreen-a"), 1920, 1080, links("youtube-endscreen-a"), f"{REL}youtube-safe-endscreen.svg")
        + k.opt_fig("B", "Deep Teal, panels in Line on dark.", pv("youtube-endscreen-b"), 1920, 1080, links("youtube-endscreen-b"), f"{REL}youtube-safe-endscreen.svg")))
    A.append(asset(
        "lowerthird", "Lower third",
        "Names the person speaking: a provider or a member of the team, only with written consent. Transparent PNG over the video, inside title-safe.",
        [("Size", "1920 × 1080 px, transparent"), ("Ratio", "16:9"), ("Type", "PNG with alpha (or MOV in the edit)"), ("Max file", "Part of the video"), ("Safe zone", "x 96 or more, bottom edge at 986")],
        k.opt_fig("A", "Paper card, the seal, name in Inter SemiBold 44, role in Slate.", pv("youtube-lowerthird-a"), 1920, 1080, links("youtube-lowerthird-a"), f"{REL}youtube-safe-video.svg", "sk-art--chk")
        + k.opt_fig("B", "Deep Teal card, the reversed seal, Paper and Wash Blue type.", pv("youtube-lowerthird-b"), 1920, 1080, links("youtube-lowerthird-b"), f"{REL}youtube-safe-video.svg", "sk-art--chk"),
        ctx=f'<div class="sk-ctx sk-ctx--even">{"".join(f"""<figure><div class="yt-player"><img src="{pv('youtube-titlecard-a')}" alt=""><img class="sk-ui" src="{pv(f'youtube-lowerthird-{o}')}" alt="Lower third option {o.upper()} over a frame"></div><figcaption><b>Option {o.upper()}</b> over a frame. On a phone the name stays at least 16 px tall.</figcaption></figure>""" for o in "ab")}</div>'))
    A.append(asset(
        "titlecard", "Title card",
        "Opens a long video after the logo sting (R-101), or marks a chapter. Four seconds, no sound needed.",
        [("Size", "1920 × 1080 px"), ("Ratio", "16:9"), ("Type", "Frame in the edit; PNG for reference"), ("Max file", "Part of the video"), ("Safe zone", "Title-safe 1728 × 972")],
        k.opt_fig("A", "Photo on the left, Paper on the right, the title in DM Serif 112.", pv("youtube-titlecard-a"), 1920, 1080, links("youtube-titlecard-a"), f"{REL}youtube-safe-video.svg")
        + k.opt_fig("B", "Deep Teal, the title at 124, two capsules on the right.", pv("youtube-titlecard-b"), 1920, 1080, links("youtube-titlecard-b"), f"{REL}youtube-safe-video.svg")))
    A.append(asset(
        "watermark", "Watermark",
        "YouTube’s branding watermark: a small mark in the bottom right of the player that becomes a Subscribe button. Transparent PNG.",
        [("Size", "150 × 150 px"), ("Ratio", "1:1"), ("Type", "PNG, transparent"), ("Max file", "1 MB"), ("Safe zone", "Whole file; YouTube places it")],
        k.opt_fig("A", "The app icon (R-93).", pv("youtube-watermark-a"), 150, 150, links("youtube-watermark-a"), None, "sk-art--sq sk-art--chk")
        + k.opt_fig("B", "The Primary seal on a Paper square, for when the full name should show.", pv("youtube-watermark-b"), 150, 150, links("youtube-watermark-b"), None, "sk-art--sq sk-art--chk"),
        ctx=f'<div class="sk-ctx sk-ctx--even">{"".join(f"""<figure><div class="yt-player"><img src="{pv('youtube-titlecard-b')}" alt=""><span class="yt-wm"><img src="{pv(f'youtube-watermark-{o}')}" alt="Watermark option {o.upper()} in the player"></span></div><figcaption><b>Option {o.upper()}</b> in the player. On a phone it is about 20 px, so Option A reads better.</figcaption></figure>""" for o in "ab")}</div>'))

    mobile_rows = [
        ("Profile picture", "Circle, 160 px", "Circle, 72 pt; 24 px beside comments", "The inscribed circle", "Both options at any size, down to 24 px"),
        ("Channel banner", "2560 × 423 strip", "1546 × 423, the centre only", "1546 × 423, centred", "Line 80 px or larger (about 12 pt on a phone)"),
        ("Thumbnail", "About 360 px wide in the grid", "168 px wide in lists; full width in the home feed", "Clear of the bottom right 210 × 90", "Headline 110 px or larger"),
        ("Shorts cover", "In the Shorts shelf, 9:16", "Full screen under the rail and title", "x 60 to 880, y 200 to 1400", "Headline 100 px or larger"),
        ("End screen", "Elements at their set size", "Elements shrink; the panels still line up", "Title-safe 1728 × 972", "Line 110 px; sub 36 px"),
        ("Lower third", "Over the video", "Same; the video is about 390 pt wide", "x 96 or more, above y 986", "Name 44 px, role 30 px"),
        ("Watermark", "About 60 px in the player", "About 20 px", "YouTube places it", "Option A only below 30 px"),
    ]
    mobile = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in mobile_rows)
    files = []
    for name, (w, h, tr) in sorted(ASSETS.items()):
        files.append((name + ".png", f"{w} × {h}" + (", transparent" if tr else ""), k.size_label(OUT / f"{name}.png")))
        if (OUT / f"{name}.jpg").exists():
            files.append((name + ".jpg", f"{w} × {h}, JPG 80 (the PNG is over 1 MB)", k.size_label(OUT / f"{name}.jpg")))
        files.append((name + ".svg", "Source", k.size_label(OUT / f"{name}.svg")))
    for n, d in (("youtube-safe-banner.svg", "Banner safe areas"), ("youtube-safe-thumb.svg", "Thumbnail template"),
                 ("youtube-safe-shorts.svg", "Shorts safe zone"), ("youtube-safe-endscreen.svg", "End screen element map"),
                 ("youtube-safe-video.svg", "Title-safe and watermark"), ("youtube-safe-avatar.svg", "Avatar crop"),
                 ("make.py", "Generator: rebuilds every file and this page"), ("sk_kit.py", "Shared helpers")):
        files.append((n, d, k.size_label(OUT / n)))
    ftable = "".join(f'<tr><td data-label="File"><a class="link" href="{REL}{n}" download>{n}</a></td><td data-label="Size">{s}</td><td data-label="Weight">{wt}</td></tr>' for n, s, wt in files)
    body = f"""      <header class="page-head">
        <span class="eyebrow">Marketing · Social</span>
        <h1>YouTube.</h1>
        <p class="lead">The unifiedmeds YouTube channel: profile, banner, thumbnails, Shorts covers, end screens, lower thirds, title cards and the watermark. Two options for each, A (editorial, photo-led) and B (graphic, colour-led), on a desktop and on a phone.</p>
        <nav class="toc" aria-label="On this page"><a href="#profile">Profile</a><a href="#assets">Asset set</a><a href="#mobile">Mobile and desktop</a><a href="#copy">Captions and copy</a><a href="#rules">Rules</a><a href="#files">Files</a></nav>
      </header>

      <div class="grid-2"><div class="rule"><span class="status status--current">Current</span><p>The kit is approved for use. The profile picture is Option B, the white u|m on Navy (R-93, U-27). Legal approves every video, title and description before it runs (U-30). Sizes follow YouTube’s published specs; check them again before the channel opens.</p></div>
      <div class="rule"><span class="status status--proposed">To confirm</span><p>Option A or B per asset (Avi). Lines are candidates; handles and links are placeholders. Photos are Pexels stand-ins, not approved, to replace (R-39, O-13).</p></div></div>

      <section class="sec" id="profile" aria-labelledby="profile-h">
        <div class="sec-head"><h2 id="profile-h">The profile, desktop and mobile.</h2><p>The channel page on youtube.com and in the app. The banner is the same file; the phone shows only its centre.</p></div>
        {profile_row('a')}
        {profile_row('b')}
      </section>

      <section class="sec" id="assets" aria-labelledby="assets-h">
        <div class="sec-head"><h2 id="assets-h">The asset set.</h2><p>Each block: use, exact size, safe zone (the dashed overlay; switch it off to see the art) and Option A beside Option B. Coral marks what YouTube covers; dotted blue lines are the other crops.</p></div>
        {''.join(A)}
      </section>

      <section class="sec" id="mobile" aria-labelledby="mobile-h">
        <div class="sec-head"><h2 id="mobile-h">Mobile and desktop differences.</h2><p>Most viewing is on phones and TVs. Sizes are at the full file size.</p></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Asset</th><th>Desktop</th><th>Mobile</th><th>Keep inside</th><th>Smallest readable type</th></tr></thead>
          <tbody>{mobile}</tbody></table></div>
      </section>

      <section class="sec" id="copy" aria-labelledby="copy-h">
        <div class="sec-head"><h2 id="copy-h">Captions and copy.</h2><p>Plain titles that say what the video is. No prescription names in any social asset or caption, no result, no symptom list. Every description that offers the assessment carries the legal line.</p></div>
        <div class="sk-copy">
          <div class="rule"><b>Channel description · option 1 (1,000 characters at most)</b><q>{esc(ABOUT[0])}</q><p class="cap">{len(ABOUT[0])} characters.</p></div>
          <div class="rule"><b>Channel description · option 2</b><q>{esc(ABOUT[1])}</q><p class="cap">{len(ABOUT[1])} characters.</p></div>
          {''.join(f'<div class="rule"><b>Video {i}: title and description</b><q>{esc(t)}</q><q>{esc(d)}</q><p class="cap">Title {len(t)} characters (100 at most; keep under 60 so a phone shows it whole).</p></div>' for i, (t, d) in enumerate(TITLES, 1))}
          <div class="rule"><b>Hashtags and links</b><p>Up to three hashtags in the description: #unifiedmeds, then broad tags only. Never a condition, a medicine or a body part. One link, to the homepage [unifiedmeds.com, O-01]. Captions (subtitles) on every video, checked by hand.</p></div>
        </div>
      </section>

      <section class="sec" id="rules" aria-labelledby="rules-h">
        <div class="sec-head"><h2 id="rules-h">Rules for this channel.</h2></div>
        <ol class="sk-num">
          <li><p><b>The banner’s logo and line stay inside the centre 1546 × 423.</b> Outside it, only mood: ground, photo edges, capsules.</p></li>
          <li><p><b>A thumbnail carries three words or fewer</b>, at 110 px or larger, and nothing in the bottom right 210 × 90.</p></li>
          <li><p><b>Every long video opens with a sting or the title card and closes on the end screen</b>; one sting per video (R-101).</p></li>
          <li><p><b>Text and elements stay inside title-safe</b>, 1728 × 972.</p></li>
          <li><p><b>A lower third names only people who agreed in writing</b>, with their real role; a provider is shown as a licensed provider, never as a doctor (R-57).</p></li>
          <li><p><b>Subtitles on every video</b>; the voice never adds a claim the screen does not show.</p></li>
          <li><p><b>The legal line is in the video and in the description</b> whenever the assessment is offered (R-63).</p></li>
          <li><p><b>No medicine, result, symptom, price, testimonial or before and after</b> in a title, thumbnail or description (R-58, R-65, R-67).</p></li>
        </ol>
      </section>

      <section class="sec" id="files" aria-labelledby="files-h">
        <div class="sec-head"><h2 id="files-h">Files.</h2><p>PNG at the exact size, plus the SVG source (fonts from Google Fonts, photos embedded) and the safe-zone templates. Rebuild with <code>python3 -I assets/social/youtube/make.py</code>.</p></div>
        <div class="table-wrap sk-files"><table>
          <thead><tr><th>File</th><th>Size</th><th>Weight</th></tr></thead>
          <tbody>{ftable}</tbody></table></div>
      </section>
"""
    (k.EXT / "src" / "social-youtube.html").write_text(f"<style>{css}</style>\n{body}")


if __name__ == "__main__":
    if "--page" in sys.argv:
        for p in OUT.glob("youtube-*.png"):
            w, h = {"avatar": (800, 800), "banner": (2560, 1440), "thumb": (1280, 720), "shorts": (1080, 1920),
                    "watermark": (150, 150)}.get(p.stem.split("-")[1], (1920, 1080))
            ASSETS[p.stem] = (w, h, any(t in p.stem for t in ("lowerthird", "watermark")))
    else:
        build_art()
    page()
    print("youtube done")
