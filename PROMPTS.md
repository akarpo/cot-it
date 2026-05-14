# Prompts behind this analysis

This project was built with Claude Code. The work splits into two sessions.

## Session 2 — budget parsing: assets, applications & asset spend

The `it_assets.*` work (this session) — parsing the IT division's Performance
Indicators out of 18 Adopted Budget PDFs, OCR-ing the FY2022 budget, and
wiring the project up for GitHub + Cloudflare. Verbatim prompts, in order:

1. > go to Downloads, cot-it, and read the readme

2. > Yes, parse the budget and record what assets (servers, computers, etc)
   > the IT department has maintained over time, and the number of endpoints
   > (applications, web services) it produces as a result. Put this in a
   > table of results along with IT asset spend over the years

   → produced `scan_budgets.py`, `extract_it_assets.py`, `build_assets_chart.py`,
   `it_assets.csv`, `it_assets_chart.png`, and the "What IT maintains" section
   of the README.

3. > Yes, OCR the 2022 budget

   → the FY2022 budget's IT pages are a non-extractable encoded font; they
   were OCR'd into `budget_pdf/Budget_FY2022_IT_ocr.pdf` and folded into
   `extract_it_assets.py`. The OCR corrected two figures (FY2022 adopted
   capital $265k→$120k; FY2019 applications 170→172 and equipment
   maintenance $3,750→$6,743).

4. > can you compile all the promots used to create this analysis, and push
   > this to github with a private repo?

5. > Files above 25mb will need to go into Cloudflare R2. Please review
   > tsd-budget project in Downloads for how the project had to be structured
   > so that it built correctly in Cloudflare. This is going to github but it
   > will be mirrored to cloudflare

   → produced this file plus the Cloudflare/R2 scaffolding (`.gitignore`,
   `.assetsignore`, `build.sh`, `upload_r2.py`, `fetch_r2.py`,
   `r2_manifest.json`, the four `*.r2.md` stubs, `R2_MANIFEST.md`) and the
   private GitHub repo.

## Session 1 — the original ACFR spend analysis

The `it_spend.*` work — `extract_it_spend.py`, `build_chart.py`,
`it_spend.csv`, `it_spend_chart.png`, and the original README — was done in
an earlier Claude Code session. Those prompts were not captured in this
session's transcript and are not reproduced here; the README's "The answer"
and "Caveats / methodology notes" sections document what that work produced.
