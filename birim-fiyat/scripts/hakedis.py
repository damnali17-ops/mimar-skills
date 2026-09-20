#!/usr/bin/env python3
"""Hakediş raporu — Yapım İşleri Genel Şartnamesi (YİGŞ) md.39–41 + 4735 sayılı KİSK md.24 (iş artışı sınırı).

Kullanım:
  python3 hakedis.py sozlesme.xlsx metraj.xlsx --no 3 --onceki 4850000 [--kdv 20] [--fiyat-farki 203231.25]
         [--avans-mahsup 0] [--damga 0.948] [--stopaj 0] [--ceza 0] [--is-artisi 20] [--cikti hakedis_3.xlsx]
  python3 hakedis.py --ornek

Sözleşme kolonları : Poz No · Tanım · Birim · Sözleşme Miktarı · Sözleşme Birim Fiyatı · [İş Grubu]
Metraj kolonları   : Poz No · Kümülatif Miktar   (işin başından bu hakediş sonuna kadar yapılan toplam)
Mantık (YİGŞ md.39): kümülatif imalat tutarı = Σ kümülatif miktar × sözleşme birim fiyatı
                     bu hakediş = kümülatif − önceki hakediş(ler) kümülatifi
İcmal: imalat + fiyat farkı = brüt → − avans mahsubu − ceza − diğer kesintiler → KDV → damga vergisi, stopaj → ÖDENECEK
Oranlar (KDV, damga, stopaj) sözleşme/mevzuata göre KULLANICI verir; varsayılan 0 = satır boş. Skill oran uydurmaz.
İş artışı: kümülatif miktar > sözleşme miktarı → satır 🟡; toplam > sözleşme bedeli × (1+%is-artisi) → 🔴 (KİSK md.24 onay gerekir).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak
import xlsx_io
from xlsx_io import Hucre as H

ORNEK_SOZ = [["Poz No", "Tanım", "Birim", "Sözleşme Miktarı", "Sözleşme Birim Fiyatı", "İş Grubu"],
             ["Y.15.001/2B", "Makine ile kazı", "m³", 1250, 58.00, "Kazı"],
             ["Y.16.050/04", "C25/30 beton", "m³", 410.5, 2750.00, "Betonarme"],
             ["Y.21.001/03", "Plywood kalıp", "m²", 2380, 560.00, "Betonarme"],
             ["Y.23.014", "Ø8-12 nervürlü çelik", "ton", 38.2, 39800.00, "Betonarme"]]
ORNEK_MET = [["Poz No", "Kümülatif Miktar"], ["Y.15.001/2B", 1250], ["Y.16.050/04", 300], ["Y.21.001/03", 1900], ["Y.23.014", 41.0]]


def yukle_sozlesme(satirlar):
    b = list(satirlar[0].keys())
    kp = ortak.kolon_bul(b, "poz", zorunlu=True); kt = ortak.kolon_bul(b, "tanim"); kb = ortak.kolon_bul(b, "birim")
    km = next((x for x in b if "sozlesme miktar" in ortak.norm(x)), None) or ortak.kolon_bul(b, "miktar", zorunlu=True)
    kf = next((x for x in b if "sozlesme birim" in ortak.norm(x) or "teklif birim" in ortak.norm(x)), None) or ortak.kolon_bul(b, "fiyat", zorunlu=True)
    kg = ortak.kolon_bul(b, "grup")
    out = []
    for r in satirlar:
        if r.get(kp) in (None, ""):
            continue
        out.append({"poz": str(r[kp]).strip(), "tanim": r.get(kt) if kt else None, "birim": r.get(kb) if kb else None,
                    "soz_miktar": ortak.sayi(r.get(km)), "soz_bf": ortak.sayi(r.get(kf)), "grup": r.get(kg) if kg else None})
    return out


def yukle_metraj(satirlar):
    b = list(satirlar[0].keys())
    kp = ortak.kolon_bul(b, "poz", zorunlu=True)
    km = next((x for x in b if "kumulatif" in ortak.norm(x)), None) or ortak.kolon_bul(b, "miktar", zorunlu=True)
    return {ortak.norm(r[kp]): ortak.sayi(r.get(km)) for r in satirlar if r.get(kp) not in (None, "")}


def hesapla(soz, met, no, onceki, kdv=0, fiyat_farki=0, avans=0, damga=0, stopaj=0, ceza=0, diger=0, is_artisi=20, yuvarla=2):
    satirlar, uyarilar = [], []
    for s in soz:
        kum = met.get(ortak.norm(s["poz"]), 0.0)
        tutar = round(kum * s["soz_bf"], yuvarla)
        g = "🟢"
        if kum > s["soz_miktar"] + 1e-9:
            g = "🟡"; uyarilar.append(f"🟡 {s['poz']}: kümülatif {kum:g} > sözleşme {s['soz_miktar']:g} {s['birim'] or ''} — iş artışı kalemi (YİGŞ md.21/22, KİSK md.24)")
        satirlar.append({**s, "kum_miktar": kum, "kum_tutar": tutar, "gerceklesme": round(kum / s["soz_miktar"], 4) if s["soz_miktar"] else None, "guven": g})
    listede_yok = [p for p in met if p not in {ortak.norm(s["poz"]) for s in soz}]
    if listede_yok:
        uyarilar.append(f"🔴 Metrajda olup sözleşmede olmayan poz: {', '.join(listede_yok)} — yeni birim fiyat tutanağı (YİGŞ md.22) gerekir; tutara alınmadı")
    soz_bedeli = round(sum(s["soz_miktar"] * s["soz_bf"] for s in soz), yuvarla)
    kum_toplam = round(sum(s["kum_tutar"] for s in satirlar), yuvarla)
    if soz_bedeli and kum_toplam > soz_bedeli * (1 + is_artisi / 100) + 1e-6:
        uyarilar.append(f"🔴 Kümülatif imalat {ortak.tl(kum_toplam)} > sözleşme bedeli × (1+%{is_artisi:g}) = {ortak.tl(soz_bedeli*(1+is_artisi/100))} — KİSK md.24 sınırı aşılıyor, onay/ek sözleşme olmadan ödenemez")
    bu_imalat = round(kum_toplam - onceki, yuvarla)
    if bu_imalat < 0:
        uyarilar.append(f"🔴 Bu hakediş imalatı negatif ({ortak.tl(bu_imalat)}): önceki hakediş tutarı veya metraj hatalı")
    brut = round(bu_imalat + fiyat_farki, yuvarla)
    kesinti_oncesi = round(brut - avans - ceza - diger, yuvarla)
    kdv_t = round(kesinti_oncesi * kdv / 100, yuvarla)
    kdv_dahil = round(kesinti_oncesi + kdv_t, yuvarla)
    damga_t = round(brut * damga / 100, yuvarla)          # damga vergisi hakediş tutarı (KDV hariç) üzerinden 🟡
    stopaj_t = round(brut * stopaj / 100, yuvarla)        # yıllara sâri iş stopajı (KDV hariç) 🟡
    odenecek = round(kdv_dahil - damga_t - stopaj_t, yuvarla)
    return {"hakedis_no": no, "satirlar": satirlar, "uyarilar": uyarilar,
            "icmal": {"sozlesme_bedeli": soz_bedeli, "kumulatif_imalat": kum_toplam, "gerceklesme_orani": round(kum_toplam / soz_bedeli, 4) if soz_bedeli else None,
                      "onceki_hakedisler": onceki, "bu_hakedis_imalat": bu_imalat, "fiyat_farki": fiyat_farki, "brut": brut,
                      "avans_mahsubu": avans, "ceza": ceza, "diger_kesinti": diger, "kdv_matrahi": kesinti_oncesi,
                      "kdv_orani": kdv, "kdv": kdv_t, "kdv_dahil": kdv_dahil, "damga_orani": damga, "damga_vergisi": damga_t,
                      "stopaj_orani": stopaj, "stopaj": stopaj_t, "odenecek": odenecek,
                      "guven": "🔴" if any(u.startswith("🔴") for u in uyarilar) else ("🟡" if uyarilar else "🟢")}}


def yaz(h, yol):
    t = [["Sıra", "İş Grubu", "Poz No", "Tanım", "Birim", "Sözleşme Miktarı", "Sözleşme BF", "Sözleşme Tutarı", "Kümülatif Miktar", "Kümülatif Tutar", "Gerçekleşme", "Güven"]]
    for i, s in enumerate(h["satirlar"], 2):
        t.append([i - 1, s["grup"], s["poz"], s["tanim"], s["birim"], H(s["soz_miktar"], sayi=2), H(s["soz_bf"], sayi=2),
                  H(round(s["soz_miktar"] * s["soz_bf"], 2), formul=f"F{i}*G{i}", sayi=2), H(s["kum_miktar"], sayi=2),
                  H(s["kum_tutar"], formul=f"I{i}*G{i}", sayi=2), H(s["gerceklesme"], sayi="pct"), s["guven"]])
    n = len(t)
    t.append([H("TOPLAM", kalin=True), "", "", "", "", "", "", H(h["icmal"]["sozlesme_bedeli"], formul=f"SUM(H2:H{n})", sayi=2, kalin=True), "",
              H(h["icmal"]["kumulatif_imalat"], formul=f"SUM(J2:J{n})", sayi=2, kalin=True), H(h["icmal"]["gerceklesme_orani"], sayi="pct", kalin=True)])
    ic = h["icmal"]
    def satir(ad, deger, kalin=False, oran=None):
        return [H(ad, kalin=kalin), H(deger, sayi=2, kalin=kalin), (f"%{oran:g}" if oran is not None else "")]
    i = [["Kalem", "Tutar (TL)", "Oran"],
         satir("Sözleşme bedeli", ic["sozlesme_bedeli"]),
         satir("Kümülatif imalat (A)", ic["kumulatif_imalat"], True),
         satir("Önceki hakedişler kümülatifi (B)", ic["onceki_hakedisler"]),
         satir(f"Bu hakediş imalatı (A−B) — No {h['hakedis_no']}", ic["bu_hakedis_imalat"], True),
         satir("Fiyat farkı (+)", ic["fiyat_farki"]),
         satir("Brüt hakediş", ic["brut"], True),
         satir("Avans mahsubu (−)", ic["avans_mahsubu"]),
         satir("Ceza (−)", ic["ceza"]),
         satir("Diğer kesinti (−)", ic["diger_kesinti"]),
         satir("KDV matrahı", ic["kdv_matrahi"], True),
         satir("KDV (+)", ic["kdv"], oran=ic["kdv_orani"]),
         satir("KDV dahil tutar", ic["kdv_dahil"], True),
         satir("Damga vergisi (−)", ic["damga_vergisi"], oran=ic["damga_orani"]),
         satir("Stopaj (−)", ic["stopaj"], oran=ic["stopaj_orani"]),
         satir("ÖDENECEK", ic["odenecek"], True),
         ["Güven", ic["guven"], ""], [],
         ["Uyarılar"]] + [[u] for u in h["uyarilar"]] + [[],
         ["Not: Oranlar kullanıcı girdisidir; 0 ise sözleşme/mevzuattan alınmalıdır. Bu tablo YİGŞ md.39 ara hakediş düzenine göre ön-hesaptır; idarenin kontrol teşkilatı onayı esastır."]]
    xlsx_io.yaz(yol, [(f"Hakediş {h['hakedis_no']}", t), ("İcmal", i)])
    return yol


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sozlesme", nargs="?"); ap.add_argument("metraj", nargs="?")
    ap.add_argument("--no", type=int, default=1); ap.add_argument("--onceki", type=float, default=0.0, help="önceki hakedişler kümülatif imalat tutarı (KDV hariç)")
    ap.add_argument("--kdv", type=float, default=0); ap.add_argument("--fiyat-farki", type=float, default=0)
    ap.add_argument("--avans-mahsup", type=float, default=0); ap.add_argument("--damga", type=float, default=0, help="%% (ör. 0.948)")
    ap.add_argument("--stopaj", type=float, default=0, help="%% yıllara sâri iş stopajı"); ap.add_argument("--ceza", type=float, default=0)
    ap.add_argument("--diger", type=float, default=0); ap.add_argument("--is-artisi", type=float, default=20, help="%% (birim fiyat 20, anahtar teslim 10)")
    ap.add_argument("--cikti"); ap.add_argument("--ornek", action="store_true")
    a = ap.parse_args()
    if a.ornek or not a.sozlesme:
        print("(örnek sözleşme + metraj — fiyatlar gerçek değil)")
        soz = yukle_sozlesme([dict(zip(ORNEK_SOZ[0], r)) for r in ORNEK_SOZ[1:]])
        met = yukle_metraj([dict(zip(ORNEK_MET[0], r)) for r in ORNEK_MET[1:]])
        if a.onceki == 0: a.onceki = 1200000.0
        if a.no == 1: a.no = 2
    else:
        soz = yukle_sozlesme(xlsx_io.oku_tablo(*xlsx_io.yukle_argv(a.sozlesme)))
        met = yukle_metraj(xlsx_io.oku_tablo(*xlsx_io.yukle_argv(a.metraj)))
    h = hesapla(soz, met, a.no, a.onceki, a.kdv, a.fiyat_farki, a.avans_mahsup, a.damga, a.stopaj, a.ceza, a.diger, a.is_artisi)
    yol = a.cikti or f"hakedis_{a.no}.xlsx"
    yaz(h, yol)
    print(json.dumps({"icmal": h["icmal"], "uyarilar": h["uyarilar"]}, ensure_ascii=False, indent=2))
    ic = h["icmal"]
    print(f"\nHAKEDİŞ No {h['hakedis_no']} → {yol}")
    print(f"  Kümülatif imalat   {ortak.tl(ic['kumulatif_imalat']):>18}   gerçekleşme %{(ic['gerceklesme_orani'] or 0)*100:.1f}")
    print(f"  Önceki hakedişler  {ortak.tl(ic['onceki_hakedisler']):>18}")
    print(f"  Bu hakediş imalat  {ortak.tl(ic['bu_hakedis_imalat']):>18}")
    print(f"  Fiyat farkı        {ortak.tl(ic['fiyat_farki']):>18}")
    print(f"  KDV %{ic['kdv_orani']:g}            {ortak.tl(ic['kdv']):>18}" + ("   (oran verilmedi — tutar KDV hariç)" if not ic['kdv_orani'] else ""))
    print(f"  ÖDENECEK           {ortak.tl(ic['odenecek']):>18}   {ic['guven']}")
    for u in h["uyarilar"]:
        print("  ", u)


if __name__ == "__main__":
    main()
