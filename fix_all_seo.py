"""
Comprehensive SEO fixer for evidepo.com
Fixes: RankMath meta, title tags, meta descriptions, focus keywords, double H1
"""
import sys
import re
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'data_sources' / 'modules'))

from dotenv import load_dotenv
env_paths = [
    Path(__file__).parent / 'data_sources' / 'config' / '.env',
    Path(__file__).parent / '.env',
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break

from wordpress_publisher import WordPressPublisher

# ============================================================
# SEO META DATA FOR ALL PAGES
# ============================================================
# Format: page_id: {seo_title, meta_desc, focus_kw, canonical}

SEO_META = {
    # === ANASAYFA ===
    6: {
        'seo_title': 'Istanbul Esya Depolama | Kilitli Oda Kiralama - Evidepo',
        'meta_desc': 'Istanbul esya depolama hizmeti. Guvenli, kamerali, kilitli oda sistemi. Randevulu erisim, Allianz sigorta, ucretsiz nakliyat. Hemen teklif alin.',
        'focus_kw': 'esya depolama istanbul',
    },
    # === HIZMET SAYFALARI ===
    8: {
        'seo_title': 'Esya Depolama Hizmetlerimiz | Istanbul - Evidepo',
        'meta_desc': 'Istanbul kilitli oda depolama, nakliyat, paketleme, kentsel donusum ve tadilat depolama. Ev, ofis, yurt disi depolama hizmetleri.',
        'focus_kw': 'depolama hizmetleri',
    },
    9: {
        'seo_title': 'Ev Esyasi Depolama Istanbul | Kilitli Oda - Evidepo',
        'meta_desc': 'Istanbul ev esyasi depolama. Kilitli ozel odalar, Allianz sigorta, randevulu erisim. Profesyonel paketleme ve nakliyat dahil. Ucretsiz ekspertiz.',
        'focus_kw': 'ev esyasi depolama',
    },
    10: {
        'seo_title': 'Ofis Depolama Istanbul | Kurumsal Cozumler - Evidepo',
        'meta_desc': 'Istanbul ofis esyasi ve arsiv depolama. Kurumsal sozlesme, faturali hizmet, kilitli oda. Profesyonel paketleme dahil. Teklif alin.',
        'focus_kw': 'ofis depolama',
    },
    11: {
        'seo_title': 'Tadilat Depolama Istanbul | Gecici Esya Saklama - Evidepo',
        'meta_desc': 'Ev tadilati sirasinda esyalarinizi guvenle depolayin. 1 aydan baslayan esnek sureler, nakliyat dahil. Tadilat bitince geri getiriyoruz.',
        'focus_kw': 'tadilat depolama',
    },
    12: {
        'seo_title': 'Kentsel Donusum Depolama Istanbul - Evidepo',
        'meta_desc': 'Kentsel donusum surecinde esyalarinizi guvenle depolayin. 18-36 ay esnek sozlesme, uzun sureli indirim. Ucretsiz ekspertiz alin.',
        'focus_kw': 'kentsel donusum depolama',
    },
    13: {
        'seo_title': 'Yurt Disi Esya Depolama Istanbul - Evidepo',
        'meta_desc': 'Yurt disina cikarken esyalarinizi guvenle depolayin. Uzun sureli indirim, uzaktan erisim, 7/24 kamera guvenligi. Hemen teklif alin.',
        'focus_kw': 'yurt disi depolama',
    },
    14: {
        'seo_title': 'Nakliyat ve Depolama Istanbul | Tek Elden - Evidepo',
        'meta_desc': 'Istanbul nakliyat ve depolama hizmeti tek elden. Sanat Evden Eve Nakliyat guvencesiyle tasima ve depolama. Ucretsiz ekspertiz alin.',
        'focus_kw': 'nakliyat ve depolama',
    },
    # === DIGER SAYFALAR ===
    15: {
        'seo_title': 'Esya Depolama Fiyatlari 2026 | Istanbul - Evidepo',
        'meta_desc': 'Istanbul esya depolama fiyatlari 2026. Kilitli oda kiralama ucretleri, aylik depolama maliyetleri. Seffaf fiyatlandirma, gizli ucret yok.',
        'focus_kw': 'esya depolama fiyatlari',
    },
    17: {
        'seo_title': 'Nasil Calisir? | Evidepo Esya Depolama Sureci',
        'meta_desc': 'Evidepo esya depolama nasil calisir? Teklif al, esyalari teslim et, guvenle depola. 4 kolay adimda depolama sureci.',
        'focus_kw': 'esya depolama nasil calisir',
    },
    18: {
        'seo_title': 'Esya Depolama SSS | Sikca Sorulan Sorular - Evidepo',
        'meta_desc': 'Esya depolama hakkinda merak edilen her sey. Guvenlik, fiyat, erisim, sigorta, nakliyat ve daha fazlasi. Sorularinizin cevaplari burada.',
        'focus_kw': 'esya depolama sikca sorulan sorular',
    },
    7: {
        'seo_title': 'Hakkimizda | Evidepo - Sanat Nakliyat Istiraki',
        'meta_desc': 'Evidepo, Sanat Evden Eve Nakliyat istiraki olarak Istanbul guvenli esya depolama hizmeti sunuyor. Hikayemiz ve degerlerimiz.',
        'focus_kw': 'evidepo hakkimizda',
    },
    16: {
        'seo_title': 'Iletisim | Evidepo Esya Depolama Istanbul',
        'meta_desc': 'Evidepo iletisim. Istanbul esya depolama hizmeti icin teklif alin. 0535 529 81 92. WhatsApp ile hizli iletisim.',
        'focus_kw': 'evidepo iletisim',
    },
    105: {
        'seo_title': 'Esya Depolama Blog | Rehberler ve Ipuclari - Evidepo',
        'meta_desc': 'Esya depolama, nakliyat, paketleme rehberleri ve ipuclari. Istanbul depolama hakkinda bilmeniz gereken her sey Evidepo blogunda.',
        'focus_kw': 'esya depolama blog',
    },
    # === BLOG YAZILARI ===
    101: {
        'seo_title': 'Istanbul Esya Depolama: 2026 Kapsamli Rehber - Evidepo',
        'meta_desc': 'Istanbul esya depolama hakkinda bilmeniz gereken her sey. Firma secimi, fiyatlar, guvenlik kriterleri. 2026 guncel kapsamli rehber.',
        'focus_kw': 'istanbul esya depolama',
    },
    102: {
        'seo_title': 'Esya Depolama Fiyatlari 2026: Fiyat Rehberi - Evidepo',
        'meta_desc': 'Istanbul esya depolama fiyatlari 2026. Oda boyutuna gore ucretler, gizli maliyetler, tasarruf yontemleri. Guncel fiyat rehberi.',
        'focus_kw': 'esya depolama fiyatlari',
    },
    106: {
        'seo_title': 'Kentsel Donusumde Esya Depolama Rehberi - Evidepo',
        'meta_desc': 'Kentsel donusum surecinde esya depolama rehberi. Ilce bazli donusum haritasi, maliyet karsilastirmasi, uzun sureli cozumler.',
        'focus_kw': 'kentsel donusum esya depolama',
    },
    107: {
        'seo_title': 'Tadilat Sirasinda Esya Koruma Rehberi - Evidepo',
        'meta_desc': 'Ev tadilati sirasinda esya koruma rehberi. 7 risk faktoru, koruma yontemleri, depolama karsilastirmasi. Pratik ipuclari.',
        'focus_kw': 'tadilat sirasinda esya depolama',
    },
    108: {
        'seo_title': 'Yurt Disina Cikarken Esya Depolama Rehberi - Evidepo',
        'meta_desc': 'Yurt disina cikarken esyalariniz ne olacak? Evi tutmak vs depolama maliyet karsilastirmasi, checklist ve pratik rehber.',
        'focus_kw': 'yurt disina cikarken esya depolama',
    },
    109: {
        'seo_title': 'Esya Paketleme Rehberi: Adim Adim Kilavuz - Evidepo',
        'meta_desc': 'Depolama oncesi profesyonel paketleme teknikleri. Mobilya, elektronik, kirilacak esya paketleme. Adim adim kilavuz.',
        'focus_kw': 'esya paketleme rehberi',
    },
    110: {
        'seo_title': 'Depolama Firmasi Secerken 12 Kriter - Evidepo',
        'meta_desc': 'Esya depolama firmasi nasil secilir? 12 kritik kriter, kirmizi bayraklar, firma karsilastirma rehberi.',
        'focus_kw': 'depolama firmasi secerken dikkat',
    },
    111: {
        'seo_title': 'Ofis Tasima ve Depolama: Kurumsal Rehber - Evidepo',
        'meta_desc': 'Istanbul ofis tasima ve kurumsal depolama rehberi. Arsiv zorunluluklari, maliyet optimizasyonu, adim adim planlama.',
        'focus_kw': 'ofis tasima depolama',
    },
    # === ILCE SAYFALARI ===
    19: {'focus_kw': 'kadikoy esya depolama',
         'seo_title': 'Kadikoy Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Kadikoy esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Kadikoy ve cevresine ucretsiz alinir. Teklif alin.'},
    20: {'focus_kw': 'uskudar esya depolama',
         'seo_title': 'Uskudar Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Uskudar esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Uskudar ve cevresine ucretsiz alinir. Teklif alin.'},
    21: {'focus_kw': 'atasehir esya depolama',
         'seo_title': 'Atasehir Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Atasehir esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Atasehir ve cevresine ucretsiz alinir. Teklif alin.'},
    22: {'focus_kw': 'umraniye esya depolama',
         'seo_title': 'Umraniye Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Umraniye esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Umraniye ve cevresine ucretsiz alinir. Teklif alin.'},
    23: {'focus_kw': 'kartal esya depolama',
         'seo_title': 'Kartal Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Kartal esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Kartal ve cevresine ucretsiz alinir. Teklif alin.'},
    24: {'focus_kw': 'pendik esya depolama',
         'seo_title': 'Pendik Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Pendik esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Pendik ve cevresine ucretsiz alinir. Teklif alin.'},
    25: {'focus_kw': 'maltepe esya depolama',
         'seo_title': 'Maltepe Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Maltepe esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Maltepe ve cevresine ucretsiz alinir. Teklif alin.'},
    26: {'focus_kw': 'tuzla esya depolama',
         'seo_title': 'Tuzla Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Tuzla esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Tuzla ve cevresine ucretsiz alinir. Teklif alin.'},
    27: {'focus_kw': 'sancaktepe esya depolama',
         'seo_title': 'Sancaktepe Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Sancaktepe esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Sancaktepe ve cevresine ucretsiz alinir. Teklif alin.'},
    28: {'focus_kw': 'sultanbeyli esya depolama',
         'seo_title': 'Sultanbeyli Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Sultanbeyli esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Sultanbeyli ve cevresine ucretsiz alinir. Teklif alin.'},
    29: {'focus_kw': 'besiktas esya depolama',
         'seo_title': 'Besiktas Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Besiktas esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Besiktas ve cevresine ucretsiz alinir. Teklif alin.'},
    30: {'focus_kw': 'sisli esya depolama',
         'seo_title': 'Sisli Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Sisli esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Sisli ve cevresine ucretsiz alinir. Teklif alin.'},
    31: {'focus_kw': 'sariyer esya depolama',
         'seo_title': 'Sariyer Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Sariyer esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Sariyer ve cevresine ucretsiz alinir. Teklif alin.'},
    32: {'focus_kw': 'beylikduzu esya depolama',
         'seo_title': 'Beylikduzu Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Beylikduzu esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Beylikduzu ve cevresine ucretsiz alinir. Teklif alin.'},
    33: {'focus_kw': 'esenyurt esya depolama',
         'seo_title': 'Esenyurt Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Esenyurt esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Esenyurt ve cevresine ucretsiz alinir. Teklif alin.'},
    34: {'focus_kw': 'bakirkoy esya depolama',
         'seo_title': 'Bakirkoy Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Bakirkoy esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Bakirkoy ve cevresine ucretsiz alinir. Teklif alin.'},
    35: {'focus_kw': 'bahcelievler esya depolama',
         'seo_title': 'Bahcelievler Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Bahcelievler esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Bahcelievler ve cevresine ucretsiz alinir.'},
    36: {'focus_kw': 'kucukcekmece esya depolama',
         'seo_title': 'Kucukcekmece Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Kucukcekmece esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Kucukcekmece ve cevresine ucretsiz alinir.'},
    37: {'focus_kw': 'basaksehir esya depolama',
         'seo_title': 'Basaksehir Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Basaksehir esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Basaksehir ve cevresine ucretsiz alinir. Teklif alin.'},
    38: {'focus_kw': 'fatih esya depolama',
         'seo_title': 'Fatih Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Fatih esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Fatih ve cevresine ucretsiz alinir. Teklif alin.'},
    145: {'focus_kw': 'bagcilar esya depolama',
         'seo_title': 'Bagcilar Esya Depolama | Kilitli Oda - Evidepo',
         'meta_desc': 'Bagcilar esya depolama hizmeti. Kilitli ozel oda, 7/24 kamera, nakliyat dahil. Bagcilar ve cevresine ucretsiz alinir. Teklif alin.'},
}


def get_publisher():
    try:
        return WordPressPublisher()
    except ValueError as e:
        print(f"Hata: {e}")
        sys.exit(1)


def fix_rankmath_meta(wp):
    """Set RankMath SEO meta for all pages via REST API"""
    print("=" * 60)
    print("RANKMATH SEO META AYARLAMA")
    print("=" * 60)

    success = 0
    failed = 0

    for obj_id, meta in SEO_META.items():
        try:
            # First try RankMath API
            resp = wp.session.post(f'{wp.url}/wp-json/rankmath/v1/updateMeta', json={
                'objectID': obj_id,
                'objectType': 'post',
                'meta': {
                    'rank_math_focus_keyword': meta.get('focus_kw', ''),
                    'rank_math_title': meta.get('seo_title', ''),
                    'rank_math_description': meta.get('meta_desc', ''),
                }
            })

            if resp.status_code == 200:
                success += 1
                print(f"  [OK] ID:{obj_id:3d} | FK: {meta.get('focus_kw','')}")
            else:
                # Fallback: try via post meta
                resp2 = wp.session.post(
                    f'{wp.api_base}/pages/{obj_id}' if obj_id < 200 else f'{wp.api_base}/posts/{obj_id}',
                    json={
                        'meta': {
                            'rank_math_focus_keyword': meta.get('focus_kw', ''),
                            'rank_math_title': meta.get('seo_title', ''),
                            'rank_math_description': meta.get('meta_desc', ''),
                        }
                    }
                )
                if resp2.status_code in [200, 201]:
                    success += 1
                    print(f"  [OK-fallback] ID:{obj_id:3d} | FK: {meta.get('focus_kw','')}")
                else:
                    failed += 1
                    print(f"  [FAIL] ID:{obj_id:3d} | Status: {resp.status_code} / {resp2.status_code}")
        except Exception as e:
            failed += 1
            print(f"  [ERROR] ID:{obj_id:3d} | {e}")

    print(f"\nSonuc: {success} basarili, {failed} basarisiz")
    return success, failed


def fix_double_h1(wp):
    """Fix double H1 tags by converting content H1s to H2s"""
    print("\n" + "=" * 60)
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
                    resp2 = wp.session.post(f'{wp.api_base}/{post_type}/{pid}', json={
                        'content': new_content
                    })
                    resp2.raise_for_status()
                    fixed += 1
                    h1_text = re.sub(r'<[^>]+>', '', h1_tags[0]).strip()[:50]
                    print(f"  [OK] ID:{pid} | {title} -> \"{h1_text}\" H1->H2")
                except Exception as e:
                    print(f"  [FAIL] ID:{pid} | {title} -> {e}")

            page_num += 1

    print(f"\n{fixed} sayfada H1 -> H2 duzeltildi.")
    return fixed


def fix_internal_links(wp):
    """Fix broken internal links in page content"""
    print("\n" + "=" * 60)
    print("IC BAGLANTI DUZELTME")
    print("=" * 60)

    # Known broken link patterns and their fixes
    link_fixes = {
        '/hizmetlerimiz/ev-eşyası-depolama/': '/hizmetlerimiz/ev-esyasi-depolama/',
        '/hizmetlerimiz/kentsel-dönüşüm-depolama/': '/hizmetlerimiz/kentsel-donusum-depolama/',
        '/hizmetlerimiz/nakliyat-ve-depolama/': '/hizmetlerimiz/nakliyat-depolama/',
    }

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

                new_content = raw_content
                changes = []
                for old_link, new_link in link_fixes.items():
                    if old_link in new_content:
                        new_content = new_content.replace(old_link, new_link)
                        changes.append(f"{old_link} -> {new_link}")

                if changes:
                    try:
                        resp2 = wp.session.post(f'{wp.api_base}/{post_type}/{pid}', json={
                            'content': new_content
                        })
                        resp2.raise_for_status()
                        fixed += 1
                        for ch in changes:
                            print(f"  [OK] ID:{pid} | {title} | {ch}")
                    except Exception as e:
                        print(f"  [FAIL] ID:{pid} | {title} | {e}")

            page_num += 1

    print(f"\n{fixed} sayfada ic baglanti duzeltildi.")
    return fixed


def main():
    wp = get_publisher()

    print("EVIDEPO.COM KAPSAMLI SEO DUZELTME")
    print("=" * 60)

    # 1. Fix RankMath meta (title, description, focus keyword)
    fix_rankmath_meta(wp)

    # 2. Fix double H1 tags
    fix_double_h1(wp)

    # 3. Fix internal links
    fix_internal_links(wp)

    print("\n" + "=" * 60)
    print("TAMAMLANDI!")
    print("=" * 60)


if __name__ == '__main__':
    main()
