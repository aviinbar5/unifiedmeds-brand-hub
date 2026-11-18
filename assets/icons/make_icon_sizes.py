"""Feature icons at their placed sizes (q124, Avi 18.11.2026).

The 12 feature icons in this folder are drawn on a 64 grid with a 1.5 stroke, which is right when they
are placed at 64 (desktop). The stroke floor of 1.5 (R-109) applies to the line AS RENDERED, so the
48px placement (mobile) gets its own file: same drawing, width and height 48, every stroke-width
multiplied by 64 / 48, so it renders at 1.5 again. A stroke without a stroke-width (SVG default 1)
is scaled from 1 the same way.

    python3 -I assets/icons/make_icon_sizes.py      # writes assets/icons/sized/icon-*-48.svg

The UI glyphs (assets/icons/ui, 20 grid, 1.75) need no sized files: at 20 they render 1.75 and in a
24 box they render 2.1.
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
GRID = 64
PLACED = (48,)


def scaled(text, size):
    k = GRID / size

    def sw(m):
        return f'stroke-width="{float(m[1]) * k:g}"'
    text = re.sub(r'stroke-width="([0-9.]+)"', sw, text)
    # strokes with no stroke-width: the default is 1
    text = re.sub(r'(<path(?![^>]*stroke-width)[^>]*stroke="[^"]+")', lambda m: m[1] + f' stroke-width="{k:g}"', text)
    text = re.sub(r'<svg width="64" height="64"', f'<svg width="{size}" height="{size}"', text, count=1)
    return text


def main():
    out = HERE / "sized"
    out.mkdir(exist_ok=True)
    n = 0
    for src in sorted(HERE.glob("icon-*.svg")):
        for size in PLACED:
            (out / f"{src.stem}-{size}.svg").write_text(scaled(src.read_text(), size))
            n += 1
    print(f"wrote {n} files to {out}")


if __name__ == "__main__":
    main()
