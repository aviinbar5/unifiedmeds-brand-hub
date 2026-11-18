"""Generate brand.css from tokens/tokens.json (unifiedmeds, Brand Edition 04).

Run from the project root:  python3 -I tools/build_tokens.py
brand.css is generated. Never edit it by hand: change tokens.json and run this again.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS = json.loads((ROOT / "tokens" / "tokens.json").read_text())

PREFIX = {"typography": "type"}  # group renames in CSS variable names
ALIAS = re.compile(r"^\{([^}]+)\}$")


def lookup(path):
    node = TOKENS
    for part in path.split("."):
        node = node[part]
    return node["$value"]


def font_stack(value):
    if isinstance(value, str) and ALIAS.match(value):
        value = lookup(ALIAS.match(value).group(1))
    return ", ".join(f"'{f}'" if " " in f else f for f in value)


def css_name(path):
    head, *rest = path
    return "--" + "-".join([PREFIX.get(head, head), *rest])


def css_value(token):
    value, kind = token["$value"], token.get("$type")
    if isinstance(value, str) and ALIAS.match(value):
        return "var(" + css_name(ALIAS.match(value).group(1).split(".")) + ")"
    if kind == "fontFamily":
        return font_stack(value)
    if kind == "cubicBezier":
        return "cubic-bezier(" + ", ".join(str(v) for v in value) + ")"
    return str(value)


def walk(node, path, out):
    for key, child in node.items():
        if key.startswith("$") or not isinstance(child, dict):
            continue
        if "$value" in child:
            name = css_name(path + [key])
            if child.get("$type") == "typography":
                v = child["$value"]
                out.append((name + "-family", font_stack(v["fontFamily"])))
                out.append((name + "-size", v["fontSize"]))
                out.append((name + "-weight", str(v["fontWeight"])))
                out.append((name + "-line", str(v["lineHeight"])))
                out.append((name + "-tracking", str(v["letterSpacing"])))
            else:
                out.append((name, css_value(child)))
        else:
            walk(child, path + [key], out)


lines = []
walk(TOKENS, [], lines)

# Reduced motion: every duration, distance, stagger and the fold-shape rotation drop to zero.
# The loader keeps its cycle (R-53); delays keep their value (nothing moves during a delay).
reduced = [n for n, _ in lines
           if n.startswith(("--motion-duration-", "--motion-distance-", "--motion-stagger", "--motion-drift-rotate"))
           and n != "--motion-duration-loader"]


def zero(name):
    if "-distance-" in name:
        return "0px"
    if name == "--motion-drift-rotate":
        return "0deg"
    return "0ms"

css = [
    "/* unifiedmeds brand tokens · Brand Edition 04 (from 18.11.2026)",
    "   GENERATED from tokens/tokens.json by tools/build_tokens.py. Do not edit by hand. */",
    "",
    ":root {",
    *[f"  {n}: {v};" for n, v in lines],
    "}",
    "",
    "@media (prefers-reduced-motion: reduce) {",
    "  :root {",
    *[f"    {n}: {zero(n)};" for n in reduced],
    "  }",
    "}",
    "",
]
(ROOT / "brand.css").write_text("\n".join(css))
print(f"brand.css: {len(lines)} variables, {len(reduced)} reduced-motion overrides")
