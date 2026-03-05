#!/usr/bin/env python3
"""
FAQ genişletme: 7 yeni soru ekle
- /sikca-sorulan-sorular/ sayfasına (WordPress blocks)
- Homepage FAQ bölümüne (custom HTML)
- MU-plugin FAQPage schema'ya (JSON-LD)
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
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'

FAQ_PAGE_ID = 18
HOMEPAGE_ID = 6

# ==========================================
# Yeni 7 FAQ - tek kaynak
# ==========================================
NEW_FAQS = [
    {
        "q": "İstanbul'da eşya depolama fiyatları ne kadar?",
        "a": "Eşya depolama fiyatları oda boyutuna ve kiralama süresine göre değişir. Evidepo'da 5m², 10m² ve 20m² oda seçenekleri mevcuttur. Ücretsiz ekspertiz hizmetimizle eşyalarınıza en uygun oda boyutunu ve fiyatı birlikte belirleriz. Gizli ücret uygulamıyoruz."
    },
    {
        "q": "Pendik dışındaki ilçelerden de hizmet alabilir miyim?",
        "a": "Evet. Depomuz Pendik'te bulunmakla birlikte, Sanat Evden Eve Nakliyat ekibimiz İstanbul'un Anadolu ve Avrupa yakasındaki tüm ilçelerden eşya alıp depoya taşır. Kadıköy, Ataşehir, Beşiktaş, Bakırköy dahil tüm ilçelere hizmet veriyoruz."
    },
    {
        "q": "Depolama alanları nemli veya rutubetli mi?",
        "a": "Hayır. Depolama odalarımız kuru, temiz ve bakımlı alanlardır. Düzenli temizlik ve havalandırma yapılır. Eşyalarınız nem, toz ve haşereden korunarak saklanır."
    },
    {
        "q": "Kentsel dönüşüm için uzun süreli depolama yapıyor musunuz?",
        "a": "Evet. Kentsel dönüşüm süreçleri için özel uzun süreli depolama paketlerimiz mevcuttur. Uzun süreli kiralamada avantajlı fiyatlar sunuyoruz."
    },
    {
        "q": "Evidepo ile diğer depolama firmaları arasındaki fark nedir?",
        "a": "Evidepo'da her müşteriye kişiye özel kilitli oda tahsis edilir ve anahtar yalnızca müşteride kalır. Firma dahil kimse odanıza erişemez. Ayrıca Sanat Evden Eve Nakliyat iştiraki olarak nakliyat ve depolama tek elden sunulur."
    },
    {
        "q": "Taşınma sırasında eşyalarım zarar görür mü?",
        "a": "Sanat Evden Eve Nakliyat'ın profesyonel ekibi eşyalarınızı özenle paketler ve taşır. Eşyalarınız sözleşme kapsamında güvence altındadır."
    },
    {
        "q": "Depo alanını görebilir miyim?",
        "a": "Evet. Randevu alarak depomuzu ziyaret edebilir, odaları yerinde görebilirsiniz. Ücretsiz ekspertiz hizmetimiz kapsamında ekibimiz size depolama alanlarını tanıtır."
    }
]


def wp_api_get(rest_route, retries=4):
    """WordPress REST API GET (curl ile, Imunify360 retry)."""
    import time
    for attempt in range(retries):
        result = subprocess.run([
            'curl', '-s',
            '-u', f'{WP_USER}:{WP_PASS}',
            '-H', f'User-Agent: {UA}',
            '-H', 'Accept: text/html,application/xhtml+xml,application/json',
            f'{WP_URL}/?rest_route={rest_route}'
        ], capture_output=True, text=True)
        data = json.loads(result.stdout)
        if 'message' in data and 'denied' in str(data.get('message', '')).lower():
            wait = 2 ** (attempt + 1)  # 2, 4, 8, 16
            print(f"   ⏳ Imunify360 engeli, {wait}s bekleniyor... (deneme {attempt+1}/{retries})")
            time.sleep(wait)
            continue
        return data
    raise RuntimeError(f"API erişim engellendi (tüm denemeler başarısız)")


def wp_api_post(rest_route, payload, retries=4):
    """WordPress REST API POST (curl ile, Imunify360 retry)."""
    import time
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
        tmp_path = f.name

    try:
        for attempt in range(retries):
            result = subprocess.run([
                'curl', '-s',
                '-X', 'POST',
                '-u', f'{WP_USER}:{WP_PASS}',
                '-H', f'User-Agent: {UA}',
                '-H', 'Content-Type: application/json',
                '-H', 'Accept: text/html,application/xhtml+xml,application/json',
                '-d', f'@{tmp_path}',
                f'{WP_URL}/?rest_route={rest_route}'
            ], capture_output=True, text=True)
            data = json.loads(result.stdout)
            if 'message' in data and 'denied' in str(data.get('message', '')).lower():
                wait = 2 ** (attempt + 1)
                print(f"   ⏳ Imunify360 engeli, {wait}s bekleniyor... (deneme {attempt+1}/{retries})")
                time.sleep(wait)
                continue
            return data
        raise RuntimeError("API erişim engellendi (tüm denemeler başarısız)")
    finally:
        os.unlink(tmp_path)


def update_faq_page():
    """SSS sayfasına 7 yeni soru ekle (WordPress block formatında)."""
    print("\n📝 FAQ sayfası güncelleniyor (ID: 18)...")

    data = wp_api_get(f'/wp/v2/pages/{FAQ_PAGE_ID}&context=edit')
    raw = data['content']['raw']

    # Yeni soruları WordPress block formatında oluştur
    new_blocks = ""
    for faq in NEW_FAQS:
        new_blocks += f"""
<!-- wp:heading {{"level":3}} -->
<h3>{faq['q']}</h3>
<!-- /wp:heading -->
<p>{faq['a']}</p>
"""

    # Mevcut içeriğin sonuna ekle
    new_content = raw.rstrip() + "\n" + new_blocks

    result = wp_api_post(f'/wp/v2/pages/{FAQ_PAGE_ID}', {'content': new_content})
    print(f"   ✓ Güncellendi! Modified: {result.get('modified')}")
    return True


def update_homepage_faq():
    """Homepage FAQ bölümüne 7 yeni soru ekle (ev-faq-item formatında)."""
    print("\n📝 Homepage FAQ bölümü güncelleniyor (ID: 6)...")

    data = wp_api_get(f'/wp/v2/pages/{HOMEPAGE_ID}&context=edit')
    raw = data['content']['raw']

    # Yeni FAQ item'ları oluştur (mevcut formatla aynı)
    new_faq_items = ""
    for faq in NEW_FAQS:
        q_escaped = faq['q'].replace("'", "&#39;")
        a_escaped = faq['a'].replace("'", "&#39;")
        new_faq_items += f'<div class="ev-faq-item"><div class="ev-faq-q" onclick="this.parentElement.classList.toggle(\'open\')">{faq["q"]}</div><div class="ev-faq-a"><p>{faq["a"]}</p></div></div>\n'

    # Son FAQ item'ından sonra, ev-faq div kapanışından önce ekle
    # Marker: son faq-item kapanışı + </div>\n</div>\n\n<!-- CTA -->
    last_faq_marker = "Gizli ücret yoktur.</p></div></div>\n</div>\n</div>\n\n<!-- CTA -->"
    if last_faq_marker in raw:
        raw = raw.replace(
            last_faq_marker,
            "Gizli ücret yoktur.</p></div></div>\n" + new_faq_items + "</div>\n</div>\n\n<!-- CTA -->"
        )
    else:
        print("   ⚠️  FAQ bölümü bulunamadı!")
        # Debug: CTA civarını göster
        cta_idx = raw.find('<!-- CTA -->')
        if cta_idx > 0:
            print(f"   CTA öncesi: {repr(raw[cta_idx-200:cta_idx])}")
        return False

    # CSS'te ev-faq-a max-height'ı artır (uzun cevaplar için)
    raw = raw.replace(
        '.ev-faq-item.open .ev-faq-a{max-height:200px;',
        '.ev-faq-item.open .ev-faq-a{max-height:500px;'
    )

    result = wp_api_post(f'/wp/v2/pages/{HOMEPAGE_ID}', {'content': raw})
    print(f"   ✓ Güncellendi! Modified: {result.get('modified')}")
    return True


def main():
    print("=" * 50)
    print("FAQ Genişletme - 7 Yeni Soru")
    print("=" * 50)

    import time

    # 1. FAQ sayfası
    update_faq_page()

    # Imunify360 cooldown
    print("\n   ⏳ API cooldown bekleniyor (10s)...")
    time.sleep(10)

    # 2. Homepage FAQ bölümü
    update_homepage_faq()

    # 3. MU-plugin güncelleme bilgisi
    print("\n📋 MU-plugin FAQPage schema güncellenmeli:")
    print("   Dosya: wordpress/seo-machine-wpcode-manager.php")
    print("   (Bu dosya yerel olarak düzenlenip sunucuya yüklenecek)")

    print("\n✅ FAQ genişletme tamamlandı!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
