#!/usr/bin/env python3
"""Birim fiyat analizi — rayiç + işçilik + makine + nakliye girdilerinden poz birim fiyatı; özel poz (ÖBF) üretimi.

Kullanım:
  python3 fiyat_analizi.py analiz.xlsx [--kar 25] [--cikti analiz_sonuc.xlsx]
  python3 fiyat_analizi.py analiz.json
  python3 fiyat_analizi.py --ornek

Girdi (xlsx sayfası veya JSON): her satır bir girdi kalemi.
  Poz No · Poz Tanımı · Poz Birimi · Tür (malzeme|iscilik|makine|nakliye|diger) · Rayiç No · Girdi Adı · Birim · Miktar · Rayiç Fiyat
  Aynı Poz No'lu satırlar tek analizde toplanır. Miktar = 1 birim imalat için sarf (ÇŞB analiz formatı).
Formül (ÇŞB analiz yapısı):
  malzeme + işçilik + makine + nakliye = ANALİZ TOPLAMI (girdi maliyeti)
  + kâr ve genel gider (%25, --kar) = BİRİM FİYAT   (ÇŞB: %25; idare sözleşmede farklı belirleyebilir)
Rayiç fiyatları kullanıcı verir (ÇŞB rayiç listesi / piyasa teklifi); skill rayiç uydurmaz. Kaynağı olmayan rayiç 🔴.
"""
import argparse
import json
import os
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak
import xlsx_io
from xlsx_io import Hucre as H

TUR = {"malzeme": "Malzeme", "iscilik": "İşçilik", "makine": "Makine", "nakliye": "Nakliye", "diger": "Diğer"}

ORNEK = [
    {"Poz No": "ÖBF-001", "Poz Tanımı": "200 dozlu demirsiz beton (örnek)", "Poz Birimi": "m³", "Tür": "malzeme", "Rayiç No": "10.130.1001", "Girdi Adı": "Çimento (torbalı)", "Birim": "ton", "Miktar": 0.200, "Rayiç Fiyat": 3100.00, "Kaynak": "ÖRNEK"},
    {"Poz No": "ÖBF-001", "Tür": "malzeme", "Rayiç No": "10.140.1004", "Girdi Adı": "Kum", "Birim": "m³", "Miktar": 0.45, "Rayiç Fiyat": 480.00, "Kaynak": "ÖRNEK"},
    {"Poz No": "ÖBF-001", "Tür": "malzeme", "Rayiç No": "10.140.1010", "Girdi Adı": "Çakıl", "Birim": "m³", "Miktar": 0.80, "Rayiç Fiyat": 520.00, "Kaynak": "ÖRNEK"},
    {"Poz No": "ÖBF-001", "Tür": "malzeme", "Rayiç No": "10.100.1002", "Girdi Adı": "Su", "Birim": "m³", "Miktar": 0.20, "Rayiç Fiyat": 45.00, "Kaynak": "ÖRNEK"},
    {"Poz No": "ÖBF-001", "Tür": "iscilik", "Rayiç No": "10.100.1062", "Girdi Adı": "Betoncu ustası", "Birim": "sa", "Miktar": 1.0, "Rayiç Fiyat": 210.00, "Kaynak": "ÖRNEK"},
    {"Poz No": "ÖBF-001", "Tür": "iscilik", "Rayiç No": "10.100.1063", "Girdi Adı": "Düz işçi", "Birim": "sa", "Miktar": 4.0, "Rayiç Fiyat": 150.00, "Kaynak": "ÖRNEK"},
    {"Poz No": "ÖBF-001", "Tür": "makine", "Rayiç No": "03.014", "Girdi Adı": "Betoniyer", "Birim": "sa", "Miktar": 0.6, "Rayiç Fiyat": 90.00, "Kaynak": "ÖRNEK"},
]


def yukle(satirlar):
    b = list(satirlar[0].keys())
    kp = ortak.kolon_bul(b, "poz", zorunlu=True)
    kt = ortak.kolon_bul(b, "tur") or "Tür"
    kr = ortak.kolon_bul(b, "rayic_no")
    ka = next((x for x in b if ortak.norm(x) in ("girdi adi", "girdi", "rayic adi", "ad", "malzeme")), None) or ortak.kolon_bul(b, "tanim")
    kb = ortak.kolon_bul(b, "birim"); km = ortak.kolon_bul(b, "miktar", zorunlu=True); kf = ortak.kolon_bul(b, "fiyat", zorunlu=True)
    kk = ortak.kolon_bul(b, "kaynak")
    kpt = next((x for x in b if ortak.norm(x) in ("poz tanimi", "poz tanim", "imalat tanimi")), None)
    kpb = next((x for x in b if ortak.norm(x) in ("poz birimi", "imalat birimi")), None)
    pozlar = OrderedDict()
    for r in satirlar:
        p = str(r.get(kp) or "").strip()
        if not p:
            continue
        d = pozlar.setdefault(p, {"poz": p, "tanim": None, "birim": None, "girdiler": []})
        if kpt and r.get(kpt): d["tanim"] = r[kpt]
        if kpb and r.get(kpb): d["birim"] = r[kpb]
        tur = ortak.norm(r.get(kt)) if r.get(kt) else "diger"
        tur = {"iscilik": "iscilik", "işçilik": "iscilik", "malzeme": "malzeme", "makine": "makine", "makina": "makine", "nakliye": "nakliye", "tasima": "nakliye"}.get(tur, "diger")
        d["girdiler"].append({"tur": tur, "rayic_no": r.get(kr) if kr else None, "ad": r.get(ka) if ka else None,
                              "birim": r.get(kb) if kb else None, "miktar": ortak.sayi(r.get(km)), "fiyat": ortak.sayi(r.get(kf)),
                              "kaynak": r.get(kk) if kk else None})
    return list(pozlar.values())


def analiz(p, kar=25.0, yuvarla=2):
    gruplar = OrderedDict((t, 0.0) for t in TUR)
    for g in p["girdiler"]:
        g["tutar"] = round(g["miktar"] * g["fiyat"], 4)
        gruplar[g["tur"]] += g["tutar"]
    toplam = round(sum(gruplar.values()), yuvarla)
    kar_t = round(toplam * kar / 100, yuvarla)
    bf = round(toplam + kar_t, yuvarla)
    kaynaksiz = [g for g in p["girdiler"] if not g["kaynak"]]
    return {**p, "gruplar": {TUR[k]: round(v, yuvarla) for k, v in gruplar.items() if v}, "analiz_toplami": toplam,
            "kar_genel_gider_%": kar, "kar_genel_gider": kar_t, "birim_fiyat": bf,
            "guven": "🔴 kaynaksız rayiç var" if kaynaksiz else "🟢",
            "iscilik_orani": round(gruplar["iscilik"] / toplam, 3) if toplam else 0}


def yaz(sonuclar, yol):
    sayfalar = []
    icmal = [["Poz No", "Tanım", "Birim", "Malzeme", "İşçilik", "Makine", "Nakliye", "Diğer", "Analiz Toplamı", "Kâr+GG %", "Kâr+GG", "BİRİM FİYAT", "İşçilik oranı", "Güven"]]
    for s in sonuclar:
        g = s["gruplar"]
        icmal.append([s["poz"], s["tanim"], s["birim"]] + [H(g.get(t, 0), sayi=2) for t in TUR.values()] +
                     [H(s["analiz_toplami"], sayi=2), s["kar_genel_gider_%"], H(s["kar_genel_gider"], sayi=2), H(s["birim_fiyat"], sayi=2, kalin=True), H(s["iscilik_orani"], sayi="pct"), s["guven"]])
        t = [[H(f"{s['poz']} — {s['tanim'] or ''}", kalin=True)], [f"Birim: {s['birim'] or '?'}   Kâr ve genel gider: %{s['kar_genel_gider_%']:g}"], [],
             ["Tür", "Rayiç No", "Girdi", "Birim", "Miktar", "Rayiç Fiyat", "Tutar", "Kaynak"]]
        b = len(t) + 1
        for i, g in enumerate(s["girdiler"], b):
            t.append([TUR[g["tur"]], g["rayic_no"], g["ad"], g["birim"], H(g["miktar"], sayi=4), H(g["fiyat"], sayi=2), H(g["tutar"], formul=f"E{i}*F{i}", sayi=2), g["kaynak"] or "🔴 kaynak yok"])
        e = len(t)
        t += [[H("Analiz toplamı", kalin=True), "", "", "", "", "", H(s["analiz_toplami"], formul=f"SUM(G{b}:G{e})", sayi=2, kalin=True)],
              [H(f"Kâr ve genel gider %{s['kar_genel_gider_%']:g}", kalin=True), "", "", "", "", "", H(s["kar_genel_gider"], formul=f"G{e+1}*{s['kar_genel_gider_%']}/100", sayi=2, kalin=True)],
              [H("BİRİM FİYAT", kalin=True), "", "", "", "", "", H(s["birim_fiyat"], formul=f"G{e+1}+G{e+2}", sayi=2, kalin=True)]]
        sayfalar.append((s["poz"][:31], t))
    xlsx_io.yaz(yol, [("İcmal", icmal)] + sayfalar)
    return yol


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("girdi", nargs="?"); ap.add_argument("--kar", type=float, default=25.0)
    ap.add_argument("--cikti", default="fiyat_analizi.xlsx"); ap.add_argument("--ornek", action="store_true")
    a = ap.parse_args()
    if a.ornek or not a.girdi:
        print("(örnek analiz — rayiçler gerçek değil)"); satirlar = ORNEK
    elif a.girdi.endswith(".json"):
        satirlar = json.load(open(a.girdi, encoding="utf-8"))
    else:
        satirlar = xlsx_io.oku_tablo(*xlsx_io.yukle_argv(a.girdi))
    sonuclar = [analiz(p, a.kar) for p in yukle(satirlar)]
    yaz(sonuclar, a.cikti)
    print(json.dumps([{k: v for k, v in s.items() if k != "girdiler"} for s in sonuclar], ensure_ascii=False, indent=2))
    for s in sonuclar:
        print(f"\n{s['poz']}  {s['tanim'] or ''}  →  BİRİM FİYAT {ortak.tl(s['birim_fiyat'])} TL/{s['birim'] or '?'}  {s['guven']}")
        for k, v in s["gruplar"].items():
            print(f"   {k:<10} {ortak.tl(v):>14}")
        print(f"   {'Kâr+GG':<10} {ortak.tl(s['kar_genel_gider']):>14}  (%{s['kar_genel_gider_%']:g})")
    print(f"\n→ {a.cikti}")


if __name__ == "__main__":
    main()
