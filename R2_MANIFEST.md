# R2-Externalized Files Manifest

The four City of Troy source PDFs larger than Cloudflare's **25 MiB**
per-asset limit are stored on Cloudflare R2 instead of in this git repo.
Each has a sibling `*.r2.md` stub with the same metadata (size, SHA-256).

**Status:** 4/4 uploaded — all externalized files are live on R2.

**Total externalized:** 4 files / 129.6 MB

Restore them into a fresh clone with `python3 fetch_r2.py`.

| # | File | Size | Stub | R2 URL | Status |
|---|------|------|------|--------|--------|
| 1 | `budget_pdf/Budget_FY2025.pdf` | 36.7 MB | [`Budget_FY2025.pdf.r2.md`](./budget_pdf/Budget_FY2025.pdf.r2.md) | [link](https://media.karpowitsch.org/cot-it/budget_pdf/Budget_FY2025.pdf) | uploaded |
| 2 | `budget_pdf/Budget_FY2026.pdf` | 36.3 MB | [`Budget_FY2026.pdf.r2.md`](./budget_pdf/Budget_FY2026.pdf.r2.md) | [link](https://media.karpowitsch.org/cot-it/budget_pdf/Budget_FY2026.pdf) | uploaded |
| 3 | `acfr_pdf/ACFR_2011_ocr.pdf` | 30.0 MB | [`ACFR_2011_ocr.pdf.r2.md`](./acfr_pdf/ACFR_2011_ocr.pdf.r2.md) | [link](https://media.karpowitsch.org/cot-it/acfr_pdf/ACFR_2011_ocr.pdf) | uploaded |
| 4 | `budget_pdf/Budget_FY2017.pdf` | 26.6 MB | [`Budget_FY2017.pdf.r2.md`](./budget_pdf/Budget_FY2017.pdf.r2.md) | [link](https://media.karpowitsch.org/cot-it/budget_pdf/Budget_FY2017.pdf) | uploaded |
