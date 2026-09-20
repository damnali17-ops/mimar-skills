#!/usr/bin/env python3
"""Salt-stdlib xlsx/csv okuma-yazma — birim-fiyat araçlarının ortak modülü.

Okuma:  oku(yol, sayfa=None) -> list[list]  (ilk sayfa ya da ad/indeks ile)
        oku_tablo(yol, sayfa=None) -> list[dict]  (ilk satır başlık)
Yazma:  yaz(yol, sayfalar)  sayfalar = {"Ad": [[hücre, ...], ...]} veya list of (ad, satırlar)
        Hücre: str | int | float | None | Hucre(deger, kalin=False, sayi=None, formul=None)
Sadece zipfile + xml.etree. openpyxl gerekmez. .csv uzantısı verilirse CSV (noktalı virgül) kullanılır.
"""
import csv
import io
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "p": "http://schemas.openxmlformats.org/package/2006/relationships"}


class Hucre:
    """Biçimli hücre. sayi: None | 0 | 2 | 4 (ondalık) | 'pct'. formul: 'SUM(C2:C9)' gibi (başında = yok)."""
    def __init__(self, deger=None, kalin=False, sayi=None, formul=None):
        self.deger, self.kalin, self.sayi, self.formul = deger, kalin, sayi, formul


# ---------- yardımcılar ----------
def _kolon_no(harf):
    n = 0
    for ch in harf:
        n = n * 26 + (ord(ch.upper()) - 64)
    return n


def kolon_harf(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _sayiya(s):
    if s is None:
        return None
    t = str(s).strip()
    if t == "":
        return None
    try:
        if re.fullmatch(r"-?\d+", t):
            return int(t)
        return float(t)
    except ValueError:
        pass
    # Türkçe biçim: 1.234,56
    t2 = t.replace(".", "").replace(",", ".") if re.fullmatch(r"-?[\d.]+,\d+", t) else t.replace(",", ".")
    try:
        return float(t2)
    except ValueError:
        return s


# ---------- okuma ----------
def _sayfalar(z):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels.findall("p:Relationship", NS)}
    out = []
    for s in wb.find("m:sheets", NS).findall("m:sheet", NS):
        rid = s.get("{%s}id" % NS["r"])
        hedef = rmap.get(rid, "")
        if not hedef.startswith("/"):
            hedef = "xl/" + hedef
        out.append((s.get("name"), hedef.lstrip("/")))
    return out


def _paylasilan(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("m:si", NS):
        out.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    return out


def oku(yol, sayfa=None, sayisal=True):
    """Ham satır listesi. sayfa: None (ilk) | int indeks | sayfa adı."""
    if yol.lower().endswith((".csv", ".txt")):
        with open(yol, encoding="utf-8-sig", newline="") as f:
            dial = csv.Sniffer().sniff(f.read(4096), delimiters=";,\t") if os.path.getsize(yol) else csv.excel
            f.seek(0)
            satirlar = [[(_sayiya(c) if sayisal else c) for c in r] for r in csv.reader(f, dial)]
        return satirlar
    with zipfile.ZipFile(yol) as z:
        sayfalar = _sayfalar(z)
        if sayfa is None:
            ad, yol_ic = sayfalar[0]
        elif isinstance(sayfa, int):
            ad, yol_ic = sayfalar[sayfa]
        else:
            eslesen = [s for s in sayfalar if s[0] == sayfa]
            if not eslesen:
                raise KeyError(f"sayfa yok: {sayfa}; mevcut: {[s[0] for s in sayfalar]}")
            ad, yol_ic = eslesen[0]
        ss = _paylasilan(z)
        root = ET.fromstring(z.read(yol_ic))
        satirlar = []
        for row in root.iter("{%s}row" % NS["m"]):
            r = []
            for c in row.findall("m:c", NS):
                ref = re.match(r"([A-Z]+)(\d+)", c.get("r") or "")
                idx = _kolon_no(ref.group(1)) - 1 if ref else len(r)
                while len(r) < idx:
                    r.append(None)
                t = c.get("t")
                v = c.find("m:v", NS)
                if t == "s":
                    deger = ss[int(v.text)] if v is not None else None
                elif t == "inlineStr":
                    deger = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif t == "b":
                    deger = bool(int(v.text)) if v is not None else None
                elif t in ("str", "e"):
                    deger = v.text if v is not None else None
                else:
                    deger = _sayiya(v.text) if (v is not None and sayisal) else (v.text if v is not None else None)
                r.append(deger)
            satirlar.append(r)
        return satirlar


def oku_tablo(yol, sayfa=None, baslik_satiri=0):
    """İlk (veya baslik_satiri) satırı başlık kabul edip dict listesi döner. Başlıklar kırpılır."""
    satirlar = oku(yol, sayfa)
    if not satirlar:
        return []
    basliklar = [str(h).strip() if h is not None else f"kolon{i+1}" for i, h in enumerate(satirlar[baslik_satiri])]
    out = []
    for r in satirlar[baslik_satiri + 1:]:
        if not any(c not in (None, "") for c in r):
            continue
        d = {basliklar[i]: (r[i] if i < len(r) else None) for i in range(len(basliklar))}
        out.append(d)
    return out


def sayfa_adlari(yol):
    with zipfile.ZipFile(yol) as z:
        return [s[0] for s in _sayfalar(z)]


# ---------- yazma ----------
_STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="3"><numFmt numFmtId="164" formatCode="#,##0.00"/><numFmt numFmtId="165" formatCode="#,##0.0000"/><numFmt numFmtId="166" formatCode="0.00%"/></numFmts>
<fonts count="2"><font><sz val="10"/><name val="Arial"/></font><font><b/><sz val="10"/><name val="Arial"/></font></fonts>
<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FFE7E6E6"/></patternFill></fill></fills>
<borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border><left style="thin"/><right style="thin"/><top style="thin"/><bottom style="thin"/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="10">
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
<xf numFmtId="164" fontId="1" fillId="2" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="1" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
<xf numFmtId="1" fontId="1" fillId="2" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
<xf numFmtId="165" fontId="1" fillId="2" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="166" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
<xf numFmtId="166" fontId="1" fillId="2" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""

_STIL = {(None, False): 0, (None, True): 1, (2, False): 2, (2, True): 3, (0, False): 4, (0, True): 5,
         (4, False): 6, (4, True): 7, ("pct", False): 8, ("pct", True): 9}


def _hucre_xml(ref, h):
    if not isinstance(h, Hucre):
        h = Hucre(h)
    s = _STIL.get((h.sayi, bool(h.kalin)), 1 if h.kalin else 0)
    if h.formul:
        v = h.deger
        onbellek = f"<v>{repr(float(v)) if isinstance(v, float) else v}</v>" if isinstance(v, (int, float)) and not isinstance(v, bool) else ""
        return f'<c r="{ref}" s="{s}"><f>{escape(str(h.formul))}</f>{onbellek}</c>'
    v = h.deger
    if v is None or v == "":
        return f'<c r="{ref}" s="{s}"/>'
    if isinstance(v, bool):
        return f'<c r="{ref}" s="{s}" t="b"><v>{int(v)}</v></c>'
    if isinstance(v, (int, float)):
        return f'<c r="{ref}" s="{s}"><v>{repr(float(v)) if isinstance(v, float) else v}</v></c>'
    metin = escape(str(v)).replace("\n", "&#10;")
    return f'<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{metin}</t></is></c>'


def _sayfa_xml(satirlar, genislikler=None):
    kol_sayisi = max((len(r) for r in satirlar), default=1)
    cols = ""
    if genislikler is None:
        genislikler = {}
        for r in satirlar[:200]:
            for i, h in enumerate(r):
                v = h.deger if isinstance(h, Hucre) else h
                uz = len(str(v)) if v is not None else 0
                genislikler[i + 1] = min(max(genislikler.get(i + 1, 8), uz + 2), 60)
    if genislikler:
        cols = "<cols>" + "".join(f'<col min="{k}" max="{k}" width="{w}" customWidth="1"/>' for k, w in sorted(genislikler.items())) + "</cols>"
    rows = []
    for i, r in enumerate(satirlar, 1):
        hs = "".join(_hucre_xml(f"{kolon_harf(j)}{i}", h) for j, h in enumerate(r, 1))
        rows.append(f'<row r="{i}">{hs}</row>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<worksheet xmlns="{NS["m"]}" xmlns:r="{NS["r"]}">'
            f'<sheetPr><outlinePr summaryBelow="0"/></sheetPr><dimension ref="A1:{kolon_harf(kol_sayisi)}{max(len(satirlar),1)}"/>'
            f'<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
            f'<sheetFormatPr defaultRowHeight="15"/>{cols}<sheetData>{"".join(rows)}</sheetData></worksheet>')


def yaz(yol, sayfalar, genislikler=None):
    """sayfalar: dict {ad: satırlar} veya [(ad, satırlar), ...]. .csv ise sadece ilk sayfa yazılır."""
    if isinstance(sayfalar, dict):
        sayfalar = list(sayfalar.items())
    if yol.lower().endswith(".csv"):
        ad, satirlar = sayfalar[0]
        with open(yol, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";")
            for r in satirlar:
                w.writerow([(h.deger if isinstance(h, Hucre) else h) for h in r])
        return yol
    with zipfile.ZipFile(yol, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                   + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sayfalar) + 1))
                   + '</Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml",
                   f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   f'<workbook xmlns="{NS["m"]}" xmlns:r="{NS["r"]}"><sheets>'
                   + "".join(f'<sheet name="{escape(ad[:31])}" sheetId="{i}" r:id="rId{i}"/>' for i, (ad, _) in enumerate(sayfalar, 1))
                   + '</sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(sayfalar) + 1))
                   + f'<Relationship Id="rId{len(sayfalar)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
        z.writestr("xl/styles.xml", _STYLES)
        for i, (ad, satirlar) in enumerate(sayfalar, 1):
            g = genislikler.get(ad) if isinstance(genislikler, dict) else None
            z.writestr(f"xl/worksheets/sheet{i}.xml", _sayfa_xml(satirlar, g))
    return yol


def yukle_argv(argv):
    """CLI yardımcı: 'dosya.xlsx[:Sayfa]' → (yol, sayfa)"""
    if ":" in argv and not re.match(r"^[A-Za-z]:\\", argv):
        yol, sayfa = argv.rsplit(":", 1)
        return yol, (int(sayfa) if sayfa.isdigit() else sayfa)
    return argv, None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    yol, sayfa = yukle_argv(sys.argv[1])
    for r in oku(yol, sayfa)[:20]:
        print(r)
