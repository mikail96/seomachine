# CLAUDE.md

Bu dosya, Claude Code'a (claude.ai/code) bu repodaki kodla çalışırken rehberlik sağlar.

## Proje Genel Bakış

SEO Machine, SEO odaklı blog içerikleri oluşturmak için açık kaynaklı bir Claude Code çalışma alanıdır. Özel komutlar, uzmanlaşmış ajanlar ve Python tabanlı analizleri bir araya getirerek herhangi bir işletme için araştırma, yazım, optimizasyon ve yayınlama işlemlerini gerçekleştirir.

## Kurulum

```bash
pip install -r data_sources/requirements.txt
```

API kimlik bilgileri `data_sources/config/.env` dosyasında yapılandırılır (GA4, GSC, DataForSEO, WordPress). GA4 hizmet hesabı kimlik bilgileri `credentials/ga4-credentials.json` dosyasına yerleştirilir.

## Komutlar

Tüm komutlar `.claude/commands/` dizininde tanımlanmıştır ve eğik çizgi komutları olarak çağrılır:

- `/research [konu]` - Anahtar kelime/rakip araştırması, `research/` klasörüne brief oluşturur
- `/write [konu]` - `drafts/` klasörüne tam makale oluşturur, optimizasyon ajanlarını otomatik tetikler
- `/rewrite [konu]` - Mevcut içeriği günceller, `rewrites/` klasörüne kaydeder
- `/optimize [dosya]` - Son SEO cilalama geçişi
- `/analyze-existing [URL veya dosya]` - İçerik sağlık denetimi
- `/performance-review` - Analitik odaklı içerik önceliklendirme
- `/publish-draft [dosya]` - WordPress REST API üzerinden yayınlama
- `/article [konu]` - Basitleştirilmiş makale oluşturma
- `/priorities` - İçerik önceliklendirme matrisi
- `/research-serp`, `/research-gaps`, `/research-trending`, `/research-performance`, `/research-topics` - Özel araştırma komutları
- `/landing-write`, `/landing-audit`, `/landing-research`, `/landing-publish`, `/landing-competitor` - Açılış sayfası komutları

## Mimari

### Komut-Ajan Modeli

**Komutlar** (`.claude/commands/`) iş akışlarını yönetir. **Ajanlar** (`.claude/agents/`) komutlar tarafından çağrılan uzmanlaşmış rollerdir. `/write` komutundan sonra bu ajanlar otomatik çalışır: SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper.

Temel ajanlar: `content-analyzer.md`, `seo-optimizer.md`, `meta-creator.md`, `internal-linker.md`, `keyword-mapper.md`, `editor.md`, `headline-generator.md`, `cro-analyst.md`, `performance.md`.

### Python Analiz Hattı

`data_sources/modules/` dizininde bulunur. İçerik Analizörü şu sırayla çalışır:
1. `search_intent_analyzer.py` - Arama niyeti sınıflandırması
2. `keyword_analyzer.py` - Yoğunluk, dağılım, anahtar kelime doldurmayı tespit
3. `content_length_comparator.py` - SERP ilk 10 sonuçla karşılaştırma
4. `readability_scorer.py` - Flesch Okunabilirlik Skoru, sınıf seviyesi
5. `seo_quality_rater.py` - Kapsamlı 0-100 SEO puanı

### Veri Entegrasyonları

- `google_analytics.py` - GA4 trafik/etkileşim verileri
- `google_search_console.py` - Sıralama ve gösterimler
- `dataforseo.py` - SERP pozisyonları, anahtar kelime metrikleri
- `data_aggregator.py` - Tüm kaynakları birleşik analize dönüştürür
- `wordpress_publisher.py` - Rank Math SEO meta verileriyle WordPress'e yayınlar

### Fırsat Puanlama

`opportunity_scorer.py` 8 ağırlıklı faktör kullanır: Hacim (%25), Pozisyon (%20), Niyet (%20), Rekabet (%15), Küme (%10), TO (%5), Tazelik (%5), Trend (%5).

## Python Scriptlerini Çalıştırma

```bash
# Araştırma ve analiz scriptleri (repo kök dizininden çalıştırın)
python3 research_quick_wins.py
python3 research_competitor_gaps.py
python3 research_performance_matrix.py
python3 research_priorities_comprehensive.py
python3 research_serp_analysis.py
python3 research_topic_clusters.py
python3 research_trending.py
python3 seo_baseline_analysis.py
python3 seo_bofu_rankings.py
python3 seo_competitor_analysis.py

# API bağlantısını test et
python3 test_dataforseo.py
```

## İçerik Hattı

`topics/` (fikirler) → `research/` (briefler) → `drafts/` (makaleler) → `review-required/` (inceleme bekleyen) → `published/` (son hali)

Yeniden yazımlar `rewrites/` klasörüne gider. Açılış sayfaları `landing-pages/` klasörüne gider. Denetimler `audits/` klasörüne gider.

## Bağlam Dosyaları

`context/` klasörü tüm içerik üretimini yönlendiren marka kurallarını içerir:
- `brand-voice.md` - Ton, mesaj ana hatları
- `style-guide.md` - Dilbilgisi, biçimlendirme standartları
- `seo-guidelines.md` - Anahtar kelime ve yapı kuralları
- `internal-links-map.md` - İç bağlantı için ana sayfalar
- `features.md` - Ürün özellikleri
- `competitor-analysis.md` - Rekabet istihbaratı
- `cro-best-practices.md` - Dönüşüm optimizasyonu kuralları

## WordPress Entegrasyonu

Yayınlama, Rank Math SEO alanlarını açığa çıkaran özel bir MU-eklentisi (`wordpress/seo-machine-rankmath-rest.php`) ile WordPress REST API kullanır. Makaleler WordPress blok formatında (Markdown dosyalarındaki HTML yorumları) yayınlanır.
