#!/usr/bin/env python3
"""City of Troy IT department — assets maintained, applications/endpoints,
and IT asset spend, FY2004–FY2026, from the Adopted Budget documents.

Where the data comes from
-------------------------
Each Adopted Budget's Information Technology section carries a "Performance
Indicators" table with ~4 fiscal years per budget (two Actual columns, one
Projected, one Budget). The tables overlap heavily between budget years, so
every fiscal year is reported 2–4 times. This script encodes every one of
those raw observations (see OBS below — each row is one cell read straight
out of one budget PDF, with its budget source, fiscal year, and column
type), then resolves each fiscal year to a single best value:

    prefer Actual > Projected > Budget; within a tier, the most recent
    budget wins (its Actual is the post-close, audited-ish figure).

Metrics
-------
  software   Applications / "Software Supported" — the count of distinct
             application packages IT keeps running ("endpoints"). Web
             services are not broken out separately in the budgets.
  pcs        Personal Computers Supported
  printers   Printers Supported          (first reported in the FY2014 budget)
  servers    Servers Supported (physical + virtual, not hosts; FY2014 on)
  helpdesk   Computer Help Desk Requests (annual workload)
  equip_maint  Equipment Maintenance Costs ($ — operating spend keeping the
             existing fleet running)
  capital_adopted  IT Capital Budget as adopted for that fiscal year ($).

Notes / caveats
---------------
* Fiscal-year convention follows the cot-it project: FY2005 = fiscal 2004/05.
* The FY2011 budget PDF is a 50-page abridged document with no IT section.
  The FY2012 and FY2013 budgets switched to a summary "Annual Budget by
  Organization" format that has the financials but NO performance-indicator
  table — so FY2011-FY2013 have no asset/endpoint counts from the budgets.
* The FY2022 budget's IT pages use a custom-encoded font that does not
  extract as text; they were OCR'd into budget_pdf/Budget_FY2022_IT_ocr.pdf
  (pages 314-317 of that budget) and are read from there.
* The FY2024 budget's Performance Indicators table is a verbatim copy of the
  FY2023 budget's (same values under shifted column labels) — a copy-paste
  error in the document. It is excluded; FY2023/FY2025/FY2026 cover those
  years correctly.
* "Software/Servers/Printers Supported" counts were re-baselined a couple of
  times (e.g. software jumped ~137->154 between the FY2016 and FY2017
  budgets when in-house software was reclassified; printers read 195-205 in
  the FY2023 budget then revert to ~136). Values are reported as-published.
* IT *capital* spend: the adopted capital budget is consistently reported and
  is what this script tabulates. The ISF "Capital Outlay/Expenditures" line
  shows ACTUALS of essentially $0 in most years because historically IT
  capital was funded by operating transfers from the Capital Projects Fund
  rather than booked as ISF capital outlay. Known non-zero ISF capital
  actuals: FY2007 ~$134.5k, FY2008 ~$267.9k, FY2017 ~$40.0k, FY2023 ~$116.1k,
  FY2024 ~$290.0k. See CAP_ACTUALS.
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), "it_assets.csv")

# --- raw observations -------------------------------------------------------
# Each budget's Performance Indicators table, as read from the PDF.
#   budget : the Budget_FY file it came from
#   fys    : the four fiscal years (cot-it FY = ending year) of the columns
#   types  : column type per the table header  A=Actual P=Projected B=Budget
#   rows   : metric -> the four cell values (None = blank/NA in the source)
BUDGETS = [
    dict(budget=2006, fys=[2004, 2005, 2005, 2006], types="APBB", rows=dict(
        software=[70, 72, 67, 72], pcs=[531, 550, 531, 550],
        helpdesk=[1520, 1620, 1600, 1700],
        equip_maint=[28450, 30000, 40000, 40000])),
    dict(budget=2007, fys=[2005, 2006, 2006, 2007], types="APBB", rows=dict(
        software=[74, 75, 72, 72], pcs=[551, 568, 550, 568],
        helpdesk=[1620, 1800, 1700, 1850],
        equip_maint=[25560, 30000, 30000, 30000])),
    dict(budget=2008, fys=[2006, 2007, 2007, 2008], types="APBB", rows=dict(
        software=[79, 85, 72, 84], pcs=[568, 588, 568, 588],
        helpdesk=[1800, 1896, 1850, 1900],
        equip_maint=[15790, 30000, 30000, 34670])),
    dict(budget=2009, fys=[2007, 2008, 2008, 2009], types="APBB", rows=dict(
        software=[87, 86, 84, 85], pcs=[588, 588, 588, 588],
        helpdesk=[1890, 2275, 1900, 2200],
        equip_maint=[26500, 34670, 34670, 31080])),
    dict(budget=2010, fys=[2008, 2009, 2009, 2010], types="APBB", rows=dict(
        software=[99, 107, 85, 104], pcs=[588, 588, 588, 566],
        helpdesk=[2268, 2000, 2200, 2200],
        equip_maint=[19388, 30000, 31080, 22200])),
    # FY2011 budget: abridged, no IT section. FY2012/FY2013: no PI table.
    dict(budget=2014, fys=[2011, 2012, 2013, 2014], types="AAPB", rows=dict(
        software=[109, 109, 116, 116], pcs=[481, 475, 484, 478],
        printers=[199, None, 136, 136], servers=[58, 65, 68, 68],
        helpdesk=[2507, 2423, 2314, 2400],
        equip_maint=[23070, 21320, 33110, 33610])),
    dict(budget=2015, fys=[2012, 2013, 2014, 2015], types="AAPB", rows=dict(
        software=[115, 123, 133, 133], pcs=[475, 484, 467, 484],
        printers=[None, 136, 140, 140], servers=[65, 68, 68, 66],
        helpdesk=[2423, 2314, 2400, 2990],
        equip_maint=[21320, 30159, 30000, 33610])),
    dict(budget=2016, fys=[2013, 2014, 2015, 2016], types="AAPB", rows=dict(
        software=[123, 133, 137, 137], pcs=[484, 484, 473, 473],
        printers=[136, 140, 140, 140], servers=[68, 66, 63, 63],
        helpdesk=[2314, 3079, 3180, 3200],
        equip_maint=[30159, 25826, 33610, 32600])),
    dict(budget=2017, fys=[2014, 2015, 2016, 2017], types="AAPB", rows=dict(
        software=[151, 154, 153, 153], pcs=[484, 484, 473, 484],
        printers=[140, 140, 144, 144], servers=[66, 63, 60, 60],
        helpdesk=[3079, 3028, 3000, 3000],
        equip_maint=[25826, 19376, 30000, 30000])),
    dict(budget=2018, fys=[2015, 2016, 2017, 2018], types="AAPB", rows=dict(
        software=[154, 153, 153, 152], pcs=[484, 473, 484, 499],
        printers=[140, 144, 144, 137], servers=[63, 60, 60, 71],
        helpdesk=[3028, 3000, 3000, 3150],
        equip_maint=[19376, 30000, 30000, 32100])),
    dict(budget=2019, fys=[2016, 2017, 2018, 2019], types="AAPB", rows=dict(
        software=[154, 162, 162, 162], pcs=[484, 498, 502, 502],
        printers=[140, 145, 145, 145], servers=[63, 70, 76, 71],
        helpdesk=[3028, 3207, 3300, 3300],
        equip_maint=[19376, 14000, 14000, 16400])),
    dict(budget=2020, fys=[2017, 2018, 2019, 2020], types="AAPB", rows=dict(
        software=[162, 164, 170, 170], pcs=[498, 503, 502, 501],
        printers=[145, 145, 140, 140], servers=[70, 72, 78, 78],
        helpdesk=[3207, 3683, 3300, 3300],
        equip_maint=[14000, 13090, 13900, 13900])),
    dict(budget=2021, fys=[2018, 2019, 2020, 2021], types="AAPB", rows=dict(
        software=[164, 170, 159, 157], pcs=[503, 502, 511, 506],
        printers=[145, 155, 155, 155], servers=[72, 74, 74, 72],
        helpdesk=[3683, 3043, 3010, 3200],
        equip_maint=[13090, 3750, 13900, 15500])),
    # FY2022 budget: IT pages OCR'd from Budget_FY2022_IT_ocr.pdf (the
    # original budget's IT pages are a non-extractable encoded font).
    dict(budget=2022, fys=[2019, 2020, 2021, 2022], types="AAPB", rows=dict(
        software=[172, 163, 164, 161], pcs=[502, 506, 512, 512],
        printers=[155, 195, 205, 205], servers=[74, 73, 75, 75],
        helpdesk=[3043, 2864, 3040, 3100],
        equip_maint=[6743, 6556, 15500, 17550])),
    dict(budget=2023, fys=[2020, 2021, 2022, 2023], types="AAPB", rows=dict(
        software=[163, 164, 161, 164], pcs=[506, 512, 512, 512],
        printers=[195, 205, 205, 205], servers=[73, 75, 75, 75],
        helpdesk=[2864, 3040, None, None],
        equip_maint=[6556, 15500, 17550, 20500])),
    # FY2024 budget PI table excluded — verbatim stale copy of FY2023's.
    dict(budget=2025, fys=[2022, 2023, 2024, 2025], types="AAPB", rows=dict(
        software=[164, 168, 168, 171], pcs=[512, 546, 567, 585],
        printers=[205, 136, 136, 111], servers=[75, 76, 81, 80],
        helpdesk=[2250, 2551, 2600, 2600],
        equip_maint=[14014, 18236, 30120, 53520])),
    dict(budget=2026, fys=[2023, 2024, 2025, 2026], types="AAPB", rows=dict(
        software=[168, 168, 168, 168], pcs=[546, 566, 585, 595],
        printers=[136, 136, 138, 138], servers=[76, 85, 82, 81],
        helpdesk=[2551, 2206, 2000, 2000],
        equip_maint=[18236, 22132, 37000, 42920])),
]

# IT capital budget as ADOPTED for each fiscal year (the budget book's own
# "Proposed"/"Final"/budget-year column). Source budget == fiscal year.
CAP_ADOPTED = {
    2008: 749000, 2009: 103100, 2010: 215000, 2012: 84430, 2013: 181500,
    2014: 46000, 2015: 238500, 2016: 165000, 2017: 145000, 2018: 120000,
    2019: 125000, 2020: 500000, 2021: 150000, 2022: 120000, 2023: 120000,
    2024: 40000, 2025: 290000, 2026: 148000,
    # FY2011: only the abridged budget exists; FY2012 budget shows FY2011
    # amended capital of $70,910 -> used as best-available adopted figure.
    2011: 70910,
}
# Years where the ISF actually booked non-zero capital outlay/expenditures
# in its own fund statement (most other years' ISF capital actual == $0,
# because IT capital was funded via Capital Projects Fund transfers).
CAP_ACTUALS = {2007: 134534, 2008: 267890, 2017: 39966, 2023: 116071,
               2024: 290000}

# --- resolve ----------------------------------------------------------------
PRIORITY = {"A": 3, "P": 2, "B": 1}
METRICS = ["software", "pcs", "printers", "servers", "helpdesk", "equip_maint"]


def resolve():
    # collect: metric -> fy -> list of (priority, budget_year, value, type)
    coll = {m: {} for m in METRICS}
    for b in BUDGETS:
        for m, vals in b["rows"].items():
            for fy, t, v in zip(b["fys"], b["types"], vals):
                if v is None:
                    continue
                coll[m].setdefault(fy, []).append(
                    (PRIORITY[t], b["budget"], v, t))
    best = {m: {} for m in METRICS}
    prov = {m: {} for m in METRICS}
    for m in METRICS:
        for fy, obs in coll[m].items():
            obs.sort(key=lambda o: (o[0], o[1]))  # highest priority, newest
            p, src, v, t = obs[-1]
            best[m][fy] = v
            prov[m][fy] = f"{t}@FY{src}budget"
    return best, prov


def main():
    best, prov = resolve()
    years = sorted(set().union(*[best[m] for m in METRICS],
                               CAP_ADOPTED, CAP_ACTUALS))
    rows = []
    for fy in years:
        rows.append(dict(
            fiscal_year=fy,
            applications_supported=best["software"].get(fy, ""),
            personal_computers=best["pcs"].get(fy, ""),
            printers=best["printers"].get(fy, ""),
            servers=best["servers"].get(fy, ""),
            help_desk_requests=best["helpdesk"].get(fy, ""),
            equipment_maintenance_cost=best["equip_maint"].get(fy, ""),
            it_capital_budget_adopted=CAP_ADOPTED.get(fy, ""),
            isf_capital_actual=CAP_ACTUALS.get(fy, ""),
        ))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # audit print
    hdr = ("FY  Apps  PCs  Prn  Srv  HelpDesk  EquipMaint   CapBudget  "
           "ISFCapActual")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        def s(x, money=False):
            if x == "":
                return "    -   " if money else "  - "
            return f"${x:>9,}" if money else f"{x:>5}"
        print(f"{r['fiscal_year']}  {s(r['applications_supported'])}"
              f"{s(r['personal_computers'])}{s(r['printers'])}"
              f"{s(r['servers'])}  {s(r['help_desk_requests'])}  "
              f"{s(r['equipment_maintenance_cost'], 1)}  "
              f"{s(r['it_capital_budget_adopted'], 1)}  "
              f"{s(r['isf_capital_actual'], 1)}")
    print(f"\nWrote {OUT}")
    print("\nProvenance (metric -> fiscal_year -> column@source budget):")
    for m in METRICS:
        items = sorted(prov[m].items())
        print(f"  {m}: " + ", ".join(f"FY{fy}={p}" for fy, p in items))


if __name__ == "__main__":
    main()
