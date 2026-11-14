#!/usr/bin/env python3
"""Fail if the published site dropped unique content from the four drafts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REQUIRED = json.loads((ROOT / "required-content.json").read_text(encoding="utf-8"))


def site_text() -> str:
    parts: list[str] = []
    if not SITE.exists():
        return ""
    for path in SITE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html", ".htm", ".css", ".js", ".txt", ".md"}:
            parts.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def main() -> int:
    errors: list[str] = []

    if not (SITE / "index.html").is_file():
        errors.append("missing site/index.html (publish target)")

    workflow = ROOT / ".github" / "workflows" / "pages.yml"
    if not workflow.is_file():
        errors.append("missing .github/workflows/pages.yml")
    else:
        yml = workflow.read_text(encoding="utf-8")
        if "path: site" not in yml:
            errors.append("pages workflow must upload the site/ directory")

    blob = site_text()
    missing = [item for item in REQUIRED["must_preserve"] if item not in blob]
    if missing:
        errors.append("published site is missing preserved content:")
        errors.extend(f"  - {item}" for item in missing)

    if errors:
        print("VERIFY FAILED")
        print("\n".join(errors))
        return 1

    print("VERIFY PASSED")
    print(f"site/index.html present; {len(REQUIRED['must_preserve'])} required strings preserved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
