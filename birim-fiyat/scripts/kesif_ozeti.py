#!/usr/bin/env python3
"""Metraj → keşif özeti (yaklaşık maliyet) — Yapım İşleri İhaleleri Uygulama Yön. md.8–11.

Kullanım:
  python3 kesif_ozeti.py metraj.xlsx liste.xlsx [--cikti kesif.xlsx] [--kdv 20] [--kar 0]
  python3 kesif_ozeti.py metraj.xlsx --fiyat-metrajdan          # metrajda birim fiyat kolonu varsa (teklif/sözleşme)
  python3 kesif_ozeti.py --ornek                                # gömülü örnek

Metraj kolonları: Poz No · [Tanım] · Miktar · [Birim] · [İş Grubu] · [Birim Fiyat]
Liste kolonları : Poz No · Tanım · Birim · Birim Fiyat · [Kaynak] · [Yıl]
Kurallar: birim fiyat listeden (poz tam eşleşme); bulunamayan poz "Eşleşmeyen" sayfasına, tutara girmez, toplam 🔴 olur.
ÇŞB birim fiyatları %25 kâr ve genel gider DAHİLdir → --kar 0 (varsayılan). Rayiçten/analizden gelen fiyatlarda --kar 25.
KDV oranı sözleşmeye/mevzuata göre verilir (--kdv), skill varsaymaz; verilmezse KDV satırı "—".
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

ORNEK_METRAJ = [["Poz No", "Tanım", "Birim", "Miktar", "İş Grubu"],
                ["Y.15.001/2B", "Makine ile yumuşak ve sert toprak kazılması", "m³", 1250, "Kazı ve dolgu"],
                ["Y.16.050/04", "C 25/30 basınç dayanım sınıfında beton", "m³", 410.5, "Betonarme"],
                ["Y.21.001/03", "Plywood ile düz yüzeyli betonarme kalıbı", "m²", 2380, "Betonarme"],
                ["Y.23.014", "Ø 8- Ø 12 mm nervürlü beton çelik çubuğu", "ton", 38.2, "Betonarme"],
                ["Y.99.999", "Listede olmayan örnek poz", "ad", 1, "Diğer"]]
ORNEK_LISTE = [["Poz No", "Tanım", "Birim", "Birim Fiyat", "Kaynak", "Yıl"],
               ["Y.15.001/2B", "Makine ile yumuşak ve sert toprak kazılması (serbest kazı)", "m³", 61.25, "ÖRNEK (gerçek değil)", "—"],
               ["Y.16.050/04", "Beton santralinde üretilen C 25/30 basınç dayanım sınıfında beton dökülmesi", "m³", 2890.00, "ÖRNEK (gerçek değil)", "—"],
               ["Y.21.001/03", "Plywood ile düz yüzeyli betonarme kalıbı yapılması", "m²", 585.40, "ÖRNEK (gerçek değil)", "—"],
               ["Y.23.014", "Ø 8- Ø 12 mm nervürlü beton çelik çubuğu, çubukların kesilmesi, bükülmesi ve yerine konulması", "ton", 41250.00, "ÖRNEK (gerçek değil)", "—"]]


def yukle_metraj(satirlar):
    b = list(satirlar[0].keys())
    k = {a: ortak.kolon_bul(b, a) for a in ("poz", "tanim", "birim", "miktar", "grup", "fiyat")}
    if not k["poz"] or not k["miktar"]:
        raise SystemExit(f"Metrajda Poz/Miktar kolonu yok. Başlıklar: {b}")
    out = []
    for r in satirlar:
        if r.get(k["poz"]) in (None, ""):
            continue
        out.append({"poz": str(r[k["poz"]]).strip(), "tanim": r.get(k["tanim"]) if k["tanim"] else None,
                    "birim": r.get(k["birim"]) if k["birim"] else None, "miktar": ortak.sayi(r[k["miktar"]]),
                    "grup": (r.get(k["grup"]) if k["grup"] else None) or None,
                    "fiyat_metraj": ortak.sayi(r.get(k["fiyat"]), None) if k["fiyat"] else None})
    return out


def yukle_liste(satirlar):
    b = list(satirlar[0].keys())
    k = {a: ortak.kolon_bul(b, a) for a in ("poz", "tanim", "birim", "fiyat", "kaynak", "yil")}
    if not k["poz"] or not k["fiyat"]:
        raise SystemExit(f"Listede Poz/Birim Fiyat kolonu yok. Başlıklar: {b}")
    d = {}
    for r in satirlar:
        p = r.get(k["poz"])
        if p in (None, ""):
            continue
        d[ortak.norm(p)] = {"poz": str(p).strip(), "tanim": r.get(k["tanim"]) if k["tanim"] else None,
                            "birim": r.get(k["birim"]) if k["birim"] else None, "fiyat": ortak.sayi(r[k["fiyat"]], None),
                            "kaynak": r.get(k["kaynak"]) if k["kaynak"] else None, "yil": r.get(k["yil"]) if k["yil"] else None}
    return d


def hesapla(metraj, liste, kar=0.0, kdv=None, fiyat_metrajdan=False, yuvarla=2):
    satirlar, eslesmeyen, gruplar = [], [], OrderedDict()
    for i, m in enumerate(metraj, 1):
        kayit = liste.get(ortak.norm(m["poz"])) if liste else None
        if fiyat_metrajdan and m["fiyat_metraj"] is not None:
            bf, kaynak, g = m["fiyat_metraj"], "metraj/teklif", "🟢"
            tanim, birim = m["tanim"], m["birim"]
        elif kayit and kayit["fiyat"] is not None:
            bf, kaynak, g = kayit["fiyat"], f"{kayit['kaynak'] or 'liste'} {kayit['yil'] or ''}".strip(), "🟢"
            tanim, birim = kayit["tanim"] or m["tanim"], kayit["birim"] or m["birim"]
            if m["birim"] and kayit["birim"]:
                yeni, carpan, notu = ortak.birim_cevir(m["miktar"], m["birim"], kayit["birim"])
                if notu:
                    g = "🟡"; kaynak += " · " + notu
                    if carpan is not None:
                        m = {**m, "miktar": round(yeni, 4)}
        else:
            eslesmeyen.append({"sira": i, "poz": m["poz"], "tanim": m["tanim"], "miktar": m["miktar"], "birim": m["birim"]})
            continue
        bf_k = round(bf * (1 + kar / 100), yuvarla)
        tutar = round(m["miktar"] * bf_k, yuvarla)
        grup = m["grup"] or f"Bölüm {ortak.poz_bolumu(m['poz'])}"
        satirlar.append({"sira": i, "grup": grup, "poz": m["poz"], "tanim": tanim, "birim": birim, "miktar": m["miktar"],
                         "birim_fiyat": bf_k, "tutar": tutar, "kaynak": kaynak, "guven": g})
        gruplar[grup] = gruplar.get(grup, 0.0) + tutar
    toplam = round(sum(s["tutar"] for s in satirlar), yuvarla)
    kdv_t = round(toplam * kdv / 100, yuvarla) if kdv is not None else None
    return {"satirlar": satirlar, "eslesmeyen": eslesmeyen, "gruplar": gruplar,
            "ozet": {"toplam_kdv_haric": toplam, "kdv_orani": kdv, "kdv": kdv_t,
                     "genel_toplam": round(toplam + kdv_t, yuvarla) if kdv_t is not None else None,
                     "kar_genel_gider_uygulanan_%": kar, "kalem": len(satirlar), "eslesmeyen": len(eslesmeyen),
                     "guven": "🔴 eşleşmeyen poz var — toplam eksik" if eslesmeyen else ("🟡" if any(s["guven"] == "🟡" for s in satirlar) else "🟢")}}


def yaz(s, yol, baslik="KEŞİF ÖZETİ (Yaklaşık Maliyet)"):
    k = [["Sıra", "İş Grubu", "Poz No", "Tanım", "Birim", "Miktar", "Birim Fiyat (TL)", "Tutar (TL)", "Kaynak", "Güven"]]
    for i, r in enumerate(s["satirlar"], 2):
        k.append([r["sira"], r["grup"], r["poz"], r["tanim"], r["birim"], H(r["miktar"], sayi=2), H(r["birim_fiyat"], sayi=2),
                  H(r["tutar"], formul=f"F{i}*G{i}", sayi=2), r["kaynak"], r["guven"]])
    n = len(k)
    k.append([H("TOPLAM (KDV hariç)", kalin=True), "", "", "", "", "", "", H(s["ozet"]["toplam_kdv_haric"], formul=f"SUM(H2:H{n})", sayi=2, kalin=True), "", s["ozet"]["guven"]])
    if s["ozet"]["kdv_orani"] is not None:
        k.append([H(f"KDV %{s['ozet']['kdv_orani']:g}", kalin=True), "", "", "", "", "", "", H(s["ozet"]["kdv"], formul=f"H{n+1}*{s['ozet']['kdv_orani']}/100", sayi=2, kalin=True)])
        k.append([H("GENEL TOPLAM", kalin=True), "", "", "", "", "", "", H(s["ozet"]["genel_toplam"], formul=f"H{n+1}+H{n+2}", sayi=2, kalin=True)])
    g = [["İş Grubu", "Tutar (TL)", "Oran"]]
    for ad, t in s["gruplar"].items():
        g.append([ad, H(t, sayi=2), H(t / s["ozet"]["toplam_kdv_haric"] if s["ozet"]["toplam_kdv_haric"] else 0, sayi="pct")])
    g.append([H("Toplam", kalin=True), H(s["ozet"]["toplam_kdv_haric"], sayi=2, kalin=True), H(1, sayi="pct", kalin=True)])
    e = [["Sıra", "Poz No", "Tanım", "Birim", "Miktar", "Not"]] + [[x["sira"], x["poz"], x["tanim"], x["birim"], x["miktar"], "🔴 listede yok — poz_bul.py ile eşle veya fiyat_analizi.py ile özel poz"] for x in s["eslesmeyen"]]
    o = [["Kalem", "Değer"], ["Başlık", baslik], ["Kalem sayısı", s["ozet"]["kalem"]], ["Eşleşmeyen", s["ozet"]["eslesmeyen"]],
         ["Kâr ve genel gider uygulanan %", s["ozet"]["kar_genel_gider_uygulanan_%"]],
         ["Toplam (KDV hariç)", H(s["ozet"]["toplam_kdv_haric"], sayi=2)], ["KDV", H(s["ozet"]["kdv"], sayi=2) if s["ozet"]["kdv"] is not None else "— (oran verilmedi)"],
         ["Genel toplam", H(s["ozet"]["genel_toplam"], sayi=2) if s["ozet"]["genel_toplam"] is not None else "—"], ["Güven", s["ozet"]["guven"]],
         ["Not", "Yaklaşık maliyet gizlidir (Yapım İşleri İhaleleri Uygulama Yön. md.9). Birim fiyatlar kullanıcının verdiği listeden alınmıştır; skill fiyat üretmez."]]
    xlsx_io.yaz(yol, [("Keşif Özeti", k), ("İş Grupları", g), ("Eşleşmeyen", e), ("Özet", o)])
    return yol


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("metraj", nargs="?"); ap.add_argument("liste", nargs="?")
    ap.add_argument("--cikti", default="kesif_ozeti.xlsx"); ap.add_argument("--kdv", type=float)
    ap.add_argument("--kar", type=float, default=0.0, help="kâr ve genel gider %% (ÇŞB listesi için 0, rayiç analizinden gelen fiyatta 25)")
    ap.add_argument("--fiyat-metrajdan", action="store_true"); ap.add_argument("--ornek", action="store_true")
    ap.add_argument("--baslik", default="KEŞİF ÖZETİ (Yaklaşık Maliyet)")
    a = ap.parse_args()
    if a.ornek or not a.metraj:
        print("(örnek metraj + örnek liste)")
        m = yukle_metraj([dict(zip(ORNEK_METRAJ[0], r)) for r in ORNEK_METRAJ[1:]])
        l = yukle_liste([dict(zip(ORNEK_LISTE[0], r)) for r in ORNEK_LISTE[1:]])
    else:
        m = yukle_metraj(xlsx_io.oku_tablo(*xlsx_io.yukle_argv(a.metraj)))
        l = yukle_liste(xlsx_io.oku_tablo(*xlsx_io.yukle_argv(a.liste))) if a.liste else {}
    s = hesapla(m, l, kar=a.kar, kdv=a.kdv, fiyat_metrajdan=a.fiyat_metrajdan)
    yaz(s, a.cikti, a.baslik)
    print(json.dumps({"ozet": s["ozet"], "gruplar": s["gruplar"], "eslesmeyen": s["eslesmeyen"]}, ensure_ascii=False, indent=2))
    print(f"\nKEŞİF → {a.cikti}   toplam {ortak.tl(s['ozet']['toplam_kdv_haric'])} TL (KDV hariç)  {s['ozet']['guven']}")
    for ad, t in s["gruplar"].items():
        print(f"  {ad:<28} {ortak.tl(t):>18}")
    if s["eslesmeyen"]:
        print("  🔴 Eşleşmeyen:", ", ".join(x["poz"] for x in s["eslesmeyen"]))


if __name__ == "__main__":
    main()
