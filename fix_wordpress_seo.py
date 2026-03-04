"""
WordPress SEO Issue Fixer

Audits all posts/pages on evidepo.com for missing SEO fields
and fixes them via the WordPress REST API + Yoast SEO.

Usage:
    # Audit only (no changes)
    python3 fix_wordpress_seo.py --audit

    # Fix all issues
    python3 fix_wordpress_seo.py --fix

    # Fix specific post by ID
    python3 fix_wordpress_seo.py --fix --id 123

Prerequisites:
    1. WordPress API credentials in data_sources/config/.env
    2. SEO Machine Yoast REST plugin installed (wordpress/seo-machine-yoast-rest.php)
"""

import sys
import os
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


# Known SEO data for evidepo.com pages that need fixes
# Map: slug -> {meta_description, focus_keyphrase, seo_title, canonical_url}
KNOWN_SEO_FIXES = {
    # Hizmet sayfaları - meta description eksik olanlar
    'ev-esyasi-depolama': {
        'meta_description': 'İstanbul\'da ev eşyası depolama hizmeti. Kilitli özel odalar, 7/24 güvenlik, sigorta ve ücretsiz nakliyat. Evidepo ile eşyalarınız güvende.',
        'focus_keyphrase': 'ev eşyası depolama',
        'seo_title': 'Ev Eşyası Depolama İstanbul | Kilitli Oda Sistemi — Evidepo',
    },
    'ofis-depolama': {
        'meta_description': 'İstanbul\'da ofis ve kurumsal depolama çözümleri. Arşiv, mobilya ve ekipman depolama. Kilitli odalar, sigorta ve esnek sözleşme seçenekleri.',
        'focus_keyphrase': 'ofis depolama',
        'seo_title': 'Ofis ve Kurumsal Depolama İstanbul — Evidepo',
    },
    'tadilat-depolama': {
        'meta_description': 'Tadilat süresince eşyalarınızı güvenle depolayın. Kısa süreli esnek sözleşme, ücretsiz nakliyat ve sigorta ile tadilat depolama hizmeti.',
        'focus_keyphrase': 'tadilat depolama',
        'seo_title': 'Tadilat Depolama İstanbul | Esnek Süreli Depolama — Evidepo',
    },
    'kentsel-donusum-depolama': {
        'meta_description': 'Kentsel dönüşüm sürecinde eşyalarınız için güvenli depolama. Uzun süreli özel fiyatlar, sigorta ve ücretsiz nakliyat. Evidepo kentsel dönüşüm depolama.',
        'focus_keyphrase': 'kentsel dönüşüm depolama',
        'seo_title': 'Kentsel Dönüşüm Depolama İstanbul — Evidepo',
    },
    'yurt-disi-depolama': {
        'meta_description': 'Yurt dışına çıkarken eşyalarınızı güvenle depolayın. Uzun süreli depolama, sigorta, vekalet ile erişim. Evidepo yurt dışı depolama hizmeti.',
        'focus_keyphrase': 'yurt dışı depolama',
        'seo_title': 'Yurt Dışı Depolama İstanbul | Uzun Süreli Güvenli Depo — Evidepo',
    },
    'nakliyat-ve-depolama': {
        'meta_description': 'Nakliyat ve depolama tek elden. İstanbul içi taşıma + güvenli depolama hizmeti. Profesyonel ekip, sigorta ve kilitli oda sistemi.',
        'focus_keyphrase': 'nakliyat ve depolama',
        'seo_title': 'Nakliyat ve Depolama İstanbul | Tek Elden Çözüm — Evidepo',
    },
    # Fiyatlar sayfası
    'fiyatlar': {
        'meta_description': 'Evidepo eşya depolama fiyatları 2026. Kilitli oda boyutlarına göre aylık fiyatlar, nakliyat dahil seçenekler. Ücretsiz keşif ve fiyat teklifi.',
        'focus_keyphrase': 'eşya depolama fiyatları',
        'seo_title': 'Eşya Depolama Fiyatları 2026 | Güncel Fiyat Listesi — Evidepo',
    },
}


def audit(publisher: WordPressPublisher):
    """Audit all posts and pages for SEO issues"""
    print("=" * 60)
    print("EVIDEPO.COM SEO AUDIT")
    print("=" * 60)

    result = publisher.audit_seo()
    issues = result['issues']
    summary = result['summary']

    if not issues:
        print("\nHiç SEO sorunu bulunamadı!")
        return

    print(f"\nToplam {summary['total_issues']} sayfa/yazıda sorun var:\n")
    print(f"  Meta Description eksik: {summary['meta_desc_missing']}")
    print(f"  SEO Title eksik:        {summary['seo_title_missing']}")
    print(f"  Canonical URL eksik:     {summary['canonical_missing']}")
    print(f"  Focus Keyphrase eksik:   {summary['keyphrase_missing']}")

    print("\n" + "-" * 60)

    for item in issues:
        print(f"\n[ID: {item['id']}] {item['title']}")
        print(f"  URL: {item['url']}")
        print(f"  Tip: {item['type']}")
        print(f"  Sorunlar: {', '.join(item['issues'])}")

    print("\n" + "=" * 60)
    print(f"Düzeltmek için: python3 fix_wordpress_seo.py --fix")


def fix(publisher: WordPressPublisher, target_id: int = None):
    """Fix SEO issues on posts and pages"""
    print("=" * 60)
    print("EVIDEPO.COM SEO FIX")
    print("=" * 60)

    fixed_count = 0

    for post_type in ['posts', 'pages']:
        items = publisher.get_all_content(post_type)

        for item in items:
            post_id = item['id']
            if target_id and post_id != target_id:
                continue

            url = item.get('link', '')
            title = item.get('title', {}).get('rendered', '')
            slug = item.get('slug', '')
            yoast = item.get('yoast_seo', {})

            needs_fix = False
            fix_data = {}

            # Check if we have known fixes for this slug
            if slug in KNOWN_SEO_FIXES:
                known = KNOWN_SEO_FIXES[slug]
                if not yoast.get('meta_description') and known.get('meta_description'):
                    fix_data['meta_description'] = known['meta_description']
                    needs_fix = True
                if not yoast.get('seo_title') and known.get('seo_title'):
                    fix_data['seo_title'] = known['seo_title']
                    needs_fix = True
                if not yoast.get('focus_keyphrase') and known.get('focus_keyphrase'):
                    fix_data['focus_keyphrase'] = known['focus_keyphrase']
                    needs_fix = True

            # Always set canonical URL if missing
            if not yoast.get('canonical_url') and url:
                fix_data['canonical_url'] = url
                needs_fix = True

            if needs_fix:
                print(f"\n[ID: {post_id}] {title}")
                print(f"  URL: {url}")

                yoast_update = {'yoast_seo': fix_data}

                try:
                    response = publisher.session.post(
                        f"{publisher.api_base}/{post_type}/{post_id}",
                        json=yoast_update
                    )
                    response.raise_for_status()

                    for key, val in fix_data.items():
                        print(f"  + {key}: {val[:60]}{'...' if len(val) > 60 else ''}")

                    fixed_count += 1
                except Exception as e:
                    print(f"  HATA: {e}")

    print(f"\n{'=' * 60}")
    print(f"Toplam {fixed_count} sayfa düzeltildi.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='WordPress SEO Issue Fixer')
    parser.add_argument('--audit', action='store_true', help='Audit only, no changes')
    parser.add_argument('--fix', action='store_true', help='Fix SEO issues')
    parser.add_argument('--id', type=int, help='Fix specific post/page by ID')
    args = parser.parse_args()

    if not args.audit and not args.fix:
        print("Kullanım:")
        print("  python3 fix_wordpress_seo.py --audit   # Sadece kontrol")
        print("  python3 fix_wordpress_seo.py --fix     # Düzelt")
        print("  python3 fix_wordpress_seo.py --fix --id 123  # Belirli sayfa")
        sys.exit(0)

    try:
        publisher = WordPressPublisher()
    except ValueError as e:
        print(f"Hata: {e}")
        print("\nWordPress API bilgilerini .env dosyasına ekleyin:")
        print("  WORDPRESS_URL=https://evidepo.com")
        print("  WORDPRESS_USERNAME=your_username")
        print("  WORDPRESS_APP_PASSWORD=your_app_password")
        sys.exit(1)

    if args.audit:
        audit(publisher)
    elif args.fix:
        fix(publisher, target_id=args.id)


if __name__ == '__main__':
    main()
