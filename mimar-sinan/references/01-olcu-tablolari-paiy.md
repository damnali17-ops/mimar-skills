# 01 — PAİY Ölçü Tabloları (md.28 · 29 · 30 · 31 · 32 · 34 · 48)

> Planlı Alanlar İmar Yönetmeliği, RG 3/7/2017 – 30113. Değerler konsolide metinden; **fıkra/bent numaraları değişikliklerle kaymış olabilir — raporda madde numarasıyla yetin, fıkra vermeden önce güncel metinden teyit et.**
> "Umumi bina": kamu hizmeti için kullanılan resmî binalar + ibadet, eğitim, sağlık, spor, sinema, tiyatro, otel, iş hanı vb. (PAİY md.5 tanımlar). Hükümet konağı, kaymakamlık, adliye, emniyet = umumi bina.

## md.28 — Kat yükseklikleri

| Kural | Değer | Güven |
|---|---|---|
| İskân edilen kat iç (net) yüksekliği | **≥2.60 m** (döşeme kaplaması üstü → tavan sıvası altı) | 🟢 |
| Kat yüksekliği planla belirlenmemişse | ticaret/karma zeminde 4.50 m, diğer katlarda 3.60 m'yi geçemez *(brüt, döşeme üstünden döşeme üstüne)* | 🟡 — plan notu varsa plan |
| Bodrum katta iskân edilen mahal | iç yüksekliği ≥2.60 m; iskân edilmeyen (depo, teknik) ≥2.20 m | 🟡 |
| Hükümet konağı | PAİY'e ek olarak İçişleri §B kat yüksekliği **≥4.50 m** — kart 03 | 🟢 |

Denetim notu: kesitte "kat yüksekliği" brüt ise iç yüksekliği **döşeme + kaplama + tavan sıva/asma tavan** düşerek hesapla; asma tavan altını iç yükseklik say. Plan–kesit uyuşmazlığında 🔴.

## md.29 — Koridorlar ve holler

| Kural | Değer | Güven |
|---|---|---|
| Hol ve koridor net genişliği (umumi bina) | **≥1.20 m** | 🟢 |
| Koridor net yüksekliği | ≥2.10 m (kaçış koridoru için BYKHY de 2.10) | 🟡 |
| Koridorda daralma yapan tesisat/dolap/kapı kanadı | net genişlik daraltılmış yerden ölçülür | 🟢 — ölçüm kuralı |

*Bu, mimari asgaridir. Aynı koridor BYKHY md.32 kaçış genişliği hesabını (kart 04) ve TS 9111 tekerlekli sandalye manevrasını (kart 05, 150 cm dönüş) ayrıca sağlamalıdır.*

## md.30 — Bina girişleri ve rampalar

| Kural | Değer | Güven |
|---|---|---|
| Umumi bina giriş koridoru / giriş holü net genişliği | **≥2.20 m** | 🟢 |
| Giriş kapısı net genişliği (umumi) | ≥1.50 m (çift kanatlıysa bir kanat ≥0.90) | 🟡 |
| Girişte kot farkı varsa | rampa zorunlu; rampa başı-sonu düz sahanlık ≥1.50 m | 🟡 |
| Rampa eğimi — yeni yapı | kot farkı ≤15 cm → **%8** · 16–50 cm → **%7** · 51–100 cm → **%6** · >100 cm → **%5** | 🟢 (md.30/12 + TS 9111 Çiz.1) |
| Rampa eğimi — mevcut yapı (tadilat) | 10 / 9 / 8 / 6 (aynı kademeler) | 🟢 |
| Rampa net genişliği | ≥0.90 m *(TS 9111 ≥1.00 m; iki yönlü 1.80)* → TS geçerli | 🟡 |
| Rampa korkuluk / küpeşte | her iki yanda, 0.90 m + 0.70 m ikili küpeşte; kenar bordürü ≥5 cm | 🟡 — TS 9111 §4.7.4 ile birlikte oku |
| Yağmur/kar için giriş saçağı | umumi binalarda giriş üstü kapalı | 🔴 — plan notu/yerel yönetmelik |

## md.31 — Merdivenler

| Kural | Değer | Güven |
|---|---|---|
| Kol ve sahanlık genişliği — umumi bina / kamu | **≥1.50 m** (md.31/1-a) | 🟢 |
| Kol ve sahanlık genişliği — konut | ≥1.20 m | 🟢 |
| TSE ile ilişki (md.31/1-c) | TSE ölçüsü küçükse yönetmelik; **TSE daha sıkıysa TSE** | 🟢 |
| Rıht yüksekliği | umumi **≤0.16 m** · konut ≤0.18 m | 🟢 |
| Basamak derinliği (genişliği) | **≥0.27 m** → TS 9111 §4.7.1.3.1 **≥0.28 m** geçerli | 🟢 |
| Formül | **2a + b = 60–64 cm** (a rıht, b basamak) | 🟢 |
| Dönel/kavisli merdivende basamak | dar uçta ≥0.10 m, kol ekseninde ≥0.27 m; kamu binasında ana merdiven dönel olamaz | 🟡 |
| Açık rıht | umumi binada **yasak** (TS 9111 §4.7.1.3.1) | 🟢 |
| Korkuluk yüksekliği | ≥0.90 m; kat boşluğu tarafında ≥1.00 m *(BYKHY 1.10 m?)* | 🔴 — BYKHY md.38 ile teyit |
| Sahanlık | kol genişliğinden dar olamaz; kapı sahanlığa açılırken kapı kanadı sahanlığı daraltamaz | 🟢 |
| Merdiven evi doğal aydınlatma/havalandırma | umumi binada dış cepheye açık pencere veya BYKHY basınçlandırma | 🟡 |

Hesap: `scripts/merdiven_kontrol.py --kat-yuksekligi <cm> --basamak <cm> --rih <cm> --kol <cm> --sahanlik <cm>`

## md.32 — Kapılar

| Kural | Değer | Güven |
|---|---|---|
| İç kapı net geçiş genişliği (yönetmelik) | ≥0.80 m *(bazı değişikliklerde 0.90)* → **TS 9111 ≥0.90 m geçerli** (kamu) | 🟡 — PAİY sayısı 🔴 teyit; sonuç değişmez |
| Kapı yüksekliği | ≥2.10 m | 🟢 |
| WC/banyo kapısı | ≥0.80 m; erişilebilir WC ≥0.90 m dışa açılır | 🟢 |
| Kaçış yolu kapıları | kaçış yönüne açılır (≥50 kişi) — BYKHY md.47 | 🟢 |
| Eşik | umumi binada eşiksiz veya ≤1.3 cm pahlı (TS 9111) | 🟢 |

## md.34 — Asansörler

| Kural | Değer | Güven |
|---|---|---|
| Kat adedi 3 | asansör **yeri** bırakılır | 🟢 |
| Kat adedi **4 ve üzeri** (bodrum dahil sayım: iskân edilen kat) | asansör **tesisi zorunlu** | 🟢 |
| Kabin | dar kenar **≥1.20 m** · alan **≥1.80 m²** · kapı net **≥0.90 m** | 🟢 |
| Umumi binada (kamu) | en az biri sedye taşıyabilecek ölçüde *(TS 9111 §4.7.2: kabin 110×140 asgari, tercih 200×140)* | 🟡 |
| Kat adedi/kullanıcı eşiği ile ikinci asansör | umumi binada birden fazla asansör gerektiren eşik | 🔴 — md.34 güncel metin |
| Asansör önü bekleme alanı | ≥1.50 × 1.50 m (TS 9111 §4.7.2) | 🟢 |
| Yangın asansörü | bina yüksekliği >51.50 m — BYKHY md.62; kamu idari binada nadir | 🟢 |
| Kat sayısı sayımı | asansör zorunluluğunda bodrum + zemin + normal katlar, iskân edilen; çatı arası iskân edilirse dahil | 🟡 |

## md.48 — Tuvaletler (umumi bina)

| Kural | Değer | Güven |
|---|---|---|
| Adet | her **50 kişiye 1** WC (K/E ayrı); her katta en az bir grup | 🟢 |
| Erişilebilir WC | **≥1 kadın + ≥1 erkek** (veya ortak kullanımlı ≥1) — her katta değil, binada; kat başına TS 9111 tercih | 🟢 |
| Erişilebilir kabin | TS 9111 §4.7.3: ≥150 × 142/150 cm, kapı ≥0.90 dışa açılır — kart 05 | 🟢 |
| Pisuvar | erkek WC grubunda; erişilebilir pisuvar ön kenar ≤43 cm | 🟡 |
| Havalandırma | doğal veya mekanik; iç WC'de mekanik zorunlu | 🟢 |
| Kişi sayısı kaynağı | ihtiyaç programı çalışan + anlık vatandaş; yoksa BYKHY Ek-5/A ile türet ve 🟡 etiketle | — |

## PAİY'de hesaba giren diğer maddeler

- **md.5 tanımlar — emsal (KAKS):** emsale dahil edilmeyen alanlar (bodrum otopark, sığınak, teknik hacimler, yangın merdiveni ve güvenlik holü, asansör boşlukları, ışıklıklar, bina girişi ...) — tam liste kart 05-imar-otopark-siginak-hesabi.md. Bent bent teyit 🟡.
- **md.19–22 çekme mesafeleri:** ön ≥5 m, yan ≥3 m (h ≤ 4 kat), arka h/2 — plan notu yoksa; kamu parselinde genelde plan verir.
- **md.56/57:** ruhsat ve proje içeriği — kart 07.
