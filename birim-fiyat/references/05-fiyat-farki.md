# 05 — Fiyat Farkı (2013/5217 sayılı BKK Esasları)

> "4734 Sayılı Kamu İhale Kanununa Göre İhale Edilen Yapım İşlerinde Uygulanacak Fiyat Farkına İlişkin Esaslar" — RG 29/8/2013 – 28750, değişiklikleriyle. Araç: `scripts/fiyat_farki.py`. **Fiyat farkı ancak idari şartname ve sözleşmede "verilecektir" deniyorsa hesaplanır**; yoksa F = 0.

## Formül (md.5)

```
Pn = a1 × (İn/İo) + a2 × [ b1 × (Çn/Ço) + b2 × (Dn/Do) + b3 × (Yn/Yo) + b4 × (Kn/Ko) + b5 × (Mn/Mo) ]
F  = An × B × (Pn − 1)
```

| Sembol | Anlam | Kaynak | Güven |
|---|---|---|---|
| F | fiyat farkı (TL, + ödenir / − kesilir) | hesap | 🟢 |
| An | hakediş dönemi imalat tutarı (sözleşme fiyatlarıyla, KDV hariç); avans ve ihzarat hariç 🟡 | hakediş | 🟢 |
| B | **0,90** sabit katsayı | md.5 | 🟢 |
| a1 | işçilik ağırlığı | idari şartname | 🟢 |
| a2 | malzeme+makine ağırlığı; **a1 + a2 = 1** | idari şartname | 🟢 |
| b1…b5 | çimento · demir-çelik · akaryakıt · kereste · makine ağırlıkları; **Σb = 1** | idari şartname | 🟢 |
| İ | işçilik endeksi | md.5'te tanımlı — 🔴 hangi TÜİK serisi/asgari ücret bazı olduğunu esas metinden teyit | 🔴 |
| Ç | çimento endeksi | TÜİK Yİ-ÜFE alt sektör (çimento/kireç/alçı) 🟡 | 🟡 |
| D | demir-çelik endeksi | Yİ-ÜFE ana metal / demir-çelik 🟡 | 🟡 |
| Y | akaryakıt endeksi | Yİ-ÜFE kok ve rafine petrol ürünleri 🟡 | 🟡 |
| K | kereste endeksi | Yİ-ÜFE ağaç ürünleri 🟡 | 🟡 |
| M | makine endeksi | Yİ-ÜFE makine ve ekipman 🟡 | 🟡 |
| o | ihale tarihi (son teklif verme) ayı endeksi | md.5 | 🟢 |
| n | uygulama ayı (imalatın yapıldığı ay) endeksi | md.5 | 🟢 |

**Genel endeks modeli (md.6):** idari şartnamede ağırlıklar belirtilmemişse Pn = Gn/Go (Yİ-ÜFE genel endeks) 🟡 → `--genel Go Gn`.

## Kurallar

- Katsayı toplamı ≠ 1 → hesap yapma, şartnameyi tekrar oku (script uyarır, 🔴).
- Uygulama ayı endeksi henüz yayımlanmamışsa geçici olarak son yayımlanan ay, sonraki hakedişte düzeltme (md.7 🟡).
- Süre uzatımı verilmişse uzatılan sürede de fiyat farkı; yüklenici kusurlu gecikmede **ihale tarihi ile iş bitim tarihi arasındaki** en düşük/… kural (md.8–9 🔴) — script uygulamaz, uyarı yaz.
- Avans verilmişse An'dan avans mahsubu düşülmez; ancak avans tutarına fiyat farkı ödenmez (md.5 🟡).
- Fiyat farkı KDV matrahına dahildir (hakedişte KDV öncesi eklenir).
- Yeni birim fiyatlı kalemler: fiyat ihale tarihi bazlı belirlenmişse fiyat farkı uygulanır; uygulama ayı bazlıysa uygulanmaz (🟡).
- Anahtar teslim işlerde An = pursantaj ilerlemesine göre dönem tutarı.

## Ek fiyat farkı ve süre uzatımı (2021–2022 düzenlemeleri)

- 4735 sayılı KİSK **geçici md.5** (RG 22/1/2022) ve **geçici md.6** (RG 15/4/2022): belirli tarih aralıklarındaki ihalelerde **ek fiyat farkı**, süre uzatımı, devir/fesih hakları; hesap esasları ayrı BKK/CK ile.
- Bu kart ve script **ek fiyat farkını hesaplamaz** (formül ve aralıklar 🔴). Kullanıcı sorarsa: sözleşme ihale tarihi geçici madde kapsamındaysa "ayrı esaslarla hesaplanır, ilgili CK'yı ekleyin" de.

## Dönem dosyası

`templates/fiyat-farki-donem-sablon.xlsx` — her satır bir hakediş: Hakediş · An · a1 · a2 · b1…b5 · İo · İn · Ço · Çn · Do · Dn · Yo · Yn · Ko · Kn · Mo · Mn · (Go · Gn). Endeks kaynağı (TÜİK tablo adı, yayım tarihi) ayrı notta yazılır; yazılmamışsa 🔴.

## Örnek okuma

`An 1.250.000 · a1 0,35 · a2 0,65 · b 0,30/0,25/0,20/0,10/0,15 · endeksler (temsilî) → Pn 1,1806 → F = 1.250.000 × 0,90 × 0,1806 = 203.231,25 TL (ödenecek)`. Endeksler gerçek değil; hesap yolu doğru.
