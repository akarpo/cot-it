#!/usr/bin/env python3
"""Scan all City of Troy Adopted Budget PDFs for the IT division pages.

Dumps, per budget, every page that looks like part of the Information
Technology section: the Performance Indicators table (asset / endpoint
counts), the financial summary, and the Capital Outlay / Capital
Expenditures line. Handles the two format eras (pre-2012 "Department at a
Glance" vs. later "Internal Service Fund" layout) and the reversed-text
pages pdfplumber sometimes produces.
"""
import glob
import os
import re
import sys

import pdfplumber

BUDGET_DIR = os.path.join(os.path.dirname(__file__), "budget_pdf")


def fix_reversed(text: str) -> str:
    """Some ISF statement pages extract right-to-left. Detect & un-reverse
    per line when the reversed form contains more real words."""
    markers = ("noitamrofni", "ygolonhcet", "erutidnepxe", "eunever", "latipac")
    out = []
    for line in text.split("\n"):
        low = line.lower()
        if any(m in low for m in markers):
            out.append(line[::-1])
        else:
            out.append(line)
    return "\n".join(out)


def page_is_it(text: str) -> bool:
    t = text.lower().replace("\n", " ")
    if "information technology" not in t and "informationtechnology" not in t:
        return False
    signals = [
        "performance indicator", "personal computers", "help desk",
        "application packages", "software supported", "servers supported",
        "printers supported", "capital outlay", "capital expenditure",
        "department at a glance", "mission statement", "department description",
        "chargeback",
    ]
    return any(s in t for s in signals)


def main():
    only = sys.argv[1:]  # optional: list of years to limit to
    files = sorted(glob.glob(os.path.join(BUDGET_DIR, "Budget_FY*.pdf")))
    for f in files:
        year = re.search(r"FY(\d{4})", f).group(1)
        if only and year not in only:
            continue
        pdf = pdfplumber.open(f)
        print(f"\n{'='*78}\nBUDGET FY{year}  ({len(pdf.pages)} pages)  {os.path.basename(f)}\n{'='*78}")
        for i, pg in enumerate(pdf.pages):
            raw = pg.extract_text() or ""
            if not page_is_it(raw):
                continue
            text = fix_reversed(raw)
            print(f"\n----- FY{year} PDF page {i} -----")
            print(text)
        pdf.close()


if __name__ == "__main__":
    main()
