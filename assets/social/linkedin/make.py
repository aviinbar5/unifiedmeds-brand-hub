"""LinkedIn kit: art, PNG and PDF exports, previews and the hub page src/social-linkedin.html.

Run:  python3 -I assets/social/linkedin/make.py   (add --page to rebuild only the page)
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
REL = "assets/social/linkedin/"
ASSETS = {}
COVER_LOGO = (0, 96, 250, 95)        # company logo overlaps the bottom left of the cover on desktop
COVER_MOBILE = (114, 0, 900, 191)    # about the centre 900 shows on a phone
EMP_PHOTO = (0, 170, 520, 226)       # the member's own photo covers the bottom left (desktop and phone)
LEGAL = k.LEGAL


def art_logo(o):
    return k.shared_avatar(o, 400)


def art_cover(o):
    b = []
    if o == "a":
        b.append(k.rect(0, 0, 1128, 191, C["paper"]))
        b.append(k.text(300, 86, ["Care that keeps", "showing up."], 40, C["teal_deep"], lh=1.08))
        b.append(k.photo("man-reading-window-wide-2048-pexels-8217708.jpg", 700, 0, 314, 191, .56, .32))
    else:
        b.append(k.rect(0, 0, 1128, 191, C["deep_teal"]))
        b.append(k.text(300, 86, ["Care that keeps", "showing up."], 40, C["paper"], lh=1.08))
        b.append(k.capsule(720, 40, 300, stroke=C["sky"], sw=8, inner=C["logo_blue"], gap=11))
        b.append(k.capsule(1040, -40, 260, vertical=True, stroke=C["sky"], sw=8))
    return k.doc(1128, 191, "".join(b))


def art_post_sq(o):
    b = []
    if o == "a":
        b.append(k.rect(0, 0, 1200, 1200, C["paper"]))
        b.append(k.photo("couple-breakfast-pexels-6248662.jpg", 0, 0, 1200, 700, .5, .3))
        b.append(k.text(80, 830, ["Discretion is part of", "the treatment."], 76, C["teal_deep"], lh=1.08))
        b.append(k.text(80, 1010, "An online assessment, reviewed by a licensed provider.", 32, C["deep_teal"], "sans", 400))
        b.append(k.text(80, 1110, LEGAL, 26, C["slate"], "sans", 500))
        b.append(k.logo("logo-seal", 1200 - 80 - 190, 1072, h=69)[0])
    else:
        b.append(k.rect(0, 0, 1200, 1200, C["deep_teal"]))
        b.append(k.capsule(700, 880, 760, stroke=C["sky"], sw=20, inner=C["logo_blue"], gap=26))
        b.append(k.capsule(960, -160, 430, vertical=True, stroke=C["sky"], sw=20))
        b.append(k.logo("logo-seal-reversed", 80, 80, h=80)[0])
        b.append(k.text(80, 440, ["Discretion is", "part of the", "treatment."], 120, C["paper"], lh=1.04))
        b.append(k.text(80, 880, "An online assessment, reviewed", 32, C["paper"], "sans", 400))
        b.append(k.text(80, 924, "by a licensed provider.", 32, C["paper"], "sans", 400))
        b.append(k.text(80, 1110, LEGAL, 26, C["wash_blue"], "sans", 500))
    return k.doc(1200, 1200, "".join(b))


def art_post_wide(o):
    b = []
    if o == "a":
        b.append(k.rect(0, 0, 1200, 627, C["paper"]))
        b.append(k.photo("man-kitchen-coffee-pexels-6269909.jpg", 0, 0, 560, 627, .55, .3))
        b.append(k.logo("logo-seal", 640, 70, h=60)[0])
        b.append(k.text(640, 290, ["Care that keeps", "showing up."], 72, C["teal_deep"], lh=1.06))
        b.append(k.text(640, 480, ["An online assessment, reviewed", "by a licensed provider."], 28, C["deep_teal"], "sans", 400, lh=1.4))
        b.append(k.text(640, 570, LEGAL, 22, C["slate"], "sans", 500))
    else:
        b.append(k.rect(0, 0, 1200, 627, C["mist"]))
        b.append(k.capsule(820, 330, 620, stroke=C["sky"], sw=16, inner=C["logo_blue"], gap=22))
        b.append(k.logo("logo-seal", 70, 70, h=60)[0])
        b.append(k.text(70, 290, ["Care that keeps", "showing up."], 84, C["teal_deep"], lh=1.04))
        b.append(k.text(70, 480, ["An online assessment, reviewed", "by a licensed provider."], 28, C["deep_teal"], "sans", 400, lh=1.4))
        b.append(k.text(70, 570, LEGAL, 22, C["slate"], "sans", 500))
    return k.doc(1200, 627, "".join(b))


DOC = [  # pages of the document post
    dict(kicker="IN FOUR STEPS", title="How unifiedmeds works."),
    dict(steps=[("01", "Tell us what’s changed."), ("02", "A licensed provider reviews your information.")]),
    dict(steps=[("03", "Receive a personalized care plan."), ("04", "Stay supported.")], cta=True, size=72),
]


def art_doc(o, i):
    p = DOC[i]
    dark = o == "b" and i != 1
    tc = C["paper"] if dark else C["teal_deep"]
    sc = C["wash_blue"] if dark else C["slate"]
    b = [k.rect(0, 0, 1080, 1350, C["deep_teal"] if dark else (C["paper"] if o == "a" or i != 1 else C["mist"]))]
    if i == 0:
        if o == "a":
            b.append(k.photo("man-mug-sunlight-pexels-6972779.jpg", 0, 0, 1080, 760, .6, .3))
            b.append(k.text(90, 880, p["kicker"], 32, sc, "sans", 600, ls="0.06em"))
            b.append(k.text(90, 1000, ["How unifiedmeds", "works."], 104, tc, lh=1.06))
            b.append(k.logo("logo-seal", 90, 1220, h=60)[0])
        else:
            b.append(k.capsule(560, 1000, 760, stroke=C["sky"], sw=20, inner=C["logo_blue"], gap=26))
            b.append(k.capsule(840, -150, 420, vertical=True, stroke=C["sky"], sw=20))
            b.append(k.logo("logo-seal-reversed", 90, 100, h=80)[0])
            b.append(k.text(90, 470, p["kicker"], 32, sc, "sans", 600, ls="0.06em"))
            b.append(k.text(90, 600, ["How", "unifiedmeds", "works."], 128, tc, lh=1.04))
    else:
        b.append(k.logo("logo-seal-reversed" if dark else "logo-seal", 90, 100, h=60)[0])
        if o == "b" and i == 1:
            b.append(k.capsule(620, 1130, 700, stroke=C["sky"], sw=18, inner=C["logo_blue"], gap=24))
        y = 330
        fs = p.get("size", 92)
        for n, t in p["steps"]:
            b.append(k.text(90, y, n, 40, sc, "sans", 600, ls="0.04em"))
            lines = k.wrap(t, fs, 880)
            b.append(k.text(90, y + 40 + fs, lines, fs, tc, lh=1.08))
            y += 40 + fs + k.block_h(len(lines), fs, 1.08) + (130 if fs > 80 else 60)
        if p.get("cta"):
            btn, _ = k.button(90, y, "Get started", 120, 40)
            b.append(btn)
            b.append(k.text(90, y + 170, LEGAL, 34, sc, "sans", 500))
            b.append(k.text(90, y + 225, "[unifiedmeds.com]", 34, sc, "sans", 500))
        if o == "a" and i == 2:
            b.append(k.capsule(-200, 1180, 700, stroke=C["line_base"], sw=18))
    b.append(k.text(990, 1290, f"{i + 1} / 3", 28, sc, "sans", 500, anchor="end"))
    return k.doc(1080, 1350, "".join(b))


def art_life(o):
    b = []
    if o == "a":
        b.append(k.rect(0, 0, 1128, 376, C["paper"]))
        b.append(k.photo("friends-talking-outdoors-pexels-13335592.jpg", 520, 0, 608, 376, .5, .35))
        b.append(k.text(64, 160, ["Life at", "unifiedmeds."], 56, C["teal_deep"], lh=1.06))
        b.append(k.text(64, 290, "[One line about the team, with HR]", 22, C["slate"], "sans", 500))
    else:
        b.append(k.rect(0, 0, 1128, 376, C["deep_teal"]))
        b.append(k.capsule(780, 150, 460, stroke=C["sky"], sw=12, inner=C["logo_blue"], gap=16))
        b.append(k.capsule(-120, 300, 360, stroke=C["sky"], sw=12))
        b.append(k.text(64, 140, ["Work on care that", "keeps showing up."], 56, C["paper"], lh=1.06))
        b.append(k.text(64, 250, "[One line about the team, with HR]", 22, C["wash_blue"], "sans", 500))
    return k.doc(1128, 376, "".join(b))


def art_emp(o):
    b = []
    if o == "a":
        b.append(k.rect(0, 0, 1584, 396, C["paper"]))
        b.append(k.capsule(-180, 300, 560, stroke=C["line_base"], sw=14))
        b.append(k.logo("logo-seal", 640, 96, h=72)[0])
        b.append(k.text(640, 260, "Care that keeps showing up.", 60, C["teal_deep"]))
        b.append(k.text(640, 320, "[Team name] at unifiedmeds", 26, C["slate"], "sans", 500))
    else:
        b.append(k.rect(0, 0, 1584, 396, C["deep_teal"]))
        b.append(k.capsule(1230, 60, 560, stroke=C["sky"], sw=14, inner=C["logo_blue"], gap=18))
        b.append(k.logo("logo-horizontal-reversed", 640, 64, h=56)[0])
        b.append(k.text(640, 210, ["Care that keeps", "showing up."], 60, C["paper"], lh=1.06))
        b.append(k.text(640, 340, "[Team name] at unifiedmeds", 26, C["wash_blue"], "sans", 500))
    return k.doc(1584, 396, "".join(b))


def build_art():
    jobs = []

    def add(name, svg, w, h, transparent=False):
        p = OUT / f"{name}.svg"
        k.write(p, svg)
        jobs.append((p, OUT / f"{name}.png", w, h, transparent))
        ASSETS[name] = (w, h, transparent)

    for o in "ab":
        add(f"linkedin-logo-{o}", art_logo(o), 400, 400)
        add(f"linkedin-cover-{o}", art_cover(o), 1128, 191)
        add(f"linkedin-post-square-{o}", art_post_sq(o), 1200, 1200)
        add(f"linkedin-post-wide-{o}", art_post_wide(o), 1200, 627)
        for i in range(3):
            add(f"linkedin-document-{o}-{i + 1}", art_doc(o, i), 1080, 1350)
        add(f"linkedin-life-{o}", art_life(o), 1128, 376)
        add(f"linkedin-employee-{o}", art_emp(o), 1584, 396)
    k.write(OUT / "linkedin-safe-logo.svg", k.overlay(400, 400, safe=(40, 40, 320, 320), labels=[(200, 30, "Square, slight rounding", "middle")], s=.6))
    k.write(OUT / "linkedin-safe-cover.svg", k.overlay(
        1128, 191, s=.5, keep=[COVER_LOGO], guides=[COVER_MOBILE],
        labels=[(125, 150, "Logo (desktop)", "middle"), (564, 184, "Phone: about the centre 900", "middle")]))
    k.write(OUT / "linkedin-safe-employee.svg", k.overlay(
        1584, 396, s=.7, keep=[EMP_PHOTO], safe=(600, 40, 944, 316),
        labels=[(260, 300, "Profile photo", "middle"), (1072, 380, "Text and logo here", "middle")]))
    k.write(OUT / "linkedin-safe-post.svg", k.overlay(1200, 1200, safe=(60, 60, 1080, 1080), labels=[(600, 46, "Keep 60 px from every edge", "middle")]))
    k.write(OUT / "linkedin-safe-doc.svg", k.overlay(1080, 1350, safe=(90, 90, 900, 1170), labels=[(540, 70, "Margin 90", "middle")], s=.9))
    k.export(jobs)
    for name in ASSETS:
        k.jpg_copy(OUT / f"{name}.png")
    for name, (w, h, tr) in ASSETS.items():
        k.preview(OUT / f"{name}.png", PREV / f"{name}.jpg", 960 if w > h * 2 else 720)
    for o in "ab":   # the document post as one PDF
        pages = "".join(f'<div class="pg">{(OUT / f"linkedin-document-{o}-{i}.svg").read_text()}</div>' for i in (1, 2, 3))
        html_p = OUT / f"_doc-{o}.html"
        html_p.write_text("<!doctype html><html><head><meta charset='utf-8'><style>@page { size: 1080px 1350px; margin: 0; } "
                          "html, body { margin: 0; } .pg { width: 1080px; height: 1350px; overflow: hidden; break-after: page; } "
                          ".pg svg { display: block; }</style></head><body>" + pages + "</body></html>")
        k.pdf(html_p, OUT / f"linkedin-document-{o}.pdf")
        html_p.unlink()


# ---------------------------------------------------------------- page
def pv(name):
    return f"{REL}preview/{name}.jpg"


def links(name):
    jpg = [("JPG", f"{REL}{name}.jpg")] if (OUT / f"{name}.jpg").exists() else []
    return [("PNG", f"{REL}{name}.png")] + jpg + [("SVG", f"{REL}{name}.svg")]


def asset(id_, title, use, spec, figs, ctx="", pair_cls="sk-pair"):
    return (f'<article class="sk-asset" id="{id_}"><h3>{esc(title)}</h3><p>{use}</p>{k.spec_dl(spec)}'
            f'{k.toggle()}<div class="{pair_cls}">{figs}</div>{ctx}</article>')


TAGLINE = ["Men’s health care, online and discreet.", "Online assessments, read by licensed providers."]
ABOUT = [
    "unifiedmeds is men’s health care, online. Members answer a few questions on their own time, a licensed provider reviews them, and the member decides what happens next. We build it to be private, plain and easy to come back to. Assessment only. Not a diagnosis.",
    "We are building a quieter kind of men’s health care: an online assessment, a licensed provider who reads it, and nothing loud in between. We hire people who care about getting the small things right. Assessment only. Not a diagnosis.",
]
POSTS = [
    "Discretion is part of the treatment.\n\nAt unifiedmeds, a member answers a few questions online and a licensed provider reviews them. Nothing about it needs to be loud.\n\nAssessment only. Not a diagnosis.\n#unifiedmeds #telehealth",
    "How unifiedmeds works, in four steps. (Document post, 3 pages.)\n\n01 Tell us what’s changed.\n02 A licensed provider reviews your information.\n03 Receive a personalized care plan.\n04 Stay supported.\n\nAssessment only. Not a diagnosis.\n#unifiedmeds #menshealth",
    "We are hiring. [Role], [location or remote].\n\nIf you care about care that keeps showing up, read the role here: [careers link].\n#unifiedmeds #hiring",
]


def profile_row(o):
    logo_ = pv(f"linkedin-logo-{o}")
    cover = pv(f"linkedin-cover-{o}")
    desk = f"""<figure><div class="sk-desk"><div class="li-d">
      <div class="li-card"><div class="li-cover">{k.crop_img(cover, 1128, 191, 0, 0, 1128, 191, f'Cover option {o.upper()}, desktop')}<div class="li-logo"><img src="{logo_}" alt="Logo option {o.upper()}"></div></div>
        <div class="li-id sk-m"><b>unifiedmeds</b><span>{esc(TAGLINE[0])}</span><span class="li-mut">[Industry] · [City, State] · [0] followers</span><span class="li-btns"><i>Follow</i><i class="li-ghost">Visit website</i></span></div>
        <div class="li-tabs sk-m"><b>Home</b><span>About</span><span>Posts</span><span>Jobs</span><span>Life</span></div></div>
      <div class="li-card li-post sk-m"><div class="li-ph"><span class="sk-dot li-mini"><img src="{logo_}" alt=""></span><span><b>unifiedmeds</b><span class="li-mut">[0] followers</span></span></div><span class="sk-bar"></span><span class="sk-bar" style="width: 60%;"></span><img src="{pv(f'linkedin-post-wide-{o}')}" alt="Wide post option {o.upper()} in the feed"></div>
      </div></div><figcaption><b>Desktop · linkedin.com</b> · the cover shows whole; the logo covers its bottom left.</figcaption></figure>"""
    phone = f"""<figure><div class="sk-phone"><div class="li-p sk-m">
      <div class="li-cover">{k.crop_img(cover, 1128, 191, *COVER_MOBILE, alt=f'Cover option {o.upper()}, phone crop')}<div class="li-logo li-logo--p"><img src="{logo_}" alt="Logo option {o.upper()} on a phone"></div></div>
      <div class="li-id"><b>unifiedmeds</b><span>{esc(TAGLINE[0])}</span><span class="li-mut">[0] followers</span><span class="li-btns"><i>Follow</i><i class="li-ghost">Visit website</i></span></div>
      <div class="li-tabs"><b>Home</b><span>About</span><span>Posts</span></div>
      <div class="li-post"><span class="sk-bar"></span><img src="{pv(f'linkedin-post-square-{o}')}" alt="Square post option {o.upper()} on a phone"></div>
      </div></div><figcaption><b>Phone · 390 wide</b> · about the centre 900 of the cover shows.</figcaption></figure>"""
    return f'<h3 class="li-row-h">Option {o.upper()} · {"editorial, photo-led" if o == "a" else "graphic, colour-led"}</h3><div class="sk-ctx">{desk}{phone}</div>'


def page():
    css = k.PAGE_CSS + """
  .li-row-h { margin-top: var(--space-6); font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); color: var(--color-text-strong); }
  .li-d { display: grid; gap: var(--space-3); padding: var(--space-3); background: var(--color-surface-mist); }
  .li-card { display: grid; gap: var(--space-2); border-radius: var(--radius-xs); background: var(--color-surface-card); overflow: hidden; padding-bottom: var(--space-2); }
  .li-cover { position: relative; }
  .li-logo { position: absolute; left: 3%; bottom: -40%; width: 13%; aspect-ratio: 1; border-radius: var(--radius-xs); overflow: hidden; box-shadow: 0 0 0 var(--space-1) var(--color-surface-card); }
  .li-logo img { display: block; width: 100%; height: 100%; }
  .li-logo--p { width: 22%; bottom: -55%; left: 5%; }
  .li-id { display: grid; gap: var(--space-1); justify-items: start; padding: var(--space-8) var(--space-3) 0; font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); }
  .li-id b { font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); }
  .li-mut { color: var(--color-text-secondary); }
  .li-btns { display: flex; gap: var(--space-2); margin-top: var(--space-1); }
  .li-btns i { font-style: normal; padding: var(--space-1) var(--space-3); border-radius: var(--radius-pill); background: var(--color-brand-deep-teal); color: var(--color-text-on-dark); }
  .li-btns i.li-ghost { background: var(--color-surface-card); box-shadow: inset 0 0 0 1px var(--color-brand-deep-teal); color: var(--color-text-strong); }
  .li-tabs { display: flex; gap: var(--space-4); padding: var(--space-2) var(--space-3) 0; border-top: 1px solid var(--color-line-base); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  .li-post { display: grid; gap: var(--space-2); padding: var(--space-3); font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); }
  .li-post img { display: block; width: 100%; height: auto; }
  .li-post .sk-bar { height: var(--space-2); }
  .li-ph { display: flex; gap: var(--space-2); align-items: center; }
  .li-ph > span:last-child { display: grid; }
  .li-mini { width: var(--space-8); height: var(--space-8); border-radius: var(--radius-xs); }
  .li-p { display: grid; align-content: start; font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); }
  .li-p .li-id { padding-top: var(--space-10); }
  .li-crops { display: grid; gap: var(--space-3); width: 100%; }
  .li-crops figure { margin: 0; display: grid; gap: var(--space-2); }
  .li-crops .sk-crop { border-radius: var(--radius-xs); box-shadow: 0 0 0 1px var(--color-line-mid); }
  .li-crops--p { width: min(100%, calc(var(--space-24) * 3.25)); }
  .li-docs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-3); }
  .li-docs img { display: block; width: 100%; height: auto; border-radius: var(--radius-xs); box-shadow: 0 0 0 1px var(--color-line-base); }
  .li-emp { position: relative; width: 100%; }
  .li-emp .sk-crop { border-radius: var(--radius-xs) var(--radius-xs) 0 0; }
  .li-emp { padding-bottom: 9.5%; }
  .li-emp--p { padding-bottom: 15%; }
  .li-emp .li-face { position: absolute; left: 4%; bottom: 0; width: 19%; aspect-ratio: 1; border-radius: 50%; overflow: hidden; box-shadow: 0 0 0 var(--space-1) var(--color-surface-card); }
  .li-emp .li-face img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .li-emp--p .li-face { width: 30%; }
  @media (max-width: 767px) { .li-docs { grid-template-columns: minmax(0, 1fr); width: min(100%, calc(var(--space-24) * 3)); justify-self: center; } }
"""
    A = []
    A.append(asset(
        "logo", "Company logo",
        "The page’s face: a square with slightly rounded corners (not a circle), 200 px on the page, 48 to 72 px beside every post. The logo files as they are.",
        [("Size", "400 × 400 px"), ("Ratio", "1:1, square"), ("Type", "PNG or JPG"), ("Max file", "8 MB [check]"), ("Safe zone", "Keep 40 px from the edges")],
        k.opt_fig("A", "The \u201cu|m\u201d mark in Navy on Cream, the same art as every other channel\u2019s profile picture.", pv("linkedin-logo-a"), 400, 400, links("linkedin-logo-a"), f"{REL}linkedin-safe-logo.svg", "sk-art--sq")
        + k.opt_fig("B", "The app icon, “u|m” on Navy (R-93): one avatar across all channels.", pv("linkedin-logo-b"), 400, 400, links("linkedin-logo-b"), f"{REL}linkedin-safe-logo.svg", "sk-art--sq")))
    cov = lambda o: f"""<div class="li-crops"><figure>{k.crop_img(pv(f'linkedin-cover-{o}'), 1128, 191, 0, 0, 1128, 191, 'Desktop')}<figcaption class="cap"><b>Desktop</b> · all 1128 × 191; the logo covers the bottom left</figcaption></figure><figure class="li-crops--p">{k.crop_img(pv(f'linkedin-cover-{o}'), 1128, 191, *COVER_MOBILE, alt='Phone')}<figcaption class="cap"><b>Phone</b> · about the centre 900</figcaption></figure></div>"""
    A.append(asset(
        "cover", "Cover",
        "A thin strip: one line and a photo or two capsules. Nothing in the bottom left (the logo) and nothing important outside the centre 900 (the phone).",
        [("Size", "1128 × 191 px"), ("Ratio", "about 5.9:1"), ("Type", "PNG or JPG"), ("Max file", "8 MB [check]"), ("Safe zone", "x 300 to 1014; keep the bottom left 250 × 95 clear")],
        k.opt_fig("A", "Paper, the line in DM Serif, a photo window inside the phone crop.", pv("linkedin-cover-a"), 1128, 191, links("linkedin-cover-a"), f"{REL}linkedin-safe-cover.svg")
        + k.opt_fig("B", "Deep Teal, the line in Paper, a split capsule and an outline at the right.", pv("linkedin-cover-b"), 1128, 191, links("linkedin-cover-b"), f"{REL}linkedin-safe-cover.svg"),
        ctx=f'<div class="sk-ctx sk-ctx--even"><figure>{cov("a")}<figcaption><b>Option A</b>, both crops.</figcaption></figure><figure>{cov("b")}<figcaption><b>Option B</b>, both crops.</figcaption></figure></div>'))
    A.append(asset(
        "post-square", "Post image, square",
        "The feed’s safest format: the same on desktop and phone. Headline, one plain line, the legal line when the assessment is offered.",
        [("Size", "1200 × 1200 px"), ("Ratio", "1:1"), ("Type", "PNG or JPG"), ("Max file", "5 MB [check]"), ("Safe zone", "60 px from every edge")],
        k.opt_fig("A", "Photo on top, Paper panel with the headline below.", pv("linkedin-post-square-a"), 1200, 1200, links("linkedin-post-square-a"), f"{REL}linkedin-safe-post.svg", "sk-art--sq")
        + k.opt_fig("B", "Deep Teal, the headline at 120, two capsules at the edges.", pv("linkedin-post-square-b"), 1200, 1200, links("linkedin-post-square-b"), f"{REL}linkedin-safe-post.svg", "sk-art--sq")))
    A.append(asset(
        "post-wide", "Post image, wide",
        "For a single image post and for link previews. On a phone it shows at about 360 pt wide, so the headline stays at 72 px or larger.",
        [("Size", "1200 × 627 px"), ("Ratio", "1.91:1"), ("Type", "PNG or JPG"), ("Max file", "5 MB [check]"), ("Safe zone", "60 px from every edge")],
        k.opt_fig("A", "Photo on the left, Paper on the right.", pv("linkedin-post-wide-a"), 1200, 627, links("linkedin-post-wide-a"))
        + k.opt_fig("B", "Mist, the headline large, one split capsule cropped by the corner.", pv("linkedin-post-wide-b"), 1200, 627, links("linkedin-post-wide-b"))))
    docs = lambda o: f'<div class="li-docs">{"".join(f"""<img src="{pv(f"linkedin-document-{o}-{i}")}" alt="Document option {o.upper()}, page {i}" loading="lazy">""" for i in (1, 2, 3))}</div>'
    A.append(f"""<article class="sk-asset" id="document"><h3>Document post (PDF, 3 pages)</h3>
      <p>LinkedIn shows a PDF as swipeable pages in the feed. Three pages: the cover, two steps, the last step with the button and the legal line. Portrait pages fill most of a phone screen.</p>
      {k.spec_dl([("Size", "1080 × 1350 px per page"), ("Ratio", "4:5"), ("Type", "PDF (PNG pages for reference)"), ("Max file", "100 MB, 300 pages [check]"), ("Safe zone", "90 px margin; page number bottom right")])}
      <div class="sk-pair"><figure class="sk-opt">{docs('a')}<figcaption><b>Option A</b> · photo cover, Paper pages · <a class="link" href="{REL}linkedin-document-a.pdf" download>PDF</a> · <a class="link" href="{REL}linkedin-document-a-1.png" download>PNG 1</a> · <a class="link" href="{REL}linkedin-document-a-2.png" download>2</a> · <a class="link" href="{REL}linkedin-document-a-3.png" download>3</a></figcaption></figure>
      <figure class="sk-opt">{docs('b')}<figcaption><b>Option B</b> · Deep Teal cover and close, a Mist page between · <a class="link" href="{REL}linkedin-document-b.pdf" download>PDF</a> · <a class="link" href="{REL}linkedin-document-b-1.png" download>PNG 1</a> · <a class="link" href="{REL}linkedin-document-b-2.png" download>2</a> · <a class="link" href="{REL}linkedin-document-b-3.png" download>3</a></figcaption></figure></div></article>""")
    A.append(asset(
        "life", "Careers (Life tab) image",
        "The header of the Life tab, for people thinking of joining. Real team photos replace the placeholder once there is a team shoot.",
        [("Size", "1128 × 376 px"), ("Ratio", "3:1"), ("Type", "PNG or JPG"), ("Max file", "8 MB [check]"), ("Safe zone", "Text in the left half")],
        k.opt_fig("A", "Paper panel, the title in DM Serif, a photo of people together.", pv("linkedin-life-a"), 1128, 376, links("linkedin-life-a"))
        + k.opt_fig("B", "Deep Teal, the line large, two capsules.", pv("linkedin-life-b"), 1128, 376, links("linkedin-life-b"))))
    emp = lambda o, ph: f"""<figure{' class="li-crops--p"' if ph else ''}><div class="li-emp{' li-emp--p' if ph else ''}">{k.crop_img(pv(f'linkedin-employee-{o}'), 1584, 396, 0, 0, 1584, 396, f'Employee banner option {o.upper()}')}<span class="li-face"><img src="assets/photos/man-selfie-avatar-pexels-23224714.jpg" alt=""></span></div><figcaption class="cap"><b>{'Phone' if ph else 'Desktop'}</b> · the member’s photo covers the bottom left</figcaption></figure>"""
    A.append(asset(
        "employee", "Employee banner template",
        "For team members who want to show where they work, on their own profile (optional, never required). Everything sits on the right, away from their photo.",
        [("Size", "1584 × 396 px"), ("Ratio", "4:1"), ("Type", "PNG or JPG"), ("Max file", "8 MB [check]"), ("Safe zone", "x 600 to 1544; keep the left 520 × 226 clear")],
        k.opt_fig("A", "Paper, the seal, the line, a team name slot.", pv("linkedin-employee-a"), 1584, 396, links("linkedin-employee-a"), f"{REL}linkedin-safe-employee.svg")
        + k.opt_fig("B", "Deep Teal, the reversed horizontal logo, one split capsule.", pv("linkedin-employee-b"), 1584, 396, links("linkedin-employee-b"), f"{REL}linkedin-safe-employee.svg"),
        ctx=f'<div class="sk-ctx sk-ctx--even"><figure><div class="li-crops">{emp("a", False)}{emp("a", True)}</div><figcaption><b>Option A</b> with a member’s photo.</figcaption></figure><figure><div class="li-crops">{emp("b", False)}{emp("b", True)}</div><figcaption><b>Option B</b> with a member’s photo.</figcaption></figure></div>'))

    mobile_rows = [
        ("Company logo", "Square, 200 px on the page", "Square, about 72 pt", "40 px from the edges", "Both options at any size"),
        ("Cover", "All 1128 × 191; logo over the bottom left", "About the centre 900; logo over the bottom left", "x 300 to 1014", "Line 40 px or larger"),
        ("Post, square", "About 550 px wide", "Full width, about 360 pt", "60 px margin", "Headline 72 px, body 30 px, legal 26 px"),
        ("Post, wide", "About 550 px wide", "Full width, about 360 pt", "60 px margin", "Headline 72 px, body 28 px, legal 22 px"),
        ("Document", "Pages in a viewer, about 550 px wide", "Swipeable, full width", "90 px margin", "Headline 92 px, body 40 px, legal 34 px"),
        ("Life tab image", "Whole", "Whole, scaled down", "Text in the left half", "Title 56 px"),
        ("Employee banner", "Whole; photo bottom left", "Whole; photo bottom left, larger", "x 600 to 1544", "Line 60 px"),
    ]
    mobile = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in mobile_rows)
    files = []
    for name, (w, h, tr) in sorted(ASSETS.items()):
        files.append((name + ".png", f"{w} × {h}", k.size_label(OUT / f"{name}.png")))
        if (OUT / f"{name}.jpg").exists():
            files.append((name + ".jpg", f"{w} × {h}, JPG 80 (the PNG is over 1 MB)", k.size_label(OUT / f"{name}.jpg")))
        files.append((name + ".svg", "Source", k.size_label(OUT / f"{name}.svg")))
    for o in "ab":
        files.append((f"linkedin-document-{o}.pdf", "3 pages, 1080 × 1350", k.size_label(OUT / f"linkedin-document-{o}.pdf")))
    for n, d in (("linkedin-safe-cover.svg", "Cover crops"), ("linkedin-safe-employee.svg", "Employee banner safe zone"),
                 ("linkedin-safe-logo.svg", "Logo margin"), ("linkedin-safe-post.svg", "Post margin"), ("linkedin-safe-doc.svg", "Document margin"),
                 ("make.py", "Generator: rebuilds every file and this page"), ("sk_kit.py", "Shared helpers")):
        files.append((n, d, k.size_label(OUT / n)))
    ftable = "".join(f'<tr><td data-label="File"><a class="link" href="{REL}{n}" download>{n}</a></td><td data-label="Size">{s}</td><td data-label="Weight">{wt}</td></tr>' for n, s, wt in files)
    body = f"""      <header class="page-head">
        <span class="eyebrow">Marketing · Social</span>
        <h1>LinkedIn.</h1>
        <p class="lead">The unifiedmeds company page: logo, cover, square and wide posts, a document post, the careers image and a banner template for the team. Two options for each, A (editorial, photo-led) and B (graphic, colour-led), on a desktop and on a phone.</p>
        <nav class="toc" aria-label="On this page"><a href="#profile">Profile</a><a href="#assets">Asset set</a><a href="#mobile">Mobile and desktop</a><a href="#copy">Captions and copy</a><a href="#rules">Rules</a><a href="#files">Files</a></nav>
      </header>

      <div class="grid-2"><div class="rule"><span class="status status--current">Current</span><p>The kit is approved for use. LinkedIn is where partners, providers and future colleagues meet the brand, so the tone is the calmest of all channels. The profile picture is Option B, the white u|m on Navy (R-93, U-27). Legal approves every post before it runs (U-30).</p></div>
      <div class="rule"><span class="status status--proposed">To confirm</span><p>Option A or B per asset (Avi). Lines are candidates; sizes marked [check] come from third-party guides and LinkedIn changes them often. Photos are Pexels stand-ins, not approved, to replace (R-39, O-13).</p></div></div>

      <section class="sec" id="profile" aria-labelledby="profile-h">
        <div class="sec-head"><h2 id="profile-h">The profile, desktop and mobile.</h2><p>The company page on linkedin.com and in the app, with a post in the feed.</p></div>
        {profile_row('a')}
        {profile_row('b')}
      </section>

      <section class="sec" id="assets" aria-labelledby="assets-h">
        <div class="sec-head"><h2 id="assets-h">The asset set.</h2><p>Each block: use, exact size, safe zone (dashed overlay; switch it off to see the art) and Option A beside Option B. Coral marks what LinkedIn covers; the dotted blue box is the phone crop.</p></div>
        {''.join(A)}
      </section>

      <section class="sec" id="mobile" aria-labelledby="mobile-h">
        <div class="sec-head"><h2 id="mobile-h">Mobile and desktop differences.</h2><p>More than half of LinkedIn is read on a phone. Sizes are at the full file size.</p></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Asset</th><th>Desktop</th><th>Mobile</th><th>Keep inside</th><th>Smallest readable type</th></tr></thead>
          <tbody>{mobile}</tbody></table></div>
      </section>

      <section class="sec" id="copy" aria-labelledby="copy-h">
        <div class="sec-head"><h2 id="copy-h">Captions and copy.</h2><p>Plain, calm and specific. No prescription names in any social asset or caption, no result, no statistic. The legal line wherever the assessment is offered.</p></div>
        <div class="sk-copy">
          <div class="rule"><b>Tagline · option 1 (120 characters at most)</b><q>{esc(TAGLINE[0])}</q><p class="cap">{len(TAGLINE[0])} characters.</p></div>
          <div class="rule"><b>Tagline · option 2</b><q>{esc(TAGLINE[1])}</q><p class="cap">{len(TAGLINE[1])} characters.</p></div>
          <div class="rule"><b>About · option 1 (2,000 characters at most)</b><q>{esc(ABOUT[0])}</q><p class="cap">{len(ABOUT[0])} characters.</p></div>
          <div class="rule"><b>About · option 2</b><q>{esc(ABOUT[1])}</q><p class="cap">{len(ABOUT[1])} characters.</p></div>
          {''.join(f'<div class="rule"><b>Post {i}</b><q>{esc(c)}</q></div>' for i, c in enumerate(POSTS, 1))}
          <div class="rule"><b>Hashtags and links</b><p>Two or three hashtags at the end: #unifiedmeds, then broad tags only. Never a condition, a medicine or a body part. Links go to the homepage or the careers page [O-01]; LinkedIn shows the first 210 characters before “see more”, so the point comes first.</p></div>
        </div>
      </section>

      <section class="sec" id="rules" aria-labelledby="rules-h">
        <div class="sec-head"><h2 id="rules-h">Rules for this channel.</h2></div>
        <ol class="sk-num">
          <li><p><b>The cover keeps the bottom left clear</b> for the logo, and everything that matters inside the centre 900 for the phone.</p></li>
          <li><p><b>The logo is a square</b>: never a circle crop, never the wordmark alone.</p></li>
          <li><p><b>Posts lead with the point</b> in the first 210 characters; no hook that teases a result.</p></li>
          <li><p><b>Document posts are three to six pages</b>, 4:5, one idea per page, the legal line on the last page.</p></li>
          <li><p><b>Team members are never asked to use the employee banner</b>, and never post about members or results.</p></li>
          <li><p><b>Careers posts name the role and place</b>, no promise about growth or pay that HR has not approved.</p></li>
          <li><p><b>No medicine, result, statistic, testimonial or certification</b> in a post or image until legal approves it (R-65, R-67).</p></li>
        </ol>
      </section>

      <section class="sec" id="files" aria-labelledby="files-h">
        <div class="sec-head"><h2 id="files-h">Files.</h2><p>PNG at the exact size, the SVG source (fonts from Google Fonts, photos embedded), the document as PDF and the safe-zone templates. Rebuild with <code>python3 -I assets/social/linkedin/make.py</code>.</p></div>
        <div class="table-wrap sk-files"><table>
          <thead><tr><th>File</th><th>Size</th><th>Weight</th></tr></thead>
          <tbody>{ftable}</tbody></table></div>
      </section>
"""
    (k.EXT / "src" / "social-linkedin.html").write_text(f"<style>{css}</style>\n{body}")


if __name__ == "__main__":
    if "--page" in sys.argv:
        for p in OUT.glob("linkedin-*.png"):
            ASSETS[p.stem] = (0, 0, False)
        sizes = {"logo": (400, 400), "cover": (1128, 191), "post-square": (1200, 1200), "post-wide": (1200, 627),
                 "life": (1128, 376), "employee": (1584, 396)}
        for n in list(ASSETS):
            key = next((s for s in sizes if f"-{s}-" in n), None)
            ASSETS[n] = (*sizes.get(key, (1080, 1350)), False)
    else:
        build_art()
    page()
    print("linkedin done")
