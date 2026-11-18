"""Assemble src/product-screens.html. Run: python3 -B -I assets/product-screens/page.py (from the extended hub root)."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_product_screens as b  # noqa: E402
import screens_funnel as f
import screens_internal as i
import screens_portal as p
import screens_states as s

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def area_toc(items):
    return '<nav class="ps-area-toc" aria-label="Screens in this area">' + "".join(f'<a href="#{a}">{t}</a>' for a, t in items) + "</nav>"


def table(head, rows):
    th = "".join(f'<th scope="col">{h}</th>' for h in head)
    tr = "".join("<tr>" + "".join(f'<td data-label="{h}">{c}</td>' for h, c in zip(head, r)) + "</tr>" for r in rows)
    return f'<div class="table-wrap ps-rtable"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


HEAD = """      <header class="page-head">
        <span class="eyebrow">Care journey</span>
        <h1>Product screens.</h1>
        <p class="lead">Step 7 of the assessment and everything after it, in the unifiedmeds system: the recommendation and checkout, the member portal, the provider's clinical admin and support. Every screen at 1440 in a browser frame and at 390 in a phone frame, built from the core components and tokens.</p>
        <nav class="toc" aria-label="On this page"><a href="#funnel">Funnel</a><a href="#portal">Member portal</a><a href="#admin">Clinical admin</a><a href="#support">Support</a><a href="#states">States</a><a href="#dev">Rules for the developer</a><a href="#open">Decisions</a></nav>
      </header>

      <div class="rule"><span class="status status--current">Current · U-29, U-32</span><p>Avi's decisions are applied (U-29, U-32). Every name, date, number and message is DEMO data. Square brackets mark what clinical, legal or operations must supply: <code>[DOSE]</code>, <code>$[price]</code>, <code>[charge line · operations]</code>, review and shipping times (R-68), legal lines. The questions, consent, account, ID and Send are designed on <a class="link" href="assessment.html">Assessment</a>; the funnel here is its step 7.</p></div>
      <div class="grid-2">
        <div class="rule rule--do"><b>Decisions applied.</b><p>Tadalafil, Sildenafil and Combo (U-21). Product colours mark the product, never text (R-85). Yellow once per screen: the next step, or the funnel's one call to action (R-11). The price only in the checkout card (E-04); plans of 1, 3 and 6 months with no badge (R-61, R-67). The provider-approval line under every treatment option. Disabled at 40% (R-42). Every capsule from tools/capsule_svg.py, with the divider (R-105, R-109).</p></div>
        <div class="rule"><b>How to read the frames.</b><p>Desktop frames are 1440 wide and scale to fit; phone frames are 390 wide. Frames show the full page height, nothing cropped. Hover and click work: the plan toggles, switches and questions respond.</p></div>
      </div>
"""


def section(sid, title, lead, toc, body):
    return (f'      <section class="sec" id="{sid}" aria-labelledby="{sid}-h">\n        <div class="sec-head"><h2 id="{sid}-h">{title}</h2><p>{lead}</p></div>\n'
            f'        {area_toc(toc)}\n{body}\n      </section>\n')


def dev():
    nav = table(["Area", "Desktop (1024 and up)", "Tablet (768 to 1023)", "Mobile (under 768)"], [
        ["Funnel (step 7)", "The assessment header (R-29): 80px, Horizontal logo 52px, \"Save and finish later\" and \"Need help?\". No site menu. Under it, in the content: the capsule 120 with \"Step 7 of 7 · Plan and send\" beside it and the parts of step 7 (Your plan, Checkout, ID, Send).", "Same header at 64px; the parts of step 7 drop, the label stays.", "Header 64px: Back, Primary seal 50px, \"Save\". The capsule 96 with its label beside it; tapping it opens the step list (U-32). A sticky bottom bar carries the price and the one button (48px, E-03)."],
        ["Member portal", "Side nav 248px: Home, My treatment, Messages, Orders, Help; Account and Sign out at the bottom. Horizontal logo 30px.", "Side nav becomes a 72px icon rail with labels in tooltips.", "Top bar 64px with the Primary seal at 40px (R-118) and a help icon. Bottom tab bar: Home, Treatment, Messages, Orders, Account. Tasks (a thread, the refill form) hide the tab bar and show a back button."],
        ["Clinical admin", "Teal Deep side nav 216px with \"Clinical · internal\"; Horizontal reversed logo 24px.", "Icon rail 72px; review becomes two columns, then one.", "Everything works on a phone (U-29): the queue as a list with filter chips; the review in one column with a sticky Sign button; signing asks for [a fresh sign-in · engineering]."],
        ["Support", "Same shell, \"Support · internal\". Inbox in three panes.", "Member panel becomes a drawer; list and ticket split into two views.", "Everything works on a phone: read, reply, macros in a bottom sheet, escalate."],
    ])
    space = table(["Part", "Desktop", "Mobile", "Token"], [
        ["Page margins", "100 (funnel), 48 (portal main), 40 (internal main)", "20", "<code>--layout-margin-*</code>, <code>--space-12</code>, <code>--space-10</code>"],
        ["Gap between cards", "24", "16", "<code>--space-6</code>, <code>--space-4</code>"],
        ["Card padding", "24", "16", "<code>--space-6</code>, <code>--space-4</code>; radius 16"],
        ["Grid", "12 columns, 20 gutter; portal 8 + 4, funnel 7 + 5", "1 column", "<code>--layout-columns</code>, <code>--layout-gutter</code>"],
        ["Table rows (internal)", "48 (12 padding + 21 line + borders)", "Rows become 44px list items", "<code>--space-3</code>"],
        ["Stacked sections in a form", "24 between, a Line Soft rule", "16", "<code>--space-6</code>"],
    ])
    types = table(["Role", "Desktop", "Mobile", "Token"], [
        ["Funnel page title", "DM Serif 46/54", "DM Serif 34/40", "<code>--type-*-hero-*</code>"],
        ["App page title (portal, admin, support)", "DM Serif 36/40", "DM Serif 28/34", "<code>--type-desktop-section-*</code>, <code>--type-mobile-section-*</code>"],
        ["Card title", "Inter SemiBold 17/24", "Inter SemiBold 16/22", "<code>--type-*-card-*</code>"],
        ["Body", "Inter 16/24", "Inter 15/23", "<code>--type-*-body-*</code>"],
        ["Supporting text, fine print", "Inter 15 and 13", "Inter 15 and 13", "<code>--type-desktop-small-*</code>, <code>--type-desktop-caption-*</code>, <code>--type-mobile-compact-*</code>"],
        ["Tables and dense internal text", "Inter 14/21, tabular figures", "Inter 13/20", "<code>--type-desktop-compact-*</code>"],
        ["Labels", "Inter SemiBold 12/16 +2%", "Inter SemiBold 11/16", "<code>--type-*-label-*</code>"],
        ["Figures (days left, totals)", "Inter SemiBold 26", "Inter SemiBold 21", "<code>--type-desktop-h3-size</code> (proposed <code>type.data-figure</code>)"],
        ["Buttons", "Inter Medium 15/20, 50px", "Same; bar buttons 48px", "<code>--type-*-button-*</code>, <code>--size-control</code>"],
    ])
    taps = table(["Element", "Size", "Note"], [
        ["Any tap target", "44 × 44 minimum", "R-74. Links in running text get 44px rows where they stand alone."],
        ["Tab bar item", "78 × 56, icon 24, label 11", "Five items at 390; the active tab has a 2px Deep Teal top bar."],
        ["Icon button", "44 × 44, icon 20", "Attach, back, help, pager. A visible border where it stands alone in a form."],
        ["Switch", "52 × 32 inside a 44px row", "The whole row toggles."],
        ["Answer option", "50px minimum, full width", "One answer: Deep Teal fill with the Yellow mark. Several answers: Deep Teal border and 1px inset (R-42, U-31)."],
        ["Fields", "50px", "Labels above, help below; never placeholder-only labels."],
    ])
    disc = table(["Event", "Push (off by default)", "Email subject", "Never"], [
        ["Provider message", "You have a new message.", "Your provider has replied", "The sender's name, the product, the text"],
        ["Provider decision", "You have an update.", "You have an update", "Approved, declined, the medicine, the dose"],
        ["Order shipped", "Your order is on its way.", "Your order is on its way", "The product name, \"pharmacy\" in the subject"],
        ["Refill due", "Time to plan your next month.", "Time to plan your next month", "The dose, the number of tablets left"],
        ["Support reply", "You have a new message.", "We replied to your message", "The ticket topic"],
    ])
    a11y = ("<ul class=\"ps-dev-list\">"
            "<li>Focus ring 2px Deep Teal (Paper on Teal Deep internal nav), never removed. Focus order follows the reading order; dialogs trap focus and return it.</li>"
            "<li>Landmarks: header, nav (labelled), main. One h1 per screen; card titles are h2.</li>"
            "<li>Current place: aria-current=\"page\" on nav items, aria-current=\"step\" on the timeline's next step, aria-current=\"date\" on today.</li>"
            "<li>Messages: role=\"log\"; toasts role=\"status\"; errors role=\"alert\". New messages are announced politely, never as alerts.</li>"
            "<li>Every chart and timeline is an ordered list or has a text equivalent; colour only repeats what the words say.</li>"
            "<li>Contrast AA on every pair used: Deep Teal on Paper 9.82:1, Paper on Deep Teal, Slate captions on Paper; Wash Yellow and Wash Green pills carry Teal Deep text.</li>"
            "<li>Product colours never carry text and never stand alone: the name is always written next to the mark.</li>"
            "<li>Reduced motion: the thumb, the accordion and the loader stop; the loader shows half filled.</li>"
            "<li>Zoom to 200% and 320px wide without sideways scroll (R-77). Tables on internal tools may scroll inside their own frame, with a visible edge.</li>"
            "<li>Disabled controls use aria-disabled so they stay focusable and the reason next to them is read.</li></ul>")
    body = (f'<div class="ps-spec"><h3>Navigation.</h3>{nav}</div>'
            f'<div class="ps-spec"><h3>Spacing and layout.</h3>{space}</div>'
            f'<div class="ps-spec"><h3>Type sizes.</h3>{types}</div>'
            f'<div class="ps-spec"><h3>Tap targets.</h3>{taps}</div>'
            f'<div class="ps-spec"><h3>Notification discretion.</h3><p class="cap">No product names, doses or conditions in push, email subjects, previews, SMS or on the lock screen (R-108). Push, text messages and sounds are off until the member turns them on; one switch controls every sound.</p>{disc}</div>'
            f'<div class="ps-spec"><h3>Accessibility.</h3>{a11y}</div>'
            '<div class="ps-spec"><h3>Files.</h3><p class="cap">Product marks and the loader as standalone SVG (hex from tokens.json): '
            '<a class="link" href="assets/product-screens/mark-tadalafil.svg" download>mark-tadalafil.svg</a>, '
            '<a class="link" href="assets/product-screens/mark-sildenafil.svg" download>mark-sildenafil.svg</a>, '
            '<a class="link" href="assets/product-screens/mark-combo.svg" download>mark-combo.svg</a>, '
            '<a class="link" href="assets/product-screens/cap-loader.svg" download>cap-loader.svg</a>. '
            'The page is generated by <code>assets/product-screens/page.py</code>; styles in <code>ps_style.css</code>.</p></div>')
    return ('      <section class="sec" id="dev" aria-labelledby="dev-h">\n        <div class="sec-head"><h2 id="dev-h">Rules for the developer.</h2>'
            '<p>One table per topic, desktop, tablet and mobile side by side. Every value is a token from the core hub.</p></div>\n'
            f'        {body}\n      </section>\n')


def open_q():
    D = '<span class="status status--current">Current · U-29</span> '
    rows = [
        ["1", "When does the provider review: after checkout or before the price appears?", '<span class="status status--current">Current · U-32</span> Decided with the assessment screens (Q99): consent, account, recommendation, checkout, ID, then Send. The provider reviews after Send. The charge line stays <code>[charge line · operations]</code> (U-31).'],
        ["2", "Recommendation wording.", D + "\"Matches your answers\" with \"Your provider makes the final decision\"; never \"Recommended for you\" alone. Legal to confirm."],
        ["3", "Clinical admin and support on a phone.", D + "Everything works on a phone, the same as on a computer: the queue, the review, signing and support. Signing on a phone asks for [a fresh sign-in · engineering]."],
        ["4", "Disabled buttons.", D + "40% opacity with the button's own colours (R-42, token <code>--opacity-disabled</code>)."],
        ["5", "Clinical flags: Wash Yellow pill with an icon, or Coral?", D + "Wash Yellow. Coral stays for errors and out-of-range results (R-15)."],
        ["6", "Portal logo.", D + "Horizontal 30px in the side nav, Primary seal 40px in the mobile top bar, for app screens. The website header rule R-103 stays for the website."],
        ["7", "The UI icons used here.", "They come from the UI set on <a class=\"link\" href=\"icons.html\">Icons</a> (assets/icons/ui/); its status lives there."],
    ]
    return ('      <section class="sec" id="open" aria-labelledby="open-h">\n        <div class="sec-head"><h2 id="open-h">Questions and decisions.</h2>'
            '<p>All seven are answered (U-29, U-32).</p></div>\n        '
            + table(["#", "Question", "Decision"], rows) + "\n      </section>\n")


SCRIPT = """
<script>
/* Product screens: fit each 1440 or 390 canvas to its frame (CSS zoom); small interactions for review. */
(() => {
  const vps = [...document.querySelectorAll('.ps-vp')];
  const fit = (vp) => {
    const cv = vp.firstElementChild; const w = +vp.dataset.w || 1440;
    const s = Math.min(1, vp.clientWidth / w);
    cv.style.zoom = s; vp.classList.add('is-fit');
  };
  if ('ResizeObserver' in window) { const ro = new ResizeObserver((es) => es.forEach((e) => fit(e.target))); vps.forEach((v) => ro.observe(v)); }
  vps.forEach(fit);
  document.addEventListener('click', (e) => {
    const a = e.target.closest('.ps-cv a[href="#"]'); if (a) e.preventDefault();
    const segb = e.target.closest('.ps-cv .segmented button');
    if (segb) { const g = segb.parentElement; [...g.children].forEach((b, i) => { const on = b === segb; b.setAttribute('aria-checked', on); if (on) g.style.setProperty('--seg-i', i); }); }
    const swb = e.target.closest('.ps-cv .ps-sw');
    if (swb) { e.preventDefault(); swb.setAttribute('aria-checked', swb.getAttribute('aria-checked') !== 'true'); }
    const opt = e.target.closest('.ps-cv .option');
    if (opt) { const g = opt.closest('[role="radiogroup"]'); if (g) g.querySelectorAll('.option').forEach((o) => o.setAttribute('aria-checked', o === opt)); }
    const tab = e.target.closest('.ps-cv .tabs [role="tab"]');
    if (tab) tab.parentElement.querySelectorAll('[role="tab"]').forEach((t) => t.setAttribute('aria-selected', t === tab));
    const chip = e.target.closest('.ps-cv .ps-chips .chip');
    if (chip) chip.parentElement.querySelectorAll('.chip').forEach((c) => c.setAttribute('aria-pressed', c === chip));
  });
})();
</script>
"""


def main():
    b.write_assets()
    style = (pathlib.Path(__file__).parent / "ps_style.css").read_text()
    funnel = section("funnel", "Funnel: step 7 and after.",
                     "One step model for the whole funnel (U-32): the assessment's seven steps, then the provider. Step 7, Plan and send, runs recommendation, checkout, ID and Send, all on the clinical intake domain (R-70). The ID and Send screens are on <a class=\"link\" href=\"assessment.html#screens\">Assessment</a>.",
                     [("s-rec", "1 · Recommendation"), ("s-checkout", "2 · Checkout"), ("s-confirm", "3 · Sent"), ("s-pending", "4 · Provider review")],
                     f.recommendation() + f.checkout() + f.confirmation() + f.pending())
    portal = section("portal", "Member portal.",
                     "His plan, his messages, his orders. Calm and private: the portal informs, it never rewards or blames (Data in the portal).",
                     [("s-home", "5 · Home"), ("s-treatment", "6 · My treatment"), ("s-messages", "7 · Messages"), ("s-orders", "8 · Orders"),
                      ("s-refill", "9 · Refill"), ("s-account", "10 · Account"), ("s-help", "11 · Help")],
                     p.home() + p.treatment() + p.messages() + p.orders() + p.refill() + p.account() + p.help_())
    admin = section("admin", "Clinical admin.",
                    "The provider's side. Desktop first, dense, on the type scale. A monospace face would be allowed here (R-18); Inter with tabular figures is enough.",
                    [("a-queue", "12 · Review queue"), ("a-review", "13 · Assessment review"), ("a-rx", "14 · Prescription"), ("a-audit", "15 · Audit trail")],
                    i.queue() + i.review() + i.prescription() + i.audit())
    support = section("support", "Support.",
                      "Orders, payment and account, answered by people who never see health data. Anything clinical goes to a provider.",
                      [("u-inbox", "16 · Inbox and macros"), ("u-escalate", "17 · Escalation")],
                      i.support_inbox() + i.escalation())
    states = section("states", "States.", "Empty, loading, error, offline and disabled, as they appear in the portal.",
                     [("x-states", "18 · All five states")], s.states())
    page = (f"<style>\n{style}  .ps-dev-list {{ margin: 0; padding-left: var(--space-5); display: grid; gap: var(--space-2); }}\n</style>\n"
            + HEAD + "\n" + funnel + portal + admin + support + states + dev() + open_q() + SCRIPT)
    page = re.sub(r'(<label class="ps-check"><input[^>]*>)(.*?)(</label>)', r'\1<span>\2</span>\3', page)
    out = ROOT / "src" / "product-screens.html"
    out.write_text(page)
    print("wrote", out, len(page) // 1024, "KB")


if __name__ == "__main__":
    main()
