#!/usr/bin/env python3
"""Otopark ve sığınak hesabı — Otopark Yönetmeliği + Sığınak Yönetmeliği md.8.

Kullanım:
  python3 otopark_siginak_hesabi.py                       # örnek veri
  python3 otopark_siginak_hesabi.py --emsal 3200 --insaat 4100 --mevcut-arac 28 --mevcut-engelli 1 --siginak-m2 120
  python3 otopark_siginak_hesabi.py girdi.json

Girdi JSON: {"emsal_alan_m2": 3200, "insaat_alan_m2": 4100,
             "mevcut_arac": 28, "mevcut_engelli": 1, "mevcut_siginak_m2": 120,
             "yerel_oran_m2_per_arac": null}
Not: Otopark oranı için Ek-1 resmî tablo ve yerel otopark yönetmeliği kesin hesapta
doğrulanmalıdır — çıktı 🟡 ile etiketlenir.
"""
import argparse
import json
import math
import sys

OTOPARK_M2_PER_ARAC = 100      # kamu kurumu — 100 m²'ye 1 araç (Otopark Yön., ikincil kaynak)
OTOPARK_BIRIM_M2 = 20          # birim otopark alanı ≥20 m²
ENGELLI_ORAN = 20              # her 20 araca 1 engelli (TS 9111 §4.4.1 / Otopark Yön.)
SIGINAK_ESIK_EMSAL = 1500      # Sığınak Yön. md.8 — emsal ≥1500 m² → zorunlu
SIGINAK_KISI_BOLEN = 20        # kişi = emsal ÷ 20
SIGINAK_M2_PER_KISI = 1.0      # ≥1 m²/kişi
SIGINAK_MIN_M2 = 9

ORNEK = {"emsal_alan_m2": 3200, "insaat_alan_m2": 4100,
         "mevcut_arac": 28, "mevcut_engelli": 1, "mevcut_siginak_m2": 120,
         "yerel_oran_m2_per_arac": None}


def hesapla(v):
    emsal = float(v["emsal_alan_m2"])
    oran = v.get("yerel_oran_m2_per_arac") or OTOPARK_M2_PER_ARAC
    gerekli_arac = math.ceil(emsal / oran)
    gerekli_engelli = max(1, math.ceil(gerekli_arac / ENGELLI_ORAN))
    mevcut_arac = int(v.get("mevcut_arac", 0))
    mevcut_eng = int(v.get("mevcut_engelli", 0))

    siginak_zorunlu = emsal >= SIGINAK_ESIK_EMSAL
    kisi = math.ceil(emsal / SIGINAK_KISI_BOLEN) if siginak_zorunlu else 0
    gerekli_siginak = max(SIGINAK_MIN_M2, math.ceil(kisi * SIGINAK_M2_PER_KISI)) if siginak_zorunlu else 0
    mevcut_sig = float(v.get("mevcut_siginak_m2", 0))

    bulgular = []
    guven_otopark = "🟡" if v.get("yerel_oran_m2_per_arac") is None else "🟢"
    if mevcut_arac < gerekli_arac:
        bulgular.append(f"{guven_otopark} Otopark: {mevcut_arac} araç < gerekli {gerekli_arac} ({emsal:.0f} m² ÷ {oran}) — Otopark Yön.")
    if mevcut_eng < gerekli_engelli:
        bulgular.append(f"🟢 Engelli otopark: {mevcut_eng} < gerekli {gerekli_engelli} (1/{ENGELLI_ORAN}) — TS 9111 §4.4.1.")
    if siginak_zorunlu and mevcut_sig < gerekli_siginak:
        bulgular.append(f"🟢 Sığınak: {mevcut_sig:.0f} m² < gerekli {gerekli_siginak} m² ({kisi} kişi × {SIGINAK_M2_PER_KISI} m²) — Sığınak Yön. md.8.")
    if siginak_zorunlu and mevcut_sig == 0:
        bulgular.append("🟢 Emsal ≥1 500 m²: sığınak ZORUNLU, projede mahal görünmüyor — Sığınak Yön. md.8.")
    if not bulgular:
        bulgular.append("🟢 Otopark ve sığınak miktarları girilen değerlerle uygun.")

    return {
        "girdi": v,
        "otopark": {"oran_m2_per_arac": oran, "gerekli_arac": gerekli_arac, "mevcut_arac": mevcut_arac,
                    "gerekli_engelli": gerekli_engelli, "mevcut_engelli": mevcut_eng,
                    "gerekli_alan_m2_min": gerekli_arac * OTOPARK_BIRIM_M2,
                    "guven": guven_otopark,
                    "dayanak": "Otopark Yön. (kamu kurumu 100 m²/araç — Ek-1 ve yerel yönetmelikle teyit) · TS 9111 §4.4.1"},
        "siginak": {"zorunlu": siginak_zorunlu, "kisi": kisi, "gerekli_m2": gerekli_siginak,
                    "mevcut_m2": mevcut_sig, "dayanak": "Sığınak Yön. md.8"},
        "bulgular": bulgular,
        "not": "Plan notları ve yerel otopark yönetmeliği bu değerlerin önüne geçer. Ön-denetimdir.",
    }


def ozet(s):
    o, g = s["otopark"], s["siginak"]
    print("\nOTOPARK  ", f"gerekli {o['gerekli_arac']} araç (+{o['gerekli_engelli']} engelli) | mevcut {o['mevcut_arac']} (+{o['mevcut_engelli']}) | min alan {o['gerekli_alan_m2_min']} m² {o['guven']}")
    print("SIĞINAK  ", ("zorunlu değil (emsal < 1 500 m²)" if not g["zorunlu"] else
                       f"{g['kisi']} kişi → gerekli {g['gerekli_m2']} m² | mevcut {g['mevcut_m2']:.0f} m²"))
    print("\nBULGULAR")
    for b in s["bulgular"]:
        print(" •", b)
    print("\n" + s["not"])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("dosya", nargs="?", help="girdi JSON dosyası (yoksa örnek/bayraklar)")
    p.add_argument("--emsal", type=float); p.add_argument("--insaat", type=float)
    p.add_argument("--mevcut-arac", type=int); p.add_argument("--mevcut-engelli", type=int)
    p.add_argument("--siginak-m2", type=float); p.add_argument("--yerel-oran", type=float)
    a = p.parse_args()
    if a.dosya:
        v = json.load(open(a.dosya, encoding="utf-8"))
    elif a.emsal:
        v = {"emsal_alan_m2": a.emsal, "insaat_alan_m2": a.insaat or a.emsal,
             "mevcut_arac": a.mevcut_arac or 0, "mevcut_engelli": a.mevcut_engelli or 0,
             "mevcut_siginak_m2": a.siginak_m2 or 0, "yerel_oran_m2_per_arac": a.yerel_oran}
    else:
        print("(örnek veriyle çalışıyor)")
        v = ORNEK
    s = hesapla(v)
    print(json.dumps(s, ensure_ascii=False, indent=2))
    ozet(s)


if __name__ == "__main__":
    main()
