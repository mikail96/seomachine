#!/usr/bin/env python3
"""
GEO (Generative Engine Optimization) - Evidepo Homepage Güncellemesi

AI arama motorları (ChatGPT, Gemini, Perplexity) için içerik optimizasyonu.
Mevcut SEO yapısını (Rank Math, schema, meta taglar) bozmadan:
1. Hero altına Entity Definition paragrafı ekler
2. H2 başlıklarını soru formatına çevirir
3. Her H2 altına answer block paragrafları ekler
"""

import json
import os
import subprocess
import sys
import tempfile
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'data_sources', 'config', '.env'))

WP_URL = os.getenv('WORDPRESS_URL', 'https://evidepo.com')
WP_USER = os.getenv('WORDPRESS_USERNAME', 'admin')
WP_PASS = os.getenv('WORDPRESS_APP_PASSWORD', '')
PAGE_ID = 6  # Homepage

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'


def get_page_raw_content():
    """WordPress REST API'den ham sayfa içeriğini al (curl ile)."""
    result = subprocess.run([
        'curl', '-s',
        '-u', f'{WP_USER}:{WP_PASS}',
        '-H', f'User-Agent: {UA}',
        '-H', 'Accept: text/html,application/xhtml+xml,application/json',
        f'{WP_URL}/?rest_route=/wp/v2/pages/{PAGE_ID}&context=edit'
    ], capture_output=True, text=True)
    data = json.loads(result.stdout)
    if 'content' not in data:
        raise RuntimeError(f"API hatası: {data.get('message', data)}")
    return data['content']['raw']


def update_page_content(new_content):
    """WordPress REST API ile sayfa içeriğini güncelle (curl ile)."""
    # JSON payload'ı geçici dosyaya yaz (büyük içerik için)
    payload = json.dumps({'content': new_content})
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(payload)
        tmp_path = f.name

    try:
        result = subprocess.run([
            'curl', '-s',
            '-X', 'POST',
            '-u', f'{WP_USER}:{WP_PASS}',
            '-H', f'User-Agent: {UA}',
            '-H', 'Content-Type: application/json',
            '-H', 'Accept: text/html,application/xhtml+xml,application/json',
            '-d', f'@{tmp_path}',
            f'{WP_URL}/?rest_route=/wp/v2/pages/{PAGE_ID}'
        ], capture_output=True, text=True)
        data = json.loads(result.stdout)
        return data
    finally:
        os.unlink(tmp_path)


def apply_geo_changes(html):
    """GEO değişikliklerini uygula."""

    # =========================================================
    # 1. ENTITY DEFINITION - Hero bölümünün hemen altına
    # =========================================================
    # Trust bar'dan hemen önce, hero kapanışından sonra ekle
    entity_block = '''
<!-- GEO: Entity Definition - AI arama motorları için -->
<div class="ev-entity-definition" style="max-width:900px;margin:0 auto;padding:32px 24px;text-align:center;">
<p style="font-family:'DM Sans',sans-serif;font-size:16px;line-height:1.8;color:#4A4640;margin:0;">Evidepo, İstanbul Pendik'te bulunan kişiye özel kilitli oda kiralama sistemiyle çalışan bir eşya depolama firmasıdır. Sanat Evden Eve Nakliyat iştiraki olarak nakliyat ve depolama hizmetini tek elden sunar. Her müşteriye ayrı kilitli oda tahsis edilir, anahtar yalnızca müşteride kalır. Tüm depolama alanları 7/24 güvenlik kamerası ile izlenir ve düzenli olarak temizlenir.</p>
</div>
'''

    # Trust bar'ın önüne entity block ekle
    html = html.replace(
        '<!-- TRUST BAR -->',
        entity_block + '\n<!-- TRUST BAR -->'
    )

    # =========================================================
    # 2. H2 BAŞLIKLARINI SORU FORMATINA ÇEVİR + ANSWER BLOCKS
    # =========================================================

    # 2a. Hizmetler bölümü
    html = html.replace(
        '<h2 class="ev-section-title">İstanbul Eşya Depolama Çözümleri</h2>\n<p class="ev-section-desc">Ev eşyasından ofis malzemelerine, tadilat sürecinden yurt dışı planlarına kadar yanınızdayız.</p>',
        '<h2 class="ev-section-title">İstanbul\'da Hangi Depolama Hizmetlerini Sunuyoruz?</h2>\n<p class="ev-section-desc">Evidepo olarak ev eşyası, ofis, tadilat, kentsel dönüşüm, yurt dışı ve nakliyat+depolama olmak üzere 6 farklı depolama hizmeti sunuyoruz. Tüm hizmetlerimizde kişiye özel kilitli oda, 7/24 kamera güvenliği ve Sanat Nakliyat güvencesi mevcuttur.</p>'
    )

    # 2b. Nasıl Çalışır bölümü
    html = html.replace(
        '<h2 class="ev-section-title">4 Adımda Kolay Depolama</h2>\n<p class="ev-section-desc">Sadece arayın, gerisini biz halledelim.</p>',
        '<h2 class="ev-section-title">Eşya Depolama Nasıl Çalışır?</h2>\n<p class="ev-section-desc">Evidepo\'da eşya depolama 4 basit adımda tamamlanır: Bize ulaşın, ücretsiz ekspertiz ile oda boyutunuzu belirleyin, Sanat Nakliyat ekibimiz eşyalarınızı taşısın ve kilitli odanızın anahtarını teslim alın. Tüm süreç profesyonel ekibimiz tarafından yönetilir.</p>'
    )

    # 2c. Neden Evidepo bölümü
    html = html.replace(
        '<h2 class="ev-section-title">İstanbul\'da Güvenli Eşya Depolama — Neden Evidepo?</h2>\n<p class="ev-section-desc">Sanat Evden Eve Nakliyat\'ın yıllara dayanan deneyimiyle güvenli depolama.</p>',
        '<h2 class="ev-section-title">Eşyalarınız Neden Evidepo\'da Güvende?</h2>\n<p class="ev-section-desc">Evidepo\'da her müşteriye özel kilitli oda tahsis edilir ve anahtar yalnızca müşteride kalır. 7/24 kamera güvenliği, düzenli temizlik, randevulu erişim ve Sanat Evden Eve Nakliyat\'ın yıllara dayanan deneyimi ile eşyalarınız eviniz kadar güvende.</p>'
    )

    # 2d. Fiyatlar bölümü
    html = html.replace(
        '<h2 class="ev-section-title">Eşya Depolama Fiyatları — Bütçenize Uygun</h2>\n<p class="ev-section-desc">Her ihtiyaca uygun oda boyutları. Gizli ücret yok, şeffaf fiyatlandırma.</p>',
        '<h2 class="ev-section-title">Eşya Depolama Fiyatları Ne Kadar?</h2>\n<p class="ev-section-desc">Evidepo eşya depolama fiyatları oda büyüklüğüne ve kiralama süresine göre belirlenir. Küçük (5-8 m²), orta (10-15 m²) ve büyük (20+ m²) oda seçenekleri mevcuttur. Gizli ücret yoktur, ücretsiz ekspertiz ile size en uygun fiyat teklifi sunulur.</p>'
    )

    # 2e. SSS bölümü
    html = html.replace(
        '<h2 class="ev-section-title">Merak Ettikleriniz</h2>',
        '<h2 class="ev-section-title">Eşya Depolama Hakkında Sıkça Sorulan Sorular</h2>'
    )

    return html


def main():
    print("📥 Homepage içeriği alınıyor...")
    raw_content = get_page_raw_content()
    print(f"   ✓ {len(raw_content)} karakter alındı")

    # Yedek al
    backup_path = os.path.join(os.path.dirname(__file__), '..', 'backups', 'homepage_pre_geo.html')
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(raw_content)
    print(f"   ✓ Yedek alındı: {backup_path}")

    print("\n🔄 GEO değişiklikleri uygulanıyor...")
    new_content = apply_geo_changes(raw_content)

    # Değişiklikleri doğrula
    changes = []
    if 'ev-entity-definition' in new_content:
        changes.append("Entity Definition paragrafı eklendi")
    if "Hangi Depolama Hizmetlerini Sunuyoruz?" in new_content:
        changes.append("Hizmetler H2 → soru formatı")
    if "Eşya Depolama Nasıl Çalışır?" in new_content:
        changes.append("Nasıl Çalışır H2 → soru formatı")
    if "Eşyalarınız Neden Evidepo'da Güvende?" in new_content:
        changes.append("Neden Evidepo H2 → soru formatı")
    if "Eşya Depolama Fiyatları Ne Kadar?" in new_content:
        changes.append("Fiyatlar H2 → soru formatı")
    if "Sıkça Sorulan Sorular" in new_content:
        changes.append("SSS H2 → soru formatı")

    for c in changes:
        print(f"   ✓ {c}")

    if len(changes) < 6:
        print("\n⚠️  Bazı değişiklikler uygulanamadı! Kontrol edin.")
        return 1

    # Değişiklik sonrası içeriği dosyaya kaydet (review için)
    review_path = os.path.join(os.path.dirname(__file__), '..', 'backups', 'homepage_post_geo.html')
    with open(review_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"\n📄 Yeni içerik review için kaydedildi: {review_path}")

    print(f"\n📤 WordPress'e gönderiliyor...")
    result = update_page_content(new_content)
    print(f"   ✓ Güncelleme başarılı! Sayfa ID: {result.get('id')}")
    print(f"   ✓ Güncellenme tarihi: {result.get('modified')}")

    print("\n✅ GEO optimizasyonu tamamlandı!")
    print("   Kontrol et: https://evidepo.com")
    return 0


if __name__ == '__main__':
    sys.exit(main())
