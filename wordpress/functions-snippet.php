<?php
/**
 * SEO Machine - Rank Math REST API Support
 *
 * Add this code to your theme's functions.php file (or use a code snippets plugin).
 * This enables the SEO Machine tool to set Rank Math SEO meta fields via REST API.
 *
 * Fields exposed:
 * - focus_keyword (Focus Keyword)
 * - seo_title (SEO Title)
 * - meta_description (Meta Description)
 * - robots (Robots Meta)
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
                    return new WP_Error('rest_forbidden', 'Permission denied.', ['status' => 403]);
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
                    'focus_keyword' => ['type' => 'string', 'description' => 'Rank Math Focus Keyword'],
                    'seo_title' => ['type' => 'string', 'description' => 'Rank Math SEO Title'],
                    'meta_description' => ['type' => 'string', 'description' => 'Rank Math Meta Description'],
                    'robots' => ['type' => 'string', 'description' => 'Rank Math Robots Meta'],
                ],
            ],
        ]);
    }
});
