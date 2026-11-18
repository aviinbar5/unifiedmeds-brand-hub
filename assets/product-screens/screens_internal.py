"""Clinical admin (provider side) and support. Desktop first. All data DEMO."""
from build_product_screens import (browser, field, flag, ic, internal_d, mark, notes, option, phone, pill, screen, select, tl)

QUEUE = [
    ("DR", "Daniel R.", "M-20417", "New assessment", "TX", 2, "Nov 17, 08:12", "1 h 30 min", "You"),
    ("MK", "Marcus K.", "M-20409", "Refill", "FL", 0, "Nov 17, 07:40", "2 h 02 min", "Unassigned"),
    ("AT", "Andre T.", "M-20398", "New assessment", "CA", 1, "Nov 17, 06:55", "2 h 47 min", "Unassigned"),
    ("PS", "Paul S.", "M-20377", "Member replied", "NY", 0, "Nov 16, 21:18", "12 h 24 min", "You"),
    ("RB", "Robert B.", "M-20361", "Refill", "TX", 0, "Nov 16, 19:03", "14 h 39 min", "A. Patel, MD"),
    ("JW", "James W.", "M-20352", "New assessment", "GA", 3, "Nov 16, 17:47", "15 h 55 min", "Unassigned"),
    ("CH", "Chris H.", "M-20340", "Plan change", "WA", 0, "Nov 16, 15:20", "18 h 22 min", "Unassigned"),
]


def queue():
    rows = []
    for i, (av, name, mid, req, st, fl, sub, wait, who) in enumerate(QUEUE):
        f = flag(f"{fl} flag{'s' if fl > 1 else ''}") if fl else '<span class="ps-cp">None</span>'
        sel = ' class="is-sel"' if i == 0 else ""
        rows.append(f'<tr{sel}><td><span class="ps-who"><span class="ps-av ps-av--s">{av}</span><span class="ps-stack ps-stack--s"><b>{name}</b>'
                    f'<span class="ps-cp">{mid}</span></span></span></td><td>{req}</td><td>{st}</td><td>{f}</td><td>{sub}</td><td>{wait}</td><td>{who}</td>'
                    f'<td><a class="link" href="#">Review</a></td></tr>')
    chips = ('<div class="ps-chips" role="group" aria-label="Filter">'
             + "".join(f'<button class="chip" type="button" aria-pressed="{"true" if k == 0 else "false"}">{t}<b>{n}</b></button>' for k, (t, n) in enumerate(
                 [("All", 12), ("New assessment", 7), ("Refill", 4), ("Member replied", 1), ("Flagged", 3)])) + '</div>')
    tools = (f'<div class="ps-tools"><div class="ps-search">{ic("search")}<label class="ps-sr" for="qs">Search members</label>'
             '<input class="field__input" id="qs" type="search" placeholder="Search by name or member ID"></div>'
             f'<button class="btn btn--outline btn--icon" type="button">Sort: waiting longest{ic("chevron-down", "btn-icon")}</button>'
             f'<span class="ps-push-r">{pill("Review target: [service level · clinical ops]", "info", "clock")}</span></div>')
    table = (f'<div class="ps-tblw"><table class="ps-tbl"><thead><tr><th scope="col">Member</th><th scope="col">Request</th><th scope="col">State</th>'
             f'<th scope="col">Flags</th><th scope="col">Submitted</th><th scope="col">Waiting</th><th scope="col">Assigned</th><th scope="col"><span class="ps-sr">Action</span></th></tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table></div>')
    pager = (f'<div class="ps-pager"><span class="ps-cp">Showing 7 of 12 · Only members in states where you are licensed</span>'
             f'<span class="ps-row"><button class="ps-ib ps-ib--line" type="button" aria-label="Previous page">{ic("chevron-left")}</button>'
             f'<button class="ps-ib ps-ib--line" type="button" aria-label="Next page">{ic("chevron-right")}</button></span></div>')
    d = internal_d("clinical", "queue", '<div class="ps-main-head"><h1 class="ps-h1">Review queue.</h1></div>' + tools + chips + table + pager)
    mlist = "".join(f'<a class="ps-linkrow" href="#"><span class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">{name} · {req}</b>'
                    f'<span class="ps-cp">{mid} · {st} · waiting {wait}</span></span>{flag(str(fl)) if fl else ic("chevron-right")}</a>' for av, name, mid, req, st, fl, sub, wait, who in QUEUE[:5])
    # U-29 (Q86): everything works on a phone, the same as on a computer
    mchips = ('<div class="ps-chips" role="group" aria-label="Filter">'
              + "".join(f'<button class="chip" type="button" aria-pressed="{"true" if k == 0 else "false"}">{t}<b>{n}</b></button>' for k, (t, n) in enumerate(
                  [("All", 12), ("New", 7), ("Refill", 4), ("Flagged", 3)])) + '</div>')
    m = (f'<header class="ps-top" style="background: var(--color-brand-teal-deep); color: var(--color-text-on-dark)"><span class="ps-lb" style="color: var(--color-text-on-dark-muted)">Clinical · internal</span>'
         f'<span class="ps-comp">Jordan Lee, NP</span></header><main class="ps-mmain"><h1 class="ps-h1">Review queue.</h1>'
         + mchips +
         f'<section class="ps-card" style="padding-block: var(--space-2)"><div>{mlist}</div></section>'
         f'<p class="ps-cp">Showing 5 of 12 · Only members in states where you are licensed</p></main>')
    return screen(
        "a-queue", "12 · Review queue.",
        "Every request waiting for a provider, oldest first. Dense, but on the type scale: rows 48px, text 14/21, labels 12/16. Flags are Wash Yellow pills with an icon; Coral stays for errors.",
        browser("clinical.[domain]/queue", d, "Dark side nav marks an internal tool. The selected row stays Mist after returning from a review."),
        [phone(m, "The full queue on a phone (U-29): filters as chips, rows of 44px or more, a tap opens the review with every action of the desktop.")],
        notes("Tablet and build notes", [
            "1024 to 1439: the Assigned column hides (shown in the row detail); the side nav stays 216px.",
            "768 to 1023: the side nav becomes a 72px icon rail with tooltips; Submitted and State merge into one column.",
            "Below 768: the full queue as a list, filters as chips that wrap; a row opens the review (screen 13, mobile). Same actions and permissions as on a computer.",
            "The queue shows only members in states where the signed-in provider is licensed.",
            "Waiting time counts from submission; a target is shown only once clinical operations set one (R-68).",
        ]))


def review():
    member = ('<section class="ps-card" aria-labelledby="mb-h"><div class="ps-who"><span class="ps-av">DR</span><span class="ps-stack ps-stack--s">'
              '<h2 class="ps-h2" id="mb-h">Daniel R.</h2><span class="ps-cp">M-20417 · DEMO</span></span></div>'
              '<dl class="ps-kv ps-kv--stack"><div><dt>Age</dt><dd>44</dd></div><div><dt>State of residence</dt><dd>TX · you are licensed here</dd></div>'
              f'<div><dt>Identity check</dt><dd>{pill("Verified", "ok", "check")} [vendor]</dd></div>'
              '<div><dt>Allergies</dt><dd>None reported</dd></div><div><dt>Current medicines</dt><dd>[as answered]</dd></div>'
              '<div><dt>Earlier orders</dt><dd>None</dd></div></dl>'
              f'<a class="link ps-comp" href="#">Message history (0)</a></section>')
    qa = [("Main reason for this assessment", "[answer]", None), ("How long has this been going on?", "[answer]", None),
          ("Current medicines", "[medicine name], [medicine name]", "Matches review rule [rule name · clinical team]"),
          ("Heart and blood pressure history", "[answer]", "Answer needs review [rule name · clinical team]"),
          ("Recent blood pressure reading", "[value, self-reported]", None), ("Allergies to medicines", "None", None),
          ("Anything else for the provider?", "\"[free text from the member]\"", None)]
    rows = "".join(f'<div class="ps-qa{" is-flag" if fl else ""}"><span class="q">{q}</span><span class="a">{a}{flag(fl) if fl else ""}</span></div>' for q, a, fl in qa)
    answers = (f'<section class="ps-card ps-card--flat" aria-labelledby="an-h"><div class="ps-sechead ps-row ps-between"><h2 class="ps-h2" id="an-h">Assessment answers</h2>'
               f'<span class="ps-row"><span class="ps-cp">Submitted Nov 17, 08:12</span>{pill("2 flags", "att", "alert-triangle")}</span></div>{rows}</section>')
    decide = ('<section class="ps-card" aria-labelledby="dc-h"><h2 class="ps-h2" id="dc-h">Your decision</h2>'
              f'<div class="ps-prod">{mark("tad")}<span class="ps-comp"><b class="ps-strong">Requested:</b> Tadalafil, [DOSE] · 3-month plan</span></div>'
              '<div class="ps-stack" role="radiogroup" aria-label="Decision">' + option("Approve and prescribe", True) + option("Ask the member a question") + option("Decline") + '</div>'
              + select("Medicine", "Tadalafil") + '<div class="ps-fields2">' + select("Strength", "[DOSE]") + field("Quantity", "[qty]") + '</div>'
              + '<div class="ps-fields2">' + field("Refills", "[n]") + select("Pharmacy", "[partner pharmacy]") + '</div>'
              + '<label class="field"><span class="field__label">Directions for the label</span><textarea class="ps-ta" placeholder="[directions · provider]"></textarea></label>'
              + '<label class="ps-check"><input type="checkbox" checked>I reviewed both flags.</label>'
              + '<button class="btn ps-full" type="button">Sign and send to pharmacy</button>'
              + '<p class="ps-legal">Your decision, signature and time go to the audit trail. The member sees: "Your provider approved your plan."</p></section>')
    crumb = f'<nav class="ps-crumb" aria-label="Breadcrumb"><a href="#">Review queue</a>{ic("chevron-right", "ps-ic ps-ic--s")}<span>M-20417 · New assessment</span></nav>'
    d = internal_d("clinical", "queue", crumb + '<div class="ps-main-head"><h1 class="ps-h1">Assessment review.</h1>'
                   f'<button class="btn btn--outline btn--icon" type="button">Show flagged only{ic("filter", "btn-icon")}</button></div>'
                   f'<div class="ps-rev">{member}{answers}{decide}</div>')
    ask = ('<section class="ps-card" aria-labelledby="as-h"><h2 class="ps-h2" id="as-h">Ask the member a question</h2>'
           '<div class="ps-stack" role="radiogroup">' + option("Approve and prescribe") + option("Ask the member a question", True) + option("Decline") + '</div>'
           + select("Start from a template", "Clarify a medicine") + '<label class="field"><span class="field__label">Your question</span><textarea class="ps-ta">Can you tell me the strength of [medicine] you take? [DEMO]</textarea></label>'
           '<button class="btn ps-full" type="button">Send question</button><p class="ps-legal">The case moves to "Waiting for member". The member gets a push and an email: "You have an update."</p></section>')
    dec = ('<section class="ps-card" aria-labelledby="de-h"><h2 class="ps-h2" id="de-h">Decline</h2>'
           '<div class="ps-stack" role="radiogroup">' + option("Approve and prescribe") + option("Ask the member a question") + option("Decline", True) + '</div>'
           + select("Reason (internal)", "[reason list · clinical team]") + '<label class="field"><span class="field__label">Note to the member</span><textarea class="ps-ta">[template · clinical and legal]</textarea></label>'
           '<label class="ps-check"><input type="checkbox">Suggest an in-person visit</label><button class="btn ps-full" type="button">Decline and notify</button>'
           '<p class="ps-legal">Refund follows [refund rule · operations]. The member reads the note in Messages, never in an email.</p></section>')
    side = f'<div class="ps-cv ps-cv--free"><div class="ps-panels">{ask}{dec}</div></div>'
    # U-29 (Q86): decisions, prescriptions and signing also work on a phone
    mtop = (f'<header class="ps-top" style="background: var(--color-brand-teal-deep); color: var(--color-text-on-dark)">'
            f'<a class="ps-ib" href="#" aria-label="Back to the queue" style="color: inherit">{ic("chevron-left")}</a>'
            '<span class="ps-lb" style="color: var(--color-text-on-dark-muted)">Clinical · internal</span></header>')
    mmember = ('<section class="ps-card" aria-labelledby="mb-hm"><div class="ps-who"><span class="ps-av">DR</span><span class="ps-stack ps-stack--s">'
               '<h2 class="ps-h2" id="mb-hm">Daniel R.</h2><span class="ps-cp">M-20417 · 44 · TX, you are licensed here</span></span></div>'
               f'<div class="ps-row">{pill("ID verified", "ok", "check")}<a class="link ps-comp" href="#">Message history (0)</a></div></section>')
    manswers = (f'<section class="ps-card ps-card--flat" aria-labelledby="an-hm"><div class="ps-sechead ps-row ps-between"><h2 class="ps-h2" id="an-hm">Answers</h2>'
                f'{pill("2 flags", "att", "alert-triangle")}</div>{rows}</section>')
    mdecide = ('<section class="ps-card" aria-labelledby="dc-hm"><h2 class="ps-h2" id="dc-hm">Your decision</h2>'
               f'<div class="ps-prod">{mark("tad")}<span class="ps-comp"><b class="ps-strong">Requested:</b> Tadalafil, [DOSE] · 3-month plan</span></div>'
               '<div class="ps-stack" role="radiogroup" aria-label="Decision">' + option("Approve and prescribe", True) + option("Ask the member a question") + option("Decline") + '</div>'
               + select("Medicine", "Tadalafil") + select("Strength", "[DOSE]") + '<div class="ps-fields2">' + field("Quantity", "[qty]") + field("Refills", "[n]") + '</div>'
               + select("Pharmacy", "[partner pharmacy]")
               + '<label class="field"><span class="field__label">Directions for the label</span><textarea class="ps-ta" placeholder="[directions · provider]"></textarea></label>'
               + '<label class="ps-check"><input type="checkbox" checked>I reviewed both flags.</label>'
               + '<p class="ps-legal">Your decision, signature and time go to the audit trail. Signing on a phone asks for [a fresh sign-in · engineering].</p></section>')
    mrev = (mtop + '<main class="ps-mmain"><h1 class="ps-h1">Assessment review.</h1>'
            + f'<button class="btn btn--outline btn--icon" type="button">Show flagged only{ic("filter", "btn-icon")}</button>'
            + mmember + manswers + mdecide + '</main>'
            + '<div class="ps-mbar"><button class="btn btn--bar" type="button">Sign and send to pharmacy</button></div>')
    return screen(
        "a-review", "13 · Assessment review with flags.",
        "Member summary, the answers with flags, the decision panel. Approve, ask or decline is one choice; the panel below changes with it, and there is one button. Flags never decide; the provider does.",
        browser("clinical.[domain]/review/M-20417", d, "Three columns: 288 · flexible · 384. Flagged answers carry a Deep Teal bar and a Wash Yellow pill."),
        [phone(mrev, "The full review on a phone (U-29): member, answers with flags, the decision. The one button sits in a sticky bar (48px, E-03); Ask and Decline swap the panel as on desktop.")],
        side=('<div class="ps-stack"><p class="cap">The decision panel in its other two states (desktop size).</p>' + side
                  + notes("Tablet and build notes", [
                      "1024 to 1439: the member summary folds into a bar above the answers (name, age, state, ID check); answers and decision stay side by side.",
                      "768 to 1023: one column; the decision panel follows the answers and its button sticks to the bottom of the screen.",
                      "Below 768: the same single column at phone size, with every action of the desktop (U-29). The member summary shrinks to one card.",
                      "Flags come from rules the clinical team writes; the hub never invents one (R-69). Each flag names its rule.",
                      "\"I reviewed both flags\" is required when flags exist; the button stays disabled (40% opacity) until it is checked.",
                      "Keyboard: J and K move between flagged answers; every shortcut also has a visible button.",
                  ]) + '</div>'))


def prescription():
    steps = [("done", "Signed", "Nov 17, 09:41"), ("done", "Sent to pharmacy", "Nov 17, 09:41"), ("next", "Received", "Waiting for [pharmacy]"),
             ("", "Filled", ""), ("", "Shipped", "")]
    summ = ('<section class="ps-card" aria-labelledby="rx-h"><div class="ps-row ps-between"><h2 class="ps-h2" id="rx-h">Prescription RX-88213 · DEMO</h2>'
            f'{pill("Sent", "info", "check")}</div><dl class="ps-kv"><div><dt>Member</dt><dd>Daniel R. · M-20417</dd></div>'
            '<div><dt>Medicine</dt><dd>Tadalafil, [DOSE] tablets</dd></div><div><dt>Quantity and refills</dt><dd>[qty] · [n] refills</dd></div>'
            '<div><dt>Directions</dt><dd>[directions · provider]</dd></div><div><dt>Pharmacy</dt><dd>[partner pharmacy] · [eRx network]</dd></div>'
            '<div><dt>Prescriber</dt><dd>Jordan Lee, NP · [licence number]</dd></div></dl></section>')
    status = f'<section class="ps-card" aria-labelledby="st-h"><h2 class="ps-h2" id="st-h">Status</h2>{tl(steps, vertical=True)}</section>'
    err = (f'<div class="toast toast--error" role="alert"><span class="toast-icon">{ic("alert-circle")}</span><p><b>The pharmacy has not confirmed yet.</b> '
           'We try again automatically [retry rule · engineering]. You can resend now or call the pharmacy.</p><button class="toast-close" type="button" aria-label="Close">'
           f'{ic("close")}</button></div>')
    acts = '<div class="ps-row"><button class="btn" type="button">Resend to pharmacy</button><a class="link ps-comp" href="#">Cancel prescription</a></div>'
    d = internal_d("clinical", "rx", '<div class="ps-main-head"><h1 class="ps-h1">Prescription sent.</h1></div>'
                   f'<div class="ps-cols"><div class="ps-c7 ps-stack ps-stack--l">{summ}</div><div class="ps-c5 ps-stack ps-stack--l">{status}{err}{acts}</div></div>')
    return screen(
        "a-rx", "14 · Prescription to the pharmacy.",
        "After signing: what was sent, where, and whether the pharmacy received it. A failed hand-off is an error toast with a way out, never a silent wait.",
        browser("clinical.[domain]/prescriptions/RX-88213", d, "Summary on the left; the transmission status and the error state on the right."),
        (), side=notes("Tablet and build notes", [
            "The status follows the pharmacy's messages; each step shows the time it happened, never a forecast.",
            "Cancel prescription asks for a reason and notifies the pharmacy; it is logged in the audit trail.",
            "Tablet: one column, status first.",
            "The member never sees the prescription number or the pharmacy network; the portal says \"At the pharmacy\".",
        ]))


def audit():
    ev = [("Nov 17, 09:41:22", "Jordan Lee, NP", "Sent prescription", "RX-88213 to [partner pharmacy]"),
          ("Nov 17, 09:41:05", "Jordan Lee, NP", "Signed prescription", "RX-88213"),
          ("Nov 17, 09:40:51", "Jordan Lee, NP", "Approved", "Assessment A-55120"),
          ("Nov 17, 09:32:10", "Jordan Lee, NP", "Viewed assessment", "A-55120, 2 flags shown"),
          ("Nov 17, 09:31:58", "Jordan Lee, NP", "Opened member record", "M-20417"),
          ("Nov 17, 08:12:40", "System", "Flags added", "2 rules [rule names · clinical team]"),
          ("Nov 17, 08:12:39", "Daniel R. (member)", "Submitted assessment", "A-55120"),
          ("Nov 16, 18:03:11", "Sam Ortiz, Support", "Viewed order", "#10482 (no health data)")]
    rows = "".join(f'<tr><td>{t}</td><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for t, a, b, c in ev)
    tools = ('<div class="ps-tools">' + select("Member", "M-20417") + select("Who", "Everyone") + select("Action", "All actions")
             + select("Dates", "Last 7 days") + '</div>')
    d = internal_d("clinical", "audit", '<div class="ps-main-head"><h1 class="ps-h1">Audit trail.</h1>'
                   f'<button class="btn btn--outline btn--icon" type="button">Export CSV{ic("document", "btn-icon")}</button></div>'
                   f'<p class="ps-note">{ic("lock")}<span>Read only. Entries cannot be edited or deleted. Kept for [retention period · legal].</span></p>' + tools
                   + f'<div class="ps-tblw"><table class="ps-tbl"><thead><tr><th scope="col">Time (local)</th><th scope="col">Who</th><th scope="col">Action</th><th scope="col">Record</th></tr></thead><tbody>{rows}</tbody></table></div>')
    return screen(
        "a-audit", "15 · Audit trail.",
        "Every view, decision and hand-off, newest first, for one member or for everyone. Support views appear too, marked with no health data.",
        browser("clinical.[domain]/audit?member=M-20417", d, "Filters are 50px selects in a row; the table uses tabular figures for times."),
        (), side=notes("Tablet and build notes", [
            "Times are local with the zone in the export; seconds are shown because order matters.",
            "Tablet: Record wraps under Action; filters wrap to two rows.",
            "Export is logged as its own event.",
        ]))


def support_inbox():
    tickets = [("Where is my order?", "Shipping", "Marcus K.", "18 min", True), ("Card was declined", "Billing", "Paul S.", "42 min", False),
               ("Question about my dose", "Clinical, escalate", "Daniel R.", "1 h 05 min", False), ("Change my address", "Account", "Chris H.", "2 h 10 min", False),
               ("Cancel my plan", "Account", "James W.", "3 h 30 min", False)]
    lst = "".join(f'<a class="ps-thr" href="#"{" aria-current=\"true\"" if on else ""}><span class="ps-av ps-av--s">{n.split()[0][0]}{n.split()[1][0]}</span>'
                  f'<span class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">{s}</b><span class="ps-cp">{n} · {w}</span><span>{pill(t, "att" if "escalate" in t else "")}</span></span>'
                  f'<span class="ps-unread"{"" if on else " hidden"}></span></a>' for s, t, n, w, on in tickets)
    tabs = ('<div class="tabs" role="tablist" aria-label="Inbox"><button role="tab" aria-selected="true" type="button">Open · 9</button>'
            '<button role="tab" aria-selected="false" type="button">Waiting on member · 4</button><button role="tab" aria-selected="false" type="button">Escalated · 2</button>'
            '<button role="tab" aria-selected="false" type="button">Closed</button></div>')
    bubbles = ('<div class="ps-bubbles" role="log" aria-label="Conversation"><span class="ps-day">Today</span>'
               '<div class="ps-b ps-b--them">Hi, my order shows shipped but the tracking has not moved since Friday.</div><span class="ps-bmeta">Marcus K. · 18 min ago</span></div>')
    menu = ('<div class="overlay ps-menu" style="left: var(--space-6); bottom: calc(var(--space-24) - var(--space-2))" role="menu" aria-label="Macros">'
            '<span class="ps-lb">Macros</span><a class="is-hot" href="#" role="menuitem">Order status and tracking</a><a href="#" role="menuitem">Plain packaging</a>'
            '<a href="#" role="menuitem">Update payment card</a><a href="#" role="menuitem">Change address</a><a href="#" role="menuitem">Clinical question: escalate</a></div>')
    composer = (f'<div class="ps-composer" style="position: relative">{menu}<button class="btn btn--outline btn--icon" type="button" aria-expanded="true">Macros{ic("chevron-up", "btn-icon")}</button>'
                '<label class="ps-sr" for="sup-r">Reply</label><textarea class="ps-ta" id="sup-r">Hi Marcus, thanks for writing. I checked your order: [macro text · DEMO]</textarea><button class="btn" type="button">Send</button></div>')
    conv = (f'<section class="ps-conv" aria-label="Ticket"><div class="ps-conv-h ps-between"><div class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">Where is my order?</b>'
            f'<span class="ps-cp">Ticket T-3307 · Shipping · opened by Marcus K. · DEMO</span></div>'
            f'<button class="btn btn--outline btn--icon" type="button">Escalate to a provider{ic("chevron-right", "btn-icon")}</button></div>{bubbles}{composer}</section>')
    mem = (f'<aside class="ps-mem" aria-label="Member"><div class="ps-who"><span class="ps-av">MK</span><span class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">Marcus K.</b><span class="ps-cp">M-20409</span></span></div>'
           '<dl class="ps-kv ps-kv--stack"><div><dt>Latest order</dt><dd>#10517 · Shipped Nov 14</dd></div><div><dt>Carrier</dt><dd>[carrier] · [tracking number]</dd></div>'
           '<div><dt>Ships to</dt><dd>[city], [state]</dd></div><div><dt>Plan</dt><dd>3 months</dd></div><div><dt>Treatment</dt><dd>Hidden</dd></div></dl>'
           f'<p class="ps-wall">{ic("lock")}<span>Behind the PHI wall: treatment, answers and provider notes. Support sees orders, shipping and account only.</span></p></aside>')
    d = internal_d("support", "inbox", '<div class="ps-main-head"><h1 class="ps-h1">Inbox.</h1></div>' + tabs
                   + f'<div class="ps-inbox"><nav class="ps-threads" aria-label="Tickets">{lst}</nav>{conv}{mem}</div>')
    mlist = "".join(f'<a class="ps-linkrow" href="#"><span class="ps-stack ps-stack--s"><b class="ps-strong ps-comp">{s}</b><span class="ps-cp">{n} · {t} · {w}</span></span>{ic("chevron-right")}</a>' for s, t, n, w, on in tickets)
    m = (f'<header class="ps-top" style="background: var(--color-brand-teal-deep)"><span class="ps-lb" style="color: var(--color-text-on-dark-muted)">Support · internal</span>'
         f'<span class="ps-comp" style="color: var(--color-text-on-dark)">Sam Ortiz</span></header><main class="ps-mmain"><h1 class="ps-h1">Inbox.</h1>'
         f'<section class="ps-card" style="padding-block: var(--space-2)"><div>{mlist}</div></section></main>')
    return screen(
        "u-inbox", "16 · Support inbox, ticket and macros.",
        "Three panes: tickets, the open ticket, the member's order details. The macro menu is open over the composer. The PHI wall is visible, so agents know what they cannot see and why.",
        browser("support.[domain]/inbox/T-3307", d, "Ticket list 360px, conversation, member panel 288px. Topic pills: Wash Yellow only for tickets that need a provider."),
        [phone(m, "Everything works on a phone (U-29): read, reply, macros in a bottom sheet, escalate (screen 17).")],
        notes("Tablet and build notes", [
            "1024 to 1439: the member panel becomes a drawer opened from the ticket header.",
            "768 to 1023: list and ticket are separate views, like the member portal on mobile.",
            "Macros fill the composer; the agent always edits before sending. Macros never contain health advice.",
            "A ticket that mentions symptoms, doses or side effects shows the escalate prompt; support never answers it.",
        ]))


def escalation():
    form = ('<div class="ps-scrim"></div><div class="overlay ps-dlg" role="dialog" aria-modal="true" aria-labelledby="esc-h">'
            '<h2 class="ps-h2" id="esc-h">Escalate to a provider</h2><p class="ps-sm">The ticket moves to the clinical queue. Support keeps the order side.</p>'
            + select("Reason", "Question about treatment or dose")
            + '<label class="field"><span class="field__label">Note for the provider</span><textarea class="ps-ta">Member asks about his dose. Ticket T-3312. [DEMO]</textarea></label>'
            + '<p class="ps-note">' + ic("mail") + '<span>The member sees in Messages: "A provider will reply here." Push and email say only "You have an update."</span></p>'
            + '<p class="ps-note">' + ic("alert-circle") + '<span>Possible side effect? Use the side effect reason; it starts [adverse event process · clinical and legal].</span></p>'
            + '<div class="ps-row"><button class="btn" type="button">Escalate</button><button class="btn btn--outline" type="button">Cancel</button></div></div>')
    behind = ('<div class="ps-main-head"><h1 class="ps-h1">Inbox.</h1></div><div class="ps-card" style="min-height: calc(var(--space-24) * 6)">'
              '<div class="ps-skel" aria-hidden="true"><span class="skeleton skeleton--title"></span><span class="skeleton"></span><span class="skeleton skeleton--short"></span></div></div>')
    d = internal_d("support", "inbox", behind) + form
    m = (f'<header class="ps-top" style="background: var(--color-brand-teal-deep)"><span class="ps-lb" style="color: var(--color-text-on-dark-muted)">Support · internal</span></header>'
         f'<main class="ps-mmain" style="min-height: calc(var(--space-24) * 7)"><h1 class="ps-h1">Ticket T-3312.</h1></main>' + form)
    return screen(
        "u-escalate", "17 · Escalation to a provider.",
        "A dialog over the ticket: the reason, a note, and exactly what the member will see. The two buttons differ in colour (R-112).",
        browser("support.[domain]/inbox/T-3312/escalate", d, "Dialog 528px wide, the single shadow (R-36), a Teal Deep scrim at 45%."),
        [phone(m, "On a phone the dialog fills the width with 12px margins; buttons stack only if their labels do not fit.")],
        notes("Build notes", [
            "Focus moves into the dialog and returns to the Escalate button when it closes; Esc cancels.",
            "The escalated ticket shows in both inboxes, with one owner on each side.",
            "Support never forwards the member's health words into an email.",
        ]))
