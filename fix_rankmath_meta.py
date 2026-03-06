#!/usr/bin/env python3
"""
Fix Rank Math SEO meta for all pages and posts.
Updates SEO title and description to include focus keywords properly.
"""

import requests
import json
import sys

WP_URL = "https://evidepo.com"
WP_USER = "admin"
WP_APP_PASS = "HQmY kKaQ kDY6 W91l v4G5 sHtA"

session = requests.Session()
session.auth = (WP_USER, WP_APP_PASS)

# Optimized meta data for each page/post
# Format: post_id -> { title, description }
# Rules: FK must appear in both title and desc, title < 60 chars, desc 120-160 chars
META_FIXES = {
    # ===== PAGES =====

    # Anasayfa - score 85, FK: eşya depolama istanbul
    6: {
        "title": "Eşya Depolama İstanbul | Kilitli Oda Sistemi | Evidepo",
        "desc": "İstanbul eşya depolama hizmeti. Kilitli özel oda, anahtar sizde, 7/24 kamera güvenliği ve nakliyat dahil. Ücretsiz ekspertiz için hemen arayın."
    },

    # Hakkımızda - FK: eşya depolama firması istanbul
    7: {
        "title": "Eşya Depolama Firması İstanbul | Evidepo Hakkımızda",
        "desc": "İstanbul eşya depolama firması Evidepo hakkında. Sanat Evden Eve Nakliyat iştiraki, Pendik merkezli, kilitli oda sistemi ve 7/24 kameralı güvenlik."
    },

    # Hizmetlerimiz - FK: eşya depolama hizmetleri istanbul
    8: {
        "title": "Eşya Depolama Hizmetleri İstanbul | Evidepo",
        "desc": "İstanbul eşya depolama hizmetleri: Ev eşyası, ofis, tadilat, kentsel dönüşüm, yurt dışı ve nakliyat depolama. Kilitli oda, 7/24 güvenlik."
    },

    # Ev Eşyası Depolama - FK: ev eşyası depolama istanbul
    9: {
        "title": "Ev Eşyası Depolama İstanbul | Evidepo",
        "desc": "İstanbul ev eşyası depolama hizmeti. Kilitli özel oda, 7/24 kamera güvenliği, profesyonel paketleme ve nakliyat dahil. Ücretsiz ekspertiz alın."
    },

    # Ofis Depolama - FK: ofis depolama istanbul
    10: {
        "title": "Ofis Depolama İstanbul | Kurumsal | Evidepo",
        "desc": "İstanbul ofis depolama hizmeti. Arşiv, ofis mobilyası ve kurumsal malzeme için kilitli oda. Faturalı hizmet. Ücretsiz ekspertiz için arayın."
    },

    # Tadilat Depolama - FK: tadilat depolama istanbul
    11: {
        "title": "Tadilat Depolama İstanbul | Evidepo",
        "desc": "İstanbul tadilat depolama hizmeti. Tadilat süresince eşyalarınız kilitli odada güvende. Paketleme, nakliyat dahil. Ücretsiz ekspertiz alın."
    },

    # Kentsel Dönüşüm - FK: kentsel dönüşüm eşya depolama
    12: {
        "title": "Kentsel Dönüşüm Eşya Depolama | Evidepo",
        "desc": "Kentsel dönüşüm eşya depolama hizmeti. Uzun süreli özel fiyatlar, nakliyat dahil, kilitli oda. Bina yıkımından yeni daireye kadar yanınızdayız."
    },

    # Yurt Dışı Depolama - FK: yurt dışı eşya depolama
    13: {
        "title": "Yurt Dışı Eşya Depolama | Evidepo İstanbul",
        "desc": "Yurt dışı eşya depolama hizmeti. Uzun süreli kilitli oda, 7/24 kamera güvenliği, yakınlarınıza erişim yetkisi. Ücretsiz ekspertiz alın."
    },

    # Nakliyat ve Depolama - FK: nakliyat ve depolama istanbul
    14: {
        "title": "Nakliyat ve Depolama İstanbul | Evidepo",
        "desc": "İstanbul nakliyat ve depolama tek elden. Eşyalarınızı alıyor, paketliyor, kilitli odada depoluyoruz. İhtiyacınızda geri getiriyoruz."
    },

    # Fiyatlar - FK: eşya depolama fiyatları (title > 60, fix)
    15: {
        "title": "Eşya Depolama Fiyatları 2026 | Evidepo",
        "desc": "2026 güncel eşya depolama fiyatları. Oda boyutuna göre aylık ücretler, fiyata dahil hizmetler ve ücretsiz ekspertiz. Evidepo İstanbul fiyat listesi."
    },

    # İletişim - FK: eşya depolama iletişim
    16: {
        "title": "Eşya Depolama İletişim | Evidepo | 0535 529 81 92",
        "desc": "Evidepo eşya depolama iletişim bilgileri. Pendik merkez depo. WhatsApp, telefon ve e-posta ile ücretsiz teklif alın. 0535 529 81 92."
    },

    # SSS - FK: eşya depolama sıkça sorulan sorular (desc too long)
    18: {
        "title": "Eşya Depolama Sıkça Sorulan Sorular | Evidepo",
        "desc": "Eşya depolama sıkça sorulan sorular: Güvenlik, sigorta, fiyatlar, minimum süre, erişim ve daha fazlası. Tüm yanıtlar bu sayfada."
    },

    # Blog - FK: eşya depolama blog
    105: {
        "title": "Eşya Depolama Blog | Rehberler | Evidepo",
        "desc": "Eşya depolama blog: İstanbul depolama, nakliyat, paketleme ve saklama ipuçları. Evidepo uzmanlarından pratik bilgiler ve kapsamlı rehberler."
    },

    # Hakkımızda already fixed above (7)

    # ===== İLÇE SAYFALARI =====
    # Pattern: FK is "[ilçe] eşya depolama", need to include in desc

    19: {
        "desc": "Kadıköy eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Kadıköy ve çevresinden ücretsiz ekspertiz."
    },
    20: {
        "desc": "Üsküdar eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Üsküdar ve çevresinden ücretsiz ekspertiz."
    },
    21: {
        "desc": "Ataşehir eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Ataşehir ve çevresinden ücretsiz ekspertiz."
    },
    22: {
        "desc": "Ümraniye eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Ümraniye ve çevresinden ücretsiz ekspertiz."
    },
    23: {
        "desc": "Kartal eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Kartal ve çevresinden ücretsiz ekspertiz."
    },
    24: {
        "desc": "Pendik eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Pendik merkezde depomuz mevcut."
    },
    25: {
        "desc": "Maltepe eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Maltepe ve çevresinden ücretsiz ekspertiz."
    },
    26: {
        "desc": "Tuzla eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera güvenliği, nakliyat dahil. Tuzla ve çevresinden ücretsiz ekspertiz."
    },
    27: {
        "desc": "Sancaktepe eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Sancaktepe ve çevresinden ücretsiz ekspertiz."
    },
    28: {
        "desc": "Sultanbeyli eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Sultanbeyli ve çevresinden ücretsiz ekspertiz."
    },
    29: {
        "desc": "Beşiktaş eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Beşiktaş ve çevresinden ücretsiz ekspertiz."
    },
    30: {
        "desc": "Şişli eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera güvenliği, nakliyat dahil. Şişli ve çevresinden ücretsiz ekspertiz."
    },
    31: {
        "desc": "Sarıyer eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Sarıyer ve çevresinden ücretsiz ekspertiz."
    },
    32: {
        "desc": "Beylikdüzü eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Beylikdüzü ve çevresinden ücretsiz ekspertiz."
    },
    33: {
        "desc": "Esenyurt eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Esenyurt ve çevresinden ücretsiz ekspertiz."
    },
    34: {
        "desc": "Bakırköy eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Bakırköy ve çevresinden ücretsiz ekspertiz."
    },
    35: {
        "desc": "Bahçelievler eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Bahçelievler ve çevresinden ücretsiz ekspertiz."
    },
    36: {
        "desc": "Küçükçekmece eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Küçükçekmece çevresinden ücretsiz ekspertiz."
    },
    37: {
        "desc": "Başakşehir eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Başakşehir ve çevresinden ücretsiz ekspertiz."
    },
    38: {
        "desc": "Fatih eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera güvenliği, nakliyat dahil. Fatih ve çevresinden ücretsiz ekspertiz."
    },
    145: {
        "desc": "Bağcılar eşya depolama hizmeti arıyorsanız doğru yerdesiniz. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Bağcılar ve çevresinden ücretsiz ekspertiz."
    },

    # ===== BLOG POSTS =====

    # Güvenli Eşya Depolama İstanbul - score 71, FK: güvenli eşya depolama istanbul
    252: {
        "title": "Güvenli Eşya Depolama İstanbul | 7 Altın Kural",
        "desc": "Güvenli eşya depolama İstanbul rehberi. Eşyalarınızı koruma altına almanın 7 altın kuralı: Kilitli oda, kamera, sigorta ve daha fazlası."
    },

    # Kiralık Eşya Deposu İstanbul - score 68, FK: kiralık eşya deposu istanbul
    254: {
        "title": "Kiralık Eşya Deposu İstanbul | Rehber 2026",
        "desc": "Kiralık eşya deposu İstanbul rehberi. Güvenli ve uygun fiyatlı depolama seçenekleri, fiyat karşılaştırması ve doğru depo seçim ipuçları."
    },

    # Uzun Süreli Eşya Depolama - FK: uzun süreli eşya depolama
    256: {
        "title": "Uzun Süreli Eşya Depolama | Evidepo Rehber",
        "desc": "Uzun süreli eşya depolama rehberi. Eşyalarınız yıllarca güvende kalsın: Kilitli oda, 7/24 kamera, sigorta güvencesi ve avantajlı uzun dönem fiyatları."
    },

    # Evden Eve Nakliyat ve Depolama - score 72, FK: evden eve nakliyat ve depolama
    # Already OK but let's improve desc slightly

    # Ofis Taşıma Depolama - FK: ofis taşıma depolama
    111: {
        "title": "Ofis Taşıma Depolama | İstanbul Rehber 2026",
        "desc": "İstanbul ofis taşıma depolama rehberi. Kurumsal taşınma planlaması, arşiv yönetimi, maliyet hesaplama ve süreç adımları. 2026 güncel kılavuz."
    },

    # Depolama Firması Seçerken - FK: depolama firması seçerken dikkat
    110: {
        "title": "Depolama Firması Seçerken Dikkat | 12 Kriter",
        "desc": "Depolama firması seçerken dikkat edilmesi gereken 12 kriter. Güvenlik, sigorta, fiyat şeffaflığı ve sözleşme detaylarıyla doğru firmayı bulun."
    },

    # Yurt Dışına Çıkarken Eşya Depolama - FK: yurt dışına çıkarken eşya depolama
    108: {
        "title": "Yurt Dışına Çıkarken Eşya Depolama | Rehber",
        "desc": "Yurt dışına çıkarken eşya depolama rehberi. Depolama süresi, sigorta, erişim yetkisi ve maliyet hakkında bilmeniz gereken her şey bu yazıda."
    },

    # Tadilat Sırasında - FK: tadilat sırasında eşya depolama
    107: {
        "title": "Tadilat Sırasında Eşya Depolama | Rehber",
        "desc": "Tadilat sırasında eşya depolama rehberi. Eşyalarınızı nasıl korursunuz? Paketleme, nakliyat, depolama ve geri taşıma sürecinin tüm adımları."
    },

    # Kentsel Dönüşümde - FK: kentsel dönüşüm eşya depolama
    106: {
        "title": "Kentsel Dönüşüm Eşya Depolama | Rehber",
        "desc": "Kentsel dönüşüm eşya depolama rehberi. Depolama süresi, fiyatlar, yasal haklar ve pratik adımlar. Eşyalarınızı güvenle saklayın."
    },

    # Eşya Depolama Fiyatları 2026 - FK: eşya depolama fiyatları 2026
    102: {
        "title": "Eşya Depolama Fiyatları 2026 | Fiyat Rehberi",
        "desc": "Eşya depolama fiyatları 2026 güncel rehberi. İstanbul oda boyutlarına göre aylık ücretler, fiyatı etkileyen faktörler ve tasarruf ipuçları."
    },

    # İstanbul Eşya Depolama Rehberi - FK: istanbul eşya depolama
    101: {
        "title": "İstanbul Eşya Depolama | 2026 Kapsamlı Rehber",
        "desc": "İstanbul eşya depolama hakkında bilmeniz gereken her şey. Fiyatlar, güvenlik kriterleri, firma seçimi ve depolama türleri. 2026 güncel rehber."
    },
}


def update_meta(post_id, key, value):
    """Update a single Rank Math meta via REST API."""
    resp = session.post(
        f"{WP_URL}/wp-json/seo-machine/v1/post-meta/{post_id}",
        json={"key": key, "value": value}
    )
    return resp.status_code == 200


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN MODE ===\n")

    total = 0
    errors = 0

    for post_id, fixes in META_FIXES.items():
        title = fixes.get("title")
        desc = fixes.get("desc")

        print(f"\n[{post_id}]", end=" ")

        if title:
            tlen = len(title)
            marker = "OK" if tlen <= 60 else f"WARN({tlen}ch)"
            print(f"Title ({marker}): {title}")
            if not dry_run:
                if update_meta(post_id, "rank_math_title", title):
                    total += 1
                else:
                    errors += 1
                    print(f"  ERROR updating title for {post_id}")

        if desc:
            dlen = len(desc)
            marker = "OK" if 120 <= dlen <= 160 else f"WARN({dlen}ch)"
            print(f"  Desc ({marker}): {desc}")
            if not dry_run:
                if update_meta(post_id, "rank_math_description", desc):
                    total += 1
                else:
                    errors += 1
                    print(f"  ERROR updating desc for {post_id}")

    print(f"\n{'='*60}")
    if dry_run:
        print(f"Would update meta for {len(META_FIXES)} pages/posts")
    else:
        print(f"Updated {total} meta fields, {errors} errors")


if __name__ == "__main__":
    main()
