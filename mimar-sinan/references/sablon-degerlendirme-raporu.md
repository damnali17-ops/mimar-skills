# [Proje adı] — Mimari Proje Ön-Değerlendirme Raporu

| | |
|---|---|
| Yapı | [hükümet konağı / kaymakamlık / adliye / …] · sınıf [ ] |
| İdare / müellif | [ ] / [ ] |
| Safha · ölçek | [avan 1/200 · kesin 1/100 · uygulama 1/50] |
| Değerlendirilen belge | [PDF adı, tarih, rev] |
| İmar durumu | [belge elde / **plan varsayımıyla**] |
| Rapor tarihi | [ ] |

## 1. Sonuç

[≤5 cümle. "Proje şu N noktada uygun değil: … Bağlayıcı (sonradan düzelmez) olanlar: … Eksik belgeler nedeniyle yapılamayan kontroller: … En kritik: …"]

## 2. Eksik belgeler ve yapılamayan kontroller

| Belge | Durum | Yapılamayan kontrol | Etki |
|---|---|---|---|
| Yangın tahliye projesi / yağmurlama kararı | yok | J uzaklık sınırı (15/45 yağmurlamasız varsayıldı) | 🔴 |
| … | | | |

## 3. Pafta envanteri

| # | Pafta | Ölçek | Tarih/rev | Antet | Okunabilirlik | Kalibrasyon / not |
|---|---|---|---|---|---|---|
| 1 | Vaziyet planı | 1/500 | | tam | vektör | yazılı ölçü |
| … | | | | | | |

## 4. Bulgular (A–N)

Sütunlar: Kod · Konu · Ölçülen vs gereken · Durum · Dayanak + güven · Kaynak · Öneri (sorumlu)

### A · İmar
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|
| A-1 | | | | | | |

### B · Kat yükseklikleri
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### C · Giriş ve holler
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### D · Koridorlar
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### E · Merdivenler
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### F · Asansörler
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### G · Kapılar
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### H · Islak hacimler
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### I · Mahal ölçüleri ve m² programı
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### J · Yangın kaçış
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### K · Erişilebilirlik rotası
| Halka | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|
| K-1 | Engelli otopark | | | | | |
| K-2 | Yaya yolu | | | | | |
| K-3 | Giriş / rampa | | | | | |
| K-4 | Hol / danışma | | | | | |
| K-5 | Asansör / merdiven | | | | | |
| K-6 | Koridor | | | | | |
| K-7 | Birim kapısı | | | | | |
| K-8 | Erişilebilir WC | | | | | |
| K-9 | Salon | | | | | |
| K-10 | Kaçış / kurtarma alanı | | | | | |

### L · Otopark
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### M · Sığınak
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

### N · Tür-özel ve teslim içeriği
| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak | Kaynak | Öneri |
|---|---|---|---|---|---|---|

## 5. Hesap özetleri (script çıktıları)

**Kaçış (`kacis_hesabi.py`, yağmurlama: [var/yok])**
| Kat | Yük (kişi) | Kapı mevcut/gerekli (cm) | Merdiven mevcut/gerekli (cm) | Tek yön (m) | İki yön (m) |
|---|---|---|---|---|---|

**Merdiven (`merdiven_kontrol.py`)**
| Merdiven | Rıht | Basamak | 2a+b | Kol | Sahanlık | Sonuç |
|---|---|---|---|---|---|---|

**Otopark / sığınak (`otopark_siginak_hesabi.py`)**
| Emsal alanı | Araç gerekli/mevcut | Engelli gerekli/mevcut | Sığınak zorunlu | Kişi | m² gerekli/mevcut |
|---|---|---|---|---|---|

**İhtiyaç programı karşılaştırma (`ihtiyac_programi.py`)** — [varsa]

JSON çıktıları: Ek-1…Ek-4.

## 6. Çapraz doğrulama

| Kontrol | Sonuç | Etkilenen gruplar |
|---|---|---|
| Σ kat yükseklikleri = kesit | | |
| Kat planı brüt = m² cetveli | | |
| Vaziyet oturumu = zemin planı | | |
| Rıht adedi × rıht = kat yüksekliği | | |
| Mahal listesi = plan m² (±%5) | | |
| Emsal alanı (cetvel) = hesap girdisi | | |

## 7. İçişleri esaslarına aykırılıklar *(hükümet konağı ise)*

| Kod | Konu | Ölçülen vs gereken | Durum | Dayanak |
|---|---|---|---|---|
| | | | UD-B | İçişleri §B |

## 8. Uygulama projesinde kontrol edilecekler *(avan ise)*

- [ ] …

## 9. Kapanış

> Bu rapor ön-denetimdir. Ruhsat, onay ve uygunluk kararı ilgili idarenin (belediye / İl Özel İdare / Bakanlık / mimari estetik komisyonu) yetkisindedir. Yerel uygulama imar planı ve plan notları bu raporda kullanılan yönetmelik hükümlerinin önüne geçer.

---
Güven etiketleri: 🟢 doğrulandı (projede yazılı + madde elde) · 🟡 hesaplandı/ölçekten/türetildi (±%3) · 🔴 teyit gerekli. Durum kodları: U · U-S · U-N · UD · UD-B · E · Ö · NA · P (bkz. `06-rapor-formati.md`).
