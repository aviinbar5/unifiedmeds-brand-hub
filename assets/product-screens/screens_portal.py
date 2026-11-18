"""Member portal: home, my treatment, messages, orders, refill, account, help. All data DEMO."""
from build_product_screens import (APP_ICON, BOTTLE, CHECK, back_top, browser, field, ic, mark, meter, notes, option, phone,
                                   pill, portal_d, portal_m, prod, screen, seg, select, setrow, tl)

PROVIDER = "Jordan Lee, NP"


def _week():
    days = [("Mon", "quiet"), ("Tue", "on"), ("Wed", "quiet"), ("Thu", "quiet"), ("Fri", "today"), ("Sat", "quiet"), ("Sun", "quiet")]
    out = []
    for d, s in days:
        cls = {"on": "is-on", "quiet": "is-quiet", "today": "is-quiet is-today"}[s]
        mk = CHECK if s == "on" else ""
        sr = {"on": ": marked as taken", "quiet": ": nothing marked", "today": ", today: nothing marked yet"}[s]
        cur = ' aria-current="date"' if s == "today" else ""
        out.append(f'<li class="{cls}"{cur}><span class="ps-wd" aria-hidden="true">{mk}</span>{d}<span class="ps-sr">{sr}</span></li>')
    return f'<ol class="ps-week" aria-label="This week, as-needed plan">{"".join(out)}</ol>'


NEXT_STEPS = [("done", "First shipment", "Delivered Oct 8"), ("done", "Check-in", "Nov 1"), ("next", "Refill review", "Next · Dec 2"),
              ("", "Second shipment", "After the review")]


def treatment_card(full=True):
    link = '<a class="link ps-comp" href="#">See your plan</a>' if full else ""
    return (f'<section class="ps-card" aria-labelledby="tc-h{int(full)}"><div class="ps-row ps-between"><span class="ps-lb">Your treatment</span>{pill("Active", "ok")}</div>'
            f'<div class="ps-prod">{mark("tad")}<h2 class="ps-h2" id="tc-h{int(full)}">Tadalafil, [DOSE] tablets</h2></div>'
            '<p class="ps-cp">As needed · 3-month plan · prescribed by ' + PROVIDER + '</p>'
            + meter(40, "<b>12 of 30 days</b> left", "Review Dec 2", "12 of 30 days left in your current supply. Refill review on Dec 2.") + link + '</section>')


def msg_card():
    return (f'<section class="ps-card" aria-labelledby="mc-h"><div class="ps-row ps-between"><span class="ps-lb">Messages</span><span class="ps-badge" style="margin: 0">1</span></div>'
            f'<div class="ps-row ps-row--top" style="flex-wrap: nowrap"><span class="ps-av">JL</span><div class="ps-stack ps-stack--s">'
            f'<h2 class="ps-h2" id="mc-h">1 new message from your provider</h2><span class="ps-cp">{PROVIDER} · Nov 15</span></div></div>'
            '<a class="btn btn--outline" href="#" style="justify-self: start">Open messages</a></section>')


def home():
    nxt = ('<section class="ps-card" aria-labelledby="nx-h"><span class="ps-lb">Next step</span><h2 class="ps-h2" id="nx-h">Your provider reviews your refill on Dec 2.</h2>'
           + tl(NEXT_STEPS) + '<p class="ps-cp">A licensed provider reviews every refill before it ships (R-64).</p></section>')
    order = ('<section class="ps-card" aria-labelledby="oc-h"><span class="ps-lb">Latest order</span><h2 class="ps-h2" id="oc-h">Delivered Nov 8</h2>'
             '<p class="ps-cp">Order #10482 · packed with care</p><a class="link ps-comp" href="#">See your orders</a></section>')
    helpc = (f'<section class="ps-card ps-card--mist" aria-labelledby="hc-h"><h2 class="ps-h2" id="hc-h">Need help?</h2>'
             '<p class="ps-cp">Questions about your treatment go to your provider. Orders and account go to support.</p><a class="link ps-comp" href="#">Get help</a></section>')
    head = '<div class="ps-main-head"><div class="ps-stack ps-stack--s"><span class="ps-lb">Tuesday, Nov 17 · DEMO</span><h1 class="ps-h1">Good morning, Daniel.</h1></div></div>'
    d = portal_d("home", head + f'<div class="ps-cols"><div class="ps-c8 ps-stack ps-stack--l">{nxt}{treatment_card()}</div>'
                 f'<div class="ps-c4 ps-stack ps-stack--l">{msg_card()}{order}{helpc}</div></div>')
    m = portal_m("home", '<h1 class="ps-h1">Good morning, Daniel.</h1>' + nxt + treatment_card() + msg_card() + order)
    return screen(
        "s-home", "5 · Home.",
        "Three questions answered on arrival: what happens next, how my treatment stands, whether someone wrote to me. The message card never previews the message.",
        browser("app.[domain]/home", d, "Side nav 248px. Main area: 8 columns for plan content, 4 for messages, orders and help."),
        [phone(m, "Top bar with the Primary seal at 40px (R-118 minimum), tab bar with five tabs. The timeline is vertical.")],
        notes("Mobile and build notes", [
            "Order on mobile: greeting, next step, treatment, messages, latest order. Help moves to the top bar icon.",
            "One Yellow mark per screen: the next step on the timeline (Data in the portal, U-30).",
            "The unread badge is Deep Teal with a Paper number, never Coral or Yellow. Screen readers hear \"1 new\".",
            "The greeting uses the first name only. No health words on the home screen above the treatment card.",
        ]))


def treatment():
    plan = (f'<section class="ps-card" aria-label="Your plan"><div class="ps-opt"><div class="ps-btl ps-btl--s"><img src="{BOTTLE["tad"]}" alt="Your Tadalafil bottle" width="62" height="100" loading="lazy"></div>'
            f'<div class="ps-stack">{prod("tad", "[DOSE] tablets · as needed")}</div></div>'
            '<dl class="ps-kv ps-kv--stack"><div><dt>How to take it</dt><dd>[Directions exactly as on your prescription label · provider]</dd></div>'
            f'<div><dt>Prescribed by</dt><dd>{PROVIDER} · Oct 4</dd></div><div><dt>Refills left</dt><dd>[n] · DEMO</dd></div></dl>'
            '<a class="link ps-comp" href="#">Read the safety information</a></section>')
    remind = ('<section class="ps-card" aria-labelledby="rm-h"><span class="ps-lb">Plan reminder</span><h2 class="ps-h2" id="rm-h">You marked 1 dose this week.</h2>'
              '<p class="ps-cp">As-needed plan: there is no missed day. The check is optional, only for you, never a score.</p>'
              + _week() + '<div class="ps-row"><button class="btn btn--outline" type="button">Mark today as taken</button>'
              '<span class="ps-cp">Optional</span></div>'
              + setrow("Reminder", "Off. Turn it on to get a quiet reminder at a time you choose. It never names your treatment.") + '</section>')
    refill = ('<section class="ps-card" aria-labelledby="rf-h"><span class="ps-lb">Refill</span><h2 class="ps-h2" id="rf-h">Your next refill is in 12 days.</h2>'
              + meter(40, "<b>12 of 30 days</b> left", "Review Dec 2", "12 of 30 days left in your current supply.")
              + '<a class="btn" href="#" style="justify-self: start">Request a refill</a><p class="ps-cp">Your provider reviews every refill before it ships.</p></section>')
    ask = (f'<section class="ps-card ps-card--mist" aria-labelledby="ak-h"><h2 class="ps-h2" id="ak-h">Questions about your dose?</h2>'
           '<p class="ps-cp">Ask your provider. Never change your dose without your provider.</p><a class="link ps-comp" href="#">Message your provider</a></section>')
    tabs = ('<div class="tabs" role="tablist" aria-label="Treatment"><button role="tab" aria-selected="true" type="button">Plan</button>'
            '<button role="tab" aria-selected="false" type="button">Safety information</button><button role="tab" aria-selected="false" type="button">History</button></div>')
    head = '<div class="ps-main-head"><h1 class="ps-h1">My treatment.</h1></div>'
    d = portal_d("treatment", head + tabs + f'<div class="ps-cols"><div class="ps-c7 ps-stack ps-stack--l">{plan}{remind}</div>'
                 f'<div class="ps-c5 ps-stack ps-stack--l">{refill}{ask}</div></div>')
    m = portal_m("treatment", '<h1 class="ps-h1">My treatment.</h1>' + tabs + plan + refill + remind + ask)
    return screen(
        "s-treatment", "6 · My treatment.",
        "The dose plan from the prescription, the plan reminder with its optional check, and the refill. No streaks, no scores, no \"missed\" days on an as-needed plan.",
        browser("app.[domain]/treatment", d, "Plan and reminder on the left, refill and the provider link on the right."),
        [phone(m, "Refill moves above the reminder on mobile, because it carries the only action with a date.")],
        notes("Mobile and build notes", [
            "Directions are shown exactly as the pharmacy label prints them; the portal never rewrites a dose.",
            "Week dots (R-113): a marked dose fills Blue on an As-needed plan, Green on a Daily plan, with a Deep Teal check; nothing marked is Mist; today has a ring. Never red, never a product colour.",
            "The reminder switch is off by default. The whole row is the 44px target; the switch itself is 52 × 32.",
            "Tabs: 44px tall, the active tab underlined in Deep Teal. On 390 all three tabs fit; no horizontal scroll.",
        ]))


def messages():
    threads = (f'<nav class="ps-threads" aria-label="Conversations"><a class="ps-thr" href="#" aria-current="true"><span class="ps-av">JL</span>'
               f'<span class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">{PROVIDER}</b><span class="ps-cp">Your provider · Nov 15</span></span><span class="ps-unread" aria-label="Unread"></span></a>'
               '<a class="ps-thr" href="#"><span class="ps-av ps-av--dark">um</span><span class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">Care team</b>'
               '<span class="ps-cp">Orders and account · Nov 2</span></span><span></span></a></nav>')
    bubbles = ('<div class="ps-bubbles" role="log" aria-label="Conversation with your provider"><span class="ps-day">Nov 14</span>'
               '<div class="ps-b ps-b--me">I have a question about taking it with [medicine]. Photo of the label attached.'
               f'<a class="ps-att" href="#">{ic("document")}label-photo.jpg<span class="ps-cp">1.2 MB</span></a></div>'
               '<span class="ps-bmeta ps-bmeta--me">Sent Nov 14 · Read</span><span class="ps-day">Nov 15</span>'
               f'<div class="ps-b ps-b--them">Thanks, Daniel. I looked at the label. [Provider reply · DEMO, written by the provider]</div>'
               f'<span class="ps-bmeta">{PROVIDER} · Nov 15</span></div>')
    composer = (f'<div class="ps-composer"><button class="ps-ib ps-ib--line" type="button" aria-label="Attach a file">{ic("upload")}</button>'
                '<label class="ps-sr" for="cmp">Message</label><textarea class="ps-ta" id="cmp" placeholder="Write to your provider"></textarea>'
                '<button class="btn" type="button">Send</button></div>')
    conv = (f'<section class="ps-conv" aria-label="Conversation"><div class="ps-conv-h"><span class="ps-av">JL</span><div class="ps-stack ps-stack--s">'
            f'<b class="ps-strong ps-comp">{PROVIDER}</b><span class="ps-cp">Your provider · licensed in [state]</span></div></div>{bubbles}{composer}</section>')
    head = ('<div class="ps-main-head"><h1 class="ps-h1">Messages.</h1><span class="ps-cp">Private. For an emergency, call 911 [clinical and legal].</span></div>')
    d = portal_d("messages", head + f'<div class="ps-msgs">{threads}{conv}</div>'
                 '<p class="ps-cp">Attachments: JPG, PNG or PDF up to [size · engineering]. Reply time: [service level · operations, R-68].</p>')
    m = portal_m("messages", bubbles.replace('class="ps-bubbles"', 'class="ps-bubbles" style="padding: 0"'), top=back_top(PROVIDER, "Your provider"), tabbar=False) + composer
    lock = ('<div class="ps-lock"><span class="ps-lock-time">9:41</span><span class="ps-lock-date">Tuesday, November 17</span>'
            f'<div class="ps-push"><img src="{APP_ICON}" alt="" width="32" height="32"><span class="ps-stack ps-stack--s"><b>unifiedmeds</b>'
            '<span class="ps-comp">You have a new message.</span></span><span class="ps-cp">now</span></div></div>')
    return screen(
        "s-messages", "7 · Messages with the provider.",
        "One thread per person: the provider and the care team. Attachments are chips with name and size. Notifications say only that a message arrived.",
        browser("app.[domain]/messages", d, "Thread list 336px, conversation fills the rest. The composer stays at the bottom of the conversation."),
        [phone(m, "Inside a conversation the tab bar hides; the back button returns to the list. The composer sits above the home indicator."),
         phone(lock, "The lock screen: app name and \"You have a new message.\" Never the sender, a product, a dose or the text.", dark_status=True)],
        notes("Mobile and build notes", [
            "Member bubbles are Deep Teal with Paper text (9.82:1); provider bubbles Mist with Deep Teal text.",
            "The thread is a role=\"log\" region so new messages are announced politely.",
            "Push: off by default (Account). When on, the text is fixed: \"You have a new message.\" Email subject: \"Your provider has replied\".",
            "Sound: one setting for all sounds, off by default; the message sound comes from the Sound page.",
            "The attach button is a 44px icon button with a visible border and a label for screen readers.",
        ]))


def orders():
    steps = [("done", "Provider approved", "Nov 2"), ("done", "At the pharmacy", "Nov 3"), ("done", "Shipped", "Nov 4"), ("next", "Delivery", "[carrier] estimate")]
    cur = (f'<section class="ps-card" aria-labelledby="co-h"><div class="ps-row ps-between"><div class="ps-stack ps-stack--s"><span class="ps-lb">Current order · #10517</span>'
           f'<h2 class="ps-h2" id="co-h">On its way</h2></div>{pill("Shipped", "info", "truck")}</div>{tl(steps)}'
           '<dl class="ps-kv"><div><dt>Carrier</dt><dd>[carrier]</dd></div><div><dt>Tracking number</dt><dd>[tracking number]</dd></div></dl>'
           f'<a class="btn btn--outline btn--icon" href="#" style="justify-self: start">Track with [carrier]{ic("chevron-right", "btn-icon")}</a>'
           f'<p class="ps-note">{ic("package")}<span>Plain mailer. Outside: the sender name unifiedmeds and a short discreet line. Delivery dates come from the carrier; we never promise one (R-68).</span></p></section>')
    rows = [("#10482", "Oct 6", "Tadalafil, [DOSE] · 1 bottle", "$[total]", "Delivered"), ("#10311", "Jul 8", "Tadalafil, [DOSE] · 1 bottle", "$[total]", "Delivered")]
    tr = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{pill(e, "ok")}</td><td><a class="link" href="#">Receipt</a></td></tr>' for a, b, c, d, e in rows)
    past = (f'<section class="ps-stack" aria-labelledby="po2-h"><h2 class="ps-h2" id="po2-h">Past orders</h2><div class="ps-tblw"><table class="ps-tbl">'
            f'<thead><tr><th scope="col">Order</th><th scope="col">Date</th><th scope="col">Items</th><th scope="col">Total</th><th scope="col">Status</th><th scope="col"><span class="ps-sr">Receipt</span></th></tr></thead><tbody>{tr}</tbody></table></div></section>')
    pastm = ('<section class="ps-card" aria-labelledby="po3-h"><h2 class="ps-h2" id="po3-h">Past orders</h2><div>'
             + "".join(f'<a class="ps-linkrow" href="#"><span class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">{a} · {b}</b><span class="ps-cp">{e} · {d}</span></span>{ic("chevron-right")}</a>' for a, b, c, d, e in rows)
             + '</div></section>')
    d = portal_d("orders", '<div class="ps-main-head"><h1 class="ps-h1">Orders.</h1></div>' + cur + past)
    m = portal_m("orders", '<h1 class="ps-h1">Orders.</h1>' + cur + pastm)
    return screen(
        "s-orders", "8 · Orders and tracking.",
        "The current order with its stages, the carrier link and the plain-packaging note; past orders below with receipts. No promised delivery time.",
        browser("app.[domain]/orders", d, "Tracking stages across the card; the past orders table is 48px per row."),
        [phone(m, "Stages go vertical. Past orders become 44px rows that open the order; the receipt sits inside the order.")],
        notes("Mobile and build notes", [
            "The next stage carries the one Yellow mark; finished stages are Deep Teal with a check.",
            "Dates are the dates events happened. A future date shows only when the carrier provides it, labelled as the carrier's.",
            "The carrier button opens the carrier site in a new tab (icon button family, R-100); it says so to screen readers.",
            "Receipts are PDFs without the product name on the first line [legal to confirm].",
        ]))


def refill():
    q1 = ('<fieldset class="ps-form-sec"><legend class="ps-h2">Since your last check-in, has anything changed in your health or your medicines?</legend>'
          '<div class="ps-stack" role="radiogroup">' + option("No changes", True) + option("Yes, something changed") + '</div></fieldset>')
    q2 = ('<fieldset class="ps-form-sec"><legend class="ps-h2">Anything you want your provider to know?</legend>'
          '<label class="ps-sr" for="rq2">Note for your provider</label><textarea class="ps-ta" id="rq2" placeholder="Optional"></textarea></fieldset>')
    q3 = ('<fieldset class="ps-form-sec"><legend class="ps-h2">Your next order</legend>' + seg(["1 month", "3 months", "6 months"], i=1, label="Plan length")
          + '<dl class="ps-kv"><div><dt>Ships to</dt><dd>[street], [city], [state] · <a href="#">Change</a></dd></div>'
          '<div><dt>Price per order</dt><dd>$[price]</dd></div></dl></fieldset>')
    form = ('<form class="ps-card ps-stack--l" onsubmit="return false" style="gap: var(--gap)">' + q1 + q2 + q3
            + '<div class="ps-row"><button class="btn" type="button">Send to your provider</button><a class="link ps-comp" href="#">Cancel</a></div>'
            '<p class="ps-legal">Questions are DEMO ONLY: the real refill questions come from the clinical team (R-69). '
            '[charge line · operations]</p></form>')
    head = ('<div class="ps-stack" style="max-width: var(--layout-measure)"><h1 class="ps-h1">Request a refill.</h1>'
            '<p class="ps-sm">Three short questions. Your provider reviews your answers before your refill ships.</p></div>')
    d = portal_d("treatment", head + f'<div class="ps-cols"><div class="ps-c8">{form}</div><div class="ps-c4">'
                 f'<section class="ps-card ps-card--mist"><div class="ps-prod">{mark("tad")}<span class="ps-strong ps-comp">Tadalafil, [DOSE] tablets</span></div>'
                 '<p class="ps-cp">12 of 30 days left · review Dec 2</p></section></div></div>')
    m = portal_m("treatment", head + form.replace('<div class="ps-row"><button class="btn" type="button">Send to your provider</button><a class="link ps-comp" href="#">Cancel</a></div>', ''),
                 top=back_top("My treatment"), tabbar=False) + '<div class="ps-mbar"><button class="btn btn--bar" type="button">Send to your provider</button></div>'
    return screen(
        "s-refill", "9 · Refill request.",
        "A short form that goes to the provider: what changed, a note, the plan and the address. Answer options use the assessment's selected style (Deep Teal border), so no Yellow appears.",
        browser("app.[domain]/treatment/refill", d, "Form in 8 columns; the product summary on Mist beside it."),
        [phone(m, "Opened from My treatment; the tab bar hides for the task. The send button is a 48px bar (E-03).")],
        notes("Mobile and build notes", [
            "\"Yes, something changed\" opens one follow-up field below it (cross-fade 180ms), never a new page.",
            "Plan change here applies to the next order only; say so in the confirmation toast.",
            "After sending: a toast \"Sent to your provider.\" and the home timeline moves the review to the next step.",
            "Draft answers are kept if he leaves the page; nothing is sent until he presses the button.",
        ]))


def account():
    sub = ('<nav class="ps-subnav" aria-label="Account sections"><a href="#" aria-current="true">Notifications</a><a href="#">Profile</a>'
           '<a href="#">Privacy</a><a href="#">Payment</a><a href="#">Sign out</a></nav>')
    notif = ('<section class="ps-card" aria-labelledby="nt-h"><h2 class="ps-h2" id="nt-h">Notifications</h2><p class="ps-cp">Everything here is off until you turn it on.</p><div>'
             + setrow("Push notifications", "\"You have a new message\" or \"You have an update\". Nothing more.")
             + setrow("Text messages", "Delivery updates only.")
             + setrow("Sounds", "One setting for every sound the app plays.")
             + setrow("Newsletter", "Tips and news. We ask you to confirm by email first.")
             + '</div><p class="ps-note">' + ic("mail") + '<span>Service emails are always on: orders, safety and your provider. Subject lines never say what they are about.</span></p></section>')
    privacy = ('<section class="ps-card" aria-labelledby="pv-h"><h2 class="ps-h2" id="pv-h">Privacy</h2><div>'
               f'<a class="ps-linkrow" href="#">Who can see your records{ic("chevron-right")}</a>'
               f'<a class="ps-linkrow" href="#">Download your data{ic("chevron-right")}</a>'
               f'<a class="ps-linkrow" href="#">Delete your account{ic("chevron-right")}</a></div>'
               '<p class="ps-cp">You, your provider and the pharmacy that fills your prescription [legal to confirm].</p></section>')
    pay = ('<section class="ps-card" aria-labelledby="py-h"><h2 class="ps-h2" id="py-h">Payment</h2>'
           f'<div class="ps-row">{ic("card")}<span class="ps-comp">Card ending 4242 · expires 08/28 · DEMO</span></div>'
           '<a class="link ps-comp" href="#">Update card</a></section>')
    profile = ('<section class="ps-card" aria-labelledby="pf-h"><h2 class="ps-h2" id="pf-h">Profile</h2>'
               '<dl class="ps-kv"><div><dt>Name</dt><dd>Daniel R.</dd></div><div><dt>Email</dt><dd>d•••@example.com</dd></div>'
               '<div><dt>Phone</dt><dd>(•••) •••-0142</dd></div></dl><a class="link ps-comp" href="#">Edit profile</a></section>')
    d = portal_d("account", '<div class="ps-main-head"><h1 class="ps-h1">Account.</h1></div>'
                 f'<div class="ps-cols"><div class="ps-c3">{sub}</div><div class="ps-c6 ps-stack ps-stack--l">{notif}{privacy}</div>'
                 f'<div class="ps-c3 ps-stack ps-stack--l">{profile}{pay}</div></div>')
    lst = ('<section class="ps-card" style="padding-block: var(--space-2)"><div>'
           + "".join(f'<a class="ps-linkrow" href="#"><span class="ps-row">{ic(i)}{t}</span>{ic("chevron-right")}</a>' for i, t in
                     [("user", "Profile"), ("bell", "Notifications"), ("lock", "Privacy"), ("card", "Payment"), ("help", "Help"), ("log-out", "Sign out")])
           + '</div></section>')
    m1 = portal_m("account", '<h1 class="ps-h1">Account.</h1>' + lst)
    m2 = portal_m("account", notif, top=back_top("Account"))
    return screen(
        "s-account", "10 · Account and settings.",
        "Notifications are all off by default, with one switch for every sound. Privacy and payment sit one tap away. Personal details are masked.",
        browser("app.[domain]/account/notifications", d, "A section list on the left; the open section in the middle; profile and payment on the right."),
        [phone(m1, "Account is the fifth tab; Help lives here and in the top bar."), phone(m2, "Notifications: four switches, all off; the service-email note.")],
        notes("Mobile and build notes", [
            "Switch: 52 × 32, a generic UI pill (R-105). Off: Card ground, Slate border and thumb (3:1 or more). On: Deep Teal, Paper thumb. Thumb slides 220ms.",
            "Newsletter uses double opt-in (U-28): turning it on sends a confirmation email; the switch shows \"Waiting for your confirmation\".",
            "Delete your account opens a dialog that explains what is kept by law [legal] and asks for the password again.",
            "Masked values (email, phone) reveal only after a fresh sign-in.",
        ]))


def help_():
    acc = ('<div class="ps-acc">'
           + "".join(f'<details name="faq-{{k}}"{" open" if i == 0 else ""}><summary>{q}{ic("chevron-down")}</summary><p>{a}</p></details>' for i, (q, a) in enumerate([
               ("When will my order ship?", "After your provider approves it and the pharmacy fills it. [Shipping window · operations]. We never promise a time we cannot keep."),
               ("Can I pause or stop my plan?", "[Policy · operations]. You can change it in My treatment."),
               ("Who sees my answers?", "Your provider and the pharmacy that fills your prescription. Support never sees your health answers."),
               ("How do I change my address?", "Account, then Profile. A change applies to the next order that has not shipped.")]))
           + '</div>')
    cards = ('<div class="ps-g2">'
             '<article class="ps-card"><h2 class="ps-h2">A question about your treatment?</h2><p class="ps-sm">Your provider answers questions about doses, side effects and your plan.</p>'
             '<a class="btn" href="#" style="justify-self: start">Message your provider</a></article>'
             '<article class="ps-card"><h2 class="ps-h2">Orders, payment or your account?</h2><p class="ps-sm">Support answers [support hours · operations]. Support does not see your health answers.</p>'
             '<a class="btn btn--outline" href="#" style="justify-self: start">Message support</a></article></div>')
    sos = f'<p class="ps-note">{ic("alert-circle")}<span><b>If this is an emergency, call 911.</b> Messages are not watched around the clock [clinical and legal to confirm].</span></p>'
    search = f'<div class="ps-search" style="flex-basis: auto">{ic("search")}<label class="ps-sr" for="hs-{{k}}">Search help</label><input class="field__input" id="hs-{{k}}" type="search" placeholder="Search help"></div>'
    body = ('<div class="ps-main-head"><h1 class="ps-h1">Help.</h1></div>' + search + sos + cards
            + '<section class="ps-stack" aria-label="Common questions"><h2 class="ps-h2">Common questions</h2>' + acc + '</section>'
            + '<p class="ps-cp">Email: [support email · O-01] · Phone: [support phone · operations]</p>')
    d = portal_d("help", body.replace("{k}", "d"))
    m = portal_m("account", body.replace("{k}", "m"), top=back_top("Account"))
    return screen(
        "s-help", "11 · Help.",
        "Two clear doors: the provider for treatment, support for orders and account. The emergency line sits above both. Questions open one at a time.",
        browser("app.[domain]/help", d, "Search, the emergency line, two cards with the action on one line (R-98), then the questions."),
        [phone(m, "Opened from Account or the top bar. The cards stack; each button is full width.")],
        notes("Mobile and build notes", [
            "Accordion: native details elements in one named group, so only one answer is open (R-113). Chevron turns 180° in 220ms.",
            "The two help buttons differ in colour (Dark and Outline), so they never read as the same action (R-112).",
            "Search covers the questions only; it never searches messages or health data.",
        ]))
