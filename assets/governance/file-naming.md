# unifiedmeds · File naming guide

Current · Brand Edition 04 (R-126 naming and versions, R-124 Drive and the approved folder, R-125 approval log, R-127 archive, U-30). The same guide is on How we work (how-we-work.html#naming).

## Pattern

    um_<channel>_<asset>_<product-or-category>_<variant>_<size>_v<NN>_<yyyymmdd>.<ext>

- Eight fields, always in this order, always all eight.
- Lowercase letters and numbers only. Hyphens inside a field, underscores between fields.
- No spaces, no capitals, no accents. Never "final", "new", "latest" or "copy".

## Fields

| Field | Allowed values |
|---|---|
| um | always "um" |
| channel | brand, web, lp, ads, social, email, nl, pack, video, photo, print |
| asset | what it is, for example logo-horizontal, label, static, cover-linkedin, sting-b, order-confirmation, page |
| product-or-category | all, sexual-health, longevity, hair-loss, or a product such as tadalafil, sildenafil, combo. Always "all" for files a customer can see the address of, such as email images |
| variant | default when there is only one; otherwise light, dark, reversed, navy, desktop, mobile, photo-a, option-a |
| size | 1080x1350 (pixels), 600w (width only), any (vector or responsive), 90x120mm (print) |
| vNN | v01 to v99 |
| yyyymmdd | the day this version was saved, for example 20261116 |

## Examples

| Asset type | Name |
|---|---|
| Logo export | um_brand_logo-horizontal_all_navy_any_v01_20261115.svg |
| Label | um_pack_label_tadalafil_default_560x640_v04_20261116.png |
| Ad 4:5 | um_ads_static_sexual-health_photo-a_1080x1350_v02_20261116.png |
| Social cover | um_social_cover-linkedin_all_seal-left_1128x191_v01_20261116.png |
| Video | um_video_sting-b_all_default_1920x1080_v03_20261116.mp4 |
| Email | um_email_order-confirmation_all_default_600w_v02_20261116.html |
| Figma frame | frame "Ad · Static 4:5 · Photo A", exported as the ad name above |
| Landing page | um_lp_page_sexual-health_option-a_any_v01_20261116.html |

## Versions and status

- v01 is the first version anyone else sees. Every change that is shared again gets the next number.
- Approved files move from 1-work to 3-approved with the name unchanged. The approval log records who approved and when.
- Never edit an approved file. A change starts the next version in 1-work; when it is approved, the old one moves to 9-archive.
- Code and the brand hub keep their own short names; their history lives in the repository.

## Folders

    unifiedmeds/
      00-admin/  01-brand/  02-website/  03-landing-pages/  04-ads/  05-social/
      06-email/  07-packaging/  08-video/  09-photography/  10-clinical-legal/  99-archive/

    each channel folder:
      1-work/  2-review/  3-approved/  9-archive/

## Figma names (our own files only: design system, website working copy, assessment working copy)

- Page: Area, or Area · Subject. Example: Packaging · Labels.
- Frame: Kind · Subject · Variant. Example: Spec · Buttons · Desktop.
- Component set: Name set, family before a slash. Example: Button / Icon set.
- The separator is " · ". No status or version in a Figma name.

## Archive

Never delete. Move the file, with its name unchanged, to 9-archive (or a whole edition to 99-archive), and note it in the approval log. Nothing in the archive is linked as current.
