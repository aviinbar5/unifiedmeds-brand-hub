"""Make product labels from Avi's Figma label (Packaging · Labels, 2680:38), exported as assets/packaging/label-template.svg.

Run from the repo root:  python3 -I tools/make_labels.py
Writes inline SVG labels into src/packaging.html between <!-- labels:start --> and <!-- labels:end -->.
Only the product name, the strength · form line and the capsule colour change. Everything else is the template.
Product colours for the launch products are approved tokens (R-85); the others are proposals until Avi approves them.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "assets/packaging/label-template.svg").read_text()
TEMPLATE_COLOUR = "#9CC9E3"

# The label capsule in the logo's true shape (R-105, Avi 17.11.2026). The Figma export draws it close to, but not
# exactly at, the logo proportions (width 149 on a 434.8 length = 34.3%, logo 35.8%; top half 92.8% of the bottom
# half's width, logo 93.3%). Redraw it with tools/capsule_svg.py on the same centre line: same top (240.18), same
# length (434.79), same centre (x 523.5), same stroke (14.3086) and the same 19.08 inset for the filled top half.
import sys  # noqa: E402
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import capsule_svg as cs  # noqa: E402

_CAP_LEN, _CAP_TOP, _CAP_CX, _CAP_SW, _CAP_INSET = 674.971 - 240.181, 240.181, 523.5, "14.3086", 19.078
_cap_x = _CAP_CX - cs.geometry(_CAP_LEN)["H"] / 2
_top_d, _bot_d, _ = cs.capsule_paths(_cap_x, _CAP_TOP, _CAP_LEN, vertical=True)
_fill_d = cs.capsule_paths(_cap_x, _CAP_TOP, _CAP_LEN, vertical=True, inset=_CAP_INSET)[0]
_old_caps = re.findall(r'<path d="M(?:592\.658 480\.04|598 480\.04|573\.58 309\.339)[^"]*"[^>]*/>\n', TEMPLATE)
assert len(_old_caps) == 3, "label template capsule paths not found"
TEMPLATE = TEMPLATE.replace(_old_caps[0], f'<path d="{_top_d}" stroke="{TEMPLATE_COLOUR}" stroke-width="{_CAP_SW}"/>\n')
TEMPLATE = TEMPLATE.replace(_old_caps[1], f'<path d="{_bot_d}" stroke="{TEMPLATE_COLOUR}" stroke-width="{_CAP_SW}"/>\n')
TEMPLATE = TEMPLATE.replace(_old_caps[2], f'<path d="{_fill_d}" fill="{TEMPLATE_COLOUR}"/>\n')

# Approved by Avi 16.11.2026: ground = category, capsule = product, a capsule hue never repeats in the catalogue.
CATEGORIES = {
    "Sexual health": {"ground": "#264653", "ink": "#FEFCF6", "size": 84, "light": False},
    "Longevity": {"ground": "#2F5240", "ink": "#FEFCF6", "size": 79, "light": False},
    "Hair loss": {"ground": "#BFD9EA", "ink": "#264653", "size": 68, "light": True},
}
PRODUCTS = [
    # (name, strength, form, capsule colour, category, phase)
    ("Tadalafil", "20 mg", "Tablets", "#9CC9E3", "Sexual health", "Launch"),
    ("Sildenafil", "100 mg", "Tablets", "#F4A38C", "Sexual health", "Launch"),
    ("Combo", "[DOSE]", "Tablets", "#82CFCB", "Sexual health", "Launch"),
    ("PT-141", "[DOSE]", "Injection", "#CFE08F", "Sexual health", "Planned"),  # not in the launch catalogue (R-06, U-21)
    ("NAD+", "[DOSE]", "Capsules", "#E6EEF2", "Longevity", "Phase 2"),
    ("NAD+", "[DOSE]", "Injection", "#E7A6D9", "Longevity", "Phase 2"),
    ("Metformin", "[DOSE]", "Tablets", "#E9CC98", "Longevity", "Phase 2"),
    ("Finasteride", "[DOSE]", "Tablets", "#5B4A9E", "Hair loss", "Phase 2"),
    ("Hair Growth", "[DOSE]", "Spray", "#2E7D4F", "Hair loss", "Phase 2"),
]




def label_svg(i, name, strength, form, colour, cat):
    c = CATEGORIES[cat]
    s = TEMPLATE
    s = re.sub(r'id="(clip\d+_2680_38)"', lambda m: f'id="{m.group(1)}_{i}"', s)
    s = re.sub(r'url\(#(clip\d+_2680_38)\)', lambda m: f'url(#{m.group(1)}_{i})', s)
    s = s.replace(TEMPLATE_COLOUR, colour)
    s = re.sub(r'<tspan x="48" y="439.442">Tadalafil</tspan>', f'<tspan x="48" y="439.442">{html.escape(name)}</tspan>', s)
    s = s.replace('font-size="84"', f'font-size="{c["size"]}"')
    # one flowing line for strength · form, so the dot follows the text width
    block = re.search(r'<g clip-path="url\(#clip3_2680_38_\d+\)">.*?</g>\n</g>\n', s, flags=re.S).group(0)
    line = (f'<text fill="#FEFCF6" xml:space="preserve" font-family="Inter" font-size="26" letter-spacing="0em" x="48" y="486.955">'
            f'<tspan font-weight="600">{html.escape(strength)}</tspan><tspan opacity="0.7"> · </tspan><tspan opacity="0.85">{html.escape(form)}</tspan></text>\n')
    s = s.replace(block, line)
    s = s.replace('<rect width="560" height="640" fill="#264653"/>', f'<rect width="560" height="640" fill="{c["ground"]}"/>')
    if c['light']:
        s = s.replace('#FEFCF6', c['ink'])
    # the word "unified" in the seal knocks out to the label ground
    s = re.sub(r'(<path d="M65\.7961 81\.2678[^"]*" fill=")[^"]*(")', lambda m: m.group(1) + c['ground'] + m.group(2), s)
    s = s.replace('<svg width="560" height="640"', f'<svg role="img" aria-label="{html.escape(name)} {html.escape(strength)} {html.escape(form)} label" width="560" height="640"', 1)
    return s


# Grouped by category (Avi 17.11.2026): one row per category, its ground colour named in the row head.
CAT_INFO = {
    "Sexual health": ("sexual-health", "Deep Teal ground", "Launch"),
    "Longevity": ("longevity", "Forest ground", "Phase 2"),
    "Hair loss": ("hair-loss", "Sky ground, light label", "Phase 2"),
}
def stage_line(cat, stage):
    rows = [p for p in PRODUCTS if p[4] == cat]
    planned = sum(1 for p in rows if p[5] == "Planned")
    if planned:
        return f"{stage} · {len(rows) - planned} products, {planned} planned"
    return f"{stage} · {len(rows)} products"


cards = []
for cat in CATEGORIES:
    slug, ground_name, stage = CAT_INFO[cat]
    items = []
    for i, (name, strength, form, colour, c2, phase) in enumerate(PRODUCTS):
        if c2 != cat:
            continue
        pill = ('<span class="status status--proposed">Planned · not at launch</span>' if phase == "Planned"
                else f'<span class="status status--current">Approved · {phase}</span>')
        items.append(f'''            <figure class="label-card">{label_svg(i, name, strength, form, colour, cat)}<figcaption class="cap">{pill}<b>{html.escape(name)} · {html.escape(form)}</b>capsule {colour}</figcaption></figure>''')
    cards.append(f'''          <div class="label-group label-group--{slug}">
            <div class="label-group-head"><span class="swatch" aria-hidden="true"></span><b>{cat}</b><span class="cap">{ground_name} {CATEGORIES[cat]['ground']} · {stage_line(cat, stage)}</span></div>
            <div class="labels-row">
{chr(10).join(items)}
            </div>
          </div>''')
block = "<!-- labels:start -->\n" + "\n".join(cards) + "\n          <!-- labels:end -->"
p = ROOT / "src/packaging.html"
t = p.read_text()
t = re.sub(r"<!-- labels:start -->.*?<!-- labels:end -->", lambda m: block, t, flags=re.S)
p.write_text(t)
print(f"{len(cards)} labels written")
