#!/usr/bin/env python3
"""Ortak yardımcılar: Türkçe normalizasyon, kolon tanıma, sayı biçimi, güven etiketi."""
import re
import unicodedata

_TR = str.maketrans("İIıŞşĞğÜüÖöÇçØø", "iiissgguuooccoo")

# Başlık eş anlamlıları (küçük harf, normalize)
KOLON = {
    "poz":    ["poz", "poz no", "pozno", "poz numarasi", "poz nu", "no", "kod", "birim fiyat no", "bf no"],
    "tanim":  ["tanim", "aciklama", "imalat", "tarif", "is kalemi", "isin adi", "birim fiyat tarifi", "imalatin cinsi", "yapilan is"],
    "birim":  ["birim", "olcu birimi", "br", "olcu"],
    "fiyat":  ["birim fiyat", "birim fiyati", "fiyat", "b fiyat", "bf", "sozlesme birim fiyati", "teklif birim fiyati", "rayic", "rayic bedeli"],
    "miktar": ["miktar", "metraj", "adet", "kumulatif miktar", "toplam miktar", "sozlesme miktari"],
    "grup":   ["is grubu", "grup", "bolum", "kisim", "is grubu adi"],
    "kaynak": ["kaynak", "kurum", "yayin", "liste"],
    "yil":    ["yil", "yili", "donem"],
    "tur":    ["tur", "cins", "girdi turu", "kalem turu"],
    "rayic_no": ["rayic no", "rayic poz", "girdi no", "rayic kodu"],
}


def norm(s):
    """Küçük harf, Türkçe karakter sadeleştirme, noktalama → boşluk, çoklu boşluk tek."""
    if s is None:
        return ""
    s = str(s).translate(_TR).lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9/.,%+-]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\b([a-z])\s+(?=\d)", r"\1", s)          # "c 25/30" → "c25/30", "o 8" → "o8"
    s = re.sub(r"(\d)\s*-\s*(?=[a-z]?\d)", r"\1 ", s)      # "8- o12" → "8 o12" (aralık iki ayrı terim)
    return s


def kolon_bul(basliklar, anahtar, zorunlu=False):
    """Başlık listesinde KOLON[anahtar] eş anlamlılarından birini bul; orijinal başlığı döndür."""
    nb = {norm(b): b for b in basliklar if b is not None}
    for aday in KOLON[anahtar]:
        if aday in nb:
            return nb[aday]
    # kısmi eşleşme (ör. "birim fiyat (tl)")
    for aday in KOLON[anahtar]:
        for n, b in nb.items():
            if n.startswith(aday) or n.endswith(aday):
                return b
    if zorunlu:
        raise KeyError(f"'{anahtar}' kolonu bulunamadı. Başlıklar: {list(basliklar)}. Kabul edilenler: {KOLON[anahtar]}")
    return None


def sayi(v, varsayilan=0.0):
    if v is None or v == "":
        return varsayilan
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip().replace(" ", "")
    if re.fullmatch(r"-?[\d.]+,\d+", t):
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return varsayilan


def tl(x, ondalik=2):
    """1234567.891 → '1.234.567,89'"""
    s = f"{x:,.{ondalik}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def guven(skor):
    return "🟢" if skor >= 0.80 else ("🟡" if skor >= 0.50 else "🔴")


def poz_bolumu(poz):
    """'Y.16.050/03' → 'Y.16' ; '15.140/2' → '15' ; 'KGM/16.100' → 'KGM/16' ; 'ÖBF-001' → 'ÖBF'"""
    p = str(poz).strip()
    m = re.match(r"^([A-ZÖÇŞİĞÜa-z]+[/-]?\d{0,3})|^(\d{2})", p)
    if m:
        return (m.group(1) or m.group(2)).rstrip("/-.")
    return p.split(".")[0]


# ---------- birimler ----------
_BIRIM_ES = {"m3": "m³", "m³": "m³", "metrekup": "m³", "m2": "m²", "m²": "m²", "metrekare": "m²", "mt": "m", "m": "m", "metre": "m",
             "kg": "kg", "kilogram": "kg", "ton": "ton", "t": "ton", "gr": "g", "g": "g", "ad": "ad", "adet": "ad", "ad.": "ad",
             "sa": "sa", "saat": "sa", "gun": "gün", "gün": "gün", "lt": "l", "l": "l", "litre": "l", "km": "km", "cm": "cm", "mm": "mm",
             "tk": "takım", "takim": "takım", "takım": "takım", "cift": "çift", "çift": "çift", "kva": "kVA", "kw": "kW"}
_CEVRIM = {("kg", "ton"): 0.001, ("ton", "kg"): 1000.0, ("g", "kg"): 0.001, ("kg", "g"): 1000.0,
           ("cm", "m"): 0.01, ("m", "cm"): 100.0, ("mm", "m"): 0.001, ("m", "mm"): 1000.0, ("m", "km"): 0.001, ("km", "m"): 1000.0,
           ("l", "m³"): 0.001, ("m³", "l"): 1000.0, ("gün", "sa"): 8.0, ("sa", "gün"): 0.125}


def birim_norm(b):
    if b is None:
        return None
    k = str(b).strip().lower().replace("³", "3").replace("²", "2")
    k = k.translate(_TR) if k not in ("m3", "m2") else k
    return _BIRIM_ES.get(k, _BIRIM_ES.get(str(b).strip().lower(), str(b).strip()))


def birim_cevir(miktar, kaynak_birim, hedef_birim):
    """metraj birimi → liste birimi. Döner: (yeni miktar, çarpan, not) ; çevrim yoksa (miktar, None, not)."""
    a, b = birim_norm(kaynak_birim), birim_norm(hedef_birim)
    if a is None or b is None or a == b:
        return miktar, 1.0, None
    c = _CEVRIM.get((a, b))
    if c is None:
        return miktar, None, f"birim uyuşmazlığı ({kaynak_birim} → {hedef_birim}), çevrim yok"
    return miktar * c, c, f"{kaynak_birim} → {hedef_birim} ×{c:g}"
