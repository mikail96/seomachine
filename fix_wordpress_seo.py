"""
WordPress SEO Issue Fixer

Audits all posts/pages on evidepo.com for SEO issues and fixes them
via the WordPress REST API + RankMath SEO.

Usage:
    # Audit only (no changes)
    python3 fix_wordpress_seo.py --audit

    # Fix all issues
    python3 fix_wordpress_seo.py --fix

    # Fix double H1 tags in page content
    python3 fix_wordpress_seo.py --fix-h1

    # Fix specific post by ID
    python3 fix_wordpress_seo.py --fix --id 123

Prerequisites:
    1. WordPress API credentials in data_sources/config/.env
    2. RankMath SEO plugin active on WordPress
"""

import sys
import re
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / 'data_sources' / 'modules'))

from dotenv import load_dotenv

# Load env
env_paths = [
    Path(__file__).parent / 'data_sources' / 'config' / '.env',
    Path(__file__).parent / '.env',
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break

from wordpress_publisher import WordPressPublisher


# RankMath focus keywords for all content
FOCUS_KEYWORDS = {
    # Blog Posts
    101: 'istanbul eşya depolama',
    102: 'eşya depolama fiyatları',
    106: 'kentsel dönüşüm eşya depolama',
    107: 'tadilat sırasında eşya depolama',
    108: 'yurt dışına çıkarken eşya depolama',
    109: 'eşya paketleme rehberi',
    110: 'depolama firması seçerken dikkat',
    111: 'ofis taşıma depolama',
    # Hizmet Sayfaları
    9: 'ev eşyası depolama',
    10: 'ofis depolama',
    11: 'tadilat depolama',
    12: 'kentsel dönüşüm depolama',
    13: 'yurt dışı depolama',
    14: 'nakliyat ve depolama',
    # Ana Sayfalar
    6: 'eşya depolama istanbul',
    15: 'eşya depolama fiyatları',
    17: 'eşya depolama nasıl çalışır',
    18: 'eşya depolama sıkça sorulan sorular',
    8: 'depolama hizmetleri',
    # İlçe Sayfaları
    19: 'kadıköy eşya depolama',
    20: 'üsküdar eşya depolama',
    21: 'ataşehir eşya depolama',
    22: 'ümraniye eşya depolama',
    23: 'kartal eşya depolama',
    24: 'pendik eşya depolama',
    25: 'maltepe eşya depolama',
    26: 'tuzla eşya depolama',
    27: 'sancaktepe eşya depolama',
    28: 'sultanbeyli eşya depolama',
    29: 'beşiktaş eşya depolama',
    30: 'şişli eşya depolama',
    31: 'sarıyer eşya depolama',
    32: 'beylikdüzü eşya depolama',
    33: 'esenyurt eşya depolama',
    34: 'bakırköy eşya depolama',
    35: 'bahçelievler eşya depolama',
    36: 'küçükçekmece eşya depolama',
    37: 'başakşehir eşya depolama',
    38: 'fatih eşya depolama',
    145: 'bağcılar eşya depolama',
}


def get_publisher():
    """Create and return a WordPressPublisher instance"""
    try:
        return WordPressPublisher()
    except ValueError as e:
        print(f"Hata: {e}")
        print("\nWordPress API bilgilerini .env dosyasına ekleyin:")
        print("  WORDPRESS_URL=https://evidepo.com")
        print("  WORDPRESS_USERNAME=your_username")
        print("  WORDPRESS_APP_PASSWORD=your_app_password")
        sys.exit(1)


def audit(wp):
    """Audit all posts and pages for SEO issues"""
    import requests

    print("=" * 60)
    print("EVIDEPO.COM SEO AUDIT")
    print("=" * 60)

    issues_found = []

    for post_type in ['posts', 'pages']:
        items = wp.get_all_content(post_type)

        for item in items:
            url = item.get('link', '')
            title = item.get('title', {}).get('rendered', '')
            post_id = item['id']

            item_issues = []

            # Check live page for actual meta
            try:
                resp = requests.get(url, timeout=10)
                html = resp.text

                # Check meta description
                if not re.search(r'<meta\s+name=["\']description["\']', html, re.I):
                    item_issues.append('META_DESC_YOK')

                # Check canonical
                if not re.search(r'<link\s+rel=["\']canonical["\']', html, re.I):
                    item_issues.append('CANONICAL_YOK')

                # Check H1 count
                h1s = re.findall(r'<h1[^>]*>.*?</h1>', html, re.DOTALL)
                if len(h1s) > 1:
                    item_issues.append(f'CIFT_H1({len(h1s)})')
                elif len(h1s) == 0:
                    item_issues.append('H1_YOK')

                # Check focus keyword in RankMath
                if post_id not in FOCUS_KEYWORDS:
                    item_issues.append('FOCUS_KW_TANIMSIZ')

            except Exception:
                item_issues.append('SAYFA_ERISILEMEDI')

            if item_issues:
                issues_found.append({
                    'id': post_id,
                    'type': post_type,
                    'url': url,
                    'title': title,
                    'issues': item_issues,
                })

    if not issues_found:
        print("\nHiç SEO sorunu bulunamadı!")
        return

    print(f"\nToplam {len(issues_found)} sayfada sorun var:\n")
    for item in issues_found:
        print(f"[ID: {item['id']}] {item['title']}")
        print(f"  URL: {item['url']}")
        print(f"  Sorunlar: {', '.join(item['issues'])}")
        print()


def fix_focus_keywords(wp):
    """Set RankMath focus keywords for all content"""
    print("=" * 60)
    print("RANKMATH FOCUS KEYWORD AYARLAMA")
    print("=" * 60)

    success = 0
    for obj_id, keyword in FOCUS_KEYWORDS.items():
        try:
            resp = wp.session.post(f'{wp.url}/wp-json/rankmath/v1/updateMeta', json={
                'objectID': obj_id,
                'objectType': 'post',
                'meta': {
                    'rank_math_focus_keyword': keyword,
                }
            })
            if resp.status_code == 200:
                success += 1
                print(f"  [ID:{obj_id}] Focus keyword: \"{keyword}\"")
            else:
                print(f"  [ID:{obj_id}] HATA {resp.status_code}")
        except Exception as e:
            print(f"  [ID:{obj_id}] HATA: {e}")

    print(f"\n{success}/{len(FOCUS_KEYWORDS)} focus keyword ayarlandı.")


def fix_double_h1(wp):
    """Fix double H1 tags by converting content H1s to H2s"""
    print("=" * 60)
    print("CIFT H1 DUZELTME")
    print("=" * 60)

    fixed = 0

    for post_type in ['pages', 'posts']:
        page_num = 1
        while True:
            resp = wp.session.get(
                f'{wp.api_base}/{post_type}',
                params={'per_page': 100, 'page': page_num, 'status': 'publish', 'context': 'edit'}
            )
            if resp.status_code == 400:
                break
            items = resp.json()
            if not items:
                break

            for item in items:
                pid = item['id']
                title = item.get('title', {}).get('raw', '')
                raw_content = item.get('content', {}).get('raw', '')

                h1_tags = re.findall(r'<h1[^>]*>.*?</h1>', raw_content, re.DOTALL)
                if not h1_tags:
                    continue

                new_content = re.sub(r'<h1([^>]*)>', r'<h2\1>', raw_content)
                new_content = re.sub(r'</h1>', r'</h2>', new_content)

                try:
                    resp = wp.session.post(f'{wp.api_base}/{post_type}/{pid}', json={
                        'content': new_content
                    })
                    resp.raise_for_status()
                    fixed += 1
                    h1_text = re.sub(r'<[^>]+>', '', h1_tags[0]).strip()[:50]
                    print(f"  [ID:{pid}] {title} -> \"{h1_text}\" H1->H2")
                except Exception as e:
                    print(f"  [ID:{pid}] {title} -> HATA: {e}")

            page_num += 1

    print(f"\n{fixed} sayfada H1 -> H2 düzeltildi.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='WordPress SEO Issue Fixer (RankMath)')
    parser.add_argument('--audit', action='store_true', help='SEO sorunlarını tara')
    parser.add_argument('--fix', action='store_true', help='Focus keyword ayarla')
    parser.add_argument('--fix-h1', action='store_true', help='Çift H1 sorununu düzelt')
    parser.add_argument('--id', type=int, help='Belirli post/page ID')
    args = parser.parse_args()

    if not args.audit and not args.fix and not args.fix_h1:
        print("Kullanım:")
        print("  python3 fix_wordpress_seo.py --audit    # SEO sorunlarını tara")
        print("  python3 fix_wordpress_seo.py --fix      # Focus keyword ayarla")
        print("  python3 fix_wordpress_seo.py --fix-h1   # Çift H1 düzelt")
        sys.exit(0)

    wp = get_publisher()

    if args.audit:
        audit(wp)
    if args.fix:
        fix_focus_keywords(wp)
    if args.fix_h1:
        fix_double_h1(wp)


if __name__ == '__main__':
    main()
