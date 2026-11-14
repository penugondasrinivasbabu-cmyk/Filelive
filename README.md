# Northridge Field Station

**Public site:** https://penugondasrinivasbabu-cmyk.github.io/Filelive/

The canonical homepage is **`site/index.html`**. The site reconciles all four supplied drafts, preserves all **27 required strings verbatim as visible page content**, and leaves every original file under `Gitfile/` unchanged.

## Alignment and reconciliation

| Requirement | Implementation |
| --- | --- |
| One real public site | Responsive, single-page site in `site/`; local CSS and SVG assets only, no JavaScript or build dependency |
| Preserve actual content | Story, hours, admission, equipment, map reference, staff, contacts, visitor notes and all three testimonials retained |
| Resolve conflicting hours | Draft 1 wins: Tuesday–Saturday, 9:00–17:00; closed Sunday and Monday; last admission 16:15 |
| Do not change drafts | All four originals remain byte-for-byte unchanged in `Gitfile/drafts/`; hashes are checked before deployment |
| Keep the supplied contract | Root-level contract and verifier are byte-for-byte copies, not rewritten or weakened |
| Publish only `site/` | `.github/workflows/pages.yml` uploads `path: site` and deploys through GitHub Actions |
| Verify it works | Original verifier, additional integrity/link checks, browser checks and post-deployment HTTP/asset checks |

The uploaded project was nested under `Gitfile/`. Root-level runtime, workflow and verification files were added without moving or editing those originals. The `source_drafts` paths in the unchanged contract are relative to that original `Gitfile/` project.

## Repository layout

- `site/index.html`: canonical homepage.
- `site/styles.css`, `site/hillside.svg`, `site/favicon.svg`: all public assets; no external font, script or image service.
- `.github/workflows/pages.yml`: validate, upload **only `site/`**, deploy, then verify the served homepage and assets.
- `required-content.json` and `scripts/verify_site.py`: unchanged copies of the original preservation contract and verifier, runnable from the repository root.
- `scripts/check_site.py`: extra source-integrity, body-content, HTML, fragment/asset-link and optional live HTTP checks; Python standard library only.
- `Gitfile/`: original imported project, including the four untouched drafts and original README.
- `docs/reconciliation.md`: draft-by-draft ledger, conflict decision and source limitations.

## Verify and preview locally

Use Python 3.9 or newer, from the repository root:

```sh
python scripts/verify_site.py
python scripts/check_site.py
python -m http.server 8000 --directory site
```

The supplied verifier reports:

```text
VERIFY PASSED
site/index.html present; 27 required strings preserved.
```

Open http://localhost:8000/. All navigation uses page fragments and every asset URL is relative, so the site also works at the `/Filelive/` GitHub Pages project subpath.

Prepublication Chromium checks passed at widths of **320, 375, 768, 1024, 1440 and 1920 pixels**, with JavaScript disabled: all required text visible, navigation and keyboard skip link working, no horizontal page overflow or failed asset requests. These browser checks complement, rather than replace, the automated workflow checks.

## Deployment and live checks

GitHub Pages is configured with **Source: GitHub Actions**, not a legacy branch/root build. See the [Pages workflow and runs](https://github.com/penugondasrinivasbabu-cmyk/Filelive/actions/workflows/pages.yml).

Changes to the site, verification scripts, original source project, content contract or workflow pushed to `main` run these stages:

1. Run `python scripts/verify_site.py` and `python scripts/check_site.py`. A failure prevents deployment.
2. Upload only `site/` with `actions/upload-pages-artifact`.
3. Deploy with `actions/deploy-pages`.
4. Fetch the public homepage and every local asset, require HTTP 200 and correct content types, and compare the bytes against the tested revision. Retry briefly for Pages propagation.

Pull requests run validation without publishing. Documentation-only changes do not redeploy. The workflow also supports manual dispatch.

To recheck the public site yourself:

```sh
python scripts/check_site.py --url https://penugondasrinivasbabu-cmyk.github.io/Filelive/ --retries 8
```

## Known source limitations

- **Trail-map PDF not supplied.** The exact required text `Trail map PDF at /maps/ridge-loop.pdf` is visible on the site, together with an explicit unavailable notice. There is no fabricated map or broken download link. Supply the real PDF before enabling a download.
- **Contact delivery is not verified.** The source email uses the reserved `.example` domain and the source telephone is `555-0148`. Both are preserved rather than replaced with invented details. Mailto/tel formatting is checked; successful delivery or calling is not claimed.
- **Illustration, not a map.** The hillside SVG is decorative artwork, not a photograph, surveyed map or navigational aid.
