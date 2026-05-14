# R2-Externalized Files Manifest

The four City of Troy source PDFs larger than Cloudflare's **25 MiB**
per-asset limit are stored on Cloudflare R2 instead of in this git repo.
Each has a sibling `*.r2.md` stub with the same metadata (size, SHA-256).

**Status:** 0/4 uploaded — run `CLOUDFLARE_API_TOKEN=... python3 upload_r2.py` to upload.

**Total externalized:** 4 files / 129.6 MB

Restore them into a fresh clone with `python3 fetch_r2.py`.

| # | File | Size | Stub | R2 URL | Status |
|---|------|------|------|--------|--------|
| 1 | `budget_pdf/Budget_FY2025.pdf` | 36.7 MB | [`Budget_FY2025.pdf.r2.md`](./budget_pdf/Budget_FY2025.pdf.r2.md) | pending | pending |
| 2 | `budget_pdf/Budget_FY2026.pdf` | 36.3 MB | [`Budget_FY2026.pdf.r2.md`](./budget_pdf/Budget_FY2026.pdf.r2.md) | pending | pending |
| 3 | `acfr_pdf/ACFR_2011_ocr.pdf` | 30.0 MB | [`ACFR_2011_ocr.pdf.r2.md`](./acfr_pdf/ACFR_2011_ocr.pdf.r2.md) | pending | pending |
| 4 | `budget_pdf/Budget_FY2017.pdf` | 26.6 MB | [`Budget_FY2017.pdf.r2.md`](./budget_pdf/Budget_FY2017.pdf.r2.md) | pending | pending |
