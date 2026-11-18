"""sk_kit: shared helpers for the TikTok, YouTube and LinkedIn kits (agent S2, 17.11.2026).

The same file sits in assets/social/tiktok/, assets/social/youtube/ and assets/social/linkedin/
so every channel folder rebuilds on its own. Each channel's make.py imports it.

What it does
  * draws SVG art with brand values only (hex values from core tokens/tokens.json);
  * places the logo files as they are (never redrawn) and the capsule from tools/capsule_svg.py;
  * embeds photos from assets/photos/ so a downloaded SVG still shows them;
  * exports PNG at the exact pixel size with headless Chrome (fonts load from Google Fonts),
    plus small JPG/PNG previews for the hub page (sips);
  * writes the hub page HTML (src/social-<channel>.html) with the shared sk- classes.
"""
import base64
import concurrent.futures
import html
import importlib.util
import os
import pathlib
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
EXT = HERE.parents[2]                       # the hub root (unifiedmeds-brand-hub-merged)
CORE = EXT                                  # the hub root: logo files in assets/brand
PHOTOS = EXT / "assets" / "photos"
BRAND = CORE / "assets" / "brand"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Hex values copied from core tokens/tokens.json (standalone asset files may use them).
C = {
    "deep_teal": "#264653", "teal_deep": "#1C3742", "paper": "#FEFCF6", "mist": "#E8E7E1",
    "card": "#FFFFFF", "wash_blue": "#A8BEC7", "slate": "#55747F", "blue_dark": "#4E6873",
    "yellow": "#FFBE0B", "coral": "#E76F51", "line_base": "#E3DFD5", "line_on_dark": "#3E5C6B",
    "navy": "#0F2E57", "ink": "#031D2C", "sky": "#C9DDEA", "logo_blue": "#3976C6",
}
SERIF = "'DM Serif Display', Georgia, serif"
SANS = "Inter, 'Helvetica Neue', Arial, sans-serif"
FONT_IMPORT = ("@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display"
               "&amp;family=Inter:wght@400;500;600&amp;display=block');")

_spec = importlib.util.spec_from_file_location("capsule_svg", EXT / "tools" / "capsule_svg.py")
capsule_svg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(capsule_svg)


def f(n):
    return capsule_svg.f(n)


# ---------------------------------------------------------------- drawing
_uid = [0]


def uid(p="c"):
    _uid[0] += 1
    return f"{p}{_uid[0]}"


def rect(x, y, w, h, fill, r=0, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}" fill="{fill}"{extra}/>'


def est(s, size, fam="serif", weight=400):
    k = 0.47 if fam == "serif" else (0.56 if weight >= 600 else 0.53)
    return len(s) * size * k


def wrap(s, size, maxw, fam="serif", weight=400):
    """Greedy wrap, then rebalanced so the last line never holds a single word."""
    base = _wrap(s, size, maxw, fam, weight)
    if len(base) < 2 or len(base[-1].split()) > 1:
        return base
    m = maxw
    while m > maxw * 0.55:
        m -= maxw * 0.04
        t = _wrap(s, size, m, fam, weight)
        if len(t) > len(base) + 1:
            break
        if len(t[-1].split()) > 1 and len(t) == len(base):
            return t
    return base


def _wrap(s, size, maxw, fam="serif", weight=400):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and est(t, size, fam, weight) > maxw:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def text(x, y, lines, size, fill, fam="serif", weight=400, lh=1.12, anchor="start", ls=0, opacity=1):
    if isinstance(lines, str):
        lines = [lines]
    family = SERIF if fam == "serif" else SANS
    out = [f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{f(size)}" '
           f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
           + (f' letter-spacing="{ls}"' if ls else "") + (f' opacity="{opacity}"' if opacity != 1 else "") + ">"]
    for i, ln in enumerate(lines):
        dy = 0 if i == 0 else size * lh
        out.append(f'<tspan x="{f(x)}" dy="{f(dy)}">{html.escape(ln)}</tspan>')
    out.append("</text>")
    return "".join(out)


def block_h(n, size, lh=1.12):
    return size + (n - 1) * size * lh


_logo_cache = {}


def logo(name, x, y, w=None, h=None):
    """Place a logo file from the core hub as it is. Give w or h; the other follows the file."""
    if name not in _logo_cache:
        _logo_cache[name] = (BRAND / f"{name}.svg").read_text()
    src = _logo_cache[name]
    head_end = src.index(">") + 1
    head = src[:head_end]
    vb = head.split('viewBox="')[1].split('"')[0]
    vw, vh = [float(v) for v in vb.split()[2:]]
    if w is None:
        w = h * vw / vh
    if h is None:
        h = w * vh / vw
    inner = src[head_end:].rsplit("</svg>", 1)[0]
    return (f'<svg x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" viewBox="{vb}" fill="none" '
            f'overflow="visible">{inner}</svg>'), w, h


def logo_ratio(name):
    _, w, h = logo(name, 0, 0, w=100)
    return w / h


_dims = {}


def photo_dims(name):
    if name not in _dims:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(PHOTOS / name)],
                             capture_output=True, text=True).stdout.split()
        _dims[name] = (int(out[-3]), int(out[-1]))
    return _dims[name]


_b64 = {}


def photo(name, x, y, w, h, fx=0.5, fy=0.4, r=0, zoom=1.0):
    """A photo cropped to the box (cover), focal point fx, fy (0..1 of the photo)."""
    iw, ih = photo_dims(name)
    s = max(w / iw, h / ih) * zoom
    dw, dh = iw * s, ih * s
    ox = min(0, max(w - dw, w / 2 - fx * dw))
    oy = min(0, max(h - dh, h / 2 - fy * dh))
    if name not in _b64:
        _b64[name] = base64.b64encode((PHOTOS / name).read_bytes()).decode()
    cid = uid("p")
    return (f'<clipPath id="{cid}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}"/></clipPath>'
            f'<image href="data:image/jpeg;base64,{_b64[name]}" x="{f(x + ox)}" y="{f(y + oy)}" '
            f'width="{f(dw)}" height="{f(dh)}" preserveAspectRatio="none" clip-path="url(#{cid})"/>')


def capsule(x, y, length, vertical=False, stroke=None, sw=0, inner=None, gap=None, fill_left="none",
            fill_right="none"):
    """The true logo capsule (asymmetric), from tools/capsule_svg.py. Outline, optionally the inner fill."""
    ld, rd, _ = capsule_svg.capsule_paths(x, y, length, vertical)
    st = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
    out = [f'<path d="{ld}" fill="{fill_left}"{st}/>', f'<path d="{rd}" fill="{fill_right}"{st}/>']
    if inner:
        g = gap if gap is not None else sw * 1.6
        ild, _, _ = capsule_svg.capsule_paths(x, y, length, vertical, inset=g)
        out.append(f'<path d="{ild}" fill="{inner}"/>')
    return "".join(out)


def capsule_box(length, vertical=False):
    g = capsule_svg.geometry(length)
    return (g["H"], length) if vertical else (length, g["H"])


def button(x, y, label, h, size=None, anchor="start"):
    """The Yellow CTA: a rounded rectangle (radius = 10% of the height, as 5 of 50), Teal Deep label."""
    size = size or h * 0.3
    w = est(label, size, "sans", 500) + h * 0.96
    if anchor == "middle":
        x = x - w / 2
    return (rect(x, y, w, h, C["yellow"], r=h * 0.1)
            + text(x + w / 2, y + h / 2 + size * 0.36, label, size, C["teal_deep"], "sans", 500, anchor="middle")), w


def doc(w, h, body, bg=None, title="unifiedmeds"):
    b = rect(0, 0, w, h, bg) if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{html.escape(title)}</title><style>{FONT_IMPORT}</style>{b}{body}</svg>\n')


# ---------------------------------------------------------------- overlays (safe-zone templates)
def overlay(w, h, keep=(), safe=None, labels=(), circle=None, s=1.0, guides=()):
    """A transparent safe-zone template. keep = rects covered by platform UI (tinted, dashed);
    safe = the rect every device shows (dashed); circle = (cx, cy, r) avatar crop."""
    lw = max(2, round(3 * s))
    dash = f"{round(14 * s)} {round(10 * s)}"
    out = []
    for (x, y, ww, hh) in keep:
        out.append(rect(x, y, ww, hh, C["coral"], extra=f' fill-opacity="0.24" stroke="{C["coral"]}" '
                        f'stroke-width="{lw}" stroke-dasharray="{dash}"'))
    if safe:
        x, y, ww, hh = safe
        out.append(rect(x, y, ww, hh, "none", extra=f' stroke="{C["deep_teal"]}" stroke-width="{lw * 2}" '
                        f'stroke-dasharray="{dash}"'))
        out.append(rect(x, y, ww, hh, "none", extra=f' stroke="{C["paper"]}" stroke-width="{lw}" '
                        f'stroke-dasharray="{dash}"'))
    if circle:
        cx, cy, r = circle
        out.append(f'<path d="M0 0H{w}V{h}H0Z M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z" '
                   f'fill="{C["ink"]}" fill-opacity="0.35" fill-rule="evenodd"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["coral"]}" stroke-width="{lw}" '
                   f'stroke-dasharray="{dash}"/>')
    for (x, y, ww, hh) in guides:
        out.append(rect(x, y, ww, hh, "none", extra=f' stroke="{C["logo_blue"]}" stroke-width="{lw}" '
                        f'stroke-dasharray="{round(4 * s)} {round(8 * s)}"'))
    for (x, y, t, anchor) in labels:
        size = round(26 * s)
        out.append(f'<text x="{f(x)}" y="{f(y)}" font-family="{SANS}" font-size="{size}" font-weight="600" '
                   f'fill="{C["ink"]}" stroke="{C["paper"]}" stroke-width="{max(3, round(6 * s))}" '
                   f'paint-order="stroke" text-anchor="{anchor}">{html.escape(t)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            + "".join(out) + "</svg>\n")


# ---------------------------------------------------------------- export
def write(path, s):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(s)


def _shot(job):
    svg, png, w, h, transparent = job
    tmp = tempfile.mkdtemp(prefix="skchrome")
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
           f"--user-data-dir={tmp}", f"--window-size={w},{h}", "--force-device-scale-factor=1",
           "--virtual-time-budget=9000", f"--screenshot={png}"]
    if transparent:
        cmd.append("--default-background-color=00000000")
    cmd.append(pathlib.Path(svg).resolve().as_uri())
    subprocess.run(cmd, capture_output=True, timeout=120)
    shutil.rmtree(tmp, ignore_errors=True)
    return png


def export(jobs, workers=6):
    """jobs: (svg_path, png_path, w, h, transparent). Writes PNGs at the exact size."""
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        list(ex.map(_shot, jobs))


def pdf(html_path, pdf_path):
    tmp = tempfile.mkdtemp(prefix="skchrome")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={tmp}", "--no-pdf-header-footer",
                    "--virtual-time-budget=9000", f"--print-to-pdf={pdf_path}",
                    pathlib.Path(html_path).resolve().as_uri()], capture_output=True, timeout=120)
    shutil.rmtree(tmp, ignore_errors=True)


def preview(png, out, maxpx=720):
    """A light preview for the hub page: JPG for opaque art, PNG where the art is transparent."""
    out = pathlib.Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix == ".jpg":
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80", "-Z", str(maxpx), str(png),
                        "--out", str(out)], capture_output=True)
    else:
        subprocess.run(["sips", "-Z", str(maxpx), str(png), "--out", str(out)], capture_output=True)


SHARED = EXT / "assets" / "social" / "shared"


def shared_avatar(opt, size):
    """The profile picture pair shared by all six kits (S1's masters in assets/social/shared/, read only):
    A = the "u|m" mark in Navy on Cream, B = the white mark on Navy (the app icon colours, R-93)."""
    s = (SHARED / f"avatar-{opt}.svg").read_text()
    return s.replace('width="800" height="800"', f'width="{size}" height="{size}"', 1)


def jpg_copy(png, limit=1048576):
    """A JPG (quality 80) beside any PNG over 1 MB, for photo-led art. Returns the path or None."""
    png = pathlib.Path(png)
    jpg = png.with_suffix(".jpg")
    if png.exists() and png.stat().st_size > limit:
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80", str(png), "--out", str(jpg)],
                       capture_output=True)
        return jpg
    if jpg.exists():
        jpg.unlink()
    return None


def size_label(path):
    n = pathlib.Path(path).stat().st_size
    return f"{n / 1048576:.1f} MB" if n >= 1048576 else f"{max(1, round(n / 1024))} KB"


# ---------------------------------------------------------------- page helpers
PAGE_CSS = """
  .rule > .status { justify-self: start; }
  .sk-asset { display: grid; gap: var(--space-4); padding-top: var(--space-8); border-top: 1px solid var(--color-line-base); margin-top: var(--space-8); }
  .sk-asset:first-of-type { border-top: 0; margin-top: 0; padding-top: 0; }
  .sk-asset > h3 { font: var(--type-desktop-h3-weight) var(--type-desktop-h3-size) / var(--type-desktop-h3-line) var(--font-family-serif); color: var(--color-text-strong); }
  .sk-asset > p { max-width: 68ch; color: var(--color-text-primary); }
  .sk-spec { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: var(--space-2) var(--space-4); margin: 0; padding: var(--space-4); border-radius: var(--radius-small); background: var(--color-surface-mist); }
  .sk-spec div { display: grid; gap: var(--space-1); min-width: 0; }
  .sk-spec dt { font: var(--type-desktop-label-weight) var(--type-desktop-label-size) / var(--type-desktop-label-line) var(--font-family-sans); letter-spacing: var(--type-desktop-label-tracking); color: var(--color-text-secondary-on-mist); }
  .sk-spec dd { margin: 0; font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); color: var(--color-text-strong); overflow-wrap: anywhere; }
  .sk-pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-6); align-items: start; }
  .sk-pair--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .sk-opt { margin: 0; display: grid; grid-row: span 2; grid-template-rows: subgrid; row-gap: var(--space-3); min-width: 0; }
  .sk-opt figcaption { color: var(--color-text-secondary); font: var(--type-desktop-caption-weight) var(--type-desktop-caption-size) / var(--type-desktop-caption-line) var(--font-family-sans); }
  .sk-opt figcaption b { color: var(--color-text-strong); font-weight: 600; }
  .sk-opt figcaption a { white-space: nowrap; }
  .sk-art { position: relative; justify-self: center; width: 100%; border-radius: var(--radius-xs); overflow: hidden; background: var(--color-surface-mist); box-shadow: 0 0 0 1px var(--color-line-base); }
  .sk-art--tall { width: min(100%, calc(var(--space-24) * 3)); }
  .sk-art--sq { width: min(100%, calc(var(--space-24) * 3.5)); }
  .sk-art--chk { background: repeating-conic-gradient(var(--color-surface-mist) 0 25%, var(--color-surface-card) 0 50%) 0 0 / var(--space-4) var(--space-4); }
  .sk-art img { display: block; width: 100%; height: auto; }
  .sk-art .sk-safe { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
  .sk-art--round { border-radius: 50%; }
  .sk-toggle { display: inline-flex; align-items: center; gap: var(--space-2); min-height: var(--size-tap-min); justify-self: start; font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); color: var(--color-text-strong); cursor: pointer; }
  .sk-toggle input { width: var(--space-5); height: var(--space-5); accent-color: var(--color-brand-deep-teal); }
  .sk-asset:has(.sk-toggle input:not(:checked)) .sk-safe, .sec:has(> .sk-toggle input:not(:checked)) .sk-safe { display: none; }
  .sk-ctx { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); gap: var(--space-6); align-items: end; padding: var(--space-6); border-radius: var(--radius-card); background: var(--color-surface-mist); }
  .sk-ctx--even { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .sk-ctx figure { margin: 0; display: grid; gap: var(--space-2); justify-items: center; min-width: 0; }
  .sk-ctx figcaption { justify-self: stretch; color: var(--color-text-secondary-on-mist); font: var(--type-desktop-caption-weight) var(--type-desktop-caption-size) / var(--type-desktop-caption-line) var(--font-family-sans); }
  .sk-ctx figcaption b { color: var(--color-text-strong); font-weight: 600; }
  .sk-phone { position: relative; width: min(100%, calc(var(--space-24) * 3.25)); aspect-ratio: 390 / 844; border: var(--space-2) solid var(--color-brand-teal-deep); border-radius: calc(var(--radius-card) * 2.5); overflow: hidden; background: var(--color-surface-card); container-type: inline-size; }
  .sk-phone--dark { background: var(--color-brand-teal-deep); }
  .sk-desk { position: relative; width: 100%; border: 1px solid var(--color-line-mid); border-radius: var(--radius-small); overflow: hidden; background: var(--color-surface-card); container-type: inline-size; }
  .sk-desk::before { content: ""; display: block; height: var(--space-6); border-bottom: 1px solid var(--color-line-base); background: radial-gradient(circle, var(--color-line-mid) 0 calc(var(--space-1) * 1.25), transparent 0) var(--space-2) 50% / var(--space-4) var(--space-4) no-repeat, radial-gradient(circle, var(--color-line-mid) 0 calc(var(--space-1) * 1.25), transparent 0) var(--space-6) 50% / var(--space-4) var(--space-4) no-repeat, radial-gradient(circle, var(--color-line-mid) 0 calc(var(--space-1) * 1.25), transparent 0) var(--space-10) 50% / var(--space-4) var(--space-4) no-repeat, var(--color-surface-paper); }
  .sk-crop { position: relative; overflow: hidden; width: 100%; }
  .sk-crop img { position: absolute; display: block; max-width: none; height: auto; }
  .sk-ui { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
  .sk-m { font-family: var(--font-family-sans); color: var(--color-text-strong); }
  .sk-bar { border-radius: var(--radius-pill); background: var(--color-line-base); }
  .sk-dot { border-radius: 50%; overflow: hidden; background: var(--color-surface-mist); flex: none; }
  .sk-dot img { display: block; width: 100%; height: 100%; }
  .sk-tag { display: inline-block; padding: 0 var(--space-2); border-radius: var(--radius-pill); background: var(--color-surface-wash-yellow); color: var(--color-brand-teal-deep); font: var(--type-desktop-label-weight) var(--type-desktop-label-size) / var(--type-desktop-label-line) var(--font-family-sans); }
  .sk-strip { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: var(--space-3); }
  .sk-strip figure { margin: 0; display: grid; gap: var(--space-2); align-content: start; min-width: 0; }
  .sk-strip img { display: block; width: 100%; height: auto; border-radius: var(--radius-xs); box-shadow: 0 0 0 1px var(--color-line-base); }
  .sk-strip figcaption { font: var(--type-desktop-fine-weight) var(--type-desktop-fine-size) / var(--type-desktop-fine-line) var(--font-family-sans); color: var(--color-text-secondary); }
  .sk-strip figcaption b { display: block; color: var(--color-text-strong); font-weight: 600; }
  .sk-board { display: grid; gap: var(--space-3); padding: var(--space-4); border-radius: var(--radius-card); border: 1px solid var(--color-line-base); }
  .sk-board > b { color: var(--color-text-strong); }
  .sk-copy { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-4); }
  .sk-copy .rule p + p { margin-top: var(--space-2); }
  .sk-copy q { quotes: none; display: block; padding: var(--space-3) var(--space-4); border-radius: var(--radius-small); background: var(--color-surface-paper); border: 1px solid var(--color-line-base); color: var(--color-text-strong); white-space: pre-line; }
  .sk-num { counter-reset: skr; display: grid; gap: var(--space-3); margin: 0; padding: 0; list-style: none; }
  .sk-num li { counter-increment: skr; display: grid; grid-template-columns: var(--space-10) minmax(0, 1fr); gap: var(--space-3); align-items: start; }
  .sk-num li::before { content: counter(skr, decimal-leading-zero); font: var(--type-desktop-card-weight) var(--type-desktop-card-size) / var(--type-desktop-card-line) var(--font-family-sans); color: var(--color-text-secondary); }
  .sk-num b { color: var(--color-text-strong); }
  .sk-files td:first-child { overflow-wrap: anywhere; }
  @media (max-width: 1023px) {
    .sk-spec { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .sk-ctx, .sk-ctx--even { grid-template-columns: minmax(0, 1fr); justify-items: center; }
    .sk-ctx > figure { width: 100%; }
    .sk-strip { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .sk-pair--3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (max-width: 767px) {
    .sk-pair, .sk-pair--3, .sk-copy { grid-template-columns: minmax(0, 1fr); }
    .sk-opt { grid-row: auto; grid-template-rows: none; }
    .sk-spec { grid-template-columns: minmax(0, 1fr); }
    .sk-ctx { padding: var(--space-4); }
    .sk-asset > h3 { font-size: var(--type-mobile-section-size); line-height: var(--type-mobile-section-line); }
    .sk-files thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
    .sk-files table, .sk-files tbody, .sk-files tr, .sk-files td { display: block; width: 100%; }
    .sk-files tr { padding: var(--space-3) 0; border-bottom: 1px solid var(--color-line-base); }
    .sk-files td { border-bottom: 0; padding: var(--space-1) var(--space-4); }
    .sk-files td[data-label]::before { content: attr(data-label) ": "; font-weight: 600; color: var(--color-text-strong); }
  }
"""


def esc(s):
    return html.escape(s, quote=True)


def crop_img(src, full_w, full_h, x, y, w, h, alt="", cls="sk-crop", extra_style=""):
    """Show the (x, y, w, h) region of a full_w x full_h image, scaled to the container width."""
    return (f'<div class="{cls}" style="aspect-ratio: {f(w)} / {f(h)};{extra_style}">'
            f'<img src="{esc(src)}" alt="{esc(alt)}" loading="lazy" style="width: {f(full_w / w * 100)}%; '
            f'left: {f(-x / w * 100)}%; top: {f(-y / h * 100)}%;"></div>')


def spec_dl(items):
    return '<dl class="sk-spec">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in items) + "</dl>"


def toggle(label="Show safe zones", checked=True):
    return (f'<label class="sk-toggle"><input type="checkbox"{" checked" if checked else ""}> {esc(label)}</label>')


def opt_fig(letter, line, prev, w, h, links, overlay_src=None, art_cls="", alt=""):
    ov = f'<img class="sk-safe" src="{esc(overlay_src)}" alt="" aria-hidden="true">' if overlay_src else ""
    lk = " · ".join(f'<a class="link" href="{esc(href)}" download>{esc(lab)}</a>' for lab, href in links)
    return (f'<figure class="sk-opt"><div class="sk-art {art_cls}"><img src="{esc(prev)}" width="{w}" height="{h}" '
            f'alt="{esc(alt or ("Option " + letter))}" loading="lazy">{ov}</div>'
            f'<figcaption><b>Option {letter}</b> · {line} {("· " + lk) if lk else ""}</figcaption></figure>')


# ---------------------------------------------------------------- vertical 9:16 frames (TikTok, Shorts)
LEGAL = "Assessment only. Not a diagnosis."


class V:
    """A 1080 x 1920 frame. safe = (x0, y0, x1, y1): the area no platform UI covers."""
    W, H = 1080, 1920

    def __init__(self, safe=(60, 160, 920, 1440)):
        self.x0, self.y0, self.x1, self.y1 = safe
        self.cx = (self.x0 + self.x1) / 2
        self.sw = self.x1 - self.x0


def seal_top(v, dark, y=None):
    y = v.y0 + 100 if y is None else y
    s, _, _ = logo("logo-seal-reversed" if dark else "logo-seal", v.x0 + 12, y, h=84)
    return s


def scrim_top(h=520):
    gid = uid("g")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["ink"]}" '
            f'stop-opacity="0.45"/><stop offset="1" stop-color="{C["ink"]}" stop-opacity="0"/></linearGradient>'
            f'<rect x="0" y="0" width="1080" height="{h}" fill="url(#{gid})"/>')


def caption_box(v, s, opt, y_bottom=None, size=50, kicker=None):
    """Lower caption: A = Paper box, radius 24, Teal Deep text; B = Deep Teal box, radius 12, Paper text."""
    y_bottom = v.y1 - 30 if y_bottom is None else y_bottom
    pad = 36
    lines = wrap(s, size, v.sw - 2 * pad, "sans", 600)
    kh = 44 if kicker else 0
    bh = block_h(len(lines), size, 1.2) + 2 * pad + kh + 8
    bw = min(v.sw, max(est(l, size, "sans", 600) for l in lines) + 2 * pad + 10)
    y = y_bottom - bh
    fill, tc, r = (C["paper"], C["teal_deep"], 24) if opt == "a" else (C["deep_teal"], C["paper"], 12)
    out = rect(v.x0, y, bw, bh, fill, r=r)
    ty = y + pad + size * 0.86
    if kicker:
        out += text(v.x0 + pad, y + pad + 26, kicker, 28, C["slate"] if opt == "a" else C["wash_blue"], "sans", 600, ls="0.04em")
        ty += kh
    out += text(v.x0 + pad, ty, lines, size, tc, "sans", 600, lh=1.2)
    return out, y


def vframe(kind, opt, d, v=None):
    """kind: cover, title, caption, form, placeholder, end. opt: 'a' (editorial) or 'b' (graphic).
    d: dict with text, sub, kicker, photo, fx, fy, n (frame number)."""
    v = v or V()
    t = d.get("text", "")
    b = []
    dark = False
    if kind == "cover":
        if opt == "a":
            b.append(rect(0, 0, 1080, 1920, C["paper"]))
            b.append(photo(d["photo"], 0, 860, 1080, 1060, d.get("fx", .5), d.get("fy", .35)))
            b.append(seal_top(v, False, 260))
            b.append(text(v.x0 + 12, 420, d.get("kicker", ""), 32, C["slate"], "sans", 600, ls="0.04em"))
            lines = wrap(t, 100, v.sw - 30)
            b.append(text(v.x0 + 12, 530, lines, 100, C["teal_deep"], lh=1.08))
        else:
            dark = True
            b.append(rect(0, 0, 1080, 1920, C["deep_teal"]))
            b.append(capsule(880, -150, 470, vertical=True, stroke=C["sky"], sw=20, inner=C["logo_blue"], gap=26))
            b.append(capsule(430, 1520, 900, stroke=C["sky"], sw=20))
            b.append(seal_top(v, True, 260))
            b.append(text(v.x0 + 12, 640, d.get("kicker", ""), 32, C["wash_blue"], "sans", 600, ls="0.04em"))
            lines = wrap(t, 124, v.sw - 30)
            b.append(text(v.x0 + 12, 790, lines, 124, C["paper"], lh=1.06))
    elif kind == "title":
        lines = wrap(t, 112 if opt == "a" else 124, v.sw - 30)
        size = 112 if opt == "a" else 124
        hgt = block_h(len(lines), size, 1.08)
        y = (v.y0 + v.y1) / 2 - hgt / 2 + size * 0.8 + 40
        if opt == "a":
            b.append(rect(0, 0, 1080, 1920, C["paper"]))
            b.append(capsule(-260, 1560, 820, stroke=C["line_base"], sw=20))
            b.append(seal_top(v, False))
            if d.get("kicker"):
                b.append(text(v.x0 + 12, y - size - 30, d["kicker"], 32, C["slate"], "sans", 600, ls="0.04em"))
            b.append(text(v.x0 + 12, y, lines, size, C["teal_deep"], lh=1.08))
            if d.get("sub"):
                b.append(text(v.x0 + 12, y + hgt + 30, wrap(d["sub"], 42, v.sw - 30, "sans"), 42, C["deep_teal"], "sans", 400, lh=1.35))
        else:
            dark = True
            b.append(rect(0, 0, 1080, 1920, C["deep_teal"]))
            b.append(capsule(-200, 1500, 760, stroke=C["sky"], sw=20, inner=C["logo_blue"], gap=26))
            b.append(capsule(820, -120, 420, vertical=True, stroke=C["sky"], sw=20))
            b.append(seal_top(v, True))
            if d.get("kicker"):
                b.append(text(v.x0 + 12, y - size - 30, d["kicker"], 32, C["wash_blue"], "sans", 600, ls="0.04em"))
            b.append(text(v.x0 + 12, y, lines, size, C["paper"], lh=1.06))
            if d.get("sub"):
                b.append(text(v.x0 + 12, y + hgt + 30, wrap(d["sub"], 42, v.sw - 30, "sans"), 42, C["paper"], "sans", 400, lh=1.35))
    elif kind == "caption":
        if opt == "a":
            dark = True
            b.append(photo(d["photo"], 0, 0, 1080, 1920, d.get("fx", .5), d.get("fy", .35)))
            b.append(scrim_top())
            b.append(seal_top(v, True))
            box, _ = caption_box(v, t, "a", kicker=d.get("kicker"))
            b.append(box)
        else:
            ground = C["mist"] if d.get("n", 1) % 2 else C["paper"]
            b.append(rect(0, 0, 1080, 1920, ground))
            b.append(capsule(560, 1560, 760, stroke=C["sky"], sw=20, inner=C["logo_blue"], gap=26))
            b.append(seal_top(v, False))
            b.append(photo(d["photo"], v.x0, 360, v.sw, 640, d.get("fx", .5), d.get("fy", .35), r=24))
            if d.get("kicker"):
                b.append(text(v.x0 + 12, 1110, d["kicker"], 32, C["slate"], "sans", 600, ls="0.04em"))
            lines = wrap(t, 84, v.sw - 30)
            b.append(text(v.x0 + 12, 1210, lines, 84, C["teal_deep"], lh=1.08))
    elif kind == "form":
        ground = C["paper"] if opt == "a" else C["mist"]
        b.append(rect(0, 0, 1080, 1920, ground))
        if opt == "b":
            b.append(capsule(600, 1560, 760, stroke=C["sky"], sw=20, inner=C["logo_blue"], gap=26))
        b.append(seal_top(v, False))
        lines = wrap(t, 84, v.sw - 30)
        b.append(text(v.x0 + 12, 470, lines, 84, C["teal_deep"], lh=1.08))
        cy = 470 + block_h(len(lines), 84, 1.08) + 70
        b.append(rect(v.x0, cy, v.sw, 560, C["card"], r=32, extra=f' stroke="{C["line_base"]}" stroke-width="2"'))
        b.append(rect(v.x0 + 40, cy + 40, 190, 44, C["mist"], r=22))
        b.append(text(v.x0 + 135, cy + 71, "DEMO ONLY", 22, C["teal_deep"], "sans", 600, anchor="middle", ls="0.06em"))
        b.append(text(v.x0 + 40, cy + 150, wrap(d.get("q", "Which state are you in right now?"), 44, v.sw - 80, "sans", 600), 44,
                      C["teal_deep"], "sans", 600, lh=1.25))
        for i, o in enumerate(("California", "New York", "Texas")):  # a neutral screen: the state question (never a symptom question)
            oy = cy + 230 + i * 104
            b.append(rect(v.x0 + 40, oy, v.sw - 80, 84, C["paper"], r=12, extra=f' stroke="{C["line_base"]}" stroke-width="2"'))
            b.append(f'<circle cx="{v.x0 + 86}" cy="{oy + 42}" r="14" fill="none" stroke="{C["slate"]}" stroke-width="3"/>')
            b.append(text(v.x0 + 124, oy + 55, o, 36, C["deep_teal"], "sans", 500))
    elif kind == "placeholder":
        ground = C["paper"] if opt == "a" else C["deep_teal"]
        dark = opt == "b"
        b.append(rect(0, 0, 1080, 1920, ground))
        b.append(rect(v.x0, 300, v.sw, 760, C["mist"], r=24, extra=f' stroke="{C["slate"]}" stroke-width="3" stroke-dasharray="16 12"'))
        b.append(text(v.cx, 640, ["Placeholder photo:", "a licensed provider at work,", "real and consenting"], 38, C["slate"], "sans", 500, anchor="middle", lh=1.3))
        b.append(seal_top(v, dark, 200))
        b.append(text(v.x0 + 12, 1210, wrap(t, 84, v.sw - 30), 84, C["teal_deep"] if opt == "a" else C["paper"], lh=1.08))
    elif kind == "end":
        line = d.get("text", "Discretion is part of the treatment.")
        sub = d.get("sub", "An online assessment, reviewed by a licensed provider.")
        if opt == "a":
            b.append(rect(0, 0, 1080, 1920, C["paper"]))
            b.append(logo("logo-seal", v.cx - 280, 380, w=560)[0])
            tc, sc, lc = C["teal_deep"], C["deep_teal"], C["slate"]
        else:
            dark = True
            b.append(rect(0, 0, 1080, 1920, C["deep_teal"]))
            b.append(capsule(-180, 1540, 820, stroke=C["sky"], sw=20))
            b.append(logo("logo-seal-reversed", v.cx - 280, 380, w=560)[0])
            tc, sc, lc = C["paper"], C["paper"], C["wash_blue"]
        lines = wrap(line, 76, v.sw - 40)
        b.append(text(v.cx, 720, lines, 76, tc, anchor="middle", lh=1.1))
        y = 720 + block_h(len(lines), 76, 1.1) + 60
        sl = wrap(sub, 38, v.sw - 60, "sans")
        b.append(text(v.cx, y, sl, 38, sc, "sans", 400, anchor="middle", lh=1.35))
        y += block_h(len(sl), 38, 1.35) + 70
        btn, _ = button(v.cx, y, "Get started", 120, 40, anchor="middle")
        b.append(btn)
        b.append(text(v.cx, y + 200, LEGAL, 34, lc, "sans", 500, anchor="middle"))
    return doc(1080, 1920, "".join(b))
