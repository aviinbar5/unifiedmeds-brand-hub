"""States: empty, loading, error, offline, disabled. All data DEMO."""
from build_product_screens import browser, field, ic, loader, notes, phone, portal_d, portal_m, screen


def _empty():
    return ('<div class="empty"><b>No messages yet.</b><p>When your provider or the care team writes to you, it shows here.</p>'
            '<a class="btn btn--outline" href="#">Message your provider</a></div>')


def _loading():
    return ('<section class="ps-card" aria-busy="true" aria-label="Loading your orders"><div class="ps-skel" aria-hidden="true"><span class="skeleton skeleton--title"></span>'
            '<span class="skeleton"></span><span class="skeleton skeleton--short"></span></div>'
            f'<div class="ps-load">{loader("Loading your orders")}<span class="ps-cp">Loading your orders</span></div></section>')


def _error():
    return ('<div class="errpage" role="alert"><p class="errpage-title">We could not load your orders.</p>'
            '<p>Your information is safe. Check your connection and try again.</p><a class="btn" href="#" style="justify-self: start">Try again</a></div>')


def _offline():
    return (f'<div class="ps-stack"><p class="ps-banner" role="status">{ic("alert-circle")}<span><b>You are offline.</b> You can read what is here. '
            'New messages send when you are back online.</span></p><div class="ps-composer" style="border: 1px solid var(--color-line-base); border-radius: var(--radius-small)">'
            '<label class="ps-sr" for="off-{k}">Message</label><textarea class="ps-ta" id="off-{k}">Thanks, that helps.</textarea>'
            '<button class="btn" type="button">Send later</button></div></div>')


def _disabled():
    return ('<section class="ps-card" aria-labelledby="dis-{k}"><h2 class="ps-h2" id="dis-{k}">Request a refill</h2>'
            '<div class="ps-off">' + field("Note for your provider", "", "", "text", "Optional") + '</div>'
            '<button class="btn ps-off" type="button" aria-disabled="true" style="justify-self: start">Request a refill</button>'
            '<p class="ps-cp">Available from Nov 20 [refill window · operations]. A disabled control always says why.</p></section>')


def states():
    panel = lambda t, b: f'<section class="ps-stack"><span class="ps-lb">{t}</span>{b}</section>'  # noqa: E731
    grid = ('<div class="ps-cols">'
            f'<div class="ps-c6">{panel("Empty", _empty())}</div><div class="ps-c6">{panel("Loading", _loading())}</div>'
            f'<div class="ps-c6">{panel("Error", _error())}</div><div class="ps-c6">{panel("Offline", _offline().replace("{k}", "d"))}</div>'
            f'<div class="ps-c6">{panel("Disabled", _disabled().replace("{k}", "d"))}</div></div>')
    d = portal_d("messages", '<div class="ps-main-head"><h1 class="ps-h1">States.</h1><span class="ps-cp">Shown in the portal; the same patterns serve the funnel, admin and support.</span></div>' + grid)
    m1 = portal_m("messages", '<h1 class="ps-h1">Messages.</h1>' + _empty(), badge=0)
    m2 = portal_m("orders", '<h1 class="ps-h1">Orders.</h1>' + _loading() + _error(), badge=0)
    off_bar = (f'<p class="ps-banner ps-banner--bar" role="status">{ic("alert-circle")}<span><b>You are offline.</b> Messages send when you are back.</span></p>')
    m3 = portal_m("treatment", '<h1 class="ps-h1">My treatment.</h1>' + _disabled().replace("{k}", "m"),
                  top=None) .replace('<main class="ps-mmain">', off_bar + '<main class="ps-mmain">', 1)
    return screen(
        "x-states", "18 · Empty, loading, error, offline, disabled.",
        "Five states every screen needs. Each one says in words what is happening and what he can do. Loading shows the skeleton at once and the capsule loader (with the divider) after 400ms. Disabled is 40% opacity, no hover, always with the reason.",
        browser("app.[domain]/states", d, "All five in the portal content area. The loader is the core .cap-loader, drawn from tools/capsule_svg.py."),
        [phone(m1, "Empty: one sentence, one action. Never invented sample data."),
         phone(m2, "Loading, then error: the error keeps the page frame and offers one way forward."),
         phone(m3, "Offline: a full-width bar under the top bar. Disabled: field and button at 40%, the reason below.")],
        notes("Build notes", [
            "Loading: skeleton at once; the loader appears only after 400ms (--motion-loader-delay) and never flashes. It is the only loop (R-53). Reduced motion: half-filled and still.",
            "Error: role=\"alert\"; the page keeps its navigation. Field errors use the core field error (Coral border and dot, text in Deep Teal).",
            "Offline: role=\"status\"; drafts are kept; sending queues and says \"Send later\".",
            "Disabled: aria-disabled=\"true\" (stays focusable so the reason is announced), opacity 0.4 (--opacity-disabled), no hover or lift, the control keeps its own colours (R-42).",
        ]))
