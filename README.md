# cot-it — City of Troy IT spending from ACFRs (FY2005–FY2025)

Answers: **What has the City of Troy spent on Information Technology over time?**
— extracted from 21 years of the City's Annual Comprehensive Financial Reports
and 18 Adopted Budgets.

The analysis is published as a single-page site, [`index.html`](./index.html)
(interactive charts + data tables). Self-contained — open this folder in Claude
Code to continue the analysis.

---

## The answer

The City of Troy runs **IT as an internal service fund**, so every ACFR reports
it as its own line of business with full financial statements. "IT spend" here =
the **total operating expenses of the Information Technology internal service
fund** (includes depreciation; excludes capital-asset purchases, which flow
through the fund's balance sheet / cash-flow statement).

| FY | IT operating expenses | YoY | IT operating revenues (charges billed) |
|----|----------------------:|----:|---------------------------------------:|
| 2005 | $1,500,672 | — | $1,322,190 |
| 2006 | $1,430,321 | −4.7% | $1,430,493 |
| 2007 | $1,653,649 | +15.6% | $1,515,678 |
| 2008 | $1,583,195 | −4.3% | $1,605,304 |
| 2009 | $1,570,371 | −0.8% | $1,634,795 |
| 2010 | $1,352,419 | −13.9% | $1,576,310 |
| 2011 | $1,395,019 | +3.1% | $1,365,821 |
| 2012 | $1,499,330 | +7.5% | $1,553,645 |
| 2013 | $1,708,100 | +13.9% | $1,552,009 |
| 2014 | $1,778,680 | +4.1% | $1,509,585 |
| 2015 | $2,056,254 | +15.6% | $1,809,404 |
| 2016 | $1,902,658 | −7.5% | $1,845,450 |
| 2017 | $1,821,152 | −4.3% | $1,963,408 |
| 2018 | $2,028,008 | +11.4% | $2,057,212 |
| 2019 | $1,962,479 | −3.2% | $2,150,401 |
| 2020 | $2,152,469 | +9.7% | $2,205,776 |
| 2021 | $2,088,314 | −3.0% | $2,252,386 |
| 2022 | $2,065,383 | −1.1% | $2,342,368 |
| 2023 | $2,131,109 | +3.2% | $2,517,508 |
| 2024 | $2,383,834 | +11.9% | $2,620,404 |
| 2025 | $2,678,683 | +12.4% | $2,681,092 |

**FY2005 → FY2025: +78% total, ~2.9%/yr** (CPI rose ~67% / ~2.6%/yr over the
same span — IT spend grew modestly faster than inflation). Low point FY2010
($1.35M, post-2008 austerity); steepest recent growth FY2024–FY2025 (+12%/yr).

Chart: `it_spend_chart.png`. Data: `it_spend.csv`.

## What IT maintains — assets, applications & asset spend (from the budgets)

The ACFR gives the *fund total*. The **Adopted Budget** documents give the
*scope*: each budget's IT section has a **Performance Indicators** table
listing how many devices and applications the department keeps running, plus
its equipment-maintenance and capital spend. Stitching 18 budgets together
(the tables overlap 2–4×, so most years are cross-checked) yields FY2004–FY2026:

| FY | Applications supported | PCs | Printers | Servers | Help-desk requests | Equip. maintenance $ | IT capital budget (adopted) $ |
|----|----:|----:|----:|----:|----:|----:|----:|
| 2004 | 70 | 531 | — | — | 1,520 | $28,450 | — |
| 2005 | 74 | 551 | — | — | 1,620 | $25,560 | — |
| 2006 | 79 | 568 | — | — | 1,800 | $15,790 | — |
| 2007 | 87 | 588 | — | — | 1,890 | $26,500 | — |
| 2008 | 99 | 588 | — | — | 2,268 | $19,388 | $749,000 |
| 2009 | 107 | 588 | — | — | 2,000 | $30,000 | $103,100 |
| 2010 | 104 | 566 | — | — | 2,200 | $22,200 | $215,000 |
| 2011 | 109 | 481 | 199 | 58 | 2,507 | $23,070 | $70,910 |
| 2012 | 115 | 475 | — | 65 | 2,423 | $21,320 | $84,430 |
| 2013 | 123 | 484 | 136 | 68 | 2,314 | $30,159 | $181,500 |
| 2014 | 151 | 484 | 140 | 66 | 3,079 | $25,826 | $46,000 |
| 2015 | 154 | 484 | 140 | 63 | 3,028 | $19,376 | $238,500 |
| 2016 | 154 | 484 | 140 | 63 | 3,028 | $19,376 | $165,000 |
| 2017 | 162 | 498 | 145 | 70 | 3,207 | $14,000 | $145,000 |
| 2018 | 164 | 503 | 145 | 72 | 3,683 | $13,090 | $120,000 |
| 2019 | 172 | 502 | 155 | 74 | 3,043 | $6,743 | $125,000 |
| 2020 | 163 | 506 | 195 | 73 | 2,864 | $6,556 | $500,000 |
| 2021 | 164 | 512 | 205 | 75 | 3,040 | $15,500 | $150,000 |
| 2022 | 164 | 512 | 205 | 75 | 2,250 | $14,014 | $120,000 |
| 2023 | 168 | 546 | 136 | 76 | 2,551 | $18,236 | $120,000 |
| 2024 | 168 | 566 | 136 | 85 | 2,206 | $22,132 | $40,000 |
| 2025 | 168 | 585 | 138 | 82 | 2,000 | $37,000 | $290,000 |
| 2026 | 168 | 595 | 138 | 81 | 2,000 | $42,920 | $148,000 |

**The story:** the **PC fleet** is essentially flat over 22 years (~530 → ~595,
+12%) — a built-out city, not a growing one. What grew is **applications**:
70 → 168 supported software packages (+140%), i.e. the same staff (~9 FTE
throughout) running 2.4× more systems — that is the "more endpoints as a
result" effect. **Servers** climbed 58 → ~80 as virtualization let one
team run more services. **Asset *spend*** is lumpy, not a trend: the adopted
IT **capital budget** swings between $40k and $749k year to year (spikes =
one-time projects — the FY2008 financial-system replacement, the FY2020
$500k, the FY2025 $290k SQL/DR rebuild), averaging ~$190k/yr; **equipment
maintenance** is the steady ~$6–43k/yr cost of keeping the existing fleet
alive.

Chart: `it_assets_chart.png`. Data: `it_assets.csv`.

### Caveats specific to this table

- **"Applications supported"** is the budgets' own *Software Supported* /
  *Application Packages Supported* metric — commercial/publicly-available
  software only, not in-house code, and not separately broken out by
  web service. It was re-baselined at least twice (the ~137→154 jump between
  the FY2016 and FY2017 budgets is a reclassification, not real growth).
- **Printers** read 195–205 in the FY2020–FY2022 budgets, then revert to ~136.
  The FY2022 budget explains it: *"Printers include local label printers not
  all previously counted"* — a counting-scope change, not a fleet change;
  values are shown as published.
- **FY2011–FY2013** have no asset counts: the FY2011 budget is a 50-page
  abridged document, and the FY2012/FY2013 budgets dropped the Performance
  Indicators table. The **FY2022** budget's IT pages were a non-extractable
  encoded font; they were OCR'd into `budget_pdf/Budget_FY2022_IT_ocr.pdf`
  and are now parsed normally.
- **IT capital budget** = the *adopted* figure. Actual ISF capital booked is
  ~$0 in most years because IT capital was historically funded via operating
  transfers from the Capital Projects Fund, not the ISF capital line; the few
  years with non-zero ISF capital actuals (FY2007/08/17/23/24) are in
  `it_assets.csv`'s `isf_capital_actual` column.
- Every figure carries its full provenance (which budget, which column type)
  in the output of `python3 extract_it_assets.py`.

## Caveats / methodology notes

- This is the **internal service fund operating expense** figure — the most
  consistent IT measure available across all 21 ACFRs. It is *not* the same as
  a "general fund IT department budget"; the fund recovers its costs by billing
  other City departments (the "operating revenues" column).
- It **excludes capital outlay** (new servers, major software) — those are
  capitalized, not operating expenses. A fuller "IT investment" number would add
  capital purchases from the fund's cash-flow statement (a possible next step).
- FY2011's ACFR is a **scanned PDF**; it was OCR'd (`acfr_pdf/ACFR_2011_ocr.pdf`)
  before extraction. That one year is the most worth spot-checking by eye.
- Every extracted figure is printed with its full source row when you run
  `extract_it_spend.py` — re-run it to audit.

## Files

| Path | What it is |
|------|------------|
| `index.html` | The published single-page site — hero, TL;DR, three Chart.js sections (IT spend / what IT maintains / asset spend), methodology, and per-section collapsible source panels with full data tables. Self-contained; this is what Cloudflare serves. |
| `extract_it_spend.py` | Coordinate-aware (pdfplumber) extractor. Finds the ISF revenues/expenses combining statement in each ACFR, handles both single-page and wide-table-wrapped layouts, pulls the IT column's operating expenses & revenues. Prints every figure with its source row; writes `it_spend.csv`. |
| `build_chart.py` | Reads `it_spend.csv`, writes `it_spend_chart.png`, prints the summary table + growth stats. |
| `it_spend.csv` | The 21-year time series (fiscal_year, it_operating_expenses, it_operating_revenues). |
| `it_spend_chart.png` | Bar chart of operating expenses vs revenues, FY2005–FY2025. |
| `scan_budgets.py` | Sweeps all 22 `budget_pdf/` files and dumps every Information Technology section page (handles the two format eras + reversed-text pages). Run it (optionally with year args) to see the raw source pages behind the assets table. |
| `extract_it_assets.py` | Encodes every Performance-Indicators cell read from the 18 budgets that have one — each with its budget source & column type — then resolves each fiscal year (Actual > Projected > Budget, newest budget wins) and writes `it_assets.csv`. Prints the table + full per-figure provenance. |
| `build_assets_chart.py` | Reads `it_assets.csv`, writes `it_assets_chart.png` (assets/applications counts on top, asset spend on the bottom), prints a summary. |
| `it_assets.csv` | FY2004–FY2026 series: applications supported, PCs, printers, servers, help-desk requests, equipment maintenance $, adopted IT capital budget $, and (sparse) actual ISF capital $. |
| `it_assets_chart.png` | Two-panel chart of what IT maintains and what it spends on assets. |
| `acfr_pdf/` | All 21 ACFRs `ACFR_2005.pdf` … `ACFR_2025.pdf`, plus `ACFR_2011_ocr.pdf`. |
| `budget_pdf/` | City of Troy **Adopted Budget** documents `Budget_FY2005.pdf` … `Budget_FY2026.pdf` (22 files). Parsed by `extract_it_assets.py` for the IT division's Performance Indicators (assets, applications, maintenance & capital spend). FY2011 is a 50-page abridged doc; FY2012/FY2013 have no Performance Indicators table. |
| `budget_pdf/Budget_FY2022_IT_ocr.pdf` | The FY2022 budget's 4 IT-section pages (314–317), OCR'd — the original budget's IT pages are a non-extractable encoded font. `extract_it_assets.py` reads FY2022 from here. |
| `PROMPTS.md` | The prompts that drove this analysis (this is a Claude Code project). |
| `R2_MANIFEST.md` · `r2_manifest.json` · `*.r2.md` | The four source PDFs >25 MB live on Cloudflare R2, not in git (see [Deploying to Cloudflare](#deploying-to-cloudflare)). `R2_MANIFEST.md` is the human index; `r2_manifest.json` is the machine manifest; each externalized file has a sibling `*.r2.md` stub (size, SHA-256, R2 URL). |
| `upload_r2.py` · `fetch_r2.py` | `upload_r2.py` pushes the >25 MB files to R2 via `wrangler` and rewrites the stubs/manifests; `fetch_r2.py` restores them into a fresh clone (no credentials needed) and verifies SHA-256. |
| `.gitignore` · `.assetsignore` · `build.sh` | Git/Cloudflare deploy support — see [Deploying to Cloudflare](#deploying-to-cloudflare). |

## Reproduce

```bash
python3 fetch_r2.py             # fresh clone only: pull the 4 PDFs >25MB back from R2

python3 extract_it_spend.py     # re-extract from acfr_pdf/  -> it_spend.csv (prints source rows)
python3 build_chart.py          # -> it_spend_chart.png + summary
python3 extract_it_spend.py 2011  # spot-check a single year

python3 extract_it_assets.py    # -> it_assets.csv (prints table + per-figure provenance)
python3 build_assets_chart.py   # -> it_assets_chart.png + summary
python3 scan_budgets.py 2026    # dump the raw IT section pages of one budget to audit
```
Dependencies: `pdfplumber`, `matplotlib` (installed). `ocrmypdf` was used to
build `acfr_pdf/ACFR_2011_ocr.pdf` and `budget_pdf/Budget_FY2022_IT_ocr.pdf`
(only needed if regenerating those). A fresh `git clone` is missing the four
source PDFs >25 MB (`ACFR_2011_ocr.pdf`, `Budget_FY2017/2025/2026.pdf`) —
`python3 fetch_r2.py` pulls them back from R2; everything else is in git.

## Deploying to Cloudflare

This repo is mirrored to Cloudflare as a **Workers Static Assets** project:
push to `main` on GitHub triggers a deploy, and Cloudflare serves the repo
root directly (no build step). The site entry point is
[`index.html`](./index.html) — a self-contained single-page analysis with
interactive charts; the source PDFs and CSVs remain browsable alongside it.

Two structural constraints come from Cloudflare's **25 MiB per-asset limit**,
both handled the same way the sibling `tsd-budget` project handles them:

1. **The `.git/` packfile** would otherwise be served as an asset and exceeds
   25 MiB. [`.assetsignore`](./.assetsignore) excludes `.git/`, build
   artifacts, and editor/OS cruft from the deployed asset set — no dashboard
   settings needed.
2. **Four source PDFs are larger than 25 MiB** (`Budget_FY2025.pdf` 36.7 MB,
   `Budget_FY2026.pdf` 36.3 MB, `ACFR_2011_ocr.pdf` 30.0 MB,
   `Budget_FY2017.pdf` 26.6 MB). They are `.gitignore`d — kept out of the
   repo entirely — and live on Cloudflare R2 under
   `media.karpowitsch.org/cot-it/…`. Every other PDF (≤25 MiB) stays in the
   repo and deploys normally. See [`R2_MANIFEST.md`](./R2_MANIFEST.md).

Working with the externalized files:

```bash
python3 fetch_r2.py                          # restore them into a clone (public, no auth)
CLOUDFLARE_API_TOKEN=...  python3 upload_r2.py   # (re-)upload them to R2
bash build.sh                                # write a clean ./dist/ mirror to preview
```

`build.sh` is for local preview only; the live deploy uses the GitHub
connection + `.assetsignore` path described above.

## Suggested next steps

1. ~~**Parse the budget documents** in `budget_pdf/` for the IT division's
   line-item budget.~~ **Done** — the IT division's Performance Indicators
   (assets, applications, maintenance & capital spend) are in `it_assets.csv`;
   see "What IT maintains" above. Still open: the line-item *operating* budget
   (personnel / contractual-services split) and named systems/projects from the
   budget narratives.
2. **Add capital outlay** from each ACFR's ISF cash-flow statement
   ("Purchases/construction of capital assets", IT column) for a total-IT-
   investment series alongside operating expense.
3. **Per-capita / % of total budget** normalization — Troy's population and
   total governmental expenditures are both in the ACFR statistical sections.

## Data sources

- **City of Troy ACFRs** — `https://cms6.revize.com/revize/citytroymi/` (recent
  years under `Departments/City Manager/Financial Services/Financial Documents/ACFR/`;
  FY2005–FY2007 at the site root as `YYYY CAFR.pdf`). The CMS 403s non-browser
  requests — a normal browser User-Agent header is required.
- **City of Troy Adopted Budgets** — same CMS; index page:
  `https://troymi.gov/departments/city_manager/financial_services/financial_documents.php`
  (budget archive there runs back to 1978).

## Related folders

- `~/Downloads/cot-permits/` — Troy permits scraper.
- `~/Downloads/cot-celltower/` — AT&T cell-tower-near-Boulan-Park inquiry.
- `~/Downloads/tsd-budget/` — Troy *School District* budget project (separate
  entity; its `scripts/` has a BoardDocs API harvester).
