# unifiedmeds · brand-rules.md

**Brand Edition 03 · 15.11.2026 · Owner: Avi · Status: APPROVED by Avi 15.11.2026 (open items O-01 to O-14 stay To confirm)**
Supersedes Brand Edition 02 (08.10.2026, archived outside the published hub). Rule IDs R-01 to R-83 keep their Edition 02 numbers so every change can be traced. New rules start at R-84.

Status words: **Current** (decided, build it) · **Phase 2** (designed, ships after launch) · **To confirm** (open item, never ships as decided) · **Retired** (no longer applies).
Change marks: **[same]** unchanged from Edition 02 · **[changed]** rewritten in Edition 03 · **[new]** added in Edition 03.

## Edition 03 decisions (Avi, 15.11.2026)

| ID | Decision |
|---|---|
| U-01 | The brand name is written **unifiedmeds**, all lowercase, everywhere, including at the start of a sentence and in the footer. |
| U-02 | The website keeps its palette (Deep Teal and the Pastel set). The logo colours are a separate group, used by the logo only. |
| U-03 | Two shape families work together as needed: the Quadrant Kit and the capsule. The capsule may be filled, outline or transparent, shown whole or cropped. |
| U-04 | Launch: Sexual health only, with the short menu. Longevity and Hair loss follow right after launch (Phase 2). |
| U-05 | The third Sexual health product is **Combo**. "SoviCare Trio" is retired. |
| U-06 | Longevity and Hair loss product pages stay in the design, marked "Legal review required". R-65 still applies. |
| U-07 | Legal entity, domain and contact email are To confirm. The footer reads "© 2026 unifiedmeds". |
| U-08 | The new brand hub lives in a new GitHub repository, `unifiedmeds-brand-hub`, on GitHub Pages. |
| U-09 | The October Astro site code is a reference for the developer, who decides whether to reuse it. |
| U-10 | The Claude Design project "SoviCare Homepage Desktop V1" is archive only. |
| U-11 | Buttons are rounded rectangles (5px corners), not pills: the capsule shape belongs to the logo. Button and label values follow Avi's Figma (Button set 2676:310, Packaging 2678:2). |
| U-12 | 16.11.2026 · Three logo stings are approved: B (two halves), C1 (built from the u), C2 (built from u and m). |
| U-13 | 16.11.2026 · Labels: Avi's label master stays exactly as is; the ground is the category, the capsule colour is the product (R-96, R-97). |
| U-14 | 16.11.2026 · A capsule hue never repeats in the catalogue while it is small (R-97). |
| U-15 | 16.11.2026 · Both hubs open to anyone with the link, hidden from search engines (R-102). |
| U-16 | 16.11.2026 · Every trace of the former brand leaves the published hubs; earlier editions are archived outside them, never deleted. |
| U-17 | 16.11.2026 · Everything aligned and uniform: cards in a row share one height and one action line (R-98). |
| U-18 | 16.11.2026 · Buttons get the full state set and an icon-button family, in Figma and in the hub (R-99, R-100). |
| U-19 | 16.11.2026 · In every sticky header, on the website and on landing pages, the logo is taller than the call-to-action button. Mobile uses the Primary seal (R-103). |

---

## Rules

### Authority

- **R-01** [changed] Figma `h7D0eRszARBaWdJT1NWrpZ` (the website file, still named "SoviCare - Website" in Figma) wins on every visual value. The logo file `VX5oKsl1ZIKbiWLR0tjf7L`, page "B · capsule seal", wins on the logo. If the hub and Figma disagree, the hub is wrong and the hub is fixed.
- **R-02** [same] `brand-rules.md` wins on compliance and wording. The hub explains and mirrors both and never adds a rule of its own.
- **R-03** [same] Every value has one home: `tokens/tokens.json`. `brand.css` is generated from it and never edited by hand. No colour, size or duration outside the tokens.
- **R-04** [changed] This is Brand Edition 03 (15.11.2026), the first unifiedmeds edition. SoviCare Editions 01 and 02 are archived, never deleted and never linked as current.

### Brand and naming

- **R-05** [changed] unifiedmeds is a men's health telehealth brand that launches with Sexual health. Vibe: masculine, on the gentle side. · Source: U-04
- **R-06** [changed] Launch catalogue: Tadalafil, Sildenafil and Combo. Longevity and Hair loss are Phase 2 categories (designed in Figma, not linked as live at launch). Some future products will be for women (Planned). · Source: U-04, U-05
- **R-07** [changed] The name is **unifiedmeds** everywhere, all lowercase, also at the start of a sentence. Never "Unifiedmeds", "UnifiedMeds", "Unified Meds" or "UNIFIEDMEDS". The legal entity name is **To confirm**; until then no entity name appears in new material, and "SoviCare LLC" never appears. · Source: U-01, U-07
- **R-08** [same] The category is "Sexual health" in navigation and on the category page. "Better Intimacy" is used only as the editorial hero title.
- **R-09** [same] A tagline sits under the name. Until Avi chooses one, no tagline ships. **To confirm.**

### Colour

- **R-10** [same] Paper #FEFCF6 is the page. Mist #E8E7E1 is the alternate band and hero ground. Card #FFFFFF is for dropdowns and raised cards.
- **R-11** [same] Yellow #FFBE0B may be a CTA, a hover or a step marker, at most one Yellow element per viewport. Never a section background, never text.
- **R-12** [same] Pastel Blue #6E8B97 is for shapes and surfaces only, never behind a label. Blue-dark #4E6873 is the Yellow button hover fill, with a Paper label (5.76:1).
- **R-13** [same] Text on light surfaces: body Deep Teal, headlines Teal Deep #1C3742, captions and labels Slate #55747F (on Mist and washes Blue-dark). Slate Light #7E9AA6 never sits on a light surface.
- **R-14** [same] Links are Deep Teal #264653 and underlined.
- **R-15** [changed] Coral #E76F51 marks errors and out-of-range results only, always with an icon, never as a text colour. Clay #CFC6B8 is for posters only, never website UI. Packaging follows R-89. · Source: Figma 2678:2
- **R-16** [same] Pastel Green #6A8670 is for shapes, in-range markers and icons. Never text.
- **R-17** [same] There is no dark mode for now.
- **R-84** [new] Logo colours are a separate token group used **only** by the logo, the app icon and the favicon: Navy #0F2E57, Ink #031D2C, Sky #C9DDEA, Logo Blue #3976C6, Cream #F1ECE0, plus White. They never colour website UI, text, buttons or sections. · Source: U-02, Figma VX5o 5:7
- **R-85** [changed] Product colours identify a product on labels and packaging (16.11.2026): Tadalafil Sky #9CC9E3, Sildenafil Coral #F4A38C, Combo Aqua #82CFCB, PT-141 Lime #CFE08F, NAD+ Capsules Ice #E6EEF2, NAD+ Injection Orchid #E7A6D9, Metformin Sand #E9CC98, Finasteride Violet #5B4A9E, Hair Growth Green #2E7D4F. Tokens `--color-product-*`. Use on the website (for example product cards) is **To confirm** (O-03). · Source: U-13, U-14

### Type

- **R-18** [same] Two typefaces: DM Serif Display (Regular only) and Inter (400 to 700). A monospace face appears only on internal and code screens. The logo wordmark is artwork, not live type. It is drawn in Outfit Medium (from the logo sting source; confirmed by Avi 15.11.2026). Outfit is never used for website text.
- **R-19** [same] The hub copies Figma's text styles 1:1. No size outside the scale.
- **R-20** [same] Hero: 70/60 on the homepage only, 46/54 on every other page, mobile 34/40. Checked in Figma 15.11.2026: homepage 70/60, Sexual health 46.
- **R-21** [same] Serif floor: DM Serif never below 24px on desktop or 21px on mobile.
- **R-22** [same] Labels are sentence case, Inter SemiBold 12/16 +2% (mobile 11/16). No uppercase labels.
- **R-23** [same] No serif-italic highlight. Avi may re-open it.
- **R-24** [same] Sentence case for every heading, label, button and nav item. Section headlines end with a full stop and are never questions.
- **R-25** [same] Assessment questions are DM Serif 26/1.3 and may be questions.

### Layout

- **R-26** [same] Frames 1440 desktop and 390 mobile. Content max 1240. Side margins 100 desktop, 40 tablet, 20 mobile.
- **R-27** [same] 12 columns, 20px gutter. Breakpoints 390 / 768 / 1024 / 1440.
- **R-28** [same] Spacing scale only: 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 72, 96. Section padding 96 desktop, 56 mobile.
- **R-29** [same] Header 80px desktop, 64px mobile, desktop inset 56. Paper, sticky. A 1px Line/Soft border appears after 8px of scroll.

### Shape and imagery

- **R-30** [changed] Radius: buttons 5 (`--radius-button`); cards 16; fields, chips and the dropdown panel 12; menu rows and thumbnails 8; chips, nav pills and status pills 999 (`--radius-pill`). No other radius. The capsule is a shape (R-31), not a radius value. · Source: U-11, Figma 2676:310
- **R-31** [changed] Two shape families. **Quadrant Kit:** Square, Quarter, Half, Circle, Arch, Arc. **Capsule:** the logo's capsule form, in the variants Split, Split Blue, Outline and Vertical (Figma "Capsule Kit", 2678:2), plus the capsule as an image crop. Both families may appear on the website, as needed. No oval and no soft-cornered rectangle. · Source: U-03
- **R-32** [changed] A capsule may be filled, outline or transparent, and may be shown whole or cropped by the frame edge. Website pattern (Figma homepage, Avi 15.11.2026): a large outline capsule with a 20px stroke (`--size-capsule-stroke`) in Wash Blue at 70% opacity (`--opacity-capsule`), cropped by a section edge; vertical in dark sections; filled capsules at 50% (`--opacity-capsule-soft`). Quadrant pieces stay axis-aligned and may rotate only during their entrance. How many shapes per surface is still **To confirm**. · Source: U-03, Figma 2673:209
- **R-33** [changed] No text on a shape, ever. A disclaimer never sits on a shape. A photo may be cropped to a capsule.
- **R-34** [changed] Logo: see R-90 to R-94. The SoviCare quadrant symbol is Retired and kept only in the archive.
- **R-35** [changed] Icons: the unifiedmeds line set built on the capsule (12 icons, Figma 3042:221). 1.5px stroke, round caps, no fill, never Yellow. Drawn on a 64px grid. Placed sizes and icon colour on the website are **To confirm** (`GAP`: Figma places them at 40 and 48px; Foundations draws them in Navy, which R-84 reserves for the logo). · Source: Figma 3042:221
- **R-36** [same] The UI is flat, with borders. One shadow, for dropdowns and dialogs only.
- **R-37** [same] Photography: men aged 35 to 65 lead. Partners may appear in sexual-health stories. Women lead only in future women's products.
- **R-38** [same] Closed, branded bottles are allowed. Never loose pills, syringes, lab coats or before/after images. At most one faceless detail crop per page.
- **R-39** [same] Watermarked placeholder photos never ship. Replace them before launch. **To confirm.**

### Logo

- **R-90** [new] The logo is the **capsule seal**: "unified" (bold) in the filled half of a capsule, "meds" (regular) in the open half. Three lockups: Primary seal (where the brand needs presence), Horizontal (capsule icon + wordmark, the website navigation), Stacked (square spaces). In the header: the Horizontal lockup 52px tall on desktop, the Primary seal 50px tall on mobile (R-103); in the footer the Horizontal lockup 30px desktop and 28px mobile. · Source: Figma 3038:178, VX5o 5:80, Avi 15.11.2026
- **R-91** [new] On light grounds (Paper, Mist, Cream) use the main version in Navy. On dark grounds (Deep Teal, Ink, Navy) and on photography use the reversed versions only. The website footer uses Horizontal reversed. · Source: Figma 3038:211
- **R-92** [new] Clear space: the height of the "meds" half on every side. Never recolour individual parts, stretch, rotate, redraw or add effects. Use the exported files only.
- **R-93** [new] App icon and favicon: the "u|m" capsule on a Navy rounded square. Favicon sizes 48, 32 and 16; at 16px the capsule is solid. The favicon never uses the wordmark. · Source: VX5o 5:144
- **R-94** [new] The logo file also holds Scrubs green, Clinic sky, Black on white, White on black and Grey versions. Where each may be used is **To confirm**. Until then, only the versions in R-91 ship.
- **R-103** [new] In every sticky header, on the website and on landing pages, the logo is always taller than the call-to-action button next to it. The header button is 44px (`.btn--header`); the logo is the Horizontal lockup at 52px on desktop (`--size-logo-header-desktop`) and the Primary seal at 50px on mobile (`--size-logo-header-mobile`), because the Horizontal lockup at that height does not fit beside the button on a phone. Header heights stay 80 and 64. Never shrink the logo below the button to make room: shorten the navigation first. · Source: Avi 16.11.2026

### Components

- **R-40** [changed] Buttons are rounded rectangles, never pills: radius 5 (`--radius-button`), one height 50px (`--size-control`), side padding 24 (`--size-button-padding-x`), so width = label width + 48. Label Inter Medium 15/20, sentence case. Only logged exceptions differ in height (E-02, E-03). · Source: U-11, Figma 2676:310
- **R-41** [changed] Button types and hover (Figma 2676:310 and 2719:4438): Dark fills Teal-deep #1C3742 with a Paper label and hovers to Yellow; Outline (Teal-deep border) hovers to Yellow; Light (Paper fill) hovers to Yellow; Outline Light on Deep Teal hovers to Yellow, on photos to Blue-dark; Yellow hovers to Blue-dark with a Paper label. Labels on Yellow and Paper are Deep Teal #264653. On a Yellow, Blue or Wash surface every button hovers to Paper, and Light hovers to Deep Teal. Every button lifts 2px in 150ms ease-out. Figma draws the Yellow hover in Pastel Blue #6E8B97 (Paper label 3.53:1, fails AA); Avi confirmed Blue-dark on 15.11.2026 (R-12, R-72); Figma's Pastel Blue is on the clean-up list. · Source: U-11, D-08
- **R-42** [changed] Fields: 50px, radius 12, 1px Slate border. Selected: Deep Teal border plus a 1px inset, no scale. Disabled and Loading variants are still to be added in Figma. Progress mark (quadrant or capsule) **To confirm**.
- **R-43** [same] Cards: radius 16. Cards that are links fill Deep Teal with light text on hover, with no lift.
- **R-44** [same] Step numbers: on hover or tap the circle fills Yellow with dark digits.
- **R-45** [changed] Launch menu (Figma "short nav" 2738:2783, mobile 2743:3337): Sexual health ▾ · How it works · FAQ · Sign in · Get started. The dropdown lists Tadalafil, Sildenafil, Combo and "View all Sexual health". · Source: U-04, U-05
- **R-86** [new] Phase 2 menu (Figma "full nav" 2641:14411, dropdowns 2791:5681 to 2791:5709): adds Longevity and Hair loss, plus a Help dropdown. Its labels follow R-08 and R-24 (sentence case, "Sexual health" not "Better Intimacy"); the final wording is **To confirm** before Phase 2. · Source: U-04
- **R-46** [same] Menu behaviour: hover shows a Line/Soft pill (150ms). The dropdown opens on hover after a 100ms intent delay, or on click, Enter or ↓. One dropdown at a time. Esc closes it and returns focus.
- **R-47** [same] Mobile menu: ☰ in a 44×44 target opens a full-screen menu and locks body scroll. The bottom bar holds Get started and "Assessment only. Not a diagnosis."
- **R-48** [changed] Footer: Figma "Footer/Desktop" 2738:370 and "footer mobile" 2741:3169, with the CTA band 2738:1093 / 2741:3168. Deep Teal ground, logo Horizontal reversed.
- **R-98** [new] Alignment: elements in one row share one height; the action (button or link) sits at the bottom of every card on one line across the row; captions sit on one line; image galleries use one frame ratio per row. · Source: U-17
- **R-99** [new] Button states: Default, Hover, Pressed (hover colours, no lift), Focus (hover look plus the 2px ring), Disabled (**To confirm**, O-09). Mobile has no hover: a tap shows Pressed. Same spec on desktop and mobile: Inter Medium 15/20, height 50, padding 24, radius 5, border 1.5 inside; exceptions Header 44 and Mobile bar 48; tap target at least 44. · Source: U-18
- **R-100** [new] Buttons with an icon are a second family, never a replacement: same types, colours and states; one 20px icon on the right of the label, in the label colour, 8px gap, padding 24 on the label side and 20 on the icon side. The icon never replaces the label and is never Yellow. On hover the icon moves 2px in its direction (none with reduced motion). · Source: U-18

### Motion

- **R-49** [same] One principle: "Motion confirms, it never performs."
- **R-50** [same] Durations: 150 hover, press, select, focus · 220 open, close, slide, accordion, step · 320 reveal · 420 wipe · 520 shape · 1400 loader. No other duration.
- **R-51** [same] Easing: ease-out for every UI transition; the enter curve only for brand shapes entering.
- **R-52** [same] Brand moves: Rise 12px; Pivot 520ms, no fade; Wipe 420ms; stagger 90ms, three items at most; Count for results only.
- **R-53** [changed] Nothing loops on the website except the loader (1.4s). Loader shape (quadrant or capsule) **To confirm**. Hero: static copy plus one shape entrance.
- **R-54** [same] The hub's motion page is the only motion reference (M-001 to M-024).
- **R-101** [new] Logo stings: B is the default, C1 for brand and story moments, C2 for short social openers. One sting per video, at the start or the end, never in the middle. · Source: U-12

### Content

- **R-55** [same] The primary CTA is "Get started", in sentence case everywhere.
- **R-56** [same] US English. Plain, short sentences in the active voice.
- **R-57** [same] Glossary: provider (not doctor or clinician), assessment (not quiz or visit), member (not patient).
- **R-58** [same] A hero headline and subhead carry no benefit claim, price or symptom list.
- **R-59** [same] At most one normalising line per page, with no numbers.
- **R-60** [same] A number never appears bare: it carries its unit and, for results, its range. One assessment length everywhere. **To confirm.**
- **R-61** [same] No prices in heroes. Savings as a dollar amount per product, never a blanket "Save 15%".
- **R-62** [same] One consultation line everywhere: "Consultation included with treatment purchase. Otherwise, $25." **To confirm.**

### Compliance and privacy

- **R-63** [same] "Assessment only. Not a diagnosis." next to every assessment CTA above the fold, in the mobile menu bottom bar and on every assessment screen. Visible on load.
- **R-64** [same] Wherever a next step is offered, a licensed provider is named as responsible for it.
- **R-65** [same] Rx product names may appear in navigation and on product pages that carry safety information. Never in heroes or ads, and never next to a benefit claim.
- **R-87** [new] Longevity and Hair loss product pages (NAD+ Capsules, NAD+ injection, Metformin, Finasteride, Hair Growth Spray) carry the status **Legal review required** and do not ship until legal approves them. This replaces the earlier decision to remove drug names from Longevity. · Source: U-06
- **R-66** [same] Safety information on a product page is always fully expanded.
- **R-67** [same] No press strip, clinical statistics, success rates, reviews, testimonials, endorsements, certifications or star ratings until legal approves real data.
- **R-68** [same] No promised review or shipping time until operations confirm a service level.
- **R-69** [same] Illustrative medical content shows the DEMO ONLY notice. Never invent clinical rules or statistics.
- **R-70** [same] Assessment answers are collected only on the clinical intake domain.
- **R-71** [same] No tracking pixels, ad tags or session replay on condition or product pages.
- **R-88** [new] Footer legal line: "© 2026 unifiedmeds". Entity name, domain and contact email are added when confirmed. · Source: U-07

### Packaging

- **R-89** [changed] Labels follow the Figma label master (2680:16) on the bottle master "Bottle / Amber 360" (2680:89): the ground is the category colour (R-96); the primary seal small, reversed, top left; the product name in DM Serif Display, Paper; strength (Inter SemiBold) · form (Inter Regular); a thin divider; "Prescription treatment" and "Rx only" (Inter Regular); one vertical capsule cropped by the right edge, outlined in the product colour with its upper half filled (R-85). Clay is not used on labels. Combo label strength reads 100 mg in Figma: **To confirm**. · Source: Figma 2678:2, U-11
- **R-96** [new] Label ground per category: Sexual health Deep Teal #264653, Longevity Forest #2F5240, Hair loss Sky #BFD9EA. Hair loss is a light label: name, text, divider and seal in Deep Teal; the word "unified" in the seal always knocks out to the label ground. Tokens `--color-category-*`. · Source: U-13
- **R-97** [new] A capsule hue never repeats in the catalogue: "repeat" means the same hue family, not only the same hex. Past about 12 products a hue may repeat across categories but never within one. One product-name size per category (84, 79, 68 at the 560 master). Unknown strengths read "[DOSE]" until the clinical team confirms them. Every capsule keeps at least 3:1 against its ground. · Source: U-14

### Accessibility

- **R-72** to **R-77** [same] WCAG AA contrast, 2px Deep Teal focus ring (Paper on dark), 44×44 tap targets, hover also works with touch and keyboard, reduced motion is instant, no sideways scroll at 390px.
- **R-95** [new] The logo colours meet contrast in the versions in R-91. Any new logo pairing is checked for 3:1 before use.
- **R-102** [new] Every page of both hubs carries `<meta name="robots" content="noindex, nofollow">`: open to anyone with the link, never listed by search engines. · Source: U-15

### Governance

- **R-78** to **R-83** [same] A rule changes in this order: decision → `brand-rules.md` → tokens → changelog → release. No silent mismatches. Exceptions are logged before they ship. Open items are marked To confirm. A change to palette, type scale, layout or a rule's meaning opens a new edition.

---

## Exceptions log

| ID | Date | Scope | Rule | Exception | Status |
|---|---|---|---|---|---|
| E-01 | 05.10.2026 | Mobile footer links | R-74 | 36px tall, below 44px | Approved (carried from Edition 02) |
| E-02 | 08.10.2026 | Header CTA | R-40 | 44px instead of 50px | Approved (carried from Edition 02) |
| E-03 | 08.10.2026 | Mobile menu bottom bar CTA | R-40 | 48px, full width | Approved (carried from Edition 02) |

## Open items (To confirm)

| ID | Item | Rule |
|---|---|---|
| O-01 | Legal entity, domain, contact email | R-07, R-88 |
| O-02 | Tagline | R-09 |
| O-03 | Website use of product colours | R-85 |
| ~~O-04~~ | Closed 15.11.2026 (Avi): the wordmark is Outfit Medium | R-18 |
| O-05 | Shape limits and how Quadrant and capsule combine (opacity values set 15.11.2026) | R-32 |
| O-06 | Icon sizes and icon colour on the website | R-35 |
| O-07 | Secondary logo colour versions | R-94 |
| ~~O-08~~ | Closed 15.11.2026: Light hovers to Yellow; on Yellow, Blue or Wash it hovers to Deep Teal (Figma 3045:2714) | R-41 |
| O-09 | Disabled and Loading states; progress mark | R-42 |
| O-10 | Phase 2 menu wording | R-86 |
| O-11 | Loader shape | R-53 |
| O-12 | Assessment length; consultation fee line | R-60, R-62 |
| O-13 | Licensed photography | R-39 |
| O-14 | Legal approval of Longevity and Hair loss product pages | R-87 |
| ~~O-16~~ | Closed 15.11.2026 (Avi): the Yellow button hovers to Blue-dark #4E6873 with a Paper label (5.76:1). Figma's Pastel Blue stays on the clean-up list | R-41 |
| ~~O-15~~ | Closed 15.11.2026: logo height in the desktop header is 30px in both menus (`--size-logo-header-desktop`). Superseded 16.11.2026 by R-103: 52px. Figma short nav (45px) goes on the clean-up list | R-90 |
