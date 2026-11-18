# unifiedmeds Brand Hub

**Brand Edition 04.** One static site with every unifiedmeds rule, value, asset and output: the brand, the logo, the voice, the visual system, the website, the care journey (assessment, product screens, emails, packaging), marketing (social, ads, newsletter, videos, media kit) and the developer handoff. Published with GitHub Pages. The edition stamp on every page is written by the build from the top entry of `CHANGELOG.md`.

## Authority
The same order as on `how-we-work.html#authority` (R-01, R-02, R-121):
1. Decided rules and tokens win: `brand-rules.md` (rules, decisions, exceptions, open items) and `tokens/tokens.json` (every value).
2. `brand-rules.md` wins on wording and compliance. The pages explain and mirror the rules and never add one of their own.
3. The designer's Figma files (website and logo) are the source only for what is not decided yet. They are read and exported, never changed.
4. Our own Figma files (design system, website working copy, assessment working copy) are kept in sync with the rules.
5. A clinical or legal no stops any asset.

## Folders
| Folder or file | What it holds |
|---|---|
| `src/` | Page sources: an optional `<style>` block, then the page body. Edit these, never the root `*.html` |
| `*.html` (root) | Generated pages. Never edited by hand |
| `brand-rules.md` | Every rule (R-), decision (U-), exception (E-) and open item (O-) |
| `tokens/tokens.json` | Every value: colour, type, spacing, radius, size, shadow, motion |
| `brand.css` | CSS custom properties generated from the tokens. Never edited by hand |
| `components.css` | Reference components (buttons, fields, cards, chips, header, footer, overlay) |
| `hub.css`, `extended.css`, `hub.js`, `search-index.js` | The hub shell, its menu and search (`search-index.js` is generated) |
| `CHANGELOG.md` | What changed: rules and values, pages and assets |
| `assets/` | Every file the pages show or offer for download, one folder per subject (brand, icons, photos, social, ads, email, packaging, governance and more). `assets/photos/CREDITS.md` lists every photo and its licence |
| `lp/` | Landing pages, built as stand-alone HTML |
| `tools/` | Build and check scripts; `tools/images/` holds the Swift image tools used for packshots |
| `archive/` | Pages and files that left the site, with their path kept. Never linked as current |

## Build order
Run everything from this folder, in this order:
```
python3 -I tools/build_tokens.py    # tokens/tokens.json -> brand.css
python3 -I tools/build_rulebook.py  # brand-rules.md -> src/rulebook.html
python3 -I tools/build_pages.py     # src/*.html -> the root pages, menu, search index and redirects
python3 -I tools/check.py           # brand check: must print 0 problems
```
Page parts with their own generator (run the generator, then `build_pages.py`):
| Generator | Writes |
|---|---|
| `assets/assessment/build_assessment.py` | the assessment screens and parts of `src/assessment.html` |
| `assets/product-screens/page.py` (with `screens_*.py`) | `src/product-screens.html` |
| `tools/make_labels.py` | the labels inside `src/packaging.html` |
| `assets/governance/build_checklist.py` | `assets/governance/pre-publish-checklist.md` from the checklist on `src/how-we-work.html` |
| `assets/social/shared/make_social.py`, `build_kit_pages.py` | Facebook, Instagram and Threads, and X art, and their three kit pages |
| `assets/social/tiktok/make.py`, `youtube/make.py`, `linkedin/make.py` | the TikTok, YouTube and LinkedIn art and kit pages (`--page` rebuilds only the page) |

The art generators render PNG files with headless Google Chrome and read the logo files from `assets/brand/`.

## How a change travels
Two paths, both on `how-we-work.html#changes`:
1. A rule or a value: decision → `brand-rules.md` → tokens → changelog → release (R-78 to R-83). The release rebuilds the pages, runs `check.py` and brings our Figma files in line.
2. An asset: draft → brand check → clinical (if medical) → legal → final sign-off → publish → log (R-121; legal approves every social post, R-122), with the one coded pre-publish checklist (R-123).

## For developers
Link `brand.css` (and `components.css` if useful), use only `var(--…)` tokens, and read `handoff.html`. Never copy a value from a screenshot. Report with the four labels BUG, CHANGE, ADOPT and QUESTION (`how-we-work.html#feedback`).

## Publish
The site lives in the public repository `aviinbar5/unifiedmeds-brand-hub` on GitHub Pages (Settings → Pages → Deploy from a branch, `main`, `/ (root)`). `.nojekyll` is present, so every file is served as is.

There is no git remote on the working machine: files are uploaded with the GitHub web uploader, folder by folder, to the same path (`github.com/aviinbar5/unifiedmeds-brand-hub/upload/main/<folder>`). Upload only after `check.py` prints 0 problems. Wait for "Processing your files" to finish before leaving the page, or the commit is lost. Then compare the repository with this folder file by file.
