# unifiedmeds Brand Hub · changelog

## Edition 03 · update 16.11.2026 (review with Avi)
- Labels: the ground is the category (Sexual health Deep Teal, Longevity Forest, Hair loss Sky as a light label), the capsule colour is the product, and a capsule hue never repeats in the catalogue (U-13, U-14, R-96, R-97). New tokens `--color-category-*`; product colours updated, Sildenafil is now Coral #F4A38C.
- Buttons: full state set (Default, Hover, Pressed, Focus, Disabled proposed), one spec for desktop and mobile, and a second family with an icon on the right; eight UI icons in `assets/icons/ui/` (U-18, R-99, R-100).
- Alignment: cards in a row share one height and one action line; fixed rows on Brand, Components and Motion (U-17, R-98).
- Former brand removed from the published hub: archive link, archive folder, Figma URL slugs and wording; earlier editions are archived outside the hub, not deleted (U-16).
- Every page is hidden from search engines and stays open by link (U-15, R-102). Three logo stings approved (U-12, R-101).

## Edition 03 · update 15.11.2026 (buttons and labels)
- Buttons are rounded rectangles, not pills (U-11): radius 5 (`--radius-button`), padding 24 (`--size-button-padding-x`), height 50. The Dark button fills Teal-deep; labels on Yellow and Paper are Deep Teal; new Light button type. Source: Avi's Figma Button set 2676:310.
- Labels: R-89 rewritten from the Figma label master (2680:16): Deep Teal ground, reversed seal, vertical capsule in the product colour. Product images now show the unifiedmeds label.
- Yellow button hover: Blue-dark with a Paper label, confirmed by Avi (O-16 closed). Figma's Pastel Blue fails AA.

## unifiedmeds Brand Edition 03 · 15.11.2026.
The rebrand from SoviCare to unifiedmeds. Figma read on 15.11.2026: website file h7D0eRszARBaWdJT1NWrpZ and logo file VX5oKsl1ZIKbiWLR0tjf7L ("B · capsule seal"). Nothing in either Figma file was changed.
Decisions: U-01 to U-10, approved by Avi on 15.11.2026 (see brand-rules.md).
**Changed**
- Name: unifiedmeds, all lowercase, everywhere (U-01). "SoviCare Trio" becomes Combo (U-05).
- Logo: the capsule seal, with Primary seal, Horizontal and Stacked lockups, reversed versions, app icon and favicon (R-90 to R-94). Header logo 30px desktop, 26px mobile.
- Colour: new logo colour group, logo only (Navy #0F2E57, Ink #031D2C, Logo Blue #3976C6, Sky #C9DDEA, Cream #F1ECE0). New product colours (Tadalafil #9CC9E3, Sildenafil #3976C6, Combo #82CFCB). The website palette is unchanged (U-02).
- Shapes: the capsule joins the Quadrant Kit. It may be filled, outline or transparent, whole or cropped, and may crop a photo (U-03).
- Icons: a 12-icon line set built on the capsule.
- Catalogue and menu: launch with Sexual health and the short menu. Longevity and Hair loss are Phase 2 (U-04).
- Compliance: Longevity and Hair loss product pages carry "Legal review required" (U-06). Footer line "© 2026 unifiedmeds"; entity, domain and email to confirm (U-07).
- New chapter: packaging and labels (R-89).
**Unchanged from Edition 02**
- Website palette, type scale, layout, spacing, radius, buttons, fields, cards, motion, content and accessibility rules.
**Archived (not deleted)**
- Edition 02 is archived outside the published hub. Edition 01 stays on its own site.
Open items: O-01 to O-14 in brand-rules.md (legal details, tagline, product colours on the website, wordmark typeface, shape limits, icon size and colour, secondary logo versions, Light button hover, field states, Phase 2 menu wording, loader shape, assessment length and fee line, licensed photography, legal review of Phase 2 product pages).

---

# Earlier: SoviCare

## Brand Edition 02 · 08.10.2026

Figma version: live file `h7D0eRszARBaWdJT1NWrpZ` "SoviCare - Website", read 08.10.2026 (no named version yet — Avi is still editing it).
Tokens: `tokens/tokens.json` → `brand.css` (generated).
Decisions: 29 decisions approved by Avi on 08.10.2026, with three amendments (see `rulebook.html#decisions`).

**Changed**
- One token file (`tokens/tokens.json`) replaces brand.css, the handoff data, navigation.html and brand-rules.md as competing sources of values.
- Colour: Pastel palette from Figma. Blue #219EBC → #6E8B97, Green #2A9D8F → #6A8670, Mist #F2F7F9 → #E8E7E1 (alternate surface), Paper #FFFFFF → #FEFCF6 (the page), cool lines → warm lines (#EDEAE2 / #E3DFD5 / #C4BDAE). New: Blue-dark #4E6873, Teal-light #5F7075, washes, Card #FFFFFF.
- Accessibility: Yellow button hover → Blue-dark with Paper label (5.76:1); focus ring 2px Deep Teal (Paper on dark); links Deep Teal underlined; captions Slate, never Slate Light on light; field borders Slate (4.88:1).
- Type: Figma text styles 1:1 (desktop + mobile). Homepage hero 70/60 only; other heroes 46/54. Serif floor 24 desktop / 21 mobile. Labels sentence case. Italic highlight retired.
- Layout: 1440 / 390 frames, 1240 content, margins 100 / 40 / 20, 12 columns, breakpoints 390 / 768 / 1024 / 1440, spacing scale 4…96.
- Radius: pill 999, card 16, small 12, xs 8.
- Buttons: one height (50px), side padding = radius = height ÷ 2, Figma hover matrix, 2px lift. Exceptions: header 44, mobile bar 48.
- Motion: one principle; durations 150 / 220 / 320 / 420 / 520; easing ease-out (UI) + one enter curve (brand shapes); rise 12px; 24 motion cards.
- Navigation: Main menu v3 (Sexual health · How it works · FAQ · Sign in · Get started) and Footer v2 compact are the only patterns.
- Logo: symbol redrawn in the Pastel palette; wordmark "SoviCare"; backgrounds Paper / Mist / Deep Teal only.
- Content: primary CTA "Get started", sentence case; glossary (provider, assessment, member); required lines; privacy rules (no pixels on condition/product pages).

**Removed / retired**
- From the build guide: press strip, clinical stats count-up, reviews, star ratings, "Save 15%".
- Edition 01 motion: loops (except the loader), bounce/overshoot, Pivot fade, rolling odometer, 82px type.
- All Figma links to trashed files (Csrbx…, ILQVNp…, yimfrn…).

**Archived (not deleted)**
- All 42 Edition 01 pages, the old brand.css, brand-rules.md and README, the interactive showcase, demo scripts and Edition 01 photos → `archive/edition-01/`, each page with an "Archived" banner. Old URLs redirect via `404.html`.
- Longevity and Hair loss pages are archived as planned categories; they will return as new categories.

**Brand check:** `python3 tools/check.py` — passes for Edition 02 files.
**Exceptions:** E-01 mobile footer links 36px · E-02 header CTA 44px · E-03 mobile bar CTA 48px.
**Not in this edition (open items):** tagline choice · consultation fee · assessment length · Disabled/Loading button variants in Figma · Figma clean-up after Avi's edits (spacers, 72 vs 100 inset, wordmark, symbol colours, sentence-case CTAs, menu timings).

## Brand Edition 01 · 27.09 – 06.10.2026
"Meeting Review V1" (27.09), developer handoff (01.10), menu v3 navigation page (06.10). Archived in `archive/edition-01/`.
