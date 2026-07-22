#!/bin/bash
# Double-click to (re)build the St. Expedite wiki and open it in your browser.
cd "$(dirname "$0")" || exit 1
echo "Building St. Expedite wiki…"
python3 build.py || { echo "Build failed. Press any key."; read -n1; exit 1; }
echo "Opening…"
open "docs/index.html"
echo "Done. You can close this window."
