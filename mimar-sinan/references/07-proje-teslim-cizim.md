# 07 — Proje Teslim İçeriği, Kamu Ruhsat Rejimi, Pafta Standardı

> PAİY md.57 (yapı projeleri) · md.56 (kamu yapıları) · Mimarlık ve Mühendislik Hizmetleri Şartnamesi (Bayındırlık, 1985 – avan/kesin/uygulama tanımları) · TS 88 / ISO 128 çizim (antet, ölçek, kuzey).
> Bu kart **FAZ 1 pafta envanteri**nin kontrol listesidir. Eksik pafta = "eksik belge", bulgu değil; ama eksik yüzünden yapılamayan kontroller raporun başına yazılır.

## Safha tanımları (şartname)

| Safha | Ölçek | İçerik asgari | Neye bulgu yazılır |
|---|---|---|---|
| **Avan (ön) proje** | 1/200 (vaziyet 1/500) | vaziyet, kat planları, ≥2 kesit, cepheler, m² cetveli, ihtiyaç programı karşılaştırma, mimari rapor | mahal m², kat sayısı/yüksekliği, sirkülasyon şeması, giriş-çekirdek yeri, otopark/sığınak yeri, imar uyumu, İçişleri §B |
| **Kesin proje** | 1/100 | avan + tüm ölçülendirme, mahal listesi, kapı/pencere şeması, tesisat şaftları | koridor/merdiven/kapı ölçüleri, WC adedi, kaçış uzaklığı |
| **Uygulama projesi** | 1/50 (+ detay 1/20, 1/5, 1/1) | kesin + sistem detayları, merdiven-WC-rampa detayları, mahal listesi, kapı-pencere cetveli, tavan planı | tüm A–N grupları; detay eksiği; malzeme |

**Avan projeye detay eksikliği yazılmaz** (kapı kolu yüksekliği, tutunma barı vb.). Avan raporunda bu kalemler "uygulama projesinde kontrol edilecek" listesine gider.

## md.57 — Mimari proje içeriği (ruhsata esas)

| Pafta | Ölçek | Zorunlu içerik | Güven |
|---|---|---|---|
| Vaziyet planı | 1/500 – 1/200 | parsel sınırı, ada/parsel no, çekme mesafeleri, yol kotu, bina köşe kotları, kuzey, yapı yaklaşma, otopark, giriş, ağaç, tören alanı (HK) | 🟢 |
| Kat planları (tüm katlar, bodrum, çatı) | 1/50 (avan 1/200, kesin 1/100) | mahal adı + net m², ölçülendirme, kapı-pencere no, döşeme kotu, kesit çizgileri, yangın kaçış oku (tercih) | 🟢 |
| Kesitler | ≥2, biri merdivenden | kat yükseklikleri (brüt + iç), zemin kotu, saçak/mahya kotu, Hmax kontrolü, bodrum derinliği | 🟢 |
| Cepheler | tüm cepheler | malzeme, kotlar, Hmax çizgisi | 🟢 |
| Çatı planı | | eğim, dere, çıkış | 🟢 |
| Mahal listesi | | döşeme/duvar/tavan malzemesi, süpürgelik | 🟢 (uygulama) |
| m² cetveli | | kat × brüt/net/emsale dahil-hariç; toplam emsal alanı | 🟢 |
| Mimari rapor | | ihtiyaç programı özeti, tasarım kararları, yangın ve erişilebilirlik yaklaşımı | 🟡 |
| Sistem detayları | 1/20 | cephe kesiti, merdiven, rampa, erişilebilir WC, asansör kuyusu | 🟢 (uygulama) |
| İmar durumu belgesi + aplikasyon krokisi + zemin etüdü | ek | ruhsat ekleri | 🟢 |

## md.56 — Kamu yapılarında ruhsat

- Kamu kurum ve kuruluşlarına ait yapılar da **ruhsata tabidir**; ruhsat ilgili belediye/İl Özel İdare'den. İstisna: gizlilik/güvenlik gerekçeli (MSB, MİT) bazı yapılar — kamu idari bina istisna değil. 🟢
- Kamu yapılarında projeler ilgili idarece (yatırımcı kuruluş / ÇŞİDB Yapı İşleri) **onaylanmış** olur; belediye imar durumu, plan uygunluğu ve TUS için inceler. 🟡
- Mimari estetik komisyonu: PAİY md.66 — belediye komisyonu kararı ruhsat öncesi; HK'da ayrıca İçişleri görüşü. 🟡
- Kamu yapılarında **yapı denetimi**: 4708 kapsam dışı; kontrollük idarece (TUS/kontrol teşkilatı). 🟢 — rapor kapsamı dışı.

## Pafta standardı (antet ve okunabilirlik)

Her paftada: proje adı · idare · müellif (oda sicil) · pafta adı/no · **ölçek** · **tarih / revizyon** · **kuzey oku** (vaziyet + kat planı) · kot referansı (±0.00 tanımı). Biri eksikse pafta envanterinde "antet eksik" işaretle; ölçek yoksa **ölçekten hesap yapılamaz** → o paftaya dayanan tüm ölçüler 🔴.

## PDF okuma notları

- Vektörel PDF: ölçü yazıları metin olarak okunur → `projede yazılı` (🟢).
- Yazılı ölçü yok, ölçek var: ölçekten ölçüm ±%3 → 🟡 `ölçekten hesaplandı`.
- Taranmış PDF: pdf skill ile rasterize; ölçek doğrulaması için iki bilinen ölçüyü (kapı 90, aks aralığı) karşılaştır; tutmazsa 🔴 `ölçülemedi`.
- Sayfa boyutu (A0/A1) ile ölçek çarpanı: PDF 1:1 basılmamış olabilir; **paftadaki yazılı bir ölçüyle kalibre et**, kalibrasyon oranını raporda belirt.
