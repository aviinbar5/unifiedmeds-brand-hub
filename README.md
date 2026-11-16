# unifiedmeds Brand Hub

**Brand Edition 03 · 15.11.2026.** The design system and brand book for unifiedmeds. Static site, no build step: every page is plain HTML. Published with GitHub Pages.

## Authority
1. Figma `h7D0eRszARBaWdJT1NWrpZ` (website) wins on every visual value. Figma `VX5oKsl1ZIKbiWLR0tjf7L` ("B · capsule seal") wins on the logo.
2. `brand-rules.md` wins on compliance and wording.
3. This hub explains and mirrors both. If the hub and Figma disagree, the hub is wrong.

## Where things live
| What | File |
|---|---|
| Every value (colour, type, spacing, radius, size, shadow, motion) | `tokens/tokens.json` |
| CSS custom properties, generated, never edited by hand | `brand.css` (`python3 -I tools/build_tokens.py`) |
| Reference components (buttons, fields, cards, chips, overlay) | `components.css` |
| Rules, decisions, exceptions, open items | `brand-rules.md` · `rulebook.html` |
| What changed | `CHANGELOG.md` · `changelog.html` |
| Logo files (SVG, exported from Figma) | `assets/brand/` |
| Icon set (SVG, exported from Figma) | `assets/icons/` |
| Earlier editions | Archived outside the published hub, not deleted |

## For developers
Link `brand.css` (and `components.css` if useful), use only `var(--…)` tokens, and read `handoff.html`. Never copy hex values from screenshots.

## Publish on GitHub Pages
Settings → Pages → Source: **Deploy from a branch**, Branch `main`, Folder `/ (root)`. `.nojekyll` is present so every file is served as is.

## Change order
decision → `brand-rules.md` → `tokens/tokens.json` → pages → changelog entry.

## Before every release
```
python3 -I tools/build_tokens.py    # regenerate brand.css from tokens.json
python3 -I tools/build_rulebook.py  # regenerate rulebook.html from brand-rules.md
python3 -I tools/check.py           # brand check: 0 problems
```
