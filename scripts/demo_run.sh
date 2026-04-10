#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE_DIR"

echo "[1/3] Starting TALASH API on http://127.0.0.1:8000"
uvicorn app.main:app --reload &
API_PID=$!
trap 'kill $API_PID >/dev/null 2>&1 || true' EXIT
sleep 2

echo "[2/3] Processing all PDFs in data/input"
curl -sS -X POST "http://127.0.0.1:8000/process/all" | cat

echo "[3/3] Fetching preprocessing report"
curl -sS "http://127.0.0.1:8000/results/report" | cat

echo "Demo run complete."
