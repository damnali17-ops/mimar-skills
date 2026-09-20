# KL-01 — Avan Proje (1/200) Kontrol Listesi

> Doldurulabilir. `[ ]` → `[x]` uygun · `[-]` uygun değil · `[?]` belge/ölçü yok · `[n]` safha dışı. Sonuna durum kodu ve dayanak yaz (kart `06-rapor-formati.md`).
> Avan projede **detay** kalemi (kapı kolu, tutunma barı, işaret) sorulmaz; safha-bağlayıcı (UD-B) kalemler koyu.

## 0 · Girdi ve belge
- [ ] `proje-context.md` dolu (yapı türü, sınıf, safha, imar durumu)
- [ ] İmar durumu belgesi elde — yoksa A grubu "plan varsayımıyla"
- [ ] İhtiyaç programı (idare onaylı) elde
- [ ] Yağmurlama kararı yazılı (tahliye projesi / mimari rapor)
- [ ] Mimari estetik komisyon görüşü (varsa)

## 1 · Pafta envanteri
- [ ] Vaziyet planı ölçekli, kuzey oku, kotlar, çekme mesafeleri yazılı
- [ ] Tüm kat planları (bodrum dahil) + mahal adı/m²
- [ ] ≥2 kesit, biri merdivenden; kat yükseklikleri yazılı
- [ ] Tüm cepheler, Hmax çizgisi
- [ ] m² cetveli: kat × emsale dahil/hariç
- [ ] Antet tam (proje, idare, müellif, ölçek, tarih/rev)

## A · İmar
- [ ] **Emsal alanı ≤ izin** (parsel × KAKS) — cetvel emsale esas sütunu
- [ ] **TAKS** sağlanıyor
- [ ] **Hmax / kat adedi** sağlanıyor (kesit kotları)
- [ ] **Çekme mesafeleri** 4 yön (plan / PAİY md.19–22)
- [ ] Plan notları listelendi, yönetmeliği aşanlar ayrı satır

## B · Kat yükseklikleri
- [ ] İskân edilen kat iç yüksekliği ≥2.60 (PAİY md.28)
- [ ] **HK: kat yüksekliği ≥4.50** (İçişleri §B)
- [ ] Plan kotları toplamı = kesit (çapraz)

## C · Giriş
- [ ] Giriş holü/koridoru ≥2.20 (PAİY md.30)
- [ ] Giriş kotu: kot farkı varsa rampa, eğim %8/7/6/5, kol ≤10 m
- [ ] ≥1 erişilebilir giriş zemin kotunda; girişlerin ≥%50'si (TS 9111 §4.5.4)
- [ ] HK/adliye/emniyet: ana + protokol + servis girişleri ayrı; erişilebilir giriş güvenlikli

## D · Koridorlar
- [ ] Ana koridorlar ≥1.20 (PAİY md.29); en dar nokta (kolon) kontrol
- [ ] Kaçış koridoru genişliği kaçış hesabına yetiyor (kacis_hesabi.py)

## E · Merdivenler
- [ ] Kol/sahanlık ≥1.50 (PAİY md.31/1-a)
- [ ] Rıht ≤16, basamak ≥28, 2a+b 60–64 (merdiven_kontrol.py) — kesitte yazılıysa
- [ ] Rıht adedi × rıht = kat yüksekliği (çapraz)
- [ ] Kaçış merdiveni sayısı ve konumu (birbirinden uzak, dışa çıkış)

## F · Asansör
- [ ] Kat adedi 3 → yer; **≥4 → tesis** (PAİY md.34)
- [ ] Kabin ≥1.20 dar kenar / ≥1.80 m² / kapı ≥0.90; kamu: sedye ölçüsü
- [ ] Kat önü ≥1.50 × 1.50

## H · Islak hacimler
- [ ] WC adedi: her 50 kişiye 1, K/E ayrı, her katta grup (PAİY md.48)
- [ ] Erişilebilir WC ≥1K + ≥1E; kabin ≥150 × 142/150 planda görünüyor

## I · Mahal programı
- [ ] Mahal listesi = ihtiyaç programı (eksik/fazla mahal listesi)
- [ ] **Makam odaları İçişleri §A m²** (Vali 80 · Vali Yrd 40 · İl Müd 35 · Kaymakam 60 · İlçe Müd 24)
- [ ] KBS §4.3 kişi başı azami (9 / 6 / 12) aşılmıyor
- [ ] Toplantı normu ve paylaşımlı toplantı ilkesi
- [ ] Sirkülasyon ≈%60, teknik ≤%4 (cetvelden)
- [ ] Vatandaş yoğun birimler zemin katta (HK)

## J · Yangın kaçış (avan seviyesi)
- [ ] Kat başına kullanıcı yükü ve ≥2 çıkış (≥50 kişi)
- [ ] Tek/iki yön kaçış uzaklıkları ≤15/45 (yağmurlamasız) — script
- [ ] Kaçış merdiveni bodruma iniyorsa YGH yeri var
- [ ] Kaçış kapı/merdiven toplam genişliği ≥ gerekli (md.32)

## K · Erişilebilirlik (avan seviyesi)
- [ ] Engelli otopark ≥1 (1/20), girişe ≤30 m
- [ ] Rampa eğimi ve genişliği (C ile)
- [ ] Asansör var/ölçü (F ile)
- [ ] Erişilebilir WC var/ölçü (H ile)
- [ ] ≥4 kat: kurtarma yardım alanı yeri (kaçış merdiveni/YGH)

## L · Otopark
- [ ] Araç adedi ≥ emsal ÷ 100 (yerel oran varsa o) — script
- [ ] Engelli ≥1/20
- [ ] Kapalı otopark h ≥2.20 (engelli güzergâhı 2.50)

## M · Sığınak
- [ ] **Emsal ≥1 500 m² → sığınak mahali var**
- [ ] Alan ≥ (emsal ÷ 20) × 1 m², ≥9 — script
- [ ] Bodrumda, emsal dışı gösterilmiş

## N · Tür-özel (HK için KL-03'e geç)
- [ ] **Kat sayısı ≤ zemin+2**, makam katı sınır içinde
- [ ] Giriş holü 8 m (çift kat) — İçişleri §B
- [ ] Tören alanı, bayrak direği, Atatürk büstü vaziyette
- [ ] Adliye/emniyet: kurum tip proje kriterleri 🔴 istenir

## Uygulama projesine bırakılanlar (raporda ayrı liste)
Kapı kolu yüksekliği · tutunma barları · küpeşte detayı · işaret/Braille · banko ölçüsü · eşik · hissedilebilir yüzey · kapı yönü/panik bar · malzeme listesi · kapı-pencere cetveli.
