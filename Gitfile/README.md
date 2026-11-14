# Northridge Field Station — reconcile, publish, verify

Four incomplete website drafts need to become one public site. Unique facts must survive the merge.

## Objective

Natural kickoff (also in `PROMPTS.md` / `instruction.md`):

> hey check the repo livefile — review the 4 drafts, reconcile them without dropping content, then publish and verify.

## Layout

| Path | Role |
| --- | --- |
| `drafts/` | Four source drafts. Do not edit. |
| `required-content.json` | Strings that must appear verbatim on the published site |
| `site/` | Canonical public site (`index.html` required) |
| `.github/workflows/pages.yml` | GitHub Pages deploy from `site/` |
| `scripts/verify_site.py` | Local verifier |
| `instruction.md` | Agent task prompt |
| `PROMPTS.md` | Review / reconcile / publish / verify prompts |
| `AGENTS.md` | Persistent agent rules |

## Git files in this folder

- `.gitignore`
- `.gitattributes`
- `.github/workflows/pages.yml`
- `README.md`

Initialize when you are ready:

```bash
git init -b main
git add .
git commit -m "Add four drafts, Pages workflow, and verify contract"
```

Then push to GitHub and enable Pages (Source: GitHub Actions).

## Verify

```bash
python scripts/verify_site.py
```
