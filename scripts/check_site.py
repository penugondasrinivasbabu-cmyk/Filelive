#!/usr/bin/env python3
"""Additional dependency-free integrity, HTML, link and live-deployment checks."""
from __future__ import annotations
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import sys
import time
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
DRAFT_HASHES = {
    '01-story-hours.html': '380c7df583a484d332468cc8a8b9d4d63a9f28a6',
    '02-services-pricing.html': 'cdf58ef1b5661d3a22376ccd76fabbc0c67e2de1',
    '03-team-contact.html': 'f1350038d5da514cb74354ecede1648bdff89cd7',
    '04-faq-testimonials.html': '7f20601354fd3f691bace198399a1970a241ca93',
}
REQUIRED = json.loads((ROOT / 'required-content.json').read_text(encoding='utf-8'))['must_preserve']

class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.refs = []
        self.text = []
        self.errors = []
        self.body = False
        self.suppressed = 0
        self.h1 = 0
        self.lang = False
        self.viewport = False
        self.title = False
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang') == 'en'
        if tag == 'meta' and a.get('name') == 'viewport': self.viewport = 'width=device-width' in a.get('content', '')
        if tag == 'title': self.title = True
        if tag == 'body': self.body = True
        if tag in {'script', 'style', 'template'}: self.suppressed += 1
        if tag == 'h1': self.h1 += 1
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'img' and 'alt' not in a: self.errors.append('image without alt')
        for key in ['href', 'src']:
            if key in a: self.refs.append(a[key])

    def handle_endtag(self, tag):
        if tag == 'body': self.body = False
        if tag in {'script', 'style', 'template'}: self.suppressed = max(0, self.suppressed - 1)

    def handle_data(self, data):
        if self.body and not self.suppressed: self.text.append(data)

def git_hash(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()

def validate_html(raw: str) -> tuple[list[str], set[str]]:
    page = Page(raw)
    errors = page.errors[:]
    body = ' '.join(' '.join(page.text).split())
    for item in REQUIRED:
        if item not in raw: errors.append('missing verbatim source text: ' + item)
        if item not in body: errors.append('missing body text: ' + item)
    if 'weekdays 10' in body.lower(): errors.append('obsolete draft-2 hours are published')
    for condition, label in [(page.h1 == 1, 'exactly one h1'), (page.lang, 'English language'), (page.viewport, 'mobile viewport'), (page.title, 'document title')]:
        if not condition: errors.append('missing/invalid ' + label)
    assets = set()
    for ref in page.refs:
        u = urlsplit(ref)
        if u.scheme in {'mailto', 'tel'}: continue
        if u.scheme or u.netloc:
            errors.append('unexpected external dependency/link: ' + ref)
            continue
        if u.path.startswith('/'):
            errors.append('root-relative URL breaks project subpaths: ' + ref)
            continue
        if u.path:
            target = (SITE / unquote(u.path)).resolve()
            if not target.is_relative_to(SITE.resolve()) or not target.is_file():
                errors.append('missing/unsafe local asset: ' + ref)
            else: assets.add(u.path)
        if u.fragment and not u.path and unquote(u.fragment) not in page.ids:
            errors.append('missing fragment target: ' + ref)
        if not ref: errors.append('empty URL')
    return errors, assets

def fetch(url: str) -> tuple[bytes, str]:
    request = Request(url, headers={'User-Agent': 'NorthridgeSiteVerifier/1.0', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=25) as response:
        if response.status != 200: raise ValueError(f'{url}: HTTP {response.status}')
        return response.read(), response.headers.get_content_type()

def live_checks(base: str, assets: set[str]) -> None:
    if urlsplit(base).scheme not in {'https', 'http'}: raise ValueError('live URL must use http or https')
    base = base.rstrip('/') + '/'
    raw, kind = fetch(base)
    if kind != 'text/html': raise ValueError('homepage was not served as HTML')
    if raw != (SITE / 'index.html').read_bytes(): raise ValueError('served homepage differs from the tested revision')
    errors, remote_assets = validate_html(raw.decode('utf-8'))
    if errors: raise ValueError('; '.join(errors))
    for asset in sorted(assets | remote_assets):
        raw, kind = fetch(urljoin(base, asset))
        if raw != (SITE / asset).read_bytes(): raise ValueError('served asset differs: ' + asset)
        expected = {'.css': 'text/css', '.svg': 'image/svg+xml'}.get(Path(asset).suffix)
        if expected and kind != expected: raise ValueError(f'{asset}: content type {kind}, expected {expected}')
    print(f'LIVE CHECK PASSED: homepage and {len(assets)} local assets return HTTP 200 and match tested files.')

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', help='deployed site root, including any project subpath')
    parser.add_argument('--retries', type=int, default=1)
    args = parser.parse_args()
    errors = []
    for name, sha in DRAFT_HASHES.items():
        path = ROOT / 'Gitfile' / 'drafts' / name
        if not path.is_file() or git_hash(path) != sha: errors.append('source draft changed: ' + name)
    for rel in ['required-content.json', 'scripts/verify_site.py']:
        if (ROOT / rel).read_bytes() != (ROOT / 'Gitfile' / rel).read_bytes(): errors.append('supplied contract/verifier changed: ' + rel)
    if not (SITE / 'index.html').is_file(): errors.append('missing homepage')
    if errors:
        print('SITE CHECK FAILED\n' + '\n'.join(errors)); return 1
    html_errors, assets = validate_html((SITE / 'index.html').read_text(encoding='utf-8'))
    if html_errors:
        print('SITE CHECK FAILED\n' + '\n'.join(html_errors)); return 1
    print(f'SITE CHECK PASSED: 4 original drafts unchanged; {len(REQUIRED)} verbatim strings in body text; local links and assets valid.')
    if args.url:
        attempts = max(1, args.retries)
        for attempt in range(attempts):
            try:
                live_checks(args.url, assets); break
            except Exception as exc:
                if attempt + 1 == attempts:
                    print('LIVE CHECK FAILED: ' + str(exc)); return 1
                print(f'Waiting for deployment ({attempt + 1}/{attempts}): {exc}', flush=True)
                time.sleep(10)
    return 0

if __name__ == '__main__':
    sys.exit(main())
