#!/usr/bin/env python3
"""Merdiven geometri kontrolü — PAİY md.31 + TS 9111 §4.7.1.3 (en sıkı kural geçerli).

Kullanım:
  python3 merdiven_kontrol.py                                   # örnek
  python3 merdiven_kontrol.py --kat-yuksekligi 450 --basamak 27 --rih 16.5 --kol 150 --sahanlik 150
  python3 merdiven_kontrol.py girdi.json   # {"merdivenler":[{"ad":"M1","kat_yuksekligi_cm":450,...}]}

Kontroller: rıht yüksekliği, basamak derinliği, 2a+b formülü, kol/sahanlık genişliği,
kat başına basamak adedi (rıht sayısı tam sayı mı), açık rıht.
"""
import argparse
import json
import math
import sys

RIHT_MAX_UMUMI = 16.0        # PAİY md.31/2 — umumi bina ≤16 cm (konut ≤18)
BASAMAK_MIN_PAIY = 27.0      # PAİY md.31/2
BASAMAK_MIN_TS = 28.0        # TS 9111 §4.7.1.3.1 — daha sıkı → geçerli
FORMUL_MIN, FORMUL_MAX = 60.0, 64.0   # 2a+b
KOL_MIN_KAMU = 150.0         # PAİY md.31/1-a
SAHANLIK_MIN_KAMU = 150.0
MAX_BASAMAK_SAHANLIKSIZ = 16 # yaygın uygulama (TS 9111 §4.7.1.3 kol başına) — 🟡 teyit

ORNEK = {"merdivenler": [
    {"ad": "M1 (ana)", "kat_yuksekligi_cm": 450, "basamak_derinligi_cm": 29, "riht_cm": 15.52,
     "kol_genisligi_cm": 150, "sahanlik_cm": 150, "acik_riht": False, "kol_basi_basamak": 15},
    {"ad": "M2 (yangın)", "kat_yuksekligi_cm": 450, "basamak_derinligi_cm": 27, "riht_cm": 17.3,
     "kol_genisligi_cm": 140, "sahanlik_cm": 140, "acik_riht": True, "kol_basi_basamak": 13},
]}


def kontrol(m):
    b, a = float(m["basamak_derinligi_cm"]), float(m["riht_cm"])
    h = float(m["kat_yuksekligi_cm"])
    n = h / a if a else 0
    satirlar = []

    def s(konu, olculen, gerek, ok, dayanak, guven="🟢"):
        satirlar.append({"konu": konu, "olculen": olculen, "gereken": gerek,
                         "durum": "UYGUN" if ok else "UYGUN DEĞİL", "dayanak": dayanak, "guven": guven})

    s("Rıht yüksekliği", f"{a:.2f} cm", f"≤{RIHT_MAX_UMUMI:.0f} cm", a <= RIHT_MAX_UMUMI, "PAİY md.31/2 (umumi bina) · TS 9111 §4.7.1.3.1")
    s("Basamak derinliği", f"{b:.1f} cm", f"≥{BASAMAK_MIN_TS:.0f} cm (PAİY ≥27, TS daha sıkı → TS)", b >= BASAMAK_MIN_TS, "TS 9111 §4.7.1.3.1 · PAİY md.31/1-c")
    f = 2 * a + b
    s("2a+b formülü", f"{f:.1f}", f"{FORMUL_MIN:.0f}–{FORMUL_MAX:.0f}", FORMUL_MIN <= f <= FORMUL_MAX, "PAİY md.31/2")
    s("Kol genişliği", f"{m['kol_genisligi_cm']} cm", f"≥{KOL_MIN_KAMU:.0f} cm", float(m["kol_genisligi_cm"]) >= KOL_MIN_KAMU, "PAİY md.31/1-a (kamu binası)")
    s("Sahanlık genişliği", f"{m['sahanlik_cm']} cm", f"≥{SAHANLIK_MIN_KAMU:.0f} cm", float(m["sahanlik_cm"]) >= SAHANLIK_MIN_KAMU, "PAİY md.31/1-a")
    tam = abs(n - round(n)) < 0.02
    s("Rıht adedi (kat yüksekliği ÷ rıht)", f"{n:.2f}", "tam sayı", tam, "geometri kontrolü — kesitle çapraz doğrula", "🟡" if not tam else "🟢")
    s("Açık rıht", "var" if m.get("acik_riht") else "yok", "yasak", not m.get("acik_riht"), "TS 9111 §4.7.1.3.1")
    if "kol_basi_basamak" in m:
        k = int(m["kol_basi_basamak"])
        s("Kol başına basamak", str(k), f"≤{MAX_BASAMAK_SAHANLIKSIZ}", k <= MAX_BASAMAK_SAHANLIKSIZ, "TS 9111 §4.7.1.3 — sayı teyit edilmeli", "🟡")

    return {"ad": m["ad"], "kontroller": satirlar,
            "sonuc": "UYGUN" if all(x["durum"] == "UYGUN" for x in satirlar) else "UYGUN DEĞİL",
            "kaldi": [x for x in satirlar if x["durum"] != "UYGUN"]}


def ozet(sonuclar):
    for r in sonuclar:
        print(f"\n{r['ad']}  →  {r['sonuc']}")
        print("-" * 72)
        for k in r["kontroller"]:
            print(f"  {k['guven']} {k['konu']:<36} {k['olculen']:>10}  gereken {k['gereken']:<32} {k['durum']}")
    print("\nNot: 'En sıkı kural geçerli' (PAİY md.31/1-c). Ön-denetimdir.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("dosya", nargs="?")
    p.add_argument("--ad", default="M1"); p.add_argument("--kat-yuksekligi", type=float)
    p.add_argument("--basamak", type=float); p.add_argument("--rih", "--riht", dest="riht", type=float)
    p.add_argument("--kol", type=float); p.add_argument("--sahanlik", type=float)
    p.add_argument("--acik-riht", action="store_true"); p.add_argument("--kol-basi", type=int)
    a = p.parse_args()
    if a.dosya:
        v = json.load(open(a.dosya, encoding="utf-8"))
    elif a.kat_yuksekligi:
        m = {"ad": a.ad, "kat_yuksekligi_cm": a.kat_yuksekligi, "basamak_derinligi_cm": a.basamak,
             "riht_cm": a.riht, "kol_genisligi_cm": a.kol, "sahanlik_cm": a.sahanlik or a.kol,
             "acik_riht": a.acik_riht}
        if a.kol_basi:
            m["kol_basi_basamak"] = a.kol_basi
        v = {"merdivenler": [m]}
    else:
        print("(örnek veriyle çalışıyor)")
        v = ORNEK
    sonuclar = [kontrol(m) for m in v["merdivenler"]]
    print(json.dumps(sonuclar, ensure_ascii=False, indent=2))
    ozet(sonuclar)


if __name__ == "__main__":
    main()
