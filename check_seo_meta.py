"""Check live SEO meta tags for all service pages"""
import re
import requests

PAGES = {
    'ev-esyasi-depolama': 'https://evidepo.com/hizmetlerimiz/ev-esyasi-depolama/',
    'ofis-depolama': 'https://evidepo.com/hizmetlerimiz/ofis-depolama/',
    'tadilat-depolama': 'https://evidepo.com/hizmetlerimiz/tadilat-depolama/',
    'kentsel-donusum-depolama': 'https://evidepo.com/hizmetlerimiz/kentsel-donusum-depolama/',
    'yurt-disi-depolama': 'https://evidepo.com/hizmetlerimiz/yurt-disi-depolama/',
    'nakliyat-ve-depolama': 'https://evidepo.com/hizmetlerimiz/nakliyat-ve-depolama/',
    'anasayfa': 'https://evidepo.com/',
    'fiyatlar': 'https://evidepo.com/fiyatlar/',
    'nasil-calisir': 'https://evidepo.com/nasil-calisir/',
    'hakkimizda': 'https://evidepo.com/hakkimizda/',
    'iletisim': 'https://evidepo.com/iletisim/',
    'hizmetlerimiz': 'https://evidepo.com/hizmetlerimiz/',
    'sss': 'https://evidepo.com/sikca-sorulan-sorular/',
    'blog': 'https://evidepo.com/blog/',
}

BLOG_POSTS = {
    'istanbul-rehber': 'https://evidepo.com/istanbul-esya-depolama-rehberi/',
    'fiyat-rehber': 'https://evidepo.com/esya-depolama-fiyatlari-2026/',
    'firma-secimi': 'https://evidepo.com/depolama-firmasi-secerken-dikkat/',
    'paketleme': 'https://evidepo.com/esya-paketleme-rehberi/',
    'yurt-disi-blog': 'https://evidepo.com/yurt-disina-cikarken-esya-depolama/',
    'tadilat-blog': 'https://evidepo.com/tadilat-sirasinda-esya-depolama/',
    'kentsel-blog': 'https://evidepo.com/kentsel-donusumde-esya-depolama/',
    'ofis-blog': 'https://evidepo.com/ofis-tasima-depolama-kurumsal-rehber/',
}

def check_page(name, url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"  STATUS: {resp.status_code}")
            return
        html = resp.text
    except Exception as e:
        print(f"  ERROR: {e}")
        return

    # Title tag
    tt = re.search(r'<title>([^<]+)</title>', html)
    title = tt.group(1).strip() if tt else 'YOK'

    # Meta description
    md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.I)
    if not md:
        md = re.search(r"<meta\s+name='description'\s+content='([^']*)'", html, re.I)
    meta_desc = md.group(1).strip() if md else 'YOK'

    # Canonical
    can = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html, re.I)
    canonical = can.group(1) if can else 'YOK'

    # OG Title
    ogt = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html, re.I)
    og_title = ogt.group(1) if ogt else 'YOK'

    # OG Description
    ogd = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', html, re.I)
    og_desc = ogd.group(1)[:60] if ogd else 'YOK'

    # H1 count
    h1s = re.findall(r'<h1[^>]*>.*?</h1>', html, re.DOTALL | re.I)

    # Schema markup
    has_schema = 'application/ld+json' in html

    issues = []
    if meta_desc == 'YOK':
        issues.append('META_DESC_YOK')
    elif len(meta_desc) < 50:
        issues.append(f'META_DESC_KISA({len(meta_desc)})')
    elif len(meta_desc) > 160:
        issues.append(f'META_DESC_UZUN({len(meta_desc)})')

    if canonical == 'YOK':
        issues.append('CANONICAL_YOK')
    elif canonical != url:
        issues.append(f'CANONICAL_FARKLI')

    if og_title == 'YOK':
        issues.append('OG_TITLE_YOK')
    if og_desc == 'YOK':
        issues.append('OG_DESC_YOK')

    if len(h1s) == 0:
        issues.append('H1_YOK')
    elif len(h1s) > 1:
        issues.append(f'CIFT_H1({len(h1s)})')

    if not has_schema:
        issues.append('SCHEMA_YOK')

    if len(title) > 65:
        issues.append(f'TITLE_UZUN({len(title)})')

    status = 'OK' if not issues else ', '.join(issues)

    print(f"  Title: {title[:70]}")
    print(f"  Meta Desc: {meta_desc[:80]}{'...' if len(meta_desc) > 80 else ''}")
    print(f"  Canonical: {canonical}")
    print(f"  H1 Count: {len(h1s)}")
    print(f"  Schema: {'VAR' if has_schema else 'YOK'}")
    print(f"  DURUM: {status}")

print("=" * 70)
print("EVIDEPO.COM DETAYLI SEO AUDIT")
print("=" * 70)

print("\n--- SAYFALAR ---")
for name, url in PAGES.items():
    print(f"\n[{name}] {url}")
    check_page(name, url)

print("\n--- BLOG YAZILARI ---")
for name, url in BLOG_POSTS.items():
    print(f"\n[{name}] {url}")
    check_page(name, url)
