#!/usr/bin/env bash
# Local-preview build for the Cloudflare Workers Static Assets deploy.
#
# The live deploy does NOT use this script — Cloudflare is wired to the
# GitHub repo and deploys the repo root directly, with `.assetsignore`
# excluding `.git/` and other infrastructure paths from the asset set
# (the .git packfile alone exceeds Workers' 25 MiB per-asset limit).
#
# This script just writes a clean ./dist/ mirror containing exactly the
# tracked files — handy for eyeballing what Cloudflare will actually serve.
#
#   $ bash build.sh
#   $ open dist/README.md      # (no index.html — this is a file-listing site)
#
set -euo pipefail

OUT=dist
rm -rf "$OUT"
mkdir -p "$OUT"

# `git archive` emits exactly the tracked files (respects .gitignore,
# excludes the .git/ directory) — the same content Cloudflare's clone sees.
git archive HEAD --format=tar | tar -x -C "$OUT"

# Defensive sweep — should already be excluded but cheap insurance.
rm -rf "$OUT/.git" "$OUT/dist"

echo ""
echo "=== Build complete ==="
du -sh "$OUT"
echo ""
echo "Files > 25MB in build output (must be empty — Cloudflare's per-asset limit):"
find "$OUT" -type f -size +25M -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}' || true
echo "(if the line above is blank, the deploy will not hit the per-asset limit)"
