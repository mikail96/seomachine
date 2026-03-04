# eVidepo.com Kapsamlı SEO Audit Raporu

**Tarih:** 4 Mart 2026
**Site:** https://evidepo.com
**Tema:** GeneratePress
**SEO Eklentisi:** Rank Math SEO
**Cache:** LiteSpeed Cache
**CDN:** Cloudflare

---

## Genel Durum Özeti

| Kategori | Durum | Detay |
|----------|-------|-------|
| Sayfa Sayısı | 35 sayfa + 13 blog yazısı | Toplam 48 yayında içerik |
| İndeksleme | ✅ Sorunsuz | Tüm sayfalar `follow, index` |
| SSL/HTTPS | ✅ Aktif | Cloudflare üzerinden |
| Mobil Uyumluluk | ✅ Viewport doğru | `width=device-width, initial-scale=1` |
| HTML Dili | ✅ Doğru | `lang="tr"` |
| 404 Sayfası | ✅ Düzgün | Arama kutusu mevcut |
| WWW Yönlendirme | ✅ Çalışıyor | www → non-www 301 redirect |
| Gzip Sıkıştırma | ✅ Aktif | Tüm sayfalarda |
| Canonical Tags | ✅ Mevcut | Tüm sayfalarda doğru canonical |

---

## KRİTİK SORUNLAR (Hemen Düzeltilmeli)

### 1. ❌ SITEMAP INDEX 404

**Durum:** `sitemap_index.xml` 404 döndürüyor. `robots.txt`'de referans verilen sitemap çalışmıyor.

**Etki:** Google sitemap'i okuyamıyor, yeni içeriklerin keşfedilmesi gecikiyor.

**Detay:**
- `sitemap_index.xml` → 404 ❌
- `post-sitemap.xml` → 200 ✅ (14 URL)
- `page-sitemap.xml` → 200 ✅ (34 URL)
- `category-sitemap.xml` → 200 ✅ (6 URL)

**Yapılan:** Rank Math sitemap modülü aktifleştirildi. Alt sitemap'ler çalışıyor.

**Yapılması Gereken (WordPress Admin'den):**
1. WordPress Admin → Ayarlar → Kalıcı Bağlantılar → "Değişiklikleri Kaydet" butonuna basın (rewrite kurallarını yenilemek için)
2. Rank Math → Genel Ayarlar → Sitemap → "Sitemap" modülünün aktif olduğunu doğrulayın
3. Doğrulama: `https://evidepo.com/sitemap_index.xml` açılmalı
4. Google Search Console'dan sitemap'leri submit edin:
   - `https://evidepo.com/sitemap_index.xml` (düzeldikten sonra)
   - Düzelmezse alt sitemap'leri ayrı ayrı ekleyin:
     - `https://evidepo.com/post-sitemap.xml`
     - `https://evidepo.com/page-sitemap.xml`

---

### 2. ❌ BOZUK SCHEMA MARKUP (Tüm Sayfalarda)

**Durum:** Her sayfada 4-5 adet duplike LocalBusiness/SelfStorage schema var. Bunlardan **biri INVALID JSON** içeriyor.

**Etki:** Google Schema doğrulama hataları, zengin sonuç kaybı, Search Console hata raporları.

**Detay:**
Her sayfada şu schema'lar mevcut:
1. ✅ Rank Math'ın kendi schema'sı (Organization + BreadcrumbList) — Doğru
2. ❌ SelfStorage + LocalBusiness — Header'dan (duplike #1)
3. ❌ SelfStorage + LocalBusiness — Header'dan (duplike #2)
4. ❌ SelfStorage + LocalBusiness — **INVALID JSON** (`"description":"description":` duplike key)
5. ❌ LocalBusiness — Footer'dan (duplike #3)

**Kaynak:** WPCode Lite (Insert Headers and Footers) eklentisi veya GeneratePress tema şablonları.

**Yapılması Gereken (WordPress Admin'den):**
1. WordPress Admin → Code Snippets (WPCode) → Tüm snippet'leri kontrol edin
2. Schema/LocalBusiness/JSON-LD içeren snippet'leri **deaktif edin veya silin**
3. Aynı şekilde Görünüm → Tema Düzenleyici → header.php ve footer.php dosyalarında ld+json script'lerini arayın
4. Sadece Rank Math'ın schema'sını bırakın — o zaten Organization + BreadcrumbList üretiyor
5. Rank Math → Schema Templates → Anasayfa için LocalBusiness schema eklenebilir (tek ve doğru)

**Bozuk JSON Hatası:**
```
"description":"description": "İstanbul'da güvenli..."
```
`"description"` key'i iki kez yazılmış. Bu script tamamen kaldırılmalı.

---

### 3. ❌ SSS Sayfasında FAQ Schema Eksik

**Durum:** Sıkça Sorulan Sorular sayfasında FAQPage schema markup yok.

**Etki:** Google'da zengin sonuçlar (FAQ rich snippets) gösterilemiyor.

**Yapılması Gereken:**
1. Rank Math → SSS sayfasını düzenleyin → Schema sekmesi → FAQPage schema ekleyin
2. Veya SSS içeriğini Rank Math FAQ block'u ile yeniden oluşturun

---

## ORTA ÖNCELİKLİ SORUNLAR

### 4. ⚠️ OG Image Tüm Sayfalarda Eksik

**Durum:** Hiçbir sayfada `og:image` meta tag'ı yok.

**Etki:** Sosyal medyada (Facebook, LinkedIn, WhatsApp) paylaşıldığında görsel gösterilmiyor.

**Yapılması Gereken:**
1. Rank Math → Genel Ayarlar → Social Meta → Varsayılan OG Image ekleyin (evidepo logo veya marka görseli)
2. Tüm önemli sayfaların öne çıkan görselini (featured image) ayarlayın

---

### 5. ⚠️ İlçe Sayfalarında Yüksek İçerik Benzerliği

**Durum:** 21 ilçe sayfası arasında %72-75 kelime örtüşmesi var. Her sayfa ~450-480 kelime.

**Örtüşen çiftler:**
- Beşiktaş vs Bakırköy: %75
- Esenyurt vs Şişli: %73
- Bakırköy vs Şişli: %72

**Etki:** Google duplicate content olarak değerlendirebilir, sıralama düşüşü riski.

**Öneriler:**
- Her ilçe sayfasına o ilçeye özel paragraflar ekleyin (ulaşım, bölge özellikleri, yakın depolar)
- İlçeye özel müşteri yorumları/testimonial'lar ekleyin
- Her sayfayı en az 800 kelimeye çıkarın
- İlçe haritası veya konum görseli ekleyin

---

### 6. ⚠️ HSTS Header Eksik

**Durum:** `Strict-Transport-Security` header'ı yok.

**Etki:** Tarayıcı her seferinde HTTP → HTTPS yönlendirmesi bekliyor, küçük güvenlik riski.

**Yapılması Gereken:** Cloudflare Dashboard → SSL/TLS → Edge Certificates → "Always Use HTTPS" ve "HSTS" aktifleştirin.

---

### 7. ⚠️ Cache-Control: no-cache

**Durum:** Anasayfa `cache-control: no-cache, no-store, must-revalidate` döndürüyor.

**Etki:** LiteSpeed cache hit veriyor ama tarayıcı cache yapmıyor, gereksiz yeniden yükleme.

**Yapılması Gereken:** LiteSpeed Cache ayarlarından uygun cache-control header'ları ayarlayın (statik sayfalar için `max-age=3600` gibi).

---

## YAPILAN DÜZELTMELERİN ÖZETİ

### Meta Title/Description Optimizasyonları

| Sayfa | Eski Title (char) | Yeni Title (char) |
|-------|-------------------|-------------------|
| Anasayfa | Eşya Depolama İstanbul \| Kilitli Oda, Anahtar Sizde \| Evidepo (61) | Eşya Depolama İstanbul \| Kilitli Oda \| Evidepo (46) |
| Hizmetlerimiz | Depolama Hizmetlerimiz \| Ev, Ofis, Tadilat, Kentsel Dönüşüm \| Evidepo (69) | Depolama Hizmetleri \| Ev, Ofis, Tadilat \| Evidepo (49) |
| Fiyatlar | Eşya Depolama Fiyatları 2026 \| Güncel Fiyat Listesi \| Evidepo (61) | Eşya Depolama Fiyatları 2026 \| Evidepo (38) |

### Focus Keyword Atama

Tüm 35 sayfa ve 13 blog yazısı için Rank Math focus keyword atandı:
- Ana sayfalar: Hizmet bazlı anahtar kelimeler
- İlçe sayfaları: `[ilçe adı] eşya depolama` formatı
- Blog yazıları: Önceden atanmış keyword'ler korundu

### Rank Math Sitemap Modülü
- Aktifleştirildi (daha önce kapalıydı)
- Alt sitemap'ler çalışıyor, index dosyası sunucu rewrite gerektirebilir

---

## SONRAKI ADIMLAR (Öncelik Sırasına Göre)

1. **[ACİL]** WordPress Admin'den permalink kaydet → Sitemap index'i düzeltir
2. **[ACİL]** WPCode/tema'daki duplike schema'ları kaldır
3. **[ACİL]** Google Search Console'a sitemap submit et
4. **[YÜKSEK]** Tüm sayfalara OG image ekle
5. **[YÜKSEK]** SSS sayfasına FAQ schema ekle
6. **[ORTA]** İlçe sayfalarını benzersiz içerikle zenginleştir
7. **[ORTA]** Cloudflare'den HSTS aktifleştir
8. **[DÜŞÜK]** Cache-control header'larını optimize et
