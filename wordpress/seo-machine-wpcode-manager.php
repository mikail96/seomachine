<?php
/**
 * Plugin Name: SEO Machine - WPCode Manager
 * Description: WPCode header/footer script'lerini REST API üzerinden okuma/yazma endpoint'i
 * Version: 1.0
 * Author: SEO Machine
 *
 * Kurulum: wp-content/mu-plugins/ klasörüne yükleyin
 * Kullanım sonrası silebilirsiniz.
 */

// ============================================================
// FIX: Duplike LocalBusiness schema bloklarını output buffer ile kaldır
// Block 1 (@graph) kalır, Block 2 ve Block 3 kaldırılır
// Birleştirilmiş schema WPCode header üzerinden enjekte edilir
// ============================================================
if (!is_admin()) {
    add_action('template_redirect', function () {
        ob_start(function ($html) {
            // 1. Rank Math'ın ürettiği duplike LocalBusiness/SelfStorage bloklarını kaldır
            $html = preg_replace(
                '/<script[^>]*type=["\']application\/ld\+json["\'][^>]*>\s*\{[^}]*"@type"\s*:\s*(\["SelfStorage"[^<]*|"LocalBusiness"[^<]*)<\/script>/s',
                '',
                $html
            );

            // 2. Birleştirilmiş tek schema'yı </head> öncesine enjekte et
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
