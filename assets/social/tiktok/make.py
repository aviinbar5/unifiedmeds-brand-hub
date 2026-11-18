"""TikTok kit: art, PNG exports, previews and the hub page src/social-tiktok.html.

Run from anywhere:  python3 -I assets/social/tiktok/make.py   (add --page to rebuild only the page)
Hub page status: Current (hub merge 18.11.2026).
"""
import os
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sk_kit as k  # noqa: E402
from sk_kit import C, esc  # noqa: E402

OUT = k.HERE
PREV = OUT / "preview"
REL = "assets/social/tiktok/"
V = k.V()                       # TikTok safe area: x 60..920, y 160..1440

# ---------------------------------------------------------------- content
BOARD1 = [  # How it works, 15 s
    ("caption", dict(text="A private next step, on your schedule.", photo="man-mug-sunlight-pexels-6972779.jpg", fx=.6, fy=.3, n=1),
     "0 to 2 s", "Hook. One line, a real person at home."),
    ("form", dict(text="01 · Tell us what’s changed.", n=2), "2 to 5 s", "Step 01. The assessment, a demo screen with the neutral state question (DEMO ONLY, R-69)."),
    ("placeholder", dict(text="02 · A licensed provider reviews your information.", n=3), "5 to 8 s", "Step 02. The provider: a real, consenting provider or no face."),
    ("caption", dict(text="03 · Receive a personalized care plan.", photo="friends-talking-outdoors-pexels-13335592.jpg", fx=.45, fy=.4, n=4), "8 to 11 s", "Step 03. Life outside. No product, no result."),
    ("title", dict(text="04 · Stay supported.", sub="Discretion is part of the treatment.", n=5), "11 to 13 s", "Step 04, with the brand line, type only."),
    ("end", dict(), "13 to 15 s", "End card: one Yellow button, the legal line."),
]
BOARD2 = [  # Things you don't have to do, 12 s
    ("title", dict(text="Things you don’t have to do.", kicker="A SHORT LIST", n=1), "0 to 2 s", "Hook. Type only, read in one second."),
    ("caption", dict(text="Sit in a waiting room.", photo="man-home-office-pexels-8055837.jpg", fy=.3, kicker="01", n=2), "2 to 4 s", "One item per frame."),
    ("caption", dict(text="Explain it out loud.", photo="man-kitchen-coffee-pexels-6269909.jpg", fx=.55, fy=.3, kicker="02", n=3), "4 to 6 s", "Faces stay clear of every caption."),
    ("caption", dict(text="Make it a whole thing.", photo="father-son-kitchen-hug-pexels-4259702.jpg", fx=.45, fy=.35, kicker="03", n=4), "6 to 8 s", "Ordinary life, no clinic."),
    ("title", dict(text="Tell us what’s changed.", sub="A licensed provider reviews your information.", n=5), "8 to 10 s", "What happens instead (steps 01 and 02 of How it works)."),
    ("end", dict(text="Nothing is looked at alone."), "10 to 12 s", "End card."),
]

ASSETS = {}   # name -> (w, h, transparent)


def art_avatar(opt):
    return k.shared_avatar(opt, 400)


def art_text_style(kind, opt):
    if kind == "title":
        return k.vframe("title", opt, dict(text="Things you don’t have to do.", kicker="A SHORT LIST"))
    if kind == "caption":
        return k.vframe("caption", opt, dict(text="Sit in a waiting room.", photo="man-home-office-pexels-8055837.jpg", fy=.3, kicker="01", n=1))
    return k.vframe("end", opt, {})


def build_art():
    jobs = []

    def add(name, svg, w, h, transparent=False):
        p = OUT / f"{name}.svg"
        k.write(p, svg)
        jobs.append((p, OUT / f"{name}.png", w, h, transparent))
        ASSETS[name] = (w, h, transparent)

    for o in "ab":
        add(f"tiktok-avatar-{o}", art_avatar(o), 400, 400)
        add(f"tiktok-cover-{o}", k.vframe("cover", o, dict(text="A private next step, on your schedule.", kicker="HOW IT WORKS",
                                                           photo="man-mug-sunlight-pexels-6972779.jpg", fx=.6, fy=.3)), 1080, 1920)
        for kind in ("title", "caption", "end"):
            add(f"tiktok-{kind}-{o}", art_text_style(kind, o), 1080, 1920)
        for bi, board in ((1, BOARD1), (2, BOARD2)):
            for i, (kind, d, _, _) in enumerate(board, 1):
                add(f"tiktok-board{bi}-{o}-{i:02d}", k.vframe(kind, o, d), 1080, 1920)
    # safe-zone templates
    k.write(OUT / "tiktok-safe-9x16.svg", k.overlay(
        1080, 1920, s=1.6,
        keep=[(0, 0, 1080, V.y0), (V.x1, V.y0, 1080 - V.x1, V.y1 - V.y0), (0, V.y1, 1080, 1920 - V.y1)],
        safe=(V.x0, V.y0, V.x1 - V.x0, V.y1 - V.y0),
        guides=[(0, 240, 1080, 1440)],
        labels=[(540, 105, "Tabs and search · 160", "middle"), (1000, 900, "Rail", "middle"),
                (540, 1690, "Caption, sound, buttons · 480", "middle"), (490, 1415, "Safe 860 × 1280", "middle"),
                (540, 232, "Profile grid crop 3:4", "middle")]))
    k.write(OUT / "tiktok-safe-avatar.svg", k.overlay(400, 400, circle=(200, 200, 200), s=.6))
    k.write(OUT / "tiktok-ui.svg", ui_overlay())
    k.export(jobs)
    for name in ASSETS:
        if "-board" not in name:
            k.jpg_copy(OUT / f"{name}.png")
    for name, (w, h, tr) in ASSETS.items():
        k.preview(OUT / f"{name}.png", PREV / f"{name}.{'png' if tr else 'jpg'}", 640 if h > w else 720)
    for bi in (1, 2):
        for o in "ab":
            z = OUT / f"tiktok-board{bi}-{o}.zip"
            if z.exists():
                z.unlink()
            frames = [OUT / f"tiktok-board{bi}-{o}-{i:02d}.png" for i in range(1, 7)]
            subprocess.run(["zip", "-q", "-j", str(z)] + [str(p) for p in frames])
            jz = OUT / f"tiktok-board{bi}-{o}-jpg.zip"
            if jz.exists():
                jz.unlink()
            jpgs = [j for j in (k.jpg_copy(p) for p in frames) if j]
            if jpgs:                  # photo-led frames over 1 MB also ship as JPG (quality 80)
                subprocess.run(["zip", "-q", "-j", str(jz)] + [str(p) for p in jpgs])
            for p in frames + jpgs:   # the ZIPs carry the frames; the SVG sources and previews stay
                p.unlink()


def ui_overlay():
    """Generic phone UI over a 9:16 video (not the platform's own artwork): tabs, rail, caption, nav."""
    p, ink = C["paper"], C["ink"]
    o = [f'<rect x="0" y="1780" width="1080" height="140" fill="{ink}" opacity="0.92"/>']
    for i, x in enumerate((90, 300, 540, 780, 990)):
        o.append(f'<rect x="{x - 36}" y="1830" width="72" height="40" rx="12" fill="{p}" opacity="{0.9 if i == 2 else 0.55}"/>')
    o.append(f'<rect x="330" y="80" width="170" height="26" rx="13" fill="{p}" opacity="0.6"/>')
    o.append(f'<rect x="560" y="80" width="190" height="26" rx="13" fill="{p}" opacity="0.95"/>')
    o.append(f'<rect x="985" y="74" width="40" height="40" rx="20" fill="none" stroke="{p}" stroke-width="6" opacity="0.9"/>')
    for i, y in enumerate((900, 1060, 1210, 1360, 1530)):
        o.append(f'<circle cx="1000" cy="{y}" r="{48 if i in (0, 4) else 40}" fill="{p}" opacity="{0.9 if i == 0 else 0.75}"/>')
    o.append(f'<rect x="40" y="1520" width="300" height="34" rx="17" fill="{p}" opacity="0.95"/>')
    o.append(f'<rect x="40" y="1590" width="760" height="26" rx="13" fill="{p}" opacity="0.75"/>')
    o.append(f'<rect x="40" y="1640" width="560" height="26" rx="13" fill="{p}" opacity="0.75"/>')
    o.append(f'<rect x="40" y="1700" width="420" height="24" rx="12" fill="{p}" opacity="0.6"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">{"".join(o)}</svg>\n'


# ---------------------------------------------------------------- page
def pv(name):
    w, h, tr = ASSETS.get(name, (1080, 1920, False))
    return f"{REL}preview/{name}.{'png' if tr else 'jpg'}"


def links(name, svg=True):
    out = [("PNG", f"{REL}{name}.png")]
    if (OUT / f"{name}.jpg").exists():
        out.append(("JPG", f"{REL}{name}.jpg"))
    if svg:
        out.append(("SVG", f"{REL}{name}.svg"))
    return out


def tile(name, alt=""):
    return k.crop_img(pv(name), 1080, 1920, 0, 240, 1080, 1440, alt, cls="sk-crop tt-tile")


def profile_row(o):
    tiles_d = [f"tiktok-cover-{o}", f"tiktok-board1-{o}-01", f"tiktok-board2-{o}-01", f"tiktok-title-{o}",
               f"tiktok-caption-{o}", f"tiktok-end-{o}"]
    av = pv(f"tiktok-avatar-{o}")
    desk = f"""<figure><div class="sk-desk"><div class="tt-d">
        <aside class="tt-d-side" aria-hidden="true"><span class="sk-bar"></span><span class="sk-bar"></span><span class="sk-bar"></span><span class="sk-bar"></span></aside>
        <div class="tt-d-main">
          <div class="tt-d-head"><div class="sk-dot tt-d-av"><img src="{av}" alt="Profile picture, option {o.upper()}"></div>
            <div class="sk-m tt-d-id"><b>unifiedmeds</b><span>[@unifiedmeds]</span><span class="tt-btns"><i>Follow</i><i class="tt-ghost">Message</i></span>
            <span class="tt-stats">[0] Following · [0] Followers · [0] Likes</span><span>{esc(BIO[0])}</span><span class="tt-link">[unifiedmeds.com]</span></div></div>
          <div class="tt-tabs sk-m"><b>Videos</b><span>Liked</span></div>
          <div class="tt-grid6">{''.join(tile(t) for t in tiles_d)}</div>
        </div></div></div><figcaption><b>Desktop · tiktok.com</b> · avatar 116 px, videos in a 6-column grid cropped to 3:4.</figcaption></figure>"""
    phone = f"""<figure><div class="sk-phone"><div class="tt-p sk-m">
        <div class="tt-p-top"><b>unifiedmeds</b></div>
        <div class="sk-dot tt-p-av"><img src="{av}" alt="Profile picture, option {o.upper()}, on a phone"></div>
        <span class="tt-p-handle">[@unifiedmeds]</span>
        <span class="tt-p-stats"><span><b>[0]</b>Following</span><span><b>[0]</b>Followers</span><span><b>[0]</b>Likes</span></span>
        <span class="tt-btns tt-btns--c"><i>Follow</i><i class="tt-ghost">Message</i></span>
        <span class="tt-p-bio">{esc(BIO[0])}</span>
        <div class="tt-grid3">{''.join(tile(t) for t in tiles_d)}</div>
      </div></div><figcaption><b>Phone · 390 wide</b> · avatar 96 pt, 3-column grid, same 3:4 crop.</figcaption></figure>"""
    return f'<h3 class="tt-row-h">Option {o.upper()} · {"editorial, photo-led" if o == "a" else "graphic, colour-led"}</h3><div class="sk-ctx">{desk}{phone}</div>'


BIO = ["Men’s health care, online. Reviewed by licensed providers.",
       "Online assessments, read by licensed providers. Discreet by design."]
CAPTIONS = [
    "A private next step, on your schedule. Tell us what’s changed, and a licensed provider reviews your information.\nAssessment only. Not a diagnosis.\n#unifiedmeds #menshealth #telehealth",
    "Things you don’t have to do: sit in a waiting room, explain it out loud, make it a whole thing.\nAssessment only. Not a diagnosis.\n#unifiedmeds #menshealth",
    "Discretion is part of the treatment. Nothing on your screen says more than you want it to.\nAssessment only. Not a diagnosis.\n#unifiedmeds",
]


def asset(id_, title, use, spec, figs, ctx="", pair_cls="sk-pair", note=""):
    return (f'<article class="sk-asset" id="{id_}"><h3>{esc(title)}</h3><p>{use}</p>{k.spec_dl(spec)}'
            f'{k.toggle()}<div class="{pair_cls}">{figs}</div>{ctx}{note}</article>')


def board_html(bi, board, o):
    figs = []
    for i, (kind, d, t, line) in enumerate(board, 1):
        n = f"tiktok-board{bi}-{o}-{i:02d}"
        figs.append(f'<figure><img src="{pv(n)}" width="1080" height="1920" alt="Storyboard {bi}, option {o.upper()}, frame {i}" loading="lazy">'
                    f'<figcaption><b>{i:02d} · {esc(t)}</b>{esc(line)}</figcaption></figure>')
    return (f'<div class="sk-board"><b>Option {o.upper()} · {"editorial, photo-led" if o == "a" else "graphic, colour-led"}</b>'
            f'<div class="sk-strip">{"".join(figs)}</div><p class="cap"><a class="link" href="{REL}tiktok-board{bi}-{o}.zip" download>All 6 frames, PNG 1080 × 1920 (ZIP)</a>'
            + (f' · <a class="link" href="{REL}tiktok-board{bi}-{o}-jpg.zip" download>the photo frames as JPG (ZIP)</a>' if (OUT / f"tiktok-board{bi}-{o}-jpg.zip").exists() else "")
            + '</p></div>')


def page():
    css = k.PAGE_CSS + """
  .tt-row-h { margin-top: var(--space-6); font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); color: var(--color-text-strong); }
  .tt-tile { border-radius: var(--radius-xs); }
  .tt-d { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 5fr); }
  .tt-d-side { display: grid; align-content: start; gap: var(--space-3); padding: var(--space-4) var(--space-3); border-right: 1px solid var(--color-line-base); }
  .tt-d-side .sk-bar { height: var(--space-2); }
  .tt-d-main { display: grid; gap: var(--space-3); padding: var(--space-4); min-width: 0; }
  .tt-d-head { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 3fr); gap: var(--space-4); align-items: start; }
  .tt-d-av { width: 100%; aspect-ratio: 1; }
  .tt-d-id, .tt-p { display: grid; gap: var(--space-1); font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); min-width: 0; }
  .tt-d-id b { font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); }
  .tt-btns { display: flex; gap: var(--space-2); }
  .tt-btns--c { justify-content: center; }
  .tt-btns i { font-style: normal; padding: var(--space-1) var(--space-4); border-radius: var(--radius-button); background: var(--color-brand-deep-teal); color: var(--color-text-on-dark); }
  .tt-btns i.tt-ghost { background: var(--color-surface-mist); color: var(--color-text-strong); }
  .tt-stats, .tt-p-handle { color: var(--color-text-secondary); }
  .tt-link { color: var(--color-text-strong); font-weight: 600; }
  .tt-tabs { display: flex; gap: var(--space-6); padding-bottom: var(--space-2); border-bottom: 1px solid var(--color-line-base); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  .tt-grid6 { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: var(--space-1); }
  .tt-p { justify-items: center; text-align: center; padding: var(--space-3) var(--space-2) 0; }
  .tt-p-top { padding-bottom: var(--space-2); }
  .tt-p-av { width: 30%; aspect-ratio: 1; }
  .tt-p-stats { display: flex; gap: var(--space-4); }
  .tt-p-stats > span { display: grid; }
  .tt-p-bio { padding: 0 var(--space-4); }
  .tt-grid3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-1); width: calc(100% + var(--space-4)); margin-top: var(--space-2); }
  .tt-feed { position: relative; width: 100%; aspect-ratio: 9 / 16; }
  .tt-feed > img:first-child { display: block; width: 100%; height: auto; }
  .tt-web { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr) minmax(0, 1fr); gap: var(--space-4); padding: var(--space-4); align-items: end; background: var(--color-brand-teal-deep); }
  .tt-web .tt-vid { position: relative; border-radius: var(--radius-xs); overflow: hidden; }
  .tt-web .tt-vid img { display: block; width: 100%; height: auto; }
  .tt-web .tt-rail { display: grid; gap: var(--space-3); justify-items: start; }
  .tt-web .tt-rail span { width: var(--space-8); height: var(--space-8); border-radius: 50%; background: var(--color-line-on-dark); }
  .tt-grid-demo { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-1); width: 100%; }
"""
    A = []
    # avatar
    A.append(asset(
        "avatar", "Profile picture",
        "Shown as a circle everywhere: 116 px on desktop, 96 pt on a phone, 32 px next to comments. Nothing sits in the corners. The logo files are placed as they are, never redrawn.",
        [("Size", "400 × 400 px (shown from 200)"), ("Ratio", "1:1, cropped to a circle"), ("Type", "PNG or JPG"),
         ("Max file", "Small, under 1 MB [check in the app]"), ("Safe zone", "The inscribed circle; the dashed ring")],
        k.opt_fig("A", "The \u201cu|m\u201d mark in Navy on Cream, the same in all six kits. Light and calm, reads at every size.", pv("tiktok-avatar-a"), 400, 400,
                  links("tiktok-avatar-a"), f"{REL}tiktok-safe-avatar.svg", "sk-art--sq")
        + k.opt_fig("B", "The app icon, “u|m” on Navy (R-93). Reads at every size, also at 32 px.", pv("tiktok-avatar-b"), 400, 400,
                    links("tiktok-avatar-b"), f"{REL}tiktok-safe-avatar.svg", "sk-art--sq"),
        ctx=f"""<div class="sk-ctx sk-ctx--even"><figure><div class="tt-sizes">{''.join(f'<div class="sk-dot" style="width: {s}%; aspect-ratio: 1;"><img src="{pv("tiktok-avatar-a")}" alt="Option A at {p} px"></div>' for s, p in ((40, 116), (28, 96), (10, 32)))}</div><figcaption><b>Option A</b> at 116, 96 and 32. The mark still reads at 32.</figcaption></figure>
<figure><div class="tt-sizes">{''.join(f'<div class="sk-dot" style="width: {s}%; aspect-ratio: 1;"><img src="{pv("tiktok-avatar-b")}" alt="Option B at {p} px"></div>' for s, p in ((40, 116), (28, 96), (10, 32)))}</div><figcaption><b>Option B</b> at 116, 96 and 32. The capsule still reads at 32.</figcaption></figure></div>"""))
    # cover
    feed = lambda o: f"""<figure><div class="sk-phone sk-phone--dark"><div class="tt-feed"><img src="{pv(f'tiktok-cover-{o}')}" alt="Cover option {o.upper()} in the For You feed"><img class="sk-ui" src="{REL}tiktok-ui.svg" alt=""></div></div><figcaption><b>Phone · feed, option {o.upper()}</b> · the rail and caption sit over the video.</figcaption></figure>"""
    web = f"""<figure><div class="sk-desk"><div class="tt-web"><div class="tt-grid-demo">{tile('tiktok-cover-a')}{tile('tiktok-cover-b')}{tile('tiktok-board2-a-01')}</div><div class="tt-vid"><img src="{pv('tiktok-cover-a')}" alt="Cover option A in the desktop player"><img class="sk-ui" src="{REL}tiktok-ui.svg" alt="" style="clip-path: inset(0 0 7.3% 0);"></div><div class="tt-rail" aria-hidden="true"><span></span><span></span><span></span><span></span></div></div></div><figcaption><b>Desktop · player and profile grid</b> · the grid shows the 3:4 centre crop; in the player the buttons move beside the video, the caption still overlays the bottom.</figcaption></figure>"""
    A.append(asset(
        "cover", "Video cover",
        "The still that sells the video in the profile grid and in search. Chosen from a frame or uploaded. The title must survive two crops: the 3:4 profile grid and the feed UI.",
        [("Size", "1080 × 1920 px"), ("Ratio", "9:16; grid shows the centre 3:4 (1080 × 1440)"), ("Type", "PNG or JPG (from the video)"),
         ("Max file", "Part of the video upload"), ("Safe zone", "x 60 to 920, y 240 to 1440: inside both the UI and the 3:4 crop")],
        k.opt_fig("A", "Paper panel, serif headline, the photo below. Faces stay out of the bottom 480.", pv("tiktok-cover-a"), 1080, 1920,
                  links("tiktok-cover-a"), f"{REL}tiktok-safe-9x16.svg", "sk-art--tall")
        + k.opt_fig("B", "Deep Teal, the headline large, two capsules cropped by the edges.", pv("tiktok-cover-b"), 1080, 1920,
                    links("tiktok-cover-b"), f"{REL}tiktok-safe-9x16.svg", "sk-art--tall"),
        ctx=f'<div class="sk-ctx">{web}<div class="sk-pair">{feed("a")}{feed("b")}</div></div>'))
    # text styles
    for kind, title, use, la, lb in (
        ("title", "Title card", "The first frame of a type-led video, or a chapter inside one. One idea, read in a second.",
         "Paper, DM Serif 112 in Teal Deep, the seal top left, one capsule outline in Line.",
         "Deep Teal, DM Serif 124 in Paper, two capsules (outline and split) cropped by the corners."),
        ("caption", "Lower caption", "The caption for every spoken line and every on-screen statement. Sound off is the default, so the caption carries the video.",
         "Paper box, radius 24, Inter SemiBold 50 in Teal Deep, over the photo. Sits on the bottom of the safe area.",
         "The photo framed in a 24 radius window, the statement in DM Serif 84 below. Mist or Paper ground."),
        ("end", "End card", "The last 2 to 3 seconds of every video. The only place with a button and the legal line.",
         "Paper, the Primary seal, the line, one Yellow button, the legal line in Slate.",
         "Deep Teal, the reversed seal, the same lines in Paper, the legal line in Wash Blue."),
    ):
        A.append(asset(
            kind, title, use,
            [("Size", "1080 × 1920 px"), ("Ratio", "9:16"), ("Type", "Frame in the video edit; PNG for reference"),
             ("Min type on a phone", "Headline 84 px, caption 48 px, legal 34 px (at 1080 wide)"), ("Safe zone", "x 60 to 920, y 160 to 1440")],
            k.opt_fig("A", la, pv(f"tiktok-{kind}-a"), 1080, 1920, links(f"tiktok-{kind}-a"), f"{REL}tiktok-safe-9x16.svg", "sk-art--tall")
            + k.opt_fig("B", lb, pv(f"tiktok-{kind}-b"), 1080, 1920, links(f"tiktok-{kind}-b"), f"{REL}tiktok-safe-9x16.svg", "sk-art--tall")))
    # storyboards
    A.append(f"""<article class="sk-asset" id="boards"><h3>Two short video storyboards</h3>
      <p>Six static frames each, in both options, with the captions styled. Every spoken line is on screen. The seal is in the corner from the first frame; the video ends on the end card or on the last 2 seconds of a logo sting (R-101, C2 for short social openers). Faces never sit under a caption.</p>
      {k.spec_dl([("Length", "15 s and 12 s"), ("Frame", "1080 × 1920, 9:16"), ("Sound", "Optional. Music bed and the sting sound; captions repeat every word"), ("Text per frame", "One line, nine words or fewer"), ("Safe zone", "Every caption inside x 60 to 920, y 160 to 1440")])}
      <h3 class="tt-row-h">Storyboard 1 · How it works (15 s)</h3>{board_html(1, BOARD1, 'a')}{board_html(1, BOARD1, 'b')}
      <h3 class="tt-row-h">Storyboard 2 · Things you don’t have to do (12 s)</h3>{board_html(2, BOARD2, 'a')}{board_html(2, BOARD2, 'b')}
      <p class="cap">Lines are candidates from the <a class="link" href="ads.html#ugc">Ads</a> page and the line bank, not approved copy. Storyboard 1, frame 3 needs a real provider photo with written consent; until then the placeholder stays (Photo · not approved · to replace).</p></article>""")

    mobile_rows = [
        ("Profile picture", "Circle, 116 px", "Circle, 96 pt; 32 px in comments", "The inscribed circle", "Both options at any size, down to 32 px"),
        ("Video cover", "3:4 crop in a 6-column grid; full 9:16 in the player with the buttons beside it", "3:4 crop in a 3-column grid; full 9:16 in the feed under the rail and caption", "x 60 to 920, y 240 to 1440", "Headline 100 px or larger"),
        ("Title card", "Full 9:16, centred in the player", "Full screen under the UI", "x 60 to 920, y 160 to 1440", "Headline 84 px or larger"),
        ("Lower caption", "Same frame, caption still over the video bottom", "Same, the TikTok caption sits just below it", "Bottom edge at y 1410 or higher", "48 px, Inter SemiBold"),
        ("End card", "Full 9:16", "Full screen; the platform’s own buttons cover the bottom", "Button and legal line above y 1440", "Legal line 34 px"),
    ]
    mobile = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in mobile_rows)

    files = []
    for name, (w, h, tr) in sorted(ASSETS.items()):
        if "-board" in name:
            continue
        files.append((name + ".png", f"{w} × {h}", k.size_label(OUT / f"{name}.png")))
        if (OUT / f"{name}.jpg").exists():
            files.append((name + ".jpg", f"{w} × {h}, JPG 80 (the PNG is over 1 MB)", k.size_label(OUT / f"{name}.jpg")))
        files.append((name + ".svg", "Source", k.size_label(OUT / f"{name}.svg")))
    for bi in (1, 2):
        for o in "ab":
            files.append((f"tiktok-board{bi}-{o}.zip", "6 × 1080 × 1920, PNG", k.size_label(OUT / f"tiktok-board{bi}-{o}.zip")))
            jz = OUT / f"tiktok-board{bi}-{o}-jpg.zip"
            if jz.exists():
                files.append((jz.name, "Photo frames over 1 MB as JPG 80", k.size_label(jz)))
    files += [("tiktok-safe-9x16.svg", "Safe-zone template", k.size_label(OUT / "tiktok-safe-9x16.svg")),
              ("tiktok-safe-avatar.svg", "Avatar crop template", k.size_label(OUT / "tiktok-safe-avatar.svg")),
              ("make.py", "Generator: rebuilds every file and this page", k.size_label(OUT / "make.py")),
              ("sk_kit.py", "Shared helpers (same file in the YouTube and LinkedIn folders)", k.size_label(OUT / "sk_kit.py"))]
    ftable = "".join(f'<tr><td data-label="File"><a class="link" href="{REL}{n}" download>{n}</a></td><td data-label="Size">{s}</td><td data-label="Weight">{wt}</td></tr>' for n, s, wt in files)

    body = f"""      <header class="page-head">
        <span class="eyebrow">Marketing · Social</span>
        <h1>TikTok.</h1>
        <p class="lead">Everything the unifiedmeds TikTok account needs: the profile, video covers, three on-screen text styles and two short storyboards. Every asset comes in two options, A (editorial, photo-led) and B (graphic, colour-led), shown on desktop and on a phone.</p>
        <nav class="toc" aria-label="On this page"><a href="#profile">Profile</a><a href="#assets">Asset set</a><a href="#mobile">Mobile and desktop</a><a href="#copy">Captions and copy</a><a href="#rules">Rules</a><a href="#files">Files</a></nav>
      </header>

      <div class="grid-2"><div class="rule"><span class="status status--current">Current</span><p>The kit is approved for use. TikTok carries every content type after legal review (U-27); paid ads keep their own, stricter limits on the <a class="link" href="ads.html#policy">Ads</a> page. The profile picture is Option B, the white u|m on Navy (R-93). Legal approves every post before it runs (U-30).</p></div>
      <div class="rule"><span class="status status--proposed">To confirm</span><p>Option A or B per asset (Avi). Lines are candidates; handles and links are placeholders. Photos are Pexels stand-ins, not approved, to replace (R-39, O-13). TikTok publishes no official safe zone: the numbers here are a careful middle of third-party measurements, so check them on a phone before the first post.</p></div></div>

      <section class="sec" id="profile" aria-labelledby="profile-h">
        <div class="sec-head"><h2 id="profile-h">The profile, desktop and mobile.</h2><p>The same account on tiktok.com and in the app. The grid crops every 9:16 cover to its centre 3:4, on both.</p></div>
        {profile_row('a')}
        {profile_row('b')}
      </section>

      <section class="sec" id="assets" aria-labelledby="assets-h">
        <div class="sec-head"><h2 id="assets-h">The asset set.</h2><p>Each block: what it is for, the exact size, the safe zone (the dashed overlay; switch it off to see the art), and Option A beside Option B. Coral marks what the app covers; the blue dotted box is the 3:4 grid crop.</p></div>
        {''.join(A)}
      </section>

      <section class="sec" id="mobile" aria-labelledby="mobile-h">
        <div class="sec-head"><h2 id="mobile-h">Mobile and desktop differences.</h2><p>TikTok is watched on a phone first. Sizes are at the 1080 px frame; on a 390 pt phone everything shows at about a third.</p></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Asset</th><th>Desktop</th><th>Mobile</th><th>Keep inside</th><th>Smallest readable type</th></tr></thead>
          <tbody>{mobile}</tbody></table></div>
      </section>

      <section class="sec" id="copy" aria-labelledby="copy-h">
        <div class="sec-head"><h2 id="copy-h">Captions and copy.</h2><p>Discreet and plain. No prescription names in any social asset or caption, no result promised, no before and after. Every caption that offers the assessment carries the legal line.</p></div>
        <div class="sk-copy">
          <div class="rule"><b>Bio · option 1 (80 characters at most)</b><q>{esc(BIO[0])}</q><p class="cap">{len(BIO[0])} characters.</p></div>
          <div class="rule"><b>Bio · option 2</b><q>{esc(BIO[1])}</q><p class="cap">{len(BIO[1])} characters.</p></div>
          {''.join(f'<div class="rule"><b>Caption {i}</b><q>{esc(c)}</q></div>' for i, c in enumerate(CAPTIONS, 1))}
          <div class="rule"><b>Hashtags</b><p>Three to five. Always #unifiedmeds, then broad tags only (#menshealth, #telehealth). Never a condition, a medicine, a body part or a trend that has nothing to do with the video.</p></div>
          <div class="rule"><b>Link</b><p>One link in the bio, to the homepage [unifiedmeds.com, O-01]. Never a product page, never a link in a comment. Business account settings to confirm before launch.</p></div>
        </div>
      </section>

      <section class="sec" id="rules" aria-labelledby="rules-h">
        <div class="sec-head"><h2 id="rules-h">Rules for this channel.</h2></div>
        <ol class="sk-num">
          <li><p><b>Everything that matters sits inside x 60 to 920, y 160 to 1440.</b> The rail, the caption and the tabs cover the rest.</p></li>
          <li><p><b>Covers keep the headline inside the centre 3:4</b> (y 240 to 1440), so the profile grid shows it whole.</p></li>
          <li><p><b>Every spoken word is on screen</b> in the lower caption style; the video makes sense with the sound off.</p></li>
          <li><p><b>One line per frame</b>, nine words or fewer, at least 48 px at the 1080 frame.</p></li>
          <li><p><b>The seal is in the top left from the first frame</b>; the video ends on the end card or a logo sting (R-101).</p></li>
          <li><p><b>Yellow only on the end card button</b>, once per video (R-11).</p></li>
          <li><p><b>The legal line is in the video</b>, on the end card, whenever the assessment is offered (R-63).</p></li>
          <li><p><b>No face under a caption, no shape under a word</b>; at most two capsules per frame.</p></li>
          <li><p><b>No medicine, result, symptom, price or before and after</b>, in the video, the caption or the hashtags (R-58, R-65, R-67).</p></li>
        </ol>
      </section>

      <section class="sec" id="files" aria-labelledby="files-h">
        <div class="sec-head"><h2 id="files-h">Files.</h2><p>PNG at the exact size, plus the SVG source (fonts load from Google Fonts, photos are embedded). Rebuild everything with <code>python3 -I assets/social/tiktok/make.py</code>.</p></div>
        <div class="table-wrap sk-files"><table>
          <thead><tr><th>File</th><th>Size</th><th>Weight</th></tr></thead>
          <tbody>{ftable}</tbody></table></div>
      </section>
"""
    css += "  .tt-sizes { display: flex; align-items: flex-end; justify-content: center; gap: var(--space-4); width: 100%; }\n"
    (k.EXT / "src" / "social-tiktok.html").write_text(f"<style>{css}</style>\n{body}")


if __name__ == "__main__":
    if "--page" in sys.argv:
        for o in "ab":
            ASSETS[f"tiktok-avatar-{o}"] = (400, 400, False)
        for p in list(OUT.glob("tiktok-*.png")):
            ASSETS.setdefault(p.stem, (1080, 1920, False))
    else:
        build_art()
    page()
    print("tiktok done")
