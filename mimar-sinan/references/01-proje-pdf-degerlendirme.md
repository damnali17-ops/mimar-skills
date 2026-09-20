# 01 — Proje PDF Değerlendirme Prosedürü (FAZ 0–5)

> Mod 1'in ana akışı. Her FAZ'ın çıktısı bir sonrakinin girdisidir; FAZ atlanmaz, ama avan projede FAZ 3'ün detay kalemleri "uygulamada kontrol edilecek" listesine kayar.

## FAZ 0 — Bağlam ve girdi

1. `proje-context.md` oku; yoksa `templates/proje-context-template.md` ile taslak çıkar, sadece eksikleri sor.
2. Yapı türü → `08-mevzuat-haritasi.md` ile kart seti.
3. Safha → hangi kontroller uygulanır (`07-proje-teslim-cizim.md` safha tablosu).
4. **Eksik belge listesi** yaz: imar durumu · ihtiyaç programı · mahal listesi · yangın tahliye projesi (yağmurlama?) · estetik komisyon kararı. Her eksik için "yapılamayan kontrol": ör. *yangın tahliye projesi yok → J grubu yağmurlamasız varsayımla, 🔴*.

## FAZ 1 — Pafta envanteri

Tablo: `# | pafta adı | ölçek | tarih/rev | antet tam mı | okunabilirlik (vektör/taranmış) | kalibrasyon`.
- Ölçek yazılı değilse ve kalibre edilemiyorsa: paftayı **"ölçü kaynağı olarak kullanılamaz"** işaretle.
- Eksik pafta (ör. bodrum planı yok, kesit tek): "eksik belge" — bulgu değil.
- Kesit sayısı <2 veya merdivenden geçmiyorsa: B ve E grupları 🔴.

## FAZ 2 — Sayısal veri toplama

Tek bir veri tablosu doldur (raporun eki olur). Her satırda **kaynak**: `yazılı` / `ölçekten ±%3` / `ölçülemedi`.

| Grup | Toplanacak veri |
|---|---|
| Vaziyet | parsel alanı, çekme mesafeleri (4 yön), bina oturumu, yol kotu, ±0.00, otopark yerleri (adet + engelli), tören alanı, giriş sayısı |
| Kat planları | her kat: brüt alan, net alan, mahal listesi (ad + m²), koridor genişlikleri (en dar nokta), kapı genişlikleri (mahal → koridor → kaçış), WC adetleri (K/E/erişilebilir), merdiven/asansör konumu |
| Kesitler | kat yükseklikleri brüt + iç (asma tavan altı), toplam bina yüksekliği, saçak/mahya kotu, bodrum derinliği, merdiven rıht/basamak |
| Sirkülasyon | merdiven kol/sahanlık, basamak sayısı, asansör kabin ölçüsü, YGH ölçüsü, kaçış uzaklıkları (tek/iki yön, her kat, en uzak mahal) |
| m² cetveli | kat × emsale dahil/hariç, toplam emsal alanı, sirkülasyon oranı |

Hesap gereken her yerde `scripts/` çalıştır, JSON çıktısını sakla.

## FAZ 3 — 14 kontrol grubu (A–N)

| Grup | Konu | Kart | Script |
|---|---|---|---|
| **A** | İmar uyumu: emsal, Hmax, kat adedi, çekme, plan notları | 05-imar-otopark-siginak-hesabi · 01 PAİY md.19–22 | — |
| **B** | Kat yükseklikleri: iç ≥2.60; HK ≥4.50; bodrum | 01 md.28 · 03 §B | — |
| **C** | Giriş ve holler: giriş koridoru ≥2.20, giriş kapısı, erişilebilir giriş, rampa | 01 md.30 · 05 §4.5 | — |
| **D** | Koridorlar: ≥1.20 (PAİY) · kaçış ≥1.10 (BYKHY) · 150 dönüş (TS) | 01 md.29 · 04 · 05 §4.6 | kacis_hesabi |
| **E** | Merdivenler: kol ≥1.50, rıht ≤16, basamak ≥28, 2a+b, açık rıht, küpeşte | 01 md.31 · 05 §4.7.1 · 04 md.38 | merdiven_kontrol |
| **F** | Asansörler: 3 kat yer / 4+ tesis, kabin, kat önü, sedye | 01 md.34 · 05 §4.7.2 | — |
| **G** | Kapılar: net ≥90, yön, panik bar, eşik, kol | 01 md.32 · 05 §4.6.2 · 04 md.47 | — |
| **H** | Islak hacimler: WC adedi (50 kişi/1), erişilebilir WC ölçü, havalandırma | 01 md.48 · 05 §4.7.3 | ihtiyac_programi (adet) |
| **I** | Mahal ölçüleri ve m² programı: KBS normları, makam m², toplantı, sirkülasyon %60, teknik %4 | 02 · 03 §A · 02-mahal-ve-olcu-denetimi | ihtiyac_programi |
| **J** | Yangın kaçış: kullanıcı yükü, çıkış sayısı/genişliği, uzaklık, YGH | 04 · 04-yangin-erisilebilirlik-kontrolu | kacis_hesabi |
| **K** | Erişilebilirlik rotası: otopark → giriş → banko → asansör → WC → kurtarma alanı; işaretleme | 05 | — |
| **L** | Otopark: adet, engelli, birim alan, yükseklik | 06 | otopark_siginak_hesabi |
| **M** | Sığınak: zorunluluk, kişi, m², konum | 06 | otopark_siginak_hesabi |
| **N** | Tür-özel + teslim: HK İçişleri §B–D (kat sınırı, giriş holü, makam katı, tören alanı) · proje içeriği md.57 | 03 · 07 · KL-03 | — |

Her grup için bulgu satırı formatı `06-rapor-formati.md`. Bulgu yoksa da satır yaz: "A-0 · kontrol edildi, bulgu yok · U".

## FAZ 4 — Çapraz doğrulama

| Kontrol | Uyuşmazlıkta |
|---|---|
| Σ kat yükseklikleri (plan kotları) = kesit toplam yükseklik | B ve E grubu tamamen 🔴; kaynağı sor |
| Kat planı brüt alan = m² cetveli | I ve A grubu 🔴; hangisi esas? |
| Vaziyet bina oturumu = zemin kat planı dış hat | A grubu 🔴 |
| Kesit merdiven rıht sayısı × rıht = kat yüksekliği | E grubu 🟡 (script "rıht adedi" satırı) |
| Kapı cetveli genişlikleri = plan ölçüleri | G grubu 🟡 |
| Mahal listesi m² = plan yazılı m² | I grubu 🟡; ±%5 tolerans |
| Emsal alanı (cetvel) = script hesap girdisi | A/L/M 🔴 |
| Kaçış uzaklığı ölçümü, iki farklı mahalden tekrar | ±%3 dışında ise 🟡 → 🔴 |

## FAZ 5 — Rapor

`sablon-degerlendirme-raporu.md` doldur. Sıra: **sonuç paragrafı → eksik belgeler → pafta envanteri → A–N bulgu tablosu → çapraz doğrulama → uygulamada kontrol edilecekler (avan ise) → kapanış paragrafı (harfiyen)**. HK ise İçişleri aykırılıkları ayrı başlıkta. Script JSON'ları ek olarak.
