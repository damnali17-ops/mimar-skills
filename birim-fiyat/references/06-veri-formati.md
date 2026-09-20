# 06 — Veri Formatı: Girdi/Çıktı Şemaları

> Tüm araçlar `xlsx_io.py` ile xlsx **veya** csv (noktalı virgül) okur; sayfa seçimi `dosya.xlsx:SayfaAdı` veya `dosya.xlsx:1` (0 tabanlı indeks). İlk satır başlık. Kolon adları esnek: `ortak.KOLON` eş anlamlıları (küçük harf, Türkçe karakter sadeleştirilmiş) ile bulunur. Sayı biçimi `1.234,56` ve `1234.56` ikisi de kabul.

## Kolon eş anlamlıları (ortak.KOLON)

| Anahtar | Kabul edilen başlıklar |
|---|---|
| poz | Poz, Poz No, Poz Numarası, No, Kod, Birim Fiyat No, BF No |
| tanim | Tanım, Açıklama, İmalat, Tarif, İş Kalemi, İşin Adı, Birim Fiyat Tarifi, İmalatın Cinsi, Yapılan İş |
| birim | Birim, Ölçü Birimi, Br, Ölçü |
| fiyat | Birim Fiyat, Birim Fiyatı, Fiyat, B.Fiyat, BF, Sözleşme Birim Fiyatı, Teklif Birim Fiyatı, Rayiç, Rayiç Bedeli |
| miktar | Miktar, Metraj, Adet, Kümülatif Miktar, Toplam Miktar, Sözleşme Miktarı |
| grup | İş Grubu, Grup, Bölüm, Kısım |
| kaynak | Kaynak, Kurum, Yayın, Liste |
| yil | Yıl, Yılı, Dönem |
| tur | Tür, Cins, Girdi Türü, Kalem Türü |
| rayic_no | Rayiç No, Rayiç Poz, Girdi No, Rayiç Kodu |

Başlık "Birim Fiyat (TL)" gibi ek içerirse ön/son ek eşleşmesiyle bulunur. Bulunamazsa script hata verir ve başlıkları listeler.

## Girdi şemaları

| Dosya | Zorunlu | İsteğe bağlı | Şablon |
|---|---|---|---|
| Birim fiyat listesi | Poz No · Tanım · Birim Fiyat | Birim · Kaynak · Yıl | `birim-fiyat-listesi-sablon.xlsx` |
| Metraj (keşif) | Poz No · Miktar | Tanım · Birim · İş Grubu · Birim Fiyat (`--fiyat-metrajdan`) | `metraj-sablon.xlsx` |
| Analiz | Poz No · Tür · Miktar · Rayiç Fiyat | Poz Tanımı · Poz Birimi · Rayiç No · Girdi Adı · Birim · Kaynak | `analiz-sablon.xlsx` |
| Hakediş — Sözleşme | Poz No · Sözleşme Miktarı · Sözleşme Birim Fiyatı | Tanım · Birim · İş Grubu | `hakedis-sablon.xlsx:Sözleşme` |
| Hakediş — Metraj | Poz No · Kümülatif Miktar | | `hakedis-sablon.xlsx:Metraj` |
| Fiyat farkı dönem | Hakediş · An · a1 · a2 · b1…b5 · endeks çiftleri | Go · Gn | `fiyat-farki-donem-sablon.xlsx` |

## Çıktı şemaları

| Araç | Dosya | Sayfalar |
|---|---|---|
| poz_bul --dosya | `poz_eslesme.xlsx` | Eşleşme: Sıra · Tarif · Girilen poz · Önerilen poz · Tanım · Birim · Birim fiyat · Puan · Güven · 2. aday · 2. puan |
| kesif_ozeti | `kesif_ozeti.xlsx` | Keşif Özeti · İş Grupları · Eşleşmeyen · Özet |
| fiyat_analizi | `fiyat_analizi.xlsx` | İcmal · (poz başına sayfa) |
| hakedis | `hakedis_N.xlsx` | Hakediş N · İcmal |
| fiyat_farki | `fiyat_farki.xlsx` | Fiyat Farkı |

Her araç ayrıca stdout'a **JSON** (programatik) + okunabilir özet basar. JSON'u rapora göm; sayıları elle kopyalama.

## Excel teknik notları

- Formül hücreleri `<f>` + önbellek değeri `<v>` ile yazılır: Excel açınca yeniden hesaplar; Excel dışı okuyucular önbelleği görür.
- Stil: başlık kalın + gri, sayı `#,##0.00`, yüzde `0.00%`, üst satır dondurulmuş.
- Sayfa adı ≤31 karakter (Excel sınırı); poz numaraları kısaltılır.
- Türkçe karakterler UTF-8; CSV çıktısı UTF-8 BOM'lu, `;` ayraçlı (Türkçe Excel varsayılanı).
- `xlsx_io.oku` formüllü kaynak dosyada yalnızca önbellek değerini okur; kaynak Excel'de hesaplanmamış formül varsa `None` gelir → kullanıcıya "dosyayı Excel'de kaydedin" de.

## Puanlama (poz_bul)

`puan = 0,50 × sorgu kelimelerinin tanımda bulunma oranı + 0,10 × Jaccard + 0,20 × dizi benzerliği + 0,20 × sayısal terim uyumu (C25/30, Ø12, 20 cm)`. Eş anlamlılar (demir↔çelik, kalıp↔kalıbı…) tanım tarafında genişletilir. Poz numarası tam/ön ek eşleşmesi 1,00/0,95. Güven: 🟢 ≥0,80 · 🟡 0,50–0,79 · 🔴 <0,50.
