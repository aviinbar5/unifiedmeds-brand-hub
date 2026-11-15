# SoviCare Brand Hub — changelog

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
