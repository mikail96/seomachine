"""
Enrich all district (ilçe) pages with unique, SEO-optimized content.
Each page gets 500-700 words of unique content specific to that district.
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

# District data with unique characteristics
ILCE_DATA = {
    19: {
        'name': 'Kadıköy',
        'slug': 'kadikoy',
        'yaka': 'Anadolu',
        'ozellik': 'İstanbul\'un en köklü ve kültürel açıdan zengin ilçelerinden biri olan Kadıköy, yoğun nüfusu ve hareketli gayrimenkul piyasasıyla öne çıkar.',
        'kentsel_donusum': 'Kadıköy\'de özellikle Fikirtepe ve çevresi yoğun kentsel dönüşüm projelerine ev sahipliği yapmaktadır. Caferağa, Osmanağa ve Rasimpaşa mahallelerinde de bina yenileme çalışmaları devam etmektedir.',
        'tasınma': 'Kadıköy, İstanbul\'un en çok tercih edilen yaşam alanlarından biridir. Yüksek kira fiyatları nedeniyle sık ev değiştirme ve küçülme eğilimi yaygındır.',
        'ozel_hizmet': 'Kadıköy\'ün dar sokakları ve tarihi binaları nedeniyle özel taşıma ekipmanları kullanıyoruz. Moda, Bahariye ve Feneryolu bölgelerinde asansörlü taşıma hizmeti sunuyoruz.',
        'mahalleler': 'Moda, Bahariye, Feneryolu, Fikirtepe, Caferağa, Osmanağa, Göztepe, Erenköy, Suadiye, Bostancı',
    },
    20: {
        'name': 'Üsküdar',
        'slug': 'uskudar',
        'yaka': 'Anadolu',
        'ozellik': 'İstanbul Boğazı\'na kıyısı olan Üsküdar, tarihi dokusu ve yoğun konut alanlarıyla bilinen önemli bir Anadolu Yakası ilçesidir.',
        'kentsel_donusum': 'Üsküdar\'da özellikle iç mahallelerde ve Ünalan, Bulgurlu gibi bölgelerde kentsel dönüşüm projeleri hız kazanmıştır.',
        'tasınma': 'Marmaray ve metro bağlantısının güçlenmesiyle Üsküdar\'a taşınma ve Üsküdar\'dan çevre ilçelere geçiş yoğundur.',
        'ozel_hizmet': 'Üsküdar\'ın tarihi semtlerinde dar sokak ve çıkmaz sokak yoğunluğu nedeniyle küçük araçlarla taşıma hizmeti veriyoruz.',
        'mahalleler': 'Çengelköy, Kuzguncuk, Beylerbeyi, Ünalan, Acıbadem, Altunizade, Bulgurlu, Küçükçamlıca',
    },
    21: {
        'name': 'Ataşehir',
        'slug': 'atasehir',
        'yaka': 'Anadolu',
        'ozellik': 'İstanbul\'un yeni iş ve finans merkezi olan Ataşehir, modern konut projeleri ve yüksek nüfus yoğunluğuyla dikkat çeker.',
        'kentsel_donusum': 'Ataşehir\'de özellikle Barbaros, Yeni Çamlıca ve eski yapılaşma bölgelerinde kapsamlı kentsel dönüşüm projeleri yürütülmektedir.',
        'tasınma': 'İstanbul Finans Merkezi\'nin Ataşehir\'de konumlanmasıyla bölgeye kurumsal taşınma talebi artmıştır. Ofis ve ev depolama ihtiyacı yüksektir.',
        'ozel_hizmet': 'Ataşehir\'deki yüksek katlı rezidanslar için asansörlü taşıma ve özel paketleme hizmeti sunuyoruz. Kurumsal müşterilerimize faturalı hizmet veriyoruz.',
        'mahalleler': 'Barbaros, Atatürk, İçerenköy, Yeni Çamlıca, Küçükbakkalköy, Ferhatpaşa, Kayışdağı, Esatpaşa',
    },
    22: {
        'name': 'Ümraniye',
        'slug': 'umraniye',
        'yaka': 'Anadolu',
        'ozellik': 'İstanbul\'un en kalabalık ilçelerinden biri olan Ümraniye, hızlı kentleşme ve yoğun konut yapılaşmasıyla öne çıkar.',
        'kentsel_donusum': 'Ümraniye\'nin birçok mahallesinde kentsel dönüşüm projeleri aktif olarak devam etmektedir. Özellikle eski gecekondu bölgelerinde dönüşüm hız kazanmıştır.',
        'tasınma': 'Ümraniye\'nin hızlı büyümesi ve yeni konut projelerinin artması nedeniyle taşınma ve depolama talebi sürekli yükselmektedir.',
        'ozel_hizmet': 'Ümraniye\'nin geniş coğrafi alanı nedeniyle tüm mahallelere hızlı erişim sağlıyoruz. Toplu konut sitelerinde ekip koordinasyonuyla verimli taşıma yapıyoruz.',
        'mahalleler': 'Çakmak, Hekimbaşı, Istiklal, Esenevler, Altınşehir, Ihlamurkuyu, Namık Kemal, Elmalıkent',
    },
    23: {
        'name': 'Kartal',
        'slug': 'kartal',
        'yaka': 'Anadolu',
        'ozellik': 'Anadolu Yakası\'nın önemli merkezlerinden Kartal, sahil şeridi boyunca modern dönüşüm yaşayan dinamik bir ilçedir.',
        'kentsel_donusum': 'Kartal, İstanbul\'un en kapsamlı kentsel dönüşüm projelerinden birine ev sahipliği yapmaktadır. Kartal Sahili ve çevresi tamamen yenilenmektedir.',
        'tasınma': 'Kartal\'ın dönüşüm projeleri nedeniyle bölgede taşınma ve geçici depolama talebi oldukça yüksektir.',
        'ozel_hizmet': 'Kartal sahil bölgesindeki yeni rezidanslar için özel taşıma ve depolama çözümleri sunuyoruz.',
        'mahalleler': 'Soğanlık, Yakacık, Uğur Mumcu, Kordonboyu, Cevizli, Hürriyet, Topselvi, Esentepe',
    },
    24: {
        'name': 'Pendik',
        'slug': 'pendik',
        'yaka': 'Anadolu',
        'ozellik': 'Sabiha Gökçen Havalimanı\'na yakınlığıyla öne çıkan Pendik, hem konut hem ticari alanda hızla gelişen bir ilçedir.',
        'kentsel_donusum': 'Pendik\'te özellikle Yenişehir, Kavakpınar ve eski yerleşim bölgelerinde kentsel dönüşüm projeleri sürmektedir.',
        'tasınma': 'Havalimanı bağlantısı ve Marmaray hattı sayesinde Pendik\'e taşınma talebi artmaktadır. Yurt dışı depolama talebi de havalimanı yakınlığı nedeniyle yüksektir.',
        'ozel_hizmet': 'Pendik\'in geniş alanı nedeniyle Kurtköy, Yenişehir ve sahil bölgelerine özel lojistik planlamayla hizmet veriyoruz.',
        'mahalleler': 'Kurtköy, Yenişehir, Kavakpınar, Kaynarca, Velibaba, Güllü Bağlar, Esenyalı, Çamçeşme',
    },
    25: {
        'name': 'Maltepe',
        'slug': 'maltepe',
        'yaka': 'Anadolu',
        'ozellik': 'Sahil dolgu alanları ve yeni konut projeleriyle değişen Maltepe, Anadolu Yakası\'nın gelişen merkezlerinden biridir.',
        'kentsel_donusum': 'Maltepe\'de özellikle Başıbüyük ve Gülensu mahallelerinde kentsel dönüşüm projeleri yoğun şekilde devam etmektedir.',
        'tasınma': 'Maltepe sahil düzenlemesi ve yeni ulaşım projeleri bölgeye olan talebi artırmıştır. Taşınma ve depolama ihtiyacı yükselmektedir.',
        'ozel_hizmet': 'Maltepe\'nin sahil ve tepe bölgeleri arasındaki rakım farkı nedeniyle uygun araç seçimi yaparak güvenli taşıma sağlıyoruz.',
        'mahalleler': 'Cevizli, Altayçeşme, Fındıklı, Bağlarbaşı, Başıbüyük, Gülensu, İdealtepe, Küçükyalı',
    },
    26: {
        'name': 'Tuzla',
        'slug': 'tuzla',
        'yaka': 'Anadolu',
        'ozellik': 'İstanbul\'un doğu ucunda yer alan Tuzla, sanayi bölgeleri ve yeni konut projeleriyle gelişen bir ilçedir.',
        'kentsel_donusum': 'Tuzla\'da yeni konut projeleri ve sanayi bölgesi dönüşümleri eş zamanlı ilerlemektedir.',
        'tasınma': 'Tuzla\'nın sanayi bölgeleri nedeniyle kurumsal depolama talebi yüksektir. Ayrıca yeni konut projelerine taşınma yoğundur.',
        'ozel_hizmet': 'Tuzla Organize Sanayi Bölgesi\'ndeki firmalara kurumsal depolama ve arşiv saklama hizmeti sunuyoruz.',
        'mahalleler': 'Aydınlı, Şifa, Postane, Mimar Sinan, İçmeler, Orhanlı, Tepeören, Aydıntepe',
    },
    27: {
        'name': 'Sancaktepe',
        'slug': 'sancaktepe',
        'yaka': 'Anadolu',
        'ozellik': 'İstanbul\'un genç ilçelerinden Sancaktepe, hızla büyüyen nüfusu ve yeni konut projeleriyle dikkat çeker.',
        'kentsel_donusum': 'Sancaktepe\'de özellikle Sarıgazi ve Samandıra bölgelerinde kentsel dönüşüm projeleri aktif durumdadır.',
        'tasınma': 'Sancaktepe\'nin hızlı büyümesi sürekli taşınma ve depolama talebi yaratmaktadır. Yeni sitelere taşınma yoğundur.',
        'ozel_hizmet': 'Sancaktepe\'nin toplu konut bölgelerine özel ekip ve araç planlamasıyla hızlı hizmet veriyoruz.',
        'mahalleler': 'Sarıgazi, Samandıra, Yenidoğan, İnönü, Meclis, Akpınar, Abdurrahman Gazi, Eyüp Sultan',
    },
    28: {
        'name': 'Sultanbeyli',
        'slug': 'sultanbeyli',
        'yaka': 'Anadolu',
        'ozellik': 'Yoğun kentsel dönüşüm yaşayan Sultanbeyli, İstanbul\'un en dinamik dönüşüm bölgelerinden biridir.',
        'kentsel_donusum': 'Sultanbeyli, İstanbul\'da en yoğun kentsel dönüşüm yaşayan ilçelerden biridir. Hemen hemen tüm mahallelerde dönüşüm projeleri devam etmektedir. Bu durum uzun süreli depolama talebini ciddi oranda artırmaktadır.',
        'tasınma': 'Kentsel dönüşüm kaynaklı taşınma ve depolama ihtiyacı Sultanbeyli\'de çok yüksektir.',
        'ozel_hizmet': 'Sultanbeyli\'deki yoğun kentsel dönüşüm nedeniyle toplu depolama paketleri ve uzun süreli özel fiyatlar sunuyoruz.',
        'mahalleler': 'Battalgazi, Hamidiye, Hasanpaşa, Mehmet Akif, Mimar Sinan, Necip Fazıl, Orhangazi, Turgut Reis',
    },
    29: {
        'name': 'Beşiktaş',
        'slug': 'besiktas',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un en prestijli ilçelerinden Beşiktaş, Boğaz kıyısında konumuyla ve yüksek yaşam standartlarıyla öne çıkar.',
        'kentsel_donusum': 'Beşiktaş\'ta büyük ölçekli kentsel dönüşüm projesi az olmakla birlikte, eski binaların renovasyonu ve daire yenilemeleri yaygındır.',
        'tasınma': 'Beşiktaş\'ta yüksek kira fiyatları nedeniyle sık taşınma görülür. Öğrenci yoğunluğu da geçici depolama talebini artırır.',
        'ozel_hizmet': 'Beşiktaş\'ın dar sokakları, dik yokuşları ve tarihi binaları için özel küçük araçlar ve asansörlü taşıma ekipmanları kullanıyoruz.',
        'mahalleler': 'Ortaköy, Arnavutköy, Bebek, Etiler, Levent, Nişantaşı, Akatlar, Ulus',
    },
    30: {
        'name': 'Şişli',
        'slug': 'sisli',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un merkezi iş alanlarından biri olan Şişli, hem ticari hem konut yoğunluğuyla dikkat çeker.',
        'kentsel_donusum': 'Şişli\'de özellikle Kuştepe, Feriköy ve eski yapılaşma bölgelerinde dönüşüm projeleri sürmektedir.',
        'tasınma': 'Şişli\'nin iş merkezi konumu nedeniyle hem konut hem ofis taşınma ve depolama talebi yüksektir.',
        'ozel_hizmet': 'Şişli\'nin yoğun trafiği nedeniyle taşıma işlemlerini erken saatlerde veya hafta sonları planlayarak verimli hizmet sunuyoruz.',
        'mahalleler': 'Mecidiyeköy, Feriköy, Nişantaşı, Osmanbey, Teşvikiye, Bomonti, Kuştepe, Fulya',
    },
    31: {
        'name': 'Sarıyer',
        'slug': 'sariyer',
        'yaka': 'Avrupa',
        'ozellik': 'Boğaz\'ın kuzey ucunda yer alan Sarıyer, orman alanları ve lüks konut bölgeleriyle İstanbul\'un en yeşil ilçelerinden biridir.',
        'kentsel_donusum': 'Sarıyer\'de özellikle Derbent ve Armutlu gibi eski yerleşim bölgelerinde dönüşüm projeleri planlanmaktadır.',
        'tasınma': 'Sarıyer\'in villa ve müstakil ev yoğunluğu, büyük hacimli eşya depolama talebini artırmaktadır.',
        'ozel_hizmet': 'Sarıyer\'deki villa ve müstakil evler için geniş depolama odaları ve büyük hacimli nakliyat araçları sunuyoruz.',
        'mahalleler': 'Emirgan, İstinye, Tarabya, Maslak, Ayazağa, Derbent, Rumelihisarı, Baltalimanı',
    },
    32: {
        'name': 'Beylikdüzü',
        'slug': 'beylikduzu',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un batısında planlı yapılaşmasıyla bilinen Beylikdüzü, genç ailelerin ve yeni konut projelerinin merkezi haline gelmiştir.',
        'kentsel_donusum': 'Beylikdüzü\'nde büyük kentsel dönüşüm projesi az olmakla birlikte, ilk dönem sitelerin yenilenmesi gündemdedir.',
        'tasınma': 'Beylikdüzü\'ne İstanbul\'un diğer ilçelerinden taşınma yoğundur. Uygun fiyatlı konutlar bölgeye sürekli yeni sakin çekmektedir.',
        'ozel_hizmet': 'Beylikdüzü\'ndeki toplu konut siteleri için özel ekip planlaması yapıyor, site yönetimleriyle koordineli çalışıyoruz.',
        'mahalleler': 'Adnan Kahveci, Barış, Büyükşehir, Cumhuriyet, Dereağzı, Gürpınar, Kavakli, Yakuplu',
    },
    33: {
        'name': 'Esenyurt',
        'slug': 'esenyurt',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un en kalabalık ilçesi olan Esenyurt, yüksek nüfus yoğunluğu ve sürekli büyüyen konut stokuyla dikkat çeker.',
        'kentsel_donusum': 'Esenyurt\'ta eski yapılaşma bölgelerinde kentsel dönüşüm projeleri başlamıştır. Nüfus yoğunluğu nedeniyle dönüşüm talebi yüksektir.',
        'tasınma': 'İstanbul\'un en yoğun taşınma trafiğinin yaşandığı ilçelerden biridir. Hem yeni gelenler hem de ilçe içi taşınmalar çok yoğundur.',
        'ozel_hizmet': 'Esenyurt\'un yoğun nüfusu nedeniyle geniş araç filosu ve çoklu ekiplerle aynı gün birden fazla taşıma organize edebiliyoruz.',
        'mahalleler': 'Fatih, Piri Reis, Saadetdere, Ardıçlı, Namık Kemal, İncirtepe, Mehter Çeşme, Yeşilkent',
    },
    34: {
        'name': 'Bakırköy',
        'slug': 'bakirkoy',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un köklü ilçelerinden Bakırköy, sahil şeridi ve merkezi konumuyla prestijli bir yaşam alanıdır.',
        'kentsel_donusum': 'Bakırköy\'de büyük ölçekli kentsel dönüşüm projesi az olsa da eski binaların yenilenmesi ve tadilat çalışmaları yaygındır.',
        'tasınma': 'Bakırköy\'ün yüksek emlak değerleri nedeniyle ev küçültme ve tadilat kaynaklı depolama talebi yaygındır.',
        'ozel_hizmet': 'Bakırköy sahil bölgesindeki eski apartmanlar için asansörlü taşıma ve özel paketleme hizmeti sunuyoruz.',
        'mahalleler': 'Ataköy, Yeşilköy, Florya, Zuhuratbaba, Cevizlik, Osmaniye, Kartaltepe, Yenimahalle',
    },
    35: {
        'name': 'Bahçelievler',
        'slug': 'bahcelievler',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un en yoğun nüfuslu ilçelerinden Bahçelievler, merkezi konumu ve ulaşım bağlantılarıyla öne çıkar.',
        'kentsel_donusum': 'Bahçelievler\'de birçok mahallede kentsel dönüşüm projeleri aktif durumdadır. Özellikle Siyavuşpaşa ve Kocasinan bölgelerinde dönüşüm yoğundur.',
        'tasınma': 'Bahçelievler\'in merkezi konumu ve metro bağlantısı sürekli taşınma talebi yaratmaktadır.',
        'ozel_hizmet': 'Bahçelievler\'in yoğun yapılaşması nedeniyle koordineli ekip çalışmasıyla hızlı ve güvenli taşıma sağlıyoruz.',
        'mahalleler': 'Siyavuşpaşa, Kocasinan, Yenibosna, Şirinevler, Çobançeşme, Soğanlı, Fevzi Çakmak, Hürriyet',
    },
    36: {
        'name': 'Küçükçekmece',
        'slug': 'kucukcekmece',
        'yaka': 'Avrupa',
        'ozellik': 'Geniş yüzölçümü ve yüksek nüfusuyla Küçükçekmece, İstanbul\'un en büyük ilçelerinden biridir.',
        'kentsel_donusum': 'Küçükçekmece\'de özellikle Halkalı ve çevresinde kapsamlı kentsel dönüşüm ve yeni konut projeleri sürmektedir.',
        'tasınma': 'İstanbul Yeni Havalimanı\'na yakınlığı ve yeni metro hatları Küçükçekmece\'ye olan talebi artırmıştır.',
        'ozel_hizmet': 'Küçükçekmece\'nin geniş alanı nedeniyle tüm bölgelere etkin lojistik planlamayla hizmet veriyoruz.',
        'mahalleler': 'Halkalı, Atakent, Sefaköy, İkitelli, Cennet, Kanarya, Beşyol, Gültepe',
    },
    37: {
        'name': 'Başakşehir',
        'slug': 'basaksehir',
        'yaka': 'Avrupa',
        'ozellik': 'Planlı yapılaşması ve modern konut projeleriyle bilinen Başakşehir, İstanbul\'un en hızlı gelişen ilçelerinden biridir.',
        'kentsel_donusum': 'Başakşehir\'de eski yapılaşma çok az olduğundan kentsel dönüşüm yerine yeni proje yapılaşması hakimdir.',
        'tasınma': 'Başakşehir Şehir Hastanesi ve Kayaşehir gibi mega projelerin tamamlanmasıyla bölgeye taşınma talebi sürekli artmaktadır.',
        'ozel_hizmet': 'Başakşehir\'deki büyük toplu konut projeleri için site yönetimleriyle koordineli taşıma ve depolama hizmeti sunuyoruz.',
        'mahalleler': 'Kayaşehir, Başak, Bahçeşehir, Kayabaşı, Şahintepe, Ziya Gökalp, Altınşehir, Güvercintepe',
    },
    38: {
        'name': 'Fatih',
        'slug': 'fatih',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un tarihi yarımadasında yer alan Fatih, Sultanahmet, Eminönü ve Aksaray gibi tarihi bölgeleri barındırır.',
        'kentsel_donusum': 'Fatih\'te tarihi doku korunması nedeniyle klasik kentsel dönüşüm sınırlıdır. Ancak eski binaların restorasyon ve güçlendirme çalışmaları yoğundur.',
        'tasınma': 'Fatih\'in turizm ve ticaret yoğunluğu, özellikle ofis ve dükkan depolama talebini artırmaktadır.',
        'ozel_hizmet': 'Fatih\'in tarihi yarımada konumu, dar ve tarihi sokakları nedeniyle küçük araçlar ve el arabalarıyla dikkatli taşıma yapıyoruz.',
        'mahalleler': 'Sultanahmet, Eminönü, Aksaray, Balat, Fener, Çarşamba, Karagümrük, Vefa, Laleli',
    },
    145: {
        'name': 'Bağcılar',
        'slug': 'bagcilar',
        'yaka': 'Avrupa',
        'ozellik': 'İstanbul\'un en yoğun nüfuslu ilçelerinden Bağcılar, sanayi ve konut alanlarının iç içe geçtiği dinamik bir bölgedir.',
        'kentsel_donusum': 'Bağcılar, İstanbul\'un en yoğun kentsel dönüşüm yaşayan ilçelerinden biridir. Kirazlı, Güneşli ve Demirkapı mahallelerinde kapsamlı dönüşüm projeleri devam etmektedir.',
        'tasınma': 'Bağcılar\'ın yoğun nüfusu ve kentsel dönüşüm projeleri sürekli taşınma ve depolama talebi yaratmaktadır.',
        'ozel_hizmet': 'Bağcılar\'daki yoğun kentsel dönüşüm nedeniyle toplu depolama paketleri ve komşu avantajları sunuyoruz. Aynı binadan birden fazla daire için özel fiyatlar.',
        'mahalleler': 'Kirazlı, Güneşli, Demirkapı, Mahmutbey, Yıldıztepe, Fevzi Çakmak, Kemalpaşa, Kazım Karabekir',
    },
}


def generate_content(data):
    """Generate enriched HTML content for a district page"""
    name = data['name']
    yaka = data['yaka']
    mahalleler = data['mahalleler']

    html = f'''<div style="background:linear-gradient(135deg,#1B2D4F 0%,#0f1d35 100%);padding:50px 40px;border-radius:20px;margin-bottom:40px;color:#fff">
<h2 style="color:#fff;font-size:36px;margin-bottom:15px">{name} Eşya Depolama Hizmeti</h2>
<p style="color:#cbd5e1;font-size:18px;max-width:700px">{name} ve çevresinde kişiye özel kilitli odalarda güvenli eşya depolama. Profesyonel nakliyat dahil, anahtarınız sizde.</p>
</div>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin:30px 0">
<div style="text-align:center;padding:20px;background:#f0f9ff;border-radius:12px"><div style="font-size:32px;margin-bottom:8px">&#x1f512;</div><strong>Kişiye Özel Kilitli Oda</strong><p style="color:#64748b;font-size:14px">Anahtarınız sadece sizde</p></div>
<div style="text-align:center;padding:20px;background:#f0fdf4;border-radius:12px"><div style="font-size:32px;margin-bottom:8px">&#x1f4f9;</div><strong>7/24 Kamera</strong><p style="color:#64748b;font-size:14px">Güvenlik kamera sistemi</p></div>
<div style="text-align:center;padding:20px;background:#fff7ed;border-radius:12px"><div style="font-size:32px;margin-bottom:8px">&#x1f69a;</div><strong>Ücretsiz Nakliye</strong><p style="color:#64748b;font-size:14px">{name} adresinizden alınır</p></div>
<div style="text-align:center;padding:20px;background:#fdf4ff;border-radius:12px"><div style="font-size:32px;margin-bottom:8px">&#x1f6e1;</div><strong>Sigorta Güvencesi</strong><p style="color:#64748b;font-size:14px">Allianz sigorta koruması</p></div>
</div>

<h2>{name} Eşya Depolama</h2>
<p>{data['ozellik']}</p>
<p>{name} bölgesinde eşya depolama ve evden eve nakliyat hizmeti arıyorsanız, Evidepo ile tanışın. {name} ve çevresindeki müşterilerimize kişiye özel kilitli odalarda güvenli depolama hizmeti sunuyoruz. Eşyalarınızı {name} adresinizden alıyor, profesyonelce paketliyor ve kilitli depolama odanıza yerleştiriyoruz.</p>

<h2>{name} Depolama Nasıl Çalışır?</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin:25px 0">
<div style="background:#f0f9ff;padding:25px;border-radius:12px;border-left:4px solid #3b82f6">
<strong style="color:#1e40af">1. Ücretsiz Ekspertiz</strong>
<p style="color:#475569;margin-top:8px">Ekibimiz {name} adresinize gelir, eşyalarınızı değerlendirir ve net fiyat teklifi sunar.</p>
</div>
<div style="background:#f0fdf4;padding:25px;border-radius:12px;border-left:4px solid #22c55e">
<strong style="color:#15803d">2. Paketleme ve Taşıma</strong>
<p style="color:#475569;margin-top:8px">Profesyonel ekip eşyalarınızı özenle paketler ve güvenli araçlarla tesisimize taşır.</p>
</div>
<div style="background:#fff7ed;padding:25px;border-radius:12px;border-left:4px solid #f97316">
<strong style="color:#c2410c">3. Kilitli Odada Saklama</strong>
<p style="color:#475569;margin-top:8px">Eşyalarınız yalnızca sizin anahtarınızla açılan odanızda, 7/24 kamera gözetiminde korunur.</p>
</div>
<div style="background:#fdf4ff;padding:25px;border-radius:12px;border-left:4px solid #a855f7">
<strong style="color:#7c3aed">4. Geri Teslim</strong>
<p style="color:#475569;margin-top:8px">İhtiyaç duyduğunuzda eşyalarınızı {name} veya İstanbul\'daki herhangi bir adrese teslim ederiz.</p>
</div>
</div>

<h2>{name} Kentsel Dönüşüm Depolama</h2>
<p>{data['kentsel_donusum']}</p>
<p>Kentsel dönüşüm sürecinde eşyalarınız için 18-36 ay esnek sözleşme ve uzun süreli özel fiyatlar sunuyoruz. Yeni daireniz hazır olduğunda eşyalarınızı adresinize teslim ediyoruz.</p>
<p>Detaylı bilgi için <a href="/hizmetlerimiz/kentsel-donusum-depolama/">kentsel dönüşüm depolama</a> sayfamızı ziyaret edin.</p>

<h2>{name} Evden Eve Nakliyat ve Depolama</h2>
<p>{data['tasınma']}</p>
<p>Sanat Evden Eve Nakliyat güvencesiyle {name} bölgesinde evden eve nakliyat hizmeti sunuyoruz. Taşınma ve depolama ihtiyaçlarınızı tek elden karşılıyoruz. {name} içi, İstanbul içi ve şehirler arası nakliyat + depolama paketlerimiz mevcuttur.</p>
<p>Nakliyat ve depolama hakkında detaylı bilgi için <a href="/hizmetlerimiz/nakliyat-depolama/">nakliyat ve depolama</a> sayfamızı inceleyin.</p>

<h2>{name} Özel Hizmetlerimiz</h2>
<p>{data['ozel_hizmet']}</p>

<h2>{name} Depolama Hizmetlerimiz</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin:20px 0">
<a href="/hizmetlerimiz/ev-esyasi-depolama/" style="display:flex;align-items:center;gap:12px;padding:16px;background:#f8fafc;border-radius:10px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;transition:all 0.2s"><span style="font-size:24px">&#x1f3e0;</span><div><strong>Ev Eşyası Depolama</strong><br><span style="color:#64748b;font-size:13px">Mobilya, beyaz eşya, kişisel eşyalar</span></div></a>
<a href="/hizmetlerimiz/ofis-depolama/" style="display:flex;align-items:center;gap:12px;padding:16px;background:#f8fafc;border-radius:10px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;transition:all 0.2s"><span style="font-size:24px">&#x1f3e2;</span><div><strong>Ofis Depolama</strong><br><span style="color:#64748b;font-size:13px">Ofis mobilyası, arşiv, ekipman</span></div></a>
<a href="/hizmetlerimiz/tadilat-depolama/" style="display:flex;align-items:center;gap:12px;padding:16px;background:#f8fafc;border-radius:10px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;transition:all 0.2s"><span style="font-size:24px">&#x1f528;</span><div><strong>Tadilat Depolama</strong><br><span style="color:#64748b;font-size:13px">Tadilat süresince eşya koruma</span></div></a>
<a href="/hizmetlerimiz/kentsel-donusum-depolama/" style="display:flex;align-items:center;gap:12px;padding:16px;background:#f8fafc;border-radius:10px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;transition:all 0.2s"><span style="font-size:24px">&#x1f3d7;</span><div><strong>Kentsel Dönüşüm</strong><br><span style="color:#64748b;font-size:13px">Uzun süreli esnek depolama</span></div></a>
<a href="/hizmetlerimiz/yurt-disi-depolama/" style="display:flex;align-items:center;gap:12px;padding:16px;background:#f8fafc;border-radius:10px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;transition:all 0.2s"><span style="font-size:24px">&#x2708;</span><div><strong>Yurt Dışı Depolama</strong><br><span style="color:#64748b;font-size:13px">Yurt dışındayken güvenli saklama</span></div></a>
<a href="/hizmetlerimiz/nakliyat-depolama/" style="display:flex;align-items:center;gap:12px;padding:16px;background:#f8fafc;border-radius:10px;text-decoration:none;color:#1B2D4F;border:1px solid #e2e8f0;transition:all 0.2s"><span style="font-size:24px">&#x1f69a;</span><div><strong>Nakliyat + Depolama</strong><br><span style="color:#64748b;font-size:13px">Tek elden taşıma ve depolama</span></div></a>
</div>

<h2>Hizmet Verdiğimiz {name} Mahalleleri</h2>
<p>{name} ilçesinin tüm mahallelerine eşya depolama ve nakliyat hizmeti sunuyoruz:</p>
<p style="background:#f8fafc;padding:16px;border-radius:10px;color:#475569"><strong>{mahalleler}</strong> ve diğer tüm {name} mahalleleri.</p>

<h2>Neden Evidepo?</h2>
<ul style="list-style:none;padding:0">
<li style="padding:10px 0;border-bottom:1px solid #f1f5f9">&#x2705; <strong>Anahtar Sizde güvencesi</strong> — kilitli odanızın anahtarı yalnızca sizde</li>
<li style="padding:10px 0;border-bottom:1px solid #f1f5f9">&#x2705; <strong>7/24 kamera güvenliği</strong> — tesis kesintisiz izlenir</li>
<li style="padding:10px 0;border-bottom:1px solid #f1f5f9">&#x2705; <strong>Allianz sigorta güvencesi</strong> — eşyalarınız sigortalı</li>
<li style="padding:10px 0;border-bottom:1px solid #f1f5f9">&#x2705; <strong>Ücretsiz nakliyat</strong> — {name} adresinizden alınır</li>
<li style="padding:10px 0;border-bottom:1px solid #f1f5f9">&#x2705; <strong>Profesyonel paketleme</strong> — eğitimli ekip ile özenli koruma</li>
<li style="padding:10px 0;border-bottom:1px solid #f1f5f9">&#x2705; <strong>Şeffaf fiyatlandırma</strong> — gizli ücret yok, net teklif</li>
<li style="padding:10px 0">&#x2705; <strong>Sanat Nakliyat deneyimi</strong> — yılların profesyonel birikimi</li>
</ul>

<div style="background:linear-gradient(135deg,#1B2D4F 0%,#2a4270 100%);padding:40px;border-radius:16px;text-align:center;margin:40px 0">
<h3 style="color:#fff;font-size:24px;margin-bottom:10px">{name} Eşya Depolama Teklifi Alın</h3>
<p style="color:#cbd5e1;margin-bottom:20px">Ücretsiz ekspertiz ile {name} adresinize gelir, net fiyat teklifi sunarız.</p>
<a href="https://wa.me/905355298192" style="display:inline-block;background:#25D366;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:bold;margin:5px">WhatsApp ile Teklif Al</a>
<a href="tel:05355298192" style="display:inline-block;background:#E8614D;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:bold;margin:5px">0535 529 81 92</a>
</div>'''

    return html


def main():
    wp = WordPressPublisher()

    print("İLÇE SAYFALARI ZENGİNLEŞTİRME")
    print("=" * 60)

    success = 0
    failed = 0

    for page_id, data in ILCE_DATA.items():
        try:
            content = generate_content(data)

            resp = wp.session.post(
                f'{wp.api_base}/pages/{page_id}',
                json={'content': content}
            )
            resp.raise_for_status()

            # Count words
            import re
            text = re.sub(r'<[^>]+>', '', content).strip()
            words = len(text.split())

            success += 1
            print(f"  [OK] ID:{page_id:3d} | {data['name']:15s} | {words} kelime")
        except Exception as e:
            failed += 1
            print(f"  [FAIL] ID:{page_id:3d} | {data['name']:15s} | {e}")

    print(f"\nSonuç: {success} başarılı, {failed} başarısız")


if __name__ == '__main__':
    main()
