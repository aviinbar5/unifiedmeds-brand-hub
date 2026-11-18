"""unifiedmeds Social overview: wrote the first version of src/social.html (17.11.2026).

RETIRED at the hub merge (18.11.2026): src/social.html now carries decisions and statuses edited by hand.
Do not run this script: it would overwrite them. Kept for reference only.
"""
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_kit_pages as K  # noqa: E402

EXT = HERE.parents[2]
ARCHIVE = EXT.parent / "drafts" / "archive-social" / "social-src-2026-11-16.html"
E = html.escape
MAN = json.loads((HERE / "manifest.json").read_text())

old = ARCHIVE.read_text().splitlines()
end = old.index("</style>")
old_css = [l for l in old[1:end] if l.strip() and ".post" not in l
           and not l.strip().startswith("@media (max-width: 1023px)")]   # the post styles move to the kits
old_avatar_options = old[59] + "\n" + old[60]          # the two option galleries (16.11.2026)
old_covers = "\n".join(old[65:75])                     # the cover options, four platforms each

CSS = "<style>\n" + "\n".join(old_css) + """
  /* 17.11.2026: the cover capsule is the logo's own asymmetric shape (file), never a rounded rectangle */
  .cover::after { border: 0; border-radius: 0; height: auto; aspect-ratio: 614.73 / 223.66; background: url('assets/social/shared/capsule-outline-wash.svg') center / 100% 100% no-repeat; }
  .cover--paper::after { background-image: url('assets/social/shared/capsule-outline-field.svg'); }
  .r-li::after { height: auto; top: 20%; width: 30%; right: -10%; }
  @media (max-width: 1023px) { .social-row { grid-template-columns: minmax(0, 1fr); } }
  .so-cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-4); }
  .so-card { display: grid; grid-template-rows: auto auto 1fr auto; gap: var(--space-2); padding: var(--space-4); border: 1px solid var(--color-line-base); border-radius: var(--radius-card); background: var(--color-surface-card); color: var(--color-text-primary); text-decoration: none; min-height: var(--size-tap-min); }
  .so-card img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: contain; border-radius: var(--radius-xs); background: var(--color-surface-mist); }
  .so-card b { font: 400 var(--type-desktop-card-serif-size) / var(--type-desktop-card-serif-line) var(--font-family-serif); color: var(--color-text-strong); }
  .so-card span { color: var(--color-text-secondary); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  .so-card em { font-style: normal; color: var(--color-text-link); text-decoration: underline; font: 500 var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  .so-card:hover, .so-card:focus-visible { background: var(--color-brand-deep-teal); border-color: var(--color-brand-deep-teal); }
  .so-card:hover b, .so-card:hover em, .so-card:focus-visible b, .so-card:focus-visible em { color: var(--color-text-on-dark); }
  .so-card:hover span, .so-card:focus-visible span { color: var(--color-text-on-dark-muted); }
  .so-ab { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-6); }
  .so-ab figure { margin: 0; display: grid; gap: var(--space-3); align-content: start; }
  .so-ab .so-av { display: flex; align-items: flex-end; gap: var(--space-4); }
  .so-ab .so-av img { display: block; border-radius: 50%; border: 1px solid var(--color-line-base); }
  .so-ab figcaption { color: var(--color-text-secondary); font: var(--type-desktop-compact-weight) var(--type-desktop-compact-size) / var(--type-desktop-compact-line) var(--font-family-sans); }
  .so-ab figcaption b { color: var(--color-text-strong); }
  .so-l { width: calc(var(--space-24) + var(--space-12)); height: calc(var(--space-24) + var(--space-12)); } .so-m { width: var(--space-12); height: var(--space-12); } .so-s { width: var(--space-8); height: var(--space-8); }
  .so-rules { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-4); }
  .so-rules .rule b { display: block; }
  .rule > .status { justify-self: start; }
  @media (max-width: 1023px) { .so-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 767px) { .so-cards, .so-ab, .so-rules { grid-template-columns: minmax(0, 1fr); } }
</style>
"""

CARDS = [
    ("social-facebook.html", "Facebook", "Page, cover, feed posts, link share, story, event cover, ad-ready post.", "assets/social/facebook/facebook-cover-a.png"),
    ("social-instagram.html", "Instagram and Threads", "Profile, grid rhythm, posts, carousel, story, reel cover, highlights, Threads card.", "assets/social/instagram/instagram-carousel-b-1.png"),
    ("social-tiktok.html", "TikTok", "Profile, video cover with UI safe zones, on-screen text, two storyboards.", "assets/social/tiktok/tiktok-cover-a.png"),
    ("social-youtube.html", "YouTube", "Channel banner, thumbnails, Shorts cover, end screen, lower third, watermark.", "assets/social/youtube/youtube-banner-a.png"),
    ("social-linkedin.html", "LinkedIn", "Company logo, cover, posts, document carousel, careers tab, employee banner.", "assets/social/linkedin/linkedin-cover-a.png"),
    ("social-x.html", "X", "Profile, header, post images, link card.", "assets/social/x/x-header-b.png"),
]

SHARED_RULES = [
    ("Two options, one logic.", "Every asset comes as Option A (calm, editorial: a photo and a serif line) and Option B (graphic: the capsule kit and colour). Avi picks per asset; once picked, the other is archived."),
    ("Phone first.", "Most people meet every channel on a phone. Each asset is checked at 390 wide: type stays readable (serif from about 21 px on screen, Inter from about 11 px), nothing important sits in the platform's own overlays."),
    ("One profile picture everywhere.", "The same mark on every channel, from the shared pair below. Never the full seal or the wordmark at avatar size."),
    ("Safe zones before style.", "Type and logo live inside the safe zone of each platform. A capsule may be cropped by the edge; if it would land under a platform button, it moves."),
    ("The legal line where an assessment is offered.", "\"Assessment only. Not a diagnosis.\" in the art of every ad and on the last card of a carousel that offers the assessment, and in the caption of every organic post that links to it (R-63)."),
    ("Yellow once, for the action.", "At most one Yellow element per asset, only for \"Get started\" (R-11, R-55). Organic posts usually have none."),
    ("Two capsule shapes per surface at most.", "Type never sits on a shape, and a face is never covered by type, a card or a shape (R-33)."),
    ("No claims, no medicine names, no proof.", "No benefit claims, statistics, prices, reviews, before and after, or prescription names in any social asset or caption (R-58, R-65, R-67)."),
    ("Discretion in public.", "No condition or symptom hashtags. Never ask about health in comments; move to a private message, then to the assessment. Never tag or name a member."),
    ("Captions and alt text, always.", "Video carries captions for every spoken word; every image has alt text that describes it plainly."),
]

S2_SIZES = [
    ("TikTok", "Profile picture", "400 × 400 (shown from 200)", "1:1, circle", "Circle on the profile", "Same, smaller"),
    ("TikTok", "Video cover", "1080 × 1920", "9:16", "Profile grid crop 3:4", "Full screen; keep x 60 to 920, y 240 to 1440"),
    ("TikTok", "On-screen text (title, caption, end card)", "1080 × 1920", "9:16", "Video player", "Inside x 60 to 920, y 160 to 1440 (right rail and caption clear)"),
    ("YouTube", "Profile picture", "800 × 800", "1:1, circle", "Circle on the channel", "Same, smaller"),
    ("YouTube", "Channel banner", "2560 × 1440", "16:9", "Desktop shows 2560 × 423", "Phone shows 1546 × 423 centred (the safe area)"),
    ("YouTube", "Thumbnail", "1280 × 720", "16:9", "Home and search", "About 168 wide in lists; bottom right under the duration badge"),
    ("YouTube", "Shorts cover", "1080 × 1920", "9:16", "Shorts shelf", "Full screen; keep x 60 to 880, y 200 to 1400"),
    ("YouTube", "End screen, lower third, title card", "1920 × 1080", "16:9", "In the video", "Title-safe 1728 × 972"),
    ("YouTube", "Watermark", "150 × 150", "1:1", "Bottom right of the player", "Same"),
    ("LinkedIn", "Company logo", "400 × 400", "1:1, square", "Square on the page", "Square, smaller"),
    ("LinkedIn", "Cover", "1128 × 191", "about 5.9:1", "Full width", "Cropped at the sides; keep x 300 to 1014"),
    ("LinkedIn", "Post image", "1200 × 1200 and 1200 × 627", "1:1 and 1.91:1", "Feed", "Feed, full width"),
    ("LinkedIn", "Document post (PDF)", "1080 × 1350 per page", "4:5", "Swipe in the feed", "Swipe in the feed"),
    ("LinkedIn", "Careers (Life tab), employee banner", "1128 × 376 and 1584 × 396", "3:1 and 4:1", "Full width", "Cropped; see the LinkedIn kit"),
]


def size_rows():
    rows = []
    names = {"facebook": "Facebook", "instagram": "Instagram and Threads", "x": "X"}
    for ch in ("facebook", "instagram", "x"):
        for key in K.CHANNELS[ch]["assets"]:
            m = next(a for a in MAN if a["channel"] == ch and a["key"] == key)
            w, h = m["size"]
            norm = lambda t: t.lower().replace(",", "").replace(":", "")
            row = next((r for r in K.MOBILE[ch] if norm(r[0]).startswith(norm(m["title"]))), None) or \
                next((r for r in K.MOBILE[ch] if norm(r[0]).split(" ")[0] in norm(m["title"]).split(" ")), None)
            desk_, phone_ = (row[1], row[2]) if row else ("", "")
            rows.append((names[ch], m["title"], f"{w} × {h}", m["ratio"], desk_, phone_, K.CHANNELS[ch]["page"] + f"#{ch}-{key}"))
    pages = {"TikTok": "social-tiktok.html", "YouTube": "social-youtube.html", "LinkedIn": "social-linkedin.html"}
    for r in S2_SIZES:
        rows.append(r + (pages[r[0]],))
    order = ["Facebook", "Instagram and Threads", "TikTok", "YouTube", "LinkedIn", "X"]
    rows.sort(key=lambda r: order.index(r[0]))
    return "".join(f'<tr><td>{E(a)}</td><td><a class="link" href="{E(l)}">{E(b)}</a></td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td>{E(f)}</td></tr>'
                   for a, b, c, d, e, f, l in rows)


def main():
    cards = "".join(f'<a class="so-card" href="{p}"><img src="{img}" alt="" loading="lazy"><b>{E(t)}</b><span>{E(d)}</span><em>Open the kit</em></a>'
                    for p, t, d, img in CARDS)
    rules = "".join(f'<div class="rule"><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in SHARED_RULES)
    body = f"""
      <header class="page-head">
        <span class="eyebrow">Channels</span>
        <h1>Social.</h1>
        <p class="lead">The shared rules for every social channel, a kit for each of the six channels, and every size in one table. Each kit holds every asset its channel needs, in two options, with the desktop and the phone version side by side.</p>
        <nav class="toc" aria-label="On this page"><a href="#channels">Channel kits</a><a href="#shared">Shared rules</a><a href="#avatar">Profile picture</a><a href="#sizes">Every size</a><a href="#options">Options from 16.11</a></nav>
      </header>
      <div class="rule"><span class="status status--proposed">Proposed · {K.DATE}</span><p>The six channel kits are new proposals; nothing in them is approved yet. The profile picture and cover options from 16.11.2026 stay open below until Avi picks (R-93 stays in force until then). The posts that used to sit on this page now live in the channel kits.</p></div>

      <section class="sec" id="channels" aria-labelledby="channels-h">
        <div class="sec-head"><h2 id="channels-h">Six channel kits.</h2><p>Same six sections on every kit: the profile on desktop and phone, the asset set (Option A and Option B), the mobile differences, captions, rules and files.</p></div>
        <div class="so-cards">{cards}</div>
      </section>

      <section class="sec" id="shared" aria-labelledby="shared-h">
        <div class="sec-head"><h2 id="shared-h">Shared social rules.</h2><p>They sit on top of the content and compliance rules of the core hub and the paid rules on the <a class="link" href="ads.html">Ads</a> page, which apply to every boosted or ad-ready post.</p></div>
        <div class="so-rules">{rules}</div>
      </section>

      <section class="sec" id="avatar" aria-labelledby="avatar-h">
        <div class="sec-head"><h2 id="avatar-h">One profile picture for every channel.</h2><p>The app icon's "u|m" capsule, from the logo file, never redrawn. Option A puts it in Navy on Cream; Option B is the app icon itself, White on Navy (R-93). Every platform masks it to a circle, so nothing sits in the corners. Master files 800 × 800; each kit exports its own size.</p></div>
        <div class="so-ab">
          <figure><div class="so-av"><img class="so-l" src="assets/social/shared/avatar-a.png" alt="Profile picture, Option A: Navy mark on Cream"><img class="so-m" src="assets/social/shared/avatar-a.png" alt=""><img class="so-s" src="assets/social/shared/avatar-a.png" alt=""></div>
            <figcaption><b>Option A · Cream.</b> Light and calm on white feeds. <a class="link" href="assets/social/shared/avatar-a.png" download>PNG</a> · <a class="link" href="assets/social/shared/avatar-a.svg" download>SVG</a></figcaption></figure>
          <figure><div class="so-av"><img class="so-l" src="assets/social/shared/avatar-b.png" alt="Profile picture, Option B: White mark on Navy"><img class="so-m" src="assets/social/shared/avatar-b.png" alt=""><img class="so-s" src="assets/social/shared/avatar-b.png" alt=""></div>
            <figcaption><b>Option B · Navy (R-93).</b> The app icon colours; the strongest at 32 px. <a class="link" href="assets/social/shared/avatar-b.png" download>PNG</a> · <a class="link" href="assets/social/shared/avatar-b.svg" download>SVG</a></figcaption></figure>
        </div>
        <div class="rule"><span class="status status--proposed">Proposed · 17.11.2026</span><p>All six kits use this pair: Option A the Cream mark, Option B the app icon on Navy. The Primary seal is not used at avatar size, since its words cannot be read in a 32 px circle.</p></div>
      </section>

      <section class="sec" id="sizes" aria-labelledby="sizes-h">
        <div class="sec-head"><h2 id="sizes-h">Every size, desktop and mobile.</h2><p>Every file in the six kits, at the exact pixel size to export. Display sizes are approximate and platforms change them: check again before every campaign.</p></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Channel</th><th>Asset</th><th>File (px)</th><th>Ratio</th><th>Desktop shows</th><th>Phone shows</th></tr></thead>
          <tbody>{size_rows()}</tbody>
        </table></div>
      </section>

      <section class="sec" id="options" aria-labelledby="options-h">
        <div class="sec-head"><h2 id="options-h">Profile picture and cover options from 16.11.</h2><p>The gallery Avi asked for on 16.11.2026, kept as it was. Nothing here replaces R-93 until Avi picks. The cover capsule is now drawn in the logo's own shape.</p></div>
{old_avatar_options}
        <div class="sub" id="covers"><h3>Cover options</h3><p class="cap">Deep Teal ground, the horizontal reversed logo on the left, one outline capsule cropped by the right edge, then the other grounds and seal positions. Proportions are true to each platform.</p></div>
{old_covers}
      </section>
"""
    (EXT / "src" / "social.html").write_text(CSS + body)
    print("wrote social.html")


if __name__ == "__main__" and "--force" in sys.argv:
    main()
