# 06 — Rapor Formatı: Bulgu Satırı Anatomisi ve Durum Kodları

> Her bulgu tek satır, altı sütun. Süreç anlatılmaz. "Sonuç önce".

## Bulgu satırı

`<Kod> · <Konu> · <Ölçülen> vs <Gereken> · <Durum> · <Dayanak> <Güven> · <Kaynak> · <Öneri / sorumlu>`

| Sütun | Kural |
|---|---|
| **Kod** | Grup harfi + sıra: `E-3`. Bulgu yoksa `E-0 · kontrol edildi, bulgu yok · U`. |
| **Konu** | Mahal/öğe adı + kat: "M1 ana merdiven, zemin–1. kat". |
| **Ölçülen vs gereken** | Sayı + birim, ikisi de: "rıht 17.5 cm vs ≤16 cm". Ölçülemediyse "ölçülemedi vs ≤16". |
| **Durum** | Aşağıdaki kod. |
| **Dayanak + güven** | Madde/tablo + 🟢🟡🔴. Birden çok katman: en sıkı olan önce: "TS 9111 §4.7.1.3.1 (PAİY md.31/2 ≥27)". |
| **Kaynak** | `yazılı` / `ölçekten ±%3` / `ölçülemedi` / `hesap: kacis_hesabi.py`. |
| **Öneri / sorumlu** | Tek cümle, ne yapılmalı, kim: "(müellif) rıht 15 cm'e çekilip basamak sayısı 30'a çıkarılmalı" · "(idare) yağmurlama kararı yazılı verilmeli". |

## Durum kodları

| Kod | Anlam | Ne zaman |
|---|---|---|
| **U** | Uygun | ölçü elde + norm sağlanıyor |
| **U-S** | Uygun, sınırda | ölçekten ölçüm ve normun ±%3 içinde → "yazılı ölçü istenir" |
| **U-N** | Uygun, not | sağlanıyor ama sapma/verimsizlik (sirkülasyon %78) |
| **UD** | Uygun değil | ölçü elde + norm sağlanmıyor |
| **UD-B** | Uygun değil, bağlayıcı safha | avan'da düzelmezse sonradan düzelmez (İçişleri §B, kat adedi, emsal) |
| **E** | Eksik belge | kontrol yapılamadı, belge yok (tahliye projesi, imar durumu) |
| **Ö** | Ölçülemedi | belge var, ölçü okunamıyor (ölçek yok, taranmış) |
| **NA** | Kapsam dışı / safha dışı | avan projede detay; başka disiplin |
| **P** | Plan notuna bağlı | yönetmelikten sapıyor ama plan notu izin veriyor/verebilir |

**Durum × güven ilişkisi:** UD sadece 🟢 veya 🟡 ile yazılır. 🔴 varsa durum **E** veya **Ö** olur, UD olmaz ("doğrulayamadığına uygun değil deme" de geçerlidir).

## Güven etiketleri

- 🟢 **doğrulandı** — ölçü projede yazılı + madde elde.
- 🟡 **hesaplandı / ölçekten / türetildi** — ±%3 ölçüm, script türevi, ikincil kaynak normu, tipik program değeri.
- 🔴 **teyit gerekli** — madde/tablo elde değil, belge yok, plan–kesit uyuşmazlığı.

## Rapor bölüm sırası

1. **Sonuç paragrafı** (≤5 cümle): "Proje şu N noktada uygun değil: …; şu belgeler eksik: …; en kritik: …" — UD-B'ler önce.
2. **Eksik belgeler ve yapılamayan kontroller** (E satırları).
3. **Pafta envanteri** (FAZ 1 tablosu).
4. **Bulgu tablosu A–N** — grup sırasıyla, grup içinde UD-B → UD → U-S → U-N → E/Ö → U → NA.
5. **Script çıktıları** (özet tablo; JSON ek).
6. **Çapraz doğrulama** (FAZ 4 tablosu).
7. **HK ise:** "İçişleri esaslarına aykırılıklar" ayrı başlık (N ve B/C'den ilgili satırlar tekrar).
8. **Avan ise:** "Uygulama projesinde kontrol edilecekler" listesi (NA satırları).
9. **Kapanış paragrafı** — SKILL.md'deki metin **harfiyen**.

## Üslup

- Her bulgu **Ne + Neden + Nasıl**. "Dikkat edilmeli" gibi eylemsiz öneri yok.
- Maliyet, birim fiyat, oran, ticari şart, "kolayca", "basitçe" yok.
- Sayılar script çıktısından; elle yuvarlama yok. Metinde en fazla iki sayı; gerisi tabloda.
- Türkçe; kısaltmalar ilk geçişte açılır: PAİY (Planlı Alanlar İmar Yönetmeliği), BYKHY, KBS, YGH, HK.

## Örnek satırlar

```
E-1 · M1 ana merdiven rıht, tüm katlar · 17.3 cm vs ≤16 cm · UD · PAİY md.31/2 (umumi) 🟢 · yazılı (kesit A-A) · (müellif) rıht 15 cm, kat başı 30 basamak, 2a+b = 59 → basamak 29'a çıkar
J-2 · 1. kat tek yönlü kaçış · 19 m vs ≤15 m (yağmurlamasız) · E · BYKHY Ek-5/B 🔴 · ölçekten ±%3 · (idare) yağmurlama kararı yazılı verilirse sınır 30 m; verilmezse ikinci çıkış (müellif)
N-1 · Makam katı konumu · zemin+3 vs ≤ zemin+2 · UD-B · İçişleri §B 🟢 · yazılı (kesit) · (müellif) makam katı 2. kata; 3. kat kaldırılır veya plan Hmax ile tekrar değerlendirilir
I-4 · Sirkülasyon oranı · %38 vs ≈%60 · U-N · KBS §4.7 🟡 · cetvel · (müellif) cetvelde koridorlar hangi kaleme yazıldı? m² cetveli mahal bazlı yeniden verilmeli
```
