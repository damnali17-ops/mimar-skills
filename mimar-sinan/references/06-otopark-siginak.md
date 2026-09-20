# 06 — Otopark ve Sığınak Hesapları

> Otopark Yönetmeliği RG 22/2/2018 – 30340 (+ yerel otopark yönetmeliği) · Sığınak Yönetmeliği RG 25/8/1988 – 19910 (2010 değ.). Hesap aracı: `scripts/otopark_siginak_hesabi.py`.
> **Plan notu ve yerel otopark yönetmeliği bu kartın önüne geçer.**

## Otopark

| Kural | Değer | Güven | Dayanak |
|---|---|---|---|
| Kamu kurumu / resmî bina oranı | **100 m² inşaat alanına 1 araç** | 🟡 — Ek-1 resmî tablo + yerel yönetmelikle teyit | Otopark Yön. Ek-1 |
| Hangi alan? | emsale esas (KAKS) inşaat alanı; bodrum otopark/sığınak/teknik hariç | 🟡 | Ek-1 dipnot |
| Birim park alanı | **≥20 m²** (manevra dahil); araç yeri 2.50 × 5.00 (açık) / 2.50 × 5.00 + geçiş | 🟢 | md.4 tanım |
| Engelli park yeri | her **20 araca 1**, en az 1; ölçü TS 9111 §4.4.1 (250×600 + 150 transfer / tek 400×600) | 🟢 | Otopark Yön. + TS 9111 |
| Kapalı otopark net yüksekliği | ≥2.20 m; engelli güzergâhında ≥2.50 (TS 9111) | 🟢 | |
| Rampa eğimi (araç) | ≤%15 düz, kavisli ≤%12; giriş ilk 3.5 m ≤%7 | 🟡 | md.? teyit |
| Otopark yeri parselde karşılanamıyorsa | plan notu/idare kararıyla bedel — raporda "plan notuna göre" etiket | 🟢 | md.10–12 🟡 |
| Bisiklet / elektrikli şarj | umumi binada elektrikli araç şarj altyapısı — oran 🔴 | 🔴 | 2021 değ. |
| Kamu aracı / makam aracı | HK'da kapalı makam otoparkı (kart 03 §B) | 🔴 | İçişleri |

**Hesap:** gerekli araç = ceil(emsal alanı ÷ oran); engelli = max(1, ceil(araç ÷ 20)); asgari otopark alanı = araç × 20 m² (yalnız kapasite kontrolü için; gerçek alan projeden).

## Sığınak

| Kural | Değer | Güven | Dayanak |
|---|---|---|---|
| Zorunluluk eşiği (konut dışı) | emsale esas toplam inşaat alanı **≥1 500 m²** → sığınak zorunlu | 🟢 | Sığınak Yön. md.8 |
| Kişi hesabı — resmî daire/işyeri | kişi = **emsal alanı ÷ 20** | 🟢 | md.8 |
| Alan | **≥1 m²/kişi**, asgari **9 m²** | 🟢 | md.8–9 |
| Yükseklik | net ≥2.40 m | 🟡 | md.9 |
| Konum | bodrumda, tercihen en alt kat, dış duvara bitişik olmayan; toprak örtüsü/ betonarme; iki giriş (biri acil çıkış) | 🟡 | md.9–10 |
| Hava, WC, su | kişi başı hava, ≥1 WC / 25 kişi? — 🔴 | 🔴 | md.10 |
| Barışta kullanım | depo/arşiv/spor vb. — sığınak fonksiyonunu bozmayan; otopark olamaz | 🟡 | md.12 |
| Emsale dahil mi? | sığınak emsale dahil **değil** (PAİY md.5) | 🟢 | PAİY |
| Eşik altı | emsal <1 500 m² → zorunlu değil; ortak sığınak/yerel karar | 🟢 | |

**Hesap:** kişi = ceil(emsal ÷ 20); gerekli m² = max(9, kişi × 1.0). Birden fazla bloktan oluşan kampüste her blok ayrı.

## Rapor satırı örnekleri

- `L-1 · Otopark adedi · 28 araç mevcut / 32 gerekli (3 200 m² ÷ 100) · UD · Otopark Yön. Ek-1 🟡 · yerel yönetmelik oranı teyit; eksik 4 yer için plan notu bedel hükmü var mı?`
- `M-1 · Sığınak · emsal 3 200 m² ≥ 1 500 → zorunlu; 160 kişi → ≥160 m²; projede 120 m² · UD · Sığınak Yön. md.8 🟢`
- `M-2 · Sığınak mahali yok · UD · md.8 · bodrumda arşivin bir kısmı sığınağa dönüştürülebilir (barışta kullanım md.12)`
