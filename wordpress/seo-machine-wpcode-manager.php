<?php
/**
 * Plugin Name: SEO Machine - WPCode Manager
 * Description: WPCode header/footer script'lerini REST API üzerinden okuma/yazma endpoint'i
 * Version: 1.1
 * Author: SEO Machine
 *
 * Kurulum: wp-content/mu-plugins/ klasörüne yükleyin
 * Kullanım sonrası silebilirsiniz.
 */

// ============================================================
// Browser Cache Headers - statik kaynaklar için cache süreleri
// ============================================================
if (!is_admin()) {
    add_action('send_headers', function () {
        if (!is_user_logged_in()) {
            header('Cache-Control: public, max-age=3600, s-maxage=86400');
            header_remove('Pragma');
            header_remove('Expires');
        }
    });
}

// ============================================================
// FIX: Duplike LocalBusiness schema bloklarını output buffer ile kaldır
// Block 1 (@graph) kalır, Block 2 ve Block 3 kaldırılır
// Birleştirilmiş schema WPCode header üzerinden enjekte edilir
// + SSS sayfasına FAQPage schema, Nasıl Çalışır'a HowTo schema
// ============================================================
if (!is_admin()) {
    add_action('template_redirect', function () {
        ob_start(function ($html) {
            // 0. CSS düzeltmeleri: hero h2, "En Popüler" badge, footer kontrast
            $css_fixes = '<style id="ev-css-fixes">
/* FIX: Hero bölümünde h2 kullanılıyor ama CSS h1 hedefliyor */
.ev-hero h2{font-family:"Plus Jakarta Sans",sans-serif;font-size:48px;font-weight:800;line-height:1.12;color:#fff;margin-bottom:24px;letter-spacing:-1px}
.ev-hero h2 em{font-style:normal;color:#E8614D}
@media(max-width:1024px){.ev-hero h2{font-size:38px}}
@media(max-width:768px){.ev-hero h2{font-size:30px}}
@media(max-width:480px){.ev-hero h2{font-size:26px}}

/* FIX: "En Popüler" badge taşma sorunu */
.ev-pricing-grid{overflow:visible}
.ev-price-card.popular{overflow:visible;margin-top:16px}

/* FIX: Footer - koyu arka plan üzerinde koyu metin görünmüyor */
.site-footer{background:#0F1A2E !important}
.site-footer,.site-footer p,.site-footer .copyright-bar{color:rgba(255,255,255,0.7) !important}
.site-footer a{color:rgba(255,255,255,0.85) !important}
.site-footer a:hover{color:#E8614D !important}
.site-footer h2,.site-footer h3,.site-footer h4,.site-footer .footer-widget-title{color:#fff !important}
.site-footer .site-info{color:rgba(255,255,255,0.5) !important}
.site-footer .site-info a{color:rgba(255,255,255,0.65) !important}
</style>';
            $html = str_replace('</head>', $css_fixes . "\n</head>", $html);

            // 1. Rank Math'ın ürettiği duplike LocalBusiness/SelfStorage bloklarını kaldır
            $html = preg_replace(
                '/<script[^>]*type=["\']application\/ld\+json["\'][^>]*>\s*\{[^}]*"@type"\s*:\s*(\["SelfStorage"[^<]*|"LocalBusiness"[^<]*)<\/script>/s',
                '',
                $html
            );

            // 2. Birleştirilmiş LocalBusiness schema'yı </head> öncesine enjekte et
            $schema = '<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["SelfStorage", "LocalBusiness"],
  "@id": "https://evidepo.com/#localbusiness",
  "name": "Evidepo",
  "description": "İstanbul\'da güvenli, kameralı ve kilitli oda kiralama sistemiyle eşya depolama hizmeti. Randevulu erişim, anahtar müşteride. Sanat Evden Eve Nakliyat iştiraki.",
  "url": "https://evidepo.com",
  "telephone": "+905355298192",
  "email": "mikailaymaz1@gmail.com",
  "image": "https://evidepo.com/wp-content/uploads/2026/03/evidepo-logo-112.png",
  "logo": "https://evidepo.com/wp-content/uploads/2026/03/evidepo-logo-112.png",
  "priceRange": "₺₺",
  "currenciesAccepted": "TRY",
  "paymentAccepted": "Nakit, Kredi Kartı, Havale",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Güllübağlar Mahallesi, Sümer Sokak",
    "addressLocality": "Pendik",
    "addressRegion": "İstanbul",
    "postalCode": "34906",
    "addressCountry": "TR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "40.8783",
    "longitude": "29.2333"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "areaServed": {"@type": "City", "name": "İstanbul"},
  "parentOrganization": {"@type": "Organization", "name": "Sanat Evden Eve Nakliyat"},
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
  },
  "sameAs": []
}
</script>';
            $html = str_replace('</head>', $schema . "\n</head>", $html);

            // 3. SSS sayfasına FAQPage schema ekle (zengin snippet için)
            if (strpos($_SERVER['REQUEST_URI'], '/sikca-sorulan-sorular') !== false) {
                $faq_schema = '<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Eşyalarıma nasıl ulaşabilirim?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Randevu alarak eşyalarınıza ulaşabilirsiniz. Randevu saatlerimiz hafta içi ve hafta sonu esnek şekilde ayarlanabilir. Alanınızın anahtarı sadece sizde olduğu için eşyalarınıza güvenle erişirsiniz."
      }
    },
    {
      "@type": "Question",
      "name": "Depolama alanları ne kadar güvenli?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Tüm depolama alanlarımız 7/24 kamera güvenlik sistemi ile izlenmektedir. Her alan ayrı kilitlidir ve anahtarı sadece müşterimizde bulunur. Biz dahil kimse izniniz olmadan alanınıza erişemez."
      }
    },
    {
      "@type": "Question",
      "name": "Eşyalarım sigortalı mı?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet, tüm depolanan eşyalar sözleşme kapsamında sigorta güvencesi altındadır."
      }
    },
    {
      "@type": "Question",
      "name": "Minimum depolama süresi ne kadar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Minimum depolama süremiz 1 aydır. Aylık olarak kiralama yapabilir, istediğiniz süre boyunca depolama hizmetinden yararlanabilirsiniz."
      }
    },
    {
      "@type": "Question",
      "name": "Nakliyat hizmeti de veriyor musunuz?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet! Sanat Evden Eve Nakliyat iştiraki olarak evden eve taşıma ve depolama hizmetini tek elden sunuyoruz. İstanbul genelinde nakliyat hizmeti veriyoruz."
      }
    },
    {
      "@type": "Question",
      "name": "Fiyatlar neye göre belirleniyor?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Fiyatlar alan büyüklüğüne ve depolama süresine göre belirlenir. Ücretsiz ekspertiz ile en uygun fiyatı belirleriz. Gizli ücret yoktur."
      }
    },
    {
      "@type": "Question",
      "name": "Hangi eşyaları depolayabilirim?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ev eşyaları, ofis mobilyaları, beyaz eşya, elektronik aletler, kişisel eşyalar, mevsimlik ürünler, arşiv dosyaları ve daha birçok eşyanızı güvenle depolayabilirsiniz. Yanıcı, patlayıcı ve yasal olmayan maddeler kabul edilmez."
      }
    },
    {
      "@type": "Question",
      "name": "Depolama alanları temiz mi?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet, tüm alanlarımız düzenli olarak temizlenir ve bakımı yapılır. Eşyalarınız hijyenik bir ortamda muhafaza edilir."
      }
    },
    {
      "@type": "Question",
      "name": "Sözleşme yapılıyor mu?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet, tüm depolama hizmetlerimiz resmi sözleşme ile güvence altına alınır."
      }
    },
    {
      "@type": "Question",
      "name": "İstanbul\'da eşya depolama fiyatları ne kadar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Eşya depolama fiyatları oda boyutuna ve kiralama süresine göre değişir. Evidepo\'da 5m², 10m² ve 20m² oda seçenekleri mevcuttur. Ücretsiz ekspertiz hizmetimizle eşyalarınıza en uygun oda boyutunu ve fiyatı birlikte belirleriz. Gizli ücret uygulamıyoruz."
      }
    },
    {
      "@type": "Question",
      "name": "Pendik dışındaki ilçelerden de hizmet alabilir miyim?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet. Depomuz Pendik\'te bulunmakla birlikte, Sanat Evden Eve Nakliyat ekibimiz İstanbul\'un Anadolu ve Avrupa yakasındaki tüm ilçelerden eşya alıp depoya taşır. Kadıköy, Ataşehir, Beşiktaş, Bakırköy dahil tüm ilçelere hizmet veriyoruz."
      }
    },
    {
      "@type": "Question",
      "name": "Depolama alanları nemli veya rutubetli mi?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Hayır. Depolama odalarımız kuru, temiz ve bakımlı alanlardır. Düzenli temizlik ve havalandırma yapılır. Eşyalarınız nem, toz ve haşereden korunarak saklanır."
      }
    },
    {
      "@type": "Question",
      "name": "Kentsel dönüşüm için uzun süreli depolama yapıyor musunuz?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet. Kentsel dönüşüm süreçleri için özel uzun süreli depolama paketlerimiz mevcuttur. Uzun süreli kiralamada avantajlı fiyatlar sunuyoruz."
      }
    },
    {
      "@type": "Question",
      "name": "Evidepo ile diğer depolama firmaları arasındaki fark nedir?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evidepo\'da her müşteriye kişiye özel kilitli oda tahsis edilir ve anahtar yalnızca müşteride kalır. Firma dahil kimse odanıza erişemez. Ayrıca Sanat Evden Eve Nakliyat iştiraki olarak nakliyat ve depolama tek elden sunulur."
      }
    },
    {
      "@type": "Question",
      "name": "Taşınma sırasında eşyalarım zarar görür mü?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sanat Evden Eve Nakliyat\'ın profesyonel ekibi eşyalarınızı özenle paketler ve taşır. Eşyalarınız sözleşme kapsamında güvence altındadır."
      }
    },
    {
      "@type": "Question",
      "name": "Depo alanını görebilir miyim?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Evet. Randevu alarak depomuzu ziyaret edebilir, odaları yerinde görebilirsiniz. Ücretsiz ekspertiz hizmetimiz kapsamında ekibimiz size depolama alanlarını tanıtır."
      }
    }
  ]
}
</script>';
                $html = str_replace('</head>', $faq_schema . "\n</head>", $html);
            }

            // 4. Nasıl Çalışır sayfasına HowTo schema ekle
            if (strpos($_SERVER['REQUEST_URI'], '/nasil-calisir') !== false) {
                $howto_schema = '<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Eşya Depolama Nasıl Çalışır?",
  "description": "Evidepo ile eşyalarınızı depolamak sadece 4 adımda tamamlanır.",
  "totalTime": "PT2H",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Bize Ulaşın",
      "text": "Telefon, WhatsApp veya web sitemiz üzerinden bize ulaşın. Depolama ve nakliyat ihtiyacınız hakkında bilgi verin. Ekibimiz size uygun çözüm önerileri sunacak ve sorularınızı yanıtlayacaktır."
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Ücretsiz Ekspertiz",
      "text": "Uzman ekibimiz eşyalarınızı yerinde değerlendirir. Eşya miktarınıza göre en uygun alan boyutunu belirler ve net fiyat teklifini sunar. Ekspertiz hizmetimiz tamamen ücretsizdir."
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "Paketleme ve Taşıma",
      "text": "Anlaşma sağlandıktan sonra Sanat Evden Eve Nakliyat ekibimiz devreye girer. Eşyalarınız profesyonel ekip tarafından özenle paketlenir ve depolama tesisimize güvenle taşınır."
    },
    {
      "@type": "HowToStep",
      "position": 4,
      "name": "Anahtar Teslim",
      "text": "Eşyalarınız kişiye özel kilitli alanınıza yerleştirilir. Alanınızın anahtarı size teslim edilir. Artık anahtarınız sizde, eşyalarınız güvende. Randevu alarak istediğiniz zaman eşyalarınıza ulaşabilirsiniz."
    }
  ]
}
</script>';
                $html = str_replace('</head>', $howto_schema . "\n</head>", $html);
            }

            return $html;
        });
    });
}

// ============================================================
// REST API: Option okuma/yazma endpoint'leri
// ============================================================
add_action('rest_api_init', function () {

    // GET: Belirli bir WP option'ı oku (serialized dahil)
    register_rest_route('seo-machine/v1', '/option/(?P<name>[a-zA-Z0-9_-]+)', array(
        'methods'  => 'GET',
        'callback' => function ($request) {
            $name = $request->get_param('name');
            $value = get_option($name, null);
            return array('name' => $name, 'value' => $value);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // POST: Belirli bir WP option'ı güncelle
    register_rest_route('seo-machine/v1', '/option/(?P<name>[a-zA-Z0-9_-]+)', array(
        'methods'  => 'POST',
        'callback' => function ($request) {
            $name = $request->get_param('name');
            $params = $request->get_json_params();
            $value = $params['value'] ?? null;
            if ($value === null) return new WP_Error('missing_param', 'value required');
            update_option($name, $value);
            return array('success' => true, 'name' => $name);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // GET: Belirli bir post'un meta verilerini oku
    register_rest_route('seo-machine/v1', '/post-meta/(?P<id>\d+)', array(
        'methods'  => 'GET',
        'callback' => function ($request) {
            global $wpdb;
            $id = (int) $request->get_param('id');
            $filter = $request->get_param('filter');
            $sql = $wpdb->prepare("SELECT meta_key, meta_value FROM {$wpdb->postmeta} WHERE post_id = %d", $id);
            if ($filter) {
                $sql .= $wpdb->prepare(" AND meta_key LIKE %s", '%' . $wpdb->esc_like($filter) . '%');
            }
            $sql .= " LIMIT 100";
            $rows = $wpdb->get_results($sql);
            $result = array();
            foreach ($rows as $r) {
                $result[] = array('key' => $r->meta_key, 'value' => maybe_unserialize($r->meta_value));
            }
            return $result;
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // POST: Belirli bir post'un meta verisini güncelle
    register_rest_route('seo-machine/v1', '/post-meta/(?P<id>\d+)', array(
        'methods'  => 'POST',
        'callback' => function ($request) {
            $id = (int) $request->get_param('id');
            $params = $request->get_json_params();
            $key = $params['key'] ?? '';
            $value = $params['value'] ?? '';
            if (!$key) return new WP_Error('missing_param', 'key required');
            update_post_meta($id, $key, $value);
            return array('success' => true, 'post_id' => $id, 'key' => $key);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // DELETE: Belirli bir post'un meta verisini sil
    register_rest_route('seo-machine/v1', '/post-meta/(?P<id>\d+)', array(
        'methods'  => 'DELETE',
        'callback' => function ($request) {
            $id = (int) $request->get_param('id');
            $params = $request->get_json_params();
            $key = $params['key'] ?? '';
            if (!$key) return new WP_Error('missing_param', 'key required');
            delete_post_meta($id, $key);
            return array('success' => true, 'deleted_meta' => $key, 'post_id' => $id);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));
});

add_action('rest_api_init', function () {

    // GET: Mevcut header/footer/body script'lerini oku
    register_rest_route('seo-machine/v1', '/wpcode', array(
        'methods'  => 'GET',
        'callback' => function () {
            return array(
                'header' => get_option('ihaf_insert_header', ''),
                'body'   => get_option('ihaf_insert_body', ''),
                'footer' => get_option('ihaf_insert_footer', ''),
            );
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // POST: Header/footer/body script'lerini güncelle
    register_rest_route('seo-machine/v1', '/wpcode', array(
        'methods'  => 'POST',
        'callback' => function ($request) {
            $params  = $request->get_json_params();
            $updated = array();

            foreach (array('header', 'body', 'footer') as $key) {
                if (isset($params[$key])) {
                    $option_name = 'ihaf_insert_' . $key;
                    update_option($option_name, wp_unslash($params[$key]));
                    $updated[] = $key;
                }
            }

            return array(
                'success' => true,
                'updated' => $updated,
            );
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // GET: ld+json içeren tüm kaynakları tara
    register_rest_route('seo-machine/v1', '/find-schema', array(
        'methods'  => 'GET',
        'callback' => function () {
            global $wpdb;
            $results = array();

            // 1. wp_options tablosunda ld+json ara
            $options = $wpdb->get_results(
                "SELECT option_name, option_value FROM {$wpdb->options} WHERE option_value LIKE '%ld+json%' LIMIT 50"
            );
            foreach ($options as $opt) {
                $results[] = array(
                    'source' => 'wp_options',
                    'key'    => $opt->option_name,
                    'value'  => substr($opt->option_value, 0, 2000),
                );
            }

            // 2. wp_postmeta tablosunda ld+json ara
            $metas = $wpdb->get_results(
                "SELECT post_id, meta_key, meta_value FROM {$wpdb->postmeta} WHERE meta_value LIKE '%ld+json%' LIMIT 50"
            );
            foreach ($metas as $m) {
                $results[] = array(
                    'source'  => 'wp_postmeta',
                    'post_id' => $m->post_id,
                    'key'     => $m->meta_key,
                    'value'   => substr($m->meta_value, 0, 2000),
                );
            }

            // 3. wp_posts tablosunda ld+json ara (content)
            $posts = $wpdb->get_results(
                "SELECT ID, post_title, post_type, post_status FROM {$wpdb->posts} WHERE post_content LIKE '%ld+json%' LIMIT 50"
            );
            foreach ($posts as $p) {
                $results[] = array(
                    'source'  => 'wp_posts',
                    'post_id' => $p->ID,
                    'title'   => $p->post_title,
                    'type'    => $p->post_type,
                    'status'  => $p->post_status,
                );
            }

            // 4. Tema customizer (theme_mods)
            $theme_mods = get_theme_mods();
            foreach ($theme_mods as $key => $val) {
                if (is_string($val) && strpos($val, 'ld+json') !== false) {
                    $results[] = array(
                        'source' => 'theme_mods',
                        'key'    => $key,
                        'value'  => substr($val, 0, 2000),
                    );
                }
            }

            // 5. Widget'larda ara
            $sidebars = get_option('sidebars_widgets', array());
            foreach ($sidebars as $sidebar => $widgets) {
                if (!is_array($widgets)) continue;
                foreach ($widgets as $widget_id) {
                    $base = preg_replace('/-\d+$/', '', $widget_id);
                    $num  = preg_replace('/^.+-/', '', $widget_id);
                    $instances = get_option("widget_{$base}", array());
                    if (isset($instances[$num])) {
                        $content = json_encode($instances[$num]);
                        if (strpos($content, 'ld+json') !== false) {
                            $results[] = array(
                                'source'    => 'widget',
                                'sidebar'   => $sidebar,
                                'widget_id' => $widget_id,
                                'content'   => substr($content, 0, 2000),
                            );
                        }
                    }
                }
            }

            return $results;
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // GET: Veritabanında herhangi bir metni ara
    register_rest_route('seo-machine/v1', '/db-search', array(
        'methods'  => 'GET',
        'callback' => function ($request) {
            global $wpdb;
            $q = $request->get_param('q');
            if (!$q) return new WP_Error('missing_param', 'q parameter required');
            $like = '%' . $wpdb->esc_like($q) . '%';
            $results = array();

            $opts = $wpdb->get_results($wpdb->prepare(
                "SELECT option_name, LEFT(option_value,500) as val FROM {$wpdb->options} WHERE option_value LIKE %s LIMIT 20", $like
            ));
            foreach ($opts as $o) $results[] = array('src'=>'option','key'=>$o->option_name,'val'=>$o->val);

            $posts = $wpdb->get_results($wpdb->prepare(
                "SELECT ID,post_title,post_type,post_status FROM {$wpdb->posts} WHERE post_content LIKE %s LIMIT 20", $like
            ));
            foreach ($posts as $p) $results[] = array('src'=>'post','id'=>$p->ID,'title'=>$p->post_title,'type'=>$p->post_type,'status'=>$p->post_status);

            $metas = $wpdb->get_results($wpdb->prepare(
                "SELECT post_id,meta_key,LEFT(meta_value,500) as val FROM {$wpdb->postmeta} WHERE meta_value LIKE %s LIMIT 20", $like
            ));
            foreach ($metas as $m) $results[] = array('src'=>'postmeta','post_id'=>$m->post_id,'key'=>$m->meta_key,'val'=>$m->val);

            return $results;
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // GET: Belirli bir post'un tüm meta verilerini oku
    register_rest_route('seo-machine/v1', '/post-meta/(?P<id>\d+)', array(
        'methods'  => 'GET',
        'callback' => function ($request) {
            global $wpdb;
            $id = (int) $request->get_param('id');
            $filter = $request->get_param('filter');
            $sql = $wpdb->prepare("SELECT meta_key, meta_value FROM {$wpdb->postmeta} WHERE post_id = %d", $id);
            if ($filter) {
                $sql .= $wpdb->prepare(" AND meta_key LIKE %s", '%' . $wpdb->esc_like($filter) . '%');
            }
            $sql .= " LIMIT 100";
            $rows = $wpdb->get_results($sql);
            $result = array();
            foreach ($rows as $r) {
                $result[] = array('key' => $r->meta_key, 'value' => substr($r->meta_value, 0, 2000));
            }
            return $result;
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // POST: Belirli bir post'un meta verisini güncelle
    register_rest_route('seo-machine/v1', '/post-meta/(?P<id>\d+)', array(
        'methods'  => 'POST',
        'callback' => function ($request) {
            $id = (int) $request->get_param('id');
            $params = $request->get_json_params();
            $key = $params['key'] ?? '';
            $value = $params['value'] ?? '';
            if (!$key) return new WP_Error('missing_param', 'key required');
            update_post_meta($id, $key, $value);
            return array('success' => true, 'post_id' => $id, 'key' => $key);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // DELETE: Belirli bir post'un meta verisini sil
    register_rest_route('seo-machine/v1', '/post-meta/(?P<id>\d+)', array(
        'methods'  => 'DELETE',
        'callback' => function ($request) {
            $id = (int) $request->get_param('id');
            $params = $request->get_json_params();
            $key = $params['key'] ?? '';
            if (!$key) return new WP_Error('missing_param', 'key required');
            delete_post_meta($id, $key);
            return array('success' => true, 'deleted_meta' => $key, 'post_id' => $id);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // GET: Belirli bir WP option'ı oku
    register_rest_route('seo-machine/v1', '/option/(?P<name>[a-zA-Z0-9_-]+)', array(
        'methods'  => 'GET',
        'callback' => function ($request) {
            $name = $request->get_param('name');
            $value = get_option($name, null);
            return array('name' => $name, 'value' => $value);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // POST: Belirli bir WPCode snippet'ini sil veya deaktive et
    register_rest_route('seo-machine/v1', '/delete-snippet/(?P<id>\d+)', array(
        'methods'  => 'DELETE',
        'callback' => function ($request) {
            $id = (int) $request->get_param('id');
            $post = get_post($id);
            if (!$post) return new WP_Error('not_found', 'Post not found');
            wp_delete_post($id, true);
            return array('success' => true, 'deleted' => $id);
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));

    // GET: WPCode snippet'lerini listele (eğer varsa)
    register_rest_route('seo-machine/v1', '/wpcode-snippets', array(
        'methods'  => 'GET',
        'callback' => function () {
            $snippets = get_posts(array(
                'post_type'   => 'wpcode',
                'post_status' => 'any',
                'numberposts' => 50,
            ));

            $result = array();
            foreach ($snippets as $s) {
                $result[] = array(
                    'id'      => $s->ID,
                    'title'   => $s->post_title,
                    'status'  => $s->post_status,
                    'content' => $s->post_content,
                    'has_schema' => (strpos($s->post_content, 'ld+json') !== false),
                );
            }
            return $result;
        },
        'permission_callback' => function () {
            return current_user_can('manage_options');
        },
    ));
});
