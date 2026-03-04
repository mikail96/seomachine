<?php
/**
 * Plugin Name: Evidepo Rich Footer
 * Description: Adds a rich, SEO-optimized footer with services, contact, and district links.
 * Version: 1.0
 * Author: SEO Machine
 *
 * Installation:
 * 1. Upload this file to: wp-content/mu-plugins/evidepo-rich-footer.php
 * 2. That's it - mu-plugins are automatically activated
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('generate_before_footer', function() {
    ?>
    <div id="evidepo-footer" style="background:#0f1d35;color:#cbd5e1;padding:60px 0 30px;">
        <div style="max-width:1200px;margin:0 auto;padding:0 20px;">
            <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:40px;">

                <!-- Kolon 1: Hakkımızda -->
                <div>
                    <h3 style="color:#fff;font-size:18px;margin-bottom:16px;font-weight:600;">Evidepo</h3>
                    <p style="font-size:14px;line-height:1.7;margin-bottom:12px;">İstanbul'un güvenilir eşya depolama hizmeti. Sanat Evden Eve Nakliyat altyapısıyla kilitli özel oda, 7/24 kamera güvenliği ve profesyonel nakliyat dahil depolama çözümleri.</p>
                    <p style="font-size:14px;line-height:1.7;"><strong style="color:#fff;">Anahtar Sizde Güvencesi</strong> ile eşyalarınıza sadece siz erişebilirsiniz.</p>
                    <div style="margin-top:20px;display:flex;gap:10px;flex-wrap:wrap;">
                        <a href="https://wa.me/905355298192" style="display:inline-flex;align-items:center;gap:6px;background:#25D366;color:#fff;padding:8px 16px;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600;">💬 WhatsApp</a>
                        <a href="tel:+905355298192" style="display:inline-flex;align-items:center;gap:6px;background:#1B2D4F;color:#fff;padding:8px 16px;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600;border:1px solid #334155;">📞 Ara</a>
                    </div>
                </div>

                <!-- Kolon 2: Hizmetler + Rehberler -->
                <div>
                    <h3 style="color:#fff;font-size:18px;margin-bottom:16px;font-weight:600;">Hizmetlerimiz</h3>
                    <ul style="list-style:none;padding:0;margin:0 0 20px;">
                        <li style="margin-bottom:8px;"><a href="/hizmetlerimiz/ev-esyasi-depolama/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Ev Eşyası Depolama</a></li>
                        <li style="margin-bottom:8px;"><a href="/hizmetlerimiz/ofis-depolama/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Ofis ve Kurumsal Depolama</a></li>
                        <li style="margin-bottom:8px;"><a href="/hizmetlerimiz/tadilat-depolama/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Tadilat Depolama</a></li>
                        <li style="margin-bottom:8px;"><a href="/hizmetlerimiz/kentsel-donusum-depolama/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Kentsel Dönüşüm Depolama</a></li>
                        <li style="margin-bottom:8px;"><a href="/hizmetlerimiz/yurt-disi-depolama/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Yurt Dışı Depolama</a></li>
                        <li style="margin-bottom:8px;"><a href="/hizmetlerimiz/nakliyat-depolama/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Nakliyat ve Depolama</a></li>
                    </ul>
                    <h3 style="color:#fff;font-size:18px;margin-bottom:16px;font-weight:600;">Rehberler</h3>
                    <ul style="list-style:none;padding:0;margin:0;">
                        <li style="margin-bottom:8px;"><a href="/nasil-calisir/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Nasıl Çalışır?</a></li>
                        <li style="margin-bottom:8px;"><a href="/fiyatlar/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Fiyatlar</a></li>
                        <li style="margin-bottom:8px;"><a href="/sikca-sorulan-sorular/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Sıkça Sorulan Sorular</a></li>
                        <li style="margin-bottom:8px;"><a href="/blog/" style="color:#cbd5e1;text-decoration:none;font-size:14px;">› Blog</a></li>
                    </ul>
                </div>

                <!-- Kolon 3: İletişim -->
                <div>
                    <h3 style="color:#fff;font-size:18px;margin-bottom:16px;font-weight:600;">İletişim</h3>
                    <div style="margin-bottom:14px;">
                        <p style="font-size:14px;margin:0;">📞 <a href="tel:+905355298192" style="color:#fff;text-decoration:none;font-weight:600;">0535 529 81 92</a></p>
                    </div>
                    <div style="margin-bottom:14px;">
                        <p style="font-size:14px;margin:0;">💬 <a href="https://wa.me/905355298192" style="color:#25D366;text-decoration:none;font-weight:600;">WhatsApp ile Yazın</a></p>
                    </div>
                    <div style="margin-bottom:14px;">
                        <p style="font-size:14px;margin:0;">📧 <a href="mailto:info@evidepo.com" style="color:#cbd5e1;text-decoration:none;">info@evidepo.com</a></p>
                    </div>
                    <div style="margin-bottom:14px;">
                        <p style="font-size:14px;margin:0;">📍 İstanbul, Türkiye</p>
                        <p style="color:#94a3b8;font-size:13px;margin:4px 0 0;">Avrupa ve Anadolu Yakası tüm ilçelere hizmet</p>
                    </div>
                    <div style="margin-top:20px;padding-top:16px;border-top:1px solid #1e3a5f;">
                        <p style="font-size:13px;margin:0;"><strong style="color:#fff;">Çalışma Saatleri</strong></p>
                        <p style="color:#94a3b8;font-size:13px;margin:4px 0;">Pzt - Cmt: 08:00 - 19:00</p>
                        <p style="color:#94a3b8;font-size:13px;margin:0;">Pazar: Randevuyla</p>
                    </div>
                </div>

                <!-- Kolon 4: Hizmet Bölgeleri -->
                <div>
                    <h3 style="color:#fff;font-size:18px;margin-bottom:16px;font-weight:600;">Hizmet Bölgelerimiz</h3>
                    <p style="color:#fff;font-size:13px;font-weight:600;margin-bottom:6px;">Anadolu Yakası</p>
                    <p style="color:#94a3b8;font-size:13px;line-height:2;margin-bottom:16px;">
                        <a href="/kadikoy-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Kadıköy</a> ·
                        <a href="/uskudar-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Üsküdar</a> ·
                        <a href="/atasehir-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Ataşehir</a> ·
                        <a href="/umraniye-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Ümraniye</a> ·
                        <a href="/kartal-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Kartal</a> ·
                        <a href="/pendik-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Pendik</a> ·
                        <a href="/maltepe-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Maltepe</a> ·
                        <a href="/tuzla-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Tuzla</a> ·
                        <a href="/sancaktepe-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Sancaktepe</a> ·
                        <a href="/sultanbeyli-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Sultanbeyli</a>
                    </p>
                    <p style="color:#fff;font-size:13px;font-weight:600;margin-bottom:6px;">Avrupa Yakası</p>
                    <p style="color:#94a3b8;font-size:13px;line-height:2;">
                        <a href="/besiktas-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Beşiktaş</a> ·
                        <a href="/sisli-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Şişli</a> ·
                        <a href="/sariyer-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Sarıyer</a> ·
                        <a href="/beylikduzu-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Beylikdüzü</a> ·
                        <a href="/esenyurt-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Esenyurt</a> ·
                        <a href="/bakirkoy-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Bakırköy</a> ·
                        <a href="/bahcelievler-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Bahçelievler</a> ·
                        <a href="/kucukcekmece-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Küçükçekmece</a> ·
                        <a href="/basaksehir-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Başakşehir</a> ·
                        <a href="/fatih-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Fatih</a> ·
                        <a href="/bagcilar-esya-depolama/" style="color:#cbd5e1;text-decoration:none;">Bağcılar</a>
                    </p>
                </div>

            </div>

            <!-- Alt Çizgi: Güven Sinyalleri -->
            <div style="margin-top:40px;padding-top:24px;border-top:1px solid #1e3a5f;display:flex;justify-content:center;gap:30px;flex-wrap:wrap;">
                <span style="color:#94a3b8;font-size:13px;">🔒 Kilitli Özel Oda</span>
                <span style="color:#94a3b8;font-size:13px;">📹 7/24 Kamera Güvenliği</span>
                <span style="color:#94a3b8;font-size:13px;">📋 Sözleşme Güvencesi</span>
                <span style="color:#94a3b8;font-size:13px;">🛡️ Sigorta Kapsamı</span>
                <span style="color:#94a3b8;font-size:13px;">🚛 Profesyonel Nakliyat</span>
            </div>
        </div>
    </div>

    <!-- LocalBusiness Schema Markup -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Evidepo",
        "description": "İstanbul'da güvenli eşya depolama hizmeti. Kilitli özel oda, 7/24 kamera, profesyonel nakliyat dahil.",
        "url": "https://evidepo.com",
        "telephone": "+905355298192",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "İstanbul",
            "addressCountry": "TR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "41.0082",
            "longitude": "28.9784"
        },
        "openingHours": ["Mo-Sa 08:00-19:00"],
        "priceRange": "₺₺",
        "image": "https://evidepo.com/wp-content/uploads/evidepo-logo.png",
        "sameAs": [],
        "areaServed": {
            "@type": "City",
            "name": "İstanbul"
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Depolama Hizmetleri",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Ev Eşyası Depolama"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Ofis ve Kurumsal Depolama"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Tadilat Depolama"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kentsel Dönüşüm Depolama"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Yurt Dışı Depolama"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Nakliyat ve Depolama"}}
            ]
        }
    }
    </script>

    <style>
        #evidepo-footer a:hover { color: #fff !important; }
        @media (max-width: 768px) {
            #evidepo-footer > div > div:first-child {
                grid-template-columns: 1fr !important;
                gap: 30px !important;
            }
        }
        @media (min-width: 769px) and (max-width: 1024px) {
            #evidepo-footer > div > div:first-child {
                grid-template-columns: repeat(2, 1fr) !important;
            }
        }
    </style>
    <?php
});
