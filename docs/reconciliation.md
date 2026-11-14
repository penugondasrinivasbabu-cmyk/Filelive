# Reconciliation ledger

## Layout and originals

The uploaded project is nested under `Gitfile/`, not at the repository root. Every original file stays unchanged there. The canonical public `site/` and functional `.github/workflows/pages.yml` are added at the repository root. The provided content contract and verifier are copied byte-for-byte to root-level paths; neither is weakened or rewritten.

## Content retained

All 27 required strings appear verbatim as visible homepage text, not merely in metadata, comments or hidden fixtures. The original description `Public field station est. 1987 on a 14-acre hillside campus.` is also kept verbatim. Repeated station names are consolidated where appropriate.

### Draft 01 — Story and hours

Source: `Gitfile/drafts/01-story-hours.html`. Destination: `#hero-title / #visit`.

- Northridge Field Station
- est. 1987
- 14-acre hillside campus
- Tuesday–Saturday, 9:00–17:00
- closed Sunday and Monday
- last admission 16:15
- guided ridge walk at 10:30
- Member Day is the first Saturday of each month

### Draft 02 — Admission, equipment and map reference

Source: `Gitfile/drafts/02-services-pricing.html`. Destination: `#visit`.

- Day pass $12
- Student / senior $8
- Annual household $95
- School group $6 per student
- Equipment rental $4
- Trail map PDF at /maps/ridge-loop.pdf

### Draft 03 — Staff and contact

Source: `Gitfile/drafts/03-team-contact.html`. Destination: `#team / #contact`.

- Dr. Lena Okonkwo, Director
- Marcus Hale, Collections
- Priya Shah, Education
- front desk: 555-0148
- visitors@northridgefield.example
- 88 Switchback Road, Northridge

### Draft 04 — Visitor notes and testimonials

Source: `Gitfile/drafts/04-faq-testimonials.html`. Destination: `#notes / #quotes-title`.

- Wheelchair access via the west lift
- Dogs on leash on the outer loop only
- No drones without a written permit
- Lockers next to the boot wash
- "The ridge walk is the highlight of our year." — A. Chen
- "Staff actually knew the bird calls." — J. Patel
- "Quiet enough to hear the creek." — M. Rossi

## Decisions and limitations

- **Hours:** draft 1 wins. The conflicting draft-2 phrase “weekdays 10–4” is not published as an alternative schedule. Draft 2 itself instructs reconciliation in favor of draft 1.
- **Editorial notes:** the draft-2 hours-conflict instruction and draft-3 instruction to copy missing hours/prices are production guidance, not visitor-facing facts. They are honored here rather than published as website copy.
- **Missing PDF:** the supplied repository contains no trail-map PDF. The exact string `Trail map PDF at /maps/ridge-loop.pdf` remains visible, alongside an explicit unavailable notice. There is no fake map, fabricated route or broken PDF anchor. A real PDF must be supplied before enabling a download.
- **Contacts:** the supplied `.example` email and short telephone number are preserved. Mailto/tel formatting can be checked; successful delivery or calling cannot be claimed.
- **Artwork:** the hillside SVG is an abstract decorative illustration and is hidden from assistive technology. It is not represented as a real site map.
- **No invented facts:** no new dates, prices, staff biographies, visitor policies, route directions, booking promises or facilities are added.

## Checks

Run `python scripts/verify_site.py` for the original contract. Run `python scripts/check_site.py` for source hashes, byte-identical verifier/contract copies, body-text preservation, obsolete-hours exclusion, structural checks and valid local asset/fragment links. Pass `--url` after deployment to compare the served homepage and every local asset byte-for-byte with the tested files. The Pages workflow runs these checks before and after deployment.
