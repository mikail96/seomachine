"""Fix all RankMath SEO meta with proper Turkish characters"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'data_sources' / 'modules'))

from dotenv import load_dotenv
for p in [Path(__file__).parent / 'data_sources' / 'config' / '.env', Path(__file__).parent / '.env']:
    if p.exists():
        load_dotenv(p)
        break

from wordpress_publisher import WordPressPublisher

SEO_META = {
    # === ANASAYFA ===
    6: {
        'rank_math_title': 'İstanbul Eşya Depolama | Kilitli Oda Kiralama — Evidepo',
        'rank_math_description': 'İstanbul eşya depolama hizmeti. Güvenli, kameralı, kilitli oda sistemi. Randevulu erişim, Allianz sigorta, ücretsiz nakliyat. Hemen teklif alın.',
        'rank_math_focus_keyword': 'eşya depolama istanbul',
    },
    # === HIZMET SAYFALARI ===
    8: {
        'rank_math_title': 'Eşya Depolama Hizmetlerimiz | İstanbul — Evidepo',
        'rank_math_description': 'İstanbul kilitli oda depolama, nakliyat, paketleme, kentsel dönüşüm ve tadilat depolama. Ev, ofis, yurt dışı depolama hizmetleri.',
        'rank_math_focus_keyword': 'depolama hizmetleri',
    },
    9: {
        'rank_math_title': 'Ev Eşyası Depolama İstanbul | Kilitli Oda — Evidepo',
        'rank_math_description': 'İstanbul ev eşyası depolama. Kilitli özel odalar, Allianz sigorta, randevulu erişim. Profesyonel paketleme ve nakliyat dahil. Ücretsiz ekspertiz.',
        'rank_math_focus_keyword': 'ev eşyası depolama',
    },
    10: {
        'rank_math_title': 'Ofis Depolama İstanbul | Kurumsal Çözümler — Evidepo',
        'rank_math_description': 'İstanbul ofis eşyası ve arşiv depolama. Kurumsal sözleşme, faturalı hizmet, kilitli oda. Profesyonel paketleme dahil. Teklif alın.',
        'rank_math_focus_keyword': 'ofis depolama',
    },
    11: {
        'rank_math_title': 'Tadilat Depolama İstanbul | Geçici Eşya Saklama — Evidepo',
        'rank_math_description': 'Ev tadilatı sırasında eşyalarınızı güvenle depolayın. 1 aydan başlayan esnek süreler, nakliyat dahil. Tadilat bitince geri getiriyoruz.',
        'rank_math_focus_keyword': 'tadilat depolama',
    },
    12: {
        'rank_math_title': 'Kentsel Dönüşüm Depolama İstanbul — Evidepo',
        'rank_math_description': 'Kentsel dönüşüm sürecinde eşyalarınızı güvenle depolayın. 18-36 ay esnek sözleşme, uzun süreli indirim. Ücretsiz ekspertiz alın.',
        'rank_math_focus_keyword': 'kentsel dönüşüm depolama',
    },
    13: {
        'rank_math_title': 'Yurt Dışı Eşya Depolama İstanbul — Evidepo',
        'rank_math_description': 'Yurt dışına çıkarken eşyalarınızı güvenle depolayın. Uzun süreli indirim, uzaktan erişim, 7/24 kamera güvenliği. Hemen teklif alın.',
        'rank_math_focus_keyword': 'yurt dışı depolama',
    },
    14: {
        'rank_math_title': 'Nakliyat ve Depolama İstanbul | Tek Elden — Evidepo',
        'rank_math_description': 'İstanbul nakliyat ve depolama hizmeti tek elden. Sanat Evden Eve Nakliyat güvencesiyle taşıma ve depolama. Ücretsiz ekspertiz alın.',
        'rank_math_focus_keyword': 'nakliyat ve depolama',
    },
    # === DİĞER SAYFALAR ===
    15: {
        'rank_math_title': 'Eşya Depolama Fiyatları 2026 | İstanbul — Evidepo',
        'rank_math_description': 'İstanbul eşya depolama fiyatları 2026. Kilitli oda kiralama ücretleri, aylık depolama maliyetleri. Şeffaf fiyatlandırma, gizli ücret yok.',
        'rank_math_focus_keyword': 'eşya depolama fiyatları',
    },
    17: {
        'rank_math_title': 'Nasıl Çalışır? | Evidepo Eşya Depolama Süreci',
        'rank_math_description': 'Evidepo eşya depolama nasıl çalışır? Teklif al, eşyaları teslim et, güvenle depola. 4 kolay adımda depolama süreci.',
        'rank_math_focus_keyword': 'eşya depolama nasıl çalışır',
    },
    18: {
        'rank_math_title': 'Eşya Depolama SSS | Sıkça Sorulan Sorular — Evidepo',
        'rank_math_description': 'Eşya depolama hakkında merak edilen her şey. Güvenlik, fiyat, erişim, sigorta, nakliyat ve daha fazlası. Sorularınızın cevapları burada.',
        'rank_math_focus_keyword': 'eşya depolama sıkça sorulan sorular',
    },
    7: {
        'rank_math_title': 'Hakkımızda | Evidepo — Sanat Nakliyat İştiraki',
        'rank_math_description': 'Evidepo, Sanat Evden Eve Nakliyat iştiraki olarak İstanbul güvenli eşya depolama hizmeti sunuyor. Hikayemiz ve değerlerimiz.',
        'rank_math_focus_keyword': 'evidepo hakkımızda',
    },
    16: {
        'rank_math_title': 'İletişim | Evidepo Eşya Depolama İstanbul',
        'rank_math_description': 'Evidepo iletişim. İstanbul eşya depolama hizmeti için teklif alın. 0535 529 81 92. WhatsApp ile hızlı iletişim.',
        'rank_math_focus_keyword': 'evidepo iletişim',
    },
    105: {
        'rank_math_title': 'Eşya Depolama Blog | Rehberler ve İpuçları — Evidepo',
        'rank_math_description': 'Eşya depolama, nakliyat, paketleme rehberleri ve ipuçları. İstanbul depolama hakkında bilmeniz gereken her şey Evidepo blogunda.',
        'rank_math_focus_keyword': 'eşya depolama blog',
    },
    # === BLOG YAZILARI ===
    101: {
        'rank_math_title': 'İstanbul Eşya Depolama: 2026 Kapsamlı Rehber — Evidepo',
        'rank_math_description': 'İstanbul eşya depolama hakkında bilmeniz gereken her şey. Firma seçimi, fiyatlar, güvenlik kriterleri. 2026 güncel kapsamlı rehber.',
        'rank_math_focus_keyword': 'istanbul eşya depolama',
    },
    102: {
        'rank_math_title': 'Eşya Depolama Fiyatları 2026: Fiyat Rehberi — Evidepo',
        'rank_math_description': 'İstanbul eşya depolama fiyatları 2026. Oda boyutuna göre ücretler, gizli maliyetler, tasarruf yöntemleri. Güncel fiyat rehberi.',
        'rank_math_focus_keyword': 'eşya depolama fiyatları',
    },
    106: {
        'rank_math_title': 'Kentsel Dönüşümde Eşya Depolama Rehberi — Evidepo',
        'rank_math_description': 'Kentsel dönüşüm sürecinde eşya depolama rehberi. İlçe bazlı dönüşüm haritası, maliyet karşılaştırması, uzun süreli çözümler.',
        'rank_math_focus_keyword': 'kentsel dönüşüm eşya depolama',
    },
    107: {
        'rank_math_title': 'Tadilat Sırasında Eşya Koruma Rehberi — Evidepo',
        'rank_math_description': 'Ev tadilatı sırasında eşya koruma rehberi. 7 risk faktörü, koruma yöntemleri, depolama karşılaştırması. Pratik ipuçları.',
        'rank_math_focus_keyword': 'tadilat sırasında eşya depolama',
    },
    108: {
        'rank_math_title': 'Yurt Dışına Çıkarken Eşya Depolama Rehberi — Evidepo',
        'rank_math_description': 'Yurt dışına çıkarken eşyalarınız ne olacak? Evi tutmak vs depolama maliyet karşılaştırması, checklist ve pratik rehber.',
        'rank_math_focus_keyword': 'yurt dışına çıkarken eşya depolama',
    },
    109: {
        'rank_math_title': 'Eşya Paketleme Rehberi: Adım Adım Kılavuz — Evidepo',
        'rank_math_description': 'Depolama öncesi profesyonel paketleme teknikleri. Mobilya, elektronik, kırılacak eşya paketleme. Adım adım kılavuz.',
        'rank_math_focus_keyword': 'eşya paketleme rehberi',
    },
    110: {
        'rank_math_title': 'Depolama Firması Seçerken 12 Kriter — Evidepo',
        'rank_math_description': 'Eşya depolama firması nasıl seçilir? 12 kritik kriter, kırmızı bayraklar, firma karşılaştırma rehberi.',
        'rank_math_focus_keyword': 'depolama firması seçerken dikkat',
    },
    111: {
        'rank_math_title': 'Ofis Taşıma ve Depolama: Kurumsal Rehber — Evidepo',
        'rank_math_description': 'İstanbul ofis taşıma ve kurumsal depolama rehberi. Arşiv zorunlulukları, maliyet optimizasyonu, adım adım planlama.',
        'rank_math_focus_keyword': 'ofis taşıma depolama',
    },
    # === İLÇE SAYFALARI ===
    19: {
        'rank_math_title': 'Kadıköy Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Kadıköy eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Kadıköy ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'kadıköy eşya depolama',
    },
    20: {
        'rank_math_title': 'Üsküdar Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Üsküdar eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Üsküdar ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'üsküdar eşya depolama',
    },
    21: {
        'rank_math_title': 'Ataşehir Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Ataşehir eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Ataşehir ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'ataşehir eşya depolama',
    },
    22: {
        'rank_math_title': 'Ümraniye Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Ümraniye eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Ümraniye ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'ümraniye eşya depolama',
    },
    23: {
        'rank_math_title': 'Kartal Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Kartal eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Kartal ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'kartal eşya depolama',
    },
    24: {
        'rank_math_title': 'Pendik Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Pendik eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Pendik ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'pendik eşya depolama',
    },
    25: {
        'rank_math_title': 'Maltepe Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Maltepe eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Maltepe ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'maltepe eşya depolama',
    },
    26: {
        'rank_math_title': 'Tuzla Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Tuzla eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Tuzla ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'tuzla eşya depolama',
    },
    27: {
        'rank_math_title': 'Sancaktepe Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Sancaktepe eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Sancaktepe ve çevresinden ücretsiz alınır.',
        'rank_math_focus_keyword': 'sancaktepe eşya depolama',
    },
    28: {
        'rank_math_title': 'Sultanbeyli Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Sultanbeyli eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Sultanbeyli ve çevresinden ücretsiz alınır.',
        'rank_math_focus_keyword': 'sultanbeyli eşya depolama',
    },
    29: {
        'rank_math_title': 'Beşiktaş Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Beşiktaş eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Beşiktaş ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'beşiktaş eşya depolama',
    },
    30: {
        'rank_math_title': 'Şişli Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Şişli eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Şişli ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'şişli eşya depolama',
    },
    31: {
        'rank_math_title': 'Sarıyer Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Sarıyer eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Sarıyer ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'sarıyer eşya depolama',
    },
    32: {
        'rank_math_title': 'Beylikdüzü Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Beylikdüzü eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Beylikdüzü ve çevresinden ücretsiz alınır.',
        'rank_math_focus_keyword': 'beylikdüzü eşya depolama',
    },
    33: {
        'rank_math_title': 'Esenyurt Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Esenyurt eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Esenyurt ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'esenyurt eşya depolama',
    },
    34: {
        'rank_math_title': 'Bakırköy Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Bakırköy eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Bakırköy ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'bakırköy eşya depolama',
    },
    35: {
        'rank_math_title': 'Bahçelievler Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Bahçelievler eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Bahçelievler ve çevresinden ücretsiz alınır.',
        'rank_math_focus_keyword': 'bahçelievler eşya depolama',
    },
    36: {
        'rank_math_title': 'Küçükçekmece Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Küçükçekmece eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Küçükçekmece ve çevresinden ücretsiz alınır.',
        'rank_math_focus_keyword': 'küçükçekmece eşya depolama',
    },
    37: {
        'rank_math_title': 'Başakşehir Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Başakşehir eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Başakşehir ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'başakşehir eşya depolama',
    },
    38: {
        'rank_math_title': 'Fatih Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Fatih eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Fatih ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'fatih eşya depolama',
    },
    145: {
        'rank_math_title': 'Bağcılar Eşya Depolama | Kilitli Oda — Evidepo',
        'rank_math_description': 'Bağcılar eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, nakliyat dahil. Bağcılar ve çevresinden ücretsiz alınır. Teklif alın.',
        'rank_math_focus_keyword': 'bağcılar eşya depolama',
    },
}

def main():
    wp = WordPressPublisher()

    print("RANKMATH TÜRKÇE META DÜZELTME")
    print("=" * 60)

    success = 0
    failed = 0

    for obj_id, meta in SEO_META.items():
        try:
            resp = wp.session.post(
                f'{wp.url}/wp-json/rankmath/v1/updateMeta',
                json={
                    'objectID': obj_id,
                    'objectType': 'post',
                    'meta': meta
                }
            )
            if resp.status_code == 200:
                success += 1
                fk = meta.get('rank_math_focus_keyword', '')
                print(f"  [OK] ID:{obj_id:3d} | {fk}")
            else:
                failed += 1
                print(f"  [FAIL] ID:{obj_id:3d} | {resp.status_code}: {resp.text[:100]}")
        except Exception as e:
            failed += 1
            print(f"  [ERROR] ID:{obj_id:3d} | {e}")

    print(f"\nSonuç: {success} başarılı, {failed} başarısız")


if __name__ == '__main__':
    main()
