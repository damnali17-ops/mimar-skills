#!/usr/bin/env python3
"""Kullanıcı yükü ve kaçış genişliği hesabı — BYKHY Ek-5/A + md.32.

Kullanım:
  python3 kacis_hesabi.py                      # gömülü örnek veriyle çalışır
  python3 kacis_hesabi.py girdi.json           # dosyadan
  echo '{...}' | python3 kacis_hesabi.py -     # stdin'den

Girdi JSON şeması:
{
  "yagmurlama": false,
  "katlar": [
    {"kat": "Zemin",
     "mahaller": [{"ad": "Bürolar", "tur": "ofis", "alan_m2": 420},
                  {"ad": "Bekleme", "tur": "bekleme", "alan_m2": 60}],
     "kapi_genislik_cm": [90, 90, 120],
     "merdiven_genislik_cm": [150, 150],
     "tek_yon_kacis_m": 12, "iki_yon_kacis_m": 38}
  ]
}
Çıktı: JSON + okunabilir özet. Her satır dayanak maddesi taşır.
"""
import json
import math
import sys

# BYKHY Ek-5/A — kullanıcı yükü katsayıları (m²/kişi). Sadece elde olanlar.
KULLANICI_YUKU = {
    "ofis": 10.0,
    "bekleme": 3.0,
    "salon": 1.5,          # toplantı/konferans, sandalyesiz
    "arsiv": 30.0,
    "yemekhane": 1.5,
}
BIRIM_GENISLIK_CM = 50          # BYKHY md.32 — 1 birim = 50 cm
KAPI_BIRIM_KISI = 100           # md.32 — kapı/koridor birim kişi
MERDIVEN_BIRIM_KISI = 60        # md.32 — merdiven birim kişi
MIN_KAPI_NET_CM = 90            # TS 9111 §4.6.2 (erişilebilirlik) — PAİY 80
MIN_MERDIVEN_KAMU_CM = 150      # PAİY md.31/1-a
KACIS_UZAKLIK = {               # BYKHY Ek-5/B, büro
    "tek_yon": {False: 15, True: 30},
    "iki_yon": {False: 45, True: 75},
}

ORNEK = {
    "yagmurlama": False,
    "katlar": [
        {"kat": "Zemin", "mahaller": [
            {"ad": "Nüfus / vergi bürosu", "tur": "ofis", "alan_m2": 380},
            {"ad": "Vatandaş bekleme", "tur": "bekleme", "alan_m2": 70}],
         "kapi_genislik_cm": [120, 90], "merdiven_genislik_cm": [150, 150],
         "tek_yon_kacis_m": 14, "iki_yon_kacis_m": 41},
        {"kat": "1. Kat", "mahaller": [
            {"ad": "Bürolar", "tur": "ofis", "alan_m2": 520},
            {"ad": "Toplantı salonu", "tur": "salon", "alan_m2": 60}],
         "kapi_genislik_cm": [90], "merdiven_genislik_cm": [150, 140],
         "tek_yon_kacis_m": 19, "iki_yon_kacis_m": 44},
    ],
}


def yuk(mahal):
    kat = KULLANICI_YUKU.get(mahal["tur"])
    if kat is None:
        return None
    return math.ceil(mahal["alan_m2"] / kat)


def hesapla(veri):
    yag = bool(veri.get("yagmurlama", False))
    sonuc = {"yagmurlama": yag, "katlar": [], "bulgular": []}
    for k in veri["katlar"]:
        toplam = 0
        mahaller = []
        for m in k["mahaller"]:
            y = yuk(m)
            mahaller.append({**m, "kisi": y,
                             "dayanak": "BYKHY Ek-5/A" if y is not None else "TEYİT GEREKLİ — tür katsayısı elde yok"})
            if y is None:
                sonuc["bulgular"].append(f"🔴 {k['kat']} / {m['ad']}: '{m['tur']}' için katsayı yok — Ek-5/A'dan teyit et.")
            else:
                toplam += y
        kapi_gerekli = math.ceil(toplam / KAPI_BIRIM_KISI) * BIRIM_GENISLIK_CM
        merd_gerekli = math.ceil(toplam / MERDIVEN_BIRIM_KISI) * BIRIM_GENISLIK_CM
        kapi_mevcut = sum(k.get("kapi_genislik_cm", []))
        merd_mevcut = sum(k.get("merdiven_genislik_cm", []))
        kat_s = {
            "kat": k["kat"], "kullanici_yuku": toplam, "mahaller": mahaller,
            "kapi": {"gerekli_cm": kapi_gerekli, "mevcut_cm": kapi_mevcut,
                     "durum": "UYGUN" if kapi_mevcut >= kapi_gerekli else "UYGUN DEĞİL", "dayanak": "BYKHY md.32"},
            "merdiven": {"gerekli_cm": merd_gerekli, "mevcut_cm": merd_mevcut,
                         "durum": "UYGUN" if merd_mevcut >= merd_gerekli else "UYGUN DEĞİL", "dayanak": "BYKHY md.32"},
        }
        # tekil genişlik kontrolleri
        for g in k.get("kapi_genislik_cm", []):
            if g < MIN_KAPI_NET_CM:
                sonuc["bulgular"].append(f"🟢 {k['kat']}: kapı {g} cm < {MIN_KAPI_NET_CM} cm — TS 9111 §4.6.2 (PAİY md.32 ≥80 ama TS daha sıkı → TS geçerli).")
        for g in k.get("merdiven_genislik_cm", []):
            if g < MIN_MERDIVEN_KAMU_CM:
                sonuc["bulgular"].append(f"🟢 {k['kat']}: merdiven kolu {g} cm < {MIN_MERDIVEN_KAMU_CM} cm — PAİY md.31/1-a (kamu binası).")
        # kaçış uzaklıkları
        for anahtar, etiket in (("tek_yon_kacis_m", "tek_yon"), ("iki_yon_kacis_m", "iki_yon")):
            if anahtar in k:
                limit = KACIS_UZAKLIK[etiket][yag]
                durum = "UYGUN" if k[anahtar] <= limit else "UYGUN DEĞİL"
                kat_s[etiket] = {"olculen_m": k[anahtar], "limit_m": limit, "durum": durum,
                                 "dayanak": f"BYKHY Ek-5/B ({'yağmurlamalı' if yag else 'yağmurlamasız'})"}
                if durum != "UYGUN":
                    sonuc["bulgular"].append(f"🟢 {k['kat']}: {etiket.replace('_', ' ')} kaçış {k[anahtar]} m > {limit} m — BYKHY Ek-5/B.")
        if kat_s["kapi"]["durum"] != "UYGUN":
            sonuc["bulgular"].append(f"🟢 {k['kat']}: kapı toplam {kapi_mevcut} cm < gerekli {kapi_gerekli} cm — BYKHY md.32.")
        if kat_s["merdiven"]["durum"] != "UYGUN":
            sonuc["bulgular"].append(f"🟢 {k['kat']}: merdiven toplam {merd_mevcut} cm < gerekli {merd_gerekli} cm — BYKHY md.32.")
        sonuc["katlar"].append(kat_s)
    if not sonuc["bulgular"]:
        sonuc["bulgular"].append("🟢 Girilen değerlerle kaçış kapasitesi ve uzaklıkları uygun.")
    sonuc["not"] = "Ön-denetim. Yangın tahliye projesi ve yağmurlama durumu idarece teyit edilmeli."
    return sonuc


def ozet(s):
    print(f"\nKAÇIŞ HESABI  (yağmurlama: {'var' if s['yagmurlama'] else 'yok'})")
    print("-" * 64)
    for k in s["katlar"]:
        print(f"{k['kat']:<12} yük {k['kullanici_yuku']:>4} kişi | kapı {k['kapi']['mevcut_cm']}/{k['kapi']['gerekli_cm']} cm {k['kapi']['durum']:<12}"
              f"| merdiven {k['merdiven']['mevcut_cm']}/{k['merdiven']['gerekli_cm']} cm {k['merdiven']['durum']}")
    print("\nBULGULAR")
    for b in s["bulgular"]:
        print(" •", b)
    print("\n" + s["not"])


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__); return
    if len(sys.argv) > 1:
        veri = json.load(sys.stdin) if sys.argv[1] == "-" else json.load(open(sys.argv[1], encoding="utf-8"))
    else:
        print("(örnek veriyle çalışıyor — kendi verini JSON olarak ver)")
        veri = ORNEK
    s = hesapla(veri)
    print(json.dumps(s, ensure_ascii=False, indent=2))
    ozet(s)


if __name__ == "__main__":
    main()
