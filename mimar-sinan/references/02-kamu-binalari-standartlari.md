# 02 — Kamu Binaları Standartları Rehberi (2018/9 Genelge)

> Kapsam: merkezî idare, bağlı-ilgili-ilişkili kuruluşlar ve mahalli idarelerin **idari hizmet binaları**. Eğitim/sağlık/adliye salon-koğuş-derslik gibi özel mahaller kapsam dışı; onların idari bölümü kapsamda.
> Rehberdeki değerler **azami**dir: altına inmek uygundur, üstüne çıkmak bulgudur. Rapor dili: "KBS §4.3 azami 9 m²/kişi; projede 13.5 m²/kişi → aşım".

## §4.3 — Çalışma alanları (kişi başı net m²)

| Kullanıcı | Norm | Not | Güven |
|---|---|---|---|
| Masa başı personel (memur, uzman, şef) | **≤9 m²/kişi** | açık ofis veya oda; masa + dolap + geçiş | 🟢 |
| Hareketli personel (saha, koruma, destek, şoför) | **≤6 m²/kişi** | masaya sürekli bağlı değil | 🟢 |
| Şube müdürü / birim amiri | **12 m²** (+12 m² toplantı köşesi opsiyonel) | toplantı köşesi eklenirse 24 m² azami | 🟢 |
| Daire başkanı / il müdürü seviyesi | 20–30 m² | 🔴 — §4.3 alt bentleri teyit; HK'da İçişleri §A geçerli (İl Müd. 35) | 🔴 |
| Genel müdür / üst yönetici | **80–100 m²** (sekreterlik, bekleme, toplantı köşesi dahil) | script orta değer 90 alır | 🟢 |
| Sekreterlik | 9–12 m² | 🟡 |
| Çağrı merkezi / operatör | 4–5 m²/kişi | 🔴 |

**Kişi sayısı kaynağı:** onaylı kadro/norm kadro + **%10–15 büyüme payı** (rehber büyüme payını kabul eder; oranı idare belirler — 🟡). Boş kadro ve hizmet alımı personeli sayıma dahil.

## §4.4 — Toplantı, konferans, eğitim

| Mahal | Norm | Güven |
|---|---|---|
| Toplantı odası (küçük, ≤10 kişi) | **2.00 m²/kişi** | 🟢 |
| Toplantı salonu (orta, 10–30) | **1.50 m²/kişi** | 🟢 |
| Toplantı/konferans salonu (büyük, >30) | **1.00 m²/kişi** (sıralı sabit koltuk) | 🟢 |
| Konferans salonu — script sabiti | 1.50 m²/kişi (orta değer; sabit koltuklu ise 1.00 uygula) | 🟡 |
| Eğitim/seminer salonu | 1.50–2.00 m²/kişi (masalı) | 🟡 |
| Fuaye | salon alanının %25–30 | 🔴 |

Bir binada her birime toplantı odası verilmez; **paylaşımlı toplantı havuzu** esastır (rehber ilkesi). Toplantı odası sayısı > birim sayısı → bulgu.

## §4.5–4.6 — Ortak ve destek alanları

| Mahal | Norm | Güven |
|---|---|---|
| Vatandaş bekleme (hizmet alan birim) | **3 m²/kişi** (anlık bekleyen) — BYKHY Ek-5/A ile uyumlu | 🟡 |
| Danışma / güvenlik / turnike holü | giriş holü içinde; giriş koridoru ≥2.20 (PAİY md.30) | 🟢 |
| Arşiv (birim) | 30 m²/kişi kullanıcı yükü (BYKHY); alan: dosya metrajından, raf 0.4 m²/raf-m | 🔴 — dosya envanteri iste |
| Arşiv (kurum, bodrum) | net taşıyıcı yükü ≥7.5 kN/m² (statik proje notu) | 🟡 |
| Yemekhane / kafeterya | 1.5 m²/kişi oturan; 2–3 seans ile çalışan ÷ seans | 🟡 |
| Mescit | çalışan sayısının %10–20'si × 1 m² | 🔴 |
| Kreş | kurum kararı; kapsam dışı standart (ASPB) | 🔴 |
| Sistem odası | 12–25 m²; klimalı, yükseltilmiş döşeme | 🟡 |
| Çay ocağı | kat başına 6–9 m² | 🟡 |
| Temizlik odası | kat başına ≥4 m² | 🟡 |

## §4.7 — Sirkülasyon

**Sirkülasyon alanı = (çalışma alanı + ortak alan) × %60** — koridor, hol, merdiven, asansör, YGH, giriş.

Yorum: rehber oranı **üst sınır** verir; %60'ın **belirgin altı** (≤%40) genelde m² cetvelinde koridorların başka kaleme yazıldığını, **belirgin üstü** (≥%75) plan verimsizliğini gösterir. İkisi de bulgudur (kart 06-rapor-formati durum kodu **U-N** not).

## §4.8 — Teknik alanlar

**Teknik alan ≤ toplam inşaat alanının %4** — kazan/ısı merkezi, trafo/jeneratör, su deposu/hidrofor, havalandırma, asansör makine dairesi, elektrik odaları. Sığınak ve otopark **bu %4'e dahil değil**.

Script formülü: teknik = net_toplam × 0.04 / (1 − 0.04) → toplam inşaat içinde tam %4.

## §5 — Kapalı brüt inşaat alanı tablosu

**Yayımlanan PDF'te boş.** Bina türü × personel sayısı → toplam m² tablosu verilmemiştir. Toplam istenirse §4.3–4.8 normlarından türet, `🟡 türetildi` etiketle, `scripts/ihtiyac_programi.py` çıktısını göm. **Asla sabit bir "kaymakamlık X m²" değeri verme.**

## Alan hesabı kuralları (rehber §3 tanımlar)

- **Net alan:** duvar içi kullanılabilir alan; kolon ve tesisat şaftı düşülür.
- **Brüt kat alanı:** dış duvar dış yüzünden.
- **Toplam inşaat alanı:** tüm katların brüt toplamı (bodrum dahil, açık teras/balkon %50 — 🟡 PAİY md.5 ile uyumlu okuyun).
- Norm kontrolü **net** alan üzerinden yapılır; m² cetveli brüt veriyorsa %12–15 duvar payı düşülerek 🟡 hesaplanır — kaynak belirt.

## Sık hatalar

1. Kişi başı 9 m²'yi "asgari" sanıp 7 m²'lik açık ofise bulgu yazmak → uygun, bulgu değil.
2. Makam odalarını KBS'den almak (HK'da İçişleri §A).
3. Toplantı odasını her birime vermek.
4. Sirkülasyonu çalışma alanına gömüp cetvelde %35 göstermek.
5. Toplam m²'yi KBS'den "çıkmış gibi" vermek — §5 boş.
