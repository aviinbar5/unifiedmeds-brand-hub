# SoviCare Brand Hub

**Brand Edition 02 · 08.10.2026.** Live at https://aviinbar5.github.io/sovicare-brand-hub/

## Authority
1. Figma `h7D0eRszARBaWdJT1NWrpZ` ("SoviCare - Website") wins on every visual value.
2. `brand-rules.md` wins on compliance and wording.
3. This hub explains and mirrors both. If the hub and Figma disagree, the hub is wrong.

## Where things live
| What | File |
|---|---|
| Every value (colour, type, spacing, radius, size, shadow, motion) | `tokens/tokens.json` |
| CSS custom properties, generated — never edit by hand | `brand.css` (`python3 tools/build_tokens.py`) |
| Reference components (buttons, fields, cards, chips, overlay) | `components.css` |
| Rulebook, exceptions log | `brand-rules.md` · `rulebook.html` |
| What changed | `CHANGELOG.md` · `changelog.html` |
| Hub pages | `index.html`, `brand.html`, `logo.html`, `content.html`, `foundations.html`, `components.html`, `motion.html`, `handoff.html` |
| Brand files | `assets/brand/` |
| Edition 01 (archived, not deleted) | `archive/edition-01/` · index: `archive/index.html` |

## Before every release
```
python3 tools/build_tokens.py   # regenerate brand.css from tokens.json
python3 tools/check.py          # brand check: no colour literals in styling, no broken links, no trashed Figma links, fonts
```
A change reaches the hub in this order: decision → rulebook → tokens → pages → changelog entry.
