"""Step 7 of the assessment and after it: recommendation, checkout, confirmation, provider review. All data DEMO.
Order (U-32, Q99): consent, account, recommendation, checkout, ID, send. The ID and the send screens are drawn on the Assessment page."""
from build_product_screens import (APPROVAL, BOTTLE, CHARGE, CHECK, browser, field, funnel_foot, funnel_hdr, funnel_prog, ic, mark,
                                   meter, notes, phone, pill, portal_d, portal_m, prod, screen, seg, select, tl)

PLANS = ["1 month", "3 months", "6 months"]  # Q100: plans of 1, 3 and 6 months; the parameters may change, the principle stays

ISI = ('<section class="ps-isi" aria-labelledby="{id}"><h2 class="ps-h2" id="{id}">Important safety information.</h2>'
       '<p class="ps-sm">Shown in full, never collapsed (R-66). The text below is a placeholder for the approved safety information.</p>'
       '<dl><div><dt>Who should not take Tadalafil</dt><dd>[Approved text · clinical and legal]</dd></div>'
       '<div><dt>Tell your provider before you start</dt><dd>[Approved text · clinical and legal]</dd></div>'
       '<div><dt>Possible side effects</dt><dd>[Approved text · clinical and legal]</dd></div>'
       '<div><dt>Get help right away if</dt><dd>[Approved text · clinical and legal]</dd></div></dl>'
       '<a class="link ps-comp" href="#">Full prescribing information [link · legal]</a></section>')

INCLUDED = ('<ul class="check-list"><li>{c}A licensed provider reviews your answers before anything is prescribed</li>'
            '<li>{c}Ships packed with care; nothing outside says what is inside</li><li>{c}Messages with your provider in your account</li></ul>').format(c=CHECK)


def price_card(mobile=False):
    btn = "" if mobile else '<a class="btn btn--yellow ps-full" href="#">Continue to checkout</a>'
    return (f'<section class="ps-card" aria-labelledby="pc-{int(mobile)}"><div class="ps-row ps-between"><h2 class="ps-h2" id="pc-{int(mobile)}">Your plan</h2>'
            f'<span class="ps-demo">E-04 · price allowed here</span></div>'
            f'{seg(PLANS, i=1, full=True, label="Plan length")}'
            '<dl class="ps-kv"><div><dt>Tadalafil, [DOSE] tablets</dt><dd>[qty] tablets a month</dd></div>'
            '<div><dt>Plan</dt><dd>3 months, ships [schedule · operations]</dd></div>'
            '<div><dt>Price per month</dt><dd>$[price]</dd></div>'
            '<div><dt>Compared with 1 month</dt><dd>You save $[amount] a month</dd></div>'
            '<div class="ps-total"><dt>Plan total</dt><dd>$[total]</dd></div></dl>'
            f'{btn}'
            f'<p class="ps-legal">{CHARGE} Your provider reviews your answers first. Change or stop your plan any time [policy · operations]. '
            '[Renewal terms for 3 and 6 months · legal]</p></section>')


def alt_card(p, line):
    return (f'<article class="ps-card"><div class="ps-opt"><div class="ps-btl ps-btl--s"><img src="{BOTTLE[p]}" alt="" width="62" height="100" loading="lazy"></div>'
            f'<div class="ps-stack">{prod(p, line, size="h2")}<a class="link ps-comp" href="#">Choose {p_name(p)} instead</a></div></div></article>')


def p_name(p):
    return {"tad": "Tadalafil", "sil": "Sildenafil", "com": "Combo"}[p]


def recommendation():
    main = (f'<article class="ps-card"><div class="ps-row ps-between"><span class="tag tag--highlight">Matches your answers</span>'
            f'<span class="ps-cp">Your provider makes the final decision</span></div>'
            f'<div class="ps-opt"><div class="ps-btl"><img src="{BOTTLE["tad"]}" alt="A closed unifiedmeds Tadalafil bottle" width="155" height="250" loading="lazy"></div>'
            f'<div class="ps-stack ps-stack--l">{prod("tad", "[DOSE] tablets · as needed or daily, as your provider decides")}'
            f'{INCLUDED}<p class="ps-legal">{APPROVAL}</p><a class="link ps-comp" href="#isi">Read the important safety information</a></div></div></article>')
    alts = ('<section class="ps-stack" aria-labelledby="alt-h"><h2 class="ps-h2" id="alt-h">Other options your provider may consider.</h2>'
            f'<div class="ps-g2">{alt_card("sil", "[DOSE] tablets · [one factual line · clinical]")}'
            f'{alt_card("com", "Tadalafil and [ingredient] · [one factual line · clinical]")}</div>'
            f'<p class="ps-legal">{APPROVAL}</p></section>')
    head = ('<div class="ps-stack" style="max-width: var(--layout-measure)"><span class="ps-lb">Based on your assessment</span>'
            '<h1 class="ps-hero">Your plan options.</h1>'
            '<p class="ps-p">These options match your answers. A licensed provider reviews your assessment and decides what, if anything, to prescribe.</p>'
            '<p class="ps-cp">Assessment only. Not a diagnosis.</p></div>')
    d = (funnel_hdr(0) + f'<div class="ps-wrap">{funnel_prog(0)}{head}<div class="ps-cols"><div class="ps-c7 ps-stack ps-stack--l">{main}{alts}</div>'
         f'<div class="ps-c5">{price_card()}</div><div class="ps-c12">{ISI.format(id="isi")}</div></div></div>' + funnel_foot())
    m = (funnel_hdr(0, mobile=True) + '<div class="ps-wrap">' + funnel_prog(0, mobile=True) + head + main + price_card(mobile=True) + alts + ISI.format(id="isi") + '</div>'
         + '<div class="ps-mbar"><div class="ps-row ps-between"><span class="ps-cp">3-month plan</span><span class="ps-strong ps-comp">$[price] a month</span></div>'
         '<a class="btn btn--yellow btn--bar" href="#">Continue to checkout</a></div>')
    return screen(
        "s-rec", "1 · Recommendation.",
        "Step 7 of the assessment opens here, after consent and the account (U-32). One option leads, two alternatives follow, the plan choice and the price card sit together. "
        "Plans of 1, 3 and 6 months, no \"Most popular\" or \"Best value\" badge (R-61, R-67). The price shows only in the checkout card (E-04). "
        "The provider-approval line sits under the options. Product colours mark the products; the text stays Deep Teal. One Yellow element: the checkout button.",
        browser("[intake domain]/plan", d, "Main option and alternatives on the left (7 columns), the price card on the right (5 columns, sticky). Safety information below, fully open."),
        [phone(m, "One column. The price card follows the main option; a sticky bar carries the price and the Yellow button (48px, E-03).")],
        notes("Mobile and build notes", [
            "Order on mobile: title, main option, price card, alternatives, safety information. Nothing is hidden.",
            "The bottle tile drops from 250 to 175px tall; alternatives become a single column with a 130px bottle.",
            "The sticky bar appears once the price card scrolls out of view; it never covers the safety information heading.",
            "Plan choice: the core segmented control with three options (1, 3 and 6 months) and the sliding thumb (220ms). The price lines cross-fade (180ms). No badge on any plan.",
            "The saving is said in dollars, \"You save $[amount] a month\", never as a percentage or a crossed-out price (R-61).",
            "Charge line: the placeholder [charge line · operations] until operations decide when and what a member pays (U-31).",
            "Wording follows R-64: the provider decides. Never \"recommended for you\" without the provider line.",
            "[DOSE], $[price] and $[amount] stay in brackets until clinical and operations confirm them (R-97, R-61).",
        ]))


def checkout():
    summary = ('<section class="ps-card" aria-labelledby="sum-{k}"><h2 class="ps-h2" id="sum-{k}">Order summary</h2>'
               f'<div class="ps-prod">{mark("tad")}<span class="ps-strong">Tadalafil, [DOSE] tablets</span></div>'
               '<dl class="ps-kv"><div><dt>Plan</dt><dd>3 months</dd></div><div><dt>Price per month</dt><dd>$[price]</dd></div>'
               '<div><dt>Shipping</dt><dd>$[amount] [operations]</dd></div>'
               '<div class="ps-total"><dt>Plan total</dt><dd>$[total]</dd></div></dl>'
               f'<p class="ps-legal">{CHARGE} A licensed provider reviews your assessment before anything ships. No delivery date is promised until operations confirm one (R-68).</p></section>')
    discreet = (f'<p class="ps-note">{ic("package")}<span>Outside, the box says only "Packed with care, just for you." and the sender name unifiedmeds. Nothing about what is inside.</span></p>')
    pay_note = f'<p class="ps-note">{ic("lock")}<span>UI only. In production these are the payment provider\'s hosted fields [provider · operations]; card data never touches our pages.</span></p>'

    def form(mobile):
        zip_ = field("ZIP code", "9021", "Enter a 5-digit ZIP code.", err=True) if mobile else field("ZIP code", "[ZIP]")
        return ('<form class="ps-stack ps-stack--l" onsubmit="return false">'
                '<fieldset class="ps-form-sec"><legend class="ps-h2">Contact</legend><div class="ps-fields2">'
                + field("Email", "daniel.r@example.com", "From the start of your assessment. Order emails never say what you ordered.", "email")
                + field("Mobile phone", "(555) 010-0142", "For delivery updates only. Off by default.", "tel") + '</div></fieldset>'
                '<fieldset class="ps-form-sec"><legend class="ps-h2">Shipping address</legend><div class="ps-fields2 ps-keep">'
                + field("First name", "Daniel") + field("Last name", "R.") + '</div>'
                + field("Address", "[street address]") + field("Apartment, suite (optional)")
                + '<div class="ps-fields3">' + field("City", "[city]") + select("State", "[state]") + zip_ + '</div>' + discreet + '</fieldset>'
                '<fieldset class="ps-form-sec"><legend class="ps-h2">Payment</legend>'
                + field("Card number", "", "", "text", "1234 1234 1234 1234")
                + '<div class="ps-fields2 ps-keep">' + field("Expiry", "", "", "text", "MM / YY") + field("Security code", "", "", "text", "CVC") + '</div>'
                + '<label class="ps-check"><input type="checkbox" checked>Billing address is the same as shipping</label>' + pay_note + '</fieldset>'
                '<fieldset class="ps-form-sec"><p class="ps-sm">You agreed to the Terms, the Privacy notice and the Telehealth consent in step 6. [Payment terms line · legal]</p>'
                + ('' if mobile else '<a class="btn btn--yellow" href="#" style="justify-self: start">Continue to ID</a>') + '</fieldset></form>')

    head = '<div class="ps-stack"><h1 class="ps-h1">Checkout.</h1><p class="ps-sm">Next: a photo of your ID, then you send everything to your provider.</p></div>'
    d = (funnel_hdr(1) + f'<div class="ps-wrap">{funnel_prog(1)}{head}<div class="ps-cols"><div class="ps-c7">{form(False)}</div>'
         f'<div class="ps-c5">{summary.format(k="d")}</div></div></div>' + funnel_foot())
    acc = ('<details class="ps-card" style="gap: 0"><summary class="ps-row ps-between" style="min-height: var(--size-tap-min); cursor: pointer">'
           f'<span class="ps-strong ps-comp">Show order summary</span><span class="ps-strong ps-comp">$[total]</span></summary>{summary.format(k="m")}</details>')
    m = (funnel_hdr(1, mobile=True) + f'<div class="ps-wrap">{funnel_prog(1, mobile=True)}{head}{acc}{form(True)}</div>'
         '<div class="ps-mbar"><a class="btn btn--yellow btn--bar" href="#">Continue to ID</a></div>')
    return screen(
        "s-checkout", "2 · Checkout.",
        "Contact, shipping and payment in one page, the order summary beside it. The email comes from the start of the assessment (no password, U-32). Payment fields are UI only. "
        "The packaging line sits with the address, where the member thinks about it. After checkout: the ID, then Send (Assessment page, screens S8 and S9).",
        browser("[intake domain]/checkout", d, "Form on the left, summary on the right (sticky). One Yellow element: Continue to ID."),
        [phone(m, "The summary collapses to one line at the top. The ZIP field shows the error state: Coral border and dot, the message in Deep Teal.")],
        notes("Mobile and build notes", [
            "Fields are 50px tall, full width; first and last name, expiry and code stay in pairs (each half is still 150px or more).",
            "Errors appear on blur and on submit, under the field, with the core error style (R-15). Focus moves to the first error.",
            "Use autocomplete tokens (email, tel, given-name, address-line1, postal-code, cc-number) and inputmode numeric for numbers.",
            "Continue to ID shows the button loader (core .is-loading) while the payment provider answers; never a second click.",
            "Consents are not asked again here: they were given in step 6 (U-32). Only a payment terms line from legal.",
            "No countdowns, no \"only today\", no upsell between the form and the button (R-61).",
        ]))


def confirmation():
    hero_d = (f'<span class="um-cap ps-decor" style="width: calc(var(--space-24) * 6); right: calc(var(--space-24) * -1.5); top: calc(var(--space-12) * -1)" aria-hidden="true"></span>'
              '<div class="ps-stack ps-over" style="max-width: var(--layout-measure)"><span class="ps-lb">Order #10482 · DEMO</span>'
              '<h1 class="ps-hero">Sent to your provider.</h1><p class="ps-p">Your answers, your plan and your ID are with a licensed provider. '
              'We email you when there is an update; the email only says that there is one.</p></div>')
    steps = [("done", "Assessment", "Nov 17"), ("done", "Plan and ID", "Nov 17"), ("next", "Provider review", "Next"),
             ("", "Prescription", "If prescribed"), ("", "Pharmacy", "After approval"), ("", "Shipping", "Packed with care")]
    cards = ('<div class="ps-g3 ps-over">'
             f'<article class="ps-card"><h2 class="ps-h2">Check your email.</h2><p class="ps-sm">We sent a receipt to d•••@example.com. Subject: "We received your order".</p><span></span></article>'
             f'<article class="ps-card"><h2 class="ps-h2">Anything to add?</h2><p class="ps-sm">Write to your provider before the review. It goes with your assessment.</p><a class="link ps-comp" href="#">Message your provider</a></article>'
             f'<article class="ps-card"><h2 class="ps-h2">Your account.</h2><p class="ps-sm">Your plan, orders and messages, in one place.</p><a class="link ps-comp" href="#">Go to your account</a></article></div>')
    tlcard = f'<section class="ps-card ps-over" aria-label="What happens next"><h2 class="ps-h2">What happens next.</h2>{tl(steps)}</section>'
    d = (funnel_hdr(3) + f'<div class="ps-wrap" style="position: relative; overflow: hidden">{hero_d}{tlcard}{cards}<p class="ps-legal ps-over">{CHARGE}</p>'
         '<a class="btn ps-over" href="#" style="justify-self: start">Go to your account</a></div>' + funnel_foot())
    hero_m = hero_d.replace("calc(var(--space-24) * 6); right: calc(var(--space-24) * -1.5); top: calc(var(--space-12) * -1)",
                            "calc(var(--space-24) * 2); right: calc(var(--space-24) * -0.9); top: calc(var(--space-10) * -1)")
    m = (funnel_hdr(3, mobile=True) + f'<div class="ps-wrap" style="position: relative; overflow: hidden">{hero_m}{tlcard}{cards}<p class="ps-legal ps-over">{CHARGE}</p>'
         '<a class="btn btn--bar ps-over" href="#">Go to your account</a></div>')
    return screen(
        "s-confirm", "3 · Sent and confirmed.",
        "After Send (the last screen of step 7, U-32): says everything arrived and what comes next. The capsule progress is full. The timeline carries the one Yellow mark: the next step, the provider review. No time is promised (R-68). One shape: an outline capsule cropped by the frame edge, never under text.",
        browser("[intake domain]/order/10482", d, "Timeline across the width; three equal cards with the action on one line (R-98)."),
        [phone(m, "The timeline turns vertical; the cards stack; the capsule shrinks and stays in the top right corner, clear of the title.")],
        notes("Mobile and build notes", [
            "The capsule is the extended hub .um-cap outline (assets/patterns, built by tools/capsule_svg.py), Wash Blue at 70%.",
            "Header: the account button is Outline at 44px; the logo stays taller (R-103). On mobile the header shows Account as a link; sign-in is by email link, no password (U-32).",
            "Only the timeline's next step is Yellow. The page button is Dark.",
            "Email address is masked on screen (d•••@example.com).",
        ]))


def pending():
    steps = [("done", "Assessment", "Submitted Nov 17"), ("next", "Provider review", "In progress"), ("", "Prescription", "If prescribed"),
             ("", "Shipping", "After the pharmacy")]
    status = (f'<section class="ps-card" aria-labelledby="pr-h"><div class="ps-row ps-between">{pill("In review", "info", "clock")}'
              '<span class="ps-cp">Order #10482 · DEMO</span></div><h2 class="ps-h2" id="pr-h">Your provider is reviewing your answers.</h2>'
              '<p class="ps-sm">A licensed provider reads every assessment. If your provider has a question, it appears here and in Messages. '
              'Review time: [service level · operations, R-68].</p>' + tl(steps, vertical=True) + '</section>')
    wait = ('<section class="ps-card" aria-labelledby="wt-h"><h2 class="ps-h2" id="wt-h">While you wait.</h2>'
            f'<div><a class="ps-linkrow" href="#">Add something for your provider{ic("chevron-right")}</a>'
            f'<a class="ps-linkrow" href="#">Check your shipping address{ic("chevron-right")}</a>'
            f'<a class="ps-linkrow" href="#">Read about your plan options{ic("chevron-right")}</a></div></section>')
    order = (f'<section class="ps-card" aria-labelledby="po-h"><h2 class="ps-h2" id="po-h">Your order.</h2><div class="ps-prod">{mark("tad")}'
             '<span class="ps-strong ps-comp">Tadalafil, [DOSE] tablets</span></div><p class="ps-cp">3-month plan · Nothing is prescribed or shipped before the review.</p></section>')
    head = '<div class="ps-main-head"><h1 class="ps-h1">Welcome, Daniel.</h1></div>'
    d = portal_d("home", head + f'<div class="ps-cols"><div class="ps-c8">{status}</div><div class="ps-c4 ps-stack ps-stack--l">{wait}{order}</div></div>', badge=0)
    m1 = portal_m("home", '<h1 class="ps-h1">Welcome, Daniel.</h1>' + status + wait, badge=0)
    q = (f'<section class="ps-card" aria-labelledby="pq-h"><div>{pill("Your reply needed", "att", "alert-circle")}</div>'
         '<h2 class="ps-h2" id="pq-h">Your provider has a question.</h2><p class="ps-sm">Jordan Lee, NP asked about one of your answers. '
         'Your review continues when you reply.</p><a class="btn" href="#">Read and reply</a></section>')
    m2 = portal_m("home", '<h1 class="ps-h1">Welcome, Daniel.</h1>' + q + order, badge=1)
    no = ('<section class="ps-card" aria-labelledby="pn-h"><h2 class="ps-h2" id="pn-h">Your provider did not prescribe a treatment.</h2>'
          '<p class="ps-sm">Jordan Lee, NP explains why in Messages. [charge line · operations]</p>'
          '<a class="btn" href="#">Read your provider\'s note</a><a class="link ps-comp" href="#">Talk to support about your order</a></section>')
    m3 = portal_m("home", '<h1 class="ps-h1">Welcome, Daniel.</h1>' + no, badge=1)
    return screen(
        "s-pending", "4 · Provider review (pending).",
        "What the member sees between Send and the provider's decision: the portal home in its first state. "
        "Three phones show the states that follow: in review, the provider has a question, not prescribed.",
        browser("app.[domain]/home", d, "The portal shell from day one, so the member learns one place. The timeline is vertical in the status card."),
        [phone(m1, "In review."), phone(m2, "The provider asked a question: a Wash Yellow pill with an icon, one Dark button."),
         phone(m3, "Not prescribed: calm, plain, the reason lives in Messages, never on this card.")])
