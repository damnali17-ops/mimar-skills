# 04 — Hakediş: Süreç, Kesintiler, İş Artışı

> Araç: `scripts/hakedis.py`. Dayanak: Yapım İşleri Genel Şartnamesi (YİGŞ, RG 9/10/2003 – 25254, değişiklikleriyle) md.39 (geçici hakedişler), md.40 (kesin hakediş), md.21–22 (iş artışı/eksilişi, yeni birim fiyat); 4735 sayılı Kamu İhale Sözleşmeleri Kanunu md.24 (iş artışı sınırı). Madde numaraları 🟡 — güncel YİGŞ metniyle teyit.

## Geçici (ara) hakediş mantığı — YİGŞ md.39

1. **Metraj:** işin başından hakediş dönemi sonuna kadar yapılan **kümülatif** miktar, kontrol teşkilatı ile birlikte ölçülür; ataşman/röleve/yeşil defter dayanaklı.
2. **Kümülatif imalat tutarı** = Σ kümülatif miktar × **sözleşme birim fiyatı** (birim fiyatlı) veya Σ iş grubu pursantajı × sözleşme bedeli (anahtar teslim).
3. **Bu hakediş** = kümülatif − önceki hakedişler kümülatifi.
4. + fiyat farkı (kart 05) · + ihzarat (sözleşmede varsa 🟡) · − avans mahsubu · − ceza · − diğer kesintiler → KDV → damga vergisi, stopaj → **ödenecek**.
5. Aylık düzenlenir (sözleşme farklı süre verebilir); yüklenici imzalamazsa idarece tek taraflı; itiraz şerhi 🟡.

## Kesintiler ve oranlar (kullanıcı girer, skill varsaymaz)

| Kalem | Uygulama | Not | Güven |
|---|---|---|---|
| KDV | KDV matrahı (brüt − mahsup/ceza) × oran | genel oran; istisna/tevkifat sözleşmeye göre | 🟡 |
| Damga vergisi | hakediş tutarı (KDV hariç) × binde 9,48 | DVK (1) sayılı tablo — her hakedişte | 🟡 |
| Gelir/kurumlar vergisi stopajı | yıllara sâri inşaat/onarım işlerinde hakedişten kesinti; oran güncel GVK md.94 | 2024'te oran değişti — kullanıcı teyit eder | 🟡 |
| Avans mahsubu | avans tutarı × (bu hakediş imalatı / kalan iş) veya sözleşmedeki oran | sözleşme md. 🟡 | 🟡 |
| Gecikme cezası | sözleşmede günlük oran (binde x) × gecikme günü | süre uzatımı varsa uygulanmaz | 🟢 |
| Kesin teminat | sözleşme bedelinin %6'sı sözleşme imzasında; hakedişten kesinti **yoktur** (eski uygulama %10 teminat kesintisi kalktı 🟡) | iş artışında ek kesin teminat | 🟡 |
| SGK ilişiksizlik | kesin hakediş/kesin teminat iadesi için gerekli; ara hakedişten kesinti değil | | 🟡 |

## İş artışı / eksilişi — KİSK md.24, YİGŞ md.21

| Sözleşme türü | Sınır | Aşılırsa |
|---|---|---|
| Anahtar teslim götürü bedel | sözleşme bedelinin **%10**'u | tasfiye veya idare kararı; ek sözleşme |
| Birim fiyatlı | **%20** | aynı |
| Karma | ilgili kısım kendi oranı | |

- Şartlar: öngörülemeyen durum, sözleşme kapsamında, aynı yüklenici, ihale dokümanı değişmeden.
- Script: kalem bazında kümülatif > sözleşme miktarı → 🟡 satır; toplam > bedel × (1 + sınır) → 🔴 "onay olmadan ödenemez".
- Sözleşmede olmayan imalat → **yeni birim fiyat** (YİGŞ md.22, kart 03 §2); tutanak onaylanmadan hakedişe girmez → script "listede yok, tutara alınmadı" uyarısı.

## Kesin hakediş — YİGŞ md.40

- Geçici kabulden sonra; kesin metraj + kesin hesap; tüm geçici hakedişler düşülür.
- Kesin hakediş = kesin kabul tutanağı + SGK ilişiksizlik + kesin teminat iadesi zinciriyle bağlı (🟡).
- Script kesin hakedişi "son geçici hakediş + kesin metraj farkı" olarak modeller; kesin hesap cetvelini kullanıcı kontrol eder.

## Anahtar teslim işlerde pursantaj

- Hakediş = Σ (iş grubu pursantajı × gerçekleşme %) × sözleşme bedeli.
- Metraj yerine iş grubu ilerleme yüzdesi girilir; `hakedis.py` için "Sözleşme Miktarı = pursantaj %, Sözleşme BF = sözleşme bedeli/100, Kümülatif Miktar = gerçekleşen %" olarak uyarlanır (🟡 — açıkça belirt).

## Çıktı kontrol listesi

- [ ] Kümülatif ≥ önceki hakediş kümülatifi (negatif imalat yok)
- [ ] Sözleşme birim fiyatı kullanıldı (güncel liste değil)
- [ ] İş artışı sınırı kontrol edildi
- [ ] Fiyat farkı ayrı satır, kaynağı `fiyat_farki.xlsx`
- [ ] Oranlar (KDV/damga/stopaj) sözleşme/mevzuattan; 0 ise "verilmedi" notu
- [ ] Ödenecek tutar KDV dahil/hariç açıkça yazılı
