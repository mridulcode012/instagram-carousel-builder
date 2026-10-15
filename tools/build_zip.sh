#!/bin/sh
# Build the claude.ai upload: dist/instagram-carousel-builder-<version>.zip (the plugin folder's contents).
set -e
cd "$(dirname "$0")/.."
ver=$(python3 -c "import json; print(json.load(open('plugin/.claude-plugin/plugin.json'))['version'])")
claude plugin validate --strict ./plugin
mkdir -p dist
out="dist/instagram-carousel-builder-$ver.zip"
rm -f "$out"
(cd plugin && zip -qr "../$out" . -x '*.DS_Store' -x '*__pycache__*')
echo "$out ($(du -h "$out" | cut -f1))"
