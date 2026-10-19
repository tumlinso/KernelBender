#!/usr/bin/env python3
"""Check the consolidation's Markdown targets and introduced source locators.

Defaults name the migration's starting commits, so this also works after commit.
Network access is opt-in. Atlas URLs identify an access-gated source; --atlas
checks their pinned Git objects locally instead of requiring public access.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit, urlunsplit
from urllib.request import Request, urlopen


URL = re.compile(r'https?://[^\s<>`\)\]\"]+')
LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
ATLAS = 'github.com/tumlinso/gpu_circuit_bending_atlas'


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        self.anchors.update(value for key, value in attrs
                            if key in ('id', 'name') and value)


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wiki', type=Path, required=True)
    parser.add_argument('--atlas', type=Path)
    parser.add_argument('--external', action='store_true')
    parser.add_argument('--bender-base', default='2af536a156999e37fee06b0535a002586eee4f47')
    parser.add_argument('--wiki-base', default='c9bf8dba49f2e5cf90c1dc9a78f970359da5ba5e')
    args = parser.parse_args()
    bender = Path(__file__).resolve().parents[1]
    introduced = set()
    errors = []
    local_count = 0
    for root, base in ((bender, args.bender_base), (args.wiki.resolve(), args.wiki_base)):
        paths = set(git(root, 'diff', '--name-only', base).splitlines())
        paths.update(git(root, 'ls-files', '--others', '--exclude-standard').splitlines())
        for rel in paths:
            path = root / rel
            if path.suffix != '.md' or not path.is_file():
                continue
            body = path.read_text()
            prior = subprocess.run(['git', '-C', str(root), 'show', f'{base}:{rel}'],
                                   capture_output=True, text=True)
            old_urls = {url.rstrip('.,;') for url in URL.findall(prior.stdout)}
            introduced.update(url.rstrip('.,;') for url in URL.findall(body)
                              if url.rstrip('.,;') not in old_urls)
            for raw in LINK.findall(body):
                target = raw.strip().split(maxsplit=1)[0].strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                local_count += 1
                if not (path.parent / unquote(parsed.path)).resolve().exists():
                    errors.append(f'{path}: missing local target {target}')

    groups = {}
    for url in introduced:
        parsed = urlsplit(url)
        base = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ''))
        groups.setdefault(base, set()).add(unquote(parsed.fragment))

    def check(item):
        base, fragments = item
        result = {'url': base}
        if ATLAS in base:
            result['availability'] = 'access-gated; unauthenticated access not required'
            match = re.search(r'/(?:blob|tree)/([0-9a-f]{7,40})(?:/(.*))?$', urlsplit(base).path)
            if args.atlas and match:
                revision, path = match.groups()
                obj = revision + (':' + path if path else '^{tree}')
                exists = subprocess.run(['git', '-C', str(args.atlas), 'cat-file', '-e', obj],
                                        capture_output=True).returncode == 0
                result['local_git_object_resolves'] = exists
                if not exists:
                    result['error'] = f'Pinned Atlas object missing: {obj}'
            return result
        if not args.external:
            result['availability'] = 'network check not requested'
            return result
        try:
            request = Request(base, headers={'User-Agent': 'KernelBender-link-validation'})
            with urlopen(request, timeout=25) as response:
                result['http_status'] = response.status
                fragments = fragments - {''}
                if fragments and 'text/html' in response.headers.get('Content-Type', ''):
                    anchors = Anchors()
                    anchors.feed(response.read().decode('utf-8', errors='replace'))
                    missing = sorted(fragments - anchors.anchors)
                    if missing:
                        result['error'] = f'Missing HTML fragments: {missing}'
        except Exception as exc:
            result['error'] = str(exc)
        return result

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, sorted(groups.items())))
    errors.extend(f"{row['url']}: {row['error']}" for row in results if row.get('error'))
    print(json.dumps({'local_markdown_targets_checked': local_count,
                      'introduced_source_bases': len(results),
                      'source_results': results, 'errors': errors}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
