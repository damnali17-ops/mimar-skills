# 01 — Poz Sistemi: ÇŞB, KGM, DSİ, İLBANK ve Özel Pozlar

> Poz = tarifli, birimli, fiyatlı imalat kalemi. Skill'in poz eşleştirmesi (`poz_bul.py`) **kullanıcının verdiği listede** çalışır; bu kart listeyi okumayı ve doğru bölümde aramayı kolaylaştırır. Numaralama ve bölüm adları yıllık yayınlarla değişebilir → listenin kendi bölüm başlıkları esastır (🟡).

## ÇŞB — Yapı İşleri Birim Fiyatları (Yüksek Fen Kurulu, yıllık)

| Öğe | Biçim | Not | Güven |
|---|---|---|---|
| Birim fiyat pozu (2018 sonrası) | `Y.16.050/04` — `Y.` + bölüm + sıra `/alt` | "Y" = Yapı işleri; eski `16.050/4` numaraları listede "eski poz" sütununda | 🟡 |
| Rayiç (girdi) numarası | `10.130.1001` — 10 + grup + sıra | 10.100 işçilik/su · 10.130 çimento/bağlayıcı · 10.140 agrega · 10.160 demir-çelik … (grup kodları listeden) | 🟡 |
| Makine rayici | `03.xxx` (eski sistem) / 10.4xx | saat başı; amortisman + yakıt + operatör ayrı satır olabilir | 🔴 |
| Nakliye pozu | `07.xxx` formüllü | K (taşıma katsayısı) ve M (mesafe) ile; formül listeden | 🔴 |
| Birim | m, m², m³, kg, ton, ad, sa, takım, km | Liste birimi esas; metraj birimi farklıysa çevrim 🟡 | 🟢 |
| Tarif | uzun; "… yapılması, … temini ve yerine konulması" kalıpları | Eşleştirmede DURAK kelimeler atılır (`poz_bul.py`) | 🟢 |
| Fiyat | KDV hariç, **%25 kâr ve genel gider dahil** | Analize dayalı fiyata tekrar eklenmez | 🟢 |

**Bölüm numaraları (tipik, 🟡 — listeyle teyit):**

| Bölüm | Konu |
|---|---|
| Y.15 | Kazı, dolgu, zemin iyileştirme, iksa, nakliye ilişkili kazı kalemleri |
| Y.16 | Beton (hazır/santral beton, demirsiz-demirli, şap ile karışmaz) |
| Y.17 | Kâgir/duvar (tuğla, gazbeton, briket, taş) |
| Y.18 | Ahşap, çatı, çatı örtüsü |
| Y.19 | Yalıtım (su, ısı, ses), tecrit |
| Y.21 | Kalıp ve iskele |
| Y.23 | Demir-çelik (betonarme çeliği, profil, hasır) |
| Y.25 | Boya, badana, cila |
| Y.26 | Döşeme ve duvar kaplama (seramik, mermer, granit, laminat) |
| Y.27 | Sıva, şap, derz |
| Y.28–Y.29 | Doğrama, kapı-pencere, cam, madeni imalat (🔴 sınır) |
| Y.30+ | Peyzaj, altyapı, muhtelif (🔴) |
| Mekanik / Elektrik | ayrı listeler: "Tesisat Birim Fiyatları" (sıhhi, ısıtma, havalandırma) ve "Elektrik Tesisatı Birim Fiyatları" — poz önekleri farklı (🟡) |

**Arama ipucu:** `poz_bul.py --bolum Y.16 "C30/37"` bölümü daraltır; tarifi "malzeme + sınıf + ölçü + iş" biçiminde sadeleştir ("plywood kalıp düz yüzey", "Ø14-Ø28 nervürlü çelik").

## KGM — Karayolları Genel Müdürlüğü

- Poz biçimi `KGM/xx.xxx` veya `xx.xxx` (KGM listesi içinde); yol, köprü, sanat yapıları, üstyapı (asfalt, plentmiks), drenaj.
- Birim fiyatlar KGM Birim Fiyat Listesi (yıllık); **%25 kâr-genel gider dahil** (🟡 listeden teyit).
- Nakliye ve taşıma formülleri KGM'nin kendi tablolarında; ÇŞB formülleriyle karıştırma.
- Aynı imalat (ör. C30 beton) ÇŞB ve KGM'de farklı fiyatlı olabilir → **hangi kurumun işi** ise o liste; karışık kullanım keşifte 🟡 not.

## DSİ — Devlet Su İşleri

- Poz biçimi `DSİ-xx.xxx` / bölüm kodlu; su yapıları, kanal, gölet, sulama, içme suyu hattı.
- DSİ Birim Fiyat Cetveli (yıllık); analizler DSİ rayiçleriyle.

## İLBANK, MSB, Sağlık, diğer kurumlar

- İLBANK: altyapı (içme suyu, kanalizasyon, arıtma); kendi poz ve rayiç listesi.
- Bakanlıklar çoğunlukla ÇŞB listesini esas alır; özel imalatlar için "Kurum Özel Birim Fiyatı" yayımlayabilir.
- Sözleşmede hangi kurum listesinin esas alınacağı yazılıdır (idari şartname / sözleşme md. 🟡) — hakedişte **sözleşme birim fiyatı**, listenin güncel değeri değil.

## Özel pozlar (ÖBF / ÖZ / Y.ÖZL)

- Listede olmayan imalat için analiz yapılır (`fiyat_analizi.py`); numara `ÖBF-001` gibi idarece verilir.
- Yaklaşık maliyette: rayiç + analiz + %25 (YİİUY md.10). Sözleşme aşamasında: **yeni birim fiyat tutanağı** (YİGŞ md.22) — sıra: idare birim fiyatları → diğer kamu kurumu fiyatları → rayiç + analiz → piyasa (🟡, kart 04).
- Özel pozun tarifi, birimi ve analiz girdileri çıktıda tam yazılır; "benzer poza dayanarak" fiyat verilmez.

## Sık hatalar

1. Eski numara ile yeni numarayı aynı sanmak (`16.050/4` ≠ `Y.16.050/04` fiyatı farklı yıl/sistem).
2. ÇŞB fiyatına tekrar %25 eklemek.
3. Metrajda "ton" listede "kg" (çelik) → ×1000 çevrimi atlanır.
4. Mekanik/elektrik pozlarını inşaat listesinde aramak.
5. Farklı yılın listesinden fiyat alıp güncelleme yapmamak (YİİUY md.11).
