# SoviCare — brand-rules.md

**Brand Edition 02 · 08.10.2026 · Owner: Avi**  
Supersedes Edition 01 (archived at `archive/edition-01/brand-rules.md`). Rendered on the hub as `rulebook.html`, with the decision log and open items.

## Authority order

1. Figma `h7D0eRszARBaWdJT1NWrpZ` ("SoviCare - Website") wins on every visual value.
2. `brand-rules.md` (this file) wins on compliance and wording.
3. The hub explains and mirrors both. If the hub and Figma disagree, the hub is wrong.

Values live in `tokens/tokens.json` and are generated into `brand.css`. This file holds the rules the values cannot express.

## How to use this file

- Attach `tokens/tokens.json` (or `brand.css`) and this file to any request to build a page, screen or asset.
- Build only from tokens. Cite rules by ID (R-01 …), decisions by ID (D-01 …), exceptions by ID (E-01 …).
- Status words: **Current** (decided, build it) · **Proposed** (waiting for Avi) · **Planned** (later, not built) · **To confirm** (open item).
- Where a decision is missing, ask. Do not improvise it.

---

## Rules

### Authority

- **R-01** Figma `h7D0eRszARBaWdJT1NWrpZ` ("SoviCare - Website") wins on every visual value. If the hub and Figma disagree, the hub is wrong and the hub is fixed. — Source: D-01
- **R-02** `brand-rules.md` (this rulebook) wins on compliance and wording. The hub explains and mirrors both and never adds a rule of its own. — Source: D-01
- **R-03** Every value has one home: `tokens/tokens.json`. `brand.css` is generated from it (`python3 -I tools/build_tokens.py`) and is never edited by hand. No colour, size or duration outside the tokens. — Source: D-01
- **R-04** This is Brand Edition 02 (08.10.2026). Superseded pages move to `/archive` with an "Archived" banner. They are never deleted and never linked as current. — Source: D-02

### Brand & naming

- **R-05** SoviCare is a men's health brand that launches with Sexual health. Vibe: masculine, on the gentle side. — Source: D-04
- **R-06** Launch catalogue: Tadalafil, Sildenafil and SoviCare Trio, until Avi adds more. Hair loss and Longevity are Planned categories, and some future products will be for women. Planned items keep the status "Planned" and are not built or linked as live. — Source: D-04
- **R-07** The name is "SoviCare" everywhere (legal entity SoviCare LLC). Never "Sovicare", "SOVICARE" or "sovicare". The product is "SoviCare Trio", never "Sync". — Source: D-05
- **R-08** The category is "Sexual health" in navigation and on the category page. "Better Intimacy" is used only as the editorial hero title. — Source: D-05
- **R-09** A tagline sits under the name. The options are Proposed and Avi chooses one. Until then, no tagline ships. **To confirm.** — Source: D-05

### Colour

- **R-10** Paper #FEFCF6 (`--color-surface-paper`) is the page. Mist #E8E7E1 (`--color-surface-mist`) is the alternate band and hero ground. Card #FFFFFF (`--color-surface-card`) is for dropdowns and raised cards. — Source: Figma 2719-4672
- **R-11** Yellow #FFBE0B (`--color-brand-yellow`) may be a CTA, a hover or a step marker, at most one Yellow element per viewport. Never a section background, never text. — Source: D-07
- **R-12** Pastel Blue #6E8B97 (`--color-brand-blue`) is for shapes and surfaces only, never behind a label. Blue-dark #4E6873 (`--color-brand-blue-dark`) is the Yellow button hover fill, with a Paper label (5.76:1). — Source: D-08
- **R-13** Text on light surfaces: body `--color-text-primary`, headlines `--color-text-strong`, captions and labels Slate #55747F (`--color-text-secondary`; on Mist and washes `--color-text-secondary-on-mist`). Slate Light #7E9AA6 (`--color-text-tertiary`) never sits on a light surface. — Source: D-09
- **R-14** Links are Deep Teal #264653 (`--color-text-link`) and underlined. — Source: D-09
- **R-15** Coral #E76F51 (`--color-brand-coral`) marks errors and out-of-range results only, always with an icon, never as a text colour. Clay #CFC6B8 (`--color-brand-clay`) is for packaging and posters only, never website UI. — Source: D-10
- **R-16** Pastel Green #6A8670 (`--color-brand-green`) is for shapes, in-range markers and icons. Never text. — Source: D-08
- **R-17** There is no dark mode for now. — Source: D-29

### Type

- **R-18** Two typefaces: DM Serif Display (`--font-family-serif`, Regular only) and Inter (`--font-family-sans`, 400 to 700). A monospace face appears only on internal and code screens. — Source: D-14
- **R-19** The hub copies Figma's text styles 1:1 (`typography.*` tokens, `--type-desktop-*` and `--type-mobile-*`). No size outside the scale. — Source: D-12
- **R-20** Hero: 70/60 (`--type-desktop-hero-home-*`) on the homepage only. 46/54 (`--type-desktop-hero-*`) on every other page. Mobile hero 34/40 (`--type-mobile-hero-*`). — Source: D-12
- **R-21** Serif floor: DM Serif never below 24px on desktop (`--type-desktop-card-serif-size`) or 21px on mobile (`--type-mobile-card-serif-size`). — Source: D-12
- **R-22** Labels are sentence case, Inter SemiBold 12/16 +2% (`--type-desktop-label-*`; mobile 11/16, `--type-mobile-label-*`). No uppercase labels and no Yellow marker. — Source: D-13
- **R-23** The serif-italic highlight is not used in Edition 02 (Figma sets "yourself" upright). Avi may re-open it. — Source: D-13
- **R-24** Sentence case for every heading, label, button and nav item. Section headlines end with a full stop and are never questions. — Source: D-06, Edition 01
- **R-25** Assessment questions are DM Serif 26/1.3 (`--type-desktop-h3-*`). Assessment questions and picker prompts may be questions, because they are part of the assessment. — Source: D-14

### Layout

- **R-26** Frames: 1440 desktop and 390 mobile (`--layout-frame-desktop`, `--layout-frame-mobile`). Content max 1240 (`--layout-content-max`). Side margins: 100 desktop (`--layout-margin-desktop`), 40 tablet (`--layout-margin-tablet`), 20 mobile (`--layout-margin-mobile`). — Source: D-03
- **R-27** Grid: 12 columns (`--layout-columns`) with a 20px gutter (`--layout-gutter`). Breakpoints 390 / 768 / 1024 / 1440 (`--layout-breakpoint-*`). — Source: D-03
- **R-28** Spacing comes from the scale only: 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 72, 96 (`--space-1` to `--space-24`). Section padding 96 desktop (`--layout-section-y`), 56 mobile (`--layout-section-y-mobile`). — Source: D-03
- **R-29** Header: 80px desktop (`--size-header-desktop`), 64px mobile (`--size-header-mobile`), desktop inset 56 (`--layout-header-inset`). Paper, sticky. A 1px Line/Soft border (`--color-line-soft`) appears after 8px of scroll. — Source: D-19

### Shape & imagery

- **R-30** Radius: cards 16 (`--radius-card`); fields, chips and the dropdown panel 12 (`--radius-small`); menu rows and thumbnails 8 (`--radius-xs`); buttons and pills 999 (`--radius-pill`). No other radius. — Source: D-16
- **R-31** Quadrant Kit: six pieces only, Square, Quarter, Half, Circle, Arch and Arc. No capsule, no oval, no soft-cornered rectangle. — Source: D-17, Edition 01
- **R-32** At most two kit pieces per surface. Solid fills only, no ghost opacity. Pieces stay axis-aligned and may rotate only during their entrance. — Source: D-17
- **R-33** No text on a kit piece, ever. A disclaimer never sits on a shape. — Source: D-17
- **R-34** The logo sits on Paper, Mist or Deep Teal only. The symbol's blue and green pieces are Pastel Blue (`--color-brand-blue`) and Pastel Green (`--color-brand-green`). Use the files in `assets/brand/`, never a redraw. The favicon is the symbol only, never the wordmark. — Source: D-11, Edition 01
- **R-35** Icons: 24px line (`--size-icon`), 1.5px stroke (`--size-icon-stroke`), round caps, no fill, never Yellow. — Source: D-18
- **R-36** The UI is flat, with borders. One shadow, `--shadow-overlay`, for dropdowns and dialogs only. — Source: D-18
- **R-37** Photography: men aged 35 to 65 lead. Partners may appear in sexual-health stories. Women lead only in future women's products (Planned). — Source: D-24
- **R-38** Closed, branded bottles are allowed. Never loose pills, syringes, lab coats or before/after images. At most one faceless detail crop per page. — Source: D-24
- **R-39** Watermarked placeholder photos (Unsplash+) never ship. Replace them before launch. **To confirm.** — Source: D-24

### Components

- **R-40** Buttons have one height, 50px (`--size-control`). Side padding = radius = height ÷ 2, so the label starts where the left curve ends and ends where the right curve begins. Width = label width + one button height. Label Inter Medium 15/20 (`--type-desktop-button-*`). Only logged exceptions differ (E-02, E-03). — Source: D-30
- **R-41** Button hover (Figma 2676-309): Dark to Yellow; Outline to Yellow; Yellow to Blue-dark with a Paper label; Outline Light on Deep Teal to Yellow; Outline Light on photos fills Blue-dark; any button on a Yellow, Blue or Wash surface to White. Every button lifts 2px (`--motion-distance-lift`) in 150ms ease-out. — Source: D-08, D-30
- **R-42** Fields: 50px (`--size-control`), radius 12 (`--radius-small`), 1px Slate border (`--color-line-field`, passes 3:1). Selected: Deep Teal border plus a 1px inset, no scale. Progress: the quadrant mark. Disabled and Loading variants are still to be added in Figma. **To confirm.** — Source: D-15
- **R-43** Cards: radius 16 (`--radius-card`). Cards that are links fill Deep Teal (`--color-brand-deep-teal`) with light text (`--color-text-on-dark`) on hover, with no lift. — Source: D-16
- **R-44** Step numbers: on hover or tap the circle fills Yellow with dark digits (`--color-brand-teal-deep`). — Source: Avi 07.10.2026
- **R-45** Main menu v3: Sexual health ▾ · How it works · FAQ · Sign in · Get started. The dropdown lists Tadalafil, Sildenafil, SoviCare Trio and "View all Sexual health". No other menu option is built. — Source: D-19
- **R-46** Menu behaviour: nav item hover shows a Line/Soft pill (150ms). The dropdown opens on hover after a 100ms intent delay (`--motion-intent-delay`) or on click, Enter or ↓. One dropdown at a time. Esc closes it and returns focus. — Source: D-19
- **R-47** Mobile menu: ☰ in a 44×44 target opens a full-screen menu and locks body scroll. The bottom bar holds Get started (full width) and "Assessment only. Not a diagnosis." — Source: D-19
- **R-48** Footer: Footer v2 compact (Figma 2719-4253, mobile 2719-4343). — Source: E-01

### Motion

- **R-49** One principle: "Motion confirms, it never performs." — Source: D-20
- **R-50** Durations: fast 150 (`--motion-duration-fast`) for hover, press, select and focus; open 220 (`--motion-duration-open`) for open, close, slide, accordion and step; reveal 320; wipe 420; shape 520; loader 1400. No other duration. — Source: D-20
- **R-51** Easing: `--motion-easing-ui` (ease-out) for every UI transition. `--motion-easing-enter` only for brand shapes entering. Press equals hover at 150ms. — Source: D-20
- **R-52** Brand moves: Rise 12px (`--motion-distance-rise`); Pivot 520ms, no fade; Wipe 420ms, straight edge; stagger 90ms (`--motion-stagger`), three items at most; Count for results only, right to left, never a rolling odometer. — Source: D-21
- **R-53** Nothing loops on the website except the quadrant loader (1.4s). Hero: static copy plus one shape entrance. Assessment step change: rise only, 220ms. Documentation demos play once, with Replay. — Source: D-22
- **R-54** The hub's motion page is the only motion reference: the 24-card M-set, M-001 to M-024, built on tokens. Dead Figma motion links are removed. — Source: D-23

### Content

- **R-55** The primary CTA is "Get started", in sentence case everywhere. The Edition 01 rule "Start with answers is never reworded" is retired. — Source: D-06
- **R-56** US English. Plain, short sentences in the active voice. Sentences take a full stop. — Source: D-27, Edition 01
- **R-57** Glossary: provider (not doctor or clinician), assessment (not quiz or visit), member (not patient). — Source: D-27
- **R-58** A hero headline and subhead carry no benefit claim, price or symptom list. Experiences are described in plain words below the hero, not in it. — Source: D-27, Edition 01
- **R-59** At most one normalising line per page, with no numbers. — Source: D-27
- **R-60** A number never appears bare: it carries its unit and, for results, its range. One true assessment length is used everywhere. **To confirm.** — Source: D-27, Edition 01
- **R-61** No prices in heroes. Savings are shown as a dollar amount per product, never a blanket "Save 15%". — Source: D-26
- **R-62** One consultation line everywhere. Current Figma copy: "Consultation included with treatment purchase. Otherwise, $25." **To confirm.** — Source: D-26

### Compliance & privacy

- **R-63** "Assessment only. Not a diagnosis." appears next to every assessment CTA above the fold, in the mobile menu bottom bar and on every assessment screen. It is visible on load, never revealed by animation. — Source: Edition 01
- **R-64** Wherever a next step is offered, a licensed provider is named as the party responsible for it. This holds even when it costs the faster conversion. — Source: Edition 01
- **R-65** Rx product names may appear in navigation and on product pages that carry safety information. Never in heroes or ads, and never next to a benefit claim. — Source: D-25
- **R-66** Safety information on a product page is always fully expanded, never behind a toggle. — Source: Edition 01
- **R-67** No press strip, clinical statistics, success rates, reviews, testimonials, endorsements, certifications or star ratings until legal approves real data. Never a "Verified" label. — Source: D-25, Edition 01
- **R-68** No promised review or shipping time until operations confirm a service level. — Source: Edition 01
- **R-69** Every screen with illustrative medical content shows "DEMO ONLY — final wording, clinical logic and eligibility criteria require clinical/legal approval before production use." Even in a demo, never invent contraindication rules, diagnosis logic, eligibility thresholds or clinical statistics. — Source: Edition 01
- **R-70** Assessment answers are collected only on the clinical intake domain. The marketing site never collects health data. — Source: D-28
- **R-71** No tracking pixels, ad tags or session replay on condition or product pages. — Source: D-28

### Accessibility

- **R-72** Text meets WCAG AA: 4.5:1 for body text, 3:1 for large text and for UI boundaries. Field borders use `--color-line-field`; `--color-line-mid` is decorative only. — Source: D-08, D-15
- **R-73** Focus: a 2px Deep Teal ring (`--size-focus-width`, `--color-focus-ring`) at a 3px offset (`--size-focus-offset`); Paper on dark surfaces and photos (`--color-focus-ring-on-dark`). Never removed. — Source: D-09
- **R-74** Tap targets are at least 44×44 (`--size-tap-min`). Smaller targets ship only as logged exceptions (E-01). — Source: Edition 01
- **R-75** Everything that works on hover also works with touch and keyboard. Menu triggers are buttons with `aria-expanded` and `aria-controls`. — Source: D-19
- **R-76** With `prefers-reduced-motion: reduce`, every state appears instantly and menus open and close instantly. The motion tokens drop to 0 in `brand.css`. — Source: D-20
- **R-77** No page scrolls sideways at 390px. Wide tables scroll inside their own container. — Source: D-03

### Governance

- **R-78** A rule changes in this order: decision (logged with ID, date and owner) → `brand-rules.md` → `tokens/tokens.json` (and `brand.css` rebuilt) → changelog entry → release. No step is skipped. — Source: D-01
- **R-79** No silent mismatches. When Figma, the hub and the website disagree, the gap is logged as an open item with an owner the same day. — Source: D-01
- **R-80** An exception is written in the Exceptions log (ID, date, scope, rule, reason, status) before it ships. An unlogged exception is a bug. — Source: D-30
- **R-81** A change to the palette, type scale, layout system or a rule's meaning opens a new edition. The previous edition moves to `/archive` with a banner. Smaller fixes are dated changelog entries within the edition. — Source: D-02
- **R-82** Anything not yet decided is marked "To confirm" and listed under open items. It never ships as if it were decided. — Source: D-01
- **R-83** Brand check before every release: `python3 -I tools/check.py` prints 0 problems. — Source: D-01

---

## Exceptions log

| ID | Date | Scope | Rule | Exception | Reason | Status |
|---|---|---|---|---|---|---|
| E-01 | 05.10.2026 | Mobile footer (Footer v2 compact, Figma 2719-4343) | R-74 | Footer links are 36px tall, below the 44px tap target. | Approved with Footer v2 compact on 05.10.2026. | Approved |
| E-02 | 08.10.2026 | Header CTA (Get started), desktop header | R-40 | Header CTA is 44px (`--size-control-exception-header`) instead of 50px; label 14px. | Figma menu v3 draws the header CTA at 43px; rounded up to the 44px tap target. | Approved |
| E-03 | 08.10.2026 | Mobile menu bottom bar | R-40 | Bottom-bar CTA is 48px (`--size-control-exception-mobile-bar`) and full width. | Figma menu v3 mobile bar (4046-911 in the archive copy). | Approved |

## Decision log and open items

The 30 decisions of 08.10.2026 (D-01 … D-30, owner Avi) and the open items (O-01 …) are listed on `rulebook.html`.
