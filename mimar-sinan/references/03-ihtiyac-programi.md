# 03 — İhtiyaç Programı Üretimi (Mod 2)

> Girdi: kadro/birim listesi. Çıktı: mahal bazlı net m² tablosu + sirkülasyon + teknik + toplam inşaat (🟡). Araç: `scripts/ihtiyac_programi.py`.
> **Sınıf-başı hükümet konağı toplam m²'si asla verilmez** — İçişleri'nden teyit. KBS §5 boş.

## Adımlar

1. **Kadro topla** — birim × (makam / müdür / şube müd. / masa başı / hareketli). Boş kadro dahil; büyüme payı %10–15 (idare kararı, 🟡).
2. **Ortak alanlar** — toplantı kişi, konferans kişi, anlık bekleme (vatandaş yoğun birimlerde günlük başvuru ÷ 8 saat × ortalama bekleme saati; yoksa çalışan × 0.5 🟡).
3. **Script çalıştır** → mahal tablosu.
4. **Mahal bazında düzenle** — birim birim grupla; makam katı, vatandaş katı (zemin), personel katları.
5. **Eklenecek sabitler (script vermez):** sistem odası 12–25 · çay ocağı kat başı 6–9 · temizlik kat başı 4 · arşiv (dosya metrajından) · mescit · yemekhane (seans) · güvenlik/danışma 12–15 · kreş (karar) · nikâh salonu (kaymakamlık, karar) · şeref salonu (HK). Hepsi 🟡/🔴, kart 02 §4.5.
6. **Toplam** = çalışma + ortak + sirkülasyon(%60) + teknik(%4) → `🟡 türetildi`.
7. **Bodrum ekleri (emsal dışı):** sığınak (kart 06 hesabı), otopark, teknik — toplam inşaata **eklenir**, emsale **girmez**; ayrı satır.

## Formüller

```
çalışma        = Σ makam + Σ müdür + Σ şube×12 + Σ masa×9 + Σ hareketli×6
ortak          = toplantı×1.5 + konferans×(1.0|1.5) + bekleme×3 + WC + eklenen sabitler
WC grubu adedi = ceil((çalışan + bekleme) / 50)      # PAİY md.48
erişilebilir WC= 2 (K+E) × 5.5 m²                     # 🟡
sirkülasyon    = (çalışma + ortak) × 0.60             # KBS §4.7
net toplam     = çalışma + ortak + sirkülasyon
teknik         = net toplam × 0.04 / 0.96             # KBS §4.8 (toplamın %4'ü)
inşaat (emsal) = net toplam + teknik                   # 🟡
+ bodrum       = sığınak + otopark + ek teknik          # emsal dışı
```

## JSON girdi şeması

```json
{
  "yapi": "kaymakamlik",
  "birimler": [
    {"ad": "Kaymakamlık Makamı", "makam": "kaymakam", "masa_basi": 2, "hareketli": 1},
    {"ad": "Yazı İşleri Müdürlüğü", "mudur": "ilce_mudur", "sube_mudur": 1, "masa_basi": 6, "hareketli": 1}
  ],
  "toplanti_kisi": 40, "konferans_kisi": 0, "bekleme_kisi": 30
}
```
`makam`/`mudur` anahtarları: `vali · vali_yrd · il_mudur · kaymakam · ilce_mudur`.

## Çıktı tablosu formatı

| Kat | Birim | Mahal | Adet | Kişi başı | Net m² | Dayanak | Güven |
|---|---|---|---|---|---|---|---|

+ özet: çalışma / ortak / sirkülasyon / teknik / **emsal inşaat** / bodrum ekleri / **toplam inşaat** — her satır dayanaklı.

## Tipik kaymakamlık birimleri (kontrol listesi, 🟡)

Kaymakamlık makamı · Yazı İşleri · İlçe Nüfus · Mal Müdürlüğü · SYDV · İlçe Tarım (varsa) · İlçe Milli Eğitim (genelde ayrı bina) · Tapu (varsa) · İlçe Müftülüğü (genelde ayrı) · Seçim Kurulu (dönemsel oda) · Nikâh salonu (karar) · Toplantı salonu · Arşiv · Sığınak · Teknik. Hangilerinin HK içinde olacağı **idare kararı** — sor, varsayma.

## Rapor dili

"Bu program KBS §4.3–4.8 normlarından türetilmiştir; İçişleri sınıf-başı m² değeri elde olmadığından toplam **yol gösterici**dir (🟡). Makam odaları İçişleri §A'dan sabittir (🟢)."
