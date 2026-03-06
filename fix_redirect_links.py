#!/usr/bin/env python3
"""
Fix redirect errors: update service links from root level to /hizmetlerimiz/ subdirectory.
Scans all WordPress pages and posts, finds broken links, and fixes them.
"""

import requests
import re
import sys
from urllib.parse import quote

# WordPress config
WP_URL = "https://evidepo.com"
WP_USER = "admin"
WP_APP_PASS = "HQmY kKaQ kDY6 W91l v4G5 sHtA"

# Link mappings to fix
LINK_FIXES = {
    '"/ev-esyasi-depolama/"': '"/hizmetlerimiz/ev-esyasi-depolama/"',
    '"/ofis-depolama/"': '"/hizmetlerimiz/ofis-depolama/"',
    '"/tadilat-depolama/"': '"/hizmetlerimiz/tadilat-depolama/"',
    '"/kentsel-donusum-depolama/"': '"/hizmetlerimiz/kentsel-donusum-depolama/"',
    '"/yurt-disi-depolama/"': '"/hizmetlerimiz/yurt-disi-depolama/"',
    '"/nakliyat-depolama/"': '"/hizmetlerimiz/nakliyat-depolama/"',
    # Also catch full URL variants
    '"https://evidepo.com/ev-esyasi-depolama/"': '"https://evidepo.com/hizmetlerimiz/ev-esyasi-depolama/"',
    '"https://evidepo.com/ofis-depolama/"': '"https://evidepo.com/hizmetlerimiz/ofis-depolama/"',
    '"https://evidepo.com/tadilat-depolama/"': '"https://evidepo.com/hizmetlerimiz/tadilat-depolama/"',
    '"https://evidepo.com/kentsel-donusum-depolama/"': '"https://evidepo.com/hizmetlerimiz/kentsel-donusum-depolama/"',
    '"https://evidepo.com/yurt-disi-depolama/"': '"https://evidepo.com/hizmetlerimiz/yurt-disi-depolama/"',
    '"https://evidepo.com/nakliyat-depolama/"': '"https://evidepo.com/hizmetlerimiz/nakliyat-depolama/"',
}

# Patterns to search for (without quotes, for detection)
SEARCH_PATTERNS = [
    '/ev-esyasi-depolama/',
    '/ofis-depolama/',
    '/tadilat-depolama/',
    '/kentsel-donusum-depolama/',
    '/yurt-disi-depolama/',
    '/nakliyat-depolama/',
]

session = requests.Session()
session.auth = (WP_USER, WP_APP_PASS)
session.headers.update({'Content-Type': 'application/json'})


def get_all_content(post_type='pages'):
    """Fetch all pages or posts from WordPress."""
    items = []
    page = 1
    while True:
        resp = session.get(f"{WP_URL}/wp-json/wp/v2/{post_type}", params={
            'per_page': 100,
            'page': page,
            'status': 'publish,draft,private',
        })
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        items.extend(data)
        total_pages = int(resp.headers.get('X-WP-TotalPages', 1))
        if page >= total_pages:
            break
        page += 1
    return items


def has_broken_links(content):
    """Check if content contains any of the broken link patterns."""
    if not content:
        return False
    for pattern in SEARCH_PATTERNS:
        # Match the pattern but NOT when it's already under /hizmetlerimiz/
        if pattern in content:
            # Check it's not already correct
            correct = f'/hizmetlerimiz{pattern}'
            # Remove correct occurrences temporarily to check if broken ones exist
            temp = content.replace(correct, '')
            if pattern in temp:
                return True
    return False


def fix_content(content):
    """Replace broken links in content."""
    if not content:
        return content, False

    original = content

    for old, new in LINK_FIXES.items():
        content = content.replace(old, new)

    # Also fix without surrounding quotes (for various HTML attribute formats)
    for pattern in SEARCH_PATTERNS:
        correct = f'/hizmetlerimiz{pattern}'
        # Use regex to replace only when NOT already under /hizmetlerimiz/
        # Match href="..." or src="..." patterns
        content = re.sub(
            r'(href\s*=\s*["\'])(' + re.escape(f'https://evidepo.com{pattern}') + r')(["\'])',
            r'\1https://evidepo.com' + correct + r'\3',
            content
        )
        content = re.sub(
            r'(href\s*=\s*["\'])(' + re.escape(pattern) + r')(["\'])',
            r'\1' + correct + r'\3',
            content
        )

    changed = content != original
    return content, changed


def update_post(post_id, post_type, new_content):
    """Update a WordPress post/page content."""
    endpoint = 'pages' if post_type == 'pages' else 'posts'
    resp = session.post(
        f"{WP_URL}/wp-json/wp/v2/{endpoint}/{post_id}",
        json={'content': new_content}
    )
    return resp.status_code == 200


def main():
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("=== DRY RUN MODE - No changes will be made ===\n")

    total_fixed = 0

    for post_type in ['pages', 'posts']:
        print(f"\n--- Scanning {post_type} ---")
        items = get_all_content(post_type)
        print(f"Found {len(items)} {post_type}")

        for item in items:
            title = item.get('title', {}).get('rendered', 'Untitled')
            content = item.get('content', {}).get('rendered', '')
            post_id = item['id']

            # Also get raw content
            raw_resp = session.get(f"{WP_URL}/wp-json/wp/v2/{post_type}/{post_id}", params={'context': 'edit'})
            if raw_resp.status_code != 200:
                continue
            raw_data = raw_resp.json()
            raw_content = raw_data.get('content', {}).get('raw', '')

            if not has_broken_links(raw_content):
                continue

            print(f"\n  FOUND broken links in: [{post_id}] {title}")

            # Show which patterns were found
            for pattern in SEARCH_PATTERNS:
                correct = f'/hizmetlerimiz{pattern}'
                temp = raw_content.replace(correct, '')
                if pattern in temp:
                    print(f"    - {pattern} (should be /hizmetlerimiz{pattern})")

            new_content, changed = fix_content(raw_content)

            if changed:
                if dry_run:
                    print(f"    Would fix {post_id}")
                else:
                    endpoint = 'pages' if post_type == 'pages' else 'posts'
                    resp = session.post(
                        f"{WP_URL}/wp-json/wp/v2/{endpoint}/{post_id}",
                        json={'content': new_content}
                    )
                    if resp.status_code == 200:
                        print(f"    FIXED successfully!")
                        total_fixed += 1
                    else:
                        print(f"    ERROR: {resp.status_code} - {resp.text[:200]}")

    print(f"\n{'='*50}")
    print(f"Total {'would fix' if dry_run else 'fixed'}: {total_fixed} pages/posts")

    if dry_run:
        print("\nRun without --dry-run to apply changes.")


if __name__ == '__main__':
    main()
