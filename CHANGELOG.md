# unifiedmeds Brand Hub · changelog

Newest first. Two kinds of change: **Rules and values** (brand-rules.md and tokens) and **Pages and assets** (the hub's pages, files and tools). `changelog.html` is generated from this file by `tools/build_changelog.py`.

## Edition 04 · 18.11.2026 (one hub)
- The core hub and the extended hub are one site at one address, with one menu in seven groups (Start, Brand, System, Website, Care journey, Marketing, Build), every link internal.
- Search: pages, sections, rules, decisions, colours and files, with Hebrew words for every page (Cmd/Ctrl+K or "/").
- Merged pages: Brand book into Brand, Animations into Motion, Questionnaire patterns into Assessment, Approval and file naming into How we work. Old addresses forward to the new pages.
- One build for every page (tools/build_pages.py), and the brand check runs on every page.
- Edition 04 opens at the merge; later changes are dated updates of Edition 04 unless the palette or the type scale is replaced (U-31, R-04, R-83).
- Authority: decided rules and tokens win; the designer's Figma files are read only and the source only for what is not decided yet; our own Figma files are kept in sync with the rules (R-01). The hub adds no rule of its own; process rules are numbered (R-02).

**Rules and values**
- New: two dark bands never touch (R-119); copy beside a photo, on a solid colour panel or directly on the photo, with AA contrast on a quiet area and never over a face (R-120).
- Process rules, numbered (R-121 to R-129): who approves what, legal approves every social post, the two change paths and the one coded checklist, the Google Shared Drive and the approved folder, the approval log sheet, file naming and versions, archive never delete, data in the member portal, wrong examples stay.
- Decisions logged: governance and portal decisions of 17.11 (U-30), the hub merge, inbox q104 to q139 (U-31), the questionnaire, Q91 to Q102 (U-32).
- Exceptions: E-05, a state not served stops on screen 01 with Continue disabled and "Notify me" (Q96). E-01 retired: the footer uses 44px rows on mobile (R-114).
- Updated rules: the selected answer, single choice Deep Teal with the Yellow mark, multiple choice a border, and Continue stays active for a missing answer (R-42); assessment questions 26/1.3 on mobile too (R-25); assessment top bar 80 desktop, 64 mobile (R-29); product colours mark their product with a dot or an edge, never text or data (R-85, R-117); the footer on Mist with the Horizontal logo, its brand line, link list and legal page names (R-91, R-114); the product dropdown shows names only (R-45).
- Updated rules: the charge line placeholder "[charge line · operations]" (R-62); the assessment length placeholder (R-60); reviews only in the prototype format, DEMO ONLY and "Member · age" (R-67); consent before any analytics, the assessment included (R-71); "Learn more" on cards and "care team" in the glossary (R-55, R-57).
- Updated rules: durations add 180 crossfade and 40 stagger-fine, and the delays are listed (R-50); the loader is the capsule (R-53); the motion page covers stings, landing-page moments, drift and interactive states (R-54); stings end on Cream (R-101); the icon stroke floor applies to the line as rendered (R-35); one shape set in website colours (R-31); illustrations and patterns follow the R-109 stroke; photography sources (R-39).
- Open items: O-11 closed (the loader is the capsule), O-13 closed (Q91); new O-17 (approver names, medical content approver). Still open: O-01, O-02, O-10, O-12, O-14, O-17.
- Final batch: the assessment step model, Welcome and Email, seven steps, then provider review (R-130); the missing-answer pattern and the progress mark (R-42); checkbox 22px (R-30); copy on photos with measured contrast and the panel option (R-120); charge line and disclaimer placements (R-62, R-63); first-party assessment events need consent and carry screen IDs only (R-71); product page title is not a hero (R-65); lower-case generic names in running text (R-108); stamp inset 1.5% in exports (R-110); placed icon sizes and per-size files (R-35); the leaflet keeps "patient" (R-57); one-colour logo files (R-94); favicon 16 file (R-93).
- Tokens: new `chart` group (line, ring, markers, dot border, plot heights, hit area, Inter figures, refetch opacity; R-128); `size.capsule-stroke` and `size.capsule-divider-max` removed; `--motion-drift-rotate` drops to 0 with reduced motion; descriptions cite rule numbers.

**Pages and assets**
- The former brand's history leaves the published changelog: Editions 02 and 01 are kept in `archive/changelog-earlier-editions.md` (q115). The brand check now fails on the former brand name anywhere in the site.
- The changelog page is generated from this file (`tools/build_changelog.py`). Build order: tokens, rulebook, changelog, pages, check.
- The capsule loader everywhere (O-11 closed). Motion absorbs Animations; Assessment absorbs Questionnaire patterns, with the decided flow, the question template and the question schema; Brand absorbs the brand book, Imagery holds every photography rule, and the logo has two pages.
- How we work: one checklist, two change paths and the Figma files table. Downloads lists every file. Foundations shows the nine product colours and the category colours.
- Per-size icon files (`assets/icons/sized/`, `assets/icons-capsule/sized/`); one shape set in website colours, the Sky / Logo Blue set archived; spots and patterns redrawn to R-109; the 16px favicon; the sting end frame on Cream; the generators read tokens.json.
- Plans of 1, 3 and 6 months; the charge line is a placeholder until operations decides; the 18 earlier photos of unknown source replaced with credited stand-ins; microcopy for sign-in by email link, no password.

## Edition 03 · update 17.11.2026 night (answers 81 to 90)
- Mailer: the outside line "Packed with care, just for you." with a small outline capsule; welcome card greeting "Welcome to unifiedmeds." (U-29).
- Product screens: the recommendation wording, Wash Yellow flags and the app logo sizes are decided; clinical admin and support work fully on a phone (U-29).

**Pages and assets**
- Box and unboxing: the mailer line and the welcome card files redrawn (`assets/unboxing/`).
- Product screens: the clinical queue with filter chips and a mobile review frame with a sticky Sign button.

## Edition 03 · update 17.11.2026 evening (review and answers)
- Capsule: every capsule keeps the divider between its halves at every size, like the seal; the stroke scales at 0.85% of the length (U-26, R-109).
- Avi's review (U-25): capsule and the u|m logo stamp on photos (R-110), shapes in every fold with continuity and gentle scroll drift (R-111), adjacent buttons never the same colour (R-112), animated interactive states (R-113), the full footer (R-114), one accent per section (R-115), compact folds 64 / 48 (R-116).
- Avi's answers (U-27): category colours on category pages (R-117), logo minimum sizes (R-118), icons in Deep Teal (R-35, O-06 closed), hub-only exception for stand-in photos (R-39), assessment wording (R-57), checkout price exception (E-04).
- Avi's answers, second batch (U-28): product colours mark their product on the website (R-85, O-03 closed); only Black on white and White on black as secondary logo versions, for technical uses (R-94, O-07 closed); Disabled approved at 40% (R-42, O-09 closed); a fully filled capsule keeps a thin gap at the divider (R-109); checkboxes take radius 5 (R-30).
- Also in U-28: newsletter double opt-in with open tracking on; sender name unifiedmeds; the four big jobs (product screens, questionnaire, landing page rebrand, brand film and demos) go ahead.
- Decided on the pages the same day, logged at the merge as U-30: dose marking without streaks or scores, Yellow only for the next timeline step, Pastel Blue as the second chart series, big figures in Inter; files in a Google Shared Drive, approved files move to the approved folder, legal approves every social post, the approval log is a sheet.

**Pages and assets**
- New pages: Assessment flow, and Product screens rebuilt.
- UI glyphs: the 38 proposed glyphs joined the button icons, 46 in `assets/icons/ui/` on a 20px grid with a 1.75px stroke (tokens `--size-icon-glyph-*`). The capsule icon family became the website's working set (R-35, U-27).
- Capsule divider redrawn everywhere: pages, the landing page, masks, ads, the media kit and its ZIP, images, unboxing and social covers.
- Icons: colour matrix and six icon-motion demos. Media kit: branded images with the capsule and the stamp in four ratios. Imagery: shapes on photos and photos on a phone. Ads: formats by channel, best practice per channel, device mockups.

## Edition 03 · update 17.11.2026 (Avi's decisions)
- Capsule: always the logo's own proportions, never a symmetric pill (U-22, R-105). Page-head decor, capsule band, kit specimens, loaders, the 12 capsule icons and the shape files are redrawn from `tools/capsule_svg.py`.
- Launch products confirmed: Tadalafil, Sildenafil, Combo (U-21, R-06). New naming rule R-108: medicine names and plain descriptive names, never a reference brand.
- Shapes: two per surface at most (U-23, R-106). O-05 closed.
- Mobile gets equal treatment in every category, deliverable and element, checked at 1440 and 390 (U-24, R-107).

**Pages and assets**
- Capsule icon family: 96 icons, horizontal and standing (`assets/icons-capsule/`).
- Media kit page with a ZIP; Social overview and six channel kits, two options per asset, desktop and mobile; credited stand-in photos in empty slots, hub only.
- Brand architecture rewritten with the launch names; the landing page shows Tadalafil, Sildenafil and Combo, with bottles built from our labels.
- The logo story keeps the brief, the directions and the choice; sketches and early rounds archived.

## Edition 03 · update 16 to 17.11.2026 night (new pages)

**Pages and assets**
- New pages as proposals: Brand architecture, Brand in use, Illustration and patterns with spots and patterns (`assets/patterns/`), Sound with prototype sounds (`assets/sound/`), Newsletter, Box and unboxing, Data in the portal, Approval and file naming (`assets/governance/`). Landing pages now leads with the Sexual health landing page.
- 38 UI glyphs proposed (joined the core set on 17.11 evening).

## Edition 03 · update 16.11.2026 (review with Avi)
- Landing pages: up to three brand motion moments, each played once, scroll-driven where it tells a sequence, one desktop parallax at most, all off with reduced motion (U-20, R-104). First use: the Sexual health landing page.
- Header logo: in every sticky header, website and landing pages, the logo is taller than the call-to-action button (U-19, R-103). Desktop Horizontal lockup 52px, mobile Primary seal 50px; button 44.
- Labels: the ground is the category (Sexual health Deep Teal, Longevity Forest, Hair loss Sky as a light label), the capsule colour is the product, and a capsule hue never repeats in the catalogue (U-13, U-14, R-96, R-97). New tokens `--color-category-*`; product colours updated, Sildenafil is now Coral #F4A38C.
- Buttons: full state set (Default, Hover, Pressed, Focus, Disabled proposed), one spec for desktop and mobile, and a second family with an icon on the right; eight UI icons in `assets/icons/ui/` (U-18, R-99, R-100).
- Alignment: cards in a row share one height and one action line; fixed rows on Brand, Components and Motion (U-17, R-98).
- Former brand removed from the published hub: archive link, archive folder, Figma URL slugs and wording; earlier editions are archived outside the hub, not deleted (U-16).
- Every page is hidden from search engines and stays open by link (U-15, R-102). Three logo stings approved (U-12, R-101).

**Pages and assets**
- Approved in the page-by-page review: Videos, Animations, Social, Packaging, Website pages, Section library, Landing pages, Product screens, Templates and Ads (with more formats, photo layouts, a Reels storyboard and UGC templates).
- New: feedback and states in Components, Questionnaire patterns, System emails (`assets/email/`), the microcopy library (`assets/content/microcopy.json`), Downloads with "View in Figma" and download buttons on every asset section.
- The Sexual health landing page (`lp/sexual-health.html`), option A, approved.
- Social: the profile picture in six colours plus four concepts; covers for four platforms.

## Edition 03 · update 15.11.2026 (buttons and labels)
- Buttons are rounded rectangles, not pills (U-11): radius 5 (`--radius-button`), padding 24 (`--size-button-padding-x`), height 50. The Dark button fills Teal-deep; labels on Yellow and Paper are Deep Teal; new Light button type. Source: Avi's Figma Button set 2676:310.
- Labels: R-89 rewritten from the Figma label master (2680:16): Deep Teal ground, reversed seal, vertical capsule in the product colour. Product images now show the unifiedmeds label.
- Yellow button hover: Blue-dark with a Paper label, confirmed by Avi (O-16 closed). Figma's Pastel Blue fails AA.

## unifiedmeds Brand Edition 03 · 15.11.2026
The rebrand to unifiedmeds, the first unifiedmeds edition. Figma read on 15.11.2026: website file h7D0eRszARBaWdJT1NWrpZ and logo file VX5oKsl1ZIKbiWLR0tjf7L ("B · capsule seal"). Nothing in either Figma file was changed.
Decisions: U-01 to U-10, approved by Avi on 15.11.2026 (see brand-rules.md).
**Changed**
- Name: unifiedmeds, all lowercase, everywhere (U-01). The earlier three-product name becomes Combo (U-05).
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
- Edition 02 and Edition 01 are archived outside the published hub.
Open items: O-01 to O-14 in brand-rules.md (legal details, tagline, product colours on the website, wordmark typeface, shape limits, icon size and colour, secondary logo versions, Light button hover, field states, Phase 2 menu wording, loader shape, assessment length and fee line, licensed photography, legal review of Phase 2 product pages).

---

Earlier editions archived.
