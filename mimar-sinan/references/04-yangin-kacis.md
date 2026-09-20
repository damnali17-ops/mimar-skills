# 04 — BYKHY: Kullanıcı Yükü, Kaçış Yolları, Yangın Güvenlik Holü

> Binaların Yangından Korunması Hakkında Yönetmelik, RG 19/12/2007 – 26735 (2009, 2015, 2021 değ.). Kamu idari binası = "büro" kullanım sınıfı (md.8). Adliye/emniyet de büro; salon/mahkeme salonu "toplanma amaçlı" olarak ayrıca hesaplanır.
> Hesap aracı: `scripts/kacis_hesabi.py` — bu kartın sabitlerini kullanır.

## Ek-5/A — Kullanıcı yükü katsayıları (m²/kişi)

| Mahal | m²/kişi | Güven |
|---|---|---|
| Büro / ofis | **10** | 🟢 |
| Bekleme salonu (ayakta) | **3** | 🟢 |
| Toplantı/konferans (sandalyesiz, sabit koltuksuz) | **1.5** | 🟢 |
| Konferans (sabit koltuklu) | koltuk sayısı | 🟢 |
| Arşiv / depo | **30** | 🟢 |
| Yemekhane | **1.5** | 🟢 |
| Mahkeme salonu | 1.5 (dinleyici) — toplanma | 🟡 |
| Derslik / kütüphane / laboratuvar / otopark | katsayı elde değil | 🔴 — Ek-5/A teyit |

Kat kullanıcı yükü = Σ ceil(alan ÷ katsayı). **Net** alan kullanılır; koridor ve WC alanı yüke girmez (🟡 yaygın uygulama — brüt kullanılırsa güvenli taraf).

## md.32 — Kaçış genişliği

- **Birim genişlik = 50 cm.** Gerekli genişlik = ceil(yük ÷ birim kişi) × 50 cm.
- Birim kişi: **kapı ve koridor 100 kişi**, **merdiven 60 kişi** (yağmurlamasız); yağmurlamalı binada değerler artabilir — 🔴 md.32 tablo teyit.
- Kaçış koridoru net **≥110 cm**, yükseklik ≥210 cm; iki birimden az verilemez (≥100 cm) ama umumi bina için PAİY md.29 **120** ve md.31 merdiven **150** zaten üstünde.
- Kapı: kaçış yolunda net ≥80 cm (BYKHY) → TS 9111 **≥90 cm** geçerli; ≥50 kişi mahal kapısı kaçış yönüne açılır, kilitlenemez, panik bar (md.47).
- Kat yükü **≥50 kişi → en az 2 çıkış**; bina toplam yükü ≥500 → 3, ≥1000 → 4 çıkış (md.33) 🟡.

## Ek-5/B — Kaçış uzaklıkları (büro)

| Durum | Yağmurlamasız | Yağmurlamalı | Güven |
|---|---|---|---|
| Tek yönlü kaçış (çıkmaz koridor / tek çıkış) | **15 m** | **30 m** | 🟢 |
| İki yönlü kaçış (en uzak nokta → en yakın çıkış) | **45 m** | **75 m** | 🟢 |
| Toplanma amaçlı (salon) — tek/iki yön | 15 / 45 | 30 / 75 | 🟡 |
| Otopark | 20? / 45 | 🔴 | 🔴 |

Ölçüm: mahal içindeki en uzak noktadan, **yürüme yolu boyunca**, kaçış merdiveni kapısına veya dış kapıya kadar. Mobilya bilinmiyorsa merkez-hat + mahal köşegeni. Ölçekten alınan uzaklık ±%3 → 🟡.

## md.33–34 — Kaçış yolu sayısı, yangın güvenlik holü (YGH)

- **YGH gerekliliği:** bina yüksekliği >21.50 m veya kaçış merdiveni bodruma iniyorsa ya da yüksek bina; kamu idari binada genelde **bodrum bağlantısı** nedeniyle gerekir. 🟡
- **YGH ölçüsü:** **3–6 m²**, kaçış yönünde genişlik **≥1.80 m**, kapılar yangına dayanıklı ve kendiliğinden kapanır (md.34/3). Hol ve merdiven basınçlandırma: yüksek bina veya iç merdiven.
- İki kaçış merdiveni arası: kaçış yolu uzunluğunun ≥1/3'ü (yağmurlamalı 1/5) — 🟡.
- Kaçış merdivenleri yangın kompartımanı içinde, dışa doğrudan çıkışlı; giriş holü üzerinden çıkış korunmalıysa kabul (md.38–39).

## md.38–41 — Kaçış merdiveni geometrisi

| Kural | BYKHY | PAİY/TS ile birleşik sonuç | Güven |
|---|---|---|---|
| Basamak derinliği | ≥25 cm | **≥28** (TS 9111) | 🟢 |
| Rıht | ≤17.5 cm | **≤16** (PAİY umumi) | 🟢 |
| Kol genişliği | hesap (≥100 cm) | **≥150** (PAİY kamu) | 🟢 |
| Korkuluk | ≥110 cm (kat boşluğu) | — | 🟡 |
| Dönel merdiven | kaçış merdiveni olarak yasak (≥50 kişi) | — | 🟡 |
| Dış kaçış merdiveni | yüksekliği 21.50 m'ye kadar, korunmuş cephe | — | 🟡 |
| Kaçış rampası | eğim ≤%10 (yağmurlamalı %12) | TS 9111 ≤%8 | 🟡 |

## Kompartıman, yağmurlama, algılama (belge kontrolü)

- Yağmurlama zorunluluğu: bina yüksekliği >30.50 m veya toplam alan eşiği (md.96) — kamu idari binada genelde **isteğe bağlı**; kaçış uzaklığı hesabında yağmurlama "var" sayılabilmesi için **tahliye projesinde belirtilmiş** olmalı. Belirsizse yağmurlamasız değerle hesapla, 🔴 not.
- Yangın kompartımanı alanı, algılama sistemi, acil aydınlatma-yönlendirme (md.72–73), yangın dolabı (md.94): mimari raporda "tahliye projesinde var mı?" kontrolüyle sınırlı.

## Denetimde sıralama

1. Kat yükü → 2. gerekli çıkış sayısı → 3. gerekli genişlik (kapı + merdiven ayrı) → 4. uzaklıklar → 5. YGH/basınçlandırma → 6. kapı yönü/panik bar. Her adım `kacis_hesabi.py` çıktısından; script "TEYİT GEREKLİ" verdiyse raporda 🔴.
