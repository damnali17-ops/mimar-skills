#!/usr/bin/env python3
"""Fiyat farkı hesabı — 4734 sayılı KİK kapsamındaki Yapım İşlerinde Uygulanacak Fiyat Farkına İlişkin Esaslar
(2013/5217 sayılı BKK, RG 29/8/2013 – 28750; değişiklikleriyle).

Formül (md.5):
  Pn = a1 × (İn/İo) + a2 × [ b1 × (Çn/Ço) + b2 × (Dn/Do) + b3 × (Yn/Yo) + b4 × (Kn/Ko) + b5 × (Mn/Mo) ]
  F  = An × B × (Pn − 1)          B = 0,90 (sabit katsayı)
  a1 + a2 = 1 ; b1 + … + b5 = 1  (idari şartnamede yazılı ağırlıklar)
  o = ihale tarihi (teklif tarihi) ayı endeksi · n = hakediş dönemi (uygulama ayı) endeksi
  An = hakediş dönemi imalat tutarı (fiyat farkı hesabına esas; avans/geçici kabul eksiği hariç — md.5 🟡)

Kullanım:
  python3 fiyat_farki.py --an 1250000 --a1 0.35 --a2 0.65 --b 0.30,0.25,0.20,0.10,0.15 \
      --io 100 --in 118 --co 100 --cn 121 --do 100 --dn 109 --yo 100 --yn 132 --ko 100 --kn 115 --mo 100 --mn 111
  python3 fiyat_farki.py donem.xlsx        # her satır bir hakediş dönemi (kolonlar: Hakediş, An, İo, İn, Ço, Çn, …)
  python3 fiyat_farki.py --ornek
Sadece genel endeks kullanılan sözleşme (md.6 — ağırlık belirtilmemişse): --genel Go Gn → Pn = Gn/Go.
Endeks kaynakları (TÜİK Yİ-ÜFE alt endeksleri) ve 2022 ek fiyat farkı düzenlemeleri için references/05-fiyat-farki.md.
Skill endeks değeri uydurmaz; kullanıcı TÜİK'ten alır. Endeks kaynağı yazılmamışsa 🔴.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak
import xlsx_io
from xlsx_io import Hucre as H

B_SABIT = 0.90
ANAHTAR = [("i", "İşçilik"), ("c", "Çimento"), ("d", "Demir-çelik"), ("y", "Akaryakıt"), ("k", "Kereste"), ("m", "Makine")]


def hesapla(an, a1, a2, b, endeks, B=B_SABIT, genel=None, yuvarla=2):
    """endeks: {'io':..,'in':..,'co':..,...}; b: [b1..b5]; genel: (Go, Gn) or None"""
    uyarilar = []
    if genel:
        go, gn = genel
        pn = gn / go
        detay = {"Gn/Go": round(pn, 6)}
    else:
        if abs(a1 + a2 - 1) > 1e-6:
            uyarilar.append(f"a1+a2 = {a1+a2:.4f} ≠ 1 — idari şartnameyi kontrol et")
        if abs(sum(b) - 1) > 1e-6:
            uyarilar.append(f"Σb = {sum(b):.4f} ≠ 1 — idari şartnameyi kontrol et")
        oranlar = {}
        for (kod, ad) in ANAHTAR:
            o, n = endeks.get(kod + "o"), endeks.get(kod + "n")
            oranlar[kod] = (n / o) if (o and n) else None
        ic = 0.0
        for i, kod in enumerate(("c", "d", "y", "k", "m")):
            if b[i] and oranlar[kod] is None:
                uyarilar.append(f"b{i+1}={b[i]} ama {dict(ANAHTAR)[kod]} endeksi eksik → 0 alındı 🔴")
            ic += b[i] * (oranlar[kod] or 0)
        if a1 and oranlar["i"] is None:
            uyarilar.append("a1 verildi ama işçilik endeksi eksik → 0 alındı 🔴")
        pn = a1 * (oranlar["i"] or 0) + a2 * ic
        detay = {f"{ad} (n/o)": (round(v, 6) if v is not None else None) for (kod, ad), v in zip(ANAHTAR, [oranlar[k] for k, _ in ANAHTAR])}
    f = round(an * B * (pn - 1), yuvarla)
    return {"An": an, "B": B, "Pn": round(pn, 6), "Pn-1": round(pn - 1, 6), "fiyat_farki": f,
            "yon": "artış (ödenecek)" if f > 0 else ("azalış (kesilecek)" if f < 0 else "yok"),
            "oranlar": detay, "uyarilar": uyarilar, "guven": "🔴" if uyarilar else "🟢",
            "dayanak": "Fiyat Farkı Esasları md.5 (2013/5217 BKK)"}


def dosyadan(yol):
    satirlar = xlsx_io.oku_tablo(*xlsx_io.yukle_argv(yol))
    out = []
    for r in satirlar:
        n = {ortak.norm(k).replace(" ", ""): v for k, v in r.items()}
        def g(*adlar, default=None):
            for a in adlar:
                if a in n and n[a] not in (None, ""):
                    return ortak.sayi(n[a])
            return default
        endeks = {}
        for kod, _ in ANAHTAR:
            endeks[kod + "o"] = g(kod + "o", {"i": "io", "c": "co", "d": "do", "y": "yo", "k": "ko", "m": "mo"}[kod])
            endeks[kod + "n"] = g(kod + "n")
        b = [g(f"b{i}", default=0) for i in range(1, 6)]
        out.append({"hakedis": n.get("hakedis") or n.get("no") or len(out) + 1, "an": g("an", "tutar", default=0),
                    "a1": g("a1", default=0), "a2": g("a2", default=0), "b": b, "endeks": endeks,
                    "genel": (g("go"), g("gn")) if g("go") and g("gn") else None})
    return out


def yaz(sonuclar, yol):
    t = [["Hakediş", "An (TL)", "a1", "a2", "b1", "b2", "b3", "b4", "b5"] + [f"{ad} n/o" for _, ad in ANAHTAR] + ["Pn", "B", "Fiyat Farkı (TL)", "Yön", "Güven", "Uyarı"]]
    top = 0.0
    for d, s in sonuclar:
        oran = list(s["oranlar"].values()) if not d.get("genel") else [s["oranlar"]["Gn/Go"]] + [None] * 5
        t.append([d["hakedis"], H(d["an"], sayi=2), d["a1"], d["a2"]] + d["b"] + [H(v, sayi=4) if v is not None else None for v in oran] +
                 [H(s["Pn"], sayi=4), s["B"], H(s["fiyat_farki"], sayi=2), s["yon"], s["guven"], "; ".join(s["uyarilar"])])
        top += s["fiyat_farki"]
    t.append([H("TOPLAM", kalin=True)] + [""] * 16 + [H(round(top, 2), sayi=2, kalin=True)])
    xlsx_io.yaz(yol, {"Fiyat Farkı": t})
    return yol


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", nargs="?"); ap.add_argument("--an", type=float); ap.add_argument("--a1", type=float, default=0)
    ap.add_argument("--a2", type=float, default=0); ap.add_argument("--b", default="0,0,0,0,0", help="b1,b2,b3,b4,b5")
    for kod, _ in ANAHTAR:
        ap.add_argument(f"--{kod}o", type=float); ap.add_argument(f"--{kod}n", type=float)
    ap.add_argument("--genel", nargs=2, type=float, metavar=("Go", "Gn")); ap.add_argument("--B", type=float, default=B_SABIT)
    ap.add_argument("--cikti", default="fiyat_farki.xlsx"); ap.add_argument("--ornek", action="store_true")
    a = ap.parse_args()
    if a.dosya:
        donemler = dosyadan(a.dosya)
    elif a.ornek or a.an is None:
        print("(örnek — endeksler temsilîdir, gerçek değil)")
        donemler = [{"hakedis": 1, "an": 1250000, "a1": 0.35, "a2": 0.65, "b": [0.30, 0.25, 0.20, 0.10, 0.15],
                     "endeks": {"io": 100, "in": 118, "co": 100, "cn": 121, "do": 100, "dn": 109, "yo": 100, "yn": 132, "ko": 100, "kn": 115, "mo": 100, "mn": 111}, "genel": None}]
    else:
        endeks = {k: getattr(a, k) for kod, _ in ANAHTAR for k in (kod + "o", kod + "n")}
        donemler = [{"hakedis": 1, "an": a.an, "a1": a.a1, "a2": a.a2, "b": [float(x) for x in a.b.split(",")], "endeks": endeks, "genel": tuple(a.genel) if a.genel else None}]
    sonuclar = [(d, hesapla(d["an"], d["a1"], d["a2"], d["b"], d["endeks"], a.B, d.get("genel"))) for d in donemler]
    yaz(sonuclar, a.cikti)
    print(json.dumps([s for _, s in sonuclar], ensure_ascii=False, indent=2))
    for d, s in sonuclar:
        print(f"\nHakediş {d['hakedis']}: An {ortak.tl(d['an'])} × B {s['B']} × (Pn {s['Pn']:.4f} − 1) = FİYAT FARKI {ortak.tl(s['fiyat_farki'])} TL  {s['yon']}  {s['guven']}")
        for u in s["uyarilar"]:
            print("   ⚠", u)
    print(f"\n→ {a.cikti}")


if __name__ == "__main__":
    main()
