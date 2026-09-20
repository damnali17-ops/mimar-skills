# 07 — Yaklaşık Maliyet Mevzuatı

> Yapım İşleri İhaleleri Uygulama Yönetmeliği (YİİUY), RG 4/3/2009 – 27159 (değişiklikleriyle) md.8–11; 4734 sayılı KİK md.9; Kamu İhale Genel Tebliği ilgili bölümleri. Madde/fıkra numaraları 🟡 — güncel metinle teyit.

## md.8 — Yaklaşık maliyete esas miktarlar

- İdare, **uygulama projesi** (anahtar teslim) veya **ön/kesin proje** (birim fiyat) üzerinden metraj çıkarır; mahal listesi, teknik şartname ve birim fiyat tarifleriyle uyumlu **iş kalemleri/grupları** listesi hazırlar.
- Anahtar teslim işlerde iş grupları ve **pursantaj oranları** yaklaşık maliyetten türetilir; sözleşme eki olur.
- Skill: metraj kullanıcıdan gelir; metraj çıkarma bu skill'in işi değil (mm-metraj).

## md.9 — Fiyat kaynakları ve gizlilik

Fiyat tespitinde sıra (🟡, "veya" ile birlikte kullanılabilir):
1. Kamu kurum ve kuruluşlarınca belirlenmiş **birim fiyatlar** (ÇŞB, KGM, DSİ, İLBANK…) — tarifi ve şartları uyuyorsa.
2. İdare veya diğer idarelerin **önceki ihale/sözleşme fiyatları** (güncellenerek).
3. **Rayiç + analiz** (ÇŞB rayiçleri veya piyasa rayici, ÇŞB analiz formatı).
4. **Piyasa araştırması** — yazılı fiyat teklifleri (asgari sayı ve ortalama kuralı 🟡), meslek odaları, ilgili kuruluşlar.
- Her fiyatın kaynağı **hesap cetvelinde** belirtilir → skill'in "Kaynak" kolonu.
- Yaklaşık maliyet **ihale sonuçlanana kadar gizli**; ilanda, dokümanda, isteklilere açıklanmaz. (KİK md.9)

## md.10 — Hesaplama

- Miktar × birim fiyat = iş kalemi tutarı; toplam = **yaklaşık maliyet (KDV hariç)**.
- Analize dayalı fiyatlarda **%25 kâr ve genel gider** eklenir; kamu kurumu birim fiyatları bu payı içerir.
- Yaklaşık maliyet hesap cetveli + icmal + dayanaklar, **yaklaşık maliyet komisyonu/görevliler** tarafından imzalanır (idare kararı). Skill çıktısı bu cetvelin ekidir, imza idarenin.

## md.11 — Güncelleme

- Fiyatların ait olduğu dönem ile ihale tarihi arasında fark varsa **Yİ-ÜFE** ile güncelleme; genelde 12 ayı aşan fiyatlar için (🟡).
- Güncelleme katsayısı = ihale ayı endeksi / fiyat dönemi endeksi. Skill katsayıyı hesaplamaz; kullanıcı verir, keşifte 🟡.

## Yaklaşık maliyet neyi belirler?

| Konu | Bağlantı |
|---|---|
| İhale usulü ve eşik değerler | KİK md.8 eşikleri, ilan süreleri (md.13) — yaklaşık maliyete göre |
| Yeterlik kriterleri | iş deneyimi, banka referansı, ekipman oranları yaklaşık maliyetin yüzdesiyle (YİİUY md.29–48 🟡) |
| Aşırı düşük teklif sınır değeri | sınır değer hesabında yaklaşık maliyet girdisi (KİGT 45. madde 🟡) |
| Sözleşme bedeli üst sınırı | teklif > yaklaşık maliyet olabilir ama ödenek/uygunluk değerlendirmesi |
| Pursantaj | anahtar teslim işlerde iş grubu oranları |

## Skill davranışı

- Keşif çıktısına "Yaklaşık maliyet gizlidir" notu (Özet sayfası).
- Fiyat kaynağı olmayan kalem → hesap dışı + 🔴; "benzer poz" ile doldurulmaz.
- Liste yılı ≠ ihale yılı → md.11 uyarısı.
- ÇŞB fiyatına %25 eklenmez; analize eklenir.
- Mekanik/elektrik/altyapı icmalde ayrı satır; toplam KDV hariç.
- Yüklenici tarafında teklif hazırlarken aynı araçlar kullanılabilir; o zaman "yaklaşık maliyet" değil "teklif keşfi" başlığı (`--baslik`).
