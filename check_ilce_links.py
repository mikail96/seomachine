"""Check if ilçe pages are accessible from the site navigation"""
import re
import requests

# Check main pages for ilçe links
PAGES_TO_CHECK = {
    'Anasayfa': 'https://evidepo.com/',
    'Hizmetlerimiz': 'https://evidepo.com/hizmetlerimiz/',
    'Ev Eşyası Depolama': 'https://evidepo.com/hizmetlerimiz/ev-esyasi-depolama/',
    'Footer/Sitemap': 'https://evidepo.com/sitemap.xml',
}

ILCE_SLUGS = [
    'kadikoy', 'uskudar', 'atasehir', 'umraniye', 'kartal', 'pendik',
    'maltepe', 'tuzla', 'sancaktepe', 'sultanbeyli', 'besiktas', 'sisli',
    'sariyer', 'beylikduzu', 'esenyurt', 'bakirkoy', 'bahcelievler',
    'kucukcekmece', 'basaksehir', 'fatih', 'bagcilar'
]

print("=" * 60)
print("İLÇE SAYFALARI ERİŞİLEBİLİRLİK KONTROLÜ")
print("=" * 60)

# 1. Check if ilçe pages exist and respond
print("\n--- SAYFA DURUMU ---")
for slug in ILCE_SLUGS:
    url = f"https://evidepo.com/{slug}-esya-depolama/"
    try:
        resp = requests.head(url, timeout=10, allow_redirects=True)
        final_url = resp.url
        status = resp.status_code
        print(f"  {slug:20s} | {status} | {final_url}")
    except Exception as e:
        print(f"  {slug:20s} | ERROR | {e}")

# 2. Check if any page links to ilçe pages
print("\n--- LİNK KONTROLÜ ---")
for page_name, url in PAGES_TO_CHECK.items():
    if 'sitemap' in url:
        continue
    try:
        resp = requests.get(url, timeout=10)
        html = resp.text

        found = []
        for slug in ILCE_SLUGS:
            if f"{slug}-esya-depolama" in html:
                found.append(slug)

        print(f"\n{page_name} ({url}):")
        if found:
            print(f"  İlçe linkleri bulundu: {len(found)}")
            for s in found:
                print(f"    - {s}-esya-depolama")
        else:
            print("  İlçe linki YOK!")
    except Exception as e:
        print(f"  ERROR: {e}")

# 3. Check navigation menu
print("\n--- NAVİGASYON MENÜ KONTROLÜ ---")
try:
    resp = requests.get('https://evidepo.com/', timeout=10)
    html = resp.text

    # Find nav element
    nav_match = re.search(r'<nav[^>]*>(.*?)</nav>', html, re.DOTALL | re.I)
    if nav_match:
        nav_html = nav_match.group(1)
        ilce_in_nav = [s for s in ILCE_SLUGS if f"{s}-esya-depolama" in nav_html]
        print(f"  Navigasyon menüde ilçe linkleri: {len(ilce_in_nav)}")
        if ilce_in_nav:
            for s in ilce_in_nav:
                print(f"    - {s}")
        else:
            print("  Navigasyon menüde ilçe linki YOK!")
    else:
        print("  Nav element bulunamadı")

    # Check footer
    footer_match = re.search(r'<footer[^>]*>(.*?)</footer>', html, re.DOTALL | re.I)
    if footer_match:
        footer_html = footer_match.group(1)
        ilce_in_footer = [s for s in ILCE_SLUGS if f"{s}-esya-depolama" in footer_html]
        print(f"\n  Footer'da ilçe linkleri: {len(ilce_in_footer)}")
        if ilce_in_footer:
            for s in ilce_in_footer:
                print(f"    - {s}")
        else:
            print("  Footer'da ilçe linki YOK!")
    else:
        print("  Footer element bulunamadı")
except Exception as e:
    print(f"  ERROR: {e}")

# 4. Check XML sitemap
print("\n--- SITEMAP KONTROLÜ ---")
try:
    resp = requests.get('https://evidepo.com/sitemap_index.xml', timeout=10)
    if resp.status_code == 200:
        sitemaps = re.findall(r'<loc>(.*?)</loc>', resp.text)
        print(f"  Sitemap index bulundu: {len(sitemaps)} sitemap")
        for sm_url in sitemaps:
            if 'page' in sm_url or 'post' in sm_url:
                sm_resp = requests.get(sm_url, timeout=10)
                ilce_in_sm = [s for s in ILCE_SLUGS if f"{s}-esya-depolama" in sm_resp.text]
                print(f"\n  {sm_url}:")
                print(f"    İlçe URL sayısı: {len(ilce_in_sm)}")
    else:
        # Try other sitemap formats
        for sm_path in ['sitemap.xml', 'wp-sitemap.xml', 'sitemap_index.xml']:
            resp = requests.get(f'https://evidepo.com/{sm_path}', timeout=10)
            if resp.status_code == 200:
                ilce_in_sm = [s for s in ILCE_SLUGS if f"{s}-esya-depolama" in resp.text]
                print(f"  {sm_path}: {len(ilce_in_sm)} ilçe URL")
                break
        else:
            print("  Sitemap bulunamadı")
except Exception as e:
    print(f"  ERROR: {e}")
