#!/usr/bin/env python3
"""Restore the R2-externalized large files into a fresh clone.

The four source PDFs >25 MB are not in the git repo (see .gitignore /
R2_MANIFEST.md). This script reads `r2_manifest.json`, downloads any that
are missing locally from their R2 URLs, and verifies each against its
recorded SHA-256.

Usage:
    python3 fetch_r2.py            # download whatever is missing
    python3 fetch_r2.py --force    # re-download everything
    python3 fetch_r2.py --check    # verify local copies, download nothing

No credentials needed — the R2 bucket is served read-only over the public
media.karpowitsch.org domain.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent
MANIFEST_JSON = REPO / "r2_manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="re-download files even if present")
    ap.add_argument("--check", action="store_true",
                    help="only verify local copies; download nothing")
    args = ap.parse_args()

    rows = json.loads(MANIFEST_JSON.read_text())
    rc = 0
    for row in rows:
        dest = REPO / row["rel"]
        present = dest.exists()

        if present and not args.force:
            actual = sha256(dest)
            ok = actual == row["sha256"]
            print(f"{'OK  ' if ok else 'BAD '} {row['rel']} "
                  f"({'sha256 verified' if ok else 'sha256 MISMATCH'})")
            if not ok:
                rc = 1
            continue

        if args.check:
            print(f"MISS {row['rel']} (not present locally)")
            rc = 1
            continue

        if row.get("status") != "uploaded":
            print(f"SKIP {row['rel']} — not yet on R2 "
                  f"(status: {row.get('status')}); run upload_r2.py first")
            rc = 1
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"GET  {row['rel']}  <-  {row['r2_url']}")
        try:
            urllib.request.urlretrieve(row["r2_url"], dest)
        except Exception as e:  # noqa: BLE001
            print(f"     ERROR: {e}", file=sys.stderr)
            rc = 1
            continue
        actual = sha256(dest)
        if actual == row["sha256"]:
            print(f"     done, sha256 verified ({row['size_mb']:.1f} MB)")
        else:
            print(f"     ERROR: sha256 mismatch — expected {row['sha256']}, "
                  f"got {actual}", file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
