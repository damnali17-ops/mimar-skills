# 04 — Yangın Kaçışı ve Erişilebilirlik Kontrolü: Adım Adım (J + K grupları)

> Kartlar: `04-yangin-kacis.md`, `05-erisilebilirlik.md`. Araç: `scripts/kacis_hesabi.py`.

## J — Kaçış hesabı (her kat için)

**Adım 1 — Yağmurlama kararı.** Tahliye projesi / mimari raporda yazılı mı? Yazılı değilse **yağmurlamasız** hesapla, raporda 🔴 "yağmurlama teyit edilmedi; varsa uzaklık sınırları 30/75 m'ye çıkar".

**Adım 2 — Kat kullanıcı yükü.** Mahalleri türe ayır (ofis 10 · bekleme 3 · salon 1.5 · arşiv 30 · yemekhane 1.5 m²/kişi). Net alan. Katsayısı olmayan tür → script 🔴 verir, raporda aynen.

**Adım 3 — Çıkış sayısı.** Kat yükü ≥50 → ≥2 çıkış (birbirinden uzak; aralarındaki mesafe ≥ kat köşegeni/3, yağmurlamalı /5 🟡). Bina toplam ≥500 → 3, ≥1000 → 4 (md.33 🟡).

**Adım 4 — Genişlik.** Kapı: ceil(yük/100)×50 cm; merdiven: ceil(yük/60)×50 cm. Mevcut toplam = kata hizmet eden kaçış kapılarının/merdivenlerinin net genişlik toplamı. **Her tekil merdiven ≥150** (PAİY), **her tekil kapı ≥90** (TS) ayrıca.

**Adım 5 — Uzaklıklar.** Her katta en uzak mahalin en uzak köşesinden: tek yön (çıkmaz koridor veya tek çıkış) ≤15/30 · iki yön ≤45/75 m. Yürüme hattı ölçümü; ölçekten ise 🟡.

**Adım 6 — Kaçış merdiveni niteliği.** Yangın kompartımanı içinde mi, dışa doğrudan çıkıyor mu, bodruma iniyorsa YGH var mı (3–6 m², ≥180 kaçış yönü), basınçlandırma notu var mı, kapılar kaçış yönüne açılıyor mu, ≥50 kişi mahal kapısı panik barlı mı (md.47)?

**Adım 7 — Kurtarma yardım alanı** (TS 9111 §4.3.11–12): ≥4 kat veya asansörlü umumi binada kaçış merdiveni/YGH içinde ≥2 × 76×122 cm, kaçış genişliğini daraltmadan; her 200 kişiye kat başı ≥1.

**Script girdi (kat başına):**
```json
{"kat": "1. Kat",
 "mahaller": [{"ad": "Bürolar", "tur": "ofis", "alan_m2": 520}],
 "kapi_genislik_cm": [90, 90], "merdiven_genislik_cm": [150, 150],
 "tek_yon_kacis_m": 19, "iki_yon_kacis_m": 44}
```
Çıktıdaki `bulgular` satırları rapora **aynen** geçer (etiketiyle).

## K — Erişilebilirlik rotası (zincir kontrolü)

Rota halkaları; **her halka U olmadan bina "erişilebilir" denmez**. Bulgu halka adıyla.

| # | Halka | Kontrol | Dayanak |
|---|---|---|---|
| K-1 | Engelli otopark | adet 1/20 (≥1), ölçü 250×600+150 (tek 400×600), girişe ≤30 m, h ≥250 | TS 9111 §4.4.1 |
| K-2 | Yaya yolu otopark→giriş | ≥150 genişlik, eğim ≤%5, hissedilebilir yüzey, bordür rampası | §4.3 |
| K-3 | Giriş | ≥%50 giriş erişilebilir, ≥1 zemin kotunda; rampa %8/7/6/5, ≥100 genişlik, ≤10 m kol, sahanlık 150; kapı ≥90 (bb 100), eşik ≤1.3; HK/adliye/emniyet: tahsisli + güvenlikli geçit | §4.5.4 · §4.7.4 · PAİY md.30 |
| K-4 | Giriş holü / danışma | 150 dönüş; banko ≤86, diz ≥75, önü 150×150; işaret 120–160 + Braille; turnike yanı ≥90 geçit | §4.10.3.2 · §4.8 |
| K-5 | Düşey sirkülasyon | asansör ≥120×150 (PAİY+TS), kapı ≥90, kat önü 150×150, kumanda 90–120 + Braille; merdiven küpeşte 85–95 çift taraflı, basamak kontrast, açık rıht yok | §4.7.2 · §4.7.1 |
| K-6 | Koridor | ≥150 (kısa geçit ≥90), 150 dönüş koridor sonu, kapı önü manevra (itme 120 / çekme 150 + 45–60 yan) | §4.6 |
| K-7 | Hizmet birimi kapısı | ≥90, kol 90–110 L tipi, eşiksiz, cam işaret bantları | §4.6.2 |
| K-8 | Erişilebilir WC | ≥1K+1E (her katta tercih); kabin ≥150×142/150; kapı ≥90 dışa/sürgülü, dışarıdan açılır kilit; klozet önü 122×167.5 / yan 122×142 / ön+sol 150×142; tutunma barları; lavabo 80–85, diz ≥70; acil çağrı | §4.7.3 · PAİY md.48 |
| K-9 | Toplantı/konferans | tekerlekli sandalye yeri 90×140 (≥2, oran müellif), kürsü erişimi, indüksiyon döngüsü | §4.10 |
| K-10 | Kaçış / kurtarma | kurtarma yardım alanı (yukarı Adım 7), sesli+görsel alarm, kaçış işaretleri 120–160 | §4.3.11 · BYKHY md.72 |

**Avan projede** K-1, K-3 (rampa eğimi ve giriş kotu), K-5 (asansör var/yok, kabin), K-8 (WC var/yok ve kabin ölçüsü) kontrol edilir; K-4, K-6 manevra, K-7 kol, K-9 detay, K-10 işaret **uygulamaya** kalır.

## Raporda J ve K'nin sunumu

- J: script özet tablosu (kat · yük · kapı mevcut/gerekli · merdiven mevcut/gerekli · tek/iki yön uzaklık) + bulgular listesi.
- K: 10 halkalık tablo, her halka U / UD / Ö / NA; en az bir UD varsa başlıkta "**Erişilebilirlik zinciri kırık: K-3, K-8**".
- Proaktif: 4+ kat ve asansör yok/tek → hem F hem K-5 hem K-10 (kurtarma alanı) satırı.
