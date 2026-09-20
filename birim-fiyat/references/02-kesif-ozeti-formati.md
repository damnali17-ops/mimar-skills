# 02 — Keşif Özeti (Yaklaşık Maliyet) Formatı

> Araç: `scripts/kesif_ozeti.py`. Çıktı 4 sayfa: **Keşif Özeti · İş Grupları · Eşleşmeyen · Özet**. Bu kart kolonların anlamını, iş grubu mantığını ve icmal kurallarını verir.

## Keşif Özeti sayfası — kolonlar

| Kolon | İçerik | Kural |
|---|---|---|
| Sıra | metraj sırası | değişmez, izlenebilirlik |
| İş Grubu | metrajdan; yoksa poz bölümü (`Bölüm Y.16`) | anahtar teslimde pursantaj tabanı |
| Poz No | metrajdaki poz | listeyle **tam** eşleşme; eşleşmeyen ayrı sayfa |
| Tanım | listedeki tarif (metrajdaki değil) | listenin tarifi resmî |
| Birim | listedeki birim | metraj birimi farklıysa 🟡 + kaynak notu |
| Miktar | metrajdan, 2 ondalık | çevrim yapılmaz, kullanıcı çevirir |
| Birim Fiyat | listeden × (1 + kâr%) | ÇŞB → kâr 0 |
| Tutar | formül `=F*G` + önbellek | 2 ondalık |
| Kaynak | "ÇŞB 2026", "teklif", "KGM 2026" | yıl zorunlu |
| Güven | 🟢 listeden · 🟡 birim farkı / güncelleme · (🔴 satır yazılmaz, Eşleşmeyen'e gider) | |

Alt satırlar: TOPLAM (KDV hariç) → KDV %x → GENEL TOPLAM. KDV verilmemişse satır yok, Özet'te "— (oran verilmedi)".

## İş grupları

- **Birim fiyatlı sözleşme:** iş grubu bilgi amaçlı (dağılım, kontrol).
- **Anahtar teslim götürü bedel:** iş grupları **pursantaj** (ilerleme yüzdesi) tabanıdır; hakediş bu oranlarla yapılır → grup tanımı sözleşme ekindeki iş grupları listesiyle birebir olmalı (🟡).
- Tipik ana gruplar: **İnşaat · Mekanik tesisat · Elektrik tesisatı** (+ altyapı/çevre düzenleme). İnşaat alt grupları: kazı-dolgu, betonarme (beton+kalıp+demir), duvar, çatı, yalıtım, sıva-şap, kaplama, doğrama, boya, peyzaj (🟡, idare şablonu varsa o).
- Mekanik ve elektrik keşifleri ayrı listelerden; icmalde ayrı satır.

## İcmal (yaklaşık maliyet icmali)

```
İnşaat işleri            Σ
Mekanik tesisat          Σ
Elektrik tesisatı        Σ
Altyapı / çevre          Σ
-------------------------------
Toplam (KDV hariç)       Σ        ← yaklaşık maliyet (ihale eşiği bununla)
KDV                      (oran kullanıcı)
Genel toplam
```
Yaklaşık maliyet **KDV hariç** tutar üzerinden belirlenir (YİİUY md.10 🟡); eşik değer ve ilan kuralları bu tutara göre.

## Fiyat güncelleme (YİİUY md.11)

- Birim fiyatın yayım yılı ile ihale tarihi arasında **12 aydan fazla** varsa güncelleme (Yİ-ÜFE genel endeks) 🟡.
- Script güncelleme **yapmaz**; kullanıcı liste yılını verir, skill "güncelleme gerekir" uyarısı + keşfi 🟡 etiketler. Güncelleme katsayısı kullanıcıdan (endeks n / endeks o).

## Gizlilik ve teslim

- Yaklaşık maliyet ihale ilanına kadar gizli; ilanda/ihale dokümanında **yer almaz** (YİİUY md.9). Özet sayfasına not düşülür.
- Yaklaşık maliyet komisyonu tutanağı: hesap cetveli + icmal + fiyat kaynakları listesi + varsa analizler + güncelleme hesabı. Keşif özeti bu tutanağın ekidir; imza/onay idarenin.

## Metraj–keşif tutarlılığı (kontrol listesi)

- [ ] Her metraj satırının pozu var ve listede tam eşleşiyor
- [ ] Birimler eşit (ton/kg, m²/m³, adet/takım)
- [ ] Miktar 0 veya negatif satır yok
- [ ] Aynı poz iki kez → birleştirildi mi, bilinçli mi (farklı iş grubu)?
- [ ] Liste yılı = ihale yılı; değilse güncelleme notu
- [ ] ÇŞB pozuna %25 eklenmedi; özel poza eklendi
- [ ] Mekanik/elektrik ayrı listede
- [ ] Toplam 🟢 (eşleşmeyen yok)
