"""Spot illustrations and background patterns for unifiedmeds.

Python standard library only. Run from the hub root:  python3 -I assets/patterns/build_patterns.py
Writes SVG files next to this script. Every colour is read from tokens/tokens.json through
tools/capsule_svg.py token() (B-29): website palette only; the logo colours stay with the logo (R-84).
Shapes come only from the Quadrant Kit (Square, Quarter, Half, Circle, Arch, Arc) and the capsule.

Line weight (R-109, q126, Avi 18.11.2026): every capsule line is stroke_for() of the capsule's length AS
RENDERED: 0.85% of the length, never under 1.5px. Spots are exported once per placed size (160 on desktop,
96 on mobile and in small slots), so the rendered line is 1.5 at both. Patterns tile at 1x only.
The capsule shape files (the .um-cap mask sources) are made by tools/capsule_svg.py into assets/shapes/.
"""
import pathlib
import sys

OUT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent.parent / "tools"))
import capsule_svg as cs  # noqa: E402  (geometry, stroke_for and token())

T = cs.token
PAPER = T("color.surface.paper")
MIST = T("color.surface.mist")
DEEP = T("color.brand.deep-teal")
TEAL_DEEP = T("color.brand.teal-deep")
BLUE = T("color.brand.blue")
BLUE_DARK = T("color.brand.blue-dark")
GREEN = T("color.brand.green")
WASH_BLUE = T("color.surface.wash-blue")
WASH_GREEN = T("color.surface.wash-green")
LINE_BASE = T("color.line.base")
LINE_STRONG = T("color.line.strong")
LINE_MID = T("color.line.mid")
LINE_ON_DARK = T("color.line.on-dark")
OPACITY_CAPSULE = float(T("opacity.capsule"))

SPOT_GRID = 160
SPOT_SIZES = (160, 96)   # placed sizes; one file per size
SCALE = 1.0              # placed size / drawing grid, set per export in spots()


def line(length):
    """Capsule stroke in drawing units, so that it renders at stroke_for(rendered length) (R-109)."""
    return cs.stroke_for(length * SCALE) / SCALE


def f(n):
    return f"{n:g}"


# ---------- capsule geometry: the logo's own, asymmetric shape (R-105) ----------
# Left half = 55% of the length; right half taller (left = 93.3% of its height). Standing = turned 90 degrees
# clockwise, long half on top. Geometry from tools/capsule_svg.py (capsule_paths), never a symmetric rounded rect.


def _frame(cx, cy, length, vertical):
    """Top-left corner of the centre-line box for a capsule centred on (cx, cy) of centre-line length."""
    H = cs.geometry(length)["H"]
    bw, bh = (H, length) if vertical else (length, H)
    return cx - bw / 2, cy - bh / 2


def capsule_silhouette(x, y, length, vertical=False):
    """One closed path around both halves (no seam), same frame as cs.capsule_paths.
    RETIRED for fills (Avi 17.11.2026): a filled capsule keeps the gap at the divider, use cs.solid_paths."""
    g = cs.geometry(length)
    H, h, wl, L = g["H"], g["h"], g["wl"], length
    c = H / 2
    rl, rr = h / 2, H / 2
    tl, bl = c - h / 2, c + h / 2

    def pt(u, v):
        return (x + (H - v), y + u) if vertical else (x + u, y + v)

    def P(u, v):
        a, b = pt(u, v)
        return f"{cs.f(a)} {cs.f(b)}"
    return (f"M{P(wl, tl)}L{P(rl, tl)}A{cs.f(rl)} {cs.f(rl)} 0 0 0 {P(rl, bl)}L{P(wl, bl)}L{P(wl, H)}"
            f"L{P(L - rr, H)}A{cs.f(rr)} {cs.f(rr)} 0 0 0 {P(L - rr, 0)}L{P(wl, 0)}Z")


def capsule_outline(cx, cy, length, stroke, colour, vertical=False, seam=True, opacity=None):
    """Outline capsule centred on (cx, cy). length = OUTER length (stroke included).
    seam=True draws the two halves (the right half's closing edge is the divider, as in the seal).
    R-109 (Avi 17.11.2026): every brand capsule keeps the divider, so seam=False is retired."""
    op = f' opacity="{f(opacity)}"' if opacity is not None else ""
    L = length - stroke
    x, y = _frame(cx, cy, L, vertical)
    st = f'fill="none" stroke="{colour}" stroke-width="{f(stroke)}"{op}'
    if not seam:
        return [f'<path d="{capsule_silhouette(x, y, L, vertical)}" {st}/>']
    ld, rd, _ = cs.capsule_paths(x, y, L, vertical)
    return [f'<path d="{ld}" {st}/>', f'<path d="{rd}" {st}/>']


def capsule_half(cx, cy, length, stroke, colour, vertical=False, side="left"):
    """The filled half of a split capsule inside capsule_outline(cx, cy, length, stroke).
    side: 'left' / 'top' = the long half (filled in the seal), 'right' / 'bottom' = the short, wide half.
    Inset 1.5 stroke from the centre line, as the seal and the core capsule kit."""
    L = length - stroke
    x, y = _frame(cx, cy, L, vertical)
    ld, rd, _ = cs.capsule_paths(x, y, L, vertical, inset=stroke * 1.5)
    return f'<path d="{ld if side in ("left", "top") else rd}" fill="{colour}"/>'


def capsule_fill(cx, cy, length, colour, vertical=False, opacity=None):
    """Solid capsule centred on (cx, cy), full length = length. Avi 17.11.2026: both halves filled with a
    thin gap at the divider, one stroke wide (cs.stroke_for), like the seal. Never the continuous silhouette."""
    op = f' opacity="{f(opacity)}"' if opacity is not None else ""
    x, y = _frame(cx, cy, length, vertical)
    ld, rd, _ = cs.solid_paths(x, y, length, vertical, gap=line(length))
    return f'<path d="{ld}{rd}" fill="{colour}"{op}/>'


def capsule_height(length, stroke=0):
    """Outer height (width when vertical) of a capsule of outer length `length`."""
    return cs.geometry(length - stroke)["H"] + stroke


def quarter(cx, cy, r, corner, colour):
    """Quarter circle with its right angle at (cx, cy), opening toward corner: 'se', 'sw', 'ne', 'nw'."""
    dx = r if "e" in corner else -r
    dy = r if "s" in corner else -r
    sweep = 1 if (dx > 0) == (dy > 0) else 0
    return f'<path d="M{f(cx)} {f(cy)}H{f(cx + dx)}A{f(r)} {f(r)} 0 0 {sweep} {f(cx)} {f(cy + dy)}Z" fill="{colour}"/>'


def arch(x, y, w, h, colour, up=True):
    r = w / 2
    if up:
        return f'<path d="M{f(x)} {f(y + h)}V{f(y + r)}A{f(r)} {f(r)} 0 0 1 {f(x + w)} {f(y + r)}V{f(y + h)}Z" fill="{colour}"/>'
    return f'<path d="M{f(x)} {f(y)}V{f(y + h - r)}A{f(r)} {f(r)} 0 0 0 {f(x + w)} {f(y + h - r)}V{f(y)}Z" fill="{colour}"/>'


def circle(cx, cy, r, colour):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{colour}"/>'


def square(x, y, s, colour):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(s)}" height="{f(s)}" fill="{colour}"/>'


def svg(w, h, body, title, placed=None):
    inner = "\n".join("  " + b for b in body)
    pw = ph = placed
    if placed is None:
        pw, ph = w, h
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(pw)}" height="{f(ph)}" viewBox="0 0 {f(w)} {f(h)}" '
            f'role="img" aria-label="{title}">\n  <title>{title}</title>\n{inner}\n</svg>\n')


def write(name, text):
    (OUT / name).write_text(text)
    print("wrote", name, len(text.encode()), "bytes")


# ---------- spot illustrations: drawn on 160, transparent ground, for Paper, Mist or Card ----------

def spots():
    global SCALE
    for size in SPOT_SIZES:
        SCALE = size / SPOT_GRID
        suffix = "" if size == SPOT_GRID else f"-{size}"
        for name, (title, body) in spot_bodies().items():
            write(name.replace(".svg", f"{suffix}.svg"), svg(SPOT_GRID, SPOT_GRID, body, title, size))
    SCALE = 1.0


def spot_bodies():
    s = {}
    # Delivery: a plain square box, a split capsule across its face, a Quarter leaving the corner
    s["spot-delivery.svg"] = ("Plain box", [
        square(24, 48, 88, WASH_BLUE),
        quarter(112, 48, 26, "ne", GREEN),
        *capsule_outline(68, 92, 64, line(64), DEEP),
        capsule_half(68, 92, 64, line(64), DEEP, side="left"),
    ])
    # Provider review: an Arch frame, a split capsule inside it, a Circle that marks it reviewed
    s["spot-provider-review.svg"] = ("Provider review", [
        arch(32, 20, 80, 120, WASH_BLUE),
        *capsule_outline(72, 88, 56, line(56), DEEP),
        capsule_half(72, 88, 56, line(56), DEEP, side="left"),
        circle(116, 120, 20, GREEN),
    ])
    # Refill: a Square calendar of nine Circles, one marked, and a vertical capsule beside it
    dots = [circle(48 + 22 * c, 48 + 22 * r, 7, DEEP if (r, c) == (2, 2) else PAPER) for r in range(3) for c in range(3)]
    s["spot-refill.svg"] = ("Refill calendar", [
        square(26, 26, 88, WASH_GREEN),
        *dots,
        *capsule_outline(126, 94, 80, line(80), DEEP, vertical=True),
        capsule_half(126, 94, 80, line(80), BLUE, vertical=True, side="top"),
    ])
    # Privacy: a Circle behind, an outline capsule as the shackle, a Square body with a Paper keyhole
    s["spot-privacy.svg"] = ("Privacy lock", [
        circle(108, 38, 22, WASH_BLUE),
        *capsule_outline(70, 78, 128, line(128), DEEP, vertical=True),
        square(30, 68, 80, DEEP),
        circle(70, 98, 8, PAPER),
        capsule_fill(70, 108, 20, PAPER, vertical=True),
    ])
    # Chat: two capsules as messages, each with a Quarter tail; three Paper circles in the provider's message
    s["spot-chat.svg"] = ("Chat with a provider", [
        capsule_fill(68, 43, 96, DEEP),
        quarter(40, 43 + capsule_height(96) * cs.LEFT_HEIGHT / 2 - 0.5, 16, "se", DEEP),
        circle(52, 43, 4, PAPER), circle(68, 43, 4, PAPER), circle(84, 43, 4, PAPER),
        capsule_fill(94, 103, 92, WASH_BLUE),
        quarter(120, 103 + capsule_height(92) / 2 - 0.5, 16, "sw", WASH_BLUE),
    ])
    # Ongoing care: two Arcs make an open ring around a vertical split capsule
    def arc_band(q, colour):
        cx = cy = 80
        R, r = 56, 48  # band 8 = 14% of the radius, as the kit Arc
        if q == "ne":
            return f'<path d="M{cx} {cy - R}A{R} {R} 0 0 1 {cx + R} {cy}H{cx + r}A{r} {r} 0 0 0 {cx} {cy - r}Z" fill="{colour}"/>'
        return f'<path d="M{cx} {cy + R}A{R} {R} 0 0 1 {cx - R} {cy}H{cx - r}A{r} {r} 0 0 0 {cx} {cy + r}Z" fill="{colour}"/>'
    s["spot-ongoing.svg"] = ("Ongoing care", [
        arc_band("ne", BLUE_DARK),
        arc_band("sw", WASH_BLUE),
        *capsule_outline(80, 80, 72, line(72), DEEP, vertical=True),
        capsule_half(80, 80, 72, line(72), GREEN, vertical=True, side="top"),
    ])
    return s


# ---------- background patterns: tileable, a light and a dark version each ----------

def tile(w, h, ground, shapes, title, opacity=None):
    """shapes: callables (dx, dy) -> list of SVG strings. Each is drawn at the 9 wrap offsets so edges join."""
    body = [f"<desc>Tile {f(w)} x {f(h)}. Transparent: set the ground ({ground}) in CSS or in the layout, so tiles join without seams.</desc>"]
    grp = []
    for dx in (-w, 0, w):
        for dy in (-h, 0, h):
            for sh in shapes:
                grp.extend(sh(dx, dy))
    op = f' opacity="{f(opacity)}"' if opacity is not None else ""
    body.append(f"<g{op}>" + "".join(grp) + "</g>")
    return svg(w, h, body, title)


def patterns():
    themes = {
        "light": dict(ground_a=MIST, ground_b=PAPER, line_a=LINE_MID, line_b=LINE_STRONG, fill_a=MIST, fill_b=LINE_BASE, scatter=WASH_BLUE, scatter_op=OPACITY_CAPSULE, arch_fill=PAPER),
        "dark": dict(ground_a=DEEP, ground_b=DEEP, line_a=LINE_ON_DARK, line_b=LINE_ON_DARK, fill_a=TEAL_DEEP, fill_b=LINE_ON_DARK, scatter=LINE_ON_DARK, scatter_op=None, arch_fill=TEAL_DEEP),
    }
    for mode, t in themes.items():
        # 1 Capsule grid: small outline capsules in a brick rhythm. Tile 120 x 80.
        write(f"pattern-capsule-grid-{mode}.svg", tile(120, 80, t["ground_a"], [
            lambda dx, dy: capsule_outline(30 + dx, 20 + dy, 44, line(44), t["line_a"]),
            lambda dx, dy: capsule_outline(90 + dx, 60 + dy, 44, line(44), t["line_a"]),
        ], f"Capsule grid pattern, {mode}"))
        # 2 Half-capsule rhythm: split capsules, the filled half alternating left and right. Tile 160 x 96.
        write(f"pattern-half-capsule-{mode}.svg", tile(160, 96, t["ground_b"], [
            lambda dx, dy: capsule_outline(44 + dx, 24 + dy, 64, line(64), t["line_b"]) + [capsule_half(44 + dx, 24 + dy, 64, line(64), t["fill_a"], side="left")],
            lambda dx, dy: capsule_outline(124 + dx, 72 + dy, 64, line(64), t["line_b"]) + [capsule_half(124 + dx, 72 + dy, 64, line(64), t["fill_a"], side="right")],
        ], f"Half-capsule rhythm pattern, {mode}"))
        # 3 Quadrant field: Quarters meeting at the tile corners, a small Circle in the open cells. Tile 160 x 160.
        write(f"pattern-quadrant-field-{mode}.svg", tile(160, 160, t["ground_b"], [
            lambda dx, dy: [quarter(0 + dx, 0 + dy, 64, "se", t["fill_a"]), quarter(160 + dx, 160 + dy, 64, "nw", t["fill_a"])],
            lambda dx, dy: [circle(120 + dx, 40 + dy, 10, t["fill_b"]), circle(40 + dx, 120 + dy, 10, t["fill_b"])],
        ], f"Quadrant field pattern, {mode}"))
        # 4 Outline capsule scatter: larger outline capsules, horizontal and vertical, crossing the tile edges. Tile 320 x 320.
        write(f"pattern-capsule-scatter-{mode}.svg", tile(320, 320, t["ground_b"], [
            lambda dx, dy: capsule_outline(84 + dx, 58 + dy, 120, line(120), t["scatter"]),
            lambda dx, dy: capsule_outline(234 + dx, 76 + dy, 120, line(120), t["scatter"], vertical=True),
            lambda dx, dy: capsule_outline(310 + dx, 218 + dy, 120, line(120), t["scatter"]),
            lambda dx, dy: capsule_outline(98 + dx, 216 + dy, 120, line(120), t["scatter"], vertical=True),
            lambda dx, dy: capsule_outline(192 + dx, 296 + dy, 64, line(64), t["scatter"]),
        ], f"Outline capsule scatter pattern, {mode}", opacity=t["scatter_op"]))
        # 5 Arch rhythm: Arches standing up and hanging down, in offset rows. Tile 120 x 120.
        write(f"pattern-arch-rhythm-{mode}.svg", tile(120, 120, t["ground_a"], [
            lambda dx, dy: [arch(10 + dx, 8 + dy, 40, 52, t["arch_fill"], up=True)],
            lambda dx, dy: [arch(70 + dx, 60 + dy, 40, 52, t["arch_fill"], up=False)],
        ], f"Arch rhythm pattern, {mode}"))


if __name__ == "__main__":
    spots()
    patterns()
