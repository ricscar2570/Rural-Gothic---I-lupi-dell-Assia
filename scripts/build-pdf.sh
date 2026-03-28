#!/bin/bash
# build-pdf.sh — Genera i PDF di I Lupi dell'Assia
# Uso: bash scripts/build-pdf.sh [modulo-base|pregenerati|supplemento|all]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

MODULE="${1:-all}"

echo "════════════════════════════════════════════"
echo "  I Lupi dell'Assia — Build PDF"
echo "  Modulo: $MODULE"
echo "════════════════════════════════════════════"

python3 "$SCRIPT_DIR/assemble.py" "$MODULE"

echo ""
echo "File generati in: $ROOT_DIR/output/"
ls -la "$ROOT_DIR/output/"*.pdf 2>/dev/null || echo "(nessun PDF)"
