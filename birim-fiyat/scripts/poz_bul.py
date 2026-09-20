#!/usr/bin/env python3
"""Poz bulma / tarif eşleştirme — kullanıcının verdiği birim fiyat listesinde arama.

Kullanım:
  python3 poz_bul.py liste.xlsx "C30/37 basınç dayanımında beton"          # tek sorgu
  python3 poz_bul.py liste.xlsx --dosya metraj.xlsx [--cikti eslesme.xlsx]   # metrajdaki tarifleri toplu eşle
  python3 poz_bul.py liste.xlsx "kazı" --adet 8 --bolum Y.15               # bölüm filtresi

Liste kolonları (başlık eş anlamlıları ortak.KOLON'da): Poz No · Tanım · Birim · Birim Fiyat · [Kaynak] · [Yıl]
Puan: kelime örtüşmesi (Jaccard, ağırlıklı) + dizi benzerliği (difflib) + sayısal terim uyumu (C30, Ø12, 20 cm).
Güven: 🟢 ≥0.80 · 🟡 0.50–0.79 · 🔴 <0.50 (mutlaka elle teyit). Skill hiçbir fiyatı uydurmaz: liste ne diyorsa o.
"""
import argparse
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak
import xlsx_io

DURAK = {"ve", "ile", "veya", "icin", "her", "turlu", "olarak", "olan", "dahil", "haric", "m", "m2", "m3", "kg", "ad", "mt", "ton", "yapilmasi", "temini", "yerine", "konulmasi"}


ES_ANLAM = {"demir": "celik", "celik": "demir", "donati": "celik", "betonarme": "beton", "kazi": "kazilmasi", "kazilmasi": "kazi",
            "dolgu": "dolgusu", "sıva": "siva", "boya": "boyanmasi", "kaplama": "kaplanmasi", "kalip": "kalibi", "kalibi": "kalip",
            "duvar": "duvari", "tugla": "tugla", "seramik": "seramik", "mermer": "mermer", "izolasyon": "yalitim", "yalitim": "izolasyon"}


def genislet(tokens):
    ek = {ES_ANLAM[t] for t in tokens if t in ES_ANLAM}
    return tokens | ek


def sayisal_terimler(n):
    return set(re.findall(r"[a-z]*\d+(?:[.,/]\d+)*[a-z]*", n))


def _kok_eslesir(t, kume):
    """Türkçe ek toleransı: 'pompa' ~ 'pompasiyla' (≥5 harf ortak kök)."""
    if t in kume:
        return True
    if len(t) >= 5 and not re.search(r"\d", t):
        k = t[:5]
        return any(len(x) >= 5 and x[:5] == k for x in kume)
    return False


def _cap_uyumu(sa, sb):
    """'o16' sorgusu, tanımdaki 'o8 o12' / 'o14 o28' aralığına düşüyor mu? None = çap terimi yok."""
    qa = [int(m) for t in sa for m in re.findall(r"^o(\d+)$", t)]
    qb = sorted(int(m) for t in sb for m in re.findall(r"^o(\d+)$", t))
    if not qa or not qb:
        return None
    if len(qb) >= 2:
        return 1.0 if all(qb[0] <= q <= qb[-1] for q in qa) else 0.0
    return 1.0 if set(qa) <= set(qb) else 0.0


def puan(sorgu_n, tanim_n):
    a = {t for t in sorgu_n.split() if t not in DURAK}
    b = genislet({t for t in tanim_n.split() if t not in DURAK})
    if not a or not b:
        return 0.0
    eslesen = {t for t in a if _kok_eslesir(t, b)}
    ortusme = len(eslesen) / len(a)                # sorgunun ne kadarı tanımda (eş anlamlı + kök toleransı)
    jacc = len(eslesen) / len(a | b)
    dizi = difflib.SequenceMatcher(None, sorgu_n, tanim_n).ratio()
    sa, sb = sayisal_terimler(sorgu_n), sayisal_terimler(tanim_n)
    cap = _cap_uyumu(sa, sb)
    if cap is not None:
        sayisal = cap
    else:
        sayisal = 1.0 if not sa else len(sa & sb) / len(sa)
    return round(0.50 * ortusme + 0.10 * jacc + 0.20 * dizi + 0.20 * sayisal, 3)


def listeyi_yukle(yol, sayfa=None):
    satirlar = xlsx_io.oku_tablo(yol, sayfa)
    if not satirlar:
        raise SystemExit("liste boş")
    b = list(satirlar[0].keys())
    k = {a: ortak.kolon_bul(b, a) for a in ("poz", "tanim", "birim", "fiyat", "kaynak", "yil")}
    if not k["poz"] or not k["tanim"]:
        raise SystemExit(f"Poz/Tanım kolonu bulunamadı. Başlıklar: {b}")
    liste = []
    for r in satirlar:
        poz = r.get(k["poz"])
        if poz in (None, ""):
            continue
        liste.append({
            "poz": str(poz).strip(), "tanim": str(r.get(k["tanim"]) or "").strip(),
            "birim": r.get(k["birim"]) if k["birim"] else None,
            "fiyat": ortak.sayi(r.get(k["fiyat"]), None) if k["fiyat"] else None,
            "kaynak": r.get(k["kaynak"]) if k["kaynak"] else None,
            "yil": r.get(k["yil"]) if k["yil"] else None,
            "_n": ortak.norm(r.get(k["tanim"])), "_pn": ortak.norm(poz),
        })
    return liste


def ara(liste, sorgu, adet=5, bolum=None):
    sn = ortak.norm(sorgu)
    sonuc = []
    for p in liste:
        if bolum and not p["_pn"].startswith(ortak.norm(bolum)):
            continue
        if sn == p["_pn"] or sn == p["poz"].lower():
            s = 1.0
        else:
            s = puan(sn, p["_n"])
            if p["_pn"].startswith(sn):
                s = max(s, 0.95)
        if s > 0:
            sonuc.append({**{k: v for k, v in p.items() if not k.startswith("_")}, "puan": s, "guven": ortak.guven(s)})
    sonuc.sort(key=lambda x: -x["puan"])
    return sonuc[:adet]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("liste", help="birim fiyat listesi xlsx/csv[:Sayfa]")
    ap.add_argument("sorgu", nargs="?")
    ap.add_argument("--dosya", help="tarif kolonu olan metraj dosyası — toplu eşleştirme")
    ap.add_argument("--cikti", help="toplu eşleştirme çıktısı xlsx")
    ap.add_argument("--adet", type=int, default=5)
    ap.add_argument("--bolum", help="poz ön eki filtresi (Y.16, 15, KGM)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    liste = listeyi_yukle(*xlsx_io.yukle_argv(a.liste))

    if a.dosya:
        satirlar = xlsx_io.oku_tablo(*xlsx_io.yukle_argv(a.dosya))
        b = list(satirlar[0].keys())
        kt = ortak.kolon_bul(b, "tanim", zorunlu=True)
        kp = ortak.kolon_bul(b, "poz")
        cikti = [["Sıra", "Tarif (girdi)", "Girilen poz", "Önerilen poz", "Tanım (liste)", "Birim", "Birim fiyat", "Puan", "Güven", "2. aday", "2. puan"]]
        for i, r in enumerate(satirlar, 1):
            sorgu = str(r.get(kp) or "") if (kp and r.get(kp)) else str(r.get(kt) or "")
            e = ara(liste, sorgu, adet=2, bolum=a.bolum)
            if kp and r.get(kp) and (not e or e[0]["puan"] < 1.0):
                e = ara(liste, str(r.get(kt) or ""), adet=2, bolum=a.bolum)  # poz listede yok → tarifle ara
            b1 = e[0] if e else {}
            b2 = e[1] if len(e) > 1 else {}
            cikti.append([i, r.get(kt), r.get(kp), b1.get("poz"), b1.get("tanim"), b1.get("birim"),
                          xlsx_io.Hucre(b1.get("fiyat"), sayi=2), b1.get("puan"), b1.get("guven"), b2.get("poz"), b2.get("puan")])
        yol = a.cikti or "poz_eslesme.xlsx"
        xlsx_io.yaz(yol, {"Eşleşme": cikti})
        n = len(cikti) - 1
        kirmizi = sum(1 for r in cikti[1:] if r[8] == "🔴")
        print(f"{n} tarif eşleştirildi → {yol}   (🔴 teyit gereken: {kirmizi})")
        return

    if not a.sorgu:
        ap.print_help(); return
    e = ara(liste, a.sorgu, a.adet, a.bolum)
    if a.json:
        print(json.dumps(e, ensure_ascii=False, indent=2)); return
    print(f"\nSORGU: {a.sorgu}   ({len(liste)} poz tarandı)")
    print("-" * 100)
    for x in e:
        f = ortak.tl(x["fiyat"]) if x["fiyat"] is not None else "—"
        print(f"{x['guven']} {x['puan']:.2f}  {x['poz']:<16} {x['tanim'][:58]:<58} {str(x['birim'] or ''):<5} {f:>14}")
    if not e or e[0]["puan"] < 0.5:
        print("\n🔴 Güçlü eşleşme yok — tarifi sadeleştir (malzeme + sınıf + ölçü) veya --bolum ile daralt.")


if __name__ == "__main__":
    main()
