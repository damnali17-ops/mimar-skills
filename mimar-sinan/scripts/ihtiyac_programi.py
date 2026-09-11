#!/usr/bin/env python3
"""İhtiyaç programı (m²) üretici — Kamu Binaları Standartları 2018/9 §4.3–4.8 + İçişleri HK Esasları §A.

Kullanım:
  python3 ihtiyac_programi.py                     # örnek kaymakamlık
  python3 ihtiyac_programi.py kadro.json

Girdi JSON:
{
  "yapi": "kaymakamlik",
  "birimler": [
    {"ad": "Kaymakamlık Makamı", "makam": "kaymakam", "masa_basi": 2, "hareketli": 1},
    {"ad": "Yazı İşleri Müd.",  "mudur": "ilce_mudur", "masa_basi": 6, "hareketli": 0, "sube_mudur": 1},
    ...
  ],
  "toplanti_kisi": 40, "konferans_kisi": 0, "bekleme_kisi": 30
}
Çıktı: mahal bazlı m² tablosu + sirkülasyon (%60) + teknik pay (%4) + toplam. 🟡 = normdan türetilmiş.
KBS §5 brüt alan tablosu boş olduğundan TOPLAM her zaman 🟡 türetilmiştir.
"""
import json
import math
import sys

MASA_BASI = 9.0        # KBS §4.3 m²/kişi (azami)
HAREKETLI = 6.0        # KBS §4.3
SUBE_MUDUR = 12.0      # KBS §4.3 (+12 m² toplantı köşesi opsiyonel)
UST_YONETICI = 90.0    # KBS §4.3 80–100 → orta değer
TOPLANTI_KISI = 1.50   # KBS §4.4 (konferans 1.50; toplantı 2.00/1.50/1.00 kademeli → 1.50 orta)
BEKLEME_KISI = 3.0     # BYKHY Ek-5/A ile uyumlu, KBS bekleme normu — 🟡
SIRKULASYON = 0.60     # KBS §4.7
TEKNIK = 0.04          # KBS §4.8 (inşaat alanı üzerinden)
MAKAM = {              # İçişleri HK Esasları §A
    "vali": 80, "vali_yrd": 40, "il_mudur": 35, "kaymakam": 60, "ilce_mudur": 24,
}
WC_KISI = 50           # PAİY md.48 — her 50 kişiye 1
WC_BIRIM_M2 = 4.0      # 🟡 varsayım: 1 kabin + lavabo payı
WC_ERISILEBILIR_M2 = 5.5  # TS 9111 §4.7.3 kabin 150×150 + manevra — 🟡

ORNEK = {
    "yapi": "kaymakamlik",
    "birimler": [
        {"ad": "Kaymakamlık Makamı", "makam": "kaymakam", "masa_basi": 2, "hareketli": 1},
        {"ad": "Yazı İşleri Müdürlüğü", "mudur": "ilce_mudur", "sube_mudur": 1, "masa_basi": 6, "hareketli": 1},
        {"ad": "İlçe Nüfus Müdürlüğü", "mudur": "ilce_mudur", "masa_basi": 8, "hareketli": 2},
        {"ad": "Mal Müdürlüğü", "mudur": "ilce_mudur", "masa_basi": 10, "hareketli": 1},
        {"ad": "Sosyal Yardımlaşma Vakfı", "mudur": "ilce_mudur", "masa_basi": 5, "hareketli": 2},
    ],
    "toplanti_kisi": 40, "konferans_kisi": 0, "bekleme_kisi": 30,
}


def uret(v):
    satirlar, calisan = [], 0

    def ekle(mahal, adet, birim, m2, dayanak, guven="🟢"):
        satirlar.append({"mahal": mahal, "adet": adet, "birim_m2": birim, "m2": round(m2, 1),
                         "dayanak": dayanak, "guven": guven})

    for b in v["birimler"]:
        if b.get("makam"):
            ekle(f"{b['ad']} — makam odası", 1, MAKAM[b["makam"]], MAKAM[b["makam"]], "İçişleri HK Esasları §A")
            calisan += 1
        if b.get("mudur"):
            ekle(f"{b['ad']} — müdür odası", 1, MAKAM[b["mudur"]], MAKAM[b["mudur"]], "İçişleri HK Esasları §A")
            calisan += 1
        if b.get("sube_mudur"):
            ekle(f"{b['ad']} — şube müdürü", b["sube_mudur"], SUBE_MUDUR, b["sube_mudur"] * SUBE_MUDUR, "KBS §4.3")
            calisan += b["sube_mudur"]
        if b.get("masa_basi"):
            ekle(f"{b['ad']} — masa başı personel", b["masa_basi"], MASA_BASI, b["masa_basi"] * MASA_BASI, "KBS §4.3 (azami 9 m²/kişi)")
            calisan += b["masa_basi"]
        if b.get("hareketli"):
            ekle(f"{b['ad']} — hareketli personel", b["hareketli"], HAREKETLI, b["hareketli"] * HAREKETLI, "KBS §4.3 (azami 6 m²/kişi)")
            calisan += b["hareketli"]

    calisma = sum(s["m2"] for s in satirlar)
    ortak = []
    if v.get("toplanti_kisi"):
        ortak.append(("Toplantı salonu", v["toplanti_kisi"], TOPLANTI_KISI, "KBS §4.4", "🟢"))
    if v.get("konferans_kisi"):
        ortak.append(("Konferans salonu", v["konferans_kisi"], TOPLANTI_KISI, "KBS §4.4", "🟢"))
    if v.get("bekleme_kisi"):
        ortak.append(("Vatandaş bekleme", v["bekleme_kisi"], BEKLEME_KISI, "KBS bekleme normu / BYKHY Ek-5/A", "🟡"))
    kullanici = calisan + int(v.get("bekleme_kisi", 0))
    wc = math.ceil(kullanici / WC_KISI)
    ortak.append(("WC grubu (K/E)", wc, WC_BIRIM_M2 * 2, "PAİY md.48 — her 50 kişiye 1", "🟡"))
    ortak.append(("Erişilebilir WC (K+E)", 2, WC_ERISILEBILIR_M2, "PAİY md.48 · TS 9111 §4.7.3", "🟡"))
    for ad, adet, birim, day, g in ortak:
        ekle(ad, adet, birim, adet * birim, day, g)
    ortak_m2 = sum(s["m2"] for s in satirlar) - calisma

    sirk = (calisma + ortak_m2) * SIRKULASYON
    net_toplam = calisma + ortak_m2 + sirk
    teknik = net_toplam * TEKNIK / (1 - TEKNIK)
    insaat = net_toplam + teknik

    return {
        "yapi": v.get("yapi"), "calisan_sayisi": calisan,
        "mahaller": satirlar,
        "ozet": {
            "calisma_alani_m2": round(calisma, 1),
            "ortak_alan_m2": round(ortak_m2, 1),
            "sirkulasyon_m2": round(sirk, 1), "sirkulasyon_dayanak": "KBS §4.7 — (çalışma+ortak) × %60",
            "teknik_m2": round(teknik, 1), "teknik_dayanak": "KBS §4.8 — ≤ inşaat alanının %4",
            "toplam_insaat_m2": round(insaat, 1),
            "toplam_guven": "🟡 KBS §5 brüt alan tablosu boş — kişi başı normlardan türetildi",
        },
        "not": "Hükümet konağı sınıf-başı toplam m² İçişleri'nden teyit edilmeli. Ön-değerlendirmedir.",
    }


def ozet(s):
    print(f"\nİHTİYAÇ PROGRAMI — {s['yapi']}  ({s['calisan_sayisi']} çalışan)")
    print("-" * 84)
    for m in s["mahaller"]:
        print(f"  {m['guven']} {m['mahal']:<44} {m['adet']:>3} × {m['birim_m2']:>5}  = {m['m2']:>7.1f} m²   {m['dayanak']}")
    o = s["ozet"]
    print("-" * 84)
    print(f"  Çalışma alanı      {o['calisma_alani_m2']:>8.1f} m²")
    print(f"  Ortak alan         {o['ortak_alan_m2']:>8.1f} m²")
    print(f"  Sirkülasyon (%60)  {o['sirkulasyon_m2']:>8.1f} m²   {o['sirkulasyon_dayanak']}")
    print(f"  Teknik (%4)        {o['teknik_m2']:>8.1f} m²   {o['teknik_dayanak']}")
    print(f"  TOPLAM İNŞAAT      {o['toplam_insaat_m2']:>8.1f} m²   {o['toplam_guven']}")
    print("\n" + s["not"])


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__); return
    if len(sys.argv) > 1:
        v = json.load(sys.stdin) if sys.argv[1] == "-" else json.load(open(sys.argv[1], encoding="utf-8"))
    else:
        print("(örnek kaymakamlık kadrosuyla çalışıyor)")
        v = ORNEK
    s = uret(v)
    print(json.dumps(s, ensure_ascii=False, indent=2))
    ozet(s)


if __name__ == "__main__":
    main()
