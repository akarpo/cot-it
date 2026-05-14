#!/usr/bin/env python3
"""Upload the .gitignore'd large files (>25 MB) to Cloudflare R2.

The four source PDFs over Cloudflare's 25 MiB per-asset limit are kept out
of the git repo (see .gitignore) and live only on R2. This script reads
`r2_manifest.json`, uploads each `pending` file via `wrangler r2 object put`
to `media/cot-it/<original-path>`, then rewrites the matching `*.r2.md` stub,
`r2_manifest.json`, and `R2_MANIFEST.md` with the live URL and `uploaded`
status.

R2 layout (shared with the sibling tsd-budget project):
    bucket:        media
    key prefix:    cot-it/
    public domain: media.karpowitsch.org   ->  https://media.karpowitsch.org/cot-it/...

Auth: wrangler needs credentials. In an interactive shell `wrangler login`
is enough; otherwise set CLOUDFLARE_API_TOKEN (a token with "Workers R2
Storage: Edit" permission).

Usage:
    CLOUDFLARE_API_TOKEN=...  python3 upload_r2.py          # upload pending
    python3 upload_r2.py --dry-run                          # show plan only
    python3 upload_r2.py --force                            # re-upload all

Idempotent: files already marked `uploaded` are skipped unless --force.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
MANIFEST_JSON = REPO / "r2_manifest.json"
MANIFEST_MD = REPO / "R2_MANIFEST.md"

BUCKET = "media"
PREFIX = "cot-it"
CUSTOM_DOMAIN = "media.karpowitsch.org"

MIME = {".pdf": "application/pdf"}


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST_JSON.read_text())


def save_manifest(rows: list[dict]) -> None:
    MANIFEST_JSON.write_text(json.dumps(rows, indent=2) + "\n")


def write_stub(row: dict) -> None:
    fname = row["rel"].split("/")[-1]
    url = row["r2_url"]
    status = ("uploaded to R2." if row["status"] == "uploaded"
              else "`pending R2 upload` — run `python3 upload_r2.py`.")
    (REPO / row["stub"]).write_text(f"""# {fname}

This file is hosted on Cloudflare R2 — it is larger than Cloudflare's 25 MiB
per-asset limit, so it is kept out of the git repo. Restore it locally with
`python3 fetch_r2.py` (or download the URL below).

| Property | Value |
|---|---|
| Original filename | `{fname}` |
| Original path | `{row['rel']}` |
| Size | {row['size_mb']:.2f} MB ({row['size_bytes']:,} bytes) |
| SHA-256 | `{row['sha256']}` |
| Source | City of Troy public records (see README "Data sources") |
| R2 URL | [{url}]({url}) |

**Status:** {status}

To verify integrity after download:
```bash
shasum -a 256 {fname}
# expected: {row['sha256']}
```
""")


def write_manifest_md(rows: list[dict]) -> None:
    total_mb = sum(r["size_mb"] for r in rows)
    uploaded = sum(1 for r in rows if r["status"] == "uploaded")
    lines = [
        "# R2-Externalized Files Manifest",
        "",
        "The four City of Troy source PDFs larger than Cloudflare's **25 MiB**",
        "per-asset limit are stored on Cloudflare R2 instead of in this git repo.",
        "Each has a sibling `*.r2.md` stub with the same metadata (size, SHA-256).",
        "",
        f"**Status:** {uploaded}/{len(rows)} uploaded "
        + ("— all externalized files are live on R2."
           if uploaded == len(rows)
           else "— run `CLOUDFLARE_API_TOKEN=... python3 upload_r2.py` to upload."),
        "",
        f"**Total externalized:** {len(rows)} files / {total_mb:.1f} MB",
        "",
        "Restore them into a fresh clone with `python3 fetch_r2.py`.",
        "",
        "| # | File | Size | Stub | R2 URL | Status |",
        "|---|------|------|------|--------|--------|",
    ]
    for i, r in enumerate(sorted(rows, key=lambda r: -r["size_mb"]), 1):
        fname = r["rel"].split("/")[-1]
        url_md = f"[link]({r['r2_url']})" if r["status"] == "uploaded" else "pending"
        lines.append(
            f"| {i} | `{r['rel']}` | {r['size_mb']:.1f} MB | "
            f"[`{Path(r['stub']).name}`](./{r['stub']}) | {url_md} | {r['status']} |"
        )
    lines.append("")
    MANIFEST_MD.write_text("\n".join(lines))


def upload(local: Path, key: str) -> None:
    ct = MIME.get(local.suffix.lower(), "application/octet-stream")
    cmd = ["wrangler", "r2", "object", "put", f"{BUCKET}/{key}",
           "--file", str(local), "--content-type", ct, "--remote"]
    print(f"  uploading -> {BUCKET}/{key}  ({ct})")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  ERROR: wrangler failed (exit {res.returncode})", file=sys.stderr)
        print(f"  stderr: {res.stderr.strip()}", file=sys.stderr)
        raise SystemExit(2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="re-upload files already marked uploaded")
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would happen, upload nothing")
    args = ap.parse_args()

    rows = load_manifest()
    pending = [r for r in rows if args.force or r["status"] != "uploaded"]
    print(f"Manifest: {len(rows)} files; to upload: {len(pending)}")

    missing = [r for r in pending if not (REPO / r["rel"]).exists()]
    if missing:
        print("ERROR: these manifest files are missing locally "
              "(run fetch_r2.py first, or restore them):", file=sys.stderr)
        for r in missing:
            print(f"  - {r['rel']}", file=sys.stderr)
        return 1

    if args.dry_run:
        for r in pending:
            print(f"  WOULD upload: {r['rel']} ({r['size_mb']:.1f} MB) "
                  f"-> {r['r2_url']}")
        return 0

    for i, row in enumerate(pending, 1):
        local = REPO / row["rel"]
        key = f"{PREFIX}/{row['rel']}"
        print(f"[{i}/{len(pending)}] {row['rel']}")
        upload(local, key)
        row["r2_url"] = f"https://{CUSTOM_DOMAIN}/{key}"
        row["status"] = "uploaded"
        write_stub(row)
        print(f"  stub updated -> {row['stub']}")

    save_manifest(rows)
    write_manifest_md(rows)
    done = sum(1 for r in rows if r["status"] == "uploaded")
    print(f"\nDone. {done}/{len(rows)} uploaded; stubs + manifests rewritten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
