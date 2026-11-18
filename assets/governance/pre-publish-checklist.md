# unifiedmeds · Pre-publish checklist

Brand Edition 04 · generated from How we work (how-we-work.html#checklist) by assets/governance/build_checklist.py; edit the page, never this file.

Run it on the exact file that ships. Write the codes you checked in the approval log. Every page and screen is checked at 1440 and 390 wide at least; website builds also at 768 and 1024 (R-27, R-107). The Dev block applies to website and product builds only.

File: ______________________________  Version: v__  Date: __________  Checked by: __________

## Brand
- [ ] B1 The name is "unifiedmeds", lower case; the former brand name appears nowhere (R-07, U-16).
- [ ] B2 Colours come from the tokens; Yellow once per view at most, never a background (R-03, R-11).
- [ ] B3 DM Serif Display and Inter only; serif never below 24 desktop or 21 mobile (R-18, R-21).
- [ ] B4 Buttons are rounded rectangles, radius 5, never pills; two buttons side by side never share a colour (R-40, R-112).
- [ ] B5 Logo from the exported files, the right version for the ground, clear space and minimum sizes kept (R-91, R-92, R-118).
- [ ] B6 Sentence case; headlines end with a full stop and are never questions; no em or en dashes (R-24).
- [ ] B7 Cards in a row share one height and one action line (R-98).
- [ ] B8 Two shapes per surface at most; every capsule keeps its divider (R-106, R-109).

## Compliance
- [ ] C1 No benefit claim, price or symptom list in a hero (R-58, R-61).
- [ ] C2 Prescription names only where safety information sits; never in heroes, ads, social assets or captions (R-65, R-108).
- [ ] C3 "Assessment only. Not a diagnosis." next to every assessment button above the fold and on every assessment screen (R-63).
- [ ] C4 A licensed provider is named for every next step (R-64).
- [ ] C5 No statistics, reviews, testimonials, ratings or promised times; a demo review shows DEMO ONLY and "Member · age", never "Verified" (R-67, R-68).
- [ ] C6 Illustrative medical content shows DEMO ONLY; items marked Legal review required stay off (R-69, R-87).
- [ ] C7 Footer reads "© 2026 unifiedmeds"; marketing email has unsubscribe and address (R-88).
- [ ] C8 Open placeholders stay visible until they are decided: "[charge line · operations]" and "[about N minutes · O-12]" (R-62, O-12).

## Accessibility
- [ ] A1 Text passes WCAG AA contrast (R-72).
- [ ] A2 Every image has alt text; on web pages text is live, never inside an image.
- [ ] A3 Tap targets 44 by 44 or larger; focus ring visible (R-73, R-74).
- [ ] A4 Checked at 1440 and 390 wide: nothing cut, no sideways scroll (R-77, R-107).
- [ ] A5 With reduced motion, nothing moves (R-76).
- [ ] A6 Video has captions; nothing flashes.

## Discretion
- [ ] D1 Subject lines, previews, notifications and sender names never name a condition or a medicine (R-108).
- [ ] D2 No health data in any email.
- [ ] D3 File names and image addresses inside emails are neutral (category all).
- [ ] D4 No ad audience built from health data or from the assessment.

## Tracking
- [ ] T1 No tracking pixels, ad tags or session replay on condition or product pages (R-71).
- [ ] T2 Assessment answers only on the clinical intake domain (R-70).
- [ ] T3 No analytics before consent, the assessment included, unless legal approves an exception (U-31).
- [ ] T4 Buttons carry data-cta named by position; links carry the UTM pattern.
- [ ] T5 No name, email, ID or condition in any URL or UTM value.

## Filing
- [ ] F1 The file is named by the convention; no "final" in any name (R-126).
- [ ] F2 The approved version sits in the approved folder, unchanged (R-124).
- [ ] F3 The log has its row; the version it replaces moved to the archive (R-125, R-127).

## Dev · website and product builds
- [ ] Dev1 python3 -I tools/check.py prints 0 problems: no colour literal in styling, only DM Serif Display and Inter, no broken links (R-03, R-83).
- [ ] Dev2 Checked at 1440 and 390 always, and at 768 and 1024 for website builds (R-27, R-107).
- [ ] Dev3 Every value comes from a token; nothing is built without one, and brand.css is never edited by hand (R-03).
- [ ] Dev4 Only logged exceptions differ: E-02 header button 44px, E-03 mobile menu bar button 48px, E-04 the price in the checkout card, E-05 the inline "state not served" message on screen 01 with Continue disabled.
- [ ] Dev5 Focus: tab through every page; a 2px Deep Teal ring at a 3px offset, Paper on dark grounds and photos, never hidden (R-73).
- [ ] Dev6 Keyboard and touch: nothing works on hover only; the menu opens with Enter or ↓, Esc closes it and returns focus, aria-expanded updates (R-75, R-46).
- [ ] Dev7 Reduced motion emulated: every state is instant. With motion on, nothing loops except the loader (R-76, R-53).
- [ ] Dev8 No link to a retired Figma file, to an archived page as if current, or to a Phase 2 category before it launches (R-04, R-06).
- [ ] Dev9 No watermarked or stand-in photo ships; meaningful images have alt text, decorative images an empty alt (R-39).

## Sign-off
| Step | Name | Date | Result |
|---|---|---|---|
| Brand check | | | |
| Clinical (if medical content) | | | |
| Legal | | | |
| Final sign-off (Brand) | | | |

Codes in this checklist: B1 to B8, C1 to C8, A1 to A6, D1 to D4, T1 to T5, F1 to F3, Dev1 to Dev9.
