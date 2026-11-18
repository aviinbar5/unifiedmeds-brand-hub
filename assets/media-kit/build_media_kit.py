"""Build the unifiedmeds media kit (press and partner kit).

Run from the merged hub root (unifiedmeds-brand-hub-merged/):
    python3 -I assets/media-kit/build_media_kit.py

What it does
  1. Copies the logo SVGs from assets/brand/ (the one logo folder, A-15).
     The logo files are never redrawn or edited, only copied, scaled and placed.
     The one-colour versions (R-94: Black on white, White on black, technical uses only)
     are the same files with every colour set to black or to white, nothing else changed.
  2. Renders PNG exports with macOS `sips` (CoreSVG): every lockup at 800 px and
     2400 px wide, the app icon at 512 and 1024, and three social and mobile files
     (avatar 400 x 400, story 1080 x 1920, share card 1200 x 630).
  3. Writes the text files (boilerplates, fact sheet .md and .txt, colours and type,
     press usage, press release template, contact, README) from the strings below.
     Colours are read from tokens/tokens.json, the single home of every value.
  4. Writes everything to assets/media-kit/kit/ (the page links single files there)
     and packs assets/media-kit/unifiedmeds-media-kit.zip with fixed timestamps, so the
     same sources give the same ZIP. Photos and product shots go into the ZIP only,
     straight from assets/photos/ and assets/packaging/ (already web size). Only credited
     stand-ins (assets/photos/CREDITS.md); the earlier photos of unknown source are out (U-31).
  5. Checks the copy: exact boilerplate word counts (25, 50, 100), no em or en dashes,
     no wrong spelling of the name, no claim words, and that the page source
     (src/media-kit.html) carries the same boilerplates.

Status: to confirm (legal review before first use). Every [bracket] is an unknown fact; fill it, never guess it.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent             # assets/media-kit
EXT = HERE.parents[1]                              # unifiedmeds-brand-hub-merged (site root)
CORE = EXT                                         # one site since the merge (Edition 04)
BRAND = CORE / "assets" / "brand"
KIT = HERE / "kit"
ZIP = HERE / "unifiedmeds-media-kit.zip"
TOP = "unifiedmeds-media-kit"                      # folder name inside the ZIP
STAMP = (2026, 11, 18, 0, 0, 0)                    # fixed ZIP timestamp
DATE_US = "November 18, 2026"
EDITION = "Brand Edition 04"

# ---------------------------------------------------------------- copy (US English)

BOILERPLATE = {
    25: (
        "unifiedmeds is online men's health care. A man completes an assessment, a licensed "
        "U.S. provider reviews it, and if treatment is appropriate, it ships discreetly."
    ),
    50: (
        "unifiedmeds is a men's health telehealth brand launching with Sexual health. "
        "A man completes a short online assessment. A licensed U.S. provider reviews it and "
        "decides whether treatment is right for him. If it is, a licensed U.S. pharmacy "
        "prepares and ships it in plain packaging. Care continues after delivery."
    ),
    100: (
        "unifiedmeds is a men's health telehealth brand. It launches with Sexual health, and "
        "Longevity and Hair loss are planned to follow. A man starts with a short online "
        "assessment, from home, on his own schedule. A licensed U.S. provider reviews his "
        "answers, may ask follow-up questions, and decides whether treatment is right for him. "
        "If it is, a licensed U.S. pharmacy prepares the prescription and ships it in plain "
        "packaging, with nothing on the outside about what is inside. Care continues after "
        "delivery: the member can message his care team, and a provider reviews every refill. "
        "The brand speaks plainly."
    ),
}

PARTNER_ABOUT = (
    "unifiedmeds is online men's health care. A member completes an online assessment, a "
    "licensed U.S. provider reviews it, and if treatment is appropriate, a licensed U.S. "
    "pharmacy ships it in plain packaging. Partners may use this text, the logo files and "
    "the colors in this kit as supplied, without changes."
)

STEPS = [
    ("Assessment", "A short online assessment, from home, on his own schedule. [Length · operations, O-12]"),
    ("Provider review", "A licensed U.S. provider reviews the answers, may ask follow-up questions and decides whether treatment is appropriate."),
    ("Pharmacy", "If it is, a licensed U.S. pharmacy prepares the prescription and ships it in plain packaging. [Delivery time · operations, R-68]"),
    ("Care continues", "The member can message his care team, and a provider reviews every refill."),
]

FACTS = [
    ("Name", "unifiedmeds. Always lowercase and one word, also at the start of a sentence."),
    ("What it is", "Online men's health care (telehealth)."),
    ("Categories", "Sexual health at launch. Longevity and Hair loss are planned."),
    ("Launch products", "Tadalafil, Sildenafil and Combo. Prescription only: prescribed only when a licensed provider decides treatment is appropriate. [What Combo contains · clinical team]"),
    ("How care works", " / ".join(f"{i}. {name}" for i, (name, _) in enumerate(STEPS, 1))),
    ("Where", "[States served · operations]"),
    ("Founded", "[Year · legal, O-01]"),
    ("Headquarters", "[City, state · legal, O-01]"),
    ("Legal entity", "[Entity name · legal, O-01]"),
    ("Website", "[Domain · legal, O-01]"),
    ("Press contact", "[press@ · legal, O-01]"),
]

USAGE_NAME_DO = ["unifiedmeds"]
USAGE_NAME_DONT = ["Unifiedmeds", "UnifiedMeds", "Unified Meds", "UNIFIEDMEDS", "unified meds", "Unified-meds"]

USAGE_SAY = [
    ("online men's health care", "the plain description of the service"),
    ("a licensed U.S. provider reviews each assessment", "who is responsible for the decision"),
    ("if treatment is appropriate", "a prescription is never a given"),
    ("ships in plain packaging", "what discretion means, without promising more"),
    ("provider, assessment, member", "the brand's words for clinician, quiz or visit, and patient"),
]
USAGE_AVOID = [
    ("cure, fix, solve, guaranteed, proven", "no medical or results promises"),
    ("works in minutes, lasts for hours, better than", "no durations or comparisons outside a product page"),
    ("the best pill for..., try tadalafil", "never name a medicine as a recommendation"),
    ("100% anonymous, nobody will ever know", "no privacy promise nobody can verify"),
    ("1 in X men, X% of members", "no statistics until legal approves real data (R-67)"),
    ("doctor, quiz, patient", "use provider, assessment, member"),
]
CREDIT_LINE = "Image: unifiedmeds"

RELEASE = """\
PRESS RELEASE TEMPLATE · unifiedmeds
Proposed. Every line goes through legal before it is sent.
Fill every [bracket]. Never guess a fact, a number or a date.

FOR IMMEDIATE RELEASE   or   EMBARGOED UNTIL [Month Day, Year, time, time zone]

[Headline: one plain sentence, sentence case, ending with a full stop. No medicine name, no claim, no number.]

[Subhead: one sentence that says what is new and for whom.]

[CITY, State], [Month Day, Year]. unifiedmeds, [one-line description from the 25-word boilerplate], today [announced / launched / opened] [what, in plain words].

[Paragraph 2: what changes for men, and how care works: online assessment, review by a licensed U.S. provider, a licensed U.S. pharmacy, plain packaging. Say "if treatment is appropriate".]

[Paragraph 3: availability. Where: [States served · operations]. When: [date]. Price only if legal and operations approve it.]

"[Quote, two sentences at most, approved by legal.]" said [Name, title · only if approved].

[Optional paragraph 4: what comes next, only if approved. Longevity and Hair loss are planned.]

If a product is named in the body, the safety information link sits in the same paragraph: [Safety information URL · legal].

About unifiedmeds
[Paste the 100-word boilerplate unchanged.]

Media contact
[press@ · legal, O-01]
[Phone · legal, O-01]
Response time: [within X business hours · operations]

Images and logos: [media kit URL]. Image credit: "Image: unifiedmeds".

###
"""

CONTACT = """\
PRESS CONTACT · unifiedmeds

Press:          [press@ · legal, O-01]
Phone:          [Phone · legal, O-01]
Partnerships:   [partners@ · legal, O-01]
Response time:  [within X business hours · operations, R-68]

No interviews with members and no case stories until legal approves a consent process.
Questions about a person's own health go to [support channel · operations], never to the press line.
"""

# ---------------------------------------------------------------- logo files

LOCKUPS = [
    # (file stem in core, kit name, ground note)
    ("logo-seal", "unifiedmeds-logo-seal", "light grounds: Paper, Mist, Cream, white"),
    ("logo-seal-reversed", "unifiedmeds-logo-seal-reversed", "dark grounds and photos: Deep Teal, Ink, Navy"),
    ("logo-horizontal", "unifiedmeds-logo-horizontal", "light grounds"),
    ("logo-horizontal-reversed", "unifiedmeds-logo-horizontal-reversed", "dark grounds and photos"),
    ("logo-stacked", "unifiedmeds-logo-stacked", "light grounds"),
    ("logo-stacked-reversed", "unifiedmeds-logo-stacked-reversed", "dark grounds and photos"),
]
PNG_WIDTHS = [800, 2400]
ICON_SIZES = [512, 1024]

PHOTOS = [
    # (source relative to EXT/assets, name in ZIP, description)
    ("packaging/bottle-tadalafil.png", "product/bottle-tadalafil.png", "Tadalafil bottle, closed, front label"),
    ("packaging/bottle-sildenafil.png", "product/bottle-sildenafil.png", "Sildenafil bottle, closed, front label"),
    ("packaging/bottle-combo.png", "product/bottle-combo.png", "Combo bottle, closed, front label"),
    # credited Pexels stand-ins only (assets/photos/CREDITS.md); hub use, not licensed for press
    ("photos/man-reading-window-wide-2048-pexels-8217708.jpg", "lifestyle/man-at-home-wide.jpg", "A man reading by a tall window at home, wide (Pexels, RDNE Stock project)"),
    ("photos/man-kitchen-coffee-pexels-6269909.jpg", "lifestyle/man-in-kitchen.jpg", "A man with a cup at his kitchen table (Pexels, cottonbro studio)"),
    ("photos/friends-talking-outdoors-pexels-13335592.jpg", "lifestyle/two-men-outdoors.jpg", "Two men talking at an outdoor table (Pexels, Mizuno K)"),
    ("photos/couple-breakfast-pexels-6248662.jpg", "lifestyle/couple-at-home.jpg", "A couple talking at the kitchen table (Pexels, Gary Barnes)"),
    ("photos/man-paperwork-sunlit-pexels-8124229.jpg", "lifestyle/man-portrait.jpg", "A man in a sunlit room, portrait (Pexels, RDNE Stock project)"),
    ("photos/man-mug-sunlight-pexels-6972779.jpg", "lifestyle/man-portrait-2.jpg", "A man with a mug in window light, portrait (Pexels, Mikhail Nilov)"),
    ("photos/couple-dog-article-header-2x1-pexels-11284049.jpg", "lifestyle/article-header-wide.jpg", "A couple with a dog outdoors, 2:1 article header (Pexels, Centre for Ageing Better)"),
    ("photos/man-warm-light-vertical-9x16-pexels-40409561.jpg", "lifestyle/story-vertical-1.jpg", "A man in warm light, 9:16 for phone stories (Pexels, Doğan Alpaslan Demir)"),
    ("photos/man-beard-profile-vertical-9x16-pexels-6973179.jpg", "lifestyle/story-vertical-2.jpg", "A man in profile, 9:16 for phone stories (Pexels, Mikhail Nilov)"),
]
PLACEHOLDER = "Placeholder, not licensed for press"


def tokens():
    return json.loads((CORE / "tokens" / "tokens.json").read_text())


ONE_COLOUR = [("logo-seal", "unifiedmeds-logo-seal"), ("logo-horizontal", "unifiedmeds-logo-horizontal"), ("logo-stacked", "unifiedmeds-logo-stacked")]


def one_colour(svg_text, hexv):
    """R-94: the same logo file with every fill and stroke colour set to one colour. Nothing else changes."""
    return re.sub(r'((?:fill|stroke)=")#[0-9A-Fa-f]{3,8}(")', rf"\g<1>{hexv}\g<2>", svg_text)


def tok(t, path):
    node = t
    for k in path.split("."):
        node = node[k]
    v = node["$value"]
    if isinstance(v, str) and v.startswith("{"):
        return tok(t, v.strip("{}"))
    return v


COLOURS = [
    # (group, name, token path, use)
    ("Logo colors (logo, app icon and favicon only)", "Navy", "color.logo.navy", "Main logo color on light grounds; app icon ground"),
    ("Logo colors (logo, app icon and favicon only)", "Ink", "color.logo.ink", "\"meds\" on light; darkest logo ground"),
    ("Logo colors (logo, app icon and favicon only)", "Sky", "color.logo.sky", "Reversed logo outline and wordmark"),
    ("Logo colors (logo, app icon and favicon only)", "Logo Blue", "color.logo.blue", "Filled half of the reversed seal"),
    ("Logo colors (logo, app icon and favicon only)", "Cream", "color.logo.cream", "Light ground for the logo"),
    ("Brand colors (website and print)", "Deep Teal", "color.brand.deep-teal", "Primary ink, dark sections, the ground behind the reversed logo"),
    ("Brand colors (website and print)", "Teal Deep", "color.brand.teal-deep", "Headlines"),
    ("Brand colors (website and print)", "Paper", "color.surface.paper", "The page"),
    ("Brand colors (website and print)", "Mist", "color.surface.mist", "Alternate band"),
    ("Brand colors (website and print)", "Yellow", "color.brand.yellow", "One accent at a time; never a background, never text"),
    ("Brand colors (website and print)", "Pastel Blue", "color.brand.blue", "Shapes and surfaces"),
    ("Brand colors (website and print)", "Pastel Green", "color.brand.green", "Shapes and icons"),
]


def rgb(hexv):
    h = hexv.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- checks

BANNED_IN_COPY = re.compile(r"\b(cure[sd]?|guarantee[sd]?|proven|miracle|doctor|patient|quiz)\b", re.I)
WRONG_NAME = re.compile(r"Unifiedmeds|UnifiedMeds|Unified Meds|UNIFIEDMEDS|unified meds")


def words(s):
    return len(s.split())


def check_copy(page_src):
    problems = []
    for n, text in BOILERPLATE.items():
        if words(text) != n:
            problems.append(f"boilerplate {n}: {words(text)} words")
    copy = list(BOILERPLATE.values()) + [PARTNER_ABOUT] + [v for _, v in FACTS] + [v for _, v in STEPS]
    for text in copy:
        if BANNED_IN_COPY.search(text):
            problems.append(f"claim or glossary word in: {text[:60]}")
        if WRONG_NAME.search(text):
            problems.append(f"wrong name spelling in: {text[:60]}")
    for text in copy + [RELEASE, CONTACT]:
        if "—" in text or "–" in text:
            problems.append(f"dash in: {text[:60]}")
    for n, text in BOILERPLATE.items():
        if text not in page_src:
            problems.append(f"boilerplate {n} differs from src/media-kit.html")
    if PARTNER_ABOUT not in page_src:
        problems.append("partner about differs from src/media-kit.html")
    return problems


# ---------------------------------------------------------------- rendering

def svg_size(text):
    m = re.search(r'<svg[^>]*\bwidth="([\d.]+)"[^>]*\bheight="([\d.]+)"', text)
    return float(m.group(1)), float(m.group(2))


def inner(text):
    """The logo file without its outer <svg> tag, for placing it unchanged."""
    return re.sub(r"^\s*<svg[^>]*>|</svg>\s*$", "", text.strip())


def sips_png(svg_text, out, tmp):
    src = tmp / (out.stem + ".svg")
    src.write_text(svg_text)
    subprocess.run(["sips", "-s", "format", "png", str(src), "--out", str(out)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    got = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(out)],
                         check=True, capture_output=True, text=True).stdout
    w, h = (int(x) for x in re.findall(r"pixel\w+: (\d+)", got))
    return w, h


def scaled(svg_text, width):
    w, h = svg_size(svg_text)
    H = round(width * h / w)
    out = re.sub(r'(<svg[^>]*?)\bwidth="[\d.]+"', rf'\g<1>width="{width}"', svg_text, count=1)
    out = re.sub(r'(<svg[^>]*?)\bheight="[\d.]+"', rf'\g<1>height="{H}"', out, count=1)
    return out, H


def placed(ground_hex, W, H, logo_text, box_w):
    """A ground of W x H with the logo file centred, box_w wide. Nothing redrawn."""
    w, h = svg_size(logo_text)
    vb = re.search(r'viewBox="([^"]+)"', logo_text).group(1)
    bh = box_w * h / w
    x, y = (W - box_w) / 2, (H - bh) / 2
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{W}" height="{H}" fill="{ground_hex}"/>'
            f'<svg x="{x:.2f}" y="{y:.2f}" width="{box_w}" height="{bh:.2f}" viewBox="{vb}" fill="none">'
            f'{inner(logo_text)}</svg></svg>')


# ---------------------------------------------------------------- branded photos (R-109, R-110)
# Photos that carry the brand: a true capsule (both halves with the divider, R-109, stroke 0.85% of its
# length, the long half filled translucent inside the line), a Quadrant piece, or the corner logo stamp.
# Never over a face, never under text, at most two shapes per photo, stamp included.

FORMATS = [
    # key, W, H, label, where it runs
    ("16x9", 1920, 1080, "16:9 · 1920 × 1080", "Desktop and web: article body, LinkedIn, YouTube, X"),
    ("1x1", 1080, 1080, "1:1 · 1080 × 1080", "Square feed: Instagram, Facebook, LinkedIn"),
    ("4x5", 1080, 1350, "4:5 · 1080 × 1350", "Phone feed: Instagram, Facebook"),
    ("9x16", 1080, 1920, "9:16 · 1080 × 1920", "Phone full screen: stories, Reels, TikTok, Shorts"),
]
STORY_TOP, STORY_BOTTOM = 0.14, 0.20      # 9:16 platform UI zones (Social page)


def outline_capsule(x, y, L, vertical=False):
    """R-109 (Avi 17.11.2026): the two halves with the divider at every size, as in the seal:
    the long half open toward the joint, the short, taller half closed by the divider line.
    Returns (outline_d, long_half_d, (box_w, box_h)): outline_d holds both halves as two
    subpaths; long_half_d is the filled long half, inset 1.5 strokes like the seal's.
    Geometry from tools/capsule_svg.py capsule_paths() (the logo's own capsule)."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(EXT / "tools"))
    from capsule_svg import capsule_paths
    sw = max(1.5, 0.0085 * L)
    ld, rd, box = capsule_paths(x, y, L, vertical)
    long_half = capsule_paths(x, y, L, vertical, inset=1.5 * sw)[0] + "Z"
    return ld + rd, long_half, box


def capsule_el(x, y, L, vertical, line, fill, soft):
    o, lh, _ = outline_capsule(x, y, L, vertical)
    sw = max(1.5, 0.0085 * L)
    return (f'<path d="{lh}" fill="{fill}" fill-opacity="{soft}"/>'
            f'<path d="{o}" fill="none" stroke="{line}" stroke-width="{sw:.2f}"/>')


def stamp_el(stamps, W, H, corner, tone, story=False):
    """The photo stamp: the LOGO ICON, the u|m mark without its Navy tile (R-110),
    from assets/shapes/logo-stamp-paper.svg or logo-stamp-teal.svg, placed
    unchanged. Long side 12% of the image's short side (130 px on 1080), margin 1.5% of the
    short side (16 px equivalent). Paper on dark or busy photos, Deep Teal on light ones.
    On 9:16 it stays out of the platform UI zones."""
    text = stamps[tone]
    vb = re.search(r'viewBox="([^"]+)"', text).group(1)
    vw, vh = (float(v) for v in vb.split()[2:])
    m = 0.015 * min(W, H)
    w = 0.12 * min(W, H)
    h = w * vh / vw
    top = STORY_TOP * H + m if story else m
    bottom = H - (STORY_BOTTOM * H if story else 0) - m - h
    x = m if "l" in corner else W - m - w
    y = top if "t" in corner else bottom
    return f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" viewBox="{vb}" fill="none">{inner(text)}</svg>'


def photo_el(data_uri, iw, ih, W, H, fx, fy):
    """The photo cropped to W x H around a focus point (cover)."""
    k = max(W / iw, H / ih)
    sw_, sh_ = iw * k, ih * k
    ox = min(0, max(W - sw_, W / 2 - fx * sw_))
    oy = min(0, max(H - sh_, H / 2 - fy * sh_))
    return f'<image x="{ox:.2f}" y="{oy:.2f}" width="{sw_:.2f}" height="{sh_:.2f}" href="{data_uri}"/>', k


def treatments(t):
    teal = tok(t, "color.brand.deep-teal").upper()
    paper = tok(t, "color.surface.paper").upper()
    wash = tok(t, "color.surface.wash-blue").upper()
    soft = tok(t, "opacity.capsule-soft")

    def t1(W, H, k, icon):
        # light photo, man on the right: capsule enters from the bottom-left corner toward him
        L = 0.45 * W
        Hc = L * 0.3583
        if H / W > 1.7:
            # 9:16: the man fills the frame, so the capsule moves up to the window wall (R-110, mobile)
            return capsule_el(-0.25 * L, (STORY_TOP + 0.04) * H, L, False, teal, wash, soft)
        return capsule_el(-0.25 * L, H - 0.05 * H - Hc, L, False, teal, wash, soft)

    def t2(W, H, k, icon):
        # dark photo, face upper right: standing capsule rises from the bottom-left edge; stamp top-left
        L = 0.62 * H if H > W else 0.8 * H
        x = 0.05 * W
        return (capsule_el(x, H - 0.85 * L, L, True, paper, paper, soft)
                + stamp_el(icon, W, H, "tl", "paper", story=(H / W > 1.7)))

    def t3(W, H, k, icon):
        # busy outdoor photo, face right of centre: a Quarter in the top-left corner (trees); stamp bottom-left
        r = 0.3 * min(W, H)
        q = f'<path d="M0 0L{r:.2f} 0A{r:.2f} {r:.2f} 0 0 1 0 {r:.2f}Z" fill="{paper}" fill-opacity="{soft}"/>'
        return q + stamp_el(icon, W, H, "bl", "paper", story=(H / W > 1.7))

    return [
        dict(slug="capsule-on-light", src="photos/man-reading-window-wide-2048-pexels-8217708.jpg", focus=(0.62, 0.48),
             name="Capsule on a light photo", note="Deep Teal outline, long half in Wash Blue at 50%. Enters from the left edge on the floor, toward the man; never over his face. On 9:16 the man fills the frame, so it moves up to the wall, below the top UI zone.", draw=t1),
        dict(slug="capsule-and-stamp-on-dark", src="photos/man-beard-profile-vertical-9x16-pexels-6973179.jpg", focus=(0.55, 0.32),
             name="Capsule and stamp on a dark photo", note="Paper outline, long half in Paper at 50%, standing, rising from the bottom edge. The logo icon (u|m) sits top left as a Paper stamp. Two shapes.", draw=t2),
        dict(slug="quadrant-and-stamp", src="photos/man-resting-forest-pexels-27915307.jpg", focus=(0.57, 0.4),
             name="Quadrant piece and stamp", note="A Quarter in Paper at 50%, cropped by the top-left corner, over the trees and clear of the face. The logo icon stamp (Paper) sits bottom left, above the 9:16 UI zone.", draw=t3),
    ]


def render_branded(t, icon_inner, tmp, problems):
    """Renders every treatment in every format. Returns [(zip_rel, local_path, size, treatment, format)]."""
    import base64
    out = []
    for tr in treatments(t):
        src = EXT / "assets" / tr["src"]
        if not src.exists():
            problems.append(f"missing branded photo source {tr['src']}")
            continue
        got = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(src)],
                             check=True, capture_output=True, text=True).stdout
        iw, ih = (int(v) for v in re.findall(r"pixel\w+: (\d+)", got))
        uri = "data:image/jpeg;base64," + base64.b64encode(src.read_bytes()).decode()
        for key, W, H, label, where in FORMATS:
            img, k = photo_el(uri, iw, ih, W, H, *tr["focus"])
            svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
                   f'{img}{tr["draw"](W, H, k, icon_inner)}</svg>')
            rel = f"05-images-PLACEHOLDER/branded/{tr['slug']}-{key}.jpg"
            p = KIT / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            s_ = tmp / f"{tr['slug']}-{key}.svg"
            s_.write_text(svg)
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80", str(s_), "--out", str(p)],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            gw = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(p)],
                                check=True, capture_output=True, text=True).stdout
            size = tuple(int(v) for v in re.findall(r"pixel\w+: (\d+)", gw))
            if size != (W, H):
                problems.append(f"{rel}: rendered {size}, expected {(W, H)}")
            if k > 1.0:
                problems_note.append(f"{rel}: photo enlarged {k:.2f}x (placeholder source too small)")
            out.append((rel, p, size, tr, key))
    return out


problems_note = []


# ---------------------------------------------------------------- text files

def fact_sheet_md():
    out = ["# unifiedmeds · Fact sheet", "",
           f"Media kit, {EDITION} · {DATE_US} · To confirm. Every [bracket] is a fact still to be confirmed.", "",
           "| | |", "|---|---|"]
    out += [f"| **{k}** | {v} |" for k, v in FACTS]
    out += ["", "## How care works", ""]
    out += [f"{i}. **{k}.** {v}" for i, (k, v) in enumerate(STEPS, 1)]
    out += ["", "## About unifiedmeds", "", BOILERPLATE[100], "",
            "## Writing the name", "",
            "unifiedmeds: all lowercase, one word, also at the start of a sentence and in headlines.", ""]
    return "\n".join(out)


def fact_sheet_txt():
    width = max(len(k) for k, _ in FACTS) + 2
    out = ["unifiedmeds · FACT SHEET", f"Media kit, {EDITION} · {DATE_US} · To confirm",
           "Every [bracket] is a fact still to be confirmed.", ""]
    out += [f"{k + ':':<{width}}{v}" for k, v in FACTS]
    out += ["", "HOW CARE WORKS"]
    out += [f"{i}. {k}. {v}" for i, (k, v) in enumerate(STEPS, 1)]
    out += ["", "ABOUT unifiedmeds", BOILERPLATE[100], "",
            "The name is written unifiedmeds: all lowercase, one word, also in headings.", ""]
    return "\n".join(out)


def boilerplate_txt():
    out = ["ABOUT unifiedmeds · BOILERPLATE", f"Media kit, {EDITION} · {DATE_US} · To confirm, legal review required", ""]
    for n, text in BOILERPLATE.items():
        out += [f"{n} words", text, ""]
    out += ["Use the text unchanged. The name is always unifiedmeds, lowercase, also at the start of a sentence.", ""]
    return "\n".join(out)


def partner_txt():
    return "\n".join(["ABOUT unifiedmeds · FOR PARTNERS", f"{EDITION} · {DATE_US} · To confirm", "",
                      PARTNER_ABOUT, "",
                      "Logo: use the files in 01-logos as supplied. Never recolor, stretch, rotate or redraw them.",
                      "Link to: [Domain · legal, O-01]", ""])


def colours_txt(t):
    out = ["unifiedmeds · COLORS AND TYPE", f"{EDITION} · {DATE_US} · values from tokens/tokens.json", "",
           "CMYK and Pantone values are not set yet: [CMYK · printer proof, to confirm]. Do not convert by eye.", ""]
    group = None
    for g, name, path, use in COLOURS:
        if g != group:
            out += ["", g.upper()]
            group = g
        hx = tok(t, path).upper()
        r, gg, b = rgb(hx)
        out.append(f"{name:<14}{hx}   RGB {r:>3} {gg:>3} {b:>3}   CMYK [to confirm]   {use}")
    out += ["", "TYPE",
            "DM Serif Display, Regular only: headlines. Google Fonts, SIL Open Font License.",
            "Inter, 400 to 700: text, labels, buttons. Google Fonts, SIL Open Font License.",
            "The logo wordmark is artwork (drawn in Outfit Medium). Never retype the logo in any font.", ""]
    return "\n".join(out)


def usage_txt():
    out = ["WRITING ABOUT unifiedmeds · PRESS USAGE", f"{EDITION} · {DATE_US} · To confirm", "",
           "THE NAME", "Write: unifiedmeds (all lowercase, one word, also at the start of a sentence and in headlines).",
           "Never: " + ", ".join(USAGE_NAME_DONT) + ".", "",
           "DESCRIBING THE SERVICE: SAY"]
    out += [f"  {a}  ({b})" for a, b in USAGE_SAY]
    out += ["", "AVOID"]
    out += [f"  {a}  ({b})" for a, b in USAGE_AVOID]
    out += ["", "MEDICINES",
            "Tadalafil, Sildenafil and Combo are prescription products. Name them as facts, never as a recommendation,",
            "never in a headline, and never next to a benefit. A licensed provider decides whether any treatment is appropriate.", "",
            "IMAGES",
            f"Credit line: {CREDIT_LINE}",
            f"The photos in 05-images are placeholders, credited free stand-ins, not licensed for press (R-39). Do not publish them.", ""]
    return "\n".join(out)


def readme(png_list, social_list):
    out = ["unifiedmeds · MEDIA KIT", f"{EDITION} · {DATE_US}",
           "Status: to confirm. Facts in [brackets] are not confirmed yet; images are placeholders.", "",
           "CONTENTS", "",
           "01-logos/svg/                   The logo files, vector. Use these wherever you can.",
           "01-logos/png/                   Every lockup at 800 px (screen) and 2400 px (print and large screens) wide,",
           "                                transparent background; the app icon at 512 and 1024 px.",
           "01-logos/one-colour/            Black on white and White on black (R-94), technical uses only:",
           "                                fax, emboss, stamp, one-colour print. SVG and PNG 2400.",
           "01-logos/social-and-mobile/     avatar-400x400.png (profile picture, safe in a circle crop),",
           "                                story-1080x1920.png (phone, full screen), share-card-1200x630.png (link preview),",
           "                                logo cards 16:9 1920 x 1080, 1:1 1080 x 1080, 4:5 1080 x 1350.",
           "02-fact-sheet/                  The fact sheet as Markdown (.md) and plain text (.txt).",
           "03-about/                       Boilerplate in 25, 50 and 100 words; a short about for partners.",
           "04-color-and-type/              Colors with HEX and RGB (CMYK to confirm) and the two typefaces.",
           f"05-images-PLACEHOLDER/          Product shots and lifestyle photos at web size. {PLACEHOLDER.upper()} (R-39).",
           "05-images-PLACEHOLDER/branded/  Photos carrying the capsule, a Quadrant piece or the logo stamp, each in",
           "                                16:9 (1920 x 1080), 1:1 (1080 x 1080), 4:5 (1080 x 1350) and 9:16 (1080 x 1920).",
           "06-press/                       How to write about unifiedmeds, a press release template, the press contact.", "",
           "LOGO FILES",
           "  Main versions (Navy) on light grounds. Reversed versions on dark grounds and photos only.",
           "  Clear space: the height of the \"meds\" half on every side. Never recolor, stretch, rotate, redraw or add effects.",
           "  The capsule is not symmetric: the left half is longer, the right half is taller. Never redraw it.", "",
           "PLACEHOLDERS STILL OPEN",
           "  Founded, headquarters, legal entity, website, press email: legal (O-01).",
           "  Response time, delivery time, assessment length, states served: operations.",
           "  What Combo contains: clinical team.",
           "  Photography: a commissioned shoot plus licensed stock (Q91). Until then no image in this kit may be published.",
           "  CMYK values: printer proof.", "",
           "PNG FILES",
           ] + [f"  {p}" for p in png_list + social_list] + ["",
           "Built by build_media_kit.py in the unifiedmeds Brand Hub (assets/media-kit/).", ""]
    return "\n".join(out)


# ---------------------------------------------------------------- build

def main():
    page_src = (EXT / "src" / "media-kit.html").read_text()
    problems = check_copy(page_src)

    if KIT.exists():
        shutil.rmtree(KIT)
    files = {}                                        # name in ZIP -> local path
    t = tokens()
    navy = tok(t, "color.logo.navy").upper()
    teal = tok(t, "color.brand.deep-teal").upper()

    def put(rel, data=None, src=None):
        p = KIT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if src is not None:
            shutil.copyfile(src, p)
        elif isinstance(data, str):
            if WRONG_NAME.search(data) and "writing-about" not in rel:
                problems.append(f"{rel}: wrong spelling of the name")
            if "\u2014" in data or "\u2013" in data:
                problems.append(f"{rel}: em or en dash")
            p.write_text(data)
        files[f"{TOP}/{rel}"] = p
        return p

    png_list, social_list = [], []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for stem, name, _ in LOCKUPS + [("app-icon", "unifiedmeds-app-icon", "")]:
            text = (BRAND / f"{stem}.svg").read_text()
            put(f"01-logos/svg/{name}.svg", src=BRAND / f"{stem}.svg")
            widths = ICON_SIZES if stem == "app-icon" else PNG_WIDTHS
            for w in widths:
                svg, H = scaled(text, w)
                rel = f"01-logos/png/{name}-{w}.png"
                p = KIT / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                gw, gh = sips_png(svg, p, tmp)
                if (gw, gh) != (w, H):
                    problems.append(f"{rel}: rendered {gw}x{gh}, expected {w}x{H}")
                files[f"{TOP}/{rel}"] = p
                png_list.append(f"{rel.split('/')[-1]}  {gw} x {gh}")

        for stem, name in ONE_COLOUR:
            text = (BRAND / f"{stem}.svg").read_text()
            for tone, hexv in (("black", "#000000"), ("white", "#FFFFFF")):
                svg1 = one_colour(text, hexv)
                put(f"01-logos/one-colour/{name}-{tone}.svg", svg1)
                big, H = scaled(svg1, 2400)
                rel = f"01-logos/one-colour/{name}-{tone}-2400.png"
                p = KIT / rel
                gw, gh = sips_png(big, p, tmp)
                if (gw, gh) != (2400, H):
                    problems.append(f"{rel}: rendered {gw}x{gh}, expected 2400x{H}")
                files[f"{TOP}/{rel}"] = p
                png_list.append(f"{rel.split('/')[-1]}  {gw} x {gh}")

        icon = (BRAND / "app-icon.svg").read_text()
        seal_rev = (BRAND / "logo-seal-reversed.svg").read_text()
        hor_rev = (BRAND / "logo-horizontal-reversed.svg").read_text()
        social = [
            # The app icon on a full Navy square: the rounded corners fill with the same Navy,
            # so square and circle crops both work. Capsule stays inside the circle.
            ("avatar-400x400.png", placed(navy, 400, 400, icon, 400), (400, 400)),
            # Phone story: reversed seal, 600 px wide, centred, inside the 1080 x 1420 safe zone.
            ("story-1080x1920.png", placed(teal, 1080, 1920, seal_rev, 600), (1080, 1920)),
            # Link preview: reversed horizontal lockup, 640 px wide, centred.
            ("share-card-1200x630.png", placed(teal, 1200, 630, hor_rev, 640), (1200, 630)),
            # The same logo card in every screen format (round 2: mobile proportions).
            ("logo-card-16x9-1920x1080.png", placed(teal, 1920, 1080, seal_rev, 760), (1920, 1080)),
            ("logo-card-1x1-1080x1080.png", placed(teal, 1080, 1080, seal_rev, 600), (1080, 1080)),
            ("logo-card-4x5-1080x1350.png", placed(teal, 1080, 1350, seal_rev, 600), (1080, 1350)),
        ]
        for fname, svg, size in social:
            rel = f"01-logos/social-and-mobile/{fname}"
            p = KIT / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            got = sips_png(svg, p, tmp)
            if got != size:
                problems.append(f"{rel}: rendered {got}, expected {size}")
            files[f"{TOP}/{rel}"] = p
            social_list.append(f"{fname}  {got[0]} x {got[1]}")

        stamps = {tone: (EXT / "assets" / "shapes" / f"logo-stamp-{tone}.svg").read_text()
                  for tone in ("paper", "teal")}                       # the logo icon, u|m
        branded = render_branded(t, stamps, tmp, problems)
        for rel, p, size, tr, key in branded:
            files[f"{TOP}/{rel}"] = p

    put("02-fact-sheet/unifiedmeds-fact-sheet.md", fact_sheet_md())
    put("02-fact-sheet/unifiedmeds-fact-sheet.txt", fact_sheet_txt())
    put("03-about/boilerplate-25-50-100-words.txt", boilerplate_txt())
    put("03-about/about-for-partners.txt", partner_txt())
    put("04-color-and-type/colors-and-type.txt", colours_txt(t))
    put("06-press/writing-about-unifiedmeds.txt", usage_txt())
    put("06-press/press-release-template.txt", RELEASE)
    put("06-press/press-contact.txt", CONTACT)
    put("README.txt", readme(png_list, social_list))

    # images: ZIP only, straight from the hub's assets (already web size)
    images = {}
    for src_rel, zip_rel, _ in PHOTOS:
        src = EXT / "assets" / src_rel
        if not src.exists():
            problems.append(f"missing image {src_rel}")
            continue
        images[f"{TOP}/05-images-PLACEHOLDER/{zip_rel}"] = src
    note = ("PLACEHOLDER IMAGES, NOT LICENSED FOR PRESS (R-39)\n\n"
            "Every file in this folder is a placeholder used while the brand is built:\n"
            "credited Pexels stand-ins (hub use only) and product mockups.\n"
            "None of them may be published, printed or shared outside unifiedmeds.\n"
            "Licensed photography and product shots replace them before launch.\n\n"
            + "\n".join(f"{z}: {d}" for _, z, d in PHOTOS) + "\n")
    put("05-images-PLACEHOLDER/NOT-LICENSED-FOR-PRESS.txt", note)

    allfiles = {**files, **images}
    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(allfiles):
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, allfiles[name].read_bytes())

    print(f"kit: {len(files)} files in {KIT.relative_to(EXT)}")
    print(f"zip: {len(allfiles)} files, {ZIP.stat().st_size / 1e6:.2f} MB -> {ZIP.relative_to(EXT)}")
    if problems:
        print(f"{len(problems)} problems:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    for n in problems_note:
        print("  note:", n)
    print("0 problems")


if __name__ == "__main__":
    main()
