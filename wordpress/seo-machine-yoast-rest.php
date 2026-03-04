<?php
/**
 * Plugin Name: SEO Machine - Yoast REST API Support
 * Description: Exposes Yoast SEO meta fields via the WordPress REST API for the SEO Machine tool.
 * Version: 1.1
 * Author: SEO Machine
 *
 * Installation:
 * 1. Upload this file to: wp-content/mu-plugins/seo-machine-yoast-rest.php
 * 2. That's it - mu-plugins are automatically activated
 *
 * If the mu-plugins folder doesn't exist, create it.
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Register Yoast SEO meta fields for REST API access
 * Supports both posts and pages
 */
add_action('init', function() {
    // Only proceed if Yoast is active
    if (!defined('WPSEO_VERSION')) {
        return;
    }

    $yoast_meta_fields = [
        '_yoast_wpseo_focuskw' => [
            'description' => 'Yoast SEO Focus Keyphrase',
            'single' => true,
        ],
        '_yoast_wpseo_title' => [
            'description' => 'Yoast SEO Title',
            'single' => true,
        ],
        '_yoast_wpseo_metadesc' => [
            'description' => 'Yoast SEO Meta Description',
            'single' => true,
        ],
        '_yoast_wpseo_canonical' => [
            'description' => 'Yoast SEO Canonical URL',
            'single' => true,
        ],
        '_yoast_wpseo_opengraph-title' => [
            'description' => 'Yoast Open Graph Title',
            'single' => true,
        ],
        '_yoast_wpseo_opengraph-description' => [
            'description' => 'Yoast Open Graph Description',
            'single' => true,
        ],
        '_yoast_wpseo_opengraph-image' => [
            'description' => 'Yoast Open Graph Image URL',
            'single' => true,
        ],
        '_yoast_wpseo_linkdex' => [
            'description' => 'Yoast SEO Score',
            'single' => true,
        ],
        '_yoast_wpseo_content_score' => [
            'description' => 'Yoast Readability Score',
            'single' => true,
        ],
    ];

    // Register for both posts and pages
    $post_types = ['post', 'page'];

    foreach ($post_types as $post_type) {
        foreach ($yoast_meta_fields as $meta_key => $args) {
            register_post_meta($post_type, $meta_key, [
                'show_in_rest' => true,
                'single' => $args['single'],
                'type' => 'string',
                'description' => $args['description'],
                'auth_callback' => function() {
                    return current_user_can('edit_posts');
                },
            ]);
        }
    }
});

/**
 * Add Yoast fields to REST response and handle updates
 * Supports posts and pages
 */
add_action('rest_api_init', function() {
    // Only proceed if Yoast is active
    if (!defined('WPSEO_VERSION')) {
        return;
    }

    $post_types = ['post', 'page'];

    foreach ($post_types as $post_type) {
        register_rest_field($post_type, 'yoast_seo', [
            'get_callback' => function($post) {
                return [
                    'focus_keyphrase' => get_post_meta($post['id'], '_yoast_wpseo_focuskw', true),
                    'seo_title' => get_post_meta($post['id'], '_yoast_wpseo_title', true),
                    'meta_description' => get_post_meta($post['id'], '_yoast_wpseo_metadesc', true),
                    'canonical_url' => get_post_meta($post['id'], '_yoast_wpseo_canonical', true),
                    'og_title' => get_post_meta($post['id'], '_yoast_wpseo_opengraph-title', true),
                    'og_description' => get_post_meta($post['id'], '_yoast_wpseo_opengraph-description', true),
                    'og_image' => get_post_meta($post['id'], '_yoast_wpseo_opengraph-image', true),
                    'seo_score' => get_post_meta($post['id'], '_yoast_wpseo_linkdex', true),
                    'readability_score' => get_post_meta($post['id'], '_yoast_wpseo_content_score', true),
                ];
            },
            'update_callback' => function($value, $post) {
                if (!current_user_can('edit_post', $post->ID)) {
                    return new WP_Error('rest_forbidden', 'You do not have permission to edit this post.', ['status' => 403]);
                }

                $field_map = [
                    'focus_keyphrase' => '_yoast_wpseo_focuskw',
                    'seo_title' => '_yoast_wpseo_title',
                    'meta_description' => '_yoast_wpseo_metadesc',
                    'canonical_url' => '_yoast_wpseo_canonical',
                    'og_title' => '_yoast_wpseo_opengraph-title',
                    'og_description' => '_yoast_wpseo_opengraph-description',
                    'og_image' => '_yoast_wpseo_opengraph-image',
                ];

                foreach ($field_map as $api_key => $meta_key) {
                    if (isset($value[$api_key])) {
                        $sanitized = ($api_key === 'canonical_url' || $api_key === 'og_image')
                            ? esc_url_raw($value[$api_key])
                            : sanitize_text_field($value[$api_key]);
                        update_post_meta($post->ID, $meta_key, $sanitized);
                    }
                }

                return true;
            },
            'schema' => [
                'type' => 'object',
                'properties' => [
                    'focus_keyphrase' => ['type' => 'string'],
                    'seo_title' => ['type' => 'string'],
                    'meta_description' => ['type' => 'string'],
                    'canonical_url' => ['type' => 'string', 'format' => 'uri'],
                    'og_title' => ['type' => 'string'],
                    'og_description' => ['type' => 'string'],
                    'og_image' => ['type' => 'string', 'format' => 'uri'],
                    'seo_score' => ['type' => 'string'],
                    'readability_score' => ['type' => 'string'],
                ],
            ],
        ]);
    }
});
