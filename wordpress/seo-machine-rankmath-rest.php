<?php
/**
 * Plugin Name: SEO Machine - Rank Math REST API Support
 * Description: Exposes Rank Math SEO meta fields via the WordPress REST API for the SEO Machine tool.
 * Version: 1.0
 * Author: SEO Machine
 *
 * Installation:
 * 1. Upload this file to: wp-content/mu-plugins/seo-machine-rankmath-rest.php
 * 2. That's it - mu-plugins are automatically activated
 *
 * If the mu-plugins folder doesn't exist, create it.
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Register Rank Math SEO meta fields for REST API access
 */
add_action('init', function() {
    // Only proceed if Rank Math is active
    if (!defined('RANK_MATH_VERSION')) {
        return;
    }

    $rankmath_meta_fields = [
        'rank_math_focus_keyword' => [
            'description' => 'Rank Math Focus Keyword',
            'single' => true,
        ],
        'rank_math_title' => [
            'description' => 'Rank Math SEO Title',
            'single' => true,
        ],
        'rank_math_description' => [
            'description' => 'Rank Math Meta Description',
            'single' => true,
        ],
        'rank_math_robots' => [
            'description' => 'Rank Math Robots Meta',
            'single' => true,
        ],
        'rank_math_seo_score' => [
            'description' => 'Rank Math SEO Score',
            'single' => true,
        ],
    ];

    $post_types = ['post', 'page'];
    foreach ($post_types as $post_type) {
        foreach ($rankmath_meta_fields as $meta_key => $args) {
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
 * Add Rank Math fields to REST response and handle updates
 * This provides a cleaner API interface
 */
add_action('rest_api_init', function() {
    // Only proceed if Rank Math is active
    if (!defined('RANK_MATH_VERSION')) {
        return;
    }

    $post_types = ['post', 'page'];
    foreach ($post_types as $post_type) {
        register_rest_field($post_type, 'rankmath_seo', [
            'get_callback' => function($post) {
                return [
                    'focus_keyword' => get_post_meta($post['id'], 'rank_math_focus_keyword', true),
                    'seo_title' => get_post_meta($post['id'], 'rank_math_title', true),
                    'meta_description' => get_post_meta($post['id'], 'rank_math_description', true),
                    'robots' => get_post_meta($post['id'], 'rank_math_robots', true),
                ];
            },
            'update_callback' => function($value, $post) {
                if (!current_user_can('edit_post', $post->ID)) {
                    return new WP_Error('rest_forbidden', 'You do not have permission to edit this post.', ['status' => 403]);
                }

                if (isset($value['focus_keyword'])) {
                    update_post_meta($post->ID, 'rank_math_focus_keyword', sanitize_text_field($value['focus_keyword']));
                }
                if (isset($value['seo_title'])) {
                    update_post_meta($post->ID, 'rank_math_title', sanitize_text_field($value['seo_title']));
                }
                if (isset($value['meta_description'])) {
                    update_post_meta($post->ID, 'rank_math_description', sanitize_text_field($value['meta_description']));
                }
                if (isset($value['robots'])) {
                    update_post_meta($post->ID, 'rank_math_robots', sanitize_text_field($value['robots']));
                }

                return true;
            },
            'schema' => [
                'type' => 'object',
                'properties' => [
                    'focus_keyword' => ['type' => 'string'],
                    'seo_title' => ['type' => 'string'],
                    'meta_description' => ['type' => 'string'],
                    'robots' => ['type' => 'string'],
                ],
            ],
        ]);
    }
});
