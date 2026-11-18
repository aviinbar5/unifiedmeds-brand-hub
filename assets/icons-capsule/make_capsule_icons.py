"""Capsule icons, two orientations: the website's working icon set (R-35, U-27).

Builds the capsule icon family: 12 subjects x 2 options (a, b)
x 2 orientations (horizontal, standing) x 2 variants (line, container) = 96 master SVGs,
plus two construction sheets, plus one export per placed size in sized/ (q124, Avi 18.11.2026):
the stroke floor of 1.5 (R-109) applies to the line AS RENDERED, so each placed size gets its own
file whose stroke renders at exactly 1.5:
    horizontal 48 x 24 (desktop) and 40 x 20 (mobile), standing 64 (desktop, = the master) and 48 (mobile).
Colours come from tokens/tokens.json (tools/capsule_svg.py token(), B-29). Run from anywhere:

    python3 -I assets/icons-capsule/make_capsule_icons.py

Construction
  * The capsule is the logo's capsule, from tools/capsule_svg.py (R-105): the long,
    narrower half is 55% of the length; the short half is taller. Never symmetric.
  * Horizontal: 64 x 32 drawing grid (2:1), capsule 60 long, lying flat like the logo,
    long half on the left. Placed at 48 x 24 or 40 x 20 (use the sized/ file for each).
  * Standing: 64 x 64 drawing grid (the grid of the 12 feature icons), the same
    capsule turned 90 degrees clockwise, 56 long, long half on top. Placed at 64 or 48.
  * Subject glyph: a 13 x 13 cell, centred in the long half (where "unified" sits in
    the seal). The short half stays empty.
  * Stroke 1.5 as rendered, round caps and joins, no fill on lines (as the feature icons).
    On the 64 grids that is 1.5 in the masters; a sized export scales the stroke and the
    container gap by grid / placed size (48 x 24: 2, 40 x 20: 2.4, standing 48: 2).
  * Line variant: capsule outline + glyph, Deep Teal (color.brand.deep-teal).
  * Container variant: both halves filled Wash Blue (color.surface.wash-blue) with a 1.5 gap
    at the divider (no outline) + glyph in Deep Teal. Never Yellow.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from capsule_svg import capsule_paths, geometry, f, token  # noqa: E402  (single source of the shape)

INK = token("color.brand.deep-teal")
TINT = token("color.surface.wash-blue")
KEY = token("color.brand.blue")   # Pastel Blue: construction sheet keylines only (never in an icon)
SW = 1.5                          # rendered stroke, px
CELL = 13.0

# Placed sizes (q124): orientation -> list of (file suffix, placed width, placed height)
SIZES = {
    "horizontal": [("48x24", 48, 24), ("40x20", 40, 20)],
    "standing": [("64", 64, 64), ("48", 48, 48)],
}

ORIENT = {
    # name: (canvas w, canvas h, capsule length, vertical)
    "horizontal": (64, 32, 60, False),
    "standing": (64, 64, 56, True),
}

# --------------------------------------------------------------------------- glyphs
# Each glyph is path data in a 13 x 13 cell (0,0 top-left). Absolute commands only.


def P(x, y):
    return f"{f(x)} {f(y)}"


def arc_pts(cx, cy, r, a0, a1):
    """Point at angle (degrees, screen space: 0 = right, 90 = down)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    return p0, p1


def arc(cx, cy, r, a0, a1, move=True):
    """Arc from a0 to a1 (clockwise in screen space when a1 > a0)."""
    (x0, y0), (x1, y1) = arc_pts(cx, cy, r, a0, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    head = f"M{P(x0, y0)}" if move else ""
    return f"{head}A{f(r)} {f(r)} 0 {large} {sweep} {P(x1, y1)}"


def circle(cx, cy, r):
    return f"M{P(cx - r, cy)}A{f(r)} {f(r)} 0 1 1 {P(cx + r, cy)}A{f(r)} {f(r)} 0 1 1 {P(cx - r, cy)}Z"


def dot(x, y):
    return f"M{P(x, y)}L{P(x + 0.01, y)}"


def rrect(x0, y0, x1, y1, r):
    return (f"M{P(x0 + r, y0)}H{f(x1 - r)}A{f(r)} {f(r)} 0 0 1 {P(x1, y0 + r)}V{f(y1 - r)}"
            f"A{f(r)} {f(r)} 0 0 1 {P(x1 - r, y1)}H{f(x0 + r)}A{f(r)} {f(r)} 0 0 1 {P(x0, y1 - r)}"
            f"V{f(y0 + r)}A{f(r)} {f(r)} 0 0 1 {P(x0 + r, y0)}Z")


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d
                 for a, b, c, d in zip(p0, p1, p2, p3))


def closed_eye():
    p = [(1, 5), (3.6, 8.6), (9.4, 8.6), (12, 5)]
    d = f"M{P(*p[0])}C{P(*p[1])} {P(*p[2])} {P(*p[3])}"
    for t, ang in ((0.22, 120), (0.5, 90), (0.78, 60)):
        x, y = bez(*p, t)
        d += f"M{P(x, y)}L{P(x + 2.1 * math.cos(math.radians(ang)), y + 2.1 * math.sin(math.radians(ang)))}"
    return d


def loop_arrow():
    cx, cy, r = 6.5, 6.5, 5
    a0, a1 = -70, 225
    d = arc(cx, cy, r, a0, a1)
    ex, ey = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    # tangent (direction of travel) at a1 for a clockwise arc
    tx, ty = -math.sin(math.radians(a1)), math.cos(math.radians(a1))
    arm = 2.6
    for turn in (150, -150):
        ca, sa = math.cos(math.radians(turn)), math.sin(math.radians(turn))
        ax, ay = tx * ca - ty * sa, tx * sa + ty * ca
        d += f"M{P(ex, ey)}L{P(ex + arm * ax, ey + arm * ay)}"
    return d


def fingerprint():
    c = (6.5, 7.5)
    d = f"M{P(5.25, 12)}V7.5" + arc(c[0], c[1], 1.25, 180, 360, move=False) + "V10.5"
    d += f"M{P(2.75, 11)}V7.5" + arc(c[0], c[1], 3.75, 180, 360, move=False) + "V12"
    d += arc(c[0], c[1], 6.25, 200, 340)
    return d


def sliders():
    d = ""
    for y, kx in ((2.5, 4), (6.5, 9), (10.5, 5.5)):
        r = 1.6
        d += f"M1 {f(y)}H{f(kx - r)}M{f(kx + r)} {f(y)}H12" + circle(kx, y, r)
    return d


GLYPHS = {
    # subject: {option: (path data, short description)}
    "sexual-health": {
        "a": ("M6.5 11.75L1.9 7.25C0.4 5.75 0.5 3.25 2.2 1.95C3.7 0.85 5.6 1.25 6.5 2.75"
              "C7.4 1.25 9.3 0.85 10.8 1.95C12.5 3.25 12.6 5.75 11.1 7.25Z", "Heart"),
        "b": (circle(4.6, 6.5, 3.6) + circle(8.4, 6.5, 3.6), "Two linked rings"),
    },
    "longevity": {
        "a": ("M6.5 12.5V6M6.5 8.5C3.6 8.5 1.5 6.6 1.5 3.6C4.4 3.6 6.5 5.5 6.5 8.5"
              "M6.5 6.2C6.5 3.4 8.4 1.5 11.5 1.5C11.5 4.3 9.6 6.2 6.5 6.2", "Sprout"),
        "b": ("M1 11H12" + f"M{P(3, 11)}A3.5 3.5 0 0 1 {P(10, 11)}"
              "M6.5 1.5V4M2.2 4.6L3.8 6.2M10.8 4.6L9.2 6.2", "Rising sun"),
    },
    "hair-loss": {
        "a": ("".join(f"M{P(x, 12)}C{P(x - 1.6, 8.6)} {P(x + 1.6, 4.9)} {P(x, 1)}" for x in (3, 6.5, 10)),
              "Three strands"),
        "b": ("M1 7H12M6.5 7C6.5 4.6 8.6 3.6 8.1 1M6.5 7V9" + circle(6.5, 10.6, 1.6),
              "Follicle under the skin line"),
    },
    "weight": {
        "a": ("M1.5 10A5 5 0 0 1 11.5 10M1 10H12M6.5 10L9 6.5M6.5 4.25V5.5", "Dial scale"),
        "b": ("M4.25 5.25V4A2.25 2.25 0 0 1 8.75 4V5.25" + circle(6.5, 8.5, 4), "Kettlebell"),
    },
    "online-assessment": {
        "a": ("".join(f"M1.3 {f(y)}L2.5 {f(y + 1.2)}L4.5 {f(y - 1)}M6.5 {f(y)}H11.8" for y in (2.5, 6.5))
              + "M1.5 10.5H4.25M6.5 10.5H11.8", "Checklist"),
        "b": (rrect(1, 1.5, 12, 9.5, 1.5) + "M4.5 12H8.5M6.5 9.5V12M4.2 5.6L5.8 7.2L8.8 4.1", "Screen with a check"),
    },
    "provider-reviewed": {
        "a": (circle(6.5, 6.5, 5.75) + "M4 6.8L5.8 8.6L9.2 4.9", "Badge with a check"),
        "b": (rrect(2, 2.25, 11, 12.5, 1.5) + "M5 1H8V3.5H5ZM4.3 7.7L5.9 9.3L8.8 6.2", "Clipboard with a check"),
    },
    "chat-with-a-provider": {
        "a": ("M3 1.5H10A2 2 0 0 1 12 3.5V7.5A2 2 0 0 1 10 9.5H6L3 12V9.5A2 2 0 0 1 1 7.5V3.5A2 2 0 0 1 3 1.5Z"
              "M4 4.5H9M4 6.75H7", "Speech bubble"),
        "b": ("M3.1 10.4A5.25 5.25 0 1 1 5.2 11.6L1.5 12.3Z" + dot(4, 6.25) + dot(6.5, 6.25) + dot(9, 6.25),
              "Bubble, typing"),
    },
    "prescription": {
        "a": ("M2.5 12V1.5H6.25A2.75 2.75 0 0 1 6.25 7H2.5M5 7L11 12.5M8 12.5L11.5 9", "Rx"),
        "b": ("M2 1H8.5L11 3.5V12H2ZM8.5 1V3.5H11M6.5 5.5V10M4.25 7.75H8.75", "Document with a plus"),
    },
    "discreet": {
        "a": (closed_eye(), "Closed eye"),
        "b": ("M1.5 4L6.5 1.5L11.5 4V9.5L6.5 12L1.5 9.5ZM1.5 4L6.5 6.5L11.5 4M6.5 6.5V12", "Plain parcel"),
    },
    "privacy": {
        "a": (rrect(2, 6, 11, 12, 1.5) + "M4 6V4.25A2.5 2.5 0 0 1 9 4.25V6" + dot(6.5, 9), "Lock"),
        "b": ("M6.5 1L11.5 2.8V6.3C11.5 9.2 9.4 11.4 6.5 12.4C3.6 11.4 1.5 9.2 1.5 6.3V2.8Z", "Shield"),
    },
    "personalized": {
        "a": (fingerprint(), "Fingerprint"),
        "b": (sliders(), "Sliders"),
    },
    "ongoing": {
        "a": (loop_arrow(), "Loop"),
        "b": (rrect(1.5, 2.5, 11.5, 12, 1.5) + "M1.5 5.5H11.5M4.5 1V3.5M8.5 1V3.5"
              + dot(4.5, 8.75) + dot(8.5, 8.75), "Calendar"),
    },
}

SUBJECTS = {
    "sexual-health": "Sexual health", "longevity": "Longevity", "hair-loss": "Hair loss",
    "weight": "Weight", "online-assessment": "Online assessment",
    "provider-reviewed": "Provider reviewed", "chat-with-a-provider": "Chat with a provider",
    "prescription": "Prescription", "discreet": "Discreet", "privacy": "Privacy",
    "personalized": "Personalized", "ongoing": "Ongoing",
}

# --------------------------------------------------------------------------- path tools
TOK = re.compile(r"[MLHVCAZ]|-?\d*\.?\d+(?:e-?\d+)?")
ARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "A": 7, "Z": 0}


def translate(d, ox, oy):
    """Move absolute path data by (ox, oy)."""
    toks, out, i, cmd = TOK.findall(d), [], 0, None
    while i < len(toks):
        if toks[i] in ARGS:
            cmd = toks[i]; i += 1
            if cmd == "Z":
                out.append("Z"); continue
        n = ARGS[cmd]
        v = [float(t) for t in toks[i:i + n]]; i += n
        if cmd in "MLC":
            v = [x + (ox if k % 2 == 0 else oy) for k, x in enumerate(v)]
        elif cmd == "H":
            v = [v[0] + ox]
        elif cmd == "V":
            v = [v[0] + oy]
        elif cmd == "A":
            v = v[:5] + [v[5] + ox, v[6] + oy]
        nums = [f(x) if k not in (2, 3, 4) or cmd != "A" else str(int(x)) for k, x in enumerate(v)]
        out.append(cmd + " ".join(nums))
    return "".join(out)


def halves_filled(x, y, length, vertical, gap):
    """Closed paths for the two halves with a gap at the divider (container variant)."""
    g = geometry(length)
    H, h, wl, L = g["H"], g["h"], g["wl"], length
    cy, rl, rr = H / 2, h / 2, H / 2
    a, b = wl - gap / 2, wl + gap / 2
    left = [("M", a, cy - rl), ("L", rl, cy - rl), ("A", rl, 0, rl, cy + rl), ("L", a, cy + rl), ("Z",)]
    right = [("M", b, 0), ("L", L - rr, 0), ("A", rr, 1, L - rr, H), ("L", b, H), ("Z",)]

    def pt(u, v):
        return (x + (H - v), y + u) if vertical else (x + u, y + v)

    def render(cmds):
        d = ""
        for c in cmds:
            if c[0] in "ML":
                px, py = pt(c[1], c[2]); d += f"{c[0]}{P(px, py)}"
            elif c[0] == "A":
                px, py = pt(c[3], c[4]); d += f"A{f(c[1])} {f(c[1])} 0 0 {c[2]} {P(px, py)}"
            else:
                d += "Z"
        return d
    return render(left), render(right)


def glyph_origin(orient):
    """Top-left of the 13 cell, centred in the long half (nudged 0.5 towards the divider)."""
    W, Hc, L, vertical = ORIENT[orient]
    g = geometry(L)
    if vertical:
        x0, y0 = (W - g["H"]) / 2, (Hc - L) / 2
        cx, cy = x0 + g["H"] / 2, y0 + g["wl"] / 2 + 0.5
    else:
        x0, y0 = (W - L) / 2, (Hc - g["H"]) / 2
        cx, cy = x0 + g["wl"] / 2 + 0.5, y0 + g["H"] / 2
    return cx - CELL / 2, cy - CELL / 2, x0, y0


def build(subject, option, orient, variant, placed=None):
    """One icon. placed = (w, h) in px for a sized export: the drawing grid stays, the file is
    w x h, and the stroke and gap are SW * grid / placed so they render at SW."""
    W, Hc, L, vertical = ORIENT[orient]
    gx, gy, x0, y0 = glyph_origin(orient)
    pw, ph = placed or (W, Hc)
    sw = SW * W / pw
    title = f"{SUBJECTS[subject]} · option {option.upper()} · {orient} · {variant}" + (f" · {pw} x {ph}" if placed else "")
    s = [f'<svg width="{pw}" height="{ph}" viewBox="0 0 {W} {Hc}" fill="none" xmlns="http://www.w3.org/2000/svg">',
         f"<title>{title}</title>"]
    if variant == "line":
        ld, rd, _ = capsule_paths(x0, y0, L, vertical)
        s.append(f'<path d="{ld}{rd}" stroke="{INK}" stroke-width="{f(sw)}" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        ld, rd = halves_filled(x0, y0, L, vertical, sw)
        s.append(f'<path d="{ld}{rd}" fill="{TINT}"/>')
    s.append(f'<path d="{translate(GLYPHS[subject][option][0], gx, gy)}" stroke="{INK}" stroke-width="{f(sw)}" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    s.append("</svg>")
    return "\n".join(s) + "\n"


def construction(orient):
    """Keyline sheet: capsule, divider, 13 cell, clear space."""
    W, Hc, L, vertical = ORIENT[orient]
    gx, gy, x0, y0 = glyph_origin(orient)
    ld, rd, (bw, bh) = capsule_paths(x0, y0, L, vertical)
    k = f'stroke="{KEY}" stroke-width="0.25"'
    s = [f'<svg width="{W * 4}" height="{Hc * 4}" viewBox="0 0 {W} {Hc}" fill="none" xmlns="http://www.w3.org/2000/svg">',
         f'<rect x="0.125" y="0.125" width="{W - 0.25}" height="{Hc - 0.25}" {k} stroke-dasharray="1 1"/>',
         f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(bw)}" height="{f(bh)}" {k}/>',
         f'<rect x="{f(gx)}" y="{f(gy)}" width="{f(CELL)}" height="{f(CELL)}" {k}/>',
         f'<path d="{ld}{rd}" stroke="{INK}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"/>',
         f'<path d="{translate(GLYPHS["privacy"]["a"][0], gx, gy)}" stroke="{INK}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"/>',
         "</svg>"]
    return "\n".join(s) + "\n"


def main():
    n = m = 0
    sized = os.path.join(HERE, "sized")
    os.makedirs(sized, exist_ok=True)
    for subject in SUBJECTS:
        for option in ("a", "b"):
            for orient in ORIENT:
                for variant in ("line", "container"):
                    name = f"{subject}-{option}-{orient}-{variant}.svg"
                    with open(os.path.join(HERE, name), "w") as fh:
                        fh.write(build(subject, option, orient, variant))
                    n += 1
                    for suffix, pw, ph in SIZES[orient]:
                        with open(os.path.join(sized, name.replace(".svg", f"-{suffix}.svg")), "w") as fh:
                            fh.write(build(subject, option, orient, variant, (pw, ph)))
                        m += 1
    for orient in ORIENT:
        with open(os.path.join(HERE, f"construction-{orient}.svg"), "w") as fh:
            fh.write(construction(orient))
    print(f"wrote {n} icons + 2 construction sheets to {HERE}, and {m} sized exports to {sized}")
    if "--print" in sys.argv:
        for o in ORIENT:
            print(o, [round(v, 2) for v in glyph_origin(o)], {k: round(v, 2) for k, v in geometry(ORIENT[o][2]).items()})


if __name__ == "__main__":
    main()
