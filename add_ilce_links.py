"""
Add ilçe (district) links to Hizmetlerimiz page and all service pages.
Also adds an ilçe navigation section to the anasayfa footer area.
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'data_sources' / 'modules'))

from dotenv import load_dotenv
for p in [Path(__file__).parent / 'data_sources' / 'config' / '.env', Path(__file__).parent / '.env']:
    if p.exists():
        load_dotenv(p)
        break

from wordpress_publisher import WordPressPublisher

# İlçe bilgileri
ILCELER_ANADOLU = [
    ('Kadıköy', '/kadikoy-esya-depolama/'),
    ('Üsküdar', '/uskudar-esya-depolama/'),
    ('Ataşehir', '/atasehir-esya-depolama/'),
    ('Ümraniye', '/umraniye-esya-depolama/'),
    ('Kartal', '/kartal-esya-depolama/'),
    ('Pendik', '/pendik-esya-depolama/'),
    ('Maltepe', '/maltepe-esya-depolama/'),
    ('Tuzla', '/tuzla-esya-depolama/'),
    ('Sancaktepe', '/sancaktepe-esya-depolama/'),
    ('Sultanbeyli', '/sultanbeyli-esya-depolama/'),
]

ILCELER_AVRUPA = [
    ('Beşiktaş', '/besiktas-esya-depolama/'),
    ('Şişli', '/sisli-esya-depolama/'),
    ('Sarıyer', '/sariyer-esya-depolama/'),
    ('Beylikdüzü', '/beylikduzu-esya-depolama/'),
    ('Esenyurt', '/esenyurt-esya-depolama/'),
    ('Bakırköy', '/bakirkoy-esya-depolama/'),
    ('Bahçelievler', '/bahcelievler-esya-depolama/'),
    ('Küçükçekmece', '/kucukcekmece-esya-depolama/'),
    ('Başakşehir', '/basaksehir-esya-depolama/'),
    ('Fatih', '/fatih-esya-depolama/'),
    ('Bağcılar', '/bagcilar-esya-depolama/'),
]


def generate_ilce_section():
    """Generate the ilçe links HTML section"""

    anadolu_links = ''
    for name, url in ILCELER_ANADOLU:
        anadolu_links += f'<a href="{url}" style="display:inline-block;padding:8px 16px;background:#fff;border-radius:8px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;font-size:14px;transition:all 0.2s">{name}</a>\n'

    avrupa_links = ''
    for name, url in ILCELER_AVRUPA:
        avrupa_links += f'<a href="{url}" style="display:inline-block;padding:8px 16px;background:#fff;border-radius:8px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;font-size:14px;transition:all 0.2s">{name}</a>\n'

    html = f'''
<div style="background:#f8fafc;padding:40px;border-radius:16px;margin:40px 0">
<h2 style="text-align:center;color:#1B2D4F;margin-bottom:10px">Hizmet Verdiğimiz İlçeler</h2>
<p style="text-align:center;color:#64748b;margin-bottom:30px">İstanbul'un Avrupa ve Anadolu yakasındaki tüm ilçelere eşya depolama ve nakliyat hizmeti sunuyoruz.</p>

<h3 style="color:#1B2D4F;margin-bottom:12px">&#x1f30a; Anadolu Yakası</h3>
<div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:25px">
{anadolu_links}</div>

<h3 style="color:#1B2D4F;margin-bottom:12px">&#x1f309; Avrupa Yakası</h3>
<div style="display:flex;flex-wrap:wrap;gap:10px">
{avrupa_links}</div>
</div>'''

    return html


def generate_compact_ilce_section():
    """Generate a compact ilçe links section for service pages"""
    all_links = ''
    for name, url in ILCELER_ANADOLU + ILCELER_AVRUPA:
        all_links += f'<a href="{url}" style="padding:6px 12px;background:#f8fafc;border-radius:6px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;font-size:13px">{name}</a>\n'

    html = f'''
<div style="background:#f0f9ff;padding:30px;border-radius:12px;margin:30px 0">
<h3 style="color:#1B2D4F;margin-bottom:15px">İstanbul Eşya Depolama Hizmet Bölgelerimiz</h3>
<div style="display:flex;flex-wrap:wrap;gap:8px">
{all_links}</div>
</div>'''

    return html


def main():
    wp = WordPressPublisher()

    print("İLÇE LİNKLERİ EKLEME")
    print("=" * 60)

    ilce_section = generate_ilce_section()
    compact_section = generate_compact_ilce_section()

    # 1. Update Hizmetlerimiz page (ID 8) - append ilçe section
    print("\n1. Hizmetlerimiz sayfasına ilçe bölümü ekleniyor...")
    try:
        resp = wp.session.get(f'{wp.api_base}/pages/8', params={'context': 'edit'})
        current_content = resp.json()['content']['raw']

        # Check if ilçe section already exists
        if 'Hizmet Verdiğimiz İlçeler' not in current_content:
            new_content = current_content + ilce_section
            resp = wp.session.post(f'{wp.api_base}/pages/8', json={'content': new_content})
            resp.raise_for_status()
            print("  [OK] Hizmetlerimiz sayfasına ilçe bölümü eklendi")
        else:
            print("  [SKIP] İlçe bölümü zaten var")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # 2. Update Anasayfa (ID 6) - append ilçe section
    print("\n2. Anasayfaya ilçe bölümü ekleniyor...")
    try:
        resp = wp.session.get(f'{wp.api_base}/pages/6', params={'context': 'edit'})
        current_content = resp.json()['content']['raw']

        if 'Hizmet Verdiğimiz İlçeler' not in current_content and 'Hizmet Bölgelerimiz' not in current_content:
            new_content = current_content + ilce_section
            resp = wp.session.post(f'{wp.api_base}/pages/6', json={'content': new_content})
            resp.raise_for_status()
            print("  [OK] Anasayfaya ilçe bölümü eklendi")
        else:
            print("  [SKIP] İlçe bölümü zaten var")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # 3. Update all service pages (IDs 9-14) - append compact ilçe section
    print("\n3. Hizmet sayfalarına kompakt ilçe bölümü ekleniyor...")
    service_pages = {
        9: 'Ev Eşyası Depolama',
        10: 'Ofis Depolama',
        11: 'Tadilat Depolama',
        12: 'Kentsel Dönüşüm Depolama',
        13: 'Yurt Dışı Depolama',
        14: 'Nakliyat ve Depolama',
    }

    for page_id, name in service_pages.items():
        try:
            resp = wp.session.get(f'{wp.api_base}/pages/{page_id}', params={'context': 'edit'})
            current_content = resp.json()['content']['raw']

            if 'Hizmet Bölgelerimiz' not in current_content:
                new_content = current_content + compact_section
                resp = wp.session.post(f'{wp.api_base}/pages/{page_id}', json={'content': new_content})
                resp.raise_for_status()
                print(f"  [OK] ID:{page_id} | {name}")
            else:
                print(f"  [SKIP] ID:{page_id} | {name} - zaten var")
        except Exception as e:
            print(f"  [FAIL] ID:{page_id} | {name} | {e}")

    # 4. Update Fiyatlar page (ID 15) - append compact ilçe section
    print("\n4. Fiyatlar sayfasına kompakt ilçe bölümü ekleniyor...")
    try:
        resp = wp.session.get(f'{wp.api_base}/pages/15', params={'context': 'edit'})
        current_content = resp.json()['content']['raw']

        if 'Hizmet Bölgelerimiz' not in current_content:
            new_content = current_content + compact_section
            resp = wp.session.post(f'{wp.api_base}/pages/15', json={'content': new_content})
            resp.raise_for_status()
            print("  [OK] Fiyatlar sayfasına ilçe bölümü eklendi")
        else:
            print("  [SKIP] Zaten var")
    except Exception as e:
        print(f"  [FAIL] {e}")

    print("\n" + "=" * 60)
    print("TAMAMLANDI!")
    print("=" * 60)


if __name__ == '__main__':
    main()
