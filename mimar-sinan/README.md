# mimar-sinan

Kamu yapıları için mevzuat-atıflı mimari proje denetimi ve m² ihtiyaç programı üretimi.

## Ne yapar
- Proje PDF'ini PAİY, Kamu Binaları Standartları (2018/9), BYKHY, TS 9111, Otopark ve Sığınak Yönetmeliği'ne karşı madde atıflı kontrol eder
- Hükümet konağı / kaymakamlık için İçişleri esaslarını bağlayıcı uygular
- Kadro listesinden ihtiyaç programı (m²) türetir
- Kaçış, merdiven, otopark ve sığınak hesaplarını bağımsız Python araçlarıyla yapar

## Araçlar (stdlib-only, JSON çıktı)
| Araç | İş |
|---|---|
| `scripts/kacis_hesabi.py` | Kullanıcı yükü + kaçış genişliği/uzaklığı (BYKHY Ek-5, md.32) |
| `scripts/merdiven_kontrol.py` | Rıht, basamak, 2a+b, kol genişliği (PAİY md.31 · TS 9111) |
| `scripts/otopark_siginak_hesabi.py` | Araç adedi, engelli oranı, sığınak kişi/m² |
| `scripts/ihtiyac_programi.py` | Kadro → mahal bazlı m² programı (KBS §4.3–4.8) |

Hepsi argümansız çalıştığında gömülü örnekle demo yapar:
```
python3 scripts/merdiven_kontrol.py --kat-yuksekligi 450 --basamak 29 --rih 15.52 --kol 150
```

## Kurulum
**Claude Code:**
```
/plugin marketplace add damnali17-ops/mimar-skills
/plugin install mimar-sinan@mimar-skills
```
**Elle:** `mimar-sinan/` klasörünü `~/.claude/skills/` altına kopyala.

## Referans kartları
`references/` klasörü mevzuat özet kartlarını tutar — bkz. `references/README.md`.
