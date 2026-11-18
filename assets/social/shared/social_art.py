"""unifiedmeds social kits · drawing toolkit (shared by every channel generator).

Writes plain SVG files (live text in DM Serif Display and Inter, photos linked
from assets/photos, logo files embedded as they are) and renders each SVG to a
PNG at the exact pixel size with headless Google Chrome.

Rules built in:
  * the capsule is always the logo's own asymmetric shape (tools/capsule_svg.py);
  * logos and the app-icon mark are the core hub files, embedded, never redrawn;
  * colours are the hex values from tokens.json only (see C below).

Used by make_social.py in this folder. Python 3 standard library only.
"""
import html
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).resolve().parent          # assets/social/shared
EXT = HERE.parents[2]                                    # the hub root (unifiedmeds-brand-hub-merged)
CORE = EXT                                               # the hub root (logo files, icons in assets/)
PHOTOS = EXT / "assets" / "photos"
sys.path.insert(0, str(EXT / "tools"))
from capsule_svg import capsule_paths, geometry  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=block"

# tokens.json hex values (brand, surface, text, logo groups)
C = {
    "deep-teal": "#264653", "teal-deep": "#1C3742", "blue": "#6E8B97", "blue-dark": "#4E6873",
    "yellow": "#FFBE0B", "paper": "#FEFCF6", "mist": "#E8E7E1", "card": "#FFFFFF",
    "wash-blue": "#A8BEC7", "wash-green": "#B6CDBB", "slate": "#55747F", "line-base": "#E3DFD5",
    "navy": "#0F2E57", "cream": "#F1ECE0", "white": "#FFFFFF", "sky": "#C9DDEA",
}
SERIF = "'DM Serif Display', Georgia, serif"
SANS = "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
LEGAL = "Assessment only. Not a diagnosis."


def f(n):
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def _logo_parts(name):
    src = (CORE / "assets" / "brand" / name).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S).strip()
    _, _, w, h = (float(v) for v in vb.split())
    return vb, inner, w, h


class Art:
    """One canvas. Coordinates are output pixels."""

    def __init__(self, w, h, folder, ground=None, title=""):
        self.w, self.h, self.folder, self.title = w, h, pathlib.Path(folder), title
        self.defs, self.body, self.n = [], [], 0
        if ground:
            self.rect(0, 0, w, h, ground)

    # ---- primitives -------------------------------------------------------
    def uid(self, p):
        self.n += 1
        return f"{p}{self.n}"

    def rect(self, x, y, w, h, fill, rx=0, opacity=None, stroke=None, sw=0):
        o = f' opacity="{opacity}"' if opacity is not None else ""
        s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
        r = f' rx="{f(rx)}"' if rx else ""
        self.body.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"{r} fill="{fill}"{o}{s}/>')

    def circle(self, cx, cy, r, fill):
        self.body.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}"/>')

    def photo_href(self, name):
        return os.path.relpath(PHOTOS / name, self.folder)

    def photo(self, name, x, y, w, h, align="xMidYMid", rx=0, clip_d=None):
        """A photo filling the box (cover crop). align = SVG preserveAspectRatio alignment."""
        cid = self.uid("c")
        shape = f'<path d="{clip_d}"/>' if clip_d else f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}"/>'
        self.defs.append(f'<clipPath id="{cid}">{shape}</clipPath>')
        self.body.append(
            f'<image href="{self.photo_href(name)}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" '
            f'preserveAspectRatio="{align} slice" clip-path="url(#{cid})"/>')

    def text(self, x, y, lines, size, fam="serif", fill=None, weight=400, lh=1.1, anchor="start"):
        """y is the baseline of the first line."""
        fam_css = SERIF if fam == "serif" else SANS
        fill = fill or C["teal-deep"]
        spans = []
        for i, line in enumerate(lines):
            dy = "0" if i == 0 else f(size * lh)
            spans.append(f'<tspan x="{f(x)}" dy="{dy}">{html.escape(line)}</tspan>')
        self.body.append(
            f'<text x="{f(x)}" y="{f(y)}" font-family="{html.escape(fam_css)}" font-size="{f(size)}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{"".join(spans)}</text>')
        return y + size * lh * (len(lines) - 1)

    # ---- brand pieces -----------------------------------------------------
    def logo(self, name, x, y, h=None, w=None):
        """Embed a core logo file (logo-seal.svg, logo-horizontal-reversed.svg ...). Returns (w, h)."""
        vb, inner, vw, vh = _logo_parts(name)
        if h is None:
            h = w * vh / vw
        w = h * vw / vh
        self.body.append(f'<svg x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" viewBox="{vb}" fill="none" overflow="visible">{inner}</svg>')
        return w, h

    def mark(self, x, y, size, scheme="navy"):
        """The app-icon 'u|m' capsule (from app-icon.svg) without its rounded square.
        scheme navy: white mark (as the app icon). scheme cream: the same mark in Navy, the 'u' in Cream."""
        src = (CORE / "assets" / "brand" / "app-icon.svg").read_text()
        paths = re.findall(r"<path [^>]*/>", src)[1:]      # drop the rounded-square ground
        if scheme == "cream":
            paths = [p.replace('"white"', '"__N__"').replace('"#0F2E57"', f'"{C["cream"]}"').replace('"__N__"', f'"{C["navy"]}"') for p in paths]
        # the mark spans x 11.6..108.4, y 43.4..76.6 in the 120 box: centre it in a size x size square
        s = size / 120
        self.body.append(f'<g fill="none" transform="translate({f(x)} {f(y)}) scale({f(s)})">{"".join(paths)}</g>')

    def icon(self, name, cx, cy, size, colour, stroke_units=2.5):
        """A core capsule-set icon (64 grid), recoloured as a whole, stroke set for its placed size."""
        src = (CORE / "assets" / "icons" / name).read_text()
        inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
        inner = inner.replace("#0F2E57", colour)
        inner = re.sub(r'stroke-width="[^"]*"', f'stroke-width="{f(stroke_units)}"', inner)
        s = size / 64
        self.body.append(f'<g fill="none" transform="translate({f(cx - size / 2)} {f(cy - size / 2)}) scale({f(s)})">{inner}</g>')

    def capsule(self, x, y, length, vertical=False, stroke=None, sw=0, opacity=None, inner=None, gap=None, fill=None):
        """The logo capsule (asymmetric). stroke = outline; inner = filled long half inset by gap (like the seal);
        fill = both halves solid."""
        ld, rd, _ = capsule_paths(x, y, length, vertical)
        o = f' opacity="{opacity}"' if opacity is not None else ""
        g = [f"<g{o}>"]
        if fill:
            g.append(f'<path d="{ld}Z" fill="{fill}"/><path d="{rd}" fill="{fill}"/>')
        if stroke:
            g.append(f'<path d="{ld}" fill="none" stroke="{stroke}" stroke-width="{f(sw)}"/>'
                     f'<path d="{rd}" fill="none" stroke="{stroke}" stroke-width="{f(sw)}"/>')
        if inner:
            gp = gap if gap is not None else sw * 1.5
            ild, _, _ = capsule_paths(x, y, length, vertical, inset=gp)
            g.append(f'<path d="{ild}Z" fill="{inner}"/>')
        g.append("</g>")
        self.body.append("".join(g))
        return geometry(length)

    def capsule_photo(self, name, x, y, length, vertical=False, align="xMidYMid"):
        """A photo cropped to the capsule (R-33 allows it). Returns the bounding box (w, h)."""
        ld, rd, (bw, bh) = capsule_paths(x, y, length, vertical)
        self.photo(name, x, y, bw, bh, align=align, clip_d=f"{ld}Z {rd}")
        return bw, bh

    def button(self, x, y, label, k=1.0):
        """'Get started': Yellow, 5px corners at display size (R-11, R-40, R-55). k = canvas px per display px."""
        h, pad, fs = 50 * k, 24 * k, 15 * k
        w = pad * 2 + len(label) * fs * 0.56
        self.rect(x, y, w, h, C["yellow"], rx=5 * k)
        self.text(x + w / 2, y + h / 2 + fs * 0.36, [label], fs, "sans", C["teal-deep"], 500, anchor="middle")
        return w, h

    # ---- output -----------------------------------------------------------
    def svg(self):
        t = f"<title>{html.escape(self.title)}</title>" if self.title else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
                f'{t}<style>@import url("{FONTS.replace("&", "&amp;")}");</style>'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>\n')

    def save(self, path):
        path = pathlib.Path(path)
        path.write_text(self.svg())
        return path


def render(jobs, workers=4):
    """jobs: list of (svg_path, png_path, w, h). Renders with headless Chrome at device scale 1."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="um-social-"))

    def one(job):
        svg_path, png_path, w, h = job
        svg_path, png_path = pathlib.Path(svg_path), pathlib.Path(png_path)
        body = svg_path.read_text()
        page = tmp / (svg_path.stem + ".html")
        page.write_text(
            f'<!doctype html><html><head><meta charset="utf-8"><base href="{svg_path.parent.as_uri()}/">'
            f'<link rel="stylesheet" href="{FONTS}"><style>html,body{{margin:0;padding:0;overflow:hidden;background:transparent}}'
            f'svg{{display:block}}</style></head><body>{body}</body></html>')
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={w},{h}", "--virtual-time-budget=8000", "--allow-file-access-from-files",
                        f"--screenshot={png_path}", page.as_uri()], capture_output=True, timeout=120)
        return png_path

    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(one, jobs))
