"""The unifiedmeds capsule, drawn with the logo's own proportions (R-105) and the D1 stroke.

The logo capsule is NOT symmetric:
  * the left half (the filled half in the seal) is LONGER: 55% of the full length;
  * the right half (the open half) is TALLER: the left half is 93.3% of its height.
Measured from assets/brand/logo-seal.svg (outer stroke edges):
  full length 247.87 · left length 136.43 · right height 88.82 · left height 82.85.

Standing (vertical) capsules are the horizontal capsule turned 90 degrees
clockwise: the long, narrower half (the filled half of the seal) is on top,
the short, wider half is below. Same proportions, nothing redrawn.

Usage
  python3 -I tools/capsule_svg.py            # rewrites assets/shapes/capsule-*.svg
  python3 -I tools/capsule_svg.py --print    # prints the geometry for a 280 x 100 box
  python3 -I tools/capsule_svg.py --css      # prints the CSS mask variables used in hub.css

Copy `capsule_paths()` into any other generator that draws a capsule. Never
draw a capsule as one rounded rectangle (rx = height / 2): that is symmetric.
"""
import os
import sys

LEFT_SHARE = 136.43 / 247.87      # left half, share of the full length
HEIGHT_RATIO = 88.82 / 247.87     # right-half height, share of the full length
LEFT_HEIGHT = 82.85 / 88.82       # left-half height, share of the right-half height


def f(n):
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def geometry(length):
    """Return the two halves of a horizontal capsule of the given full length,
    sitting in a box (0, 0, length, H) where H is the right-half height."""
    H = length * HEIGHT_RATIO
    h = H * LEFT_HEIGHT
    wl = length * LEFT_SHARE
    return {"length": length, "H": H, "h": h, "wl": wl, "wr": length - wl,
            "rl": h / 2, "rr": H / 2, "cy": H / 2}


def capsule_paths(x, y, length, vertical=False, inset=0.0):
    """SVG path data for the left half and the right half.

    x, y      top-left corner of the bounding box
    length    full length (width when horizontal, height when vertical)
    vertical  True = standing: left (long) half on top, right (short, wide) half below
    inset     shrink both halves by this much on every side (for an inner fill)
    Returns (left_d, right_d, (box_w, box_h)).
    """
    g = geometry(length)
    H, h, wl, L = g["H"], g["h"], g["wl"], length
    cy = H / 2
    # left half (horizontal frame): x 0..wl, y cy-h/2..cy+h/2, round on the left
    i = inset
    lt, lb = cy - h / 2 + i, cy + h / 2 - i
    lr = (lb - lt) / 2
    lx0, lx1 = i, wl - i
    # no closing edge: the divider belongs to the right half, like the seal
    left = [("M", lx1, lt), ("H", lx0 + lr), ("A", lr, lx0 + lr, lb), ("H", lx1)]
    # right half: x wl..L, y 0..H, round on the right
    rt, rb = i, H - i
    rr = (rb - rt) / 2
    rx0, rx1 = wl + i, L - i
    right = [("M", rx0, rt), ("H", rx1 - rr), ("A", rr, rx1 - rr, rb), ("H", rx0), ("Z",)]

    def to_d(cmds, sweep):
        out = []
        for c in cmds:
            if c[0] == "M":
                px, py = c[1], c[2]
                out.append(("M", px, py))
            elif c[0] == "H":
                out.append(("H", c[1]))
            elif c[0] == "A":
                out.append(("A", c[1], c[2], c[3]))
            else:
                out.append(("Z",))
        return out

    def render(cmds, sweep):
        # horizontal: (u, v) -> (x + u, y + v)
        # vertical:   turn 90 deg clockwise inside a box of H x L:
        #             (u, v) -> (x + (H - v), y + u)
        def pt(u, v):
            return (x + (H - v), y + u) if vertical else (x + u, y + v)
        d, cur = [], None
        for c in cmds:
            if c[0] == "M":
                cur = (c[1], c[2]); px, py = pt(*cur); d.append(f"M{f(px)} {f(py)}")
            elif c[0] == "H":
                cur = (c[1], cur[1]); px, py = pt(*cur); d.append(f"L{f(px)} {f(py)}")
            elif c[0] == "A":
                r, ex_u, ey_v = c[1], c[2], c[3]
                cur = (ex_u, ey_v); px, py = pt(*cur)
                d.append(f"A{f(r)} {f(r)} 0 0 {sweep} {f(px)} {f(py)}")
            else:
                d.append("Z")
        return "".join(d)

    # left half arcs go top -> bottom around the left end: counter-clockwise in screen
    # space = sweep 0; right half arcs go top -> bottom around the right end = sweep 1.
    # A rotation keeps orientation, so the sweep flags stay the same.
    box = (H, L) if vertical else (L, H)
    return render(left, 0), render(right, 1), box


def solid_paths(x, y, length, vertical=False, gap=None):
    """A FILLED capsule (Avi 17.11.2026): both halves filled, with a thin gap at the divider,
    one stroke wide, like the seal. The right (short, taller) half is whole, as the divider
    belongs to it; the left (long) half stops `gap` before the joint.
    gap defaults to stroke_for(length), the D1 stroke of an outline capsule of this size.
    Never fill the continuous silhouette: a solid capsule always shows the gap.
    Same frame as capsule_paths(). Returns (left_d, right_d, (box_w, box_h)), both closed."""
    g = geometry(length)
    H, h, wl, L = g["H"], g["h"], g["wl"], length
    gap = stroke_for(length) if gap is None else gap
    cy, lr, rr = H / 2, h / 2, H / 2
    lt, lb, le = cy - h / 2, cy + h / 2, wl - gap

    def pt(u, v):
        return (x + (H - v), y + u) if vertical else (x + u, y + v)

    def P(u, v):
        a, b = pt(u, v)
        return f"{f(a)} {f(b)}"
    left = f"M{P(le, lt)}L{P(lr, lt)}A{f(lr)} {f(lr)} 0 0 0 {P(lr, lb)}L{P(le, lb)}Z"
    right = f"M{P(wl, 0)}L{P(L - rr, 0)}A{f(rr)} {f(rr)} 0 0 1 {P(L - rr, H)}L{P(wl, H)}Z"
    return left, right, ((H, L) if vertical else (L, H))


def svg_capsule(length, vertical=False, stroke=None, sw=0.0, fill_left="none",
                fill_right="none", inner_fill=None, inner_gap=None, divider=True, pad=None):
    """A complete SVG file. stroke/sw draw the logo-style outline; inner_fill draws
    the filled left half inset by inner_gap (like the seal)."""
    pad = sw / 2 if pad is None else pad
    ld, rd, (bw, bh) = capsule_paths(pad, pad, length, vertical)
    W, Hh = bw + 2 * pad, bh + 2 * pad
    parts = [f'<svg width="{f(W)}" height="{f(Hh)}" viewBox="0 0 {f(W)} {f(Hh)}" fill="none" xmlns="http://www.w3.org/2000/svg">']
    st = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    parts.append(f'<path d="{ld}" fill="{fill_left}"{st}/>')
    parts.append(f'<path d="{rd}" fill="{fill_right}"{st}/>')
    if inner_fill:
        gap = inner_gap if inner_gap is not None else sw * 1.5
        ild, _, _ = capsule_paths(pad, pad, length, vertical, inset=gap)
        parts.append(f'<path d="{ild}" fill="{inner_fill}"/>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


# ---------- D1 (Avi, 17.11.2026): the stroke scales with the capsule ----------
STROKE_RATIO = 0.0085   # stroke = 0.85% of the full length, as in the seal (2.08 / 247.87)
STROKE_MIN = 1.5        # never thinner than 1.5px
DIVIDER_MAX = float('inf')  # 17.11.2026 (Avi, R-109): always keep the divider, like the seal. Was 120.
                        # Every capsule, at every size, is the two halves with the divider.


def stroke_for(length):
    """D1 stroke width (px) for a capsule of this full length (px, as rendered)."""
    return max(STROKE_MIN, length * STROKE_RATIO)


def outline_path(x, y, length, vertical=False, inset=0.0):
    """ONE continuous outline that follows both halves, with the step at the joint and
    no divider. RETIRED by R-109 (Avi 17.11.2026): never draw a brand capsule with it;
    every capsule keeps the divider (use capsule_paths / svg_outline). Kept only so old
    scripts still import. Returns (d, (box_w, box_h))."""
    g = geometry(length)
    H, h, wl, L = g["H"], g["h"], g["wl"], length
    cy, i = H / 2, inset
    lt, lb = cy - h / 2 + i, cy + h / 2 - i
    lr = (lb - lt) / 2
    rt, rb = i, H - i
    rr = (rb - rt) / 2

    def pt(u, v):
        return (x + (H - v), y + u) if vertical else (x + u, y + v)

    def P(u, v):
        px, py = pt(u, v)
        return f"{f(px)} {f(py)}"
    d = (f"M{P(wl, lt)}L{P(i + lr, lt)}A{f(lr)} {f(lr)} 0 0 0 {P(i + lr, lb)}"
         f"L{P(wl, lb)}L{P(wl, rb)}L{P(L - i - rr, rb)}A{f(rr)} {f(rr)} 0 0 0 {P(L - i - rr, rt)}"
         f"L{P(wl, rt)}Z")
    return d, ((H, L) if vertical else (L, H))


def svg_outline(length, vertical=False, stroke="#000", sw=None, long_fill=None, long_opacity=None, inner_gap=None):
    """A complete D1 SVG: the two halves with the divider (R-109, every size),
    stroke = stroke_for(box length) unless sw is given; optional filled long half,
    inset 1.5 strokes inside the outline like the seal."""
    sw = stroke_for(length) if sw is None else sw
    pad = sw / 2
    inner = length - sw
    parts = []
    if length >= DIVIDER_MAX:
        d, (bw, bh) = outline_path(pad, pad, inner, vertical)
        parts.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{f(sw)}" stroke-linejoin="round"/>')
    else:
        ld, rd, (bw, bh) = capsule_paths(pad, pad, inner, vertical)
        parts.append(f'<path d="{ld}" fill="none" stroke="{stroke}" stroke-width="{f(sw)}"/>')
        parts.append(f'<path d="{rd}" fill="none" stroke="{stroke}" stroke-width="{f(sw)}"/>')
    if long_fill:
        gap = inner_gap if inner_gap is not None else sw * 1.5
        ild, _, _ = capsule_paths(pad, pad, inner, vertical, inset=gap)
        op = f' fill-opacity="{long_opacity}"' if long_opacity is not None else ""
        parts.append(f'<path d="{ild}" fill="{long_fill}"{op}/>')
    W, Hh = bw + sw, bh + sw
    return (f'<svg width="{f(W)}" height="{f(Hh)}" viewBox="0 0 {f(W)} {f(Hh)}" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            + "\n".join(parts) + "\n</svg>\n")


def mask_data_uri(length, vertical=False, sw=0.0):
    """A CSS mask (url("data:image/svg+xml,...")) of the capsule, for decor drawn in CSS.

    sw > 0   outline (stroke baked in at this size): the two halves with the divider (R-109)
    sw = 0   filled capsule: both halves, with the gap at the divider (solid_paths)
    The colour comes from the element's background-color (a token); the mask only
    gives the shape, so the black in the data URI is alpha, never a visible colour.
    Size the element to the returned box (or the same aspect ratio) with
    mask-size: 100% 100%, so the stroke renders at sw px.
    Returns (css_url, (box_w, box_h)).
    """
    from urllib.parse import quote
    pad = sw / 2
    ld, rd, (bw, bh) = capsule_paths(pad, pad, length, vertical)
    W, Hh = bw + 2 * pad, bh + 2 * pad
    if sw and length + sw >= DIVIDER_MAX:
        od, _ = outline_path(pad, pad, length, vertical)
        body = f"<path d='{od}' fill='none' stroke='black' stroke-width='{f(sw)}' stroke-linejoin='round'/>"
    elif sw:
        body = (f"<path d='{ld}' fill='none' stroke='black' stroke-width='{f(sw)}'/>"
                f"<path d='{rd}' fill='none' stroke='black' stroke-width='{f(sw)}'/>")
    else:
        sl, sr, _ = solid_paths(pad, pad, length, vertical)
        body = f"<path d='{sl}{sr}'/>"
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {f(W)} {f(Hh)}'>{body}</svg>"
    return f'url("data:image/svg+xml,{quote(svg, safe=" =:/,.-")}")', (W, Hh)


# CSS decor masks used by hub.css (Capsule decor). Design size in px. D1: the stroke is
# 0.85% of the box length (stroke_for), the two halves with the divider (R-109, every size).
#   head        page-head outline, 600px wide (calc(var(--space-24) * 6.25)), stroke 5.1
#   band-line   capsule band, standing outline, 345.6px tall (calc(var(--space-24) * 3.6)), stroke 2.94
#   band-fill   capsule band, standing filled, 249.6px tall (calc(var(--space-24) * 2.6)), with the gap at the divider
def _d1(box_length, **kw):
    sw = stroke_for(box_length)
    return dict(length=box_length - sw, sw=sw, **kw)


CSS_MASKS = {
    "head": _d1(600),
    "band-line": _d1(345.6, vertical=True),
    "band-fill": dict(length=249.6, vertical=True),
}


def print_css():
    for name, kw in CSS_MASKS.items():
        uri, (w, h) = mask_data_uri(**kw)
        print(f"  /* {name}: {f(w)} x {f(h)} */")
        print(f"  --cap-mask-{name}: {uri};")


SHAPES = {
    # name: kwargs. D1 (17.11.2026): proportional stroke, the two halves with the divider (R-109),
    # the long half filled for the split variants. Colours as before (Sky outline, Sky or Logo Blue fill).
    "capsule-outline.svg": dict(length=320, stroke="#C9DDEA"),
    "capsule-split.svg": dict(length=320, stroke="#C9DDEA", long_fill="#C9DDEA"),
    "capsule-split-blue.svg": dict(length=320, stroke="#C9DDEA", long_fill="#3976C6"),
    "capsule-vertical.svg": dict(length=206, vertical=True, stroke="#C9DDEA", long_fill="#3976C6"),
}


def main():
    if "--print" in sys.argv:
        g = geometry(280)
        print({k: round(v, 2) for k, v in g.items()})
        print(capsule_paths(0, 0, 280))
        return
    if "--css" in sys.argv:
        print_css()
        return
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "assets", "shapes")
    for name, kw in SHAPES.items():
        with open(os.path.join(out, name), "w") as fh:
            fh.write(svg_outline(**kw))
        print("wrote", name)


if __name__ == "__main__":
    main()
