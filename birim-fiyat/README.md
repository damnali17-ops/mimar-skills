# birim-fiyat

Kamu yapım işleri için keşif (yaklaşık maliyet), poz eşleştirme, fiyat analizi, hakediş ve fiyat farkı hesabı. Excel girer, Excel çıkar.

## Ne yapar
- Kullanıcının verdiği poz listesinde (ÇŞB, KGM, DSİ, İLBANK, sözleşme) tarif → poz eşleştirir
- Metrajı listeyle fiyatlandırıp keşif özeti (iş grupları, KDV, eşleşmeyenler) üretir
- Rayiç + işçilik + makine + nakliye girdilerinden analiz ve özel poz (ÖBF) birim fiyatı çıkarır
- Sözleşme + kümülatif metrajdan hakediş icmali (imalat, fiyat farkı, kesintiler, KDV, ödenecek) düzenler
- 2013/5217 esaslarına göre Pn ve fiyat farkı hesaplar

**Skill fiyat, rayiç veya endeks değeri içermez.** Her sayı kullanıcının listesinden gelir, kaynağı ve yılı çıktıya yazılır.

## Araçlar (stdlib-only, xlsx okur/yazar, JSON + özet basar)
| Araç | İş |
|---|---|
| `scripts/poz_bul.py` | Tarif → poz (Türkçe normalizasyon, eş anlamlı, sayısal terim uyumu); toplu eşleştirme |
| `scripts/kesif_ozeti.py` | Metraj × liste → keşif özeti xlsx (formüllü) |
| `scripts/fiyat_analizi.py` | Girdi kalemleri → analiz toplamı + %25 → birim fiyat |
| `scripts/hakedis.py` | Kümülatif hakediş + icmal + iş artışı uyarıları |
| `scripts/fiyat_farki.py` | Pn, F = An × 0,90 × (Pn − 1); dönem dosyası desteği |
| `scripts/xlsx_io.py` | openpyxl gerektirmeyen xlsx/csv okuma-yazma |

Hepsi `--ornek` ile gömülü (gerçek olmayan) veriyle demo yapar:
```
python3 scripts/kesif_ozeti.py --ornek --kdv 20
python3 scripts/fiyat_farki.py --an 1250000 --a1 0.35 --a2 0.65 --b 0.30,0.25,0.20,0.10,0.15 --io 100 --in 118 --co 100 --cn 121 --do 100 --dn 109 --yo 100 --yn 132 --ko 100 --kn 115 --mo 100 --mn 111
```

## Kurulum
```
/plugin marketplace add damnali17-ops/mimar-skills
/plugin install birim-fiyat@mimar-skills
```
**Elle:** `birim-fiyat/` klasörünü `~/.claude/skills/` altına kopyala.

## Şablonlar
`templates/` — birim fiyat listesi, metraj, analiz, hakediş (sözleşme + metraj), fiyat farkı dönem tablosu. Kolon adları esnek; eş anlamlılar `references/06-veri-formati.md`.
