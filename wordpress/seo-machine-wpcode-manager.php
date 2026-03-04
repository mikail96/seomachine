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
