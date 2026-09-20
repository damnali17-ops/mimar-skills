# 03 — Fiyat Analizi ve Özel Poz

> Araç: `scripts/fiyat_analizi.py`. ÇŞB analiz formatı: **1 birim imalat** için girdi sarfları × rayiç = analiz toplamı; + kâr ve genel gider = birim fiyat.

## Analiz yapısı

```
Poz No · Tanım · Birim (imalat birimi)
  Malzeme   Σ (rayiç no · ad · birim · miktar · rayiç fiyat · tutar)
  İşçilik   Σ (usta/kalfa/işçi · saat · saat rayici)
  Makine    Σ (makine · saat · saat rayici — amortisman+yakıt+operatör)
  Nakliye   Σ (ton/m³ · mesafe formülü → TL)
  = ANALİZ TOPLAMI (girdi maliyeti)
  + Kâr ve genel gider  %25   (ÇŞB; YİİUY md.10)
  = BİRİM FİYAT
```

## Kurallar

| Konu | Kural | Güven |
|---|---|---|
| Kâr ve genel gider | %25 analiz toplamı üzerinden; idare sözleşme/şartnamede farklı oran belirleyebilir → `--kar` | 🟢 |
| Rayiç kaynağı | ÇŞB rayiç listesi (yıl) / kurum rayici / piyasa (≥3 teklif ortalaması 🟡) — her satırda "Kaynak" | 🟢 |
| Zayiat (fire) | malzeme miktarına dahil edilir (ÇŞB analizlerinde miktar zaten fireli); piyasa analizinde açıkça yazılır: beton çeliği %3–5, seramik %5–10 🟡 | 🟡 |
| İşçilik saat rayici | ÇŞB "10.100.xxxx" işçilik rayiçleri; brüt saat ücreti (sigorta dahil) | 🟡 |
| Makine saat rayici | ÇŞB makine analizleri (03.xxx / 10.4xx); saat = amortisman + yedek parça + yakıt + yağ + operatör 🟡 | 🟡 |
| Nakliye | ÇŞB 07.xxx formülleri: F = f(K, M) — K taşıma katsayısı (yol sınıfı), M mesafe (m/km); formül ve katsayı listeden 🔴 | 🔴 |
| Yuvarlama | girdi tutarları 4 ondalık, analiz toplamı ve birim fiyat 2 ondalık | 🟢 |
| Birim tutarlılığı | rayiç birimi ile miktar birimi aynı (ton × TL/ton); çimento kg ise /1000 | 🟢 |

## Ne zaman analiz?

1. **Yaklaşık maliyette:** imalat kurum listelerinde yok → rayiç + analiz + %25 (YİİUY md.10). Liste pozundan "benzer" diye türetme yapılmaz.
2. **Sözleşme aşamasında (yeni birim fiyat, YİGŞ md.22):** sıra —
   - a) sözleşmedeki benzer iş kalemleri / idarenin birim fiyatları,
   - b) diğer kamu kurumlarının birim fiyatları,
   - c) sözleşme yılı rayiçleri + analiz,
   - d) piyasa araştırması (≥3 teklif 🟡).
   Tutanak: yüklenici + kontrol teşkilatı; anlaşmazlıkta YFK (Yüksek Fen Kurulu) 🟡. Yeni birim fiyat **ihale tarihi bazlı** belirlenir, fiyat farkı ayrıca uygulanır (🟡).
3. **Teklif hazırlığında (yüklenici):** kendi rayiçleriyle analiz; %25 yerine firmanın kâr-genel gider oranı.

## Girdi dosyası

`templates/analiz-sablon.xlsx` — kolonlar: Poz No · Poz Tanımı · Poz Birimi · Tür (malzeme|iscilik|makine|nakliye|diger) · Rayiç No · Girdi Adı · Birim · Miktar · Rayiç Fiyat · Kaynak. Aynı Poz No'lu satırlar tek analizde toplanır; Poz Tanımı/Birimi ilk satırda yeter.

## Çıktı

- **İcmal:** poz başına malzeme/işçilik/makine/nakliye/diğer, analiz toplamı, kâr+GG, **birim fiyat**, işçilik oranı, güven.
- **Poz sayfaları:** girdi satırları (formüllü tutar), analiz toplamı, kâr+GG, birim fiyat.
- İşçilik oranı %60'ın üstünde veya %5'in altında → "sarf/rayiç kontrol" notu 🟡 (tipik betonarme işlerinde %15–40).

## Sık hatalar

- Rayiçte KDV dahil fiyat kullanmak (rayiçler KDV hariç).
- Malzeme rayicine nakliyeyi gömüp ayrıca nakliye yazmak (çift sayım).
- Saat yerine gün yazıp 8 ile çarpmamak.
- "Kaynak" boş → analiz 🔴, keşfe alınmaz.
