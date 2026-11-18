"""Shapes for the Ads page (round 2, 17.11.2026). Python standard library only.

Run:  python3 -I assets/ads/build_ads_shapes.py   (from the extended hub root, or anywhere)

Writes, next to this script:
  capsule-line-h.svg / capsule-line-v.svg      D1 outline, R-109 (Avi 17.11.2026): the two halves with the
                                               divider at every size, as in the seal: the long half open
                                               toward the joint, the short, taller half closed by the divider.
                                               One path, two subpaths (so <use> and the draw-on keep working).
                                               Stroke = 0.85% of the full length (Paper-free: Deep Teal stroke).
  capsule-longhalf-h.svg / -v.svg              D2: the long half only, filled, inset like the seal's filled half.
  logo-icon-paper.svg / logo-icon-teal.svg     the capsule mark without words, taken from logo-seal.svg
                                               (the outline and fill paths, recoloured; nothing redrawn).
  shapes.json                                  the path data the page inlines (src/ads.html, <defs>).
Geometry: tools/capsule_svg.py (the logo's asymmetric capsule, R-105).
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXT = HERE.parent.parent
sys.path.insert(0, str(EXT / "tools"))
import capsule_svg as cs  # noqa: E402

DEEP, PAPER = "#264653", "#FEFCF6"
L = 1000.0                 # centre-line length of the master shape
SW = 0.0085 * L            # D1: stroke = 0.85% of the full length
INSET = 1.5 * SW           # the filled long half sits inside the line, as in the seal


def silhouette(x, y, length, vertical=False):
    g = cs.geometry(length)
    H, h, wl = g["H"], g["h"], g["wl"]
    c, rl, rr = H / 2, g["h"] / 2, H / 2
    tl, bl = c - h / 2, c + h / 2

    def P(u, v):
        a, b = ((x + (H - v), y + u) if vertical else (x + u, y + v))
        return f"{cs.f(a)} {cs.f(b)}"
    return (f"M{P(wl, tl)}L{P(rl, tl)}A{cs.f(rl)} {cs.f(rl)} 0 0 0 {P(rl, bl)}L{P(wl, bl)}L{P(wl, H)}"
            f"L{P(length - rr, H)}A{cs.f(rr)} {cs.f(rr)} 0 0 0 {P(length - rr, 0)}L{P(wl, 0)}Z")


def main():
    H = cs.geometry(L)["H"]
    out = {"length": L, "height": round(H, 2), "stroke": SW}
    for vertical in (False, True):
        o = "v" if vertical else "h"
        bw, bh = (H, L) if vertical else (L, H)
        ld, rd, _ = cs.capsule_paths(0, 0, L, vertical)
        line = ld + rd          # R-109: both halves with the divider, never the continuous silhouette
        half = cs.capsule_paths(0, 0, L, vertical, inset=INSET)[0]
        out[f"line_{o}"], out[f"half_{o}"], out[f"box_{o}"] = line, half, [round(bw, 2), round(bh, 2)]
        p = SW / 2
        vb = f"{cs.f(-p)} {cs.f(-p)} {cs.f(bw + SW)} {cs.f(bh + SW)}"
        (HERE / f"capsule-line-{o}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{cs.f(bw + SW)}" height="{cs.f(bh + SW)}">'
            f'<path d="{line}" fill="none" stroke="{DEEP}" stroke-width="{cs.f(SW)}"/></svg>\n')
        (HERE / f"capsule-longhalf-{o}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{cs.f(bw + SW)}" height="{cs.f(bh + SW)}">'
            f'<path d="{half}" fill="{DEEP}"/></svg>\n')
    # logo icon: the first three paths of the seal (both halves and the filled half), no words
    seal = (EXT.parent / "unifiedmeds-brand-hub" / "assets" / "brand" / "logo-seal.svg").read_text()
    paths = re.findall(r"<path [^>]*/>", seal)[:3]
    for name, col in (("paper", PAPER), ("teal", DEEP)):
        body = "".join(re.sub(r'#0F2E57', col, pth) for pth in paths)
        (HERE / f"logo-icon-{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="250" height="91" viewBox="0 0 250 91" fill="none">{body}</svg>\n')
    (HERE / "shapes.json").write_text(json.dumps(out, indent=1))
    print("ok", {k: v for k, v in out.items() if not k.startswith(("line", "half"))})


if __name__ == "__main__":
    main()
