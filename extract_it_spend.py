#!/usr/bin/env python3
"""
Extract the City of Troy's Information Technology internal-service-fund figures
from every ACFR/CAFR, FY2005-FY2025.

Troy runs IT as an internal service fund, so each ACFR has an
"Internal Service Funds - Combining Statement of Revenues, Expenses and Changes
in Fund Net Assets/Position" with an Information Technology column. We pull:
  - op_expenses : Total operating expenses  (the headline "IT spend" figure;
                  includes depreciation, excludes capital asset purchases)
  - op_revenues : Total operating revenues  (interdepartmental charges billed)

Coordinate-aware via pdfplumber. Two layouts occur and are handled explicitly:

  SINGLE-PAGE  - the whole ISF table fits on one page. The IT column index is
                 found ordinally: header words are clustered into columns by
                 x-position (restricted to the header rows ABOVE "Operating
                 revenues"), and we take the index of the IT column.
  WRAPPED      - the wide table spills onto the next physical page: row LABELS
                 stay on page L, the IT column is the FIRST (leftmost) column
                 on page L+1. Rows align by y-coordinate across the two pages.

Numbers split by pdfplumber ("7,346,699" -> "7," + "346,699") are re-merged.
FY2011's ACFR is scanned; ACFR_2011_ocr.pdf (ocrmypdf) is used if present.

Every figure prints with its full row of numbers for manual verification, and
is written to it_spend.csv.
"""
import csv
import os
import re
import sys

import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(HERE, "acfr_pdf")
YEARS = range(2005, 2026)
FUND_WORDS = {"compensated", "absences", "unemployment", "compensation", "custodial",
              "services", "information", "technology", "motor", "equipment", "pool",
              "workers", "worker's", "total", "data", "processing"}
NUM_TOK = re.compile(r"^\(?\$?\d{1,3}(?:,\d{3})*\)?$")


def pdf_path(year):
    ocr = os.path.join(PDF_DIR, f"ACFR_{year}_ocr.pdf")
    return ocr if os.path.exists(ocr) else os.path.join(PDF_DIR, f"ACFR_{year}.pdf")


def rows_by_top(page):
    buckets = {}
    for w in page.extract_words(keep_blank_chars=False):
        buckets.setdefault(round(w["top"]), []).append(w)
    return {t: sorted(ws, key=lambda w: w["x0"]) for t, ws in buckets.items()}


def merge_number_fragments(words):
    """Re-join number tokens pdfplumber split on an internal comma gap."""
    ws = sorted(words, key=lambda w: w["x0"])
    out, i = [], 0
    while i < len(ws):
        text, x0, x1 = ws[i]["text"], ws[i]["x0"], ws[i]["x1"]
        while (i + 1 < len(ws) and ws[i + 1]["x0"] - x1 < 5
               and (text.rstrip().endswith(",")
                    or ws[i + 1]["text"].lstrip().startswith(",")
                    or (re.fullmatch(r"\$?\d{1,3}", text)
                        and re.match(r"[\d,]", ws[i + 1]["text"])))):
            i += 1
            text += ws[i]["text"]
            x1 = ws[i]["x1"]
        out.append({"text": text, "x0": x0, "x1": x1})
        i += 1
    return out


def number(tok):
    if not NUM_TOK.match(tok):
        return None
    digits = re.sub(r"[^\d]", "", tok)
    return None if not digits else (-int(digits) if "(" in tok else int(digits))


def header_columns(words):
    """Cluster header fund-words into ordered columns -> list of word-lists."""
    toks = sorted(((w["text"].strip(".,").lower(), (w["x0"] + w["x1"]) / 2)
                   for w in words if w["text"].strip(".,").lower() in FUND_WORDS),
                  key=lambda t: t[1])
    cols = []
    for word, x in toks:
        if cols and x - cols[-1][0] <= 14:
            cols[-1][1].append(word)
            cols[-1][0] = (cols[-1][0] + x) / 2
        else:
            cols.append([x, [word]])
    return [c[1] for c in cols]


def extract(year):
    with pdfplumber.open(pdf_path(year)) as pdf:
        labeled = next((pi for pi, pg in enumerate(pdf.pages)
                        if all(s in (pg.extract_text() or "").lower() for s in
                               ("combining statement of revenues", "internal service",
                                "operating expense"))), None)
        if labeled is None:
            return {"year": year, "error": "ISF rev/exp statement page not found"}

        bL = rows_by_top(pdf.pages[labeled])
        tops, op_rev_label_top = {}, None
        for top, ws in sorted(bL.items()):
            low = " ".join(w["text"] for w in ws).lower()
            if low.startswith("operating revenue") and op_rev_label_top is None:
                op_rev_label_top = top
            for prefix, key in (("total operating revenue", "op_revenues"),
                                ("total operating expense", "op_expenses")):
                if low.startswith(prefix):
                    tops[key] = top
        if not tops:
            return {"year": year, "error": "target rows not found on labeled page"}

        # Is the IT column on the labeled page (single) or page L+1 (wrapped)?
        hdr_cut = op_rev_label_top if op_rev_label_top else min(tops.values())
        on_L = any(w["text"] in ("Technology", "Information")
                   for t, ws in bL.items() if t < hdr_cut for w in ws)
        if on_L:
            it_page, bIT, wrapped = pdf.pages[labeled], bL, False
        else:
            it_page = pdf.pages[labeled + 1]
            bIT = rows_by_top(it_page)
            wrapped = True

        # Header columns on the IT page (header rows only).
        hdr_limit = (hdr_cut if not wrapped else min(tops.values()))
        hdr_words = [w for t, ws in bIT.items() if t < hdr_limit for w in ws]
        cols = header_columns(hdr_words)
        # match on "technology" only: "information" can appear twice in the
        # modern stacked header and is ambiguous; "technology" is unique to IT.
        it_idx = next((i for i, words in enumerate(cols)
                       if "technology" in words), None)

        res = {"year": year, "labeled_page": labeled, "wrapped": wrapped,
               "columns": cols, "it_col_index": it_idx}
        for key, top in tops.items():
            row = [w for tt, ws in bIT.items() if abs(tt - top) <= 3 for w in ws]
            toks = merge_number_fragments(row)
            nums = [number(t["text"]) for t in toks if number(t["text"]) is not None]
            res[key + "_all"] = nums
            if wrapped:
                # On a wrapped continuation page the IT column is the leftmost,
                # so the IT figure is the first number on the row. Sanity-check
                # that "technology" is among this page's header words at all.
                if nums:
                    res[key] = nums[0]
                if not any("technology" in c for c in cols):
                    res[key + "_warn"] = "no 'technology' header on continuation page"
            elif it_idx is not None and len(nums) == len(cols):
                res[key] = nums[it_idx]
            elif it_idx is not None and len(nums) > it_idx:
                res[key] = nums[it_idx]
                res[key + "_warn"] = f"{len(cols)} cols vs {len(nums)} nums"
        return res


if __name__ == "__main__":
    targets = [int(a) for a in sys.argv[1:]] or list(YEARS)
    results = []
    for y in targets:
        r = extract(y)
        results.append(r)
        print(f"\n===== FY{y} =====")
        if "error" in r:
            print(f"  !! {r['error']}")
            continue
        print(f"  page {r['labeled_page']} | {'WRAPPED' if r['wrapped'] else 'single-page'}"
              f" | cols={r['columns']} | IT idx={r['it_col_index']}")
        for key, lab in (("op_revenues", "operating revenues"),
                         ("op_expenses", "operating EXPENSES")):
            warn = f"  <<{r[key + '_warn']}>>" if key + "_warn" in r else ""
            got = f"${r[key]:,}" if key in r else "NOT PARSED"
            print(f"  {lab:20s} = {got}{warn}")
            print(f"      row #s: {r.get(key + '_all')}")

    if len(targets) == len(list(YEARS)):
        out = os.path.join(HERE, "it_spend.csv")
        with open(out, "w", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(["fiscal_year", "it_operating_expenses", "it_operating_revenues"])
            for r in results:
                wr.writerow([r["year"], r.get("op_expenses", ""), r.get("op_revenues", "")])
        print(f"\n\nWrote {out}\n")
        print(f"{'FY':<8}{'IT operating expenses':>24}{'IT operating revenues':>24}")
        for r in results:
            e = f"${r['op_expenses']:,}" if r.get("op_expenses") else "?? REVIEW"
            v = f"${r['op_revenues']:,}" if r.get("op_revenues") else "?? REVIEW"
            print(f"FY{r['year']:<6}{e:>24}{v:>24}")
