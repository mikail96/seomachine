<?php
/**
 * Plugin Name: Evidepo Blog H1 Fix
 * Description: Adds H1 heading to blog archive page for SEO.
 * Version: 1.0
 * Author: SEO Machine
 *
 * Installation:
 * 1. Upload this file to: wp-content/mu-plugins/evidepo-blog-h1.php
 * 2. That's it - mu-plugins are automatically activated
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Add H1 to blog archive page before the post list
 */
add_action('generate_before_main_content', function() {
    if (is_home() && !is_paged()) {
        echo '<h1 class="page-title" style="margin-bottom: 20px;">Eşya Depolama Blog: Rehberler ve İpuçları</h1>';
        echo '<p style="margin-bottom: 30px; color: #64748b; font-size: 16px;">İstanbul eşya depolama, nakliyat, paketleme ve depolama ipuçları hakkında kapsamlı rehberler. Evidepo uzmanlarından pratik bilgiler ve güncel içerikler.</p>';
    }
});

/**
 * Fallback: If GeneratePress hook doesn't work, use wp_head to inject via JavaScript
 * This ensures H1 appears regardless of theme structure
 */
add_action('wp_footer', function() {
    if (is_home() && !is_paged()) {
        ?>
        <script>
        (function() {
            // Check if H1 already exists
            if (document.querySelector('h1')) return;

            // Find the main content area and prepend H1
            var main = document.querySelector('main, .site-main, #main, .content-area');
            if (main) {
                var h1 = document.createElement('h1');
                h1.className = 'page-title';
                h1.style.marginBottom = '20px';
                h1.textContent = 'Eşya Depolama Blog: Rehberler ve İpuçları';

                var p = document.createElement('p');
                p.style.marginBottom = '30px';
                p.style.color = '#64748b';
                p.style.fontSize = '16px';
                p.textContent = 'İstanbul eşya depolama, nakliyat, paketleme ve depolama ipuçları hakkında kapsamlı rehberler. Evidepo uzmanlarından pratik bilgiler ve güncel içerikler.';

                main.insertBefore(p, main.firstChild);
                main.insertBefore(h1, main.firstChild);
            }
        })();
        </script>
        <?php
    }
});
