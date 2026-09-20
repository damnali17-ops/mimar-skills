# 05 — İmar, Otopark ve Sığınak Hesabı (A + L + M grupları)

> Kartlar: `01-olcu-tablolari-paiy.md` (md.5, 19–22), `06-otopark-siginak.md`. Araç: `scripts/otopark_siginak_hesabi.py`.
> **Plan üstündür.** İmar durumu belgesi yoksa tüm A grubu `plan varsayımıyla` 🟡; L/M hesapları emsal alanı cetvelden alınır.

## A — İmar uyumu

| Kontrol | Kaynak | Nasıl |
|---|---|---|
| Emsal (KAKS) | imar durumu × parsel alanı | izin verilen emsal alanı = parsel × emsal; projede emsale esas alan (cetvel) ≤ izin |
| TAKS | imar durumu | zemin oturumu ÷ parsel ≤ TAKS |
| Hmax / kat adedi | imar durumu; HK'da ayrıca zemin+2 (03 §B) | kesit saçak/mahya kotu − yol kotu (PAİY md.5 bina yüksekliği tanımı 🟡) |
| Çekme mesafeleri | plan; yoksa PAİY md.19–22 (ön 5, yan 3, arka h/2) | vaziyet planından 4 yön; balkon/çıkma çekme içine ≤1.5 m 🟡 |
| Plan notları | belge | yönetmeliği aşan her hüküm ayrı satır; "plan notuna göre" etiketi |
| Kotlandırma | vaziyet ±0.00, yol kotu | zemin kat döşemesi yol kotundan ≤ +1.00 (PAİY md.11 🟡); bodrum iskân sayımı |

**Emsale dahil olmayan alanlar** (PAİY md.5 emsal tanımı — bent bent 🟡 teyit): bodrumdaki otopark · sığınak · teknik hacimler (kazan, trafo, su deposu, hidrofor, havalandırma) · asansör ve tesisat şaftları · ışıklıklar · yangın merdiveni ve güvenlik holleri · bina giriş holü (belirli oran) · açık çıkma/teras %50 · çatı arası (iskân edilmeyen). Cetvel bu ayrımı vermiyorsa A-grubu 🔴 ve cetvel istenir.

## L — Otopark

```
oran      = yerel otopark yön. (varsa) | 100 m²/araç (kamu, Ek-1 🟡)
araç      = ceil(emsal alanı ÷ oran)
engelli   = max(1, ceil(araç ÷ 20))
min alan  = araç × 20 m²
```
Kontrol: vaziyet + bodrum planındaki park yeri sayısı (ölçü 2.50×5.00 sağlayan) ≥ araç; engelli yerler TS ölçüsünde ve girişe ≤30 m; kapalı otopark h ≥2.20 (engelli güzergâhı 2.50); rampa eğimi ≤%15 🟡. Parselde karşılanamıyorsa plan notu/bedel → "plan notuna göre" 🟡, UD yazma.

## M — Sığınak

```
zorunlu   = emsal alanı ≥ 1 500 m²
kişi      = ceil(emsal alanı ÷ 20)
m²        = max(9, kişi × 1.0)
```
Kontrol: bodrumda mahal var mı; alan ≥ m²; net yükseklik ≥2.40 🟡; iki giriş (biri acil çıkış) 🟡; barışta kullanım otopark **değil**; sığınak emsale dahil edilmemiş mi (cetvel).

## Script

```
python3 scripts/otopark_siginak_hesabi.py --emsal 3200 --insaat 4100 --mevcut-arac 28 --mevcut-engelli 1 --siginak-m2 120 [--yerel-oran 80]
```
`--yerel-oran` verilmezse otopark satırı 🟡. Çıktı `bulgular` rapora aynen.

## Sık tuzaklar

- Emsal alanına bodrum otoparkını katıp otoparkı "fazla" hesaplamak → emsal alanı cetvelin **emsale esas** sütunundan.
- Sığınak kişi hesabında inşaat alanı kullanmak → **emsal alanı**.
- HK'da tören alanı ve makam otoparkını unutup açık otoparkı tören alanına yaymak → N grubu ile çakışır.
- Plan notu "otopark bedeli alınır" diyorsa L-grubu UD yazmak → 🟡 "plan notuna göre bedel".
