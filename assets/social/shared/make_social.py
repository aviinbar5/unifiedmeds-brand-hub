"""unifiedmeds social kits (S1): shared avatars, Facebook, Instagram and Threads, X.

Run from the extended hub root:
    python3 -I assets/social/shared/make_social.py            # SVG + PNG for every asset, plus manifest.json
    python3 -I assets/social/shared/make_social.py --svg-only # SVG files and manifest only (no Chrome)

Every asset has Option A (calm, editorial: photo-led, serif headline) and
Option B (graphic: capsule kit and colour-led). Files are written to
assets/social/<channel>/<channel>-<asset>-a|b.svg and .png.
manifest.json (this folder) lists every asset, its sizes, safe zones and files;
tools-free page builder build_kit_pages.py reads it to write the src pages.
"""
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from social_art import Art, C, LEGAL, EXT, render

SOC = EXT / "assets" / "social"
OUT = {ch: SOC / ch for ch in ("shared", "facebook", "instagram", "x")}
for p in OUT.values():
    p.mkdir(parents=True, exist_ok=True)

M = 80          # outer margin on a 1080-wide canvas
MANIFEST = []
JOBS = []


def seal(a, x, y, h, dark):
    return a.logo("logo-seal-reversed.svg" if dark else "logo-seal.svg", x, y, h=h)


def seal_br(a, right, bottom, h, dark):
    """The seal anchored by its bottom-right corner."""
    w = h * 250 / 91
    return seal(a, right - w, bottom - h, h, dark)


def out(ch, name, art):
    svg = OUT[ch] / f"{name}.svg"
    art.save(svg)
    JOBS.append((svg, OUT[ch] / f"{name}.png", art.w, art.h))
    return f"assets/social/{ch}/{name}.png"


def cap_outline(a, x, y, L, vertical=False, colour=None, sw=20):
    """Website pattern (R-32): outline, Wash Blue, 70% opacity, cropped by an edge."""
    a.capsule(x, y, L, vertical, stroke=colour or C["wash-blue"], sw=sw, opacity=0.7)


def cap_split(a, x, y, L, vertical=False, sw=16, inner=None):
    """Split capsule: outline plus the long half filled (as in the seal)."""
    a.capsule(x, y, L, vertical, stroke=C["wash-blue"], sw=sw, inner=inner or C["blue"], gap=sw * 1.6)


# ---------------------------------------------------------------- avatars
def avatar(ch, name, size, scheme):
    a = Art(size, size, OUT[ch], C["cream"] if scheme == "cream" else C["navy"],
            f"unifiedmeds profile picture, {'Cream' if scheme == 'cream' else 'Navy'}")
    box = size * 0.66 * 120 / 96.8           # the mark is 96.8 wide in its 120 box: make it 66% of the square
    a.mark((size - box) / 2, (size - box) / 2, box, scheme)
    return out(ch, name, a)


def avatar_asset(ch, size, use, maxsize):
    return dict(
        key="avatar", title="Profile picture", use=use, size=[size, size], ratio="1:1", ftype="PNG", maxsize=maxsize,
        safe=[dict(x=0, y=0, w=size, h=size, label="Circle crop", kind="round")], ctx="avatar",
        a=dict(files=[avatar(ch, f"{ch}-avatar-a", size, "cream")], line="Navy mark on Cream. Light, calm, reads best on white feeds."),
        b=dict(files=[avatar(ch, f"{ch}-avatar-b", size, "navy")], line="The app icon colours (R-93): White mark on Navy. Strongest at 32px."))


# ---------------------------------------------------------------- shared helpers for layouts
def photo_band(ch, name, w, h, photo, split, lines, size, title, align="xMidYMid", x0=M, sealh=80):
    """Photo on top, Paper band below with a serif headline; the seal small in the band's corner."""
    a = Art(w, h, OUT[ch], C["paper"], title)
    py = round(h * split)
    a.photo(photo, 0, 0, w, py, align)
    a.text(x0, py + 110 + (size - 76) * 0.6, lines, size)
    sw, _ = a.logo("logo-seal.svg", 0, -1000, h=sealh)        # measure
    a.body.pop()
    seal(a, w - x0 - sw, h - x0 - sealh, sealh, False)
    return out(ch, name, a)


def photo_card(ch, name, w, h, photo, card, lines, size, title, align="xMidYMid"):
    """Full-bleed photo; a Paper card (radius 16 at display size) where no face is."""
    a = Art(w, h, OUT[ch], C["mist"], title)
    a.photo(photo, 0, 0, w, h, align)
    x, y, cw, ch_ = card
    a.rect(x, y, cw, ch_, C["paper"], rx=44)
    a.text(x + 60, y + 60 + size * 0.85, lines, size)
    seal_br(a, x + cw - 60, y + ch_ - 60, 72, False)
    return out(ch, name, a)


# ---------------------------------------------------------------- FACEBOOK
def facebook():
    ch = "facebook"
    A = []
    A.append(avatar_asset(ch, 400, "The page's face in every post, comment and message. Facebook masks it to a circle.", "PNG or JPG, under 1 MB"))

    # cover 1640 x 624
    W, H = 1640, 624
    a = Art(W, H, OUT[ch], C["paper"], "Facebook cover, Option A")
    a.photo("man-reading-window-wide-2048-pexels-8217708.jpg", 860, 0, W - 860, H)
    a.text(300, 250, ["Discretion is part", "of the treatment."], 56)
    a.logo("logo-horizontal.svg", 300, 360, h=40)
    fa = out(ch, "facebook-cover-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "Facebook cover, Option B")
    cap_split(b, -30, -150, 440, vertical=True)
    cap_outline(b, 1230, 380, 900)
    sw, sh = b.logo("logo-seal-reversed.svg", 0, -999, h=170); b.body.pop()
    b.logo("logo-seal-reversed.svg", (W - sw) / 2, (H - sh) / 2, h=170)
    fb = out(ch, "facebook-cover-b", b)
    A.append(dict(
        key="cover", title="Cover photo", use="The banner across the top of the Page. Desktop shows the full width; the app shows a 16:9 centre crop.",
        size=[W, H], ratio="2.63:1 (desktop) · 16:9 crop (mobile)", ftype="PNG (logo and type) or JPG (photo)", maxsize="Under 1 MB; Facebook recommends a small sRGB file",
        safe=[dict(x=265, y=0, w=1110, h=624, label="Visible on mobile (16:9)", kind="keep"),
              dict(x=40, y=470, w=380, h=154, label="Profile picture overlaps (desktop, approx.)", kind="ui")],
        ctx="cover",
        a=dict(files=[fa], line="Photo right, Paper left, one serif line and the Horizontal logo inside the mobile crop."),
        b=dict(files=[fb], line="Deep Teal, the reversed seal centred, two capsules cropped by the edges.")))

    # feed post square 1080
    W = H = 1080
    fa = photo_band(ch, "facebook-post-square-a", W, H, "man-kitchen-coffee-pexels-6269909.jpg", 0.6, ["Nothing is looked", "at alone."], 80, "Facebook square post, Option A")
    b = Art(W, H, OUT[ch], C["deep-teal"], "Facebook square post, Option B")
    seal(b, M, M, 80, True)
    b.text(M, 470, ["Discretion", "is part of the", "treatment."], 104, fill=C["paper"])
    cap_outline(b, 620, 820, 760)
    fb = out(ch, "facebook-post-square-b", b)
    A.append(dict(
        key="post-square", title="Feed post, square", use="Organic posts that must also fit other placements, and carousel cards.",
        size=[1080, 1080], ratio="1:1", ftype="PNG or JPG", maxsize="Under 1 MB (Meta accepts up to 30 MB)",
        safe=[dict(x=60, y=60, w=960, h=960, label="Keep type and logo inside", kind="keep")], ctx="feed",
        a=dict(files=[fa], line="Photo above, Paper band below, serif headline, the seal small."),
        b=dict(files=[fb], line="Deep Teal, a large serif line, one outline capsule cropped by the corner.")))

    # feed post 4:5
    W, H = 1080, 1350
    fa = photo_card(ch, "facebook-post-portrait-a", W, H, "man-mug-sunlight-pexels-6972779.jpg", (60, 960, 960, 330), ["Care that keeps", "showing up."], 76, "Facebook 4:5 post, Option A")
    b = Art(W, H, OUT[ch], C["mist"], "Facebook 4:5 post, Option B")
    seal(b, M, M, 80, False)
    b.text(M, 420, ["The whole", "chart, read", "by one", "person."], 96)
    cap_split(b, 770, 330, 900, vertical=True, inner=C["wash-blue"], sw=16)
    fb = out(ch, "facebook-post-portrait-b", b)
    A.append(dict(
        key="post-portrait", title="Feed post, 4:5", use="The default feed post: the most screen on a phone.",
        size=[1080, 1350], ratio="4:5", ftype="PNG or JPG", maxsize="Under 1.5 MB (Meta accepts up to 30 MB)",
        safe=[dict(x=60, y=60, w=960, h=1230, label="Keep type and logo inside", kind="keep")], ctx="feed",
        a=dict(files=[fa], line="Full-bleed photo; the Paper card sits where no face is."),
        b=dict(files=[fb], line="Mist ground, Teal Deep serif, one standing split capsule on the right.")))

    # link share 1200 x 630
    W, H = 1200, 630
    a = Art(W, H, OUT[ch], C["paper"], "Facebook link share, Option A")
    a.photo("man-home-office-pexels-8055837.jpg", 0, 0, 285, H)
    seal(a, 330, 100, 64, False)
    a.text(330, 330, ["Evidence,", "translated."], 76)
    fa = out(ch, "facebook-link-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "Facebook link share, Option B")
    cap_outline(b, 50, 330, 520, vertical=True)
    cap_split(b, 960, 60, 500)
    seal(b, 330, 100, 64, True)
    b.text(330, 320, ["Precision is a", "form of respect."], 72, fill=C["paper"])
    fb = out(ch, "facebook-link-b", b)
    A.append(dict(
        key="link", title="Link share image", use="The image a shared website link shows (og:image). The title and domain sit under it, set by the page.",
        size=[1200, 630], ratio="1.91:1", ftype="PNG or JPG", maxsize="Under 1 MB (og:image under 8 MB)",
        safe=[dict(x=285, y=0, w=630, h=630, label="Centre square: some placements crop to 1:1", kind="keep")], ctx="link",
        a=dict(files=[fa], line="Photo strip on the left, Paper, a short serif line in the centre square."),
        b=dict(files=[fb], line="Deep Teal; both capsules live outside the centre square.")))

    # story 1080 x 1920
    W, H = 1080, 1920
    a = Art(W, H, OUT[ch], C["paper"], "Facebook story, Option A")
    seal(a, M, 320, 80, False)
    a.photo("man-kitchen-coffee-pexels-6269909.jpg", M, 440, W - 2 * M, 780, rx=44)
    a.text(M, 1340, ["Nothing is looked", "at alone."], 88)
    fa = out(ch, "facebook-story-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "Facebook story, Option B")
    seal(b, M, 320, 80, True)
    b.text(M, 640, ["Care", "that keeps", "showing up."], 124, fill=C["paper"])
    cap_split(b, 690, 1020, 1100, vertical=True)
    fb = out(ch, "facebook-story-b", b)
    story_safe = [dict(x=0, y=0, w=1080, h=270, label="Profile and progress bar · 14%", kind="ui"),
                  dict(x=0, y=1650, w=1080, h=270, label="Reply bar · 14%", kind="ui"),
                  dict(x=80, y=1490, w=520, h=120, label="Link sticker", kind="sticker")]
    A.append(dict(
        key="story", title="Story", use="Full-screen, 24 hours. Sound often on; Facebook adds the reply bar and the profile row.",
        size=[1080, 1920], ratio="9:16", ftype="PNG or JPG", maxsize="Under 1 MB (Meta accepts up to 30 MB)",
        safe=story_safe, ctx="story",
        a=dict(files=[fa], line="Paper, the photo in a 16px-radius frame, the serif line below it."),
        b=dict(files=[fb], line="Deep Teal, a large serif line, one standing split capsule cropped by the bottom.")))

    # event cover 1920 x 1005
    W, H = 1920, 1005
    a = Art(W, H, OUT[ch], C["paper"], "Facebook event cover, Option A")
    a.photo("friends-talking-outdoors-pexels-13335592.jpg", 0, 0, 900, H)
    a.text(1000, 300, ["[Date · time · online]"], 34, "sans", C["slate"], 600)
    a.text(1000, 440, ["Questions, answered", "by a provider."], 84)
    seal(a, 1000, 760, 88, False)
    fa = out(ch, "facebook-event-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "Facebook event cover, Option B")
    cap_outline(b, 1260, 540, 1100)
    cap_split(b, 1520, -230, 620, vertical=True)
    b.text(160, 330, ["[Date · time · online]"], 34, "sans", C["wash-blue"], 600)
    b.text(160, 470, ["Questions, answered", "by a provider."], 100, fill=C["paper"])
    seal(b, 160, 760, 88, True)
    fb = out(ch, "facebook-event-b", b)
    A.append(dict(
        key="event", title="Event cover", use="The header of a Facebook event (a live Q&A, a launch). Details in brackets until the event is set.",
        size=[1920, 1005], ratio="1.91:1", ftype="PNG or JPG", maxsize="Under 1.5 MB",
        safe=[dict(x=96, y=50, w=1728, h=905, label="Keep type inside (edges crop on some screens)", kind="keep")], ctx="event",
        a=dict(files=[fa], line="Photo left, Paper right: date line, serif title, seal."),
        b=dict(files=[fb], line="Deep Teal, serif title in Paper, two capsules on the right.")))

    # ad-ready post 1080 x 1350
    W, H = 1080, 1350
    k = W / 390
    a = Art(W, H, OUT[ch], C["deep-teal"], "Facebook ad-ready post, Option A")
    a.photo("man-reading-window-wide-2048-pexels-8217708.jpg", 0, 0, W, 760)
    a.text(M, 880, ["A private next step,", "on your schedule."], 72, fill=C["paper"])
    a.button(M, 1010, "Get started", k)
    a.text(M, 1222, [LEGAL], 30, "sans", C["wash-blue"])
    seal_br(a, W - M, H - M, 72, True)
    fa = out(ch, "facebook-ad-a", a)
    b = Art(W, H, OUT[ch], C["paper"], "Facebook ad-ready post, Option B")
    seal(b, M, M, 80, False)
    b.text(M, 400, ["Discretion", "is part of the", "treatment."], 100)
    b.text(M, 720, ["An online assessment, reviewed", "by a licensed provider."], 34, "sans", C["deep-teal"], lh=1.4)
    b.button(M, 830, "Get started", k)
    b.text(M, 1040, [LEGAL], 30, "sans", C["slate"])
    cap_outline(b, 640, 1100, 700)
    fb = out(ch, "facebook-ad-b", b)
    A.append(dict(
        key="ad", title="Ad-ready post", use="A boosted post or Meta ad. Follows the Ads page: headline of nine words or fewer, one Yellow CTA, the legal line inside the art.",
        size=[1080, 1350], ratio="4:5 (also export 1:1 and 9:16 from the Ads page templates)", ftype="PNG or JPG", maxsize="Meta: up to 30 MB",
        safe=[dict(x=60, y=60, w=960, h=1230, label="Nothing critical at the edges", kind="keep")], ctx="feed",
        a=dict(files=[fa], line="Photo top 56%, Deep Teal panel: headline, Yellow button, legal line."),
        b=dict(files=[fb], line="Paper, type only, one outline capsule cropped by the corner.")))
    for x in A:
        x["channel"] = ch
    MANIFEST.extend(A)


# ---------------------------------------------------------------- INSTAGRAM AND THREADS
def instagram():
    ch = "instagram"
    A = []
    A.append(avatar_asset(ch, 320, "Instagram and Threads share it. Shown as a circle in the feed, stories and comments.", "PNG or JPG, under 1 MB"))

    grid34 = lambda w, h: dict(x=round((w - h * 3 / 4) / 2) if w > h * 3 / 4 else 0, y=0 if w <= h * 3 / 4 else 0,
                               w=round(min(w, h * 3 / 4)), h=h, label="Profile grid crop (3:4)", kind="keep")

    # feed 4:5
    W, H = 1080, 1350
    fa = photo_card(ch, "instagram-post-portrait-a", W, H, "man-home-office-pexels-8055837.jpg", (60, 990, 960, 300), ["Precision is a", "form of respect."], 80, "Instagram 4:5 post, Option A", align="xMidYMax")
    b = Art(W, H, OUT[ch], C["deep-teal"], "Instagram 4:5 post, Option B")
    b.text(M, 420, ["Evidence,", "translated."], 128, fill=C["paper"])
    cap_split(b, 430, 930, 820)
    seal(b, M, H - M - 80, 80, True)
    fb = out(ch, "instagram-post-portrait-b", b)
    A.append(dict(
        key="post-portrait", title="Feed post, 4:5", use="The default feed post. The profile grid shows a 3:4 centre crop.",
        size=[W, H], ratio="4:5", ftype="PNG or JPG", maxsize="Under 1.5 MB (Meta accepts up to 30 MB)",
        safe=[dict(x=34, y=0, w=1012, h=1350, label="Profile grid crop (3:4)", kind="keep")], ctx="feed",
        a=dict(files=[fa], line="Full-bleed photo, Paper card below the face, serif line, seal."),
        b=dict(files=[fb], line="Deep Teal, a large serif line, one split capsule cropped by the corner.")))

    # feed 1:1
    W = H = 1080
    fa = photo_band(ch, "instagram-post-square-a", W, H, "friends-talking-outdoors-pexels-13335592.jpg", 0.65, ["Care that keeps", "showing up."], 76, "Instagram square post, Option A", x0=160)
    b = Art(W, H, OUT[ch], C["mist"], "Instagram square post, Option B")
    seal(b, 160, M, 80, False)
    b.text(160, 420, ["Nothing is", "looked at", "alone."], 100)
    cap_outline(b, 820, 420, 760, vertical=True)
    fb = out(ch, "instagram-post-square-b", b)
    A.append(dict(
        key="post-square", title="Feed post, 1:1", use="Square posts. The profile grid crops them to 3:4, so the sides fall away there.",
        size=[W, H], ratio="1:1", ftype="PNG or JPG", maxsize="Under 1 MB (Meta accepts up to 30 MB)",
        safe=[dict(x=135, y=0, w=810, h=1080, label="Profile grid crop (3:4)", kind="keep")], ctx="feed",
        a=dict(files=[fa], line="Photo above, Paper band, type inside the 3:4 grid crop."),
        b=dict(files=[fb], line="Mist ground, Teal Deep serif, one standing outline capsule.")))

    # carousel: cover + 2 slides, both options
    W, H = 1080, 1350
    fa = []
    a = Art(W, H, OUT[ch], C["paper"], "Instagram carousel, Option A, cover")
    a.photo("man-mug-sunlight-pexels-6972779.jpg", 0, 0, W, 820, "xMidYMin")
    a.text(M, 960, ["How the assessment", "works."], 84)
    seal_br(a, W - M, H - M, 72, False)
    fa.append(out(ch, "instagram-carousel-a-1", a))
    for i, (num, head, body, legal) in enumerate([
            ("01", ["Answer a few", "questions online."], ["On your schedule, from your", "own phone or computer."], False),
            ("02", ["A licensed provider", "reviews them."], ["Your provider explains", "what comes next."], True)], start=2):
        a = Art(W, H, OUT[ch], C["paper"], f"Instagram carousel, Option A, slide {i}")
        a.text(M, 420, [num], 40, "sans", C["slate"], 600)
        a.text(M, 570, head, 100)
        a.text(M, 820, body, 40, "sans", C["deep-teal"], lh=1.45)
        if legal:
            a.text(M, 1060, [LEGAL], 32, "sans", C["slate"])
        seal_br(a, W - M, H - M, 72, False)
        fa.append(out(ch, f"instagram-carousel-a-{i}", a))
    fb = []
    for i, (num, head, legal) in enumerate([
            (None, ["How the", "assessment", "works."], False),
            ("01", ["Answer a few", "questions", "online."], False),
            ("02", ["A licensed", "provider", "reviews them."], True)], start=1):
        b = Art(W, H, OUT[ch], C["deep-teal"], f"Instagram carousel, Option B, card {i}")
        cap_outline(b, 330 - (i - 1) * W, 860, 2600)        # one capsule runs across the three cards
        if num:
            b.text(M, 260, [num], 40, "sans", C["wash-blue"], 600)
        else:
            seal(b, M, M + 120, 80, True)
        b.text(M, 420, head, 110, fill=C["paper"])
        if legal:
            b.text(M, 760, [LEGAL], 32, "sans", C["wash-blue"])
        fb.append(out(ch, f"instagram-carousel-b-{i}", b))
    A.append(dict(
        key="carousel", title="Carousel", use="Two to ten cards, one idea per card. The cover is what the grid and the feed show first.",
        size=[W, H], ratio="4:5, every card the same", ftype="PNG or JPG", maxsize="Under 1 MB per card",
        safe=[dict(x=34, y=0, w=1012, h=1350, label="Grid crop of the cover (3:4)", kind="keep")], ctx="carousel",
        a=dict(files=fa, line="Cover photo, then Paper cards: number, serif step, one plain line; the legal line on the last card."),
        b=dict(files=fb, line="Deep Teal; one outline capsule runs across all three cards (swipe to follow it).")))

    # story
    W, H = 1080, 1920
    a = Art(W, H, OUT[ch], C["paper"], "Instagram story, Option A")
    seal(a, M, 320, 80, False)
    a.photo("man-reading-window-wide-2048-pexels-8217708.jpg", M, 440, W - 2 * M, 780, rx=44)
    a.text(M, 1340, ["Care that keeps", "showing up."], 92)
    fa = out(ch, "instagram-story-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "Instagram story, Option B")
    seal(b, M, 320, 80, True)
    b.text(M, 640, ["Nothing is", "looked at", "alone."], 124, fill=C["paper"])
    cap_split(b, 420, 1100, 900)
    fb = out(ch, "instagram-story-b", b)
    A.append(dict(
        key="story", title="Story", use="Full-screen, 24 hours. Instagram lays the profile row on top and the reply bar at the bottom.",
        size=[W, H], ratio="9:16", ftype="PNG or JPG", maxsize="Under 1 MB (Meta accepts up to 30 MB)",
        safe=[dict(x=0, y=0, w=1080, h=250, label="Profile and progress bar · 14%", kind="ui"),
              dict(x=0, y=1670, w=1080, h=250, label="Reply bar · 14%", kind="ui"),
              dict(x=80, y=1500, w=520, h=120, label="Link sticker", kind="sticker")], ctx="story",
        a=dict(files=[fa], line="Paper, a framed photo, the serif line; room for the link sticker."),
        b=dict(files=[fb], line="Deep Teal, a large serif line, one split capsule low on the right.")))

    # reel cover
    a = Art(W, H, OUT[ch], C["mist"], "Instagram reel cover, Option A")
    a.photo("father-son-kitchen-hug-pexels-4259702.jpg", 0, 0, W, H)
    a.rect(0, 1180, W, 400, C["paper"])
    a.text(M, 1300, ["How a provider", "reads your answers."], 84)
    seal_br(a, W - M, 1546, 72, False)
    fa = out(ch, "instagram-reel-cover-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "Instagram reel cover, Option B")
    seal(b, M, 320, 80, True)
    b.text(M, 640, ["Questions", "we get", "often."], 132, fill=C["paper"])
    cap_split(b, 640, 1040, 1000, vertical=True)
    fb = out(ch, "instagram-reel-cover-b", b)
    A.append(dict(
        key="reel-cover", title="Reel cover", use="The still that stands for a reel in the Reels tab (9:16) and in the profile grid (3:4 centre).",
        size=[W, H], ratio="9:16, grid crop 3:4", ftype="PNG or JPG", maxsize="Under 1.5 MB",
        safe=[dict(x=0, y=240, w=1080, h=1440, label="Profile grid crop (3:4)", kind="keep"),
              dict(x=0, y=285, w=1080, h=1350, label="4:5 crop (feed preview)", kind="keep2")], ctx="reel",
        a=dict(files=[fa], line="Photo full-height, a Paper band with the title inside the grid crop."),
        b=dict(files=[fb], line="Deep Teal, the title large, one standing split capsule.")))

    # highlight covers
    HL = [("start", "Start", "icon-online-assessment.svg"), ("how", "How it works", "icon-provider-reviewed.svg"),
          ("privacy", "Privacy", "icon-privacy.svg"), ("questions", "Questions", "icon-chat-with-a-provider.svg"),
          ("delivery", "Delivery", "icon-discreet.svg")]
    fa, fb = [], []
    for slug, label, icon in HL:
        a = Art(W, H, OUT[ch], C["mist"], f"Highlight cover {label}, Option A")
        a.icon(icon, W / 2, H / 2, 700, C["deep-teal"], 2)
        fa.append(out(ch, f"instagram-highlight-{slug}-a", a))
        b = Art(W, H, OUT[ch], C["deep-teal"], f"Highlight cover {label}, Option B")
        b.icon(icon, W / 2, H / 2, 700, C["paper"], 2)
        fb.append(out(ch, f"instagram-highlight-{slug}-b", b))
    A.append(dict(
        key="highlights", title="Highlight covers", use="Five saved story groups under the bio: Start, How it works, Privacy, Questions, Delivery. The label is typed in the app, never drawn on the cover.",
        size=[W, H], ratio="9:16 file, circle crop from the centre", ftype="PNG", maxsize="Under 500 KB",
        safe=[dict(x=0, y=420, w=1080, h=1080, label="Circle crop", kind="round")], ctx="highlights",
        labels=[h[1] for h in HL],
        a=dict(files=fa, line="Deep Teal icons on Mist: quiet, reads as a set."),
        b=dict(files=fb, line="Paper icons on Deep Teal: matches the dark posts.")))

    # threads image
    W, H = 1080, 1350
    a = Art(W, H, OUT[ch], C["paper"], "Threads post image, Option A")
    seal(a, M, M, 80, False)
    a.text(M, 560, ["The whole chart,", "read by one", "person."], 104)
    fa = out(ch, "threads-post-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "Threads post image, Option B")
    b.text(M, 420, ["Precision", "is a form", "of respect."], 120, fill=C["paper"])
    cap_outline(b, 400, 1000, 900)
    seal(b, M, H - M - 80, 80, True)
    fb = out(ch, "threads-post-b", b)
    A.append(dict(
        key="threads", title="Threads post image", use="Threads is text first: an image only when one line deserves a card. Same profile picture as Instagram.",
        size=[W, H], ratio="4:5", ftype="PNG or JPG", maxsize="Under 1 MB [Threads limit: check]",
        safe=[dict(x=60, y=60, w=960, h=1230, label="Keep type inside", kind="keep")], ctx="threads",
        a=dict(files=[fa], line="A quote card: Paper, the seal, one serif line."),
        b=dict(files=[fb], line="Deep Teal quote card with one outline capsule.")))
    for x in A:
        x["channel"] = ch
    MANIFEST.extend(A)


def instagram_grids():
    """Grid look: 9 tiles at the 3:4 grid crop, two rhythms. Run after the tiles are rendered."""
    ch = "instagram"
    cw, gap = 356, 6
    chh = round(cw * 4 / 3)
    W, H = cw * 3 + gap * 2, chh * 3 + gap * 2
    fbp = "../facebook/facebook-post-portrait-a.png"
    sets = {
        "a": ["instagram-post-portrait-a.png", "threads-post-b.png", "instagram-carousel-a-1.png",
              "instagram-post-square-b.png", "instagram-reel-cover-a.png", "instagram-carousel-b-1.png",
              "instagram-post-square-a.png", "threads-post-a.png", "../x/x-post-square-a.png"],
        "b": ["instagram-carousel-b-1.png", "instagram-reel-cover-b.png", "instagram-post-portrait-b.png",
              "instagram-post-portrait-a.png", "instagram-reel-cover-a.png", "instagram-post-square-a.png",
              "threads-post-a.png", "instagram-carousel-a-2.png", "instagram-post-square-b.png"],
    }
    files = {}
    for opt, tiles in sets.items():
        a = Art(W, H, OUT[ch], C["paper"], f"Instagram grid, Option {opt.upper()}")
        for i, t in enumerate(tiles):
            x, y = (i % 3) * (cw + gap), (i // 3) * (chh + gap)
            cid = a.uid("g")
            a.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{cw}" height="{chh}"/></clipPath>')
            a.body.append(f'<image href="{t}" x="{x}" y="{y}" width="{cw}" height="{chh}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>')
        files[opt] = out(ch, f"instagram-grid-{opt}", a)
    entry = dict(
        channel=ch, key="grid", title="Grid look", use="How nine posts read together on the profile (3:4 tiles since 2025). Plan the grid three posts at a time.",
        size=[W, H], ratio="3 × 3 tiles at 3:4", ftype="PNG (planning view, not posted)", maxsize="n/a",
        safe=[], ctx="grid",
        a=dict(files=[files["a"]], line="Checkerboard: photo, type, photo. Calm and even."),
        b=dict(files=[files["b"]], line="Rows: a dark graphic row, a photo row, a light type row."))
    # put the grid right after the avatar
    i = next(n for n, m in enumerate(MANIFEST) if m["channel"] == ch and m["key"] == "avatar")
    MANIFEST.insert(i + 1, entry)


# ---------------------------------------------------------------- X
def x_channel():
    ch = "x"
    A = []
    A.append(avatar_asset(ch, 400, "Shown as a circle on the profile, every post and every reply.", "PNG or JPG, under 2 MB"))

    W, H = 1500, 500
    a = Art(W, H, OUT[ch], C["paper"], "X header, Option A")
    a.photo("man-reading-window-wide-2048-pexels-8217708.jpg", 900, 0, W - 900, H)
    a.text(400, 180, ["Discretion is part", "of the treatment."], 56)
    a.logo("logo-horizontal.svg", 400, 290, h=40)
    fa = out(ch, "x-header-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "X header, Option B")
    cap_split(b, 120, -200, 460, vertical=True)
    cap_outline(b, 1150, 300, 760)
    sw, sh = b.logo("logo-seal-reversed.svg", 0, -999, h=150); b.body.pop()
    b.logo("logo-seal-reversed.svg", 900 - sw / 2, 250 - sh / 2, h=150)
    fb = out(ch, "x-header-b", b)
    A.append(dict(
        key="header", title="Header", use="The banner above the profile. The profile picture overlaps its lower left; phones trim the top and bottom.",
        size=[W, H], ratio="3:1", ftype="PNG or JPG", maxsize="Under 2 MB",
        safe=[dict(x=0, y=60, w=1500, h=380, label="Visible on phones (approx.)", kind="keep"),
              dict(x=40, y=330, w=330, h=170, label="Profile picture overlaps", kind="ui")], ctx="xheader",
        a=dict(files=[fa], line="Paper left with the serif line and logo, photo right; the lower left stays clear."),
        b=dict(files=[fb], line="Deep Teal, the reversed seal centred right of the avatar, two capsules.")))

    W, H = 1600, 900
    a = Art(W, H, OUT[ch], C["paper"], "X post 16:9, Option A")
    a.photo("man-kitchen-coffee-pexels-6269909.jpg", 0, 0, 900, H)
    a.text(980, 360, ["Nothing is", "looked at", "alone."], 100)
    seal(a, 980, 720, 88, False)
    fa = out(ch, "x-post-wide-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "X post 16:9, Option B")
    b.text(120, 380, ["Evidence,", "translated."], 132, fill=C["paper"])
    seal(b, 120, 720, 88, True)
    cap_split(b, 900, 380, 900)
    fb = out(ch, "x-post-wide-b", b)
    A.append(dict(
        key="post-wide", title="Post image, 16:9", use="A single image in a post. Shown whole in the timeline on phone and desktop.",
        size=[W, H], ratio="16:9", ftype="PNG or JPG", maxsize="Under 5 MB",
        safe=[dict(x=80, y=60, w=1440, h=780, label="Keep type inside", kind="keep")], ctx="xpost",
        a=dict(files=[fa], line="Photo left, Paper right, a three-line serif headline and the seal."),
        b=dict(files=[fb], line="Deep Teal, the serif line large, one split capsule cropped by the edge.")))

    W = H = 1080
    fa = photo_band(ch, "x-post-square-a", W, H, "couple-breakfast-pexels-6248662.jpg", 0.65, ["Discretion is part", "of the treatment."], 76, "X square post, Option A", align="xMidYMin")
    b = Art(W, H, OUT[ch], C["mist"], "X square post, Option B")
    seal(b, M, M, 80, False)
    b.text(M, 400, ["Care that", "keeps", "showing up."], 104)
    cap_outline(b, 770, 380, 700, vertical=True)
    fb = out(ch, "x-post-square-b", b)
    A.append(dict(
        key="post-square", title="Post image, 1:1", use="Square image posts and the first image of a set.",
        size=[W, H], ratio="1:1", ftype="PNG or JPG", maxsize="Under 5 MB",
        safe=[dict(x=60, y=60, w=960, h=960, label="Keep type inside", kind="keep")], ctx="xpost",
        a=dict(files=[fa], line="Photo above (partners may appear in Sexual health, R-37), Paper band below."),
        b=dict(files=[fb], line="Mist ground, Teal Deep serif, one standing outline capsule.")))

    W, H = 1200, 628
    a = Art(W, H, OUT[ch], C["paper"], "X card image, Option A")
    a.photo("friends-talking-outdoors-pexels-13335592.jpg", 660, 0, W - 660, H)
    seal(a, M, 90, 64, False)
    a.text(M, 300, ["Care that keeps", "showing up."], 72)
    fa = out(ch, "x-card-a", a)
    b = Art(W, H, OUT[ch], C["deep-teal"], "X card image, Option B")
    cap_split(b, 900, 140, 560, vertical=True)
    cap_outline(b, 990, -110, 520)
    seal(b, M, 90, 64, True)
    b.text(M, 300, ["Precision is a", "form of respect."], 80, fill=C["paper"])
    fb = out(ch, "x-card-b", b)
    A.append(dict(
        key="card", title="Link card image", use="The large image card a shared website link shows (twitter:image). X lays the domain over the lower left.",
        size=[W, H], ratio="1.91:1", ftype="PNG or JPG", maxsize="Under 5 MB",
        safe=[dict(x=24, y=548, w=420, h=60, label="Domain label (X adds it)", kind="ui")], ctx="xcard",
        a=dict(files=[fa], line="Paper left with the seal and a serif line, photo right."),
        b=dict(files=[fb], line="Deep Teal, two capsules on the right, the lower left kept clear.")))
    for x in A:
        x["channel"] = ch
    MANIFEST.extend(A)


def shared():
    """Shared masters: the avatar pair at 800 and the asymmetric capsule outlines used as CSS backgrounds."""
    avatar("shared", "avatar-a", 800, "cream")
    avatar("shared", "avatar-b", 800, "navy")
    from social_art import capsule_paths
    for name, colour in (("capsule-outline-wash", C["wash-blue"]), ("capsule-outline-field", "#55747F")):
        L, sw = 600, 20
        ld, rd, (bw, bh) = capsule_paths(sw / 2, sw / 2, L)
        (OUT["shared"] / f"{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{bw + sw:.0f}" height="{bh + sw:.0f}" viewBox="0 0 {bw + sw:.2f} {bh + sw:.2f}" fill="none">'
            f'<path d="{ld}" stroke="{colour}" stroke-width="{sw}"/><path d="{rd}" stroke="{colour}" stroke-width="{sw}"/></svg>\n')


def jpg_if_heavy(png, limit=1_000_000):
    """Photo-led PNGs over 1 MB also get a JPG at quality 80 (sips). Returns the JPG path or None."""
    src, jpg = EXT / png, EXT / png.replace(".png", ".jpg")
    if not src.exists() or src.stat().st_size <= limit:
        return None
    if "--svg-only" not in sys.argv or not jpg.exists():
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80", str(src), "--out", str(jpg)],
                       capture_output=True, check=True)
    return png.replace(".png", ".jpg")


def main():
    shared()
    facebook()
    instagram()
    x_channel()
    if "--svg-only" not in sys.argv:
        render(JOBS)
        JOBS.clear()
    instagram_grids()
    if "--svg-only" not in sys.argv:
        render(JOBS)
    for m in MANIFEST:
        for o in ("a", "b"):
            m[o]["svgs"] = [p.replace(".png", ".svg") for p in m[o]["files"]]
            m[o]["jpgs"] = [jpg_if_heavy(p) for p in m[o]["files"]]
    (OUT["shared"] / "manifest.json").write_text(json.dumps(MANIFEST, indent=1))
    print(f"{len(MANIFEST)} assets, manifest written")


if __name__ == "__main__":
    main()
