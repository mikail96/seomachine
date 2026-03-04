# WordPress Entegrasyon Dosyaları

Bu dosyalar, SEO Machine aracının REST API üzerinden Rank Math SEO meta alanlarını (Focus Keyword, SEO Title, Meta Description) ayarlamasını sağlar.

**BİR seçenek seçin** - ya MU-plugin YA DA functions.php snippet'i. İkisi de aynı işi yapar.

---

## Seçenek A: MU-Plugin (Önerilen)

**Dosya:** `seo-machine-rankmath-rest.php`

**Kurulum:**
1. Şuraya yükleyin: `wp-content/mu-plugins/seo-machine-rankmath-rest.php`
2. `mu-plugins` klasörü yoksa oluşturun
3. Tamam - mu-plugin'ler otomatik aktif olur, etkinleştirme gerekmez

**Artıları:**
- Tema güncellemelerinde kaybolmaz
- Yanlışlıkla devre dışı bırakılamaz
- Tema kodundan temiz ayrım

---

## Seçenek B: Functions.php Snippet

**Dosya:** `functions-snippet.php`

**Kurulum:**
1. Bu dosyanın içeriğini kopyalayın
2. Temanızın `functions.php` dosyasının sonuna yapıştırın
3. Veya bir kod snippet eklentisi kullanın (WPCode, Code Snippets, vb.)

**Artıları:**
- Yönetilecek yeni dosya yok
- Kod snippet eklentileriyle çalışır

**Eksileri:**
- Tema değiştirilir/güncellenirse kaybolur (child tema kullanılmıyorsa)

---

## Bu Kod Ne Yapar

Post ve page'lerde `rankmath_seo` adlı özel bir REST API alanı kaydeder:

- `focus_keyword` → `rank_math_focus_keyword`
- `seo_title` → `rank_math_title`
- `meta_description` → `rank_math_description`
- `robots` → `rank_math_robots`

**API Kullanımı:**
```json
POST /wp-json/wp/v2/posts/{id}
{
  "rankmath_seo": {
    "focus_keyword": "hedef anahtar kelime",
    "seo_title": "SEO Başlığınız | Marka",
    "meta_description": "Meta açıklamanız buraya."
  }
}
```

---

## Güvenlik

- Kimlik doğrulama gerektirir (Application Password)
- Kullanıcının `edit_post` yetkisi olmalı
- Tüm girdiler `sanitize_text_field()` ile temizlenir
